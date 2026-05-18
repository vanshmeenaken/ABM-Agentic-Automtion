"""
Django admin configuration for Campaigns app.
"""

from django.contrib import admin
from django.utils.html import format_html
from apps.campaigns.models import Campaign


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    """Admin interface for Campaign model."""

    list_display = (
        "name",
        "campaign_type",
        "status_badge",
        "owner",
        "target_industry",
        "created_at",
    )
    list_filter = (
        "status",
        "campaign_type",
        "created_at",
        "requires_approval",
    )
    search_fields = (
        "name",
        "target_industry",
        "target_region",
        "owner__username",
    )
    ordering = ("-created_at",)
    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Campaign Information",
            {
                "fields": (
                    "id",
                    "name",
                    "campaign_type",
                    "target_industry",
                    "target_region",
                    "target_persona",
                    "offer",
                )
            }
        ),
        (
            "Configuration",
            {
                "fields": (
                    "channel_mix",
                    "sequence_length",
                    "success_metric",
                    "requires_approval",
                )
            }
        ),
        (
            "Ownership & Status",
            {
                "fields": (
                    "owner",
                    "status",
                    "created_at",
                    "updated_at",
                )
            }
        ),
        (
            "Agent Output",
            {
                "classes": ("collapse",),
                "fields": (
                    "agent_run_id",
                    "icp_definition",
                    "persona_map",
                    "channel_plan",
                    "confidence_notes",
                ),
            }
        ),
        (
            "Approval Workflow",
            {
                "classes": ("collapse",),
                "fields": (
                    "approved_by",
                    "approved_at",
                    "rejection_note",
                ),
            }
        ),
    )

    readonly_fields = (
        "id",
        "icp_definition",
        "persona_map",
        "channel_plan",
        "confidence_notes",
        "agent_run_id",
        "created_at",
        "updated_at",
    )

    def status_badge(self, obj):
        """Display status with color coding."""
        colors = {
            "draft": "#FFA500",  # Orange
            "pending_approval": "#FFD700",  # Gold
            "active": "#00AA00",  # Green
            "paused": "#FF6347",  # Red
            "completed": "#87CEEB",  # Sky Blue
            "archived": "#696969",  # Dark Gray
        }
        color = colors.get(obj.status, "#CCCCCC")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )

    status_badge.short_description = "Status"

    def get_queryset(self, request):
        """Exclude archived campaigns by default."""
        qs = super().get_queryset(request)
        return qs.exclude(status="archived")

    actions = ["mark_active", "mark_paused"]

    def mark_active(self, request, queryset):
        """Admin action to mark campaigns as active."""
        from apps.campaigns.models import CampaignStatus

        count = 0
        for campaign in queryset:
            if campaign.status in ["draft", "paused"]:
                try:
                    campaign.transition_to(CampaignStatus.ACTIVE)
                    count += 1
                except ValueError:
                    pass

        self.message_user(request, f"{count} campaign(s) marked as active.")

    mark_active.short_description = "Mark selected campaigns as active"

    def mark_paused(self, request, queryset):
        """Admin action to mark campaigns as paused."""
        from apps.campaigns.models import CampaignStatus

        count = 0
        for campaign in queryset:
            if campaign.status == "active":
                try:
                    campaign.transition_to(CampaignStatus.PAUSED)
                    count += 1
                except ValueError:
                    pass

        self.message_user(request, f"{count} campaign(s) marked as paused.")

    mark_paused.short_description = "Mark selected campaigns as paused"
