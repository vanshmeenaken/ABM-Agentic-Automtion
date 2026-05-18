"""Real Campaign Test: India Gaming Market → Message Strategy → LinkedIn Series."""

from agents.message_strategy_agent import run_message_strategy
from agents.linkedin_copy_agent import run_linkedin_copy_agent

# Real campaign: India Gaming Market
campaign_input = {
    "campaign_name": "India Gaming Market Expansion Strategy",
    "campaign_type": "Market Research",
    "target_industry": "Gaming & Interactive Entertainment",
    "target_region": "India",
    "target_persona": "VP Product, VP Strategy, CXO",
    "offer": "Market intelligence on India's gaming market expansion, player monetization patterns, and competitive positioning",
    "preferred_channels": ["email", "linkedin"],
    "notes": "Focus on indie game studios and mid-size gaming companies expanding into India"
}

print("\n" + "="*130)
print("REAL CAMPAIGN TEST: INDIA GAMING MARKET")
print("="*130)
print(f"\nCampaign: {campaign_input['campaign_name']}")
print(f"Type: {campaign_input['campaign_type']}")
print(f"Target Industry: {campaign_input['target_industry']}")
print(f"Region: {campaign_input['target_region']}")
print(f"Personas: {campaign_input['target_persona']}")

# Step 1: Run Message Strategy Agent
print(f"\n{'='*130}")
print("STEP 1: MESSAGE STRATEGY AGENT")
print("="*130)

message_strategy_output = run_message_strategy(
    campaign_name=campaign_input['campaign_name'],
    campaign_type=campaign_input['campaign_type'],
    target_industry=campaign_input['target_industry'],
    target_personas=campaign_input['target_persona'].split(', '),
    offer=campaign_input['offer'],
    channel_mix=campaign_input['preferred_channels']
)

print(f"Overall Tone: {message_strategy_output.messaging_strategy.tone}")
print(f"Key Themes: {', '.join(message_strategy_output.messaging_strategy.key_themes[:3])}")

# Extract persona strategies for LinkedIn agent
persona_strategies = {}
for persona_name, persona_data in message_strategy_output.persona_specific_messages.items():
    persona_strategies[persona_name] = {
        "primary_angle": persona_data.primary_angle,
        "pain_points": persona_data.pain_points,
        "value_prop": persona_data.value_prop
    }

print(f"\nPersonas Identified:")
for persona in persona_strategies.keys():
    print(f"  • {persona}")
    print(f"    - Primary Angle: {persona_strategies[persona]['primary_angle'][:70]}...")
    print(f"    - Pain Points: {len(persona_strategies[persona]['pain_points'])} identified")

# Step 2: Run LinkedIn Copy Agent with Message Strategy output
print(f"\n{'='*130}")
print("STEP 2: LINKEDIN COPY AGENT (Feeds from Message Strategy)")
print("="*130)

linkedin_output = run_linkedin_copy_agent(
    campaign_name=campaign_input['campaign_name'],
    campaign_type=campaign_input['campaign_type'],
    persona_strategies=persona_strategies,
    messaging_strategy={
        "tone": message_strategy_output.messaging_strategy.tone,
        "call_to_action": "Let's discuss your India gaming expansion strategy"
    },
    channel_guidance=message_strategy_output.channel_guidance.get("linkedin", "") if message_strategy_output.channel_guidance else "",
    target_personas=list(persona_strategies.keys()),
    target_region=campaign_input['target_region']
)

# Step 3: Display Final LinkedIn Series
print(f"\n{'='*130}")
print("FINAL LINKEDIN SERIES OUTPUT")
print("="*130)

for persona, linkedin_series in linkedin_output['linkedin_series'].items():
    print(f"\n\n{'='*130}")
    print(f"PERSONA: {persona}")
    print(f"{'='*130}")

    print(f"\nPrimary Angle: {persona_strategies[persona]['primary_angle']}")
    print(f"Hook Type: {linkedin_series.get('hook_type', 'N/A')}")
    print(f"Hook: {linkedin_series.get('hook_statement', 'N/A')}")

    print(f"\n{'-'*130}")
    print("MESSAGE 1 — VARIANT A (Analytical Framing)")
    print(f"{'-'*130}")
    m1_data = linkedin_series.get('M1', {})
    if isinstance(m1_data, dict):
        print(m1_data.get('variant_a', 'N/A'))

    print(f"\n{'-'*130}")
    print("MESSAGE 1 — VARIANT B (Competitive Urgency Framing)")
    print(f"{'-'*130}")
    if isinstance(m1_data, dict):
        print(m1_data.get('variant_b', 'N/A'))

    print(f"\n{'-'*130}")
    print("MESSAGE 2 — Sample Share")
    print(f"{'-'*130}")
    m2_data = linkedin_series.get('M2', '')
    print(m2_data)

    print(f"\n{'-'*130}")
    print("MESSAGE 3 — FOMO / Fallback")
    print(f"{'-'*130}")
    m3_data = linkedin_series.get('M3', '')
    print(m3_data)

    print(f"\n[SEND TIMING]")
    timing = linkedin_series.get('send_timing', {})
    for msg, day in timing.items():
        print(f"  {msg}: {day}")

print(f"\n\n{'='*130}")
print("SUMMARY")
print("="*130)
print(f"Campaign: {campaign_input['campaign_name']}")
print(f"Message Strategy Output: COMPLETE (Tone + Themes + Personas)")
print(f"LinkedIn Series: COMPLETE (M1 Variants + M2 + M3 per persona)")
print(f"Status: Ready for campaign")
print(f"{'='*130}\n")
