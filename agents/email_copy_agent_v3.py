"""Email Copy Agent V3 — Uses LinkedIn Skill Pattern adapted to email format."""

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
    """Generate email sequence using LinkedIn Skill pattern adapted for email."""
    
    # Determine hook type based on campaign type
    hook_types = {
        "Market Research": "whitespace or emerging niche",
        "Survey": "sweet spot or emerging niche",
        "Competition Benchmarking": "sweet spot hook",
        "POV": "emerging niche"
    }
    hook_type = hook_types.get(campaign_type, "whitespace")
    
    prompt = f"""Generate M1-M4 email sequence using LinkedIn Skill pattern adapted to email. Return JSON only.

CAMPAIGN:
- Name: {campaign_name}
- Type: {campaign_type}
- Persona: {persona}
- Angle: {primary_angle}
- Tone: {tone}

PAIN POINTS:
{chr(10).join(f'  • {p}' for p in pain_points)}

VALUE PROP: {value_prop}
CTA: {call_to_action}

CHANNEL GUIDANCE: {channel_guidance}

PATTERN (LinkedIn Skill adapted to 4-email):

M1 = ICE BREAKER (Hook + Study + CTA)
  • Paragraph 1: Hook as observation (NOT pitch). Hook type: {hook_type}
  • Paragraph 2: What study covers (specific, not generic). Timing relevance.
  • Paragraph 3: CTA. Propose specific time ("this week" or day/time)
  • Length: 100-120 words
  • NO DASHES anywhere

M2 = SAMPLE SHARE / DEEPEN (Light reference + Specific insight + Soft CTA)
  • Paragraph 1: Light reference to M1 ("Following up on the {{angle}} we mentioned...")
  • Paragraph 2: Specific insight from study/research (not generic)
  • Paragraph 3: Soft CTA ("Worth discussing" or "Let's explore this")
  • Length: 120-140 words
  • NO DASHES anywhere

M3 = VALUE PROP (Research offer + Proof + Credibility)
  • Paragraph 1: What research includes (specific breakdown, not generic)
  • Paragraph 2: Who's in it (peer examples, if available) + how it solves pain
  • Paragraph 3: Early access benefit (4-week advantage, confidential access)
  • Length: 150-170 words
  • NO DASHES anywhere

M4 = FOMO / FALLBACK (Release pressure + Timing window + Peer CTA)
  • Paragraph 1: Release pressure ("no hard push here")
  • Paragraph 2: Timing window as heads-up (not sales push). Window closing.
  • Paragraph 3: Fallback CTA. Peer framing ("let's compare notes on...")
  • Length: 100-120 words
  • NO DASHES anywhere
  • End on networking note, not hard close

VOICE RULES (CRITICAL):
- Casual, human-voice. Peer to peer.
- Short punchy lines. Natural pauses.
- NO formal openers/closings ("I hope this finds you well")
- NO hollow adjectives ("comprehensive", "cutting-edge")
- One CTA per message ONLY
- NO dashes anywhere (em, en, hyphen). Use colons or split sentences.
- Write as peer observer, not vendor

RESPONSE FORMAT (JSON):
{{
    "M1": {{"subject": "Hook as subject (under 60 chars, compelling)", "body": "..."}},
    "M2": {{"subject": "Re: [reference M1]", "body": "..."}},
    "M3": {{"subject": "Re: [reference M1]", "body": "..."}},
    "M4": {{"subject": "Re: [reference M1]", "body": "..."}},
    "personalization_vars": {{"first_name": "[name]", "company_name": "[company]"}},
    "hook_type": "{hook_type}",
    "notes": "Follows LinkedIn Skill M1-M2-M3 pattern adapted to 4-email"
}}"""

    try:
        claude_response = call_claude_cli(prompt)
        sequence = parse_email_sequence(claude_response)
        return sequence
    except Exception as e:
        return {
            "M1": {"subject": f"{primary_angle}", "body": f"Hi [first_name],\n\n{pain_points[0] if pain_points else ''}\n\nWorth discussing this week?"},
            "M2": {"subject": f"Re: {primary_angle}", "body": f"Following up on {{primary_angle}}..."},
            "M3": {"subject": f"Re: {primary_angle}", "body": f"{value_prop}"},
            "M4": {"subject": f"Re: {primary_angle}", "body": f"{call_to_action}"},
            "personalization_vars": {"first_name": "[name]", "company_name": "[company]"},
            "hook_type": hook_type,
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
    """Generate email sequences using LinkedIn Skill pattern."""
    
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
        "pattern": f"LinkedIn Skill Pattern (M1: Ice Breaker, M2: Deepen, M3: Value Prop, M4: FOMO)",
        "notes": f"Email sequences for {len(target_personas)} personas",
    }

def create_email_copy_agent():
    """Factory function."""
    return run_email_copy_agent
