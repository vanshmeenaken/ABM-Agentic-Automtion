"""Email Copy Agent — Generates B2B email M1-M3 series from LinkedIn copy structure."""

import json
import random
from typing import Dict, List, Any

from agents.schemas import EmailDM, EmailDMSeries, EmailCopyAgentOutput


def generate_email_series(
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
    """Generate email M1-M3 series using B2B email best practices."""

    prospect_first = prospect_name.split()[0] if prospect_name else "there"
    company_ref = company_name if company_name else "your organization"

    pain_point_primary = pain_points[0] if pain_points else "market challenges"
    pain_point_secondary = pain_points[1] if len(pain_points) > 1 else "operational efficiency"

    # Strategic research framing by campaign type
    research_framing_map = {
        "Survey": f"We recently finished a mandate on {target_industry}",
        "POV": f"We recently completed intelligence research on {target_industry}",
        "Benchmarking": f"We recently finished an intelligence report on {target_industry}",
        "Competition Benchmarking": f"We recently completed competitive intelligence on {target_industry}",
        "Market Research": f"We recently finished market intelligence on {target_industry}",
        "Expert Network": f"We recently curated expert intelligence on {target_industry}",
        "Consulting": f"We recently developed strategic intelligence on {target_industry}",
        "Report Sales": f"We recently compiled intelligence on {target_industry}"
    }
    research_framing = research_framing_map.get(campaign_type, f"We recently conducted research on {target_industry}")

    variant = random.choice([1, 2])

    if variant == 1:
        m1_subject = f"Most leaders missing: {pain_point_primary}"
        m1_preview = "But the companies ahead of the curve are moving fast"
        m1_body = f"""Hi {prospect_first},

{research_framing} {target_region}. While reviewing the findings, we discovered something most leaders at {company_ref}'s level aren't tracking yet:

{pain_point_primary}

The companies ahead? They're already moving on this. We walked competitors through what we found, and it shifted how they're positioning on {pain_point_secondary}.

Would you be open to a 30-minute call? We walk you through the full picture, and you tell us if it maps to what you're seeing.

Looking forward to connecting.

{sender_name if sender_name else 'Best'}"""

        m2_subject = f"Re: Most leaders missing: {pain_point_primary}"
        m2_preview = "See the patterns from companies moving first"
        m2_body = f"""Hi {prospect_first},

Attaching the sample from our findings across {target_region}.

You will see:
• {pain_point_primary}
• {pain_point_secondary}
• How top performers are already responding

Let me know what stands out. Happy to answer questions on anything in the sample.

{sender_name if sender_name else 'Best'}"""

        m3_subject = f"Re: Most leaders missing: {pain_point_primary}"
        m3_preview = "By Q3, this landscape could look very different"
        m3_body = f"""Hi {prospect_first},

No pressure if timing isn't right. But wanted to flag: we're seeing {pain_point_secondary} accelerate fast.

The leaders tracking {pain_point_primary}? Already repositioned. By Q3, the landscape could be very different.

Either way, worth 30 minutes to compare notes on how you're thinking about this.

{sender_name if sender_name else 'Best'}"""

    else:
        m1_subject = f"Window closing on {pain_point_secondary}"
        m1_preview = "Companies are moving now. Waiting isn't an option."
        m1_body = f"""Hi {prospect_first},

{research_framing} {target_region}. What stood out:

{pain_point_primary}

Most leaders at {company_ref}'s level aren't actively tracking this. But the ones who are? Already seeing competitive advantage.

We walked competitors through our findings — it changed how they're positioning on {pain_point_secondary}. Worth a 30-minute conversation to see if this maps to your situation?

{sender_name if sender_name else 'Best'}"""

        m2_subject = f"Re: Window closing on {pain_point_secondary}"
        m2_preview = "Sample: how top performers are handling this"
        m2_body = f"""Hi {prospect_first},

Attached: sample from our findings across {target_region}.

Shows:
• {pain_point_primary}
• {pain_point_secondary}
• Patterns from companies ahead of the curve

The third section shows how top performers are positioning differently. Worth reviewing.

{sender_name if sender_name else 'Best'}"""

        m3_subject = f"Re: Window closing on {pain_point_secondary}"
        m3_preview = "This won't wait. Your next move?"
        m3_body = f"""Hi {prospect_first},

Not going to follow up if timing isn't right now.

But: {pain_point_secondary}. We're seeing this shift accelerate month over month. Companies ahead? Already repositioned.

Either way, let's connect once and align on where you stand. Worth 30 minutes.

{sender_name if sender_name else 'Best'}"""

    return {
        "hook_statement": primary_angle,
        "M1": {
            "subject": m1_subject,
            "preview_text": m1_preview,
            "body": m1_body,
            "word_count": len(m1_body.split()),
            "send_day": "Day 1"
        },
        "M2": {
            "subject": m2_subject,
            "preview_text": m2_preview,
            "body": m2_body,
            "word_count": len(m2_body.split()),
            "send_day": "Day 3-4"
        },
        "M3": {
            "subject": m3_subject,
            "preview_text": m3_preview,
            "body": m3_body,
            "word_count": len(m3_body.split()),
            "send_day": "Day 7-10"
        },
        "cta_type": "schedule_call",
        "notes": f"Template: Variant {variant}"
    }


def run_email_copy_agent(
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
) -> EmailCopyAgentOutput:
    """Generate email M1-M3 series for all target personas."""

    email_series = {}
    tone = messaging_strategy.get("tone", "professional")
    email_channel_guidance = channel_guidance.get("email", "Data-driven, ROI-focused")

    for persona in target_personas:
        if persona not in persona_strategies:
            continue

        persona_data = persona_strategies[persona]
        primary_angle = persona_data.get("primary_angle", "")
        pain_points = persona_data.get("pain_points", [])
        value_prop = persona_data.get("value_prop", "")

        series_dict = generate_email_series(
            campaign_name=campaign_name,
            campaign_type=campaign_type,
            persona=persona,
            primary_angle=primary_angle,
            pain_points=pain_points,
            value_prop=value_prop,
            tone=tone,
            channel_guidance=email_channel_guidance,
            target_region=target_region,
            target_industry=target_industry,
            prospect_name=prospect_name,
            company_name=company_name,
            sender_name=sender_name,
        )

        dm_series = EmailDMSeries(
            M1=series_dict["M1"],
            M2=series_dict["M2"],
            M3=series_dict["M3"],
            hook_statement=series_dict.get("hook_statement", primary_angle),
            cta_type=series_dict.get("cta_type", "schedule_call")
        )

        email_series[persona] = dm_series

    output = EmailCopyAgentOutput(
        campaign_name=campaign_name,
        campaign_type=campaign_type,
        email_series=email_series,
        channel_guidance=email_channel_guidance,
        notes="Email M1-M3 series generated."
    )

    return output


def create_email_copy_agent():
    return run_email_copy_agent
