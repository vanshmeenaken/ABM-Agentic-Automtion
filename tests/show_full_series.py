import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from agents.linkedin_copy_agent import run_linkedin_copy_agent

# Test 1: K-12 EdTech (clearest example with personalization)
persona_strategies = {
    "cxo_strategy": {
        "primary_angle": "How K-12 districts are solving teacher retention within flat budgets",
        "pain_points": [
            "Teacher turnover at 20-year high, creating curriculum continuity gaps",
            "Professional development budgets frozen or cut further",
            "Board pressure to prove ROI on any new retention initiatives"
        ],
        "value_prop": "Research findings on how peer districts implement cost-effective teacher retention programs"
    }
}

messaging_strategy = {
    "tone": "professional",
    "key_themes": ["teacher retention", "budget optimization"],
    "value_propositions": {
        "cxo_strategy": "Strategic approach to teacher retention aligned with budget constraints"
    },
}

channel_guidance = {
    "linkedin": "Peer insights on education sector challenges, thought leadership"
}

result = run_linkedin_copy_agent(
    campaign_name="K-12 Teacher Retention Research",
    campaign_type="Survey",
    persona_strategies=persona_strategies,
    messaging_strategy=messaging_strategy,
    channel_guidance=channel_guidance,
    target_personas=["cxo_strategy"],
    target_region="North America",
    prospect_name="Dr. Sarah Chen",
    company_name="Lincoln County Schools",
    sender_name="Education Research Team"
)

print("="*80)
print("FINAL LINKEDIN DM SERIES - K-12 EdTech Campaign")
print("="*80)
print(f"\nCampaign: {result.campaign_name}")
print(f"Type: {result.campaign_type}")
print(f"Prospect: Dr. Sarah Chen, Lincoln County Schools")
print(f"Persona: cxo_strategy (Chief Strategy Officer)")

series = result.linkedin_series["cxo_strategy"]

print(f"\n" + "-"*80)
print("M1 - DAY 1 (HOOK)")
print("-"*80)
print(f"\n{series.M1.message}")
print(f"\nWord Count: {series.M1.word_count} | Send: {series.M1.send_day}")

print(f"\n" + "-"*80)
print("M2 - DAY 3-4 (PROOF/SAMPLE)")
print("-"*80)
print(f"\n{series.M2.message}")
print(f"\nWord Count: {series.M2.word_count} | Send: {series.M2.send_day}")

print(f"\n" + "-"*80)
print("M3 - DAY 7-10 (LOW-PRESSURE CLOSE)")
print("-"*80)
print(f"\n{series.M3.message}")
print(f"\nWord Count: {series.M3.word_count} | Send: {series.M3.send_day}")

print(f"\n" + "="*80)
print("QUALITY CHECKS")
print("="*80)
print(f"Hook Statement: {series.hook_statement}")
print(f"CTA Type: {series.cta_type}")

# Verify quality
m1_text = series.M1.message.lower()
m3_text = series.M3.message.lower()

checks = {
    "M1 has 30-minute call": "30-minute" in m1_text,
    "M1 has value exchange (walk through)": "walk through" in m1_text,
    "M1 references prospect context": "maps to" in m1_text or "think" in m1_text,
    "M3 opens with Either way": m3_text.startswith("either way"),
    "M3 has fallback CTA": "hour" in m3_text,
    "No forbidden phrases": not any(phrase in (series.M1.message + series.M2.message + series.M3.message).lower()
                                     for phrase in ["compare notes", "quick chat", "happy to connect", "let me know", "worth a call"])
}

for check, passed in checks.items():
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} {check}")

print("\n" + "="*80)
