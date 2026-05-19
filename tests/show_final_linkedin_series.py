import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from agents.linkedin_copy_agent import run_linkedin_copy_agent

persona_strategies = {
    "cxo_strategy": {
        "primary_angle": "K-12 Education: Survey insights for Cxo Strategy",
        "pain_points": [
            "Teacher turnover at 20-year high, creating curriculum continuity gaps",
            "Board pressure to prove ROI on retention initiatives",
            "Professional development budgets frozen or cut further"
        ],
        "value_prop": "Research findings on how peer districts implement cost-effective teacher retention programs"
    }
}

messaging_strategy = {
    "tone": "consultative",
    "key_themes": ["k-12 education", "survey", "operational efficiency"],
    "value_propositions": {"cxo_strategy": "Research findings..."},
}

result = run_linkedin_copy_agent(
    campaign_name="K-12 Teacher Retention Research",
    campaign_type="Survey",
    persona_strategies=persona_strategies,
    messaging_strategy=messaging_strategy,
    channel_guidance={"linkedin": "Peer-to-peer, thought leadership"},
    target_personas=["cxo_strategy"],
    target_region="North America",
    prospect_name="Dr. Sarah Chen",
    company_name="Lincoln County Schools",
    sender_name="Education Research Team",
)

series = result.linkedin_series["cxo_strategy"]

print("="*80)
print("FINAL LINKEDIN DM SERIES - K-12 Teacher Retention Research")
print("="*80)
print(f"\nCampaign: {result.campaign_name}")
print(f"Type: {result.campaign_type}")
print(f"Prospect: Dr. Sarah Chen, Lincoln County Schools")
print(f"Persona: cxo_strategy (Chief Strategy Officer)")

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

m1_text = series.M1.message.lower()
m3_text = series.M3.message.lower()

checks = {
    "M1 has 30-minute call": any(x in m1_text for x in ["30 minutes", "30-minute"]),
    "M1 has value exchange (walk through)": "walk" in m1_text,
    "M1 references prospect context": "lincoln county" in m1_text or "schools" in m1_text,
    "M3 has Either way pattern": "either way" in m3_text,
    "M3 has compare notes": "compare notes" in m3_text,
    "Real pain points": "turnover" in m1_text or "roi" in m1_text,
}

all_pass = True
for check, passed in checks.items():
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} {check}")
    if not passed:
        all_pass = False

print("\n" + "="*80)
if all_pass:
    print("RESULT: All checks PASSED - Ready for deployment")
else:
    print("RESULT: Some checks failed - Review above")
print("="*80)
