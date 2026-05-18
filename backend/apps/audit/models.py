"""
Audit logging models for Ken ABM Platform.
Tracks all user actions, system events, and state changes.
"""

from django.db import models
from django.contrib.auth.models import User
from apps.core.models import TimeStampedModel


class AuditLog(TimeStampedModel):
    """
    Comprehensive audit log for tracking all platform activities.
    Every user action and system event is recorded here for compliance and debugging.
    """

    STATUS_CHOICES = (
        ("success", "Success"),
        ("failure", "Failure"),
        ("warning", "Warning"),
    )

    # Actor information
    actor_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="audit_logs_created",
        help_text="User who performed the action"
    )
    actor_system = models.CharField(
        max_length=100,
        blank=True,
        help_text="System/service that performed the action (e.g., 'celery-worker', 'scheduler')"
    )

    # Related objects
    campaign = models.ForeignKey(
        "campaigns.Campaign",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="audit_logs"
    )
    prospect = models.ForeignKey(
        "prospects.Prospect",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="audit_logs"
    )

    # Action details
    action = models.CharField(
        max_length=100,
        help_text="Action performed (e.g., 'campaign_created', 'campaign_approved')"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="success"
    )
    channel = models.CharField(
        max_length=50,
        blank=True,
        help_text="Channel used (e.g., 'email', 'linkedin', 'api')"
    )

    # Payload and error information
    payload = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional context data in JSON format"
    )
    failure_reason = models.TextField(
        blank=True,
        help_text="Error message if status is 'failure'"
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["action", "-created_at"]),
            models.Index(fields=["actor_user", "-created_at"]),
            models.Index(fields=["campaign", "-created_at"]),
            models.Index(fields=["status", "-created_at"]),
        ]

    def __str__(self):
        actor = self.actor_user.username if self.actor_user else self.actor_system
        return f"{self.action} by {actor} at {self.created_at}"
