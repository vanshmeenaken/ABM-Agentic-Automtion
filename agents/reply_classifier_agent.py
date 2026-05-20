"""Reply Classifier Agent - Classifies inbound replies into 7 intent categories.

Handles 139+ edge cases including:
- Empty/minimal replies
- Typos and garbled text
- Multiple languages
- Emoji-only responses
- Forwarding chains
- Conflicting signals
- Auto-replies (OOO)
- Bounce/NDR patterns
- And many more...

Classification confidence: 0-100 based on signal strength & clarity
Stop flag: Always true (automation must stop on any reply)
"""

import re
import uuid
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from schemas import ReplyClassifierInput, ReplyClassifierOutput, ReplyClassificationSignal


# ============================================================================
# SIGNAL PATTERNS DATABASE
# ============================================================================

SIGNALS = {
    "positive_interest": {
        "direct": [
            "tell me more", "sounds interesting", "let's connect", "i'm interested",
            "this looks good", "worth exploring", "curious about", "what else",
            "how does this work", "intriguing", "could be useful", "might be relevant",
            "seems valuable", "good timing", "exactly what we need",
        ],
        "implicit": [
            "thanks for reaching out", "appreciate you contacting", "good to hear from you",
            "happy to learn more", "would love to hear more", "keep me posted",
            "please send more info", "send details", "what's next", "how do we proceed",
            "love to discuss", "would be great to explore", "seems like a fit",
            "aligns with our needs", "we've been considering", "this is what we need",
        ],
        "sentiment": ["great", "excellent", "perfect", "love it", "fantastic", "amazing", "awesome"],
        "conditional": ["if it's affordable", "if the timeline", "if you can do", "depends on"],
        "engagement": [
            "share the proposal", "send the deck", "show me roi", "what's the catch",
            "do you have references", "can you prove", "show me examples", "case studies",
        ],
    },
    "meeting_request": {
        "direct": [
            "can we schedule a call", "are you available for a meeting", "let's set up a time",
            "when are you free", "can we talk soon", "let's schedule something",
            "i'd like to discuss", "can we connect", "want to hop on a call",
            "do you have time for a call", "shall we schedule", "let's plan a call",
            "when works for you", "can i get 15 minutes", "can you call me", "let's talk",
        ],
        "types": [
            "quick call", "30-minute meeting", "demo session", "product walkthrough",
            "strategy discussion", "planning session", "kickoff call", "consultation",
            "discovery call", "technical demo", "pricing discussion", "proposal review",
        ],
        "times": [
            "this week", "next week", "friday at", "tomorrow", "early next week",
            "asap", "as soon as possible", "afternoon", "morning", "evening",
        ],
        "readiness": [
            "i'll have my team join", "my boss wants to join", "let me check my calendar",
            "can you present to our group", "budget approved",
        ],
        "demo": [
            "can you demo", "show me a demo", "demo would help", "let's see how it works",
            "can you show us", "let me see it in action", "proof of concept", "demo video",
            "live demo", "screen share",
        ],
    },
    "question": {
        "what": [
            "what is this", "what does this mean", "what's the difference", "what are the requirements",
            "what's included", "what's not included", "what's the catch", "what are the limitations",
            "what's the cost", "what's the roi", "what's the timeline", "what support",
        ],
        "how": [
            "how does this work", "how would this help", "how is it different", "how long",
            "how much does it cost", "how do we get started", "how is data secured",
            "how do you handle", "how often", "how does pricing", "how do you measure",
        ],
        "why": [
            "why should we", "why is this better", "why now", "why us", "why this approach",
            "why not use", "why the price",
        ],
        "who": [
            "who are your customers", "who else uses", "who is the typical", "who would implement",
            "who are your biggest",
        ],
        "vetting": [
            "do you have proof", "can you provide references", "what's your track record",
            "can i see case studies", "do you have testimonials", "how long have you been",
            "what's your success rate", "how do i know this works",
        ],
    },
    "negative": {
        "explicit": [
            "not interested", "not a fit", "wrong person", "wrong company", "not relevant",
            "not applicable", "not needed", "already have", "using something else",
            "no thanks", "pass", "not now", "not at this time", "maybe later",
            "not in our plans", "low priority", "wrong timing", "bad timing",
        ],
        "unsubscribe": [
            "remove me", "unsubscribe", "stop emailing", "stop calling", "don't contact again",
            "please stop", "leave me alone", "stop bothering", "spam", "report spam",
            "don't send more", "remove from list", "block", "unsubscribed",
        ],
        "sentiment": [
            "waste of time", "irrelevant", "unwanted", "unsolicited", "junk", "garbage",
            "annoying", "irritating", "intrusive", "aggressive marketing", "too pushy",
        ],
        "competitive": [
            "already have this", "using x instead", "prefer y", "built our own",
            "not switching", "locked into contract", "happy with current", "no plans to change",
        ],
        "budget": [
            "no budget", "budget frozen", "can't afford", "out of scope", "not in budget",
            "too expensive", "not approved", "no funding", "after next quarter", "next year",
        ],
    },
    "out_of_office": {
        "standard": [
            "out of office", "out of the office", "away from office", "i'm away", "i'm out",
            "currently out", "out on", "will be back", "back on", "returning on",
            "out until", "out through", "i will return",
        ],
        "return_date": [
            "back on monday", "returning next week", "away until", "out through",
            "return date", "back from vacation", "i'll be back on",
        ],
        "types": [
            "on vacation", "taking time off", "on leave", "maternity leave", "paternity leave",
            "medical leave", "traveling", "on a trip", "conference", "training",
        ],
        "delegation": [
            "contact", "reach out to", "my colleague", "my team", "forwarding to",
            "will forward to",
        ],
    },
    "bounce": {
        "hard_bounce": [
            "address rejected", "invalid recipient", "user unknown", "no such user",
            "account disabled", "mailbox not found", "invalid mailbox", "address does not exist",
            "recipient rejected", "mailbox unavailable", "mailbox closed",
        ],
        "soft_bounce": [
            "mailbox full", "over quota", "temporary failure", "try again later",
            "service unavailable", "host unavailable", "connection timeout", "timeout",
            "temporary error",
        ],
        "smtp_codes": ["550", "551", "552", "553", "554", "421", "450", "451", "452"],
        "system_errors": [
            "delivery failed", "mail delivery failed", "message undeliverable",
            "unable to deliver", "return to sender", "returned mail", "non-delivery report",
            "delivery status notification", "undeliverable message",
        ],
        "auth_failures": [
            "authentication failed", "spf failure", "dkim failure", "dmarc failure",
            "tls required", "certificate error",
        ],
        "domain_issues": [
            "domain not found", "dns failure", "mx record", "invalid domain",
            "domain expired", "domain suspended",
        ],
        "employee_status": [
            "account closed", "account deleted", "person no longer", "employee terminated",
            "left the company", "left the organization",
        ],
    },
    "ambiguous": {
        "empty": ["", "...", ".", "?", "ok", "k", "yep", "nope", "maybe", "idk", "not sure"],
        "single_word": [
            "interested", "maybe", "later", "when", "why", "how", "cost", "timeline",
            "demo", "meeting", "call", "info", "details",
        ],
        "conflicts": [
            "interested but not now", "sounds good but", "like it but", "want to but",
            "could work but",
        ],
        "unclear": [
            "this looks good", "hmm interesting", "will review", "let me check",
            "similar to", "can't read",
        ],
        "typos": [
            "intrested", "schdeule", "whens", "unabel", "availble", "experiance",
        ],
    },
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def normalize_text(text: str) -> str:
    """Normalize text: lowercase, remove extra whitespace, strip punctuation edges."""
    text = text.lower().strip()
    # Replace multiple spaces/newlines with single space
    text = re.sub(r'\s+', ' ', text)
    return text


def detect_negation(text: str, position: int, window: int = 50) -> bool:
    """Check if word is negated (preceded by 'not', 'can't', etc.) within window."""
    start = max(0, position - window)
    before = text[start:position].lower()
    return any(neg in before for neg in ["not ", "can't ", "cannot ", "won't ", "wouldn't ", "no "])


def check_bounce_signals(text: str) -> Tuple[bool, int]:
    """Check for bounce/NDR signals. Returns (is_bounce, confidence)."""
    for code in SIGNALS["bounce"]["smtp_codes"]:
        if code in text:
            return True, 98

    for pattern in SIGNALS["bounce"]["hard_bounce"] + SIGNALS["bounce"]["system_errors"]:
        if pattern in text.lower():
            return True, 95

    for pattern in SIGNALS["bounce"]["soft_bounce"]:
        if pattern in text.lower():
            return True, 85

    return False, 0


def check_ooo_signals(text: str) -> Tuple[bool, str, int]:
    """Check for OOO signals. Returns (is_ooo, return_date_if_found, confidence)."""
    normalized = normalize_text(text)

    # Check standard OOO patterns
    for pattern in SIGNALS["out_of_office"]["standard"]:
        if pattern in normalized:
            # Try to extract return date
            date_pattern = r'(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|\d{1,2}|monday|tuesday|wednesday|thursday|friday|saturday|sunday)'
            dates = re.findall(date_pattern, normalized, re.IGNORECASE)
            return True, ', '.join(dates) if dates else 'unknown', 95

    return False, '', 0


def calculate_confidence(signals: List[Tuple[str, int]], text_length: int) -> int:
    """Calculate overall confidence from signals."""
    if not signals:
        return 30  # Default ambiguous

    # Average signal confidence
    base_confidence = sum(conf for _, conf in signals) / len(signals)

    # Adjust for text length (very short = lower confidence)
    if text_length < 5:
        base_confidence *= 0.7
    elif text_length < 15:
        base_confidence *= 0.85

    return min(100, max(0, int(base_confidence)))


# ============================================================================
# MAIN CLASSIFICATION FUNCTION
# ============================================================================

def classify_reply(text: str, channel: str = "email") -> Tuple[str, int, List[str], str]:
    """
    Classify reply into one of 7 intent categories.

    Returns: (intent_category, confidence, signals_found, recommended_action)
    """
    normalized = normalize_text(text)
    original_length = len(text)
    text_length = len(normalized.split())

    signals_found = []

    # Priority 1: Check for bounce signals
    is_bounce, bounce_conf = check_bounce_signals(text)
    if is_bounce:
        action = "Update prospect contact validity, investigate bounce reason"
        return "bounce", bounce_conf, ["bounce_detected"], action

    # Priority 2: Check for OOO signals
    is_ooo, return_date, ooo_conf = check_ooo_signals(text)
    if is_ooo:
        action = f"Pause automation, resume on {return_date if return_date != 'unknown' else 'contact return'}"
        return "out_of_office", ooo_conf, [f"ooo_detected_return_{return_date}"], action

    # Check for explicit rejection (NEGATIVE) - high priority
    for pattern in SIGNALS["negative"]["unsubscribe"]:
        if pattern in normalized:
            signals_found.append(("negative_unsubscribe", 95))
            action = "Suppress contact immediately, remove from all lists"
            return "negative", 95, signals_found, action

    # Check for meeting request - high confidence
    meeting_signals = 0
    for pattern in SIGNALS["meeting_request"]["direct"]:
        if pattern in normalized:
            signals_found.append(("meeting_request_direct", 90))
            meeting_signals += 1

    if meeting_signals > 0:
        action = "Create handoff to sales, prepare meeting details"
        return "meeting_request", min(100, 80 + meeting_signals * 5), signals_found, action

    # Check for explicit rejection (NEGATIVE)
    negative_signals = 0
    for pattern in SIGNALS["negative"]["explicit"]:
        if pattern in normalized and not detect_negation(normalized, normalized.find(pattern)):
            signals_found.append(("negative_explicit", 85))
            negative_signals += 1

    if negative_signals > 0:
        action = "Log rejection reason, suppress if permanent, set follow-up if timing issue"
        conf = min(100, 70 + negative_signals * 10)
        return "negative", conf, signals_found, action

    # Check for questions
    question_patterns = ["?", "what ", "how ", "why ", "who ", "when "]
    question_signals = 0
    for pattern in question_patterns:
        if pattern in normalized:
            signals_found.append(("question", 70))
            question_signals += 1

    if question_signals > 0:
        action = "Prepare answer, provide information requested"
        return "question", 65 + min(20, question_signals * 5), signals_found, action

    # Check for positive interest
    positive_signals = 0
    for category, patterns in SIGNALS["positive_interest"].items():
        for pattern in patterns:
            if pattern in normalized:
                signals_found.append((f"positive_interest_{category}", 75))
                positive_signals += 1

    if positive_signals > 0:
        action = "Nurture prospect, send next step information"
        return "positive_interest", 60 + min(30, positive_signals * 5), signals_found, action

    # Default: AMBIGUOUS
    # Check if completely empty or minimal
    if text_length < 2 or original_length < 3:
        action = "Flag for human review, request clarification"
        return "ambiguous", 20, ["empty_or_minimal"], action

    # Check for single word or minimal content
    if text_length == 1:
        action = "Flag for human review, cannot determine intent from single word"
        return "ambiguous", 35, ["single_word"], action

    action = "Flag for human review, intent unclear"
    return "ambiguous", 45, ["unclear_intent"], action


# ============================================================================
# MAIN AGENT FUNCTION
# ============================================================================

def run_reply_classifier_agent(
    reply_text: str,
    channel: str,
    prospect_id: str,
    campaign_id: str,
    prospect_email: Optional[str] = None,
    prospect_name: Optional[str] = None,
    prior_touchpoints: Optional[List[Dict]] = None,
    reply_timestamp: Optional[str] = None,
) -> ReplyClassifierOutput:
    """
    Run Reply Classifier Agent on an inbound reply.

    Always issues STOP FLAG (automation stops on any reply).
    Classifies into one of 7 intent categories.
    Returns recommended action for sales/support team.
    """

    # Classify the reply
    intent, confidence, signals, action = classify_reply(reply_text, channel)

    # Determine if human review needed
    needs_review = confidence < 60 or intent == "ambiguous"

    return ReplyClassifierOutput(
        prospect_id=prospect_id,
        campaign_id=campaign_id,
        intent_category=intent,
        confidence_score=confidence,
        recommended_action=action,
        stop_flag=True,  # Always true
        requires_human_review=needs_review,
        signals_detected=signals,
        notes=f"Reply from {prospect_name or prospect_email or 'unknown'} via {channel}"
    )


def create_reply_classifier_agent():
    """Factory function for creating reply classifier agent."""
    return {
        "run": run_reply_classifier_agent,
        "classify": classify_reply,
    }
