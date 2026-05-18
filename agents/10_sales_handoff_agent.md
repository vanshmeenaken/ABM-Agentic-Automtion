# Agent: Sales Handoff

**Category:** Response + Handoff  
**Version:** 1.0  
**Workflow:** Sales Handoff + Meeting Booking Workflow  
**Skills used:** Manual Handoff Skill, Meeting Booking Skill

---

## Purpose
Builds a complete sales handoff brief — who the prospect is, what was sent, what they replied, what to say next, and whether a meeting should be proposed immediately. Assigns the handoff to the campaign sales owner in Pipedrive.

---

## Trigger
Positive reply or meeting intent confirmed by Reply Classifier (intent_category: `positive_interest`, `meeting_request`, or `question`).

---

## Input schema
| Field | Type | Required |
|-------|------|----------|
| prospect_id | uuid | yes |
| campaign_id | uuid | yes |
| reply_text | string | yes |
| intent_category | enum | yes |
| all_touchpoints | list | yes |
| persona_tag | enum | yes |
| owner_id | uuid | yes |

---

## Reasoning logic
1. Pull full prospect record (name, title, company, persona)
2. Pull complete touchpoint history (all M1–M4 sent, delivery status, opens if available)
3. Parse reply for key signals and questions raised by prospect
4. Generate handoff brief: prospect overview + outreach history summary + reply context
5. Generate suggested response: what to say next, matching the prospect's intent
6. Set meeting_ready flag if intent is `meeting_request` or `positive_interest`
7. Assign handoff to campaign owner
8. Create Pipedrive activity + note with brief

---

## Output schema
| Field | Type | Description |
|-------|------|-------------|
| handoff_brief | string | Full formatted brief for sales owner |
| suggested_response | string | Draft response to the prospect's reply |
| meeting_ready | bool | Whether to propose a meeting immediately |
| talking_points | list[string] | Key discussion points for the meeting |
| pipedrive_activity_id | string | Activity created in Pipedrive |
| owner_notified | bool | Notification sent to owner |

---

## Handoff brief structure
```
PROSPECT: [Name], [Title], [Company]
PERSONA: [Tag]
CAMPAIGN: [Campaign name]

OUTREACH HISTORY:
  M1 sent [date] — [subject/first line]
  M2 sent [date] — [subject/first line]
  ...

THEIR REPLY: [Reply text]
INTENT: [Category]

RECOMMENDED NEXT STEP: [Action]
SUGGESTED RESPONSE: [Draft]

TALKING POINTS FOR MEETING:
  - [Point 1]
  - [Point 2]
  - [Point 3]
```

---

## Rules
- Handoff brief must reference actual touchpoint history — not generic placeholders
- Suggested response must match the prospect's actual intent — not a canned template
- Meeting_ready = True only for `positive_interest` and `meeting_request` intents
- `question` intents get handoff but meeting_ready = False
- Owner must be notified within 5 minutes of handoff creation

---

## Failure modes
| Failure | Handling |
|---------|----------|
| Touchpoint history unavailable | Generate brief with available data, flag missing history |
| Owner not found for campaign | Assign to platform admin, raise alert |
| Pipedrive activity creation fails | Retry 3x, then flag for manual Pipedrive update |
