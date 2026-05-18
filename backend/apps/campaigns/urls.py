"""
URL routing for Campaign API endpoints.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.campaigns.views import CampaignViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r"campaigns", CampaignViewSet, basename="campaign")

urlpatterns = [
    path("", include(router.urls)),
]

# Generated URLs:
# GET    /api/v1/campaigns/                    - List campaigns
# POST   /api/v1/campaigns/                    - Create campaign
# GET    /api/v1/campaigns/{id}/               - Get campaign detail
# PUT    /api/v1/campaigns/{id}/               - Update campaign (full)
# PATCH  /api/v1/campaigns/{id}/               - Partial update
# DELETE /api/v1/campaigns/{id}/               - Delete campaign
# POST   /api/v1/campaigns/{id}/approve/       - Approve campaign
# POST   /api/v1/campaigns/{id}/reject/        - Reject campaign
# POST   /api/v1/campaigns/{id}/pause/         - Pause campaign
# POST   /api/v1/campaigns/{id}/resume/        - Resume campaign
