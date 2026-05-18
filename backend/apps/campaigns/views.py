"""
Views for Campaign API endpoints.
Implements WF-001 Campaign Creation Workflow.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db import transaction

from apps.campaigns.models import Campaign, CampaignStatus
from apps.campaigns.serializers import (
    CampaignCreateSerializer,
    CampaignDetailSerializer,
    CampaignListSerializer,
    CampaignApproveSerializer,
    CampaignRejectSerializer,
)
from apps.campaigns.permissions import CampaignPermission, CanApproveCampaigns, CanManageCampaign
from apps.campaigns.tasks import enable_campaign_sequences, disable_campaign_sequences
from apps.audit.utils import log_audit_event
from apps.core.exceptions import AgentFailureException

# Import agent from wherever it's located
try:
    from agents.campaign_planner_agent import run_campaign_planner
except ImportError:
    run_campaign_planner = None


class CampaignViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing campaigns.
    Implements the full campaign lifecycle with approval workflow.
    """

    permission_classes = [IsAuthenticated, CampaignPermission]
    queryset = Campaign.objects.exclude(status=CampaignStatus.ARCHIVED)

    def get_serializer_class(self):
        if self.action == "create":
            return CampaignCreateSerializer
        elif self.action == "list":
            return CampaignListSerializer
        return CampaignDetailSerializer

    def create(self, request):
        """
        POST /api/v1/campaigns/

        WF-001 Campaign Creation Workflow:
        1. Validate input
        2. Run Campaign Planner Agent
        3. Save campaign draft
        4. Route to approval or activate
        5. Log audit event
        """
        # Step 1: Validate input
        serializer = CampaignCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Step 2: Run Campaign Planner Agent
        if not run_campaign_planner:
            log_audit_event(
                action="campaign_creation_failed",
                status="failure",
                actor_user=request.user,
                failure_reason="Campaign Planner Agent not available"
            )
            raise AgentFailureException("Campaign Planner Agent is not available.")

        try:
            agent_output = run_campaign_planner(
                campaign_name=data["campaign_name"],
                target_industry=data["target_industry"],
                target_region=data["target_region"],
                offer=data["offer"],
                campaign_type=data["campaign_type"],
                preferred_channels=data.get("preferred_channels"),
                notes=data.get("notes"),
            )
        except Exception as e:
            log_audit_event(
                action="campaign_planner_agent_failed",
                status="failure",
                actor_user=request.user,
                failure_reason=str(e)
            )
            raise AgentFailureException(f"Campaign Planner Agent failed: {str(e)}")

        # Step 3: Save campaign draft
        with transaction.atomic():
            campaign = Campaign.objects.create(
                name=agent_output.campaign_draft.name,
                campaign_type=agent_output.campaign_draft.campaign_type,
                target_industry=agent_output.campaign_draft.target_industry,
                target_region=agent_output.campaign_draft.target_region,
                offer=agent_output.campaign_draft.offer,
                icp_definition=agent_output.icp_definition.model_dump(),
                persona_map=[p.model_dump() for p in agent_output.persona_map],
                channel_plan=agent_output.channel_plan.model_dump(),
                confidence_notes=agent_output.confidence_notes,
                requires_approval=data.get("requires_approval", True),
                success_metric=data.get("success_metric", ""),
                owner=request.user,
                status=CampaignStatus.DRAFT,
            )

            # Log campaign created event
            log_audit_event(
                action="campaign_created",
                campaign=campaign,
                actor_user=request.user,
                payload={
                    "campaign_id": str(campaign.id),
                    "campaign_type": campaign.campaign_type,
                }
            )

            # Step 4: Route to approval or activate
            if campaign.requires_approval:
                campaign.transition_to(CampaignStatus.PENDING_APPROVAL)
                log_audit_event(
                    action="campaign_pending_approval",
                    campaign=campaign,
                    actor_user=request.user
                )
            else:
                campaign.transition_to(CampaignStatus.ACTIVE)
                enable_campaign_sequences.delay(str(campaign.id))
                log_audit_event(
                    action="campaign_activated",
                    campaign=campaign,
                    actor_user=request.user
                )

        return Response(
            CampaignDetailSerializer(campaign).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, CanApproveCampaigns])
    def approve(self, request, pk=None):
        """
        POST /api/v1/campaigns/{id}/approve/

        Approve a pending campaign and activate it.
        """
        campaign = self.get_object()

        # Validate current status
        if campaign.status != CampaignStatus.PENDING_APPROVAL:
            return Response(
                {"error": f"Campaign must be in pending_approval status. Current: {campaign.status}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            campaign.approved_by = request.user
            campaign.approved_at = timezone.now()
            campaign.save(update_fields=["approved_by", "approved_at"])

            campaign.transition_to(CampaignStatus.ACTIVE)
            enable_campaign_sequences.delay(str(campaign.id))

            log_audit_event(
                action="campaign_approved",
                campaign=campaign,
                actor_user=request.user,
                payload={"approved_by": request.user.email}
            )

        return Response(CampaignDetailSerializer(campaign).data)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, CanApproveCampaigns])
    def reject(self, request, pk=None):
        """
        POST /api/v1/campaigns/{id}/reject/

        Reject a pending campaign and return to draft.
        """
        serializer = CampaignRejectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        campaign = self.get_object()

        # Validate current status
        if campaign.status != CampaignStatus.PENDING_APPROVAL:
            return Response(
                {"error": f"Campaign must be in pending_approval status. Current: {campaign.status}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            campaign.rejection_note = serializer.validated_data["rejection_note"]
            campaign.save(update_fields=["rejection_note"])

            campaign.transition_to(CampaignStatus.DRAFT)

            log_audit_event(
                action="campaign_rejected",
                campaign=campaign,
                actor_user=request.user,
                payload={"rejection_note": campaign.rejection_note}
            )

        return Response(CampaignDetailSerializer(campaign).data)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, CanManageCampaign])
    def pause(self, request, pk=None):
        """
        POST /api/v1/campaigns/{id}/pause/

        Pause an active campaign.
        """
        campaign = self.get_object()

        if campaign.status != CampaignStatus.ACTIVE:
            return Response(
                {"error": f"Campaign must be active. Current: {campaign.status}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            campaign.transition_to(CampaignStatus.PAUSED)
            disable_campaign_sequences.delay(str(campaign.id))

            log_audit_event(
                action="campaign_paused",
                campaign=campaign,
                actor_user=request.user
            )

        return Response(CampaignDetailSerializer(campaign).data)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, CanManageCampaign])
    def resume(self, request, pk=None):
        """
        POST /api/v1/campaigns/{id}/resume/

        Resume a paused campaign.
        """
        campaign = self.get_object()

        if campaign.status != CampaignStatus.PAUSED:
            return Response(
                {"error": f"Campaign must be paused. Current: {campaign.status}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            campaign.transition_to(CampaignStatus.ACTIVE)
            enable_campaign_sequences.delay(str(campaign.id))

            log_audit_event(
                action="campaign_resumed",
                campaign=campaign,
                actor_user=request.user
            )

        return Response(CampaignDetailSerializer(campaign).data)
