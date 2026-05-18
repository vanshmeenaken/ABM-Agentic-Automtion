"""
Celery configuration for Ken ABM Platform.
"""

import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("ken_abm_platform")

# Load configuration from Django settings with CELERY namespace
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from all registered Django apps
app.autodiscover_tasks()

# Optional: Define periodic tasks with Celery Beat
app.conf.beat_schedule = {
    "check-pending-campaigns": {
        "task": "apps.campaigns.tasks.check_pending_campaigns",
        "schedule": crontab(minute=0, hour="*/4"),  # Every 4 hours
    },
}

@app.task(bind=True)
def debug_task(self):
    """Debug task for testing Celery connectivity."""
    print(f"Request: {self.request!r}")
