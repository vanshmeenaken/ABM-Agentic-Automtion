"""ViewSets for Agent APIs — Business logic for each endpoint."""

import sys
from pathlib import Path

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    PersonaClassifierRequestSerializer,
    PersonaClassifierResponseSerializer,
    MessageStrategyRequestSerializer,
    MessageStrategyResponseSerializer,
    EmailCopyRequestSerializer,
    EmailCopyResponseSerializer,
    WhatsAppCopyRequestSerializer,
    WhatsAppCopyResponseSerializer,
    LinkedInCopyRequestSerializer,
    LinkedInCopyResponseSerializer,
)

# Add agents path to sys.path to import agents
agents_path = Path(__file__).resolve().parent.parent.parent.parent / "agents"
if str(agents_path) not in sys.path:
    sys.path.insert(0, str(agents_path))


class PersonaClassifierViewSet(viewsets.ViewSet):
    """
    API Endpoint: POST /api/v1/agents/persona-classifier/

    Classifies prospect into buyer persona (CXO, Marketing, Operations, etc.)
    with confidence score and reasoning.

    Example request:
    {
        "designation": "VP of Sales",
        "company_type": "SaaS",
        "industry": "EdTech",
        "seniority_signals": ["manages 10+ people", "5+ years experience"]
    }
    """

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"])
    def classify(self, request):
        """Run persona classifier on prospect."""
        serializer = PersonaClassifierRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Import agent function
            from persona_classifier_agent import run_persona_classifier

            # Call agent
            result = run_persona_classifier(
                designation=serializer.validated_data.get("designation"),
                company_type=serializer.validated_data.get("company_type"),
                industry=serializer.validated_data.get("industry"),
                seniority_signals=serializer.validated_data.get("seniority_signals", []),
            )

            # Validate response
            response_serializer = PersonaClassifierResponseSerializer(data=result)
            if response_serializer.is_valid():
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(response_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except ImportError as e:
            return Response(
                {"error": f"Agent module not found: {str(e)}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            return Response(
                {"error": f"Agent execution failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request):
        """Return API documentation for persona classifier."""
        return Response({
            "endpoint": "/api/v1/agents/persona-classifier/classify/",
            "method": "POST",
            "description": "Classify prospect into buyer persona",
            "input_fields": {
                "designation": "string (required)",
                "company_type": "string (optional)",
                "industry": "string (optional)",
                "seniority_signals": "list of strings (optional)"
            },
            "output_fields": {
                "persona_tag": "cxo_strategy | marketing | operations | product_rd | investor | procurement | unknown",
                "confidence_score": "0-100",
                "classification_reason": "string",
                "low_confidence_flag": "boolean"
            }
        })


class MessageStrategyViewSet(viewsets.ViewSet):
    """
    API Endpoint: POST /api/v1/agents/message-strategy/

    Generates market-aware messaging strategy per persona, pain points,
    value propositions, and channel guidance.

    Example request:
    {
        "campaign_name": "K-12 EdTech Sales 2026",
        "campaign_type": "Market Research",
        "offer": "Research on EdTech adoption trends",
        "target_industry": "K-12 Education",
        "target_personas": ["cxo_strategy", "operations"],
        "channel_mix": ["email", "whatsapp", "linkedin"]
    }
    """

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"])
    def generate(self, request):
        """Generate messaging strategy."""
        serializer = MessageStrategyRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            from message_strategy_agent import run_message_strategy

            result = run_message_strategy(
                campaign_name=serializer.validated_data.get("campaign_name"),
                campaign_type=serializer.validated_data.get("campaign_type"),
                offer=serializer.validated_data.get("offer"),
                target_industry=serializer.validated_data.get("target_industry"),
                target_personas=serializer.validated_data.get("target_personas"),
                channel_mix=serializer.validated_data.get("channel_mix", ["email", "whatsapp"]),
            )

            response_serializer = MessageStrategyResponseSerializer(data=result)
            if response_serializer.is_valid():
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(response_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except ImportError as e:
            return Response(
                {"error": f"Agent module not found: {str(e)}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            return Response(
                {"error": f"Agent execution failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request):
        """Return API documentation."""
        return Response({
            "endpoint": "/api/v1/agents/message-strategy/generate/",
            "method": "POST",
            "description": "Generate market-aware messaging strategy",
            "requires_output_from": "Campaign Planner Agent",
            "outputs_to": "Email Copy, WhatsApp Copy, LinkedIn Copy Agents"
        })


class EmailCopyViewSet(viewsets.ViewSet):
    """
    API Endpoint: POST /api/v1/agents/email-copy/

    Generates M1-M3 email copy series from messaging strategy.

    Example request:
    {
        "campaign_name": "Survey: Crop Protection India",
        "campaign_type": "Survey",
        "persona_strategies": {...},
        "messaging_strategy": {...},
        "channel_guidance": {...},
        "target_personas": ["cxo_strategy"],
        "target_industry": "Crop Protection Pesticides",
        "target_region": "India",
        "prospect_name": "Rajesh Kumar",
        "company_name": "Syngenta India"
    }
    """

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"])
    def generate(self, request):
        """Generate email M1-M3 series."""
        serializer = EmailCopyRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            from email_copy_agent import run_email_copy_agent

            result = run_email_copy_agent(
                campaign_name=serializer.validated_data.get("campaign_name"),
                campaign_type=serializer.validated_data.get("campaign_type"),
                persona_strategies=serializer.validated_data.get("persona_strategies"),
                messaging_strategy=serializer.validated_data.get("messaging_strategy"),
                channel_guidance=serializer.validated_data.get("channel_guidance"),
                target_personas=serializer.validated_data.get("target_personas"),
                target_region=serializer.validated_data.get("target_region", "Global"),
                target_industry=serializer.validated_data.get("target_industry"),
                prospect_name=serializer.validated_data.get("prospect_name", ""),
                company_name=serializer.validated_data.get("company_name", ""),
            )

            response_serializer = EmailCopyResponseSerializer(data={
                "campaign_name": result.campaign_name,
                "campaign_type": result.campaign_type,
                "email_series": {k: v.dict() for k, v in result.email_series.items()},
                "notes": result.notes
            })
            if response_serializer.is_valid():
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(response_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except ImportError as e:
            return Response(
                {"error": f"Agent module not found: {str(e)}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            return Response(
                {"error": f"Agent execution failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request):
        """Return API documentation."""
        return Response({
            "endpoint": "/api/v1/agents/email-copy/generate/",
            "method": "POST",
            "description": "Generate email M1-M3 series from messaging strategy",
            "input_source": "Message Strategy Agent output",
            "output": "M1-M3 email series with hook, follow-ups, CTA",
            "cadence": ["Day 1", "Day 3-4", "Day 7-10"],
            "features": ["2 M1 variants (FOMO/Scarcity)", "Threading support (Re:)", "Mobile-optimized"]
        })


class WhatsAppCopyViewSet(viewsets.ViewSet):
    """
    API Endpoint: POST /api/v1/agents/whatsapp-copy/

    Generates M1-M3 WhatsApp copy series (mobile-first, conversational).

    Example request:
    {
        "campaign_name": "Survey: Crop Protection India",
        "campaign_type": "Survey",
        "persona_strategies": {...},
        "messaging_strategy": {...},
        "channel_guidance": {...},
        "target_personas": ["cxo_strategy"],
        "target_industry": "Crop Protection Pesticides",
        "target_region": "India",
        "prospect_name": "Rajesh Kumar",
        "company_name": "Syngenta India"
    }
    """

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"])
    def generate(self, request):
        """Generate WhatsApp M1-M3 series."""
        serializer = WhatsAppCopyRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            from whatsapp_copy_agent import run_whatsapp_copy_agent

            result = run_whatsapp_copy_agent(
                campaign_name=serializer.validated_data.get("campaign_name"),
                campaign_type=serializer.validated_data.get("campaign_type"),
                persona_strategies=serializer.validated_data.get("persona_strategies"),
                messaging_strategy=serializer.validated_data.get("messaging_strategy"),
                channel_guidance=serializer.validated_data.get("channel_guidance"),
                target_personas=serializer.validated_data.get("target_personas"),
                target_region=serializer.validated_data.get("target_region", "Global"),
                target_industry=serializer.validated_data.get("target_industry"),
                prospect_name=serializer.validated_data.get("prospect_name", ""),
                company_name=serializer.validated_data.get("company_name", ""),
            )

            response_serializer = WhatsAppCopyResponseSerializer(data={
                "campaign_name": result.campaign_name,
                "campaign_type": result.campaign_type,
                "whatsapp_series": {k: v.dict() for k, v in result.whatsapp_series.items()},
                "channel_guidance": result.channel_guidance,
                "notes": result.notes
            })
            if response_serializer.is_valid():
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(response_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except ImportError as e:
            return Response(
                {"error": f"Agent module not found: {str(e)}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            return Response(
                {"error": f"Agent execution failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request):
        """Return API documentation."""
        return Response({
            "endpoint": "/api/v1/agents/whatsapp-copy/generate/",
            "method": "POST",
            "description": "Generate WhatsApp M1-M3 series from messaging strategy",
            "input_source": "Message Strategy Agent output",
            "output": "M1-M3 WhatsApp series with follow-ups",
            "cadence": ["Day 1", "Day 2-3", "Day 5-7"],
            "features": ["Conversational tone", "25-40 words per bubble", "M1+M2 follow-ups", "2 M1 variants"]
        })


class LinkedInCopyViewSet(viewsets.ViewSet):
    """
    API Endpoint: POST /api/v1/agents/linkedin-copy/

    Generates LinkedIn M1-M3 DM copy series (post-connection only).

    Example request:
    {
        "campaign_name": "Survey: Crop Protection India",
        "campaign_type": "Survey",
        "persona_strategies": {...},
        "messaging_strategy": {...},
        "channel_guidance": {...},
        "target_personas": ["cxo_strategy"],
        "target_industry": "Crop Protection Pesticides",
        "target_region": "India",
        "prospect_name": "Rajesh Kumar",
        "company_name": "Syngenta India"
    }
    """

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"])
    def generate(self, request):
        """Generate LinkedIn M1-M3 DM series."""
        serializer = LinkedInCopyRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            from linkedin_copy_agent import run_linkedin_copy_agent

            result = run_linkedin_copy_agent(
                campaign_name=serializer.validated_data.get("campaign_name"),
                campaign_type=serializer.validated_data.get("campaign_type"),
                persona_strategies=serializer.validated_data.get("persona_strategies"),
                messaging_strategy=serializer.validated_data.get("messaging_strategy"),
                channel_guidance=serializer.validated_data.get("channel_guidance"),
                target_personas=serializer.validated_data.get("target_personas"),
                target_region=serializer.validated_data.get("target_region", "Global"),
                target_industry=serializer.validated_data.get("target_industry"),
                prospect_name=serializer.validated_data.get("prospect_name", ""),
                company_name=serializer.validated_data.get("company_name", ""),
            )

            response_serializer = LinkedInCopyResponseSerializer(data={
                "campaign_name": result.campaign_name,
                "campaign_type": result.campaign_type,
                "linkedin_series": {k: v.dict() for k, v in result.linkedin_series.items()},
                "channel_guidance": result.channel_guidance,
                "notes": result.notes
            })
            if response_serializer.is_valid():
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(response_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except ImportError as e:
            return Response(
                {"error": f"Agent module not found: {str(e)}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            return Response(
                {"error": f"Agent execution failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request):
        """Return API documentation."""
        return Response({
            "endpoint": "/api/v1/agents/linkedin-copy/generate/",
            "method": "POST",
            "description": "Generate LinkedIn M1-M3 DM series (post-connection)",
            "input_source": "Message Strategy Agent output",
            "output": "M1-M3 LinkedIn DM series",
            "cadence": ["Day 1", "Day 3-4", "Day 7-10"],
            "features": ["Peer-to-peer tone", "No connection request note", "2 M1 variants", "Either way M3 close"]
        })
