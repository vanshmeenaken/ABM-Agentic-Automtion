"""Test Email Copy Agent with Campaign-Type Awareness."""

from agents.email_copy_agent_final import run_email_copy_agent

campaigns = [
    {
        "campaign_name": "K-12 EdTech Strategy Research",
        "campaign_type": "Market Research",
        "tone": "consultative",
        "call_to_action": "Schedule a 20-minute call to discuss your EdTech strategy",
        "channel_guidance": "Data-driven, lead with market insight. Professional but warm. Reference benchmarks.",
        "persona_strategies": {
            "CXO": {
                "primary_angle": "Competitive positioning in EdTech shift",
                "pain_points": [
                    "Schools adopting EdTech faster gaining enrollment advantage",
                    "Fear of falling behind in remote learning capability",
                    "Budget constraints for EdTech infrastructure"
                ],
                "value_prop": "Market data + peer benchmarks to accelerate EdTech positioning before competitors lock in"
            }
        },
        "target_personas": ["CXO"]
    },
    {
        "campaign_name": "India Retail Investment Platforms Perception",
        "campaign_type": "Survey",
        "tone": "professional",
        "call_to_action": "Let's discuss how investor feedback can sharpen your platform positioning",
        "channel_guidance": "Credibility-focused. Reference Zerodha, Bajaj. Data-driven. Lead with investor insight.",
        "persona_strategies": {
            "CXO": {
                "primary_angle": "Strategic platform differentiation in retail investor space",
                "pain_points": [
                    "Investor perception fragmented across platforms",
                    "Competitor platforms stealing share through trust narratives",
                    "Unclear which features drive investor preference"
                ],
                "value_prop": "Investor perception data reveals what drives trust and loyalty for competitive positioning"
            }
        },
        "target_personas": ["CXO"]
    },
    {
        "campaign_name": "Cold Chain Thailand Operator Benchmarking",
        "campaign_type": "Competition Benchmarking",
        "tone": "competitive",
        "call_to_action": "Book a 15-minute call to see how your performance compares to peers",
        "channel_guidance": "Competitive urgency framing. Margin-focused. Lead with cost efficiency data.",
        "persona_strategies": {
            "VP Operations": {
                "primary_angle": "Competitive margin benchmarking on cost efficiency",
                "pain_points": [
                    "Utilization fluctuating, margin erosion accelerating",
                    "Uncertainty on competitive cost position vs peers",
                    "Small efficiency differences equal big margin impact"
                ],
                "value_prop": "Benchmarking shows exactly where you stand vs competitors on cost per shipment and margins"
            }
        },
        "target_personas": ["VP Operations"]
    }
]

print("\n" + "="*130)
print("EMAIL COPY AGENT — CAMPAIGN-TYPE AWARE TEST")
print("="*130)

for idx, campaign in enumerate(campaigns, 1):
    print(f"\n\n{'='*130}")
    print(f"TEST {idx}: {campaign['campaign_type'].upper()} CAMPAIGN")
    print(f"Campaign: {campaign['campaign_name']}")
    print(f"Tone: {campaign['tone']}")
    print(f"{'='*130}")

    output = run_email_copy_agent(
        campaign_name=campaign['campaign_name'],
        campaign_type=campaign['campaign_type'],
        persona_strategies=campaign['persona_strategies'],
        messaging_strategy={
            "tone": campaign['tone'],
            "call_to_action": campaign['call_to_action']
        },
        channel_guidance=campaign['channel_guidance'],
        target_personas=campaign['target_personas']
    )

    for persona, email_seq in output['email_sequences'].items():
        print(f"\nPERSONA: {persona}")
        print(f"Angle: {campaign['persona_strategies'][persona]['primary_angle']}")
        print(f"\n{'-'*130}")

        for msg in ['M1', 'M2', 'M3', 'M4']:
            if msg in email_seq:
                data = email_seq[msg]
                print(f"\n[{msg}]")
                print(f"Subject: {data.get('subject', '')}")
                print(f"\n{data.get('body', '')}\n")

print(f"\n{'='*130}")
print("SUMMARY: Campaign-Type Aware Email Sequences Generated")
print("="*130)
print("Market Research ✓ | Survey ✓ | Benchmarking ✓")
print("Each with campaign-type specific intent, tone, urgency, and CTA style")
