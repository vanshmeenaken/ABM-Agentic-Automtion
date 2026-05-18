"""
Audit logging utilities for Ken ABM Platform.
Provides convenient helper functions for logging events.
"""

from typing import Optional, Dict, Any
from django.contrib.auth.models import User
from apps.audit.models import AuditLog


def log_audit_event(
    action: str,
    status: str = "success",
    actor_user: Optional[User] = None,
    actor_system: str = "",
    campaign = None,
    prospect = None,
    channel: str = "",
    payload: Optional[Dict[str, Any]] = None,
    failure_reason: str = "",
) -> AuditLog:
    """
    Log an audit event to the database.

    Args:
        action: Description of the action (e.g., 'campaign_created')
        status: One of 'success', 'failure', 'warning' (default: 'success')
        actor_user: Django User object who performed the action
        actor_system: Name of system/service that performed the action
        campaign: Campaign object involved in the action
        prospect: Prospect object involved in the action
        channel: Communication channel used (e.g., 'email')
        payload: Additional context data as dict
        failure_reason: Error message if status is 'failure'

    Returns:
        AuditLog: The created audit log entry
    """
    if payload is None:
        payload = {}

    audit_log = AuditLog.objects.create(
        action=action,
        status=status,
        actor_user=actor_user,
        actor_system=actor_system,
        campaign=campaign,
        prospect=prospect,
        channel=channel,
        payload=payload,
        failure_reason=failure_reason,
    )

    return audit_log
