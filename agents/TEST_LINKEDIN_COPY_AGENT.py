"""Test LinkedIn Copy Agent with 3 real-world campaign scenarios."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
from agents.linkedin_copy_agent import run_linkedin_copy_agent
from agents.schemas import LinkedInCopyOutput


def test_esports_market_research():
    """Test Case 1: Global Esports Market Research Campaign.

    Persona: Chief Strategy Officer
    Pain points: viewership monetization, sponsorship ROI tracking
    """
    print("\n" + "="*80)
    print("TEST 1: Global Esports Market Research")
    print("="*80)

    persona_strategies = {
        "cxo_strategy": {
            "primary_angle": "How leading esports studios are diversifying revenue beyond media rights",
            "pain_points": [
                "Media rights revenue plateau hitting most studios",
                "Sponsorship ROI tracking fragmented across multiple platforms",
                "Competition from traditional sports for sponsorship dollars intensifying"
            ],
            "value_prop": "Research on top 20 studios' revenue diversification strategies and sponsorship ROI measurement approaches"
        },
        "marketing": {
            "primary_angle": "Audience engagement strategies that drive both brand loyalty and sponsorship value",
            "pain_points": [
                "Fan engagement metrics not connected to sponsor value",
                "Content strategy disconnected from monetization opportunities",
                "Limited competitive intelligence on peer studios' engagement tactics"
            ],
            "value_prop": "Playbook on how top studios link fan engagement to sponsor activation and retention"
        }
    }

    messaging_strategy = {
        "tone": "consultative",
        "key_themes": ["revenue diversification", "sponsorship ROI", "competitive positioning"],
        "value_propositions": {
            "cxo_strategy": "Strategic insights on revenue diversification from peer studios",
            "marketing": "Tactical engagement strategies that drive sponsor value"
        },
        "call_to_action": "Schedule research walkthrough"
    }

    channel_guidance = {
        "email": "Thought leadership focused on revenue trends",
        "linkedin": "Peer-to-peer insights on industry monetization trends, data-backed",
        "whatsapp": "Quick research highlights with soft CTA"
    }

    result = run_linkedin_copy_agent(
        campaign_name="Global Esports Monetization Study",
        campaign_type="Market Research",
        persona_strategies=persona_strategies,
        messaging_strategy=messaging_strategy,
        channel_guidance=channel_guidance,
        target_personas=["cxo_strategy", "marketing"],
        target_region="Global",
        prospect_name="",
        company_name="",
        sender_name="Research Team"
    )

    print(f"\nCampaign: {result.campaign_name}")
    print(f"Type: {result.campaign_type}")
    print(f"Personas: {list(result.linkedin_series.keys())}")

    for persona, series in result.linkedin_series.items():
        print(f"\n--- Persona: {persona} ---")
        print(f"Hook: {series.hook_statement}")
        print(f"CTA Type: {series.cta_type}")

        print(f"\nM1 (Day 1):")
        print(f"  Message: {series.M1.message[:100]}...")
        print(f"  Words: {series.M1.word_count}")
        print(f"  Send: {series.M1.send_day}")

        print(f"\nM2 (Day 3-4):")
        print(f"  Message: {series.M2.message[:80]}...")
        print(f"  Words: {series.M2.word_count}")
        print(f"  Send: {series.M2.send_day}")

        print(f"\nM3 (Day 7-10):")
        print(f"  Message: {series.M3.message[:100]}...")
        print(f"  Words: {series.M3.word_count}")
        print(f"  Send: {series.M3.send_day}")

    print(f"\nNotes: {result.notes}")
    return result


def test_cold_chain_logistics():
    """Test Case 2: Cold Chain Logistics Competition Benchmarking.

    Persona: Operations Director
    Pain points: temperature control compliance, cost optimization
    """
    print("\n" + "="*80)
    print("TEST 2: Cold Chain Logistics - Competition Benchmarking")
    print("="*80)

    persona_strategies = {
        "operations": {
            "primary_angle": "How leading logistics providers cut cold chain costs while improving compliance",
            "pain_points": [
                "Temperature excursion incidents causing product loss and regulatory penalties",
                "Cold chain operational costs rising faster than revenue",
                "Manual temperature monitoring creating compliance reporting gaps"
            ],
            "value_prop": "Benchmarking study on cost-effective compliance strategies from peer logistics providers"
        }
    }

    messaging_strategy = {
        "tone": "data-led",
        "key_themes": ["compliance efficiency", "cost optimization", "operational benchmarking"],
        "value_propositions": {
            "operations": "Cost and compliance benchmarking against peer operators"
        },
        "call_to_action": "Access benchmarking findings"
    }

    channel_guidance = {
        "email": "Data-driven, ROI-focused",
        "linkedin": "Operational benchmarks, efficiency-focused insights",
        "whatsapp": "Quick stat share with follow-up CTA"
    }

    result = run_linkedin_copy_agent(
        campaign_name="Cold Chain Efficiency Benchmark",
        campaign_type="Competition Benchmarking",
        persona_strategies=persona_strategies,
        messaging_strategy=messaging_strategy,
        channel_guidance=channel_guidance,
        target_personas=["operations"],
        target_region="EMEA",
        prospect_name="Marcus",
        company_name="Pharma Logistics AG",
        sender_name="Logistics Research Team"
    )

    print(f"\nCampaign: {result.campaign_name}")
    print(f"Type: {result.campaign_type}")
    print(f"Target Region: EMEA")

    for persona, series in result.linkedin_series.items():
        print(f"\n--- Persona: {persona} ---")
        print(f"Hook: {series.hook_statement}")
        print(f"CTA Type: {series.cta_type}")

        print(f"\nM1 (Day 1):")
        print(f"  Message: {series.M1.message[:100]}...")
        print(f"  Words: {series.M1.word_count} (target: 80-120)")

        print(f"\nM2 (Day 3-4):")
        print(f"  Message: {series.M2.message[:80]}...")
        print(f"  Words: {series.M2.word_count} (target: 60-80)")

        print(f"\nM3 (Day 7-10):")
        print(f"  Message: {series.M3.message[:100]}...")
        print(f"  Words: {series.M3.word_count} (target: 80-100)")

    print(f"\nNotes: {result.notes}")
    return result


def test_k12_edtech_survey():
    """Test Case 3: K-12 EdTech Survey Campaign.

    Persona: District Chief Technology Officer
    Pain points: teacher retention, budget constraints, EdTech ROI
    """
    print("\n" + "="*80)
    print("TEST 3: K-12 EdTech - Teacher Retention Survey")
    print("="*80)

    persona_strategies = {
        "cxo_strategy": {
            "primary_angle": "How K-12 districts are solving teacher retention within flat budgets",
            "pain_points": [
                "Teacher turnover at 20-year high, creating curriculum continuity gaps",
                "Professional development budgets frozen or cut further",
                "Board pressure to prove ROI on any new retention initiatives"
            ],
            "value_prop": "Research findings on how peer districts implement cost-effective teacher retention programs"
        },
        "operations": {
            "primary_angle": "Operational levers districts are using to reduce teacher turnover without new spend",
            "pain_points": [
                "HR processes designed for stability, not retention in crisis periods",
                "Limited visibility into which teachers are at flight risk",
                "Mentoring and support programs fragmented across departments"
            ],
            "value_prop": "Operational best practices and implementation roadmap for district retention initiatives"
        }
    }

    messaging_strategy = {
        "tone": "professional",
        "key_themes": ["teacher retention", "budget optimization", "operational resilience"],
        "value_propositions": {
            "cxo_strategy": "Strategic approach to teacher retention aligned with board budget constraints",
            "operations": "Operational roadmap for implementing retention initiatives without new budgets"
        },
        "call_to_action": "Participate in research"
    }

    channel_guidance = {
        "email": "Professional, results-oriented, ROI-focused",
        "linkedin": "Peer insights on education sector challenges, thought leadership",
        "whatsapp": "Conversational, quick research invitation"
    }

    result = run_linkedin_copy_agent(
        campaign_name="K-12 Teacher Retention Research",
        campaign_type="Survey",
        persona_strategies=persona_strategies,
        messaging_strategy=messaging_strategy,
        channel_guidance=channel_guidance,
        target_personas=["cxo_strategy", "operations"],
        target_region="North America",
        prospect_name="Dr. Sarah Chen",
        company_name="Lincoln County Schools",
        sender_name="Education Research Team"
    )

    print(f"\nCampaign: {result.campaign_name}")
    print(f"Type: {result.campaign_type}")
    print(f"Personas: {list(result.linkedin_series.keys())}")

    for persona, series in result.linkedin_series.items():
        print(f"\n--- Persona: {persona} ---")
        print(f"Hook: {series.hook_statement}")
        print(f"CTA Type: {series.cta_type}")

        print(f"\nM1 (Day 1):")
        print(f"  Message: {series.M1.message[:100]}...")
        print(f"  Words: {series.M1.word_count} (target: 80-120)")
        # Check for specific CTA requirements
        m1_text = series.M1.message.lower()
        has_timeframe = any(x in m1_text for x in ["30-minute", "hour", "15 minute"])
        print(f"  Has timeframe in CTA: {has_timeframe}")

        print(f"\nM2 (Day 3-4):")
        print(f"  Message: {series.M2.message[:80]}...")
        print(f"  Words: {series.M2.word_count} (target: 60-80)")

        print(f"\nM3 (Day 7-10):")
        print(f"  Message: {series.M3.message[:100]}...")
        print(f"  Words: {series.M3.word_count} (target: 80-100)")
        # Check for "Either way" pattern
        m3_text = series.M3.message
        has_either_way = "either way" in m3_text.lower()
        print(f"  Opens with 'Either way': {has_either_way}")

    print(f"\nNotes: {result.notes}")
    return result


def verify_cta_quality(result: LinkedInCopyOutput) -> dict:
    """Verify CTA quality across all personas.

    Check:
    - M1 CTAs have specific timeframes
    - M1 CTAs include value exchange
    - M3 uses "Either way" opener
    - No generic language (compare notes, quick chat, etc.)
    """
    verification = {
        "total_personas": len(result.linkedin_series),
        "personas_checked": [],
        "all_pass": True,
        "issues": []
    }

    forbidden_phrases = ["compare notes", "quick chat", "happy to connect", "let me know", "worth a call"]

    for persona, series in result.linkedin_series.items():
        persona_check = {
            "persona": persona,
            "m1_has_timeframe": False,
            "m1_has_value_exchange": False,
            "m3_has_either_way": False,
            "no_generic_language": True,
            "pass": True
        }

        # Check M1
        m1_lower = series.M1.message.lower()
        persona_check["m1_has_timeframe"] = any(x in m1_lower for x in ["minute", "hour"])
        persona_check["m1_has_value_exchange"] = "walk through" in m1_lower or "we " in m1_lower

        # Check M3
        m3_lower = series.M3.message.lower()
        persona_check["m3_has_either_way"] = "either way" in m3_lower

        # Check all for forbidden phrases
        full_text = (series.M1.message + series.M2.message + series.M3.message).lower()
        for phrase in forbidden_phrases:
            if phrase in full_text:
                persona_check["no_generic_language"] = False
                verification["issues"].append(f"{persona}: Found forbidden phrase '{phrase}'")

        persona_check["pass"] = all([
            persona_check["m1_has_timeframe"],
            persona_check["m1_has_value_exchange"],
            persona_check["m3_has_either_way"],
            persona_check["no_generic_language"]
        ])

        if not persona_check["pass"]:
            verification["all_pass"] = False

        verification["personas_checked"].append(persona_check)

    return verification


if __name__ == "__main__":
    print("\n" + "="*80)
    print("LinkedIn Copy Agent Test Suite")
    print("="*80)

    # Run tests
    test1 = test_esports_market_research()
    test2 = test_cold_chain_logistics()
    test3 = test_k12_edtech_survey()

    # Verify CTA quality
    print("\n" + "="*80)
    print("CTA QUALITY VERIFICATION")
    print("="*80)

    for i, test_result in enumerate([test1, test2, test3], 1):
        print(f"\nTest {i}: {test_result.campaign_name}")
        verification = verify_cta_quality(test_result)
        print(f"  All CTAs pass quality checks: {verification['all_pass']}")
        print(f"  Personas checked: {verification['total_personas']}")
        for check in verification['personas_checked']:
            print(f"    {check['persona']}: {check['pass']} "
                  f"(timeframe={check['m1_has_timeframe']}, "
                  f"value_exchange={check['m1_has_value_exchange']}, "
                  f"either_way={check['m3_has_either_way']}, "
                  f"no_generic={check['no_generic_language']})")
        if verification['issues']:
            for issue in verification['issues']:
                print(f"    [ISSUE] {issue}")

    print("\n" + "="*80)
    print("Test Suite Complete")
    print("="*80)
