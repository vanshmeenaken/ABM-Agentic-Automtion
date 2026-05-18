# 09 — Email Outreach via Microsoft Graph

**Phase:** 9  
**Inputs from:** Phase 8 (approved messages), Phase 12 (Celery schedule triggers send)  
**Outputs to:** Phase 13 (reply detection feeds reply intelligence)

---

## 1. Phase purpose
Implement Microsoft Graph email sending, conversation thread tracking, sent message logging, email reply detection, bounce detection, and Pipedrive activity logging for email channel.

---

## 2. Send flow
```
Celery scheduled task fires (M1/M2/M3/M4 due)
  → Governance check stack (Phase 5)
  → Fetch approved message from DB
  → Send via Microsoft Graph API
  → Store conversation_id + message_id
  → Create Touchpoint record
  → Log activity in Pipedrive
  → Write AuditLog
```

---

## 3. Microsoft Graph operations
| Operation | Endpoint |
|-----------|---------|
| Send email | `POST /me/sendMail` |
| Fetch sent messages | `GET /me/messages?$filter=conversationId eq '{id}'` |
| Watch for replies | Poll conversation thread every 10 min via Celery Beat |
| Read reply content | `GET /me/messages/{reply_id}` |

---

## 4. Conversation tracking
- Store `conversationId` and `internetMessageId` on Touchpoint record
- All M2–M4 follow-ups sent in same thread (same conversationId)
- Reply detection checks conversation thread for new messages from prospect

---

## 5. Bounce detection
- Parse delivery failure NDR messages from inbox
- Classify: hard bounce (invalid email) vs soft bounce (mailbox full)
- Hard bounce → mark prospect email as invalid + flag for review
- Soft bounce → retry once after 24h, then flag

---

## 6. Acceptance criteria
- [ ] Email M1 sends correctly via Microsoft Graph
- [ ] M2–M4 follow-ups appear in same thread
- [ ] Reply detected within 10 min of receipt
- [ ] Bounce classified and prospect record updated
- [ ] All sends logged as Pipedrive activities
- [ ] Governance check prevents send if prospect replied or stopped
