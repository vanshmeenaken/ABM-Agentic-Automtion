"""URL routes for Agent APIs."""

from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    PersonaClassifierViewSet,
    MessageStrategyViewSet,
    EmailCopyViewSet,
    WhatsAppCopyViewSet,
    LinkedInCopyViewSet,
    ComplianceReviewViewSet,
    ReplyClassifierViewSet,
)

router = DefaultRouter()
router.register(r"agents/persona-classifier", PersonaClassifierViewSet, basename="persona-classifier")
router.register(r"agents/message-strategy", MessageStrategyViewSet, basename="message-strategy")
router.register(r"agents/email-copy", EmailCopyViewSet, basename="email-copy")
router.register(r"agents/whatsapp-copy", WhatsAppCopyViewSet, basename="whatsapp-copy")
router.register(r"agents/linkedin-copy", LinkedInCopyViewSet, basename="linkedin-copy")
router.register(r"agents/compliance-review", ComplianceReviewViewSet, basename="compliance-review")
router.register(r"agents/reply-classifier", ReplyClassifierViewSet, basename="reply-classifier")

urlpatterns = router.urls
