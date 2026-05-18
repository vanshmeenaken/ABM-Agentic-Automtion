"""Governance models - stub for policy and compliance management."""
from apps.core.models import TimeStampedModel

class Policy(TimeStampedModel):
    """Placeholder for Policy model."""
    class Meta:
        abstract = True
