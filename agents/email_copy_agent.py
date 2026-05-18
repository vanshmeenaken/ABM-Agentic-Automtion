"""
Email Copy Agent — Generates threaded email sequences per persona using Claude CLI.

Production-ready implementation that:
1. Takes campaign context + persona strategies from Message Strategy Agent
2. Calls Claude CLI to generate M1-M4 threaded email sequence
3. Each email flows from previous (references, builds on context)
4. Pain point → angle → value prop → CTA narrative thread
5. Returns structured email sequences per persona
"""

import json
import subprocess
from typing import Dict, List, Any

def call_claude_cli(prompt: str) -> str:
    """Call Claude via CLI using subprocess."""
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
        raise RuntimeError("Claude CLI not found. Install with: npm install -g @anthropic-ai/claude")
    except subprocess.TimeoutExpired:
        raise RuntimeError("Claude CLI call timed out after 30 seconds")


def parse_email_sequence(claude_response: str) -> Dict[str, Any]:
    """Parse Claude response into structured email sequence."""
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
    """Generate threaded email sequence for single persona using Claude CLI."""
    
    prompt = f"""Generate a threaded email sequence (M1-M4) for this persona. Return JSON only.

CAMPAIGN CONTEXT:
- Campaign: {campaign_name}
- Type: {campaign_type}
- Persona: {persona}
- Tone: {tone}

PERSONA STRATEGY:
- Primary Angle: {primary_angle}
- Pain Points:
  {chr(10).join(f'  • {p}' for p in pain_points)}
- Value Proposition: {value_prop}

CHANNEL GUIDANCE:
{channel_guidance}

INSTRUCTIONS:
1. Generate M1-M4 emails that flow like threaded conversation (not separate emails)
2. Each email references/builds on previous ones
3. M1: Hook on pain point + introduce angle
4. M2: Deepen pain context, reinforce angle (reply to M1)
5. M3: Introduce value prop, add credibility/proof (reply to M1)
6. M4: Wrap up, final CTA + urgency (reply to M1)

TONE: {tone}
CTA: {call_to_action}

RESPONSE FORMAT (JSON only):
{{
    "M1": {{
        "subject": "Subject line (hook on pain point, under 60 chars)",
        "body": "Email body. Hook on pain point + angle. Under 200 words."
    }},
    "M2": {{
        "subject": "Re: [same subject as M1]",
        "body": "Reply in thread. Reference M1. Deepen pain. Reinforce angle. Under 200 words."
    }},
    "M3": {{
        "subject": "Re: [same subject as M1]",
        "body": "Reply in thread. Build on M1+M2. Introduce value prop + proof. Under 200 words."
    }},
    "M4": {{
        "subject": "Re: [same subject as M1]",
        "body": "Final reply. Wrap conversation. Final CTA. Under 150 words."
    }},
    "personalization_vars": {{"first_name": "[name]", "company_name": "[company]"}},
    "notes": "Brief notes"
}}"""

    try:
        claude_response = call_claude_cli(prompt)
        sequence = parse_email_sequence(claude_response)
        return sequence
    except Exception as e:
        return {
            "M1": {"subject": f"Regarding {primary_angle}", "body": f"Hi [first_name],\n\n{pain_points[0] if pain_points else 'Let me reach out.'}\n\n[Your name]"},
            "M2": {"subject": f"Re: Regarding {primary_angle}", "body": f"Following up on {primary_angle}..."},
            "M3": {"subject": f"Re: Regarding {primary_angle}", "body": f"{value_prop}"},
            "M4": {"subject": f"Re: Regarding {primary_angle}", "body": f"{call_to_action}"},
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
    """Generate email sequences for all target personas."""
    
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
        "notes": f"Email sequences generated for {len(target_personas)} personas",
    }


def create_email_copy_agent():
    """Factory function to create Email Copy Agent."""
    return run_email_copy_agent
