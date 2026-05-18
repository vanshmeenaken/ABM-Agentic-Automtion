#!/usr/bin/env python3
"""End-to-end test for Campaign Planner, Prospect Research, Data Quality, and Persona Classifier agents.

To run:
1. Set ANTHROPIC_API_KEY environment variable
2. python test_all_agents.py
"""

import json
import sys
from pathlib import Path

# Load .env if present
if Path(".env").exists():
    from dotenv import load_dotenv
    load_dotenv()

from agents.campaign_planner_agent import run_campaign_planner
from agents.prospect_research_agent import run_prospect_research
from agents.data_quality_agent import run_data_quality
from agents.persona_classifier_agent import run_persona_classifier


def test_campaign_planner():
    """Test Campaign Planner Agent with India EV Survey example."""
    print("\n" + "=" * 80)
    print("STEP 1: CAMPAIGN PLANNER AGENT")
    print("=" * 80)

    try:
        output = run_campaign_planner(
            campaign_name="India EV Ecosystem Survey",
            target_industry="Automotive",
            target_region="India",
            offer="Survey participation + sector report",
            campaign_type="Survey",
            preferred_channels=None,
            notes="Focus on EV component suppliers and OEMs",
        )

        print("✓ Campaign Planner completed!")
        print(f"  Campaign: {output.campaign_draft.name}")
        print(f"  ICP: {output.icp_definition.positive.industries}")
        print(f"  Personas: {[p.persona for p in output.persona_map]}")
        print(f"  Channels: {output.channel_plan.channels}")
        print()

        return output

    except Exception as e:
        print(f"❌ Campaign Planner failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_prospect_research(campaign_output):
    """Test Prospect Research Agent with Campaign Planner output."""
    print("=" * 80)
    print("STEP 2: PROSPECT RESEARCH AGENT")
    print("=" * 80)

    if not campaign_output:
        print("⚠ Skipping Prospect Research (Campaign Planner failed)")
        return None

    try:
        output = run_prospect_research(
            campaign_id="camp-ev-survey-001",
            icp_definition=campaign_output.icp_definition.model_dump(),
            persona_map=[p.model_dump() for p in campaign_output.persona_map],
            approved_sources=["Apollo", "Clay"],
            max_prospects=500,
            notes="Focus on India automotive sector",
        )

        print("✓ Prospect Research completed!")
        print(f"  Accounts found: {output.accounts_found}")
        print(f"  Total contacts: {output.contacts_found}")
        print(f"  Sources: {list(output.source_breakdown.keys())}")
        print(f"  Raw prospects count: {len(output.raw_prospects)}")
        print()

        return output

    except Exception as e:
        print(f"❌ Prospect Research failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_data_quality(prospect_output):
    """Test Data Quality Agent with Prospect Research output."""
    print("=" * 80)
    print("STEP 3: DATA QUALITY AGENT")
    print("=" * 80)

    if not prospect_output:
        print("⚠ Skipping Data Quality (Prospect Research failed)")
        return None

    try:
        output = run_data_quality(
            raw_prospects=[p.model_dump() for p in prospect_output.raw_prospects],
            campaign_id="camp-ev-survey-001",
            dedup_scope="platform",
        )

        print("✓ Data Quality completed!")
        print(f"  Cleaned records: {len(output.cleaned_prospects)}")
        print(f"  Duplicate flags: {len(output.duplicate_flags)}")
        print(f"  Low confidence: {len(output.low_confidence_flags)}")
        print(f"  Duplicate rate: {output.duplicate_rate * 100:.1f}%")
        print(f"  Corrections made: {output.field_corrections}")
        print()

        return output

    except Exception as e:
        print(f"❌ Data Quality failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_persona_classifier(quality_output, campaign_output):
    """Test Persona Classifier Agent with Data Quality output."""
    print("=" * 80)
    print("STEP 4: PERSONA CLASSIFIER AGENT")
    print("=" * 80)

    if not quality_output or not campaign_output:
        print("⚠ Skipping Persona Classifier (Data Quality or Campaign Planner failed)")
        return None

    try:
        output = run_persona_classifier(
            cleaned_prospects=[p.model_dump() for p in quality_output.cleaned_prospects],
            campaign_type="Survey",
            target_personas=[p.persona for p in campaign_output.persona_map],
        )

        print("✓ Persona Classifier completed!")
        print(f"  Classified prospects: {len(output.classified_prospects)}")
        print(f"  Persona distribution: {output.persona_distribution}")
        print(f"  Average confidence: {output.average_confidence:.1f}%")
        print(f"  Low confidence count: {output.low_confidence_count}")
        print(f"  Unclassifiable: {output.unclassifiable_count}")
        print()

        return output

    except Exception as e:
        print(f"❌ Persona Classifier failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Run full end-to-end agent test."""
    print("\n" + "🚀 " * 20)
    print("CAMPAIGN PLANNER → PROSPECT RESEARCH → DATA QUALITY → PERSONA CLASSIFIER")
    print("🚀 " * 20)

    # Step 1: Campaign Planner
    campaign_output = test_campaign_planner()

    # Step 2: Prospect Research
    prospect_output = test_prospect_research(campaign_output)

    # Step 3: Data Quality
    quality_output = test_data_quality(prospect_output)

    # Step 4: Persona Classifier
    classifier_output = test_persona_classifier(quality_output, campaign_output)

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)

    if campaign_output and prospect_output and quality_output and classifier_output:
        print("✅ ALL AGENTS COMPLETED SUCCESSFULLY!")
        print()
        print("Flow:")
        print(f"  1. Campaign Created: {campaign_output.campaign_draft.name}")
        print(f"  2. Prospects Researched: {prospect_output.contacts_found} contacts")
        print(f"  3. Data Cleaned: {len(quality_output.cleaned_prospects)} records")
        print(f"  4. Personas Classified: {len(classifier_output.classified_prospects)} classified")
        print()
        return True
    else:
        print("❌ SOME AGENTS FAILED")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
