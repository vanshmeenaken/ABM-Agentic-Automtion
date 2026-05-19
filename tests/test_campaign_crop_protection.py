import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from agents.message_strategy_agent import run_message_strategy
from agents.linkedin_copy_agent import run_linkedin_copy_agent

print("="*80)
print("TEST CAMPAIGN: Survey_India Crop Protection Pesticides")
print("="*80)

# Campaign details
campaign_name = "Survey_India Crop Protection Pesticides — Dealer NPS + Agronomist & Farmer U&A"
campaign_type = "Survey"
target_industry = "Crop Protection Pesticides"
offer = "Dealer NPS benchmarking + Agronomist/Farmer perception study"
target_personas = ["cxo_strategy", "marketing"]
channel_mix = ["email", "linkedin", "whatsapp"]

print(f"\nCampaign: {campaign_name}")
print(f"Type: {campaign_type}")
print(f"Industry: {target_industry}")
print(f"Offer: {offer}")
print(f"Personas: {', '.join(target_personas)}")

# Step 1: Message Strategy Agent
print("\n" + "-"*80)
print("[1] Running Message Strategy Agent")
print("-"*80)

strategy_output = run_message_strategy(
    campaign_name=campaign_name,
    campaign_type=campaign_type,
    offer=offer,
    target_industry=target_industry,
    target_personas=target_personas,
    channel_mix=channel_mix,
)

print(f"Tone: {strategy_output.messaging_strategy.tone}")
print(f"Key Themes: {', '.join(strategy_output.messaging_strategy.key_themes)}")
print(f"CTA: {strategy_output.messaging_strategy.call_to_action}")

# Build persona strategies
persona_strategies = {}
for persona in target_personas:
    if persona in strategy_output.persona_specific_messages:
        persona_data = strategy_output.persona_specific_messages[persona]
        persona_strategies[persona] = {
            "primary_angle": persona_data.primary_angle,
            "pain_points": persona_data.pain_points,
            "value_prop": persona_data.value_prop,
        }
        print(f"\n[{persona}]")
        print(f"  Angle: {persona_data.primary_angle[:60]}...")
        print(f"  Pain Points: {len(persona_data.pain_points)}")
        for i, pain in enumerate(persona_data.pain_points[:2], 1):
            print(f"    {i}. {pain[:55]}...")

# Step 2: LinkedIn Copy Agent
print("\n" + "-"*80)
print("[2] Running LinkedIn Copy Agent")
print("-"*80)

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
    target_region="India",
    prospect_name="Rajesh Kumar",
    company_name="Syngenta India",
    sender_name="Market Research Team",
)

print(f"Generated series for {len(linkedin_output.linkedin_series)} personas")

# Step 3: Display final series
print("\n" + "="*80)
print("FINAL LINKEDIN DM SERIES")
print("="*80)

for persona, series in linkedin_output.linkedin_series.items():
    print(f"\n[PERSONA: {persona}]")
    print(f"Hook: {series.hook_statement[:70]}...")
    print(f"CTA Type: {series.cta_type}")

    print(f"\n--- M1 (Day 1 - Hook) ---")
    print(series.M1.message)
    print(f"Word Count: {series.M1.word_count} | Send: {series.M1.send_day}")

    print(f"\n--- M2 (Day 3-4 - Proof) ---")
    print(series.M2.message)
    print(f"Word Count: {series.M2.word_count} | Send: {series.M2.send_day}")

    print(f"\n--- M3 (Day 7-10 - Close) ---")
    print(series.M3.message)
    print(f"Word Count: {series.M3.word_count} | Send: {series.M3.send_day}")

    # Quality checks
    print(f"\n--- Quality Checks ---")
    m1_lower = series.M1.message.lower()
    m3_lower = series.M3.message.lower()

    checks = {
        "M1 has timeframe": any(x in m1_lower for x in ["30 minutes", "30-minute", "hour", "15 minutes"]),
        "M1 has value exchange": "walk" in m1_lower,
        "M1 references prospect": "syngenta" in m1_lower or "india" in m1_lower,
        "M3 has Either way pattern": "either way" in m3_lower,
        "M3 has compare notes": "compare notes" in m3_lower,
        "Real pain points": not ("market challenges" in m1_lower and "operational efficiency" in m1_lower),
    }

    all_pass = all(checks.values())
    status = "[PASS]" if all_pass else "[FAIL]"
    print(f"{status} Series quality")
    for check, result in checks.items():
        check_status = "[OK]" if result else "[X]"
        print(f"  {check_status} {check}")

print("\n" + "="*80)
print("TEST COMPLETE")
print("="*80)
