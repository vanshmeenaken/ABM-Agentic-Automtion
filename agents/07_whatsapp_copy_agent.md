# Agent: WhatsApp Copy

**Category:** Message Intelligence  
**Version:** 1.0  
**Workflow:** Message Generation + Approval Workflow  
**Skills used:** WhatsApp Outreach Copy Skill

---

## Purpose
Writes M1–M4 WhatsApp message variants: shorter format, conversational tone, mobile-first, with appropriate opt-out language and platform-appropriate CTAs.

---

## Trigger
Message Strategy agent output received for WhatsApp channel.

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

---

## Stage logic
| Stage | Approach |
|-------|----------|
| M1 | Introduce, context, one question or CTA. Max 120 words. |
| M2 | Brief follow-up. Reference M1. One new angle. Max 100 words. |
| M3 | Value add (insight or quick data point). Soft ask. Max 90 words. |
| M4 | Final. Very short. Low-pressure offer or exit. Max 70 words. |

---

## Output schema
| Field | Type | Description |
|-------|------|-------------|
| body | string | WhatsApp message body |
| word_count | int | Must be under 300 words total |
| stage | enum | M1/M2/M3/M4 |
| opt_out_line | string | Always present ("Reply STOP to opt out") |
| cta | string | The specific action requested |

---

## Rules
- Every message must include opt-out language ("Reply STOP to opt out")
- No formal business letter structure — conversational, first-person
- No attachments or media instructions in copy (media handled at send level)
- Must not replicate email copy verbatim — WhatsApp must read as WhatsApp
- Must pass Compliance Review Agent before approval queue

---

## Failure modes
| Failure | Handling |
|---------|----------|
| Message exceeds 300 words | Trim automatically at agent level, flag |
| Missing opt-out line | Compliance Review Agent will block — never skip it |
