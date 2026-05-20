"""Compliance Review Agent - validates messages against compliance rules."""

import re
import sys
import os
from typing import Dict, List, Optional
from datetime import datetime
from schemas import ComplianceViolation, ComplianceCheckResult, ComplianceReviewAgentOutput

# Lazy import Telegram service (only needed when trigger_telegram_approval=True)
TelegramApprovalService = None

def _import_telegram_service():
    """Lazy import Telegram service when needed."""
    global TelegramApprovalService
    if TelegramApprovalService is None:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
        try:
            from apps.core.telegram_service import TelegramApprovalService as TAS
            TelegramApprovalService = TAS
        except ImportError:
            # Django not available (e.g., during tests without backend), use mock
            TelegramApprovalService = None
    return TelegramApprovalService


# ============================================================================
# COMPLIANCE RULES CONFIGURATION
# ============================================================================

SPAM_TRIGGER_WORDS = [
    "free", "urgent", "act now", "limited time", "winner",
    "click here", "buy now", "risk-free"
]

REGULATORY_LANGUAGE = [
    "guarantee", "guaranteed", "certainty", "promise",
    "assured results", "you will definitely"
]

FALSE_CLAIMS = [
    "we guarantee", "proven results", "100% success",
    "no risk", "zero risk"
]

BRAND_RISK_LANGUAGE = [
    "official partner", "certified by", "endorsed by", "authorized by"
]

OPT_OUT_KEYWORDS = ["stop", "opt out", "unsubscribe"]


# ============================================================================
# COMPLIANCE CHECK FUNCTIONS
# ============================================================================

def check_spam_trigger_words(message: str) -> Optional[ComplianceViolation]:
    """Rule 1: Check for spam trigger words."""
    lower_msg = message.lower()
    for word in SPAM_TRIGGER_WORDS:
        if word in lower_msg:
            return ComplianceViolation(
                rule="spam_trigger_word",
                severity="block",
                detail=f'Found spam trigger word: "{word}"',
                recommendation=f"Remove or rephrase '{word}' with more specific, direct language"
            )
    return None


def check_regulatory_language(message: str) -> Optional[ComplianceViolation]:
    """Rule 2: Check for regulatory/overpromising language."""
    lower_msg = message.lower()
    for phrase in REGULATORY_LANGUAGE:
        if phrase in lower_msg:
            return ComplianceViolation(
                rule="regulatory_language",
                severity="block",
                detail=f'Found regulatory language: "{phrase}"',
                recommendation=f"Remove promise-based language; use conditional or investigative framing instead"
            )
    return None


def check_false_claims(message: str) -> Optional[ComplianceViolation]:
    """Rule 3: Check for false or absolute claims."""
    lower_msg = message.lower()
    for claim in FALSE_CLAIMS:
        if claim in lower_msg:
            return ComplianceViolation(
                rule="false_claim",
                severity="block",
                detail=f'Found false/absolute claim: "{claim}"',
                recommendation=f"Use qualified language like 'may help', 'can improve', 'often see'"
            )
    return None


def check_specific_assertions(message: str) -> Optional[ComplianceViolation]:
    """Rule 4: Check for unsourced specific percentages or currency amounts."""
    # Pattern 1: numbers with % followed by growth/increase/revenue/ROI
    percent_pattern = r'\d+%\s*(growth|increase|revenue|ROI|boost|improvement|return)'
    if re.search(percent_pattern, message, re.IGNORECASE):
        # Check if there's a source qualifier nearby (like "based on", "according to", "from our research")
        if not re.search(r'(based on|according to|from our|per|research|study|data)', message, re.IGNORECASE):
            match = re.search(percent_pattern, message, re.IGNORECASE)
            return ComplianceViolation(
                rule="specific_assertion",
                severity="block",
                detail=f'Found specific assertion without source: "{match.group()}"',
                recommendation="Add source qualifier like 'based on our research' or 'according to industry data'"
            )

    # Pattern 2: currency amounts
    currency_pattern = r'[$₹€]\d+(?:,\d{3})*(?:\s*(?:million|billion|thousand|M|B|K))?'
    if re.search(currency_pattern, message):
        if not re.search(r'(based on|according to|from our|per|research|study|example)', message, re.IGNORECASE):
            match = re.search(currency_pattern, message)
            return ComplianceViolation(
                rule="specific_assertion",
                severity="block",
                detail=f'Found specific currency amount without context: "{match.group()}"',
                recommendation="Add context like 'for example' or 'in similar scenarios'"
            )

    return None


def check_missing_opt_out(message: str, channel: str) -> Optional[ComplianceViolation]:
    """Rule 5: Check for missing opt-out language (WhatsApp only)."""
    if channel.lower() != "whatsapp":
        return None

    lower_msg = message.lower()
    has_opt_out = any(keyword in lower_msg for keyword in OPT_OUT_KEYWORDS)

    if not has_opt_out:
        return ComplianceViolation(
            rule="missing_opt_out",
            severity="block",
            detail="No opt-out instruction found in WhatsApp message",
            recommendation="Add 'Reply STOP to unsubscribe' or similar opt-out instruction"
        )

    return None


def check_excessive_length(message: str, channel: str) -> Optional[ComplianceViolation]:
    """Rule 6: Check for excessive message length (WhatsApp only)."""
    if channel.lower() != "whatsapp":
        return None

    word_count = len(message.split())
    if word_count > 300:
        return ComplianceViolation(
            rule="excessive_length",
            severity="block",
            detail=f"WhatsApp message has {word_count} words (limit: 300)",
            recommendation="Reduce message length; split into multiple messages if needed"
        )

    return None


def check_brand_risk_language(message: str) -> Optional[ComplianceViolation]:
    """Rule 7: Check for brand-risk association language."""
    lower_msg = message.lower()
    for phrase in BRAND_RISK_LANGUAGE:
        if phrase in lower_msg:
            return ComplianceViolation(
                rule="brand_risk_language",
                severity="block",
                detail=f'Found brand-risk phrase: "{phrase}"',
                recommendation="Remove claim of official partnership/certification unless verified in campaign brief"
            )
    return None


# ============================================================================
# MAIN COMPLIANCE FUNCTION
# ============================================================================

def check_message_compliance(
    message: str,
    channel: str,
    stage: str,
    word_count: int = 0
) -> ComplianceCheckResult:
    """
    Check single message against all 7 compliance rules.

    Args:
        message: Message text to check
        channel: Channel (email, whatsapp, linkedin)
        stage: Message stage (M1, M2, M3)
        word_count: Pre-calculated word count (optional)

    Returns:
        ComplianceCheckResult with status, violations, and recommendation
    """
    if not word_count:
        word_count = len(message.split())

    violations: List[ComplianceViolation] = []

    # Run all 7 checks
    checks = [
        check_spam_trigger_words(message),
        check_regulatory_language(message),
        check_false_claims(message),
        check_specific_assertions(message),
        check_missing_opt_out(message, channel),
        check_excessive_length(message, channel),
        check_brand_risk_language(message)
    ]

    # Collect violations
    violations = [v for v in checks if v is not None]

    # Determine status and recommendation
    status = "blocked" if violations else "pass"
    can_be_approved = status == "pass"
    recommendation = "must_regenerate" if violations else "ready_for_approval"

    return ComplianceCheckResult(
        stage=stage,
        status=status,
        violations=violations,
        word_count=word_count,
        can_be_approved=can_be_approved,
        recommendation=recommendation
    )


# ============================================================================
# AGENT FUNCTION
# ============================================================================

def run_compliance_review_agent(
    campaign_name: str,
    campaign_type: str,
    channel: str,
    messages: Dict[str, Dict[str, Dict]],  # persona -> {M1: {message, word_count}, ...}
    prospect_name: str = "",
    company_name: str = "",
    trigger_telegram_approval: bool = False,
    telegram_user_id: int = 0
) -> ComplianceReviewAgentOutput:
    """
    Run compliance review across all personas and stages.

    Args:
        campaign_name: Campaign name
        campaign_type: Campaign type
        channel: Channel (email, whatsapp, linkedin)
        messages: Dict with structure: {persona: {M1: {message: str, word_count: int}, M2: {...}, M3: {...}}}
        prospect_name: Prospect name (for logging)
        company_name: Company name (for logging)
        trigger_telegram_approval: Send to Telegram if all pass?
        telegram_user_id: Telegram user ID for approval

    Returns:
        ComplianceReviewAgentOutput with compliance results and Telegram approval status
    """
    compliance_results: Dict[str, List[ComplianceCheckResult]] = {}
    all_violations: List[ComplianceViolation] = []

    # Check each persona's messages
    for persona, stages in messages.items():
        persona_results = []

        for stage in ["M1", "M2", "M3"]:
            if stage not in stages:
                continue

            stage_data = stages[stage]
            message_text = stage_data.get("message", "")
            word_count = stage_data.get("word_count", 0)

            result = check_message_compliance(
                message=message_text,
                channel=channel,
                stage=stage,
                word_count=word_count
            )

            persona_results.append(result)
            all_violations.extend(result.violations)

        compliance_results[persona] = persona_results

    # Determine overall status
    if not all_violations:
        overall_status = "all_pass"
    else:
        # Check if ALL are blocked
        all_blocked = all(
            result.status == "blocked"
            for persona_results in compliance_results.values()
            for result in persona_results
        )
        overall_status = "all_blocked" if all_blocked else "some_blocked"

    # Send to Telegram if all pass and requested
    telegram_approval_sent = False
    telegram_approval_id = ""

    if overall_status == "all_pass" and trigger_telegram_approval and telegram_user_id > 0:
        telegram_service = _import_telegram_service()

        if telegram_service:
            # Build preview from first message
            first_persona = next(iter(messages.keys()), None)
            if first_persona:
                preview_msg = messages[first_persona].get("M1", {}).get("message", "")[:300]
            else:
                preview_msg = "Messages ready for approval"

            approval_id = f"compliance_{campaign_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            success = telegram_service.send_approval_request(
                approval_id=approval_id,
                title=f"Compliance Approved - {campaign_name}",
                preview=preview_msg,
                telegram_user_id=telegram_user_id,
                approver_name="Compliance Review Agent",
                context_type="message",
                metadata={
                    "campaign_name": campaign_name,
                    "campaign_type": campaign_type,
                    "channel": channel,
                    "prospect_name": prospect_name,
                    "company_name": company_name
                }
            )

            if success:
                telegram_approval_sent = True
                telegram_approval_id = approval_id

    return ComplianceReviewAgentOutput(
        campaign_name=campaign_name,
        campaign_type=campaign_type,
        channel=channel,
        compliance_results=compliance_results,
        overall_status=overall_status,
        telegram_approval_sent=telegram_approval_sent,
        telegram_approval_id=telegram_approval_id,
        notes=f"Checked {len(compliance_results)} personas × 3 stages. Total violations: {len(all_violations)}"
    )


def create_compliance_review_agent():
    """Factory function for creating compliance review agent."""
    return {
        "run": run_compliance_review_agent,
        "check_message": check_message_compliance
    }
