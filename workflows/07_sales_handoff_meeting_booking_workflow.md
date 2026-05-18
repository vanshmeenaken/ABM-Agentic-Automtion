# Workflow: Sales Handoff + Meeting Booking

**Workflow ID:** WF-007  
**Agents involved:** Sales Handoff Agent  
**Skills involved:** Manual Handoff Skill, Meeting Booking Skill  
**Phase:** Phase 13 + Phase 14

---

## Purpose
Creates a complete sales handoff brief, notifies the campaign owner, routes to the meeting booking flow if the prospect is meeting-ready, and creates the Pipedrive activity record.

---

## Trigger
Reply Classifier routes to WF-007 with intent_category in: `positive_interest`, `meeting_request`, `question`.

---

## Pre-conditions
- Reply classified with sufficient confidence (>= 60) OR human has reviewed and confirmed intent
- Campaign owner assigned to campaign
- Prospect has complete record (name, title, company, touchpoint history)

---

## Workflow steps

```
Step 1: Run Sales Handoff Agent
  → Input: prospect, campaign, reply_text, intent_category, all_touchpoints, owner
  → Output: handoff_brief, suggested_response, meeting_ready flag, talking_points
  → Log Agent Run

Step 2: Create ManualHandoff record in DB
  → prospect, campaign, owner, brief, suggested_response, meeting_ready, status = pending

Step 3: Notify campaign owner
  → Push notification in control tower: "New handoff — [Prospect name]"
  → Email notification to owner (if configured)

Step 4: Create Pipedrive activity
  → Activity type: Handoff
  → Subject: "Handoff: [Prospect name] — [Campaign name]"
  → Note: Full handoff brief
  → Assigned to: campaign owner
  → Associated lead: prospect's Pipedrive lead ID

Step 5: If meeting_ready = True
  → Generate Meeting Brief via Meeting Booking Skill
  → Display meeting brief + slot selection in control tower handoff view
  → Owner selects slot → create calendar event (owner's calendar)
  → Create Pipedrive meeting activity
  → Set SequenceState.status = completed
  → AuditLog: meeting_booked

Step 6: If meeting_ready = False (question intent)
  → Display handoff with suggested response
  → Owner sends response to prospect (manual, via email/WA/LinkedIn)
  → Owner marks handoff as in_progress
  → Monitor for prospect's follow-up reply

Step 7: Write AuditLog
  → handoff_created, owner_notified, meeting_booked (if applicable)
```

---

## Governance gates
- Handoff cannot be created without a classified reply — no manual handoff creation without source reply
- Meeting booking can only happen after handoff is created and owner has reviewed
- Pipedrive activity must be created before handoff is marked complete

---

## Failure path
- Sales Handoff Agent failure → save partial brief, flag for human completion, notify admin
- Pipedrive activity creation failure → retry 3x, then alert for manual Pipedrive update

---

## Audit log events
| Event | Trigger |
|-------|---------|
| `handoff_created` | ManualHandoff record saved |
| `owner_notified` | Notification sent |
| `pipedrive_activity_created` | Pipedrive write confirmed |
| `meeting_brief_generated` | Meeting Booking Skill run |
| `meeting_booked` | Calendar event + Pipedrive meeting activity created |
| `handoff_completed` | Owner marks complete |

---

## Acceptance criteria
- [ ] Handoff brief contains complete prospect history (not placeholders)
- [ ] Suggested response addresses the actual prospect reply
- [ ] Owner notified within 5 min of handoff creation
- [ ] Pipedrive activity created for every handoff
- [ ] Meeting brief generated with persona-specific talking points
- [ ] Meeting booking creates both calendar event and Pipedrive meeting activity
