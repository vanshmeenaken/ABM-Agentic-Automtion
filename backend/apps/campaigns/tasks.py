"""
Celery tasks for Campaign operations.
Async operations related to campaign management.
"""

from celery import shared_task
from django.utils import timezone
from apps.campaigns.models import Campaign
from apps.audit.utils import log_audit_event


@shared_task(bind=True, max_retries=3)
def run_campaign_planner_task(self, campaign_id: str):
    """
    Async version of campaign planner agent run.
    Used for batch processing or scheduled execution.

    Args:
        campaign_id: UUID of the campaign
    """
    try:
        campaign = Campaign.objects.get(id=campaign_id)

        # This would be used for batch processing in future
        # For now, it's a placeholder for Phase 12 enhancements

        log_audit_event(
            action="campaign_planner_task_executed",
            campaign=campaign,
            actor_system="celery-worker",
            payload={"campaign_id": str(campaign.id)}
        )
    except Campaign.DoesNotExist:
        log_audit_event(
            action="campaign_planner_task_failed",
            status="failure",
            actor_system="celery-worker",
            failure_reason=f"Campaign {campaign_id} not found"
        )
    except Exception as e:
        log_audit_event(
            action="campaign_planner_task_failed",
            status="failure",
            actor_system="celery-worker",
            failure_reason=str(e)
        )
        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=60 * (2 ** self.request.retries))


@shared_task(bind=True)
def enable_campaign_sequences(self, campaign_id: str):
    """
    Enable sequences for an active campaign.
    Called when campaign is activated or resumed.
    Placeholder for Phase 12 Sequence Orchestrator.

    Args:
        campaign_id: UUID of the campaign
    """
    try:
        campaign = Campaign.objects.get(id=campaign_id)

        # Phase 12: This will trigger sequence generation and scheduling
        # For now, just log the event

        log_audit_event(
            action="campaign_sequences_enabled",
            campaign=campaign,
            actor_system="celery-worker",
            payload={
                "campaign_id": str(campaign.id),
                "enabled_at": timezone.now().isoformat()
            }
        )
    except Campaign.DoesNotExist:
        log_audit_event(
            action="campaign_sequences_enable_failed",
            status="failure",
            actor_system="celery-worker",
            failure_reason=f"Campaign {campaign_id} not found"
        )
    except Exception as e:
        log_audit_event(
            action="campaign_sequences_enable_failed",
            status="failure",
            actor_system="celery-worker",
            failure_reason=str(e)
        )


@shared_task(bind=True)
def disable_campaign_sequences(self, campaign_id: str):
    """
    Disable sequences for a campaign.
    Called when campaign is paused.
    Placeholder for Phase 12 Sequence Orchestrator.

    Args:
        campaign_id: UUID of the campaign
    """
    try:
        campaign = Campaign.objects.get(id=campaign_id)

        # Phase 12: This will stop all running sequences

        log_audit_event(
            action="campaign_sequences_disabled",
            campaign=campaign,
            actor_system="celery-worker",
            payload={
                "campaign_id": str(campaign.id),
                "disabled_at": timezone.now().isoformat()
            }
        )
    except Campaign.DoesNotExist:
        log_audit_event(
            action="campaign_sequences_disable_failed",
            status="failure",
            actor_system="celery-worker",
            failure_reason=f"Campaign {campaign_id} not found"
        )
    except Exception as e:
        log_audit_event(
            action="campaign_sequences_disable_failed",
            status="failure",
            actor_system="celery-worker",
            failure_reason=str(e)
        )


@shared_task(bind=True)
def check_pending_campaigns(self):
    """
    Periodic task to check for pending campaigns that may need attention.
    Runs every 4 hours via Celery Beat.
    """
    from apps.campaigns.models import CampaignStatus

    pending_campaigns = Campaign.objects.filter(
        status=CampaignStatus.PENDING_APPROVAL
    ).count()

    log_audit_event(
        action="pending_campaigns_check",
        actor_system="celery-beat",
        payload={"pending_count": pending_campaigns}
    )
