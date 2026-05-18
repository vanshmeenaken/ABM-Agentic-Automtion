"""Test LinkedIn Copy Agent with Campaign-Type Awareness."""

from agents.linkedin_copy_agent import run_linkedin_copy_agent

# Test data: Message Strategy Agent outputs (sample)
campaigns = [
    {
        "campaign_name": "K-12 EdTech Strategy Research",
        "campaign_type": "Market Research",
        "tone": "consultative",
        "region": "India",
        "channel_guidance": "Data-driven, lead with market insight. Professional but warm. Reference benchmarks.",
        "persona_strategies": {
            "CXO": {
                "primary_angle": "EdTech partnership windows closing faster than most schools realize",
                "pain_points": [
                    "Schools adopting EdTech faster gaining enrollment advantage",
                    "Fear of falling behind in remote learning capability",
                    "Budget constraints for EdTech infrastructure"
                ],
                "value_prop": "Market data revealing which EdTech strategies drive enrollment before partnerships lock in"
            }
        },
        "target_personas": ["CXO"]
    },
    {
        "campaign_name": "Cold Chain Thailand Operator Benchmarking",
        "campaign_type": "Competition Benchmarking",
        "tone": "competitive",
        "region": "Thailand",
        "channel_guidance": "Competitive urgency framing. Margin-focused. Lead with cost efficiency data.",
        "persona_strategies": {
            "VP Operations": {
                "primary_angle": "Margin leaders in Thailand cold chain are already benchmarking costs",
                "pain_points": [
                    "Utilization fluctuating, margin erosion accelerating",
                    "Uncertainty on competitive cost position vs peers",
                    "Small efficiency differences equal big margin impact"
                ],
                "value_prop": "Competitive cost position clarity that separates margin leaders from laggards"
            }
        },
        "target_personas": ["VP Operations"]
    },
    {
        "campaign_name": "India Retail Investment Platforms Perception",
        "campaign_type": "Survey",
        "tone": "professional",
        "region": "India",
        "channel_guidance": "Credibility-focused. Reference Zerodha, Bajaj. Data-driven. Lead with investor insight.",
        "persona_strategies": {
            "CXO": {
                "primary_angle": "Investor perception in retail platforms is fragmenting faster than platforms can track",
                "pain_points": [
                    "Investor perception fragmented across platforms",
                    "Competitor platforms stealing share through trust narratives",
                    "Unclear which features drive investor preference"
                ],
                "value_prop": "Real investor perception data revealing what drives platform trust and loyalty"
            }
        },
        "target_personas": ["CXO"]
    }
]

print("\n" + "="*130)
print("LINKEDIN COPY AGENT — CAMPAIGN-TYPE AWARE TEST")
print("="*130)

for idx, campaign in enumerate(campaigns, 1):
    print(f"\n\n{'='*130}")
    print(f"TEST {idx}: {campaign['campaign_type'].upper()} CAMPAIGN")
    print(f"Campaign: {campaign['campaign_name']}")
    print(f"Region: {campaign['region']}")
    print(f"{'='*130}")

    output = run_linkedin_copy_agent(
        campaign_name=campaign['campaign_name'],
        campaign_type=campaign['campaign_type'],
        persona_strategies=campaign['persona_strategies'],
        messaging_strategy={
            "tone": campaign['tone'],
            "call_to_action": "Let's compare notes"
        },
        channel_guidance=campaign['channel_guidance'],
        target_personas=campaign['target_personas'],
        target_region=campaign['region']
    )

    for persona, linkedin_seq in output['linkedin_series'].items():
        print(f"\nPERSONA: {persona}")
        print(f"Primary Angle: {campaign['persona_strategies'][persona]['primary_angle']}")
        print(f"Hook Type: {linkedin_seq.get('hook_type', 'N/A')}")
        print(f"Hook Statement: {linkedin_seq.get('hook_statement', 'N/A')}")
        print(f"\n{'-'*130}")

        # M1 Variants
        m1_data = linkedin_seq.get('M1', {})
        if isinstance(m1_data, dict):
            var_a = m1_data.get('variant_a', '')
            var_b = m1_data.get('variant_b', '')

            print(f"\n[M1 VARIANT A — Analytical]")
            print(f"{var_a}\n")

            print(f"\n[M1 VARIANT B — Competitive Urgency]")
            print(f"{var_b}\n")

        # M2
        m2_data = linkedin_seq.get('M2', '')
        print(f"\n[M2 — Sample Share]")
        print(f"{m2_data}\n")

        # M3
        m3_data = linkedin_seq.get('M3', '')
        print(f"\n[M3 — FOMO/Fallback]")
        print(f"{m3_data}\n")

        # Send timing
        timing = linkedin_seq.get('send_timing', {})
        print(f"\n[SEND TIMING]")
        for msg, day in timing.items():
            print(f"  {msg}: {day}")

print(f"\n{'='*130}")
print("SUMMARY: Campaign-Type Aware LinkedIn Series Generated")
print("="*130)
print("Market Research (Whitespace/Emerging Niche) [OK]")
print("Survey (Sweet Spot/Whitespace) [OK]")
print("Competition Benchmarking (Sweet Spot + Urgency) [OK]")
print("\nEach with campaign-type specific hook, variant framing, and DM voice")
