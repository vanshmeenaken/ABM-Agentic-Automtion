# 13 — Reply Intelligence and Manual Handoff

**Phase:** 13  
**Inputs from:** Phase 9 (email reply), Phase 10 (WA reply), Phase 11 (LinkedIn reply)  
**Outputs to:** Phase 14 (meeting booking), Phase 3 (handoff queue UI), Phase 4 (Pipedrive)

---

## 1. Phase purpose
Build reply classification, intent detection, stop automation trigger, manual handoff object creation, owner notification, and suggested response generation.

---

## 2. Reply intent categories
| Category | Description | Next action |
|----------|-------------|------------|
| `positive_interest` | Prospect wants to learn more or meet | Create handoff immediately |
| `meeting_request` | Direct request for a call or demo | Create handoff + meeting readiness |
| `question` | Prospect asks for more information | Create handoff for sales to respond |
| `negative` | Not interested, wrong person, remove me | Create suppression record |
| `out_of_office` | Automated OOO reply | Log, resume after OOO end date if detectable |
| `bounce` | Delivery failure | Flag email, do not create handoff |
| `ambiguous` | Unclear intent | Flag for human review |

---

## 3. Stop automation — always first
Regardless of intent category, stop flag is issued first. Automation stops before classification is even complete.

---

## 4. Handoff object fields
```
prospect, campaign, owner, reply_content, intent_category,
confidence_score, full_touchpoint_history, handoff_brief (text),
suggested_response (text), meeting_ready (bool),
status (pending/in_progress/completed)
```

---

## 5. Handoff brief generation
The Sales Handoff Agent generates:
- Who the prospect is (name, title, company, persona)
- What was sent to them (M1–M4 summary)
- What they replied
- Recommended response tone and content
- Whether to propose a meeting directly

---

## 6. Owner notification
On handoff creation:
- Notification pushed to owner in control tower UI
- Pipedrive activity created and assigned to owner
- Note added to Pipedrive lead with handoff brief

---

## 7. Acceptance criteria
- [ ] All reply types classified within 5 min of receipt
- [ ] Stop automation fires before classification completes
- [ ] Handoff created for positive_interest, meeting_request, and question intents
- [ ] Negative reply creates suppression record
- [ ] Owner notified via UI and Pipedrive activity
- [ ] Handoff brief contains complete prospect history
