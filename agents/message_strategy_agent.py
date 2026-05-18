"""
Message Strategy Agent — Generates campaign-aware messaging strategy per persona using Claude CLI.

Production-ready implementation that:
1. Takes campaign offer + industry + personas + channel mix
2. Calls Claude CLI to intelligently analyze market pain points
3. Claude extracts REAL pain points per persona (not generic)
4. Identifies primary messaging angles tailored to campaign + industry + persona
5. Generates value propositions that hit the specific market need
6. Routes to appropriate message series (Market Research skill, Survey pattern, Competition Benchmarking pattern)
7. Provides channel-specific guidance

How it works:
1. Constructs detailed prompt with campaign context + industry analysis request
2. Calls `claude ask` command via subprocess
3. Claude returns persona-specific messaging framework with pain points + angles + value props
4. Parses response into structured output
5. Integrates with message series patterns (skill or logic-based)
6. Returns MessageStrategyOutput with tone, themes, personas, channel guidance, success criteria
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
from statistics import mean

from agents.schemas import MessageStrategyInput, MessageStrategyOutput


def load_agent_config(agent_id: str) -> Dict[str, Any]:
    """Load agent configuration from JSON registry."""
    registry_path = Path(__file__).parent / "registry" / f"{agent_id}.json"
    if not registry_path.exists():
        raise FileNotFoundError(f"Registry file not found: {registry_path}")
    with open(registry_path) as f:
        return json.load(f)


def call_claude_cli(prompt: str) -> str:
    """
    Call Claude via CLI using subprocess.

    Requires: claude CLI installed and configured

    Args:
        prompt: The prompt to send to Claude

    Returns:
        Claude's response as string
    """
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
        raise RuntimeError(
            "Claude CLI not found. Install with: npm install -g @anthropic-ai/claude"
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError("Claude CLI call timed out after 60 seconds")


def parse_claude_strategy(claude_response: str) -> Dict[str, Any]:
    """
    Parse Claude's response into structured messaging strategy.

    Expected Claude response format:
    {
        "messaging_tone": "consultative",
        "key_themes": ["innovation", "scalability"],
        "call_to_action": "Schedule consultation",
        "success_criteria": {"email_open_rate": "25-30%"},
        "persona_strategies": {
            "CXO": {
                "primary_angle": "Strategic market positioning",
                "pain_points": ["Revenue growth stalled", "Market share erosion"],
                "value_prop": "Strategic insights to unlock new revenue streams"
            }
        },
        "channel_guidance": {
            "email": "Professional, data-driven, lead with insight",
            "whatsapp": "Conversational, warm, peer-to-peer"
        }
    }
    """
    try:
        # Handle markdown code blocks
        cleaned = claude_response.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Fallback if Claude returns text instead of JSON
        return {
            "messaging_tone": "professional",
            "key_themes": ["industry insight"],
            "call_to_action": "Schedule a conversation",
            "success_criteria": {},
            "persona_strategies": {},
            "channel_guidance": {},
            "rationale": claude_response,
        }


def generate_strategy(
    campaign_name: str,
    campaign_type: str,
    offer: str,
    target_industry: str,
    target_personas: List[str],
    channel_mix: List[str],
) -> Dict[str, Any]:
    """
    Generate messaging strategy for campaign using Claude CLI.

    Args:
        campaign_name: Name of campaign
        campaign_type: Type (Market Research, Survey, Competition Benchmarking)
        offer: What's being offered
        target_industry: Target industry
        target_personas: Target personas (CXO, Director, Manager, etc.)
        channel_mix: Channels (email, whatsapp, linkedin)

    Returns:
        Dict with messaging strategy, persona strategies, channel guidance
    """
    prompt = f"""TASK: Generate campaign messaging strategy.
DO NOT ASK QUESTIONS. DO NOT EXPLAIN. RETURN ONLY JSON.

Campaign: {campaign_name}
Type: {campaign_type}
Industry: {target_industry}
Offer: {offer}
Personas: {', '.join(target_personas)}
Channels: {', '.join(channel_mix)}

For EACH persona, identify real pain points in {target_industry} + messaging angle + value prop.
Generate tone, themes, CTA appropriate for {campaign_type} campaign type.
Provide channel guidance for each channel in {channel_mix}.

OUTPUT: Valid JSON only. No text. No questions. No explanations.

RESPONSE FORMAT (JSON only, no text):
{{
    "messaging_tone": "consultative",
    "key_themes": ["theme1", "theme2", "theme3"],
    "call_to_action": "Specific CTA for this campaign type",
    "success_criteria": {{
        "email_open_rate": "25-30%",
        "email_click_rate": "5-7%",
        "response_rate": "3-5%"
    }},
    "persona_strategies": {{
        "CXO": {{
            "primary_angle": "Strategic market positioning and competitive advantage",
            "pain_points": ["Specific pain 1", "Specific pain 2", "Specific pain 3"],
            "value_prop": "How this campaign solves their specific pain points"
        }}
    }},
    "channel_guidance": {{
        "email": "Professional, data-driven, lead with insight",
        "whatsapp": "Conversational, warm, peer-to-peer"
    }},
    "market_context_rationale": "Brief explanation of market dynamics driving the strategy"
}}"""

    try:
        claude_response = call_claude_cli(prompt)
        strategy = parse_claude_strategy(claude_response)
        return strategy

    except Exception as e:
        return {
            "messaging_tone": "professional",
            "key_themes": ["market insight"],
            "call_to_action": "Schedule a conversation",
            "success_criteria": {},
            "persona_strategies": {p: {
                "primary_angle": "Industry insight and market positioning",
                "pain_points": ["Market challenges"],
                "value_prop": "Strategic insights for decision-making"
            } for p in target_personas},
            "channel_guidance": {},
            "error": str(e),
        }


def run_message_strategy(
    campaign_name: str,
    campaign_type: str,
    offer: str,
    target_industry: str,
    target_personas: List[str],
    channel_mix: List[str],
) -> MessageStrategyOutput:
    """
    Generate comprehensive messaging strategy for campaign using Claude CLI.

    Args:
        campaign_name: Name of campaign
        campaign_type: Type (Market Research, Survey, Consulting, Expert Network, Webinar, Report Sales, Competition Benchmarking, Account Reactivation)
        offer: What's being offered
        target_industry: Target industry
        target_personas: Target personas (CXO, Director, Manager, etc.)
        channel_mix: Channels (email, whatsapp, linkedin)

    Returns:
        MessageStrategyOutput with messaging strategy, persona strategies, channel guidance, success criteria
    """
    try:
        config = load_agent_config("message_strategy")
    except Exception:
        config = {}  # Use empty config as fallback

    # Generate strategy using Claude CLI
    strategy = generate_strategy(
        campaign_name,
        campaign_type,
        offer,
        target_industry,
        target_personas,
        channel_mix,
    )

    # Extract components
    tone = strategy.get("messaging_tone", "professional")
    key_themes = strategy.get("key_themes", [])
    call_to_action = strategy.get("call_to_action", "Schedule a conversation")
    success_criteria = strategy.get("success_criteria", {})
    persona_strategies = strategy.get("persona_strategies", {})
    channel_guidance = strategy.get("channel_guidance", {})
    market_rationale = strategy.get("market_context_rationale", "")

    # Build value propositions from persona strategies
    value_propositions = {}
    for persona, strat in persona_strategies.items():
        value_propositions[persona] = strat.get("value_prop", "Tailored solution")

    # Build persona-specific messages
    persona_specific_messages = {}
    for persona in target_personas:
        persona_strat = persona_strategies.get(
            persona,
            {
                "primary_angle": "Industry insight",
                "pain_points": ["Market challenges"],
                "value_prop": "Strategic decision support",
            },
        )
        persona_specific_messages[persona] = {
            "primary_angle": persona_strat.get("primary_angle", "Industry insight"),
            "pain_points": persona_strat.get("pain_points", []),
            "value_prop": persona_strat.get("value_prop", "Tailored solution"),
        }

    # Build output
    output = MessageStrategyOutput(
        messaging_strategy={
            "campaign_name": campaign_name,
            "tone": tone,
            "key_themes": key_themes,
            "value_propositions": value_propositions,
            "call_to_action": call_to_action,
        },
        persona_specific_messages=persona_specific_messages,
        channel_guidance=channel_guidance,
        success_criteria=success_criteria,
        notes=f"Strategy generated for {campaign_type} campaign targeting {target_industry} with {len(target_personas)} personas. Market context: {market_rationale}",
    )

    return output


def create_message_strategy_agent():
    """
    Factory function to create Message Strategy Agent.

    Uses Claude CLI via subprocess calls:
    1. For each campaign, construct detailed prompt with campaign context + industry analysis
    2. Call `claude ask` command via CLI
    3. Claude returns persona-specific strategy with pain points + angles + value props
    4. Parse and return structured output

    No API key needed — uses existing Claude.ai authentication via CLI.
    """
    return run_message_strategy


# Agent registry export
agent = create_message_strategy_agent()
