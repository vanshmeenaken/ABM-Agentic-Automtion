# Workflow: Message Generation + Approval

**Workflow ID:** WF-003  
**Agents involved:** Message Strategy Agent, Email Copy Agent, WhatsApp Copy Agent, Compliance Review Agent  
**Skills involved:** Email Outreach Copy, WhatsApp Outreach Copy, Message Compliance  
**Phase:** Phase 8 (Message Intelligence Layer)

---

## Purpose
Generates persona-specific M1–M4 messages for each channel, runs compliance review, and routes approved messages through human approval before any send is permitted.

---

## Trigger
Prospect assigned to campaign with outreach_eligible = True, and campaign has active channel configuration.

---

## Pre-conditions
- Prospect has confirmed persona_tag (not unknown)
- Campaign has approved message templates OR message generation is enabled
- Compliance Review Agent is active

---

## Workflow steps

```
Step 1: Dispatch Message Strategy Agent
  → Input: prospect + campaign + persona + offer + prior touchpoints
  → Output: strategy brief (angle, proof points, tone, CTA)
  → Log Agent Run

Step 2: Dispatch Email Copy Agent (if email in channel mix)
  → Input: strategy brief + M-stage (M1 first, others queued)
  → Output: subject + body for each stage
  → Log Agent Run

Step 3: Dispatch WhatsApp Copy Agent (if WA in channel mix)
  → Input: strategy brief + M-stage
  → Output: body + opt-out line for each stage
  → Log Agent Run
  → Steps 2 and 3 run in parallel

Step 4: Run Compliance Review Agent on every draft
  → Input: message draft + channel + persona
  → PASS → proceed to approval queue
  → BLOCK → mark message compliance_status = block
           → log violation + reason
           → notify campaign owner
           → do not proceed to approval queue

Step 5: Human approval queue
  → Compliance-passed messages appear in control tower approval queue
  → Reviewer reads draft, can: approve / reject / edit
  → Approved → approval_status = approved, approved_by, approved_at logged
  → Rejected → approval_status = rejected, rejection_reason logged
  → Edited → save edited version, rerun Compliance Review Agent, then re-queue

Step 6: Message ready for send
  → Message with approval_status = approved enters sequence execution pool
  → Celery Sequence Orchestrator picks up and schedules send
```

---

## Governance gates
- No message enters approval queue without PASS from Compliance Review Agent
- BLOCK status cannot be manually overridden — message must be regenerated
- No message is sent without approval_status = approved
- Edited messages must repass compliance review before approval

---

## Stop path
- If all M1–M4 messages for a prospect are blocked → pause prospect sequence, notify campaign owner

---

## Audit log events
| Event | Trigger |
|-------|---------|
| `message_generated` | Agent output saved |
| `message_compliance_passed` | Compliance PASS |
| `message_compliance_blocked` | Compliance BLOCK |
| `message_approved` | Human approves |
| `message_rejected` | Human rejects |

---

## Acceptance criteria
- [ ] Strategy brief generated before any copy agent runs
- [ ] Compliance runs on every message draft without exception
- [ ] BLOCKed messages cannot reach approval queue
- [ ] Edited messages rerun compliance before approval
- [ ] Every approval action logged with user ID and timestamp
