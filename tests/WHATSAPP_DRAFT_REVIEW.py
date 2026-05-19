"""Generate WhatsApp series draft for user review."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from agents.whatsapp_copy_agent import run_whatsapp_copy_agent

output = run_whatsapp_copy_agent(
    campaign_name='Survey_India Crop Protection Pesticides',
    campaign_type='Survey',
    persona_strategies={
        'cxo_strategy': {
            'primary_angle': 'How agrochemical companies are responding to dealer consolidation',
            'pain_points': [
                'Dealer NPS declining as farm consolidation shifts power to bundled-solution agrochemical majors',
                'Board-level margin compression threat from price wars and private label penetration across regions',
                'Strategic blind spot: agronomist vs farmer preference gaps creating pricing and positioning risk'
            ],
            'value_prop': 'Research insights on how competitors are winning dealer relationships'
        }
    },
    messaging_strategy={
        'tone': 'professional',
        'key_themes': ['dealer consolidation', 'margin compression', 'competitive positioning'],
        'value_propositions': {'cxo_strategy': 'Strategic insights on dealer relationship positioning'}
    },
    channel_guidance={
        'whatsapp': 'Conversational, quick insights'
    },
    target_personas=['cxo_strategy'],
    target_region='India',
    target_industry='Crop Protection Pesticides',
    prospect_name='Rajesh Kumar',
    company_name='Syngenta India'
)

print("=" * 80)
print("WHATSAPP SERIES DRAFT — Crop Protection Pesticides Survey")
print("=" * 80)
print(f"\nCampaign: {output.campaign_name}")
print(f"Type: {output.campaign_type}")
print(f"Prospect: Rajesh Kumar, Syngenta India")
print(f"Persona: cxo_strategy")
print("\n" + "=" * 80)

for persona, series in output.whatsapp_series.items():
    print(f"\nHook Statement: {series.hook_statement}")
    print(f"CTA Type: {series.cta_type}")

    print(f"\n--- M1 --- ({series.M1.send_day}, {series.M1.word_count} words)")
    print(f"\n{series.M1.message}")
    if series.M1.follow_ups:
        print(f"\nFollow-ups if no response:")
        for i, fu in enumerate(series.M1.follow_ups, 1):
            print(f"  {i}. {fu}")

    print(f"\n--- M2 --- ({series.M2.send_day}, {series.M2.word_count} words)")
    print(f"\n{series.M2.message}")
    if series.M2.follow_ups:
        print(f"\nFollow-up:")
        for fu in series.M2.follow_ups:
            print(f"  • {fu}")

    print(f"\n--- M3 --- ({series.M3.send_day}, {series.M3.word_count} words)")
    print(f"\n{series.M3.message}")

print("\n" + "=" * 80)
print(f"Notes: {output.notes}")
print("=" * 80)
