"""Test WhatsApp Copy Agent with 3 campaign scenarios."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.whatsapp_copy_agent import run_whatsapp_copy_agent


def test_market_research_esports():
    """Test: Global Esports Market Research campaign."""
    print("\n" + "="*80)
    print("TEST 1: Global Esports Market Research")
    print("="*80)

    output = run_whatsapp_copy_agent(
        campaign_name="Global Esports Monetization Study",
        campaign_type="Market Research",
        persona_strategies={
            "cxo_strategy": {
                "primary_angle": "How esports franchises are reshaping sponsorship monetization",
                "pain_points": [
                    "Sponsorship ROI uncertainty as traditional media metrics fail",
                    "Difficulty justifying premium pricing to sponsors",
                    "Strategic blind spot on emerging sponsor expectations"
                ],
                "value_prop": "Research-backed insights on sponsorship monetization"
            }
        },
        messaging_strategy={
            "tone": "conversational",
            "key_themes": ["esports sponsorship", "revenue optimization"],
            "value_propositions": {"cxo_strategy": "Strategic insights on sponsorship monetization"}
        },
        channel_guidance={
            "whatsapp": "Conversational, quick insights with CTA"
        },
        target_personas=["cxo_strategy"],
        target_region="Global",
        target_industry="Esports",
        prospect_name="Alex",
        company_name="FaZe Clan"
    )

    print(f"\nCampaign: {output.campaign_name}")
    print(f"Type: {output.campaign_type}")
    print(f"Channel Guidance: {output.channel_guidance}")

    for persona, series in output.whatsapp_series.items():
        print(f"\n--- Persona: {persona} ---")
        print(f"Hook: {series.hook_statement}")
        print(f"CTA Type: {series.cta_type}")

        print(f"\nM1 ({series.M1.send_day}, {series.M1.word_count} words):")
        print(series.M1.message)
        if series.M1.follow_ups:
            for i, fu in enumerate(series.M1.follow_ups, 1):
                print(f"  Follow-up {i}: {fu}")

        print(f"\nM2 ({series.M2.send_day}, {series.M2.word_count} words):")
        print(series.M2.message)
        if series.M2.follow_ups:
            for i, fu in enumerate(series.M2.follow_ups, 1):
                print(f"  Follow-up {i}: {fu}")

        print(f"\nM3 ({series.M3.send_day}, {series.M3.word_count} words):")
        print(series.M3.message)

    print(f"\nNotes: {output.notes}")
    return output


def test_competition_benchmarking_logistics() -> object:
    """Test: Cold Chain Logistics Competition Benchmarking."""
    print("\n" + "="*80)
    print("TEST 2: Cold Chain Logistics - Competition Benchmarking")
    print("="*80)

    output = run_whatsapp_copy_agent(
        campaign_name="Cold Chain Efficiency Benchmark",
        campaign_type="Competition Benchmarking",
        persona_strategies={
            "operations": {
                "primary_angle": "How leading logistics providers cut cold chain costs",
                "pain_points": [
                    "Temperature excursion incidents causing product loss",
                    "Cold chain operational costs rising faster than revenue",
                    "Manual temperature monitoring creating compliance gaps"
                ],
                "value_prop": "Benchmarking study on cost-effective compliance"
            }
        },
        messaging_strategy={
            "tone": "data-led",
            "key_themes": ["compliance efficiency", "cost optimization"],
            "value_propositions": {"operations": "Cost and compliance benchmarking"}
        },
        channel_guidance={
            "whatsapp": "Quick stat share with CTA"
        },
        target_personas=["operations"],
        target_region="EMEA",
        target_industry="Logistics",
        prospect_name="Marcus",
        company_name="Pharma Logistics AG"
    )

    print(f"\nCampaign: {output.campaign_name}")
    print(f"Type: {output.campaign_type}")

    for persona, series in output.whatsapp_series.items():
        print(f"\n--- Persona: {persona} ---")

        print(f"\nM1 ({series.M1.send_day}, {series.M1.word_count} words):")
        print(series.M1.message)

        print(f"\nM2 ({series.M2.send_day}, {series.M2.word_count} words):")
        print(series.M2.message)

        print(f"\nM3 ({series.M3.send_day}, {series.M3.word_count} words):")
        print(series.M3.message)

    return output


def test_survey_k12():
    """Test: K-12 EdTech Survey."""
    print("\n" + "="*80)
    print("TEST 3: K-12 EdTech - Teacher Retention Survey")
    print("="*80)

    output = run_whatsapp_copy_agent(
        campaign_name="K-12 Teacher Retention Research",
        campaign_type="Survey",
        persona_strategies={
            "cxo_strategy": {
                "primary_angle": "How K-12 districts are solving teacher retention",
                "pain_points": [
                    "Teacher turnover at 20-year high",
                    "Board pressure to prove ROI on retention initiatives",
                    "Strategic visibility gap on retention drivers"
                ],
                "value_prop": "Research insights on peer retention strategies"
            }
        },
        messaging_strategy={
            "tone": "professional",
            "key_themes": ["teacher retention", "budget optimization"],
            "value_propositions": {"cxo_strategy": "Strategic insights on teacher retention"}
        },
        channel_guidance={
            "whatsapp": "Conversational, quick research invitation"
        },
        target_personas=["cxo_strategy"],
        target_region="North America",
        target_industry="K-12 Education",
        prospect_name="Jennifer",
        company_name="Lincoln County Schools"
    )

    print(f"\nCampaign: {output.campaign_name}")
    print(f"Type: {output.campaign_type}")

    for persona, series in output.whatsapp_series.items():
        print(f"\n--- Persona: {persona} ---")

        print(f"\nM1 ({series.M1.send_day}, {series.M1.word_count} words):")
        print(series.M1.message)
        if series.M1.follow_ups:
            print("Follow-ups:")
            for fu in series.M1.follow_ups:
                print(f"  • {fu}")

        print(f"\nM2 ({series.M2.send_day}, {series.M2.word_count} words):")
        print(series.M2.message)

        print(f"\nM3 ({series.M3.send_day}, {series.M3.word_count} words):")
        print(series.M3.message)
        m3_has_either_way = "either way" in series.M3.message.lower()
        print(f"  Opens with 'Either way': {m3_has_either_way}")

    return output


def verify_cta_quality(output):
    """Verify CTA quality."""
    checks = {
        "m1_has_timeframe": False,
        "m2_proof": False,
        "m3_either_way": False,
        "no_generic": True
    }

    forbidden = ["compare notes", "quick chat", "happy to connect"]

    for series in output.whatsapp_series.values():
        m1_lower = series.M1.message.lower()
        checks["m1_has_timeframe"] = any(x in m1_lower for x in ["30-min", "hour", "15"])

        m2_lower = series.M2.message.lower()
        checks["m2_proof"] = "sample" in m2_lower or "research" in m2_lower

        m3_lower = series.M3.message.lower()
        checks["m3_either_way"] = "either way" in m3_lower

        full_text = (series.M1.message + series.M2.message + series.M3.message).lower()
        for phrase in forbidden:
            if phrase in full_text:
                checks["no_generic"] = False

    return checks


if __name__ == "__main__":
    print("\n" + "="*80)
    print("WhatsApp Copy Agent — Test Suite")
    print("="*80)

    test1 = test_market_research_esports()
    test2 = test_competition_benchmarking_logistics()
    test3 = test_survey_k12()

    print("\n" + "="*80)
    print("CTA QUALITY VERIFICATION")
    print("="*80)

    for i, test_output in enumerate([test1, test2, test3], 1):
        print(f"\nTest {i}: {test_output.campaign_name}")
        checks = verify_cta_quality(test_output)
        print(f"  M1 has timeframe: {checks['m1_has_timeframe']}")
        print(f"  M2 includes proof: {checks['m2_proof']}")
        print(f"  M3 uses 'Either way': {checks['m3_either_way']}")
        print(f"  No generic language: {checks['no_generic']}")
        all_pass = all(checks.values())
        print(f"  Overall: {'PASS' if all_pass else 'NEEDS WORK'}")

    print("\n" + "="*80)
    print("Test Suite Complete")
    print("="*80)
