# 05 — Governance and Stop Automation

**Phase:** 5  
**Inputs from:** Phase 2 (data models), Phase 4 (Pipedrive state)  
**Outputs to:** Phase 9+ (all channel phases must pass governance before sending)

---

## 1. Phase purpose
Build all governance checks and the cross-channel stop automation system. Every send — Email, WhatsApp, or LinkedIn — must pass all applicable governance checks before execution.

---

## 2. Governance check stack (runs in order before every send)

| Order | Check | Block condition | Stop type |
|-------|-------|-----------------|-----------|
| 1 | DNC check | Prospect in SuppressionRecord | Permanent block |
| 2 | Reply status check | Reply detected on any channel | Stop automation |
| 3 | Manual intervention check | Manual Pipedrive activity detected | Stop automation |
| 4 | Duplicate send check | Touchpoint already exists for this stage + channel | Skip |
| 5 | Sender limit check | Sender account at daily send limit | Defer to next window |
| 6 | Approval check | Message approval_status != approved | Hold |
| 7 | Sequence state check | SequenceState is stopped/paused/dormant | Block |
| 8 | Outreach eligibility check | Prospect outreach_eligible == False | Block |

---

## 3. Stop automation triggers
Any of the following triggers a full stop across all channels for the prospect:
- Reply received (any channel)
- Manual sales activity in Pipedrive
- DNC marked
- Meeting booked
- Owner override via control tower

---

## 4. Stop automation propagation
When a stop is triggered:
1. Set SequenceState.status = `stopped` for all active sequences (all channels)
2. Write stop_reason to SequenceState
3. Cancel all pending Celery tasks for this prospect
4. Update Pipedrive label
5. Write AuditLog entry with trigger source, timestamp, and actor

---

## 5. Governance requirements
- Governance checks run inside a Django service class, not inside the agent
- No agent can bypass governance
- All governance decisions are audit logged
- Permanent DNC can only be removed by an admin-level user

---

## 6. Acceptance criteria
- [ ] DNC prospect receives no outreach under any condition
- [ ] Reply on Email stops WhatsApp and LinkedIn sequences for same prospect
- [ ] Manual Pipedrive activity detected within 15 min → automation stops
- [ ] Duplicate send check prevents same message being sent twice
- [ ] All governance decisions written to AuditLog
- [ ] Stop propagation completes across all channels within 5 min of trigger
