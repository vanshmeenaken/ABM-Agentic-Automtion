"""LinkedIn Copy Agent — Campaign-Type Aware LinkedIn DM Series Generation."""

import json
import subprocess
from typing import Dict, List, Any

def call_claude_cli(prompt: str) -> str:
    """Call Claude via CLI."""
    try:
        claude_path = r"C:\Users\Vansh\AppData\Roaming\npm\claude.cmd"
        result = subprocess.run(
            [claude_path, "-p", prompt],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            raise RuntimeError(f"Claude CLI error: {result.stderr}")
        return result.stdout.strip()
    except FileNotFoundError:
        raise RuntimeError("Claude CLI not found")
    except subprocess.TimeoutExpired:
        raise RuntimeError("Claude CLI timeout")

def get_linkedin_hook_strategy(campaign_type: str) -> Dict[str, Any]:
    """Campaign-type to LinkedIn hook mapping."""

    strategies = {
        "Market Research": {
            "hook_priority": ["whitespace", "emerging_niche"],
            "hook_framing": "underserved_segment_or_trend",
            "variant_a_tone": "analytical_market_observation",
            "variant_b_tone": "competitive_early_mover",
            "urgency_signal": "partnership_window_narrowing",
            "m1_length": "3_short_paragraphs",
            "m2_vibe": "sample_as_credibility_proof",
            "m3_fallback": "peer_observation_not_pressure",
        },
        "Survey": {
            "hook_priority": ["sweet_spot", "whitespace"],
            "hook_framing": "insight_segment_perception_gap",
            "variant_a_tone": "analytical_perception_insight",
            "variant_b_tone": "early_data_competitive_advantage",
            "urgency_signal": "acquisition_season_window",
            "m1_length": "3_short_paragraphs",
            "m2_vibe": "sample_shows_perception_clarity",
            "m3_fallback": "peer_observation_on_perception",
        },
        "Competition Benchmarking": {
            "hook_priority": ["sweet_spot"],
            "hook_framing": "cost_margin_competitive_gap",
            "variant_a_tone": "analytical_competitive_position",
            "variant_b_tone": "urgent_margin_erosion_early_movers_ahead",
            "urgency_signal": "optimization_window_closing",
            "m1_length": "3_short_paragraphs",
            "m2_vibe": "sample_shows_margin_impact",
            "m3_fallback": "peer_observation_on_optimization",
        },
        "POV": {
            "hook_priority": ["emerging_niche", "whitespace"],
            "hook_framing": "strategic_trend_or_framework",
            "variant_a_tone": "analytical_thought_leadership",
            "variant_b_tone": "urgent_early_adopter_advantage",
            "urgency_signal": "strategic_positioning_window",
            "m1_length": "3_short_paragraphs",
            "m2_vibe": "sample_as_research_proof",
            "m3_fallback": "peer_observation_strategic",
        },
    }

    return strategies.get(campaign_type, strategies["Market Research"])

def generate_linkedin_messages(
    campaign_name: str,
    campaign_type: str,
    persona: str,
    primary_angle: str,
    pain_points: List[str],
    value_prop: str,
    tone: str,
    channel_guidance: str,
    target_region: str = "Global",
) -> Dict[str, Any]:
    """Generate LinkedIn M1 (2 variants), M2, M3 per persona."""

    hook_strategy = get_linkedin_hook_strategy(campaign_type)

    prompt = f"""Generate LinkedIn DM series (M1-2variants, M2, M3). LinkedIn DM voice only. NO dashes. Return JSON.

CAMPAIGN:
- Name: {campaign_name}
- Type: {campaign_type}
- Persona: {persona}
- Region: {target_region}

LINKEDIN HOOK STRATEGY:
- Hook Priority: {', '.join(hook_strategy['hook_priority'])}
- Hook Framing: {hook_strategy['hook_framing']}
- Variant A Tone: {hook_strategy['variant_a_tone']}
- Variant B Tone: {hook_strategy['variant_b_tone']}
- Urgency Signal: {hook_strategy['urgency_signal']}

PRIMARY ANGLE: {primary_angle}
PAIN POINTS:
{chr(10).join(f'  • {p}' for p in pain_points)}

VALUE PROP: {value_prop}

CHANNEL GUIDANCE: {channel_guidance}

VOICE: Casual LinkedIn DM. Peer to peer. Short punchy lines. NO dashes anywhere (no em, no en, no hyphen-as-pause). Natural cadence. One CTA per message.

RESPONSE (JSON only):
{{
    "hook_type": "whitespace OR sweet_spot OR emerging_niche",
    "hook_statement": "The one-line hook (no longer)",
    "M1": {{
        "variant_a": "3 short paragraphs. Analytical framing of hook.",
        "variant_b": "3 short paragraphs. Same hook, competitive urgency framing."
    }},
    "M2": "2-3 lines only. Reference M1. Signal sample attachment. [MANUAL INPUT: Sample/illustrative to attach]",
    "M3": "3 short paragraphs. Release pressure. Surface window or observation. Peer-to-peer fallback CTA.",
    "send_timing": {{"M1": "Day 1", "M2": "Day 3-4", "M3": "Day 7-10"}},
    "notes": "Campaign-type aware LinkedIn series"
}}"""

    try:
        claude_response = call_claude_cli(prompt)
        # Handle markdown code blocks
        cleaned = claude_response.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
        sequence = json.loads(cleaned)
        return sequence
    except Exception as e:
        # Fallback structure
        return {
            "hook_type": "whitespace",
            "hook_statement": primary_angle,
            "M1": {
                "variant_a": f"Hi [{persona}],\n\n{pain_points[0] if pain_points else primary_angle}\n\nWe mapped this in recent research. Worth a quick look?\n\nLet's connect around this week?",
                "variant_b": f"Hi [{persona}],\n\nCompanies are moving on {primary_angle}. Early movers positioning now will be in a different place in 12 months.\n\nWe researched this. Should compare notes?\n\nFree for a call this week?"
            },
            "M2": f"Hey [{persona}], sharing a sample from our research. Covers {value_prop}.\n\nLet's connect once you've had a look through it.",
            "M3": f"Hey [{persona}], no follow-up needed on the sample.\n\n{primary_angle} is real though. Companies tracking this now will be ahead.\n\nLet's compare notes on how you're thinking about it.",
            "send_timing": {"M1": "Day 1", "M2": "Day 3-4", "M3": "Day 7-10"},
            "error": str(e),
            "notes": "Fallback structure due to Claude CLI failure"
        }

def run_linkedin_copy_agent(
    campaign_name: str,
    campaign_type: str,
    persona_strategies: Dict[str, Dict[str, Any]],
    messaging_strategy: Dict[str, Any],
    channel_guidance: str,
    target_personas: List[str],
    target_region: str = "Global",
) -> Dict[str, Any]:
    """Generate LinkedIn series for all personas."""

    tone = messaging_strategy.get("tone", "professional")
    call_to_action = messaging_strategy.get("call_to_action", "Let's discuss")

    persona_messages = {}
    for persona in target_personas:
        persona_strat = persona_strategies.get(persona, {})
        messages = generate_linkedin_messages(
            campaign_name=campaign_name,
            campaign_type=campaign_type,
            persona=persona,
            primary_angle=persona_strat.get("primary_angle", "Industry insight"),
            pain_points=persona_strat.get("pain_points", []),
            value_prop=persona_strat.get("value_prop", "Tailored insight"),
            tone=tone,
            channel_guidance=channel_guidance,
            target_region=target_region,
        )
        persona_messages[persona] = messages

    return {
        "campaign_name": campaign_name,
        "campaign_type": campaign_type,
        "tone": tone,
        "linkedin_series": persona_messages,
        "channel_guidance": channel_guidance,
        "pattern": "LinkedIn DM Series (Campaign-Type Aware)",
        "structure": "M1 (2 variants: Analytical + Competitive Urgency) → M2 (Sample Share) → M3 (FOMO/Fallback)",
        "notes": f"LinkedIn DM series for {campaign_type} campaign across {len(target_personas)} personas",
    }

def create_linkedin_copy_agent():
    """Factory function."""
    return run_linkedin_copy_agent
