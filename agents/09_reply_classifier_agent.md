# Agent: Reply Classifier

**Category:** Response + Handoff  
**Version:** 1.0  
**Workflow:** Reply Detection + Stop Automation Workflow  
**Skills used:** Reply Classification Skill

---

## Purpose
Classifies inbound reply intent from any channel, issues an immediate stop flag, and determines the recommended next action. Stop automation fires before classification is complete.

---

## Trigger
Inbound reply detected on Email (Microsoft Graph), WhatsApp (Periskope webhook), or LinkedIn (LinkedHelper webhook).

---

## Input schema
| Field | Type | Required |
|-------|------|----------|
| reply_text | string | yes |
| channel | enum | yes |
| prospect_id | uuid | yes |
| campaign_id | uuid | yes |
| prior_touchpoints | list | no |

---

## Reasoning logic
1. Issue stop flag IMMEDIATELY — do not wait for classification (stop is unconditional)
2. Parse reply text for intent signals
3. Classify into primary intent category
4. Assign confidence score
5. Determine recommended next action based on intent category
6. Output classification + recommendation to handoff layer

---

## Output schema
| Field | Type | Description |
|-------|------|-------------|
| stop_flag | bool | Always true |
| intent_category | enum | Reply intent classification |
| confidence_score | int (0–100) | Classification confidence |
| recommended_action | string | What to do next |
| requires_human_review | bool | True if ambiguous or low confidence |

---

## Intent categories
| Category | Signals | Next action |
|----------|---------|------------|
| `positive_interest` | "Tell me more", "Sounds interesting", "Let's connect" | Create handoff |
| `meeting_request` | "Can we schedule?", "Available for a call?" | Create handoff + meeting ready |
| `question` | "What is this?", "Who are you?" | Create handoff for sales response |
| `negative` | "Not interested", "Remove me", "Wrong person" | Create suppression record |
| `out_of_office` | OOO auto-reply signals | Log, set resume date if detectable |
| `bounce` | NDR, delivery failure | Flag email, update prospect record |
| `ambiguous` | Unclear or minimal content | Flag for human review |

---

## Rules
- Stop flag is always true regardless of intent category
- OOO replies do not create a suppression record — they create a temporary pause
- Bounce replies do not create a handoff — they update the prospect's contact validity
- Confidence below 60 → always flag for human review
- This agent cannot be bypassed under any circumstances

---

## Failure modes
| Failure | Handling |
|---------|----------|
| Reply text empty or binary | Classify as `ambiguous`, flag for human review |
| Agent errors mid-classification | Stop flag already issued, flag for manual review |
