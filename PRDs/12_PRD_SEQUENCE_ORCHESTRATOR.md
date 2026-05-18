# 12 — Sequence Orchestrator

**Phase:** 12  
**Inputs from:** Phase 6 (campaign + sequence config), Phase 9/10/11 (channel states)  
**Outputs to:** Phase 9 (email send), Phase 10 (WA send), Phase 13 (dormant prospects)

---

## 1. Phase purpose
Build the Celery-based sequence scheduling system: M1–M4 progression logic, next-action calculation, retry manager, rate limiting, idempotency keys, and dormant state management.

---

## 2. Sequence timing defaults
| Stage | Default delay from previous |
|-------|----------------------------|
| M1 | Immediate on campaign activation |
| M2 | 3 business days after M1 sent |
| M3 | 4 business days after M2 sent |
| M4 | 5 business days after M3 sent |
| Dormant | 30 days after M4 if no reply |

All timing is configurable per campaign.

---

## 3. Celery task design
- One Celery task per prospect per stage per channel
- Task ID = `{prospect_id}_{campaign_id}_{channel}_{stage}` (idempotency key)
- Duplicate task ID → skip (idempotent)
- Task runs governance check stack before executing send
- Failed task → retry with exponential backoff (max 3 retries)

---

## 4. Rate limiting
- Per sender account: max 200 emails/day, max 50 WhatsApp/day
- Rate limit checked inside governance before every send
- If limit reached → defer task to next available window

---

## 5. Dormant state
- Prospect moves to `dormant` after M4 with no reply and no stop trigger
- Dormant prospects excluded from active sequences
- Can be reactivated manually or via Account Reactivation campaign type

---

## 6. Acceptance criteria
- [ ] M1–M4 tasks scheduled correctly on campaign activation
- [ ] Idempotency key prevents duplicate sends
- [ ] Rate limit respected per sender account
- [ ] Failed send retried up to 3 times with backoff
- [ ] Prospect moves to dormant after M4 with no response
- [ ] Paused campaign cancels all pending Celery tasks immediately
