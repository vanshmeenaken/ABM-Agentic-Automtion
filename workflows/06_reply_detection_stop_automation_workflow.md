# Workflow: Reply Detection + Stop Automation

**Workflow ID:** WF-006  
**Agents involved:** Reply Classifier Agent  
**Skills involved:** Reply Classification Skill  
**Phase:** Phase 13 (Reply Intelligence + Manual Handoff)

---

## Purpose
Detects inbound replies on any channel, issues immediate stop automation, classifies reply intent, and routes to the appropriate next action (handoff, suppression, or human review).

---

## Trigger
- Microsoft Graph reply detected in email conversation thread (polled every 10 min)
- Periskope reply webhook received
- LinkedHelper reply event webhook received
- Manual stop triggered by user in control tower

---

## Pre-conditions
- Prospect has an active SequenceState on any channel
- Reply event is from the prospect (not a bounce or OOO from a system)

---

## Workflow steps

```
Step 1: Receive reply event
  → Source: MS Graph / Periskope webhook / LinkedHelper webhook / manual override
  → Extract: reply_text, channel, prospect_id, campaign_id
  → Log raw reply to Reply model

Step 2: STOP ALL AUTOMATION IMMEDIATELY
  → Set SequenceState.status = stopped for ALL channels for this prospect
  → Set stop_reason = reply_received_{channel}
  → Cancel all pending Celery tasks for this prospect
  → Update Pipedrive label to "replied"
  → Write AuditLog: automation_stopped
  (This step completes before classification begins)

Step 3: Run Reply Classifier Agent
  → Input: reply_text, channel, prospect, campaign, touchpoints
  → Output: intent_category, confidence_score, recommended_action

Step 4: Route by intent category
  → positive_interest → WF-007 (Sales Handoff + Meeting Booking)
  → meeting_request   → WF-007 with meeting_ready = True
  → question          → WF-007 with meeting_ready = False
  → negative          → Create SuppressionRecord, close sequence
  → out_of_office     → Log OOO, set tentative resume date, notify owner
  → bounce            → Update prospect email validity, flag for review
  → ambiguous         → Flag for human review in control tower

Step 5: Notify campaign owner
  → Push notification in control tower
  → Log reply event in Pipedrive as activity

Step 6: Write AuditLog
  → reply_classified, intent_category, confidence_score, action_taken
```

---

## Governance gates
- Stop automation fires BEFORE classification — it cannot be deferred
- OOO replies do not create SuppressionRecord — only `negative` and opt-out keywords do
- Ambiguous replies always go to human review — never auto-resolved

---

## Stop propagation — cross-channel
When stop fires:
- Email SequenceState → stopped
- WhatsApp SequenceState → stopped
- LinkedIn SequenceState → stopped
- All pending Celery tasks cancelled
- Pipedrive label updated
- AuditLog written

All of the above must complete within 5 minutes of the stop trigger.

---

## Audit log events
| Event | Trigger |
|-------|---------|
| `reply_received` | Reply ingested from any channel |
| `automation_stopped` | Stop flag issued |
| `reply_classified` | Classifier output |
| `handoff_routed` | Positive/question intent routed to WF-007 |
| `suppression_created` | Negative intent creates SuppressionRecord |

---

## Acceptance criteria
- [ ] Stop fires within 5 min of any reply on any channel
- [ ] Stop propagates across all channels, not just reply channel
- [ ] Classification routes correctly to handoff, suppression, or review
- [ ] Pipedrive label updated within same stop cycle
- [ ] AuditLog written at every step
