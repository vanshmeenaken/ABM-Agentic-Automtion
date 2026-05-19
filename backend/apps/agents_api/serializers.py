"""Serializers for Agent APIs — Request/Response validation."""

from rest_framework import serializers


# ============ Persona Classifier Agent ============

class PersonaClassifierRequestSerializer(serializers.Serializer):
    """Input schema for Persona Classifier Agent."""

    designation = serializers.CharField(
        max_length=200,
        help_text="Prospect job title/designation (e.g., 'VP of Sales', 'CTO')"
    )
    company_type = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        help_text="Type of company (e.g., 'SaaS', 'Manufacturing')"
    )
    industry = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        help_text="Industry vertical (e.g., 'EdTech', 'FinTech')"
    )
    seniority_signals = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
        help_text="Additional context (e.g., ['5+ years experience', 'manages 10+ people'])"
    )


class PersonaAssignmentSerializer(serializers.Serializer):
    """Persona assignment result."""

    persona_tag = serializers.CharField()
    confidence_score = serializers.IntegerField()
    classification_reason = serializers.CharField()


class PersonaClassifierResponseSerializer(serializers.Serializer):
    """Output schema for Persona Classifier Agent."""

    persona_tag = serializers.CharField(
        help_text="Primary persona: cxo_strategy, marketing, operations, product_rd, investor, procurement, unknown"
    )
    secondary_persona_tag = serializers.CharField(
        allow_null=True,
        required=False,
        help_text="Secondary persona if applicable"
    )
    confidence_score = serializers.IntegerField(
        help_text="Confidence 0-100"
    )
    classification_reason = serializers.CharField(
        help_text="Why this classification was assigned"
    )
    low_confidence_flag = serializers.BooleanField(
        help_text="True if score < 60, needs human review"
    )


# ============ Message Strategy Agent ============

class MessageStrategyRequestSerializer(serializers.Serializer):
    """Input schema for Message Strategy Agent."""

    campaign_name = serializers.CharField(
        max_length=200,
        help_text="Name of the campaign (e.g., 'K-12 EdTech Sales 2026')"
    )
    campaign_type = serializers.ChoiceField(
        choices=[
            "Market Research", "Survey", "Consulting", "Expert Network",
            "Webinar", "Report Sales", "Competition Benchmarking", "Account Reactivation"
        ],
        help_text="Type of campaign"
    )
    offer = serializers.CharField(
        max_length=500,
        help_text="Campaign offer/product description"
    )
    target_industry = serializers.CharField(
        max_length=100,
        help_text="Target industry (e.g., 'K-12 Education', 'Cold Chain Logistics')"
    )
    target_personas = serializers.ListField(
        child=serializers.ChoiceField(
            choices=["cxo_strategy", "marketing", "operations", "product_rd", "investor", "procurement"]
        ),
        help_text="Target personas for messaging"
    )
    channel_mix = serializers.ListField(
        child=serializers.ChoiceField(choices=["email", "whatsapp", "linkedin"]),
        required=False,
        help_text="Preferred channels"
    )


class PersonaStrategySerializer(serializers.Serializer):
    """Strategy for single persona."""

    primary_angle = serializers.CharField(help_text="Core value narrative")
    pain_points = serializers.ListField(
        child=serializers.CharField(),
        help_text="2-3 market-specific pain points"
    )
    value_prop = serializers.CharField(help_text="How offer solves the pain")


class ChannelGuidanceSerializer(serializers.Serializer):
    """Channel-specific tone guidance."""

    email = serializers.CharField(help_text="Email tone/rules")
    whatsapp = serializers.CharField(required=False, help_text="WhatsApp tone/rules")
    linkedin = serializers.CharField(required=False, help_text="LinkedIn tone/rules")


class SuccessCriteriaSerializer(serializers.Serializer):
    """Success metrics for campaign."""

    email_open_rate = serializers.CharField(help_text="Expected email open rate")
    click_rate = serializers.CharField(help_text="Expected click rate")
    response_rate = serializers.CharField(help_text="Expected response rate")
    meeting_rate = serializers.CharField(help_text="Expected meeting rate")


class MessageStrategyResponseSerializer(serializers.Serializer):
    """Output schema for Message Strategy Agent."""

    campaign_name = serializers.CharField()
    tone = serializers.CharField(help_text="consultative, data-led, formal, conversational")
    key_themes = serializers.ListField(
        child=serializers.CharField(),
        help_text="Core messaging themes"
    )
    value_propositions = serializers.DictField(
        child=serializers.CharField(),
        help_text="Value prop per persona"
    )
    call_to_action = serializers.CharField(help_text="Overall CTA direction")
    persona_specific_messages = serializers.DictField(
        help_text="Per-persona strategy details"
    )
    channel_guidance = ChannelGuidanceSerializer(help_text="Tone rules per channel")
    success_criteria = SuccessCriteriaSerializer(help_text="Expected performance metrics")


# ============ Email Copy Agent ============

class EmailDMSerializer(serializers.Serializer):
    """Email message (M1/M2/M3)."""
    message = serializers.CharField()
    word_count = serializers.IntegerField()
    send_day = serializers.CharField()
    follow_ups = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )


class EmailDMSeriesSerializer(serializers.Serializer):
    """Email M1-M3 series."""
    M1 = EmailDMSerializer()
    M2 = EmailDMSerializer()
    M3 = EmailDMSerializer()
    hook_statement = serializers.CharField()
    cta_type = serializers.CharField()


class EmailCopyRequestSerializer(serializers.Serializer):
    """Input schema for Email Copy Agent."""

    campaign_name = serializers.CharField(
        max_length=200,
        help_text="Campaign name"
    )
    campaign_type = serializers.ChoiceField(
        choices=["Survey", "POV", "Benchmarking", "Competition Benchmarking", "Market Research", "Expert Network", "Consulting", "Report Sales"],
        help_text="Campaign type"
    )
    persona_strategies = serializers.JSONField(
        help_text="Persona strategies with pain_points, primary_angle, value_prop"
    )
    messaging_strategy = serializers.JSONField(
        help_text="Message strategy from Message Strategy Agent"
    )
    channel_guidance = serializers.JSONField(
        help_text="Channel guidance dict"
    )
    target_personas = serializers.ListField(
        child=serializers.CharField(),
        help_text="Target personas (e.g., ['cxo_strategy', 'operations'])"
    )
    target_region = serializers.CharField(
        max_length=100,
        required=False,
        help_text="Target region (default: Global)"
    )
    target_industry = serializers.CharField(
        max_length=100,
        help_text="Target industry"
    )
    prospect_name = serializers.CharField(
        max_length=100,
        required=False,
        help_text="Prospect name"
    )
    company_name = serializers.CharField(
        max_length=200,
        required=False,
        help_text="Company name"
    )


class EmailCopyResponseSerializer(serializers.Serializer):
    """Output schema for Email Copy Agent."""

    campaign_name = serializers.CharField()
    campaign_type = serializers.CharField()
    email_series = serializers.DictField(
        child=EmailDMSeriesSerializer(),
        help_text="Per-persona email M1-M3 series"
    )
    notes = serializers.CharField()


# ============ WhatsApp Copy Agent ============

class WhatsAppDMSerializer(serializers.Serializer):
    """WhatsApp message (M1/M2/M3)."""
    message = serializers.CharField()
    word_count = serializers.IntegerField()
    send_day = serializers.CharField()
    follow_ups = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )


class WhatsAppDMSeriesSerializer(serializers.Serializer):
    """WhatsApp M1-M3 series."""
    M1 = WhatsAppDMSerializer()
    M2 = WhatsAppDMSerializer()
    M3 = WhatsAppDMSerializer()
    hook_statement = serializers.CharField()
    cta_type = serializers.CharField()


class WhatsAppCopyRequestSerializer(serializers.Serializer):
    """Input schema for WhatsApp Copy Agent."""

    campaign_name = serializers.CharField(
        max_length=200,
        help_text="Campaign name"
    )
    campaign_type = serializers.ChoiceField(
        choices=["Survey", "POV", "Benchmarking", "Competition Benchmarking", "Market Research", "Expert Network", "Consulting", "Report Sales"],
        help_text="Campaign type"
    )
    persona_strategies = serializers.JSONField(
        help_text="Persona strategies with pain_points, primary_angle, value_prop"
    )
    messaging_strategy = serializers.JSONField(
        help_text="Message strategy from Message Strategy Agent"
    )
    channel_guidance = serializers.JSONField(
        help_text="Channel guidance dict"
    )
    target_personas = serializers.ListField(
        child=serializers.CharField(),
        help_text="Target personas"
    )
    target_region = serializers.CharField(
        max_length=100,
        required=False,
        help_text="Target region (default: Global)"
    )
    target_industry = serializers.CharField(
        max_length=100,
        help_text="Target industry"
    )
    prospect_name = serializers.CharField(
        max_length=100,
        required=False,
        help_text="Prospect name"
    )
    company_name = serializers.CharField(
        max_length=200,
        required=False,
        help_text="Company name"
    )


class WhatsAppCopyResponseSerializer(serializers.Serializer):
    """Output schema for WhatsApp Copy Agent."""

    campaign_name = serializers.CharField()
    campaign_type = serializers.CharField()
    whatsapp_series = serializers.DictField(
        child=WhatsAppDMSeriesSerializer(),
        help_text="Per-persona WhatsApp M1-M3 series"
    )
    channel_guidance = serializers.CharField()
    notes = serializers.CharField()


# ============ LinkedIn Copy Agent ============

class LinkedInDMSerializer(serializers.Serializer):
    """LinkedIn DM message (M1/M2/M3)."""
    message = serializers.CharField()
    word_count = serializers.IntegerField()
    send_day = serializers.CharField()


class LinkedInDMSeriesSerializer(serializers.Serializer):
    """LinkedIn M1-M3 DM series."""
    M1 = LinkedInDMSerializer()
    M2 = LinkedInDMSerializer()
    M3 = LinkedInDMSerializer()
    hook_statement = serializers.CharField()
    cta_type = serializers.CharField()


class LinkedInCopyRequestSerializer(serializers.Serializer):
    """Input schema for LinkedIn Copy Agent."""

    campaign_name = serializers.CharField(
        max_length=200,
        help_text="Campaign name"
    )
    campaign_type = serializers.ChoiceField(
        choices=["Survey", "POV", "Benchmarking", "Competition Benchmarking", "Market Research", "Expert Network", "Consulting", "Report Sales"],
        help_text="Campaign type"
    )
    persona_strategies = serializers.JSONField(
        help_text="Persona strategies with pain_points, primary_angle, value_prop"
    )
    messaging_strategy = serializers.JSONField(
        help_text="Message strategy from Message Strategy Agent"
    )
    channel_guidance = serializers.JSONField(
        help_text="Channel guidance dict"
    )
    target_personas = serializers.ListField(
        child=serializers.CharField(),
        help_text="Target personas"
    )
    target_region = serializers.CharField(
        max_length=100,
        required=False,
        help_text="Target region (default: Global)"
    )
    target_industry = serializers.CharField(
        max_length=100,
        help_text="Target industry"
    )
    prospect_name = serializers.CharField(
        max_length=100,
        required=False,
        help_text="Prospect name"
    )
    company_name = serializers.CharField(
        max_length=200,
        required=False,
        help_text="Company name"
    )


class LinkedInCopyResponseSerializer(serializers.Serializer):
    """Output schema for LinkedIn Copy Agent."""

    campaign_name = serializers.CharField()
    campaign_type = serializers.CharField()
    linkedin_series = serializers.DictField(
        child=LinkedInDMSeriesSerializer(),
        help_text="Per-persona LinkedIn M1-M3 DM series"
    )
    channel_guidance = serializers.CharField()
    notes = serializers.CharField()
