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

class EmailCopyRequestSerializer(serializers.Serializer):
    """Input schema for Email Copy Agent."""

    strategy_brief = serializers.JSONField(
        help_text="Output from Message Strategy Agent"
    )
    persona_tag = serializers.ChoiceField(
        choices=["cxo_strategy", "marketing", "operations", "product_rd", "investor", "procurement"],
        help_text="Target persona"
    )
    prospect_name = serializers.CharField(
        max_length=100,
        help_text="Prospect name (e.g., 'John Doe')"
    )
    company_name = serializers.CharField(
        max_length=200,
        help_text="Company name"
    )
    offer = serializers.CharField(
        max_length=500,
        help_text="Campaign offer"
    )
    stage = serializers.ChoiceField(
        choices=["M1", "M2", "M3", "M4"],
        help_text="Email stage in sequence"
    )
    sender_name = serializers.CharField(
        max_length=100,
        help_text="Name of email sender"
    )
    prior_email_subjects = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="Previous subject lines (to avoid repetition)"
    )


class EmailCopyResponseSerializer(serializers.Serializer):
    """Output schema for Email Copy Agent."""

    subject = serializers.CharField(
        help_text="Email subject line (< 60 chars)"
    )
    body = serializers.CharField(
        help_text="Email body in plain text"
    )
    word_count = serializers.IntegerField(
        help_text="Word count of body"
    )
    stage = serializers.CharField(help_text="M1, M2, M3, or M4")
    cta = serializers.CharField(help_text="Specific call to action")


# ============ WhatsApp Copy Agent ============

class WhatsAppCopyRequestSerializer(serializers.Serializer):
    """Input schema for WhatsApp Copy Agent."""

    strategy_brief = serializers.JSONField(
        help_text="Output from Message Strategy Agent"
    )
    persona_tag = serializers.ChoiceField(
        choices=["cxo_strategy", "marketing", "operations", "product_rd", "investor", "procurement"],
        help_text="Target persona"
    )
    prospect_name = serializers.CharField(
        max_length=100,
        help_text="Prospect name"
    )
    company_name = serializers.CharField(
        max_length=200,
        help_text="Company name"
    )
    offer = serializers.CharField(
        max_length=500,
        help_text="Campaign offer"
    )
    stage = serializers.ChoiceField(
        choices=["M1", "M2", "M3", "M4"],
        help_text="Message stage"
    )
    sender_name = serializers.CharField(
        max_length=100,
        help_text="Sender name"
    )


class WhatsAppCopyResponseSerializer(serializers.Serializer):
    """Output schema for WhatsApp Copy Agent."""

    body = serializers.CharField(
        help_text="WhatsApp message body (max 300 words)"
    )
    word_count = serializers.IntegerField(
        help_text="Word count"
    )
    stage = serializers.CharField(help_text="M1, M2, M3, or M4")
    opt_out_line = serializers.CharField(
        help_text="Opt-out statement (e.g., 'Reply STOP to opt out')"
    )
    cta = serializers.CharField(help_text="Call to action")


# ============ LinkedIn Copy Agent ============

class LinkedInCopyRequestSerializer(serializers.Serializer):
    """Input schema for LinkedIn Copy Agent."""

    strategy_brief = serializers.JSONField(
        help_text="Output from Message Strategy Agent"
    )
    persona_tag = serializers.ChoiceField(
        choices=["cxo_strategy", "marketing", "operations", "product_rd", "investor", "procurement"],
        help_text="Target persona"
    )
    prospect_name = serializers.CharField(
        max_length=100,
        help_text="Prospect name"
    )
    company_name = serializers.CharField(
        max_length=200,
        help_text="Company name"
    )
    offer = serializers.CharField(
        max_length=500,
        help_text="Campaign offer"
    )
    sender_name = serializers.CharField(
        max_length=100,
        help_text="Sender name"
    )


class LinkedInConnectionRequestSerializer(serializers.Serializer):
    """LinkedIn connection request output."""

    connection_request_note = serializers.CharField(
        max_length=300,
        help_text="Connection request note (max 300 chars)"
    )
    character_count = serializers.IntegerField(help_text="Character count")


class LinkedInFollowUpMessageSerializer(serializers.Serializer):
    """LinkedIn follow-up message output (post-connection)."""

    follow_up_message = serializers.CharField(
        help_text="Follow-up message (max 300 words)"
    )
    word_count = serializers.IntegerField(help_text="Word count")
    optimal_delay_hours = serializers.IntegerField(
        help_text="Recommended hours to wait before sending"
    )
    cta = serializers.CharField(help_text="Call to action")


class LinkedInCopyResponseSerializer(serializers.Serializer):
    """Output schema for LinkedIn Copy Agent."""

    connection_request = LinkedInConnectionRequestSerializer()
    follow_up_message = LinkedInFollowUpMessageSerializer()
