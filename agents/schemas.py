"""Pydantic schemas for Campaign Planner Agent input/output."""

from typing import List, Optional, Dict, Literal
from pydantic import BaseModel, Field


class CampaignPlannerInput(BaseModel):
    """Input schema for Campaign Planner Agent."""

    campaign_name: str = Field(..., description="Name of the campaign")
    target_industry: str = Field(..., description="Primary industry target (e.g., Automotive)")
    target_region: str = Field(..., description="Geographic region (e.g., India, EMEA)")
    offer: str = Field(..., description="Campaign offer or product description")
    campaign_type: Literal[
        "Market Research",
        "Survey",
        "Consulting",
        "Expert Network",
        "Webinar",
        "Report Sales",
        "Competition Benchmarking",
        "Account Reactivation"
    ] = Field(..., description="Type of campaign")
    preferred_channels: Optional[List[Literal["email", "whatsapp", "linkedin"]]] = Field(
        None, description="Preferred outreach channels (optional)"
    )
    notes: Optional[str] = Field(None, description="Additional campaign context or notes")


class ICPPositive(BaseModel):
    """Positive ICP criteria."""

    industries: List[str] = Field(default_factory=list, description="Target industries")
    sub_segments: List[str] = Field(
        default_factory=list, description="Industry sub-segments (more specific than top-level)"
    )
    company_size: Dict[str, int] = Field(
        default_factory=dict, description="Min/max employees or revenue range"
    )
    regions: List[str] = Field(default_factory=list, description="Target regions")
    seniority_levels: List[str] = Field(default_factory=list, description="Target seniority levels")
    decision_maker_functions: List[str] = Field(
        default_factory=list, description="Target buyer functions"
    )
    buying_signals: List[str] = Field(default_factory=list, description="Buying signals to monitor")


class ICPNegative(BaseModel):
    """Negative ICP criteria to exclude."""

    excluded_company_types: List[str] = Field(
        default_factory=list, description="Company types to exclude (e.g., freelancers)"
    )
    excluded_industries: List[str] = Field(default_factory=list, description="Industries to exclude")
    excluded_regions: List[str] = Field(default_factory=list, description="Regions to exclude")
    excluded_company_sizes: List[str] = Field(default_factory=list, description="Company sizes to exclude")


class ICPDefinition(BaseModel):
    """Full ICP definition with positive and negative criteria."""

    positive: ICPPositive
    negative: ICPNegative


class PersonaItem(BaseModel):
    """Single persona in the persona map."""

    persona: str = Field(..., description="Persona name (e.g., CXO, Marketing, Operations)")
    persona_type: Literal["primary", "secondary"] = Field(..., description="Primary or secondary")
    rationale: str = Field(..., description="Why this persona is relevant to the campaign")


class ChannelPlan(BaseModel):
    """Channel strategy and sequence timing."""

    channels: List[Literal["email", "whatsapp", "linkedin"]] = Field(
        ..., description="Selected channels"
    )
    sequence_timing: Dict[Literal["M1", "M2", "M3", "M4"], int] = Field(
        default={"M1": 0, "M2": 3, "M3": 7, "M4": 12},
        description="Days to send each message stage"
    )


class CampaignDraft(BaseModel):
    """Campaign object ready for database creation."""

    name: str
    campaign_type: str
    target_industry: str
    target_region: str
    offer: str
    status: Literal["draft"] = "draft"
    requires_approval: bool = True


class CampaignPlannerOutput(BaseModel):
    """Full output from Campaign Planner Agent."""

    campaign_draft: CampaignDraft
    icp_definition: ICPDefinition
    persona_map: List[PersonaItem] = Field(..., description="Primary + secondary personas")
    channel_plan: ChannelPlan
    approval_flag: bool = Field(True, description="Always true for new campaigns")
    confidence_notes: str = Field(
        "", description="Agent notes on assumptions, ambiguities, or low-confidence decisions"
    )


# Prospect Research Agent schemas
class ProspectResearchInput(BaseModel):
    """Input for Prospect Research Agent."""

    campaign_id: str
    icp_definition: ICPDefinition
    persona_map: List[PersonaItem]
    approved_sources: List[str]
    max_prospects: int = Field(default=500, description="Maximum prospects to return")
    notes: Optional[str] = None


class RawProspect(BaseModel):
    """Raw prospect record from a source."""

    source: str
    first_name: str
    last_name: str
    email: str
    phone: str
    designation: str
    company_name: str
    company_id: str
    company_size: str
    industry: str
    region: str
    raw_source_data: Dict = Field(default_factory=dict)


class ProspectResearchOutput(BaseModel):
    """Output from Prospect Research Agent."""

    raw_prospects: List[RawProspect]
    accounts_found: int
    contacts_found: int
    source_breakdown: Dict[str, int]
    query_params_used: Dict
    notes: str = ""


# Data Quality Agent schemas
class DataQualityInput(BaseModel):
    """Input for Data Quality Agent."""

    raw_prospects: List[Dict]
    campaign_id: str
    dedup_scope: Literal["campaign", "platform", "pipedrive"]


class CleanedProspect(BaseModel):
    """Cleaned prospect record."""

    first_name: str
    last_name: str
    email: str
    phone: str
    designation: str
    company_name: str
    confidence_score: int
    is_duplicate: bool = False
    is_low_confidence: bool = False
    corrections_made: List[str] = Field(default_factory=list)
    raw_source_data: Dict = Field(default_factory=dict)


class DataQualityOutput(BaseModel):
    """Output from Data Quality Agent."""

    cleaned_prospects: List[CleanedProspect]
    duplicate_flags: List[Dict] = Field(default_factory=list)
    low_confidence_flags: List[Dict] = Field(default_factory=list)
    field_corrections: Dict = Field(default_factory=dict)
    confidence_score_distribution: Dict = Field(default_factory=dict)
    duplicate_rate: float = 0.0
    notes: str = ""


# Persona Classifier Agent schemas
class PersonaAssignment(BaseModel):
    """Persona assignment with confidence score."""

    persona: str
    confidence_score: int
    rationale: str


class ClassifiedProspect(BaseModel):
    """Prospect with persona classification and campaign fit validation."""

    email: str
    designation: str
    company_name: str
    primary_persona: PersonaAssignment
    secondary_persona: Optional[PersonaAssignment] = None
    seniority_level: str
    function: str
    needs_review: bool = False
    # Campaign fit validation (NEW)
    campaign_fit_score: int = Field(0, description="Campaign relevance score 0-100")
    campaign_fit_valid: bool = Field(True, description="Is this prospect valid for this campaign?")
    campaign_fit_rationale: str = Field("", description="Why/why not this prospect fits the campaign")


class PersonaClassifierInput(BaseModel):
    """Input for Persona Classifier Agent."""

    cleaned_prospects: List[Dict]
    campaign_type: Literal[
        "Market Research",
        "Survey",
        "Consulting",
        "Expert Network",
        "Webinar",
        "Report Sales",
        "Competition Benchmarking",
        "Account Reactivation"
    ]
    target_personas: List[str]
    # Campaign context for fit validation (NEW)
    target_industry: str = Field("", description="Campaign target industry (e.g., K-12 Education)")
    target_functions: List[str] = Field(default_factory=list, description="Preferred buyer functions for this campaign")


class PersonaClassifierOutput(BaseModel):
    """Output from Persona Classifier Agent."""

    classified_prospects: List[ClassifiedProspect]
    persona_distribution: Dict[str, int]
    low_confidence_count: int
    unclassifiable_count: int
    average_confidence: float
    notes: str = ""


# Message Strategy Agent schemas
class MessageStrategy(BaseModel):
    """Overall messaging strategy."""

    tone: str = Field(..., description="Tone (e.g., professional, consultative, urgent)")
    key_themes: List[str] = Field(..., description="Main messaging themes")
    value_propositions: Dict[str, str] = Field(
        ..., description="Value prop per persona (persona -> value prop)"
    )
    objection_handlers: Dict[str, str] = Field(
        default_factory=dict, description="How to handle common objections"
    )
    call_to_action: str = Field(..., description="Primary CTA for the campaign")


class MessageStrategyInput(BaseModel):
    """Input for Message Strategy Agent."""

    campaign_name: str
    campaign_type: str
    offer: str
    target_personas: List[str]
    target_industry: str
    channel_mix: List[str]


class PersonaStrategy(BaseModel):
    """Persona-specific messaging strategy with pain points and angles."""

    primary_angle: str = Field(..., description="Primary messaging angle for this persona")
    pain_points: List[str] = Field(..., description="Real pain points this persona faces")
    value_prop: str = Field(..., description="Value proposition addressing their pain points")


class MessageStrategyOutput(BaseModel):
    """Output from Message Strategy Agent."""

    messaging_strategy: MessageStrategy
    persona_specific_messages: Dict[str, PersonaStrategy] = Field(
        ..., description="Persona-specific strategy with angles, pain points, value props"
    )
    channel_guidance: Dict[str, str] = Field(
        default_factory=dict, description="Channel-specific messaging guidance"
    )
    success_criteria: Dict[str, str] = Field(
        default_factory=dict, description="Success metrics by campaign type"
    )
    notes: str = ""


# Email Copy Agent schemas
class EmailCopy(BaseModel):
    """Email copy variation."""

    subject: str = Field(..., description="Subject line")
    preview_text: str = Field(..., description="Preview text (character limit: 100)")
    body: str = Field(..., description="Email body")
    cta_text: str = Field(..., description="Call-to-action button text")
    personalization_vars: Dict[str, str] = Field(
        default_factory=dict, description="Variables to personalize ({{first_name}}, {{company}})"
    )


class EmailCopyInput(BaseModel):
    """Input for Email Copy Agent."""

    persona: str = Field(..., description="Target persona")
    company_name: str = Field(..., description="Prospect company")
    designation: str = Field(..., description="Prospect job title")
    message_strategy: Dict = Field(..., description="From Message Strategy Agent output")
    campaign_offer: str = Field(..., description="What we're offering")
    tone: str = Field(..., description="Tone for this email")


class EmailCopyOutput(BaseModel):
    """Output from Email Copy Agent."""

    primary_email: EmailCopy
    alternative_variations: List[EmailCopy] = Field(
        default_factory=list, description="2-3 alternative variations"
    )
    notes: str = ""


# WhatsApp Copy Agent schemas
class WhatsAppCopy(BaseModel):
    """WhatsApp message copy."""

    message: str = Field(..., description="WhatsApp message (keep under 160 chars)")
    follow_up_messages: List[str] = Field(
        default_factory=list, description="Follow-up messages if no reply"
    )
    personalization_vars: Dict[str, str] = Field(
        default_factory=dict, description="Variables to personalize"
    )


class WhatsAppCopyInput(BaseModel):
    """Input for WhatsApp Copy Agent."""

    persona: str = Field(..., description="Target persona")
    first_name: str = Field(..., description="Prospect first name")
    company_name: str = Field(..., description="Prospect company")
    designation: str = Field(..., description="Prospect job title")
    message_strategy: Dict = Field(..., description="From Message Strategy Agent output")
    campaign_offer: str = Field(..., description="What we're offering")
    tone: str = Field(..., description="Tone for WhatsApp (usually conversational)")


class WhatsAppCopyOutput(BaseModel):
    """Output from WhatsApp Copy Agent."""

    primary_message: WhatsAppCopy
    alternative_variations: List[WhatsAppCopy] = Field(
        default_factory=list, description="2-3 alternative variations"
    )
    notes: str = ""


# LinkedIn Copy schemas
class LinkedInDM(BaseModel):
    """Single LinkedIn DM in the series."""

    message: str = Field(..., description="DM body text")
    word_count: int = Field(..., description="Word count of message")
    send_day: str = Field(..., description="When to send (Day 1, Day 3-4, Day 7-10)")


class LinkedInDMSeries(BaseModel):
    """Complete LinkedIn M1-M3 DM series."""

    M1: LinkedInDM = Field(..., description="First message (post-connection hook)")
    M2: LinkedInDM = Field(..., description="Second message (proof/sample)")
    M3: LinkedInDM = Field(..., description="Third message (low-pressure close)")
    hook_statement: str = Field(..., description="The core insight/hook used")
    cta_type: str = Field(..., description="CTA type: 30_min_call, walk_through, sample_review, either_way")


class LinkedInCopyInput(BaseModel):
    """Input schema for LinkedIn Copy Agent."""

    campaign_name: str = Field(..., description="Campaign name")
    campaign_type: str = Field(..., description="Campaign type")
    persona: str = Field(..., description="Target persona")
    primary_angle: str = Field(..., description="Core messaging angle")
    pain_points: List[str] = Field(..., description="Market-specific pain points")
    value_prop: str = Field(..., description="Value proposition")
    tone: str = Field(..., description="Tone guidance from Message Strategy")
    channel_guidance: str = Field(..., description="LinkedIn-specific tone guidance")
    target_region: str = Field(default="Global", description="Target region")
    prospect_name: Optional[str] = Field(None, description="Prospect name (for personalization)")
    company_name: Optional[str] = Field(None, description="Company name (for personalization)")
    sender_name: Optional[str] = Field(None, description="Sender name (for sign-off)")


class LinkedInCopyOutput(BaseModel):
    """Output from LinkedIn Copy Agent."""

    campaign_name: str = Field(..., description="Campaign name")
    campaign_type: str = Field(..., description="Campaign type")
    linkedin_series: Dict[str, LinkedInDMSeries] = Field(
        ..., description="Per-persona LinkedIn DM series"
    )
    channel_guidance: str = Field(..., description="LinkedIn channel guidance")
    notes: str = Field(default="", description="Implementation notes")


# Email Copy Agent schemas (M1-M3 series)
class EmailDM(BaseModel):
    """Single email in M1-M3 series."""

    subject: str = Field(..., description="Email subject line")
    preview_text: str = Field(..., description="Preview text (100 chars max)")
    body: str = Field(..., description="Email body with formatting")
    word_count: int = Field(..., description="Word count of body")
    send_day: str = Field(..., description="When to send (Day 1, Day 3-4, Day 7-10)")


class EmailDMSeries(BaseModel):
    """Complete email M1-M3 series."""

    M1: EmailDM = Field(..., description="First email (hook + offer)")
    M2: EmailDM = Field(..., description="Second email (proof/sample)")
    M3: EmailDM = Field(..., description="Third email (urgency/close)")
    hook_statement: str = Field(..., description="Core insight/hook used")
    cta_type: str = Field(..., description="CTA type: schedule_call, review_findings, compare_approach")


class EmailCopyAgentOutput(BaseModel):
    """Output from Email Copy Agent (M1-M3 series)."""

    campaign_name: str = Field(..., description="Campaign name")
    campaign_type: str = Field(..., description="Campaign type")
    email_series: Dict[str, EmailDMSeries] = Field(
        ..., description="Per-persona email M1-M3 series"
    )
    channel_guidance: str = Field(..., description="Email channel guidance")
    notes: str = Field(default="", description="Implementation notes")


# WhatsApp Copy Agent schemas (M1-M3 series)
class WhatsAppDM(BaseModel):
    """Single WhatsApp message in M1-M3 series."""

    message: str = Field(..., description="WhatsApp message body (conversational tone)")
    word_count: int = Field(..., description="Word count of message")
    send_day: str = Field(..., description="When to send (Day 1, Day 2-3, Day 5-7)")
    follow_ups: List[str] = Field(default_factory=list, description="Follow-up messages if no reply")


class WhatsAppDMSeries(BaseModel):
    """Complete WhatsApp M1-M3 series."""

    M1: WhatsAppDM = Field(..., description="First message (hook + CTA)")
    M2: WhatsAppDM = Field(..., description="Second message (proof/insight)")
    M3: WhatsAppDM = Field(..., description="Third message (close)")
    hook_statement: str = Field(..., description="Core insight/hook used")
    cta_type: str = Field(..., description="CTA type: quick_call, review_findings, connect")


class WhatsAppCopyAgentOutput(BaseModel):
    """Output from WhatsApp Copy Agent (M1-M3 series)."""

    campaign_name: str = Field(..., description="Campaign name")
    campaign_type: str = Field(..., description="Campaign type")
    whatsapp_series: Dict[str, WhatsAppDMSeries] = Field(
        ..., description="Per-persona WhatsApp M1-M3 series"
    )
    channel_guidance: str = Field(..., description="WhatsApp channel guidance")
    notes: str = Field(default="", description="Implementation notes")


# Compliance Review Agent schemas
class ComplianceViolation(BaseModel):
    """Single compliance violation found in message."""

    rule: str = Field(
        ...,
        description="Rule violated (spam_trigger_word, regulatory_language, false_claim, specific_assertion, missing_opt_out, excessive_length, brand_risk_language)"
    )
    severity: str = Field(..., description="Severity level (block)")
    detail: str = Field(..., description="Exact word/phrase or specific detail that triggered violation")
    recommendation: str = Field(..., description="What to fix or change")


class ComplianceCheckResult(BaseModel):
    """Compliance check result for single message."""

    stage: str = Field(..., description="Message stage (M1, M2, M3)")
    status: str = Field(..., description="Status: pass or blocked")
    violations: List[ComplianceViolation] = Field(default_factory=list, description="List of violations found")
    word_count: int = Field(..., description="Word count of message")
    can_be_approved: bool = Field(..., description="Can this message be approved? False if any violation")
    recommendation: str = Field(..., description="Recommendation: ready_for_approval or must_regenerate")


class ComplianceReviewAgentOutput(BaseModel):
    """Output from Compliance Review Agent."""

    campaign_name: str = Field(..., description="Campaign name")
    campaign_type: str = Field(..., description="Campaign type")
    channel: str = Field(..., description="Channel (email, whatsapp, linkedin)")
    compliance_results: Dict[str, List[ComplianceCheckResult]] = Field(
        ..., description="Per-persona compliance results (persona -> [M1_result, M2_result, M3_result])"
    )
    overall_status: str = Field(..., description="Overall status: all_pass, some_blocked, all_blocked")
    telegram_approval_sent: bool = Field(
        ..., description="Was Telegram approval request sent? (only if all_pass and trigger_telegram_approval=True)"
    )
    telegram_approval_id: str = Field(
        default="", description="Telegram approval ID if approval request was sent"
    )
    notes: str = Field(default="", description="Additional notes or context")


# Orchestrator schemas
class OrchestrationInput(BaseModel):
    """Input to run full orchestration."""

    # Campaign info
    campaign_name: str
    target_industry: str
    target_region: str
    offer: str
    campaign_type: str
    preferred_channels: Optional[List[str]] = None
    notes: Optional[str] = None

    # Prospect info (for persona classification and messaging)
    prospects: List[Dict] = Field(
        default_factory=list, description="List of prospects with email, name, company, designation"
    )


class OrchestrationOutput(BaseModel):
    """Complete output from full orchestration."""

    campaign_plan: Dict = Field(..., description="Output from Campaign Planner Agent")
    message_strategy: Dict = Field(..., description="Output from Message Strategy Agent")
    prospect_messaging: List[Dict] = Field(
        ..., description="List of prospects with classified personas and generated copy"
    )
    execution_summary: Dict = Field(
        ..., description="Summary of what was generated, what was skipped, why"
    )
    notes: str = ""
