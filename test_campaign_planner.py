#!/usr/bin/env python3
"""Test script for Campaign Planner Agent.

To run this test:
1. Set ANTHROPIC_API_KEY environment variable
2. Or create .env file with: ANTHROPIC_API_KEY=your-key
3. Run: python test_campaign_planner.py
"""

import json
import sys
from pathlib import Path

# Load .env if present
if Path(".env").exists():
    from dotenv import load_dotenv
    load_dotenv()

from agents.campaign_planner_agent import run_campaign_planner


def test_india_ev_survey():
    """Test with India EV Ecosystem Survey example from spec."""

    print("Testing Campaign Planner Agent with India EV Survey example...")
    print()

    try:
        output = run_campaign_planner(
            campaign_name="India EV Ecosystem Survey",
            target_industry="Automotive",
            target_region="India",
            offer="Survey participation + sector report",
            campaign_type="Survey",
            preferred_channels=None,  # Use defaults
            notes="Focus on EV component suppliers and OEMs",
        )

        print("✓ Agent completed successfully!")
        print()
        print("=" * 80)
        print("CAMPAIGN DRAFT")
        print("=" * 80)
        print(json.dumps(output.campaign_draft.model_dump(), indent=2))
        print()

        print("=" * 80)
        print("ICP DEFINITION")
        print("=" * 80)
        print(json.dumps(output.icp_definition.model_dump(), indent=2))
        print()

        print("=" * 80)
        print("PERSONA MAP")
        print("=" * 80)
        for persona in output.persona_map:
            print(f"  - {persona.persona} ({persona.persona_type}): {persona.rationale}")
        print()

        print("=" * 80)
        print("CHANNEL PLAN")
        print("=" * 80)
        print(f"  Channels: {', '.join(output.channel_plan.channels)}")
        print(f"  Sequence timing: {output.channel_plan.sequence_timing}")
        print()

        print("=" * 80)
        print("APPROVAL & CONFIDENCE")
        print("=" * 80)
        print(f"  Requires approval: {output.approval_flag}")
        print(f"  Confidence notes: {output.confidence_notes}")
        print()

        # Verify against expected output
        print("=" * 80)
        print("VERIFICATION")
        print("=" * 80)

        expected_channels = {"whatsapp", "email"}
        actual_channels = set(output.channel_plan.channels)
        channels_match = expected_channels == actual_channels
        print(f"  ✓ Channels match (WhatsApp + Email): {channels_match}")

        personas = [p.persona for p in output.persona_map]
        has_cxo = "CXO" in personas
        has_ops = "Operations" in personas
        personas_match = has_cxo and has_ops
        print(f"  ✓ Personas include CXO & Operations: {personas_match}")

        timing_correct = (
            output.channel_plan.sequence_timing.get("M1") == 0
            and output.channel_plan.sequence_timing.get("M2") == 3
            and output.channel_plan.sequence_timing.get("M3") == 7
            and output.channel_plan.sequence_timing.get("M4") == 12
        )
        print(f"  ✓ Sequence timing correct (0, 3, 7, 12): {timing_correct}")

        approval_correct = output.approval_flag == True
        print(f"  ✓ Approval flag set (always true): {approval_correct}")

        if channels_match and personas_match and timing_correct and approval_correct:
            print()
            print("🎉 All verifications passed!")
            return True
        else:
            print()
            print("❌ Some verifications failed")
            return False

    except Exception as e:
        print(f"❌ Agent failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_india_ev_survey()
    sys.exit(0 if success else 1)
