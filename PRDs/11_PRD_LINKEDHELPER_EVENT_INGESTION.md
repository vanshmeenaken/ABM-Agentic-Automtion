# 11 — LinkedHelper Event Ingestion

**Phase:** 11  
**Inputs from:** LinkedHelper webhook pushes to platform endpoint  
**Outputs to:** Phase 5 (stop automation), Phase 4 (Pipedrive sync), Phase 13 (reply intelligence)

---

## 1. Phase purpose
Build the LinkedHelper webhook receiver, event normalisation layer, raw event storage, LinkedIn event to sequence state mapping, Pipedrive sync on LinkedIn events, and stop automation trigger for LinkedIn replies.

---

## 2. Platform does not control LinkedIn sending
LinkedIn outreach is executed by LinkedHelper (external tool). The platform receives events from LinkedHelper and converts them into platform state and Pipedrive records. LinkedHelper is an event source, not a channel the platform controls.

---

## 3. Event types ingested
| Event type | Platform action |
|-----------|----------------|
| `profile_visited` | Log as Touchpoint, update Pipedrive |
| `connection_request_sent` | Log Touchpoint |
| `connection_accepted` | Update prospect status, log Pipedrive activity |
| `message_sent` | Log Touchpoint + message content |
| `reply_received` | Trigger stop automation + feed Reply Classifier |
| `campaign_finished` | Mark prospect LinkedIn sequence as completed |
| `profile_failed` | Flag prospect, log failure reason |

---

## 4. Webhook receiver
- Endpoint: `POST /api/v1/integrations/linkedhelper/events/`
- Validate webhook signature
- Store raw payload to IntegrationEvent model
- Dispatch to Celery task for async processing

---

## 5. Acceptance criteria
- [ ] Webhook endpoint receives and validates LinkedHelper events
- [ ] Each event type correctly maps to platform state update
- [ ] Reply event triggers cross-channel stop automation within 5 min
- [ ] All events stored as raw IntegrationEvent records
- [ ] Pipedrive activity created for connection accepted and reply received
