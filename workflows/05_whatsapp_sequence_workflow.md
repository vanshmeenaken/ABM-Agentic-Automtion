# Workflow: WhatsApp Sequence

**Workflow ID:** WF-005  
**Agents involved:** None (execution workflow)  
**Skills involved:** None  
**Phase:** Phase 10 (WhatsApp Outreach via Periskope)

---

## Purpose
Executes WhatsApp M1–M4 sequence for a prospect via Periskope API, tracking delivery status, detecting replies via webhook, handling opt-outs, and enforcing governance at every send.

---

## Trigger
Celery Beat scans for prospects with SequenceState where:
- channel = whatsapp
- status = sequence_active
- next_action_at <= now()
- current_stage in (M1, M2, M3, M4)

---

## Workflow steps

```
Step 1: Celery task fires for prospect + campaign + stage
  → Task ID = {prospect_id}_{campaign_id}_wa_{stage} (idempotency key)
  → If already executed → skip

Step 2: Run governance check stack
  → Same 7-check sequence as email workflow
  → Any failure → halt, log, do not send

Step 3: Fetch approved WhatsApp message
  → Pull message: prospect + campaign + channel=whatsapp + stage + approved
  → Verify opt-out line present in body (secondary safety check)

Step 4: Send via Periskope API
  → POST to Periskope /messages/send with prospect WhatsApp number + body
  → Store Periskope message_id on Touchpoint

Step 5: Create Touchpoint record
  → stage, channel, sent_at, delivery_status = sent

Step 6: Log Pipedrive activity

Step 7: Schedule next stage (same timing as email)

Step 8: Write AuditLog
```

---

## Delivery tracking (via Periskope webhook)
Periskope pushes delivery events to `POST /api/v1/integrations/periskope/webhook/`:
- `sent` → update Touchpoint.delivery_status
- `delivered` → update Touchpoint
- `read` → update Touchpoint
- `failed` → update Touchpoint, flag for review

---

## Reply detection (via Periskope webhook)
Periskope pushes reply events to same webhook endpoint:
- Webhook handler → dispatch Reply Classifier Agent → stop automation

---

## Opt-out handling
Reply contains STOP / unsubscribe / remove me:
→ Create permanent SuppressionRecord
→ Stop all automation
→ Update Pipedrive label
→ AuditLog entry

---

## Acceptance criteria
- [ ] Idempotency prevents duplicate sends
- [ ] Opt-out line verified before every WhatsApp send
- [ ] Delivery status updated from Periskope webhook within 5 min
- [ ] Opt-out creates permanent SuppressionRecord
- [ ] Reply webhook triggers stop automation across all channels
