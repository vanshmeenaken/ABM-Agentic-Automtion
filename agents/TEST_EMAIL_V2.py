"""Test Email Copy Agent V2."""

from agents.email_copy_agent_v2 import run_email_copy_agent

campaign_data = {
    "campaign_name": "K-12 Learning Solutions",
    "campaign_type": "Market Research",
    "tone": "consultative",
    "call_to_action": "Schedule a 20-minute call to discuss your EdTech strategy",
    "channel_guidance": "Data-driven, lead with EdTech adoption trend insight. Professional but warm. Reference peer benchmarks.",
    "persona_strategies": {
        "CXO": {
            "primary_angle": "Competitive positioning in EdTech shift",
            "pain_points": [
                "Schools adopting EdTech faster are gaining enrollment advantage",
                "Fear of falling behind in remote learning capability",
                "Budget constraints for EdTech infrastructure"
            ],
            "value_prop": "Market data + peer benchmarks to accelerate EdTech positioning before competitors lock in partnerships"
        }
    },
    "target_personas": ["CXO"]
}

print("\n" + "="*110)
print("EMAIL COPY AGENT V2 — K-12 CAMPAIGN TEST")
print("="*110)

output = run_email_copy_agent(
    campaign_name=campaign_data['campaign_name'],
    campaign_type=campaign_data['campaign_type'],
    persona_strategies=campaign_data['persona_strategies'],
    messaging_strategy={"tone": campaign_data['tone'], "call_to_action": campaign_data['call_to_action']},
    channel_guidance=campaign_data['channel_guidance'],
    target_personas=campaign_data['target_personas']
)

for persona, email_seq in output['email_sequences'].items():
    for msg in ['M1', 'M2', 'M3', 'M4']:
        if msg in email_seq:
            data = email_seq[msg]
            print(f"\n[{msg}]")
            print(f"Subject: {data.get('subject', '')}")
            print(f"\n{data.get('body', '')}")
            print("-"*110)

print("\nPattern: LinkedIn Series Voice + Structure")
