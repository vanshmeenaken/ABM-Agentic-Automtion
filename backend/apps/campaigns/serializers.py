"""
Serializers for Campaign API endpoints.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from apps.campaigns.models import Campaign, CampaignType, CampaignStatus


class CampaignCreateSerializer(serializers.Serializer):
    """
    Input serializer for creating a new campaign.
    Validates user input for campaign creation.
    """

    campaign_name = serializers.CharField(
        max_length=255,
        help_text="Name of the campaign"
    )
    target_industry = serializers.CharField(
        max_length=100,
        help_text="Target industry"
    )
    target_region = serializers.CharField(
        max_length=100,
        help_text="Target geographic region"
    )
    offer = serializers.CharField(
        help_text="Campaign offer/value proposition"
    )
    campaign_type = serializers.ChoiceField(
        choices=CampaignType.choices,
        help_text="Type of campaign"
    )
    preferred_channels = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True,
        help_text="Preferred communication channels (email, linkedin, whatsapp)"
    )
    notes = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Additional notes or context"
    )
    success_metric = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="How success will be measured"
    )
    requires_approval = serializers.BooleanField(
        default=True,
        help_text="Whether campaign requires approval before activation"
    )


class CampaignDetailSerializer(serializers.ModelSerializer):
    """
    Full campaign detail serializer.
    Returns all campaign fields including agent outputs.
    """

    owner_email = serializers.EmailField(
        source="owner.email",
        read_only=True
    )
    owner_name = serializers.CharField(
        source="owner.get_full_name",
        read_only=True
    )
    approved_by_email = serializers.EmailField(
        source="approved_by.email",
        read_only=True,
        allow_null=True
    )
    approved_by_name = serializers.CharField(
        source="approved_by.get_full_name",
        read_only=True,
        allow_null=True
    )
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True
    )
    campaign_type_display = serializers.CharField(
        source="get_campaign_type_display",
        read_only=True
    )

    class Meta:
        model = Campaign
        fields = [
            "id",
            "name",
            "campaign_type",
            "campaign_type_display",
            "target_industry",
            "target_region",
            "target_persona",
            "offer",
            "channel_mix",
            "sequence_length",
            "success_metric",
            "requires_approval",
            "status",
            "status_display",
            "owner",
            "owner_email",
            "owner_name",
            "icp_definition",
            "persona_map",
            "channel_plan",
            "confidence_notes",
            "agent_run_id",
            "approved_by",
            "approved_by_email",
            "approved_by_name",
            "approved_at",
            "rejection_note",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "icp_definition",
            "persona_map",
            "channel_plan",
            "confidence_notes",
            "agent_run_id",
            "approved_by",
            "approved_by_email",
            "approved_by_name",
            "approved_at",
            "created_at",
            "updated_at",
        ]


class CampaignListSerializer(serializers.ModelSerializer):
    """
    Summary list serializer for campaign listings.
    Returns key fields only for list views.
    """

    owner_email = serializers.EmailField(
        source="owner.email",
        read_only=True
    )
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True
    )
    campaign_type_display = serializers.CharField(
        source="get_campaign_type_display",
        read_only=True
    )

    class Meta:
        model = Campaign
        fields = [
            "id",
            "name",
            "campaign_type",
            "campaign_type_display",
            "target_industry",
            "status",
            "status_display",
            "owner",
            "owner_email",
            "created_at",
        ]


class CampaignApproveSerializer(serializers.Serializer):
    """Input serializer for campaign approval."""

    pass  # No additional fields needed for approval


class CampaignRejectSerializer(serializers.Serializer):
    """Input serializer for campaign rejection."""

    rejection_note = serializers.CharField(
        help_text="Reason for rejection"
    )


class CampaignStateChangeSerializer(serializers.Serializer):
    """Input serializer for campaign state changes."""

    pass  # No additional fields needed for pause/resume
