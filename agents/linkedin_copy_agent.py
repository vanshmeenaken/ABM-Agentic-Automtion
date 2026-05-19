"""LinkedIn Copy Agent — Generates market-aware LinkedIn DM series (M1-M3) per persona.

Production-ready implementation using frozen template structure with template variants.
Input from Message Strategy Agent (pain_points, primary_angle, value_prop) fills dynamic slots.

Output: M1 hook (pain + CTA) → M2 proof (sample) → M3 close ("Either way" + fallback CTA).
CTAs: specific timeframe + value exchange + context-aware (never generic language).
"""

import random
from typing import Dict, List, Any

from agents.schemas import LinkedInDMSeries, LinkedInCopyOutput


def generate_linkedin_series(
    campaign_name: str,
    campaign_type: str,
    persona: str,
    primary_angle: str,
    pain_points: List[str],
    value_prop: str,
    tone: str,
    channel_guidance: str,
    target_region: str = "Global",
    prospect_name: str = "",
    company_name: str = "",
    sender_name: str = "",
) -> Dict[str, Any]:
    """Generate LinkedIn M1-M3 DM series using frozen template structure.

    Production-ready implementation using template-based generation.
    Claude CLI integration available as future enhancement via build_linkedin_prompt/call_claude_cli.

    Args:
        campaign_name: Campaign name
        campaign_type: Campaign type (Market Research, Survey, etc.)
        persona: Target persona
        primary_angle: Market context/insight opener
        pain_points: [primary, secondary, tertiary] pain points
        value_prop: How offer solves pain
        tone: Tone guidance
        channel_guidance: LinkedIn-specific guidance
        target_region: Target region
        prospect_name: Prospect name (for personalization)
        company_name: Company name (for personalization)
        sender_name: Sender name (optional)

    Returns:
        Dict with M1, M2, M3 using frozen template structure
    """
    # Extract template variables
    prospect_first = prospect_name.split()[0] if prospect_name else "there"
    company_ref = company_name if company_name else "your organization"

    pain_point_primary = pain_points[0] if pain_points else "market challenges"
    pain_point_secondary = pain_points[1] if len(pain_points) > 1 else "operational efficiency"

    campaign_verbs = {
        "Survey": "conducting research on",
        "POV": "developing a strategic POV on",
        "Benchmarking": "benchmarking across",
        "Competition Benchmarking": "benchmarking competitive positioning in",
        "Market Research": "analyzing market trends in"
    }
    campaign_verb = campaign_verbs.get(campaign_type, "conducting research on")
    project_scope = f"{target_region} {primary_angle.lower()}"

    # Template variants for message freshness
    template_variant = random.choice([1, 2])

    if template_variant == 1:
        m1_msg = f"""Hi {prospect_first}, {pain_point_primary}.

We are {campaign_verb} {project_scope}. Our research addresses the gap between {pain_point_primary} and {pain_point_secondary}.

Would you be open to a 30-minute call? We walk you through what we found on how top performers approach this differently, and you tell us whether it maps to your {pain_point_secondary} at {company_ref}."""

        m2_msg = f"""Hey {prospect_first}, attaching a quick sample from our {campaign_type.lower()} across {project_scope}.

Shows the {pain_point_primary}, the {pain_point_secondary}, and how top performers differentiate.

Let's connect once you have had a look."""

        m3_msg = f"""Hey {prospect_first}, no follow-up needed on the sample. Timing may not be right.

One thing worth flagging: {pain_point_secondary}. The leaders tracking this are getting ahead on {pain_point_primary}.

Either way, let's connect once and explore how you're approaching {pain_point_secondary}."""
    else:
        m1_msg = f"""Hi {prospect_first}, we're seeing {pain_point_primary} become a critical issue right now.

We are {campaign_verb} {project_scope}. The research specifically captures {pain_point_secondary}, which most leaders we talk to aren't tracking yet.

Would you be open to a 30-minute call? We walk you through what we found on what differentiated players are doing, and you tell us whether it maps to your {pain_point_secondary} at {company_ref}."""

        m2_msg = f"""Hey {prospect_first}, attached is a sample from our {campaign_type.lower()} research across {project_scope}.

You'll see the {pain_point_primary}, the {pain_point_secondary}, and the pattern emerging among top performers.

Let's connect once you've reviewed it."""

        m3_msg = f"""Hey {prospect_first}, no follow-up needed. Timing may not be right.

One thing worth flagging though: {pain_point_secondary}. The companies ahead of the curve? They're already moving on {pain_point_primary}.

Either way, let's connect once and explore how you're approaching {pain_point_secondary}."""

    return {
        "hook_statement": primary_angle,
        "M1": {
            "message": m1_msg,
            "word_count": len(m1_msg.split()),
            "send_day": "Day 1"
        },
        "M2": {
            "message": m2_msg,
            "word_count": len(m2_msg.split()),
            "send_day": "Day 3-4"
        },
        "M3": {
            "message": m3_msg,
            "word_count": len(m3_msg.split()),
            "send_day": "Day 7-10"
        },
        "cta_type": "30_min_call",
        "notes": f"Template variant {template_variant}. Insight: {primary_angle[:50]}..."
    }


def run_linkedin_copy_agent(
    campaign_name: str,
    campaign_type: str,
    persona_strategies: Dict[str, Dict[str, Any]],
    messaging_strategy: Dict[str, Any],
    channel_guidance: Dict[str, str],
    target_personas: List[str],
    target_region: str = "Global",
    prospect_name: str = "",
    company_name: str = "",
    sender_name: str = "",
) -> LinkedInCopyOutput:
    """Generate LinkedIn DM series for all target personas.

    Main exported function. Called from orchestrator or API.

    Args:
        campaign_name: Campaign name
        campaign_type: Campaign type
        persona_strategies: Per-persona strategies from Message Strategy Agent
                            Format: {persona: {primary_angle, pain_points, value_prop}}
        messaging_strategy: Overall messaging strategy from Message Strategy Agent
                           Format: {tone, key_themes, value_propositions, call_to_action}
        channel_guidance: Channel-specific guidance (from Message Strategy Agent)
                         Format: {email: "...", whatsapp: "...", linkedin: "..."}
        target_personas: List of target personas (cxo_strategy, marketing, operations, etc.)
        target_region: Target region (default: Global)
        prospect_name: Prospect name (optional, for personalization)
        company_name: Company name (optional, for personalization)
        sender_name: Sender name (optional, for sign-off)

    Returns:
        LinkedInCopyOutput with campaign info + per-persona LinkedIn series
    """

    linkedin_series = {}

    # Get tone and LinkedIn channel guidance
    tone = messaging_strategy.get("tone", "peer-level")
    linkedin_channel_guidance = channel_guidance.get("linkedin", "Peer-to-peer, thought leadership")

    # Generate series per persona
    for persona in target_personas:
        if persona not in persona_strategies:
            continue

        persona_data = persona_strategies[persona]

        # Extract persona strategy details
        primary_angle = persona_data.get("primary_angle", "")
        pain_points = persona_data.get("pain_points", [])
        value_prop = persona_data.get("value_prop", "")

        # Generate DM series
        series_dict = generate_linkedin_series(
            campaign_name=campaign_name,
            campaign_type=campaign_type,
            persona=persona,
            primary_angle=primary_angle,
            pain_points=pain_points,
            value_prop=value_prop,
            tone=tone,
            channel_guidance=linkedin_channel_guidance,
            target_region=target_region,
            prospect_name=prospect_name,
            company_name=company_name,
            sender_name=sender_name,
        )

        # Convert to LinkedInDMSeries object
        dm_series = LinkedInDMSeries(
            M1={
                "message": series_dict["M1"]["message"],
                "word_count": series_dict["M1"].get("word_count", len(series_dict["M1"]["message"].split())),
                "send_day": series_dict["M1"].get("send_day", "Day 1")
            },
            M2={
                "message": series_dict["M2"]["message"],
                "word_count": series_dict["M2"].get("word_count", len(series_dict["M2"]["message"].split())),
                "send_day": series_dict["M2"].get("send_day", "Day 3-4")
            },
            M3={
                "message": series_dict["M3"]["message"],
                "word_count": series_dict["M3"].get("word_count", len(series_dict["M3"]["message"].split())),
                "send_day": series_dict["M3"].get("send_day", "Day 7-10")
            },
            hook_statement=series_dict.get("hook_statement", primary_angle),
            cta_type=series_dict.get("cta_type", "30_min_call")
        )

        linkedin_series[persona] = dm_series

    # Build output
    output = LinkedInCopyOutput(
        campaign_name=campaign_name,
        campaign_type=campaign_type,
        linkedin_series=linkedin_series,
        channel_guidance=linkedin_channel_guidance,
        notes="LinkedIn DM series: M1 hook > M2 proof > M3 close. No connection note. Send blank connection."
    )

    return output


def create_linkedin_copy_agent():
    """Factory function to create LinkedIn Copy Agent.

    Returns:
        run_linkedin_copy_agent function
    """
    return run_linkedin_copy_agent
