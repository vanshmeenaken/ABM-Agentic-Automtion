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

    Generates M1-M4 email copy for prospect based on strategy.

    Example request:
    {
        "strategy_brief": {...},
        "persona_tag": "cxo_strategy",
        "prospect_name": "John Doe",
        "company_name": "Acme Corp",
        "offer": "EdTech research",
        "stage": "M1",
        "sender_name": "Your Name",
        "prior_email_subjects": []
    }
    """

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"])
    def generate(self, request):
        """Generate email copy."""
        serializer = EmailCopyRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            from email_copy_agent import generate_email_sequence

            result = generate_email_sequence(
                strategy_brief=serializer.validated_data.get("strategy_brief"),
                persona_tag=serializer.validated_data.get("persona_tag"),
                prospect_name=serializer.validated_data.get("prospect_name"),
                company_name=serializer.validated_data.get("company_name"),
                offer=serializer.validated_data.get("offer"),
                stage=serializer.validated_data.get("stage"),
                sender_name=serializer.validated_data.get("sender_name"),
                prior_email_subjects=serializer.validated_data.get("prior_email_subjects", []),
            )

            response_serializer = EmailCopyResponseSerializer(data=result)
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
            "description": "Generate email M1-M4 copy",
            "stages": ["M1 (cold first touch)", "M2 (follow-up)", "M3 (social proof)", "M4 (final low pressure)"],
            "constraints": [
                "Subject < 60 chars",
                "No spam trigger words",
                "Plain text only",
                "Must pass Compliance Review"
            ]
        })


class WhatsAppCopyViewSet(viewsets.ViewSet):
    """
    API Endpoint: POST /api/v1/agents/whatsapp-copy/

    Generates M1-M4 WhatsApp copy (mobile-first, conversational).

    Example request:
    {
        "strategy_brief": {...},
        "persona_tag": "operations",
        "prospect_name": "Jane Doe",
        "company_name": "XYZ Corp",
        "offer": "Logistics research",
        "stage": "M1",
        "sender_name": "Your Name"
    }
    """

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"])
    def generate(self, request):
        """Generate WhatsApp copy."""
        serializer = WhatsAppCopyRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            from whatsapp_copy_agent import generate_whatsapp_sequence

            result = generate_whatsapp_sequence(
                strategy_brief=serializer.validated_data.get("strategy_brief"),
                persona_tag=serializer.validated_data.get("persona_tag"),
                prospect_name=serializer.validated_data.get("prospect_name"),
                company_name=serializer.validated_data.get("company_name"),
                offer=serializer.validated_data.get("offer"),
                stage=serializer.validated_data.get("stage"),
                sender_name=serializer.validated_data.get("sender_name"),
            )

            response_serializer = WhatsAppCopyResponseSerializer(data=result)
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
            "description": "Generate WhatsApp M1-M4 copy",
            "constraints": [
                "Max 120-70 words per stage (decreasing)",
                "Conversational tone",
                "MUST include opt-out line",
                "No media instructions in copy"
            ]
        })


class LinkedInCopyViewSet(viewsets.ViewSet):
    """
    API Endpoint: POST /api/v1/agents/linkedin-copy/

    Generates LinkedIn connection request + follow-up DM copy.

    Example request:
    {
        "strategy_brief": {...},
        "persona_tag": "cxo_strategy",
        "prospect_name": "Alice Smith",
        "company_name": "Tech Corp",
        "offer": "Executive insights",
        "sender_name": "Your Name"
    }
    """

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"])
    def generate(self, request):
        """Generate LinkedIn copy (connection + DM)."""
        serializer = LinkedInCopyRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            from linkedin_copy_agent import generate_linkedin_series

            result = generate_linkedin_series(
                strategy_brief=serializer.validated_data.get("strategy_brief"),
                persona_tag=serializer.validated_data.get("persona_tag"),
                prospect_name=serializer.validated_data.get("prospect_name"),
                company_name=serializer.validated_data.get("company_name"),
                offer=serializer.validated_data.get("offer"),
                sender_name=serializer.validated_data.get("sender_name"),
            )

            response_serializer = LinkedInCopyResponseSerializer(data=result)
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
            "description": "Generate LinkedIn connection request + follow-up DM",
            "output_parts": [
                "connection_request_note (max 300 chars)",
                "follow_up_message (max 300 words, send 48h+ after connection)"
            ],
            "note": "Platform does not send via LinkedIn. Copy is for LinkedHelper setup."
        })
