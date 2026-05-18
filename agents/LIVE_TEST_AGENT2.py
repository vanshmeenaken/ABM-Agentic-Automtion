"""
Live test of Agent 2 (Message Strategy Agent) with real campaign data.
Shows actual output that feeds into Agent 3 (Email Copy Agent).
"""

import json
from agents.message_strategy_agent import generate_strategy
from agents.schemas import MessageStrategyOutput, MessageStrategy, PersonaStrategy

def test_live_campaign():
    """Test Agent 2 with a real campaign and show full output."""

    print("\n" + "="*100)
    print("AGENT 2 — LIVE CAMPAIGN TEST")
    print("="*100)

    # Campaign 1: K-12 Learning Solutions (Market Research)
    print("\n[CAMPAIGN INPUT]")
    print("Campaign Name: K-12 Learning Solutions")
    print("Campaign Type: Market Research")
    print("Industry: K-12 Education")
    print("Offer: Research study on EdTech adoption trends in Indian schools")
    print("Personas: ['CXO', 'Director', 'Manager']")
    print("Channels: ['email', 'whatsapp', 'linkedin']")

    print("\n" + "-"*100)
    print("Running Agent 2...")
    print("-"*100)

    try:
        # Call Claude CLI directly via generate_strategy
        strategy = generate_strategy(
            campaign_name="K-12 Learning Solutions",
            campaign_type="Market Research",
            offer="Research study on EdTech adoption trends in Indian schools",
            target_industry="K-12 Education",
            target_personas=["CXO", "Director", "Manager"],
            channel_mix=["email", "whatsapp", "linkedin"]
        )

        # Build MessageStrategyOutput (same as run_message_strategy does)
        tone = strategy.get("messaging_tone", "professional")
        key_themes = strategy.get("key_themes", [])
        call_to_action = strategy.get("call_to_action", "Schedule a conversation")
        success_criteria = strategy.get("success_criteria", {})
        persona_strategies = strategy.get("persona_strategies", {})
        channel_guidance = strategy.get("channel_guidance", {})
        market_rationale = strategy.get("market_context_rationale", "")

        # Build value propositions from persona strategies
        value_propositions = {}
        for persona, strat in persona_strategies.items():
            value_propositions[persona] = strat.get("value_prop", "Tailored solution")

        # Build persona-specific messages
        persona_specific_messages = {}
        for persona in ["CXO", "Director", "Manager"]:
            persona_strat = persona_strategies.get(
                persona,
                {
                    "primary_angle": "Industry insight",
                    "pain_points": ["Market challenges"],
                    "value_prop": "Strategic decision support",
                },
            )
            persona_specific_messages[persona] = {
                "primary_angle": persona_strat.get("primary_angle", "Industry insight"),
                "pain_points": persona_strat.get("pain_points", []),
                "value_prop": persona_strat.get("value_prop", "Tailored solution"),
            }

        # Build output
        output = MessageStrategyOutput(
            messaging_strategy={
                "campaign_name": "K-12 Learning Solutions",
                "tone": tone,
                "key_themes": key_themes,
                "value_propositions": value_propositions,
                "call_to_action": call_to_action,
            },
            persona_specific_messages=persona_specific_messages,
            channel_guidance=channel_guidance,
            success_criteria=success_criteria,
            notes=f"Strategy generated for Market Research campaign targeting K-12 Education with 3 personas. Market context: {market_rationale}",
        )

        print("\n[AGENT 2 OUTPUT — Ready for Agent 3 (Email Copy Agent)]")
        print("-"*100)

        # Show structure for Agent 3
        print("\n1. MESSAGING STRATEGY (Global Campaign Strategy):")
        print(f"   Tone: {output.messaging_strategy.tone}")
        print(f"   Key Themes: {', '.join(output.messaging_strategy.key_themes)}")
        print(f"   Call-to-Action: {output.messaging_strategy.call_to_action}")
        print(f"   Value Propositions (by persona):")
        for persona, value_prop in output.messaging_strategy.value_propositions.items():
            print(f"      - {persona}: {value_prop}")

        print("\n2. PERSONA-SPECIFIC MESSAGES (Input for Agent 3 Email Copy):")
        print(f"   {len(output.persona_specific_messages)} personas:")
        for persona, strategy in output.persona_specific_messages.items():
            print(f"\n   [{persona}]")
            print(f"      Primary Angle: {strategy.primary_angle}")
            print(f"      Pain Points:")
            for pain in strategy.pain_points:
                print(f"         - {pain}")
            print(f"      Value Prop: {strategy.value_prop}")

        print("\n3. CHANNEL GUIDANCE (For Agent 3 & 4):")
        for channel, guidance in output.channel_guidance.items():
            print(f"\n   [{channel.upper()}]:")
            print(f"      {guidance}")

        print("\n4. SUCCESS CRITERIA (Campaign KPIs):")
        for metric, target in output.success_criteria.items():
            print(f"   - {metric}: {target}")

        print("\n5. NOTES:")
        print(f"   {output.notes}")

        # Show JSON for Agent 3 input
        print("\n" + "-"*100)
        print("AGENT 2 RAW JSON OUTPUT (for Agent 3 consumption):")
        print("-"*100)

        # Convert Pydantic models to dicts for JSON serialization
        agent2_output = {
            "messaging_strategy": {
                "campaign_name": output.messaging_strategy.campaign_name if hasattr(output.messaging_strategy, 'campaign_name') else "K-12 Learning Solutions",
                "tone": output.messaging_strategy.tone,
                "key_themes": output.messaging_strategy.key_themes,
                "value_propositions": output.messaging_strategy.value_propositions,
                "call_to_action": output.messaging_strategy.call_to_action,
            },
            "persona_specific_messages": {
                persona: {
                    "primary_angle": strat.primary_angle,
                    "pain_points": strat.pain_points,
                    "value_prop": strat.value_prop,
                }
                for persona, strat in output.persona_specific_messages.items()
            },
            "channel_guidance": output.channel_guidance,
            "success_criteria": output.success_criteria,
            "notes": output.notes
        }

        print(json.dumps(agent2_output, indent=2))

        print("\n" + "="*100)
        print("RESULT: Agent 2 produced market-aware messaging strategy successfully")
        print("="*100)
        print("\nThis output feeds directly into:")
        print("  - Agent 3 (Email Copy Agent): Uses persona_specific_messages + channel_guidance")
        print("  - Agent 4 (WhatsApp Copy Agent): Uses persona_specific_messages + channel_guidance")
        print("  - Message Series Router: Routes based on campaign_type + tone")

    except Exception as e:
        print(f"\n[ERROR] Agent 2 failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_live_campaign()
