"""Django admin configuration for Audit app."""

from django.contrib import admin
from apps.audit.models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Admin interface for AuditLog model."""

    list_display = (
        "action",
        "status",
        "actor_user",
        "actor_system",
        "campaign",
        "created_at",
    )
    list_filter = (
        "status",
        "action",
        "created_at",
        "actor_system",
    )
    search_fields = (
        "action",
        "actor_user__username",
        "actor_system",
        "failure_reason",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "payload",
    )
    ordering = ("-created_at",)
    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Actor Information",
            {
                "fields": (
                    "actor_user",
                    "actor_system",
                )
            }
        ),
        (
            "Action Details",
            {
                "fields": (
                    "action",
                    "status",
                    "channel",
                )
            }
        ),
        (
            "Related Objects",
            {
                "fields": (
                    "campaign",
                    "prospect",
                )
            }
        ),
        (
            "Payload & Errors",
            {
                "classes": ("collapse",),
                "fields": (
                    "payload",
                    "failure_reason",
                ),
            }
        ),
        (
            "Timestamps",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            }
        ),
    )
