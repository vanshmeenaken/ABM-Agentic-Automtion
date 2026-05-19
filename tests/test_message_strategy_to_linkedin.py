"""Test: Message Strategy Agent (with deep market analysis) > LinkedIn Copy Agent flow.

Shows:
1. Message Strategy Agent analyzes market deeply
2. Generates persona-specific pain points + angles + value props
3. Passes to LinkedIn Copy Agent for M1-M3 series
4. Models: Strategy (Haiku) > Copy (Sonnet 4.6) > back to Haiku
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from agents.message_strategy_agent import run_message_strategy
from agents.linkedin_copy_agent import run_linkedin_copy_agent


def test_market_analysis_to_linkedin_series():
    """Test: K-12 EdTech campaign with market-aware LinkedIn series."""

    print("\n" + "="*80)
    print("TEST: Message Strategy (Market Analysis) > LinkedIn Copy Agent")
    print("="*80)

    campaign_name = "K-12 Teacher Retention Research"
    campaign_type = "Survey"
    target_industry = "K-12 Education"
    offer = "Research findings on cost-effective teacher retention strategies"
    target_personas = ["cxo_strategy", "operations"]
    channel_mix = ["email", "linkedin", "whatsapp"]

    # Step 1: Message Strategy Agent with deep market analysis
    print("\n[1] Running Message Strategy Agent (Haiku) - Market Analysis")
    print(f"    Campaign: {campaign_name}")
    print(f"    Industry: {target_industry}")
    print(f"    Personas: {', '.join(target_personas)}")

    strategy_output = run_message_strategy(
        campaign_name=campaign_name,
        campaign_type=campaign_type,
        offer=offer,
        target_industry=target_industry,
        target_personas=target_personas,
        channel_mix=channel_mix,
    )

    print("\n[2] Message Strategy Results:")
    print(f"    Tone: {strategy_output.messaging_strategy.tone}")
    print(f"    Key Themes: {', '.join(strategy_output.messaging_strategy.key_themes)}")
    print(f"    CTA: {strategy_output.messaging_strategy.call_to_action}")

    # Step 2: Build persona strategies from output
    persona_strategies = {}
    for persona in target_personas:
        if persona in strategy_output.persona_specific_messages:
            persona_data = strategy_output.persona_specific_messages[persona]
            persona_strategies[persona] = {
                "primary_angle": persona_data.primary_angle,
                "pain_points": persona_data.pain_points,
                "value_prop": persona_data.value_prop,
            }
            print(f"\n    [{persona}]")
            print(f"      Angle: {persona_data.primary_angle[:70]}...")
            print(f"      Pain Points: {len(persona_data.pain_points)} identified")
            if persona_data.pain_points:
                for i, pain in enumerate(persona_data.pain_points[:2], 1):
                    print(f"        {i}. {pain[:60]}...")

    # Step 3: LinkedIn Copy Agent with Sonnet 4.6
    print("\n[3] Running LinkedIn Copy Agent (Sonnet 4.6) for M1-M3 series")

    messaging_strategy_dict = {
        "tone": strategy_output.messaging_strategy.tone,
        "key_themes": strategy_output.messaging_strategy.key_themes,
        "value_propositions": strategy_output.messaging_strategy.value_propositions,
        "call_to_action": strategy_output.messaging_strategy.call_to_action,
    }

    linkedin_output = run_linkedin_copy_agent(
        campaign_name=campaign_name,
        campaign_type=campaign_type,
        persona_strategies=persona_strategies,
        messaging_strategy=messaging_strategy_dict,
        channel_guidance=strategy_output.channel_guidance,
        target_personas=target_personas,
        target_region="North America",
        prospect_name="Dr. Sarah Chen",
        company_name="Lincoln County Schools",
        sender_name="Education Research Team",
    )

    print(f"    Generated series for {len(linkedin_output.linkedin_series)} personas")

    # Step 4: Display final series
    print("\n[4] Final LinkedIn DM Series:")
    for persona, series in linkedin_output.linkedin_series.items():
        print(f"\n    --- {persona.upper()} ---")
        print(f"    Hook: {series.hook_statement[:60]}...")
        print(f"    CTA Type: {series.cta_type}")

        print(f"\n    M1 (Day 1 - Hook):")
        m1_lines = series.M1.message.split("\n")[:3]
        for line in m1_lines:
            if line.strip():
                print(f"      {line[:70]}...")

        print(f"\n    M2 (Day 3-4 - Proof):")
        m2_lines = series.M2.message.split("\n")[:2]
        for line in m2_lines:
            if line.strip():
                print(f"      {line[:70]}...")

        print(f"\n    M3 (Day 7-10 - Close):")
        m3_lines = series.M3.message.split("\n")[:2]
        for line in m3_lines:
            if line.strip():
                print(f"      {line[:70]}...")

        print(f"\n    Word Counts: M1={series.M1.word_count} | M2={series.M2.word_count} | M3={series.M3.word_count}")

    # Step 5: Quality checks
    print("\n[5] Series Quality Checks:")
    all_pass = True
    for persona, series in linkedin_output.linkedin_series.items():
        m1_lower = series.M1.message.lower()
        m3_lower = series.M3.message.lower()

        checks = {
            "M1 has timeframe": any(x in m1_lower for x in ["30 minutes", "30-minute", "hour", "15 minutes"]),
            "M1 has value exchange": "walk" in m1_lower,
            "M1 references prospect": "lincoln county" in m1_lower or "schools" in m1_lower,
            "M3 has Either way pattern": "either way" in m3_lower,
            "M3 has compare notes": "compare notes" in m3_lower,
        }

        persona_pass = all(checks.values())
        status = "[PASS]" if persona_pass else "[FAIL]"
        print(f"\n    {persona}: {status}")
        for check, result in checks.items():
            check_status = "[OK]" if result else "[X]"
            print(f"      {check_status} {check}")
            if not result:
                all_pass = False

    print("\n" + "="*80)
    if all_pass:
        print("RESULT: All quality checks PASSED")
    else:
        print("RESULT: Some checks failed - review above")
    print("="*80)

    return strategy_output, linkedin_output


if __name__ == "__main__":
    test_market_analysis_to_linkedin_series()
