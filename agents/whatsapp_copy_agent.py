"""WhatsApp Copy Agent — Generates conversational WhatsApp M1-M3 series from messaging strategy.

Production-ready implementation using frozen template structure.
Input from Message Strategy Agent (pain_points, primary_angle, value_prop) fills dynamic slots.

Output: M1 hook (pain + quick CTA) → M2 proof (insight) → M3 close (soft close).
Messages: short, conversational, WhatsApp-native (no subject lines, multiple follow-ups).
CTAs: quick, direct (30 min call, hour, review findings).
"""

import random
from typing import Dict, List, Any

from agents.schemas import WhatsAppDM, WhatsAppDMSeries, WhatsAppCopyAgentOutput


def generate_whatsapp_series(
    campaign_name: str,
    campaign_type: str,
    persona: str,
    primary_angle: str,
    pain_points: List[str],
    value_prop: str,
    tone: str,
    channel_guidance: str,
    target_region: str = "Global",
    target_industry: str = "Market",
    prospect_name: str = "",
    company_name: str = "",
    sender_name: str = "",
) -> Dict[str, Any]:
    """Generate WhatsApp M1-M3 series using frozen template structure.

    Short, conversational messages with quick CTAs and follow-ups.
    Faster cadence than email (Day 1, Day 2-3, Day 5-7).
    """

    prospect_first = prospect_name.split()[0] if prospect_name else "there"
    company_ref = company_name if company_name else "your organization"

    pain_point_primary = pain_points[0] if pain_points else "market challenges"
    pain_point_secondary = pain_points[1] if len(pain_points) > 1 else "operational efficiency"

    # Campaign context for WhatsApp opener
    campaign_context = {
        "Survey": f"research on {target_industry}",
        "POV": f"insights on {target_industry}",
        "Benchmarking": f"benchmarking in {target_industry}",
        "Competition Benchmarking": f"competitive analysis in {target_industry}",
        "Market Research": f"market trends in {target_industry}",
        "Expert Network": f"expert panel in {target_industry}",
        "Consulting": f"strategic work on {target_industry}",
        "Report Sales": f"intelligence on {target_industry}"
    }
    context = campaign_context.get(campaign_type, f"research on {target_industry}")

    # Template variants for tone variation
    variant = random.choice([1, 2])

    if variant == 1:
        # Variant 1: Direct insight opener
        m1_msg = f"Hi {prospect_first}, quick insight from our {context}:\n\n{pain_point_primary}\n\nWould you be open to a quick 30-min call to explore? We walk through what we found."
        m1_followups = [
            f"No pressure — just thought this mapped to {company_ref}.",
            f"Still interested in a quick chat?"
        ]

        m2_msg = f"Sample attached from our research. Shows {pain_point_primary} and how leaders are responding.\n\nWorth reviewing?"
        m2_followups = [
            "Let me know once you've had a chance to look."
        ]

        m3_msg = f"Either way, let's connect once. {pain_point_secondary} is shifting fast — worth aligning on how you're thinking about it.\n\nOpen to 30 min?"
        m3_followups = []

    else:
        # Variant 2: Context-first approach
        m1_msg = f"We finished {context}. Most leaders at {company_ref}'s level aren't tracking: {pain_point_primary}\n\nWorth a 30-min call to walk through what we found?"
        m1_followups = [
            "Companies ahead on this are already repositioning.",
            "Interested?"
        ]

        m2_msg = f"Sample from our research across {target_region}. You'll see the {pain_point_primary} pattern and how top performers differentiate.\n\nTake a look?"
        m2_followups = [
            "Let me know what stands out."
        ]

        m3_msg = f"Either way, let's talk once. {pain_point_secondary} is accelerating — companies ahead? Already moved. Worth 30 minutes to align on your approach."
        m3_followups = []

    return {
        "hook_statement": primary_angle,
        "M1": {
            "message": m1_msg,
            "word_count": len(m1_msg.split()),
            "send_day": "Day 1",
            "follow_ups": m1_followups
        },
        "M2": {
            "message": m2_msg,
            "word_count": len(m2_msg.split()),
            "send_day": "Day 2-3",
            "follow_ups": m2_followups
        },
        "M3": {
            "message": m3_msg,
            "word_count": len(m3_msg.split()),
            "send_day": "Day 5-7",
            "follow_ups": m3_followups
        },
        "cta_type": "quick_call",
        "notes": f"Template variant {variant}. Conversational WhatsApp tone, quick CTAs, faster cadence."
    }


def run_whatsapp_copy_agent(
    campaign_name: str,
    campaign_type: str,
    persona_strategies: Dict[str, Dict[str, Any]],
    messaging_strategy: Dict[str, Any],
    channel_guidance: Dict[str, str],
    target_personas: List[str],
    target_region: str = "Global",
    target_industry: str = "Market",
    prospect_name: str = "",
    company_name: str = "",
    sender_name: str = "",
) -> WhatsAppCopyAgentOutput:
    """Generate WhatsApp M1-M3 series for all target personas.

    Main exported function. Called from orchestrator or API.

    Args:
        campaign_name: Campaign name
        campaign_type: Campaign type
        persona_strategies: Per-persona strategies from Message Strategy Agent
        messaging_strategy: Overall messaging strategy
        channel_guidance: Channel-specific guidance
        target_personas: List of target personas
        target_region: Target region (default: Global)
        target_industry: Target industry (default: Market)
        prospect_name: Prospect name (optional)
        company_name: Company name (optional)
        sender_name: Sender name (optional)

    Returns:
        WhatsAppCopyAgentOutput with per-persona WhatsApp series
    """

    whatsapp_series = {}
    tone = messaging_strategy.get("tone", "conversational")
    whatsapp_channel_guidance = channel_guidance.get("whatsapp", "Conversational, quick insights")

    for persona in target_personas:
        if persona not in persona_strategies:
            continue

        persona_data = persona_strategies[persona]
        primary_angle = persona_data.get("primary_angle", "")
        pain_points = persona_data.get("pain_points", [])
        value_prop = persona_data.get("value_prop", "")

        # Generate DM series
        series_dict = generate_whatsapp_series(
            campaign_name=campaign_name,
            campaign_type=campaign_type,
            persona=persona,
            primary_angle=primary_angle,
            pain_points=pain_points,
            value_prop=value_prop,
            tone=tone,
            channel_guidance=whatsapp_channel_guidance,
            target_region=target_region,
            target_industry=target_industry,
            prospect_name=prospect_name,
            company_name=company_name,
            sender_name=sender_name,
        )

        # Convert to WhatsAppDMSeries object
        dm_series = WhatsAppDMSeries(
            M1=WhatsAppDM(
                message=series_dict["M1"]["message"],
                word_count=series_dict["M1"].get("word_count", len(series_dict["M1"]["message"].split())),
                send_day=series_dict["M1"].get("send_day", "Day 1"),
                follow_ups=series_dict["M1"].get("follow_ups", [])
            ),
            M2=WhatsAppDM(
                message=series_dict["M2"]["message"],
                word_count=series_dict["M2"].get("word_count", len(series_dict["M2"]["message"].split())),
                send_day=series_dict["M2"].get("send_day", "Day 2-3"),
                follow_ups=series_dict["M2"].get("follow_ups", [])
            ),
            M3=WhatsAppDM(
                message=series_dict["M3"]["message"],
                word_count=series_dict["M3"].get("word_count", len(series_dict["M3"]["message"].split())),
                send_day=series_dict["M3"].get("send_day", "Day 5-7"),
                follow_ups=series_dict["M3"].get("follow_ups", [])
            ),
            hook_statement=series_dict.get("hook_statement", primary_angle),
            cta_type=series_dict.get("cta_type", "quick_call")
        )

        whatsapp_series[persona] = dm_series

    output = WhatsAppCopyAgentOutput(
        campaign_name=campaign_name,
        campaign_type=campaign_type,
        whatsapp_series=whatsapp_series,
        channel_guidance=whatsapp_channel_guidance,
        notes="WhatsApp M1-M3 series: M1 hook > M2 proof > M3 close. Conversational tone, quick CTAs, follow-ups included."
    )

    return output


def create_whatsapp_copy_agent():
    """Factory function to create WhatsApp Copy Agent."""
    return run_whatsapp_copy_agent
