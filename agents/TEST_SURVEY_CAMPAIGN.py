"""Test Email Copy Agent V3 with Survey Campaign using LinkedIn Skill Pattern."""

from agents.email_copy_agent_v3 import run_email_copy_agent

campaign_data = {
    "campaign_name": "India Retail Investment Platforms — Investor Perception Study",
    "campaign_type": "Survey",
    "tone": "professional",
    "call_to_action": "Let's discuss how investor feedback can sharpen your platform positioning",
    "channel_guidance": "Credibility-focused. Reference real platforms (Zerodha, Bajaj Finserv). Data-driven. Lead with investor insight.",
    "persona_strategies": {
        "CXO": {
            "primary_angle": "Strategic platform differentiation in competitive retail investor space",
            "pain_points": [
                "Investor perception fragmented across platforms; hard to differentiate",
                "Competitor platforms stealing market share through trust narratives",
                "Unclear which features drive investor preference and retention"
            ],
            "value_prop": "Investor perception data reveals exactly what drives trust and loyalty, enabling sharper positioning against competitors"
        }
    },
    "target_personas": ["CXO"]
}

print("\n" + "="*120)
print("EMAIL COPY AGENT V3 — SURVEY CAMPAIGN TEST")
print("Pattern: LinkedIn Skill (M1: Ice Breaker, M2: Deepen, M3: Value Prop, M4: FOMO)")
print("="*120)

print(f"\n[CAMPAIGN INPUT]")
print(f"Campaign: {campaign_data['campaign_name']}")
print(f"Type: {campaign_data['campaign_type']}")
print(f"Persona: CXO")
print(f"Tone: {campaign_data['tone']}")

output = run_email_copy_agent(
    campaign_name=campaign_data['campaign_name'],
    campaign_type=campaign_data['campaign_type'],
    persona_strategies=campaign_data['persona_strategies'],
    messaging_strategy={"tone": campaign_data['tone'], "call_to_action": campaign_data['call_to_action']},
    channel_guidance=campaign_data['channel_guidance'],
    target_personas=campaign_data['target_personas']
)

for persona, email_seq in output['email_sequences'].items():
    print(f"\n\n{'='*120}")
    print(f"PERSONA: {persona}")
    print(f"Angle: {campaign_data['persona_strategies'][persona]['primary_angle']}")
    print(f"{'='*120}")
    
    for msg in ['M1', 'M2', 'M3', 'M4']:
        if msg in email_seq:
            data = email_seq[msg]
            print(f"\n{msg}\n{'-'*120}")
            print(f"Subject: {data.get('subject', '')}\n")
            print(data.get('body', ''))

print(f"\n\n{'='*120}")
print(f"SUMMARY")
print(f"{'='*120}")
print(f"Pattern: {output.get('pattern', '')}")
print(f"Campaign Type: {output['campaign_type']}")
print(f"Status: Ready for review")
