"""
Test script for the Orchestrator and Agent Framework.

Run without Anthropic API key — uses logic-based stub implementations.

Usage:
    python agents/test_orchestrator.py
"""

import json
from agents.orchestrator import run_orchestration
from agents.schemas import OrchestrationInput


def test_orchestrator_basic():
    """Test orchestrator with simple input."""
    print("\n" + "=" * 80)
    print("TEST 1: Basic Orchestration with 2 Prospects")
    print("=" * 80)

    input_data = OrchestrationInput(
        campaign_name="Tech Market Research Campaign",
        target_industry="Technology",
        target_region="North America",
        offer="Comprehensive market research report with 50+ industry insights",
        campaign_type="Market Research",
        preferred_channels=["email", "whatsapp", "linkedin"],
        notes="Focus on AI/ML companies with 50-500 employees",
        prospects=[
            {
                "email": "john.smith@techcorp.com",
                "first_name": "John",
                "last_name": "Smith",
                "company_name": "TechCorp Inc",
                "designation": "VP of Engineering",
                "phone": "+1-555-0101",
            },
            {
                "email": "jane.doe@innovatech.io",
                "first_name": "Jane",
                "last_name": "Doe",
                "company_name": "InnovaTech",
                "designation": "Product Manager",
                # No phone — should skip WhatsApp
            },
        ],
    )

    # Run orchestration
    output = run_orchestration(input_data)

    # Print results
    print("\n✅ ORCHESTRATION COMPLETED")
    print(f"\nCampaign: {output.campaign_plan['campaign_draft']['name']}")
    print(f"Message Tone: {output.message_strategy['messaging_strategy']['tone']}")
    print(f"Key Themes: {', '.join(output.message_strategy['messaging_strategy']['key_themes'])}")

    print(f"\nProspects Processed: {output.execution_summary['total_prospects_processed']}")
    print(f"Email Copies Generated: {output.execution_summary['email_copies_generated']}")
    print(f"WhatsApp Messages Generated: {output.execution_summary['whatsapp_copies_generated']}")
    print(f"WhatsApp Skipped: {output.execution_summary['whatsapp_skipped_count']}")

    print("\n" + "-" * 80)
    print("PROSPECT DETAILS")
    print("-" * 80)

    for prospect in output.prospect_messaging:
        print(f"\n📧 {prospect['email']}")
        print(f"   Name: {prospect['first_name']} {prospect['last_name']}")
        print(f"   Company: {prospect['company_name']}")
        print(f"   Persona: {prospect['persona_assignment']['persona']} (confidence: {prospect['persona_assignment']['confidence_score']}%)")

        if prospect["email_copy"]:
            email = prospect["email_copy"]["primary_email"]
            print(f"   Email Subject: {email['subject']}")
            print(f"   Email CTA: {email['cta_text']}")

        if prospect["whatsapp_copy"]:
            msg = prospect["whatsapp_copy"]["primary_message"]["message"]
            print(f"   WhatsApp: {msg}")
        else:
            print(f"   WhatsApp: SKIPPED (no phone number)")

    print("\n" + "-" * 80)
    print("EXECUTION LOG")
    print("-" * 80)

    for log in output.execution_summary["execution_log"][-5:]:  # Last 5 logs
        print(f"[{log['level'].upper()}] {log['message']}")

    return True


def test_orchestrator_large_batch():
    """Test orchestrator with larger prospect list."""
    print("\n" + "=" * 80)
    print("TEST 2: Large Batch Processing (5 Prospects)")
    print("=" * 80)

    prospects = [
        {
            "email": f"prospect{i}@company{i}.com",
            "first_name": f"Prospect_{i}",
            "last_name": f"User_{i}",
            "company_name": f"Company {i}",
            "designation": ["CEO", "VP Engineering", "Director", "Manager", "Specialist"][i % 5],
            "phone": f"+1-555-010{i}" if i % 2 == 0 else None,  # Half have phone
        }
        for i in range(1, 6)
    ]

    input_data = OrchestrationInput(
        campaign_name="Enterprise Solutions Campaign",
        target_industry="Finance",
        target_region="EMEA",
        offer="Enterprise compliance and security solutions",
        campaign_type="Consulting",
        prospects=prospects,
    )

    output = run_orchestration(input_data)

    print(f"\n✅ Processed {output.execution_summary['total_prospects_processed']} prospects")
    print(f"   Email: {output.execution_summary['email_copies_generated']}")
    print(f"   WhatsApp: {output.execution_summary['whatsapp_copies_generated']}")
    print(f"   Skipped: {output.execution_summary['whatsapp_skipped_count']}")
    print(f"   Personas: {', '.join(output.execution_summary['personas_assigned'])}")

    return True


def test_orchestrator_no_prospects():
    """Test orchestrator with no prospects (campaign plan only)."""
    print("\n" + "=" * 80)
    print("TEST 3: Campaign Planning Only (No Prospects)")
    print("=" * 80)

    input_data = OrchestrationInput(
        campaign_name="Awareness Campaign",
        target_industry="Healthcare",
        target_region="US",
        offer="Medical device education and training",
        campaign_type="Webinar",
        prospects=[],  # Empty
    )

    output = run_orchestration(input_data)

    print(f"\n✅ Campaign plan generated")
    print(f"   Name: {output.campaign_plan['campaign_draft']['name']}")
    print(f"   Type: {output.campaign_plan['campaign_draft']['campaign_type']}")
    print(f"   Personas: {', '.join([p['persona'] for p in output.campaign_plan['persona_map']])}")
    print(f"   Channels: {', '.join(output.campaign_plan['channel_plan']['channels'])}")

    print(f"\nProspects to process: {output.execution_summary['total_prospects_processed']}")

    return True


def print_json_sample():
    """Print sample output structure."""
    print("\n" + "=" * 80)
    print("SAMPLE OUTPUT STRUCTURE")
    print("=" * 80)

    sample = {
        "campaign_plan": {
            "campaign_draft": {
                "name": "Sample Campaign",
                "campaign_type": "Market Research",
            },
            "persona_map": [
                {"persona": "CXO", "persona_type": "primary", "rationale": "Strategic decision maker"}
            ],
        },
        "message_strategy": {
            "messaging_strategy": {
                "tone": "professional",
                "key_themes": ["innovation", "growth"],
                "value_propositions": {"CXO": "Strategic ROI"},
            }
        },
        "prospect_messaging": [
            {
                "email": "john@company.com",
                "persona_assignment": {
                    "persona": "Director",
                    "confidence_score": 88,
                    "rationale": "VP maps to Director level",
                },
                "email_copy": {
                    "primary_email": {
                        "subject": "Opportunity for Company",
                        "body": "Hi John, ...",
                    }
                },
                "whatsapp_copy": {
                    "primary_message": {
                        "message": "Hi John, quick opportunity...",
                    }
                } if True else None,  # Depends on phone
                "channels_used": ["email", "whatsapp", "linkedin"],
            }
        ],
        "execution_summary": {
            "total_prospects_processed": 1,
            "email_copies_generated": 1,
            "whatsapp_copies_generated": 1,
        },
    }

    print(json.dumps(sample, indent=2))


if __name__ == "__main__":
    print("\n" + "🚀 " * 20)
    print("ORCHESTRATOR TEST SUITE")
    print("🚀 " * 20)

    try:
        # Run tests
        test_orchestrator_basic()
        test_orchestrator_large_batch()
        test_orchestrator_no_prospects()
        print_json_sample()

        print("\n" + "=" * 80)
        print("✅ ALL TESTS PASSED")
        print("=" * 80)
        print("\nNext steps:")
        print("1. Integrate Campaign Planner Agent (external)")
        print("2. Add Anthropic API calls to agents")
        print("3. Integrate with Django backend")
        print("4. Deploy to production")

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
