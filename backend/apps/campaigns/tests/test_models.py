"""Tests for Campaign model."""

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from apps.campaigns.models import Campaign, CampaignStatus, CampaignType


class CampaignModelTest(TestCase):
    """Test cases for Campaign model."""

    def setUp(self):
        """Set up test fixtures."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )

    def test_campaign_creation(self):
        """Test creating a campaign."""
        campaign = Campaign.objects.create(
            name="Test Campaign",
            campaign_type=CampaignType.MARKET_RESEARCH,
            target_industry="Technology",
            target_region="North America",
            offer="Market research data",
            owner=self.user,
        )
        self.assertIsNotNone(campaign.id)
        self.assertEqual(campaign.status, CampaignStatus.DRAFT)
        self.assertEqual(campaign.owner, self.user)

    def test_campaign_creation_defaults(self):
        """Test campaign default values."""
        campaign = Campaign.objects.create(
            name="Test Campaign",
            campaign_type=CampaignType.SURVEY,
            target_industry="Finance",
            target_region="Europe",
            offer="Survey participation",
            owner=self.user,
        )
        self.assertTrue(campaign.requires_approval)
        self.assertEqual(campaign.sequence_length, 4)
        self.assertEqual(campaign.status, CampaignStatus.DRAFT)

    def test_valid_state_transitions(self):
        """Test valid campaign state transitions."""
        campaign = Campaign.objects.create(
            name="Test Campaign",
            campaign_type=CampaignType.SURVEY,
            target_industry="Healthcare",
            target_region="US",
            offer="Healthcare survey",
            owner=self.user,
        )

        # draft → pending_approval
        campaign.transition_to(CampaignStatus.PENDING_APPROVAL)
        self.assertEqual(campaign.status, CampaignStatus.PENDING_APPROVAL)

        # pending_approval → active
        campaign.transition_to(CampaignStatus.ACTIVE)
        self.assertEqual(campaign.status, CampaignStatus.ACTIVE)

        # active → paused
        campaign.transition_to(CampaignStatus.PAUSED)
        self.assertEqual(campaign.status, CampaignStatus.PAUSED)

        # paused → active
        campaign.transition_to(CampaignStatus.ACTIVE)
        self.assertEqual(campaign.status, CampaignStatus.ACTIVE)

        # active → completed
        campaign.transition_to(CampaignStatus.COMPLETED)
        self.assertEqual(campaign.status, CampaignStatus.COMPLETED)

        # completed → archived
        campaign.transition_to(CampaignStatus.ARCHIVED)
        self.assertEqual(campaign.status, CampaignStatus.ARCHIVED)

    def test_invalid_state_transition_raises(self):
        """Test that invalid state transitions raise ValueError."""
        campaign = Campaign.objects.create(
            name="Test Campaign",
            campaign_type=CampaignType.WEBINAR,
            target_industry="Education",
            target_region="Global",
            offer="Webinar participation",
            owner=self.user,
        )

        # draft → completed (invalid)
        with self.assertRaises(ValueError):
            campaign.transition_to(CampaignStatus.COMPLETED)

        # draft → paused (invalid)
        with self.assertRaises(ValueError):
            campaign.transition_to(CampaignStatus.PAUSED)

    def test_archived_no_transitions(self):
        """Test that archived campaigns cannot transition."""
        campaign = Campaign.objects.create(
            name="Test Campaign",
            campaign_type=CampaignType.SURVEY,
            target_industry="Tech",
            target_region="US",
            offer="Tech survey",
            owner=self.user,
            status=CampaignStatus.ARCHIVED,
        )

        # Try to transition from archived
        with self.assertRaises(ValueError):
            campaign.transition_to(CampaignStatus.ACTIVE)

    def test_campaign_validation_sequence_length(self):
        """Test sequence length validation."""
        campaign = Campaign.objects.create(
            name="Test Campaign",
            campaign_type=CampaignType.SURVEY,
            target_industry="Tech",
            target_region="US",
            offer="Tech survey",
            owner=self.user,
            sequence_length=0,
        )

        with self.assertRaises(ValidationError):
            campaign.full_clean()

        campaign.sequence_length = 13
        with self.assertRaises(ValidationError):
            campaign.full_clean()

        campaign.sequence_length = 5
        campaign.full_clean()  # Should not raise

    def test_draft_to_active_direct(self):
        """Test direct transition from draft to active."""
        campaign = Campaign.objects.create(
            name="Test Campaign",
            campaign_type=CampaignType.SURVEY,
            target_industry="Tech",
            target_region="US",
            offer="Tech survey",
            owner=self.user,
        )

        campaign.transition_to(CampaignStatus.ACTIVE)
        self.assertEqual(campaign.status, CampaignStatus.ACTIVE)

    def test_pending_approval_back_to_draft(self):
        """Test rejection flow: pending_approval → draft."""
        campaign = Campaign.objects.create(
            name="Test Campaign",
            campaign_type=CampaignType.SURVEY,
            target_industry="Tech",
            target_region="US",
            offer="Tech survey",
            owner=self.user,
        )

        campaign.transition_to(CampaignStatus.PENDING_APPROVAL)
        campaign.transition_to(CampaignStatus.DRAFT)
        self.assertEqual(campaign.status, CampaignStatus.DRAFT)
