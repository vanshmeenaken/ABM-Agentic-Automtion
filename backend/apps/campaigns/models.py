"""
Campaign models for Ken ABM Platform.
Core data models for campaign management and workflow.
"""

import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from apps.core.models import TimeStampedModel


class CampaignStatus(models.TextChoices):
    """Campaign workflow states."""
    DRAFT = "draft", "Draft"
    PENDING_APPROVAL = "pending_approval", "Pending Approval"
    ACTIVE = "active", "Active"
    PAUSED = "paused", "Paused"
    COMPLETED = "completed", "Completed"
    ARCHIVED = "archived", "Archived"


class CampaignType(models.TextChoices):
    """Campaign types."""
    MARKET_RESEARCH = "Market Research", "Market Research"
    SURVEY = "Survey", "Survey"
    CONSULTING = "Consulting", "Consulting"
    EXPERT_NETWORK = "Expert Network", "Expert Network"
    WEBINAR = "Webinar", "Webinar"
    REPORT_SALES = "Report Sales", "Report Sales"
    COMPETITION_BENCHMARKING = "Competition Benchmarking", "Competition Benchmarking"
    ACCOUNT_REACTIVATION = "Account Reactivation", "Account Reactivation"


class Campaign(TimeStampedModel):
    """
    Campaign model representing an ABM campaign.
    Manages the entire lifecycle from creation through completion.
    """

    # Unique identifier
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Core campaign information
    name = models.CharField(
        max_length=255,
        help_text="Campaign name"
    )
    campaign_type = models.CharField(
        max_length=50,
        choices=CampaignType.choices,
        help_text="Type of campaign"
    )
    target_industry = models.CharField(
        max_length=100,
        help_text="Target industry for the campaign"
    )
    target_region = models.CharField(
        max_length=100,
        help_text="Target geographic region"
    )
    target_persona = models.CharField(
        max_length=100,
        blank=True,
        help_text="Primary target persona/role"
    )
    offer = models.TextField(
        help_text="Campaign offer/value proposition"
    )

    # Campaign configuration
    channel_mix = models.JSONField(
        default=list,
        blank=True,
        help_text="List of channels to use (email, linkedin, etc)"
    )
    sequence_length = models.IntegerField(
        default=4,
        help_text="Number of touches in sequence"
    )
    success_metric = models.CharField(
        max_length=100,
        blank=True,
        help_text="How success is measured for this campaign"
    )
    requires_approval = models.BooleanField(
        default=True,
        help_text="Whether campaign requires approval before activation"
    )

    # Ownership and status
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="owned_campaigns",
        help_text="User who created the campaign"
    )
    status = models.CharField(
        max_length=30,
        choices=CampaignStatus.choices,
        default=CampaignStatus.DRAFT,
        help_text="Current campaign status"
    )

    # Agent output fields (populated by Campaign Planner Agent)
    icp_definition = models.JSONField(
        default=dict,
        blank=True,
        help_text="ICP definition from agent (positive/negative criteria)"
    )
    persona_map = models.JSONField(
        default=list,
        blank=True,
        help_text="Persona definitions from agent"
    )
    channel_plan = models.JSONField(
        default=dict,
        blank=True,
        help_text="Channel plan from agent"
    )
    confidence_notes = models.TextField(
        blank=True,
        help_text="Agent confidence and reasoning notes"
    )
    agent_run_id = models.UUIDField(
        null=True,
        blank=True,
        help_text="ID of agent run that generated this campaign"
    )

    # Approval workflow fields
    approved_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="approved_campaigns",
        help_text="User who approved the campaign"
    )
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp of approval"
    )
    rejection_note = models.TextField(
        blank=True,
        help_text="Reason for rejection if campaign was rejected"
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "-created_at"]),
            models.Index(fields=["owner", "-created_at"]),
            models.Index(fields=["campaign_type", "status"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    def clean(self):
        """Validate campaign data."""
        if self.sequence_length < 1 or self.sequence_length > 12:
            raise ValidationError(
                {"sequence_length": "Sequence length must be between 1 and 12."}
            )

    def transition_to(self, new_status: str, actor: User = None) -> None:
        """
        Transition campaign to a new status.
        Enforces valid state machine transitions.

        Args:
            new_status: Target status
            actor: User performing the transition

        Raises:
            ValueError: If transition is invalid
        """
        VALID_TRANSITIONS = {
            CampaignStatus.DRAFT: [
                CampaignStatus.PENDING_APPROVAL,
                CampaignStatus.ACTIVE,
            ],
            CampaignStatus.PENDING_APPROVAL: [
                CampaignStatus.ACTIVE,
                CampaignStatus.DRAFT,
            ],
            CampaignStatus.ACTIVE: [
                CampaignStatus.PAUSED,
                CampaignStatus.COMPLETED,
            ],
            CampaignStatus.PAUSED: [CampaignStatus.ACTIVE],
            CampaignStatus.COMPLETED: [CampaignStatus.ARCHIVED],
            CampaignStatus.ARCHIVED: [],
        }

        allowed_transitions = VALID_TRANSITIONS.get(self.status, [])
        if new_status not in allowed_transitions:
            raise ValueError(
                f"Invalid transition: {self.status} → {new_status}. "
                f"Allowed: {allowed_transitions}"
            )

        self.status = new_status
        self.save(update_fields=["status", "updated_at"])
