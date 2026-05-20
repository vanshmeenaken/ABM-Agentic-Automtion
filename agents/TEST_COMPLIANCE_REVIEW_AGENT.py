"""Test Compliance Review Agent with 3 scenarios."""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from compliance_review_agent import run_compliance_review_agent


def test_scenario_1_clean_whatsapp_all_pass():
    """
    Scenario 1: Clean WhatsApp messages (all pass, Telegram approval should be sent).
    """
    print("\n" + "=" * 80)
    print("SCENARIO 1: Clean WhatsApp Messages (All Pass)")
    print("=" * 80)

    output = run_compliance_review_agent(
        campaign_name="Survey: K-12 EdTech",
        campaign_type="Survey",
        channel="whatsapp",
        messages={
            "cxo_strategy": {
                "M1": {
                    "message": "Hi Rajesh! We recently finished research on K-12 EdTech adoption. Would you have 15 mins this week to discuss? Reply STOP to opt-out.",
                    "word_count": 26
                },
                "M2": {
                    "message": "Our research found that many schools are exploring new solutions. Thought you'd find it valuable. Reply STOP to opt-out.",
                    "word_count": 24
                },
                "M3": {
                    "message": "Either way, I'll send you the findings. If interested, let's connect. Reply STOP to opt-out.",
                    "word_count": 18
                }
            }
        },
        prospect_name="Rajesh Kumar",
        company_name="K-12 EdTech Inc",
        trigger_telegram_approval=False,  # Set to False to avoid actual Telegram call in tests
        telegram_user_id=0
    )

    print(f"\nCampaign: {output.campaign_name}")
    print(f"Channel: {output.channel}")
    print(f"Overall Status: {output.overall_status}")
    print(f"Telegram Approval Sent: {output.telegram_approval_sent}")
    print(f"Notes: {output.notes}\n")

    # Verify each stage
    for persona, results in output.compliance_results.items():
        print(f"\nPersona: {persona}")
        for result in results:
            print(f"  Stage {result.stage}: {result.status.upper()}")
            print(f"    Word Count: {result.word_count}")
            print(f"    Can Be Approved: {result.can_be_approved}")
            if result.violations:
                for v in result.violations:
                    print(f"      VIOLATION: {v.rule}: {v.detail}")
            else:
                print(f"      [PASS] No violations")

    # Assertions
    assert output.overall_status == "all_pass", f"Expected all_pass, got {output.overall_status}"
    assert all(
        result.status == "pass"
        for results in output.compliance_results.values()
        for result in results
    ), "Expected all results to be 'pass'"
    print("\n[PASS] SCENARIO 1 PASSED: All messages passed compliance checks")


def test_scenario_2_email_with_spam_words_blocked():
    """
    Scenario 2: Email with spam trigger words (should be blocked, Telegram NOT sent).
    """
    print("\n" + "=" * 80)
    print("SCENARIO 2: Email with Spam Trigger Words (Blocked)")
    print("=" * 80)

    output = run_compliance_review_agent(
        campaign_name="Survey: Logistics Optimization",
        campaign_type="Survey",
        channel="email",
        messages={
            "operations": {
                "M1": {
                    "message": "Subject: Act now for a free logistics assessment!\n\nHi, we recently completed research on cold chain optimization. Limited time offer - this analysis is worth thousands. Don't miss out!",
                    "word_count": 35
                },
                "M2": {
                    "message": "Here are the guaranteed results our clients see in the first 90 days. Risk-free evaluation included.",
                    "word_count": 18
                },
                "M3": {
                    "message": "Either way, you'll get our findings. Click here now to schedule.",
                    "word_count": 12
                }
            }
        },
        prospect_name="Operations Manager",
        company_name="Cold Chain Logistics",
        trigger_telegram_approval=False,
        telegram_user_id=0
    )

    print(f"\nCampaign: {output.campaign_name}")
    print(f"Channel: {output.channel}")
    print(f"Overall Status: {output.overall_status}")
    print(f"Telegram Approval Sent: {output.telegram_approval_sent}")
    print(f"Notes: {output.notes}\n")

    # Verify each stage
    for persona, results in output.compliance_results.items():
        print(f"\nPersona: {persona}")
        for result in results:
            print(f"  Stage {result.stage}: {result.status.upper()}")
            print(f"    Word Count: {result.word_count}")
            print(f"    Can Be Approved: {result.can_be_approved}")
            if result.violations:
                for v in result.violations:
                    print(f"      VIOLATION: {v.rule}: {v.detail}")
                    print(f"         Recommendation: {v.recommendation}")

    # Assertions
    assert output.overall_status == "all_blocked", f"Expected all_blocked, got {output.overall_status}"
    assert output.telegram_approval_sent == False, "Expected Telegram NOT sent for blocked messages"
    assert any(
        result.status == "blocked"
        for results in output.compliance_results.values()
        for result in results
    ), "Expected at least one blocked result"
    print("\n[PASS] SCENARIO 2 PASSED: Spam words blocked correctly, Telegram NOT sent")


def test_scenario_3_whatsapp_missing_optout_and_length():
    """
    Scenario 3: WhatsApp missing opt-out + excessive length (multiple violations).
    """
    print("\n" + "=" * 80)
    print("SCENARIO 3: WhatsApp Missing Opt-Out & Excessive Length (Blocked)")
    print("=" * 80)

    # Create a message that's too long and has no opt-out
    long_message = " ".join(["This is a word"] * 50)  # 100 words, acceptable
    excessive_message = " ".join(["This is a word"] * 320)  # 320 words, exceeds 300 limit

    output = run_compliance_review_agent(
        campaign_name="Market Research: Tech Talent",
        campaign_type="Market Research",
        channel="whatsapp",
        messages={
            "cxo_strategy": {
                "M1": {
                    "message": "Hi! We've completed research on tech talent market trends. Interested?",
                    "word_count": 12
                },
                "M2": {
                    "message": excessive_message,  # Too long, no opt-out
                    "word_count": 320
                },
                "M3": {
                    "message": "Let's discuss. Reply STOP to unsubscribe.",
                    "word_count": 7
                }
            }
        },
        prospect_name="CTO",
        company_name="Tech Company",
        trigger_telegram_approval=False,
        telegram_user_id=0
    )

    print(f"\nCampaign: {output.campaign_name}")
    print(f"Channel: {output.channel}")
    print(f"Overall Status: {output.overall_status}")
    print(f"Telegram Approval Sent: {output.telegram_approval_sent}")
    print(f"Notes: {output.notes}\n")

    # Verify results
    for persona, results in output.compliance_results.items():
        print(f"\nPersona: {persona}")
        for result in results:
            print(f"  Stage {result.stage}: {result.status.upper()}")
            print(f"    Word Count: {result.word_count}")
            print(f"    Can Be Approved: {result.can_be_approved}")
            if result.violations:
                for v in result.violations:
                    print(f"      VIOLATION: {v.rule}: {v.detail}")

    # Assertions
    assert output.overall_status in ["some_blocked", "all_blocked"], f"Expected some/all_blocked, got {output.overall_status}"

    # Check M2 has violation
    m2_result = output.compliance_results["cxo_strategy"][1]
    assert m2_result.status == "blocked", f"Expected M2 to be blocked, got {m2_result.status}"
    assert any(v.rule == "excessive_length" for v in m2_result.violations), "Expected excessive_length violation"

    print("\n[PASS] SCENARIO 3 PASSED: WhatsApp violations detected correctly")


def run_all_tests():
    """Run all 3 test scenarios."""
    try:
        test_scenario_1_clean_whatsapp_all_pass()
        test_scenario_2_email_with_spam_words_blocked()
        test_scenario_3_whatsapp_missing_optout_and_length()

        print("\n" + "=" * 80)
        print("[PASS] ALL TESTS PASSED")
        print("=" * 80)
        print("\nSummary:")
        print("  [OK] Scenario 1: Clean WhatsApp messages pass compliance")
        print("  [OK] Scenario 2: Spam words trigger block, Telegram not sent")
        print("  [OK] Scenario 3: Multiple violations detected correctly")
        print("\nCompliance Review Agent is working correctly!")

    except AssertionError as e:
        print(f"\n[FAIL] TEST FAILED: {str(e)}")
        raise
    except Exception as e:
        print(f"\n[FAIL] UNEXPECTED ERROR: {str(e)}")
        raise


if __name__ == "__main__":
    run_all_tests()
