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


# ============ Compliance Review Agent ============

class ComplianceViolationSerializer(serializers.Serializer):
    """Single compliance violation."""

    rule = serializers.CharField(help_text="Rule violated")
    severity = serializers.CharField(help_text="Severity level (block)")
    detail = serializers.CharField(help_text="Specific detail that triggered violation")
    recommendation = serializers.CharField(help_text="How to fix")


class ComplianceCheckResultSerializer(serializers.Serializer):
    """Compliance check result for single message."""

    stage = serializers.CharField(help_text="Message stage (M1, M2, M3)")
    status = serializers.CharField(help_text="Status: pass or blocked")
    violations = ComplianceViolationSerializer(many=True, help_text="List of violations")
    word_count = serializers.IntegerField(help_text="Word count of message")
    can_be_approved = serializers.BooleanField(help_text="Can be approved?")
    recommendation = serializers.CharField(help_text="ready_for_approval or must_regenerate")


class ComplianceReviewRequestSerializer(serializers.Serializer):
    """Input schema for Compliance Review Agent."""

    campaign_name = serializers.CharField(
        max_length=200,
        help_text="Campaign name"
    )
    campaign_type = serializers.ChoiceField(
        choices=["Survey", "POV", "Benchmarking", "Competition Benchmarking", "Market Research", "Expert Network", "Consulting", "Report Sales"],
        help_text="Campaign type"
    )
    channel = serializers.ChoiceField(
        choices=["email", "whatsapp", "linkedin"],
        help_text="Channel"
    )
    messages = serializers.JSONField(
        help_text="Messages dict: {persona: {M1: {message, word_count}, M2: {...}, M3: {...}}}"
    )
    prospect_name = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        help_text="Prospect name"
    )
    company_name = serializers.CharField(
        max_length=200,
        required=False,
        allow_blank=True,
        help_text="Company name"
    )
    trigger_telegram_approval = serializers.BooleanField(
        default=False,
        help_text="Send to Telegram if all pass?"
    )
    telegram_user_id = serializers.IntegerField(
        required=False,
        help_text="Telegram user ID for approval"
    )


class ComplianceReviewResponseSerializer(serializers.Serializer):
    """Output schema for Compliance Review Agent."""

    campaign_name = serializers.CharField()
    campaign_type = serializers.CharField()
    channel = serializers.CharField()
    compliance_results = serializers.JSONField(
        help_text="Per-persona compliance results"
    )
    overall_status = serializers.CharField(
        help_text="all_pass, some_blocked, all_blocked"
    )
    telegram_approval_sent = serializers.BooleanField()
    telegram_approval_id = serializers.CharField()
    notes = serializers.CharField()


# ============ Reply Classifier Agent ============

class ReplyClassifierRequestSerializer(serializers.Serializer):
    """Input schema for Reply Classifier Agent."""

    reply_text = serializers.CharField(
        help_text="The inbound reply text to classify"
    )
    channel = serializers.ChoiceField(
        choices=["email", "whatsapp", "linkedin"],
        help_text="Channel where reply came from"
    )
    prospect_id = serializers.CharField(
        help_text="Prospect ID (UUID)"
    )
    campaign_id = serializers.CharField(
        help_text="Campaign ID (UUID)"
    )
    prospect_email = serializers.EmailField(
        required=False,
        allow_blank=True,
        help_text="Prospect email address"
    )
    prospect_name = serializers.CharField(
        max_length=200,
        required=False,
        allow_blank=True,
        help_text="Prospect name"
    )
    prior_touchpoints = serializers.JSONField(
        required=False,
        help_text="Prior messages in conversation"
    )
    reply_timestamp = serializers.DateTimeField(
        required=False,
        help_text="When reply was received"
    )


class ReplyClassifierResponseSerializer(serializers.Serializer):
    """Output schema for Reply Classifier Agent."""

    prospect_id = serializers.CharField()
    campaign_id = serializers.CharField()
    intent_category = serializers.CharField(
        help_text="positive_interest, meeting_request, question, negative, out_of_office, bounce, ambiguous"
    )
    confidence_score = serializers.IntegerField(
        min_value=0,
        max_value=100,
        help_text="Confidence 0-100"
    )
    recommended_action = serializers.CharField(
        help_text="Recommended next action"
    )
    stop_flag = serializers.BooleanField(
        help_text="Always true - automation stops on any reply"
    )
    requires_human_review = serializers.BooleanField(
        help_text="True if confidence < 60"
    )
    signals_detected = serializers.ListField(
        child=serializers.CharField(),
        help_text="Signals/keywords found in reply"
    )
    notes = serializers.CharField(
        required=False,
        allow_blank=True
    )
