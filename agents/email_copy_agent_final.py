"""Email Copy Agent — Campaign-Type Aware (Market Research, Survey, Benchmarking, POV)."""

import json
import subprocess
from typing import Dict, List, Any

def call_claude_cli(prompt: str) -> str:
    """Call Claude via CLI."""
    try:
        result = subprocess.run(
            ["claude", "ask", prompt],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            raise RuntimeError(f"Claude CLI error: {result.stderr}")
        return result.stdout.strip()
    except FileNotFoundError:
        raise RuntimeError("Claude CLI not found")
    except subprocess.TimeoutExpired:
        raise RuntimeError("Claude CLI timeout")

def parse_email_sequence(claude_response: str) -> Dict[str, Any]:
    """Parse Claude response."""
    try:
        return json.loads(claude_response)
    except json.JSONDecodeError:
        return {"email_sequence": {}, "rationale": claude_response}

def get_campaign_type_rules(campaign_type: str) -> Dict[str, Any]:
    """Campaign-type specific rules for email generation."""

    rules = {
        "Market Research": {
            "hook_type": "whitespace or emerging niche",
            "m1_intent": "Market insight + positioning opportunity",
            "m2_intent": "Deepen market shift + competitive context",
            "m3_intent": "Research scope + peer benchmarks + strategic advantage",
            "m4_intent": "Partnership window closing + first-mover advantage",
            "tone_nuance": "consultative, insight-led, peer observer",
            "cta_style": "strategic conversation about positioning",
            "urgency": "mild (partnership windows, competitive positioning gap)",
        },
        "Survey": {
            "hook_type": "sweet spot or emerging niche",
            "m1_intent": "Buyer perception challenge + research scope",
            "m2_intent": "Deepen perception gaps + behavioral insight",
            "m3_intent": "Survey value + credibility + early access",
            "m4_intent": "Acquisition season window + perception clarity advantage",
            "tone_nuance": "professional, credibility-focused, data-driven",
            "cta_style": "feedback conversation + participation",
            "urgency": "moderate (acquisition season, research window)",
        },
        "Competition Benchmarking": {
            "hook_type": "sweet spot hook (competitive advantage)",
            "m1_intent": "Competitive cost/margin gap + urgency",
            "m2_intent": "Show margin impact + early movers ahead",
            "m3_intent": "Benchmarking offers + competitive position data",
            "m4_intent": "Optimization window closing + competitive gap widening",
            "tone_nuance": "competitive, margin-focused, urgent",
            "cta_style": "performance conversation + benchmarking access",
            "urgency": "high (margin erosion, competitive timing)",
        },
        "POV": {
            "hook_type": "emerging niche or trend",
            "m1_intent": "Strategic framework + thought leadership",
            "m2_intent": "Deepen POV logic + industry context",
            "m3_intent": "POV differentiation + exclusive perspective",
            "m4_intent": "Early adopter advantage + strategic window",
            "tone_nuance": "thought leadership, strategic, forward-looking",
            "cta_style": "strategy discussion + exclusive access",
            "urgency": "strategic (competitive positioning, market shift)",
        },
    }

    return rules.get(campaign_type, rules["Market Research"])

def generate_email_sequence(
    campaign_name: str,
    campaign_type: str,
    persona: str,
    primary_angle: str,
    pain_points: List[str],
    value_prop: str,
    call_to_action: str,
    tone: str,
    channel_guidance: str,
) -> Dict[str, Any]:
    """Generate email sequence with campaign-type awareness."""

    campaign_rules = get_campaign_type_rules(campaign_type)

    prompt = f"""Generate M1-M4 email sequence. Campaign-type specific. Return JSON only.

CAMPAIGN:
- Name: {campaign_name}
- Type: {campaign_type}
- Persona: {persona}

CAMPAIGN-TYPE RULES:
Hook: {campaign_rules['hook_type']}
M1: {campaign_rules['m1_intent']}
M2: {campaign_rules['m2_intent']}
M3: {campaign_rules['m3_intent']}
M4: {campaign_rules['m4_intent']}
Tone: {campaign_rules['tone_nuance']}
CTA Style: {campaign_rules['cta_style']}
Urgency: {campaign_rules['urgency']}

PRIMARY ANGLE: {primary_angle}
PAIN POINTS:
{chr(10).join(f'  • {p}' for p in pain_points)}

VALUE PROP: {value_prop}
CTA: {call_to_action}

CHANNEL GUIDANCE: {channel_guidance}

VOICE: Casual human tone. Peer to peer. Short punchy lines. NO dashes. NO formal openers. One CTA per message.

RESPONSE (JSON only):
{{
    "M1": {{"subject": "Hook subject (under 60 chars)", "body": "M1 body per intent..."}},
    "M2": {{"subject": "Re: [M1]", "body": "M2 body..."}},
    "M3": {{"subject": "Re: [M1]", "body": "M3 body..."}},
    "M4": {{"subject": "Re: [M1]", "body": "M4 body..."}},
    "personalization_vars": {{"first_name": "[name]", "company_name": "[company]"}},
    "campaign_type": "{campaign_type}",
    "notes": ""
}}"""

    try:
        claude_response = call_claude_cli(prompt)
        sequence = parse_email_sequence(claude_response)
        return sequence
    except Exception as e:
        return {
            "M1": {"subject": f"{primary_angle}", "body": f"Hi [first_name],\n\n{pain_points[0] if pain_points else ''}\n\nWorth discussing this week?"},
            "M2": {"subject": f"Re: {primary_angle}", "body": f"Following up on {primary_angle}..."},
            "M3": {"subject": f"Re: {primary_angle}", "body": f"{value_prop}"},
            "M4": {"subject": f"Re: {primary_angle}", "body": f"{call_to_action}"},
            "personalization_vars": {"first_name": "[name]", "company_name": "[company]"},
            "campaign_type": campaign_type,
            "error": str(e),
        }

def run_email_copy_agent(
    campaign_name: str,
    campaign_type: str,
    persona_strategies: Dict[str, Dict[str, Any]],
    messaging_strategy: Dict[str, Any],
    channel_guidance: str,
    target_personas: List[str],
) -> Dict[str, Any]:
    """Generate campaign-type-aware email sequences."""

    tone = messaging_strategy.get("tone", "professional")
    call_to_action = messaging_strategy.get("call_to_action", "Let's discuss")

    persona_emails = {}
    for persona in target_personas:
        persona_strat = persona_strategies.get(persona, {})
        sequence = generate_email_sequence(
            campaign_name=campaign_name,
            campaign_type=campaign_type,
            persona=persona,
            primary_angle=persona_strat.get("primary_angle", "Industry insight"),
            pain_points=persona_strat.get("pain_points", []),
            value_prop=persona_strat.get("value_prop", "Tailored solution"),
            call_to_action=call_to_action,
            tone=tone,
            channel_guidance=channel_guidance,
        )
        persona_emails[persona] = sequence

    return {
        "campaign_name": campaign_name,
        "campaign_type": campaign_type,
        "tone": tone,
        "email_sequences": persona_emails,
        "channel_guidance": channel_guidance,
        "pattern": "LinkedIn Skill Pattern (Campaign-Type Aware)",
        "notes": f"Email sequences for {campaign_type} campaign across {len(target_personas)} personas",
    }

def create_email_copy_agent():
    """Factory function."""
    return run_email_copy_agent
