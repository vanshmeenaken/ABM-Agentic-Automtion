"""Live test of Email Copy Agent with real campaign data."""

import json
from agents.email_copy_agent import run_email_copy_agent

campaign_data = {
    "campaign_name": "India Retail Investment Platforms",
    "campaign_type": "Survey",
    "tone": "professional",
    "call_to_action": "Let's discuss how investor feedback can sharpen your platform positioning",
    "channel_guidance": "Credibility-focused. Reference Bajaj Finserv, Zerodha, Axis Bank cases. Professional, data-driven.",
    "persona_strategies": {
        "CXO": {
            "primary_angle": "Strategic platform differentiation in competitive retail investor space",
            "pain_points": [
                "Investor perception fragmented across platforms; hard to differentiate",
                "Competitor platforms stealing market share through trust narratives",
                "Unclear which features drive investor preference and retention"
            ],
            "value_prop": "Investor perception data reveals exactly what drives trust and loyalty, enabling sharper positioning against competitors"
        },
        "Director": {
            "primary_angle": "Platform enhancement priorities based on investor feedback",
            "pain_points": [
                "Product roadmap prioritization unclear; guessing at investor needs",
                "Feature requests not validated against actual investor pain points",
                "Competitor platforms adding features that resonate with investors"
            ],
            "value_prop": "Investor feedback reveals which platform enhancements will have highest impact on usage and retention"
        }
    },
    "target_personas": ["CXO", "Director"]
}

print("\n" + "="*110)
print("EMAIL COPY AGENT — LIVE TEST")
print("="*110)

print(f"\n[CAMPAIGN INPUT]")
print(f"Campaign: {campaign_data['campaign_name']}")
print(f"Type: {campaign_data['campaign_type']}")
print(f"Tone: {campaign_data['tone']}")
print(f"CTA: {campaign_data['call_to_action']}")
print(f"Personas: {', '.join(campaign_data['target_personas'])}")

print("\n" + "-"*110)
print("Generating email sequences...")
print("-"*110)

try:
    output = run_email_copy_agent(
        campaign_name=campaign_data['campaign_name'],
        campaign_type=campaign_data['campaign_type'],
        persona_strategies=campaign_data['persona_strategies'],
        messaging_strategy={
            "tone": campaign_data['tone'],
            "call_to_action": campaign_data['call_to_action']
        },
        channel_guidance=campaign_data['channel_guidance'],
        target_personas=campaign_data['target_personas']
    )

    for persona, email_seq in output['email_sequences'].items():
        print(f"\n\n{'='*110}")
        print(f"PERSONA: {persona}")
        print(f"{'='*110}")

        persona_strat = campaign_data['persona_strategies'][persona]
        print(f"\nPain Points:")
        for pain in persona_strat['pain_points']:
            print(f"  - {pain}")
        print(f"\nPrimary Angle: {persona_strat['primary_angle']}")
        print(f"Value Prop: {persona_strat['value_prop']}")

        for msg_stage in ['M1', 'M2', 'M3', 'M4']:
            if msg_stage in email_seq:
                msg_data = email_seq[msg_stage]
                print(f"\n{'-'*110}")
                print(f"[{msg_stage}]")
                print(f"{'-'*110}")
                subject = msg_data.get('subject', '')
                body = msg_data.get('body', '')
                print(f"Subject: {subject}")
                print(f"\nBody:\n{body}")

    print(f"\n\n{'='*110}")
    print("EMAIL COPY AGENT COMPLETE")
    print(f"{'='*110}")
    print(f"\nGenerated {len(output['email_sequences'])} persona sequences")
    print(f"Each with M1-M4 threaded emails")
    print(f"Status: [OK] Ready for review")

except Exception as e:
    print(f"\n[ERROR] {str(e)}")
    import traceback
    traceback.print_exc()
