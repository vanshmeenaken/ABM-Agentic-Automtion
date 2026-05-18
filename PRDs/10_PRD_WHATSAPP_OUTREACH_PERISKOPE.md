# 10 — WhatsApp Outreach via Periskope

**Phase:** 10  
**Inputs from:** Phase 8 (approved messages), Phase 12 (Celery triggers)  
**Outputs to:** Phase 13 (reply detection)

---

## 1. Phase purpose
Implement WhatsApp M1–M4 sending via Periskope API, delivery status tracking, reply webhook handling, opt-out processing, and Pipedrive activity logging.

---

## 2. Send flow
```
Celery scheduled task fires
  → Governance check stack
  → Fetch approved WhatsApp message
  → Send via Periskope API
  → Store Periskope message_id
  → Create Touchpoint record
  → Log activity in Pipedrive
  → Write AuditLog
```

---

## 3. Periskope operations
| Operation | Method |
|-----------|--------|
| Send message | `POST /messages/send` |
| Delivery status webhook | Periskope pushes to platform webhook endpoint |
| Reply webhook | Periskope pushes to platform webhook endpoint |
| Opt-out detection | Parse STOP/unsubscribe keywords in reply |

---

## 4. Delivery status tracking
- `sent` → message dispatched to WhatsApp
- `delivered` → message delivered to device
- `read` → message read by recipient
- `failed` → delivery failed (log reason, flag for review)

---

## 5. Opt-out handling
If reply contains opt-out keywords (STOP, unsubscribe, remove me, don't contact): create SuppressionRecord → stop all automation → update Pipedrive → AuditLog.

---

## 6. Acceptance criteria
- [ ] WhatsApp M1 sends correctly via Periskope
- [ ] Delivery status updated on Touchpoint within 5 min
- [ ] Reply webhook triggers stop automation
- [ ] Opt-out creates permanent SuppressionRecord
- [ ] Governance check prevents send if prospect already replied or stopped
