# Workflow: Email Sequence

**Workflow ID:** WF-004  
**Agents involved:** None (execution workflow — no agent reasoning at send time)  
**Skills involved:** None  
**Phase:** Phase 9 (Email Outreach via Microsoft Graph)

---

## Purpose
Executes Email M1–M4 sequence for a prospect via Microsoft Graph, tracking sends, managing conversation threads, detecting replies, and enforcing all governance checks before each send.

---

## Trigger
Celery Beat scans for prospects with SequenceState where:
- channel = email
- status = sequence_active
- next_action_at <= now()
- current_stage in (M1, M2, M3, M4)

---

## Pre-conditions
- Prospect has approved M-stage email message
- Microsoft Graph sender account configured
- Governance checks not blocking

---

## Workflow steps

```
Step 1: Celery task fires for prospect + campaign + stage
  → Task ID = {prospect_id}_{campaign_id}_email_{stage} (idempotency key)
  → If task ID already executed → skip (idempotent)

Step 2: Run governance check stack (in order)
  1. DNC check
  2. Reply status check
  3. Manual intervention check
  4. Duplicate send check
  5. Sender limit check
  6. Approval check
  7. Sequence state check
  → Any check fails → halt task, log reason, do not send

Step 3: Fetch approved message
  → Pull message where prospect + campaign + channel=email + stage + approval_status=approved
  → If not found → halt, log missing_message error, alert

Step 4: Send via Microsoft Graph
  → M1: send as new email thread
  → M2–M4: send as reply to M1 conversationId (same thread)
  → Store returned message_id and conversationId on Touchpoint record

Step 5: Create Touchpoint record
  → stage, channel, sent_at, delivery_status = sent, message_id

Step 6: Log Pipedrive activity
  → POST activity to Pipedrive: email sent, stage, date, campaign

Step 7: Calculate next stage
  → If M1: schedule M2 task for day+3
  → If M2: schedule M3 task for day+4
  → If M3: schedule M4 task for day+5
  → If M4: set SequenceState.status = dormant after 30 days if no reply

Step 8: Write AuditLog
  → actor_system = celery_email_worker
  → action = email_sent, stage, prospect, campaign, message_id
```

---

## Reply detection (separate Celery Beat job)
- Every 10 minutes: poll Microsoft Graph conversation threads for active email prospects
- New message from prospect detected → dispatch to Reply Classifier Agent → stop automation

---

## Governance gates
- ALL 7 governance checks must pass before send
- Governance is checked at task execution time, not at scheduling time
- Stop automation is checked fresh at every M-stage send

---

## Failure path
- MS Graph API error → retry 3x with exponential backoff
- After 3 failures → mark Touchpoint delivery_status = failed, alert admin

---

## Audit log events
| Event | Trigger |
|-------|---------|
| `email_send_attempted` | Task fires |
| `email_send_blocked_governance` | Any governance check fails |
| `email_sent` | MS Graph confirms send |
| `email_reply_detected` | Reply found in thread |
| `email_bounce_detected` | NDR received |

---

## Acceptance criteria
- [ ] Idempotency prevents duplicate sends
- [ ] All 7 governance checks run at task execution time
- [ ] M2–M4 appear in same thread as M1
- [ ] Reply detection fires within 10 min
- [ ] Failed sends retry and alert on third failure
