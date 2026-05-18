"""Email Copy Agent V2 — Generates threaded email sequences following LinkedIn series pattern."""

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
    """Generate email sequence following LinkedIn series voice + structure pattern."""
    
    prompt = f"""Generate M1-M4 threaded email sequence. Follow LinkedIn DM series voice + structure. Return JSON only.

CONTEXT:
- Campaign: {campaign_name} ({campaign_type})
- Persona: {persona}
- Tone: {tone}
- Angle: {primary_angle}

PAIN POINTS (address in sequence):
{chr(10).join(f'  • {p}' for p in pain_points)}

VALUE PROP: {value_prop}
CTA: {call_to_action}

CHANNEL GUIDANCE:
{channel_guidance}

VOICE RULES (Critical):
1. Casual, human-voice. Not salesy. No "comprehensive"/"cutting-edge"/"robust"
2. NO dashes anywhere (no em, en, or hyphen-as-dash). Use colons or split sentences only
3. Short punchy lines. Natural pauses. Like writing a peer DM
4. No formal openers/closings ("I hope this finds you well")
5. Write as peer, not vendor
6. No hollow adjectives
7. One CTA per message. Never stack two asks

STRUCTURE (LinkedIn series pattern adapted to email):

M1 = Message 1 (Ice Breaker): Hook on PAIN POINT as observation. Describe study/research. Propose time.
  • Paragraph 1: Hook (observation, not pitch). NO DASHES
  • Paragraph 2: What study covers (specific, not generic). Why timing matters
  • Paragraph 3: CTA only. Specific time ("this week", "Thursday")
  • Tone: Peer, insight-led
  • Length: 100-120 words

M2 = Message 2 (Deepen): Reference M1. Go deeper on pain/angle. No hard sell.
  • Paragraph 1: Light reference to M1 angle ("Following up on...")
  • Paragraph 2: Data or insight deepening the pain. Show impact
  • Paragraph 3: CTA. Soft. "Worth discussing"
  • Length: 130-150 words

M3 = Message 3 (Value Prop): Release pressure. Introduce research/offer. Add proof.
  • Paragraph 1: Release email pressure ("no pressure on prior messages")
  • Paragraph 2: What research/offer includes (specific, not generic). Who's in it
  • Paragraph 3: How it solves their pain. Social proof (peer examples)
  • Length: 160-180 words
  • CTA: Soft. "Worth exploring"

M4 = Message 4 (FOMO/Close): Window closing. Final fallback CTA.
  • Paragraph 1: Timing window/urgency (not pressure). "Moving on this now"
  • Paragraph 2: Fallback CTA. Peer-to-peer framing
  • Paragraph 3: Direct ask for meeting/call
  • Length: 100-120 words

RESPONSE FORMAT (JSON only):
{{
    "M1": {{"subject": "Hook as subject (under 60 chars)", "body": "..."}},
    "M2": {{"subject": "Re: [same]", "body": "..."}},
    "M3": {{"subject": "Re: [same]", "body": "..."}},
    "M4": {{"subject": "Re: [same]", "body": "..."}},
    "personalization_vars": {{"first_name": "[name]", "company_name": "[company]"}},
    "notes": "Hook type + structure notes"
}}

CRITICAL CHECKS:
- NO dashes anywhere. Rewrite any sentence with dash as dash
- M1 hook in opening line
- Each M2-M4 references previous ("Following up on...", "no pressure on...")
- Tone: casual peer voice, not sales email
- CTAs escalate: question → soft → proof → final ask
- Pain points addressed progressively across M1-M4"""

    try:
        claude_response = call_claude_cli(prompt)
        sequence = parse_email_sequence(claude_response)
        return sequence
    except Exception as e:
        return {
            "M1": {"subject": f"Quick question on {primary_angle}", "body": f"Hi [first_name],\n\n{pain_points[0] if pain_points else 'Let me reach out.'}\n\nWorth a conversation?"},
            "M2": {"subject": f"Re: Quick question on {primary_angle}", "body": f"Following up on {primary_angle}..."},
            "M3": {"subject": f"Re: Quick question on {primary_angle}", "body": f"{value_prop}"},
            "M4": {"subject": f"Re: Quick question on {primary_angle}", "body": f"{call_to_action}"},
            "personalization_vars": {"first_name": "[name]", "company_name": "[company]"},
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
    """Generate email sequences for all personas using LinkedIn series pattern."""
    
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
        "pattern": "LinkedIn Series (M1: Hook, M2: Deepen, M3: Offer, M4: FOMO)",
        "notes": f"Email sequences following LinkedIn DM voice + structure pattern for {len(target_personas)} personas",
    }

def create_email_copy_agent():
    """Factory function."""
    return run_email_copy_agent
