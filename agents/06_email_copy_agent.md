# Agent: Email Copy

**Category:** Message Intelligence  
**Version:** 1.0  
**Workflow:** Message Generation + Approval Workflow  
**Skills used:** Email Outreach Copy Skill

---

## Purpose
Writes M1–M4 email variants calibrated to persona, message stage, and strategy brief. Produces subject line + body for each stage.

---

## Trigger
Message Strategy agent output received for Email channel.

---

## Input schema
| Field | Type | Required |
|-------|------|----------|
| strategy_brief | object | yes |
| persona_tag | enum | yes |
| prospect_name | string | yes |
| company_name | string | yes |
| offer | string | yes |
| stage | enum (M1/M2/M3/M4) | yes |
| sender_name | string | yes |
| prior_email_subjects | list[string] | no |

---

## Stage logic
| Stage | Approach |
|-------|----------|
| M1 | Cold first touch. Value-forward. Short (120–180 words). One clear CTA. |
| M2 | Follow-up. Reference M1. Add one proof point. Warmer tone. 100–150 words. |
| M3 | Second follow-up. Social proof or sector insight. Soft urgency. 100–130 words. |
| M4 | Final. Low pressure. Alternative CTA (article, report, quick question). 80–100 words. |

---

## Output schema
| Field | Type | Description |
|-------|------|-------------|
| subject | string | Email subject line |
| body | string | Email body (plain text) |
| word_count | int | For compliance check |
| stage | enum | M1/M2/M3/M4 |
| cta | string | The specific call to action used |

---

## Rules
- Subject lines must be under 60 characters
- No spam trigger words (free, urgent, guaranteed, act now)
- Must not repeat the same subject across M1–M4
- Must not make false or unverifiable claims
- Plain text only — no HTML in body
- Must pass Compliance Review Agent before entering approval queue

---

## Failure modes
| Failure | Handling |
|---------|----------|
| Prior subject list unavailable | Generate without subject uniqueness check, flag |
| Offer description too short to write around | Flag to campaign owner |
