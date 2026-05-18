"""Integration tests for Campaign Planner Agent."""

import os
import pytest
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from apps.campaigns.models import Campaign, CampaignStatus, CampaignType
from apps.audit.models import AuditLog


@pytest.mark.skipif(
    not os.getenv("ANTHROPIC_API_KEY"),
    reason="Requires ANTHROPIC_API_KEY environment variable"
)
class CampaignPlannerAgentIntegrationTest(TestCase):
    """Integration tests for Campaign Planner Agent."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )

    def test_agent_failure_logged_to_audit(self):
        """Test that agent failures are logged to AuditLog."""
        # Note: This test uses mocking to avoid real API calls in CI
        from unittest.mock import patch

        with patch("apps.campaigns.views.run_campaign_planner") as mock_agent:
            mock_agent.side_effect = Exception("Agent connection failed")

            self.client.force_authenticate(user=self.user)
            data = {
                "campaign_name": "Test Campaign",
                "target_industry": "Technology",
                "target_region": "North America",
                "offer": "Test offer",
                "campaign_type": CampaignType.SURVEY,
            }

            response = self.client.post("/api/v1/campaigns/", data, format="json")
            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Check that failure was logged
            audit_logs = AuditLog.objects.filter(
                action="campaign_planner_agent_failed",
                status="failure"
            )
            self.assertEqual(audit_logs.count(), 1)
            self.assertIn("Agent connection failed", audit_logs.first().failure_reason)

    def test_agent_runs_successfully_with_mock(self):
        """Test successful agent run with mocked output."""
        from unittest.mock import patch, MagicMock
        from agents.schemas import CampaignPlannerOutput

        mock_output = MagicMock(spec=CampaignPlannerOutput)
        mock_output.campaign_draft.name = "Tech Market Research"
        mock_output.campaign_draft.campaign_type = CampaignType.MARKET_RESEARCH
        mock_output.campaign_draft.target_industry = "Technology"
        mock_output.campaign_draft.target_region = "North America"
        mock_output.campaign_draft.offer = "Market research data"
        mock_output.icp_definition.model_dump.return_value = {
            "positive": {},
            "negative": {}
        }
        mock_output.persona_map = []
        mock_output.channel_plan.model_dump.return_value = {"channels": []}
        mock_output.confidence_notes = "High confidence"

        with patch("apps.campaigns.views.run_campaign_planner") as mock_agent:
            mock_agent.return_value = mock_output

            self.client.force_authenticate(user=self.user)
            data = {
                "campaign_name": "Tech Campaign",
                "target_industry": "Technology",
                "target_region": "North America",
                "offer": "Market research",
                "campaign_type": CampaignType.MARKET_RESEARCH,
            }

            response = self.client.post("/api/v1/campaigns/", data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            # Verify campaign was created
            self.assertEqual(Campaign.objects.count(), 1)
            campaign = Campaign.objects.first()
            self.assertEqual(campaign.name, "Tech Market Research")

            # Verify audit log
            audit_logs = AuditLog.objects.filter(action="campaign_created")
            self.assertEqual(audit_logs.count(), 1)
            self.assertEqual(audit_logs.first().actor_user, self.user)

    def test_agent_output_persisted_to_database(self):
        """Test that agent output is correctly persisted."""
        from unittest.mock import patch, MagicMock
        from agents.schemas import (
            CampaignPlannerOutput,
            CampaignDraft,
            ICPDefinition,
            PersonaItem,
            ChannelPlan,
        )

        # Create mock objects
        campaign_draft = MagicMock(spec=CampaignDraft)
        campaign_draft.name = "AI Insights Campaign"
        campaign_draft.campaign_type = CampaignType.SURVEY
        campaign_draft.target_industry = "AI/ML"
        campaign_draft.target_region = "Global"
        campaign_draft.offer = "AI insights survey"

        icp = MagicMock(spec=ICPDefinition)
        icp.model_dump.return_value = {
            "positive": {"industries": ["AI/ML", "Data Science"]},
            "negative": {"excluded_industries": ["Agriculture"]}
        }

        persona = MagicMock(spec=PersonaItem)
        persona.model_dump.return_value = {
            "persona": "AI Research Lead",
            "type": "primary",
            "rationale": "Key decision maker"
        }

        channel_plan = MagicMock(spec=ChannelPlan)
        channel_plan.model_dump.return_value = {
            "channels": ["email", "linkedin"],
            "sequence_timing": {"M1": 0, "M2": 3, "M3": 7}
        }

        mock_output = MagicMock(spec=CampaignPlannerOutput)
        mock_output.campaign_draft = campaign_draft
        mock_output.icp_definition = icp
        mock_output.persona_map = [persona]
        mock_output.channel_plan = channel_plan
        mock_output.confidence_notes = "High confidence in AI market"

        with patch("apps.campaigns.views.run_campaign_planner") as mock_agent:
            mock_agent.return_value = mock_output

            self.client.force_authenticate(user=self.user)
            data = {
                "campaign_name": "AI Campaign",
                "target_industry": "AI/ML",
                "target_region": "Global",
                "offer": "AI insights",
                "campaign_type": CampaignType.SURVEY,
            }

            response = self.client.post("/api/v1/campaigns/", data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            # Verify output was persisted
            campaign = Campaign.objects.first()
            self.assertEqual(campaign.name, "AI Insights Campaign")
            self.assertIsNotNone(campaign.icp_definition)
            self.assertIsNotNone(campaign.persona_map)
            self.assertIsNotNone(campaign.channel_plan)
            self.assertEqual(campaign.confidence_notes, "High confidence in AI market")

    def test_campaign_routing_to_approval(self):
        """Test that campaigns are routed to approval when requires_approval=True."""
        from unittest.mock import patch, MagicMock
        from agents.schemas import CampaignPlannerOutput

        mock_output = MagicMock(spec=CampaignPlannerOutput)
        mock_output.campaign_draft.name = "Approval Test Campaign"
        mock_output.campaign_draft.campaign_type = CampaignType.SURVEY
        mock_output.campaign_draft.target_industry = "Tech"
        mock_output.campaign_draft.target_region = "US"
        mock_output.campaign_draft.offer = "Survey"
        mock_output.icp_definition.model_dump.return_value = {}
        mock_output.persona_map = []
        mock_output.channel_plan.model_dump.return_value = {}
        mock_output.confidence_notes = ""

        with patch("apps.campaigns.views.run_campaign_planner") as mock_agent:
            mock_agent.return_value = mock_output

            self.client.force_authenticate(user=self.user)
            data = {
                "campaign_name": "Approval Campaign",
                "target_industry": "Tech",
                "target_region": "US",
                "offer": "Survey",
                "campaign_type": CampaignType.SURVEY,
                "requires_approval": True,
            }

            response = self.client.post("/api/v1/campaigns/", data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            # Verify routed to pending_approval
            campaign = Campaign.objects.first()
            self.assertEqual(campaign.status, CampaignStatus.PENDING_APPROVAL)

    def test_campaign_auto_activation_when_no_approval_required(self):
        """Test that campaigns are auto-activated when requires_approval=False."""
        from unittest.mock import patch, MagicMock
        from agents.schemas import CampaignPlannerOutput

        mock_output = MagicMock(spec=CampaignPlannerOutput)
        mock_output.campaign_draft.name = "Auto Activate Campaign"
        mock_output.campaign_draft.campaign_type = CampaignType.SURVEY
        mock_output.campaign_draft.target_industry = "Tech"
        mock_output.campaign_draft.target_region = "US"
        mock_output.campaign_draft.offer = "Survey"
        mock_output.icp_definition.model_dump.return_value = {}
        mock_output.persona_map = []
        mock_output.channel_plan.model_dump.return_value = {}
        mock_output.confidence_notes = ""

        with patch("apps.campaigns.views.run_campaign_planner") as mock_agent:
            with patch("apps.campaigns.tasks.enable_campaign_sequences.delay") as mock_task:
                mock_agent.return_value = mock_output

                self.client.force_authenticate(user=self.user)
                data = {
                    "campaign_name": "Auto Campaign",
                    "target_industry": "Tech",
                    "target_region": "US",
                    "offer": "Survey",
                    "campaign_type": CampaignType.SURVEY,
                    "requires_approval": False,
                }

                response = self.client.post("/api/v1/campaigns/", data, format="json")
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)

                # Verify activated
                campaign = Campaign.objects.first()
                self.assertEqual(campaign.status, CampaignStatus.ACTIVE)
                mock_task.assert_called_once()
