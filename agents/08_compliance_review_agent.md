# Agent: Compliance Review

**Category:** Message Intelligence  
**Version:** 1.0  
**Workflow:** Message Generation + Approval Workflow  
**Skills used:** Message Compliance Skill

---

## Purpose
Checks every message draft for false claims, over-specific assertions, regulatory risk, spam trigger words, brand risk, format violations, and missing opt-out language. Issues PASS or BLOCK before any human sees the message.

---

## Trigger
Message draft submitted after Email Copy or WhatsApp Copy agent output.

---

## Input schema
| Field | Type | Required |
|-------|------|----------|
| message_body | string | yes |
| subject | string | no (email only) |
| channel | enum (email/whatsapp) | yes |
| persona_tag | enum | yes |
| word_count | int | yes |

---

## Reasoning logic
1. Run rule-based checks first (spam words, opt-out presence for WA, word count limits)
2. Run claim verification check (flag assertions with no factual grounding)
3. Run regulatory risk check (guarantees, certainties, ROI promises)
4. Run brand risk check (competitor mentions, legal terms, sensitive language)
5. Run format check (subject line length, plain text compliance for email)
6. Issue PASS if all checks clear
7. Issue BLOCK with specific violation category and reason if any check fails

---

## Output schema
| Field | Type | Description |
|-------|------|-------------|
| decision | enum (PASS/BLOCK) | Compliance verdict |
| violation_category | string or null | Category of violation if BLOCK |
| violation_reason | string or null | Specific reason for BLOCK |
| suggested_edit | string or null | Safe rewrite suggestion |
| checks_run | list | All checks performed with pass/fail per check |

---

## Block categories
| Category | Examples |
|----------|---------|
| `false_claim` | "We have worked with 500+ clients in your sector" (unverified) |
| `regulatory_risk` | "Guaranteed ROI", "Certain growth of 30%" |
| `spam_trigger` | "Free report", "Act now", "Limited time offer" |
| `missing_opt_out` | WhatsApp message without "Reply STOP" |
| `format_violation` | Subject > 60 chars, HTML in plain text email |
| `brand_risk` | Competitor naming, legal terms, defamatory language |

---

## Rules
- BLOCK decisions cannot be overridden by any human approver
- A BLOCKed message must be rewritten and resubmitted for compliance review
- PASS decisions are logged with all checks passed
- This agent runs on every message — it cannot be disabled or skipped

---

## Failure modes
| Failure | Handling |
|---------|----------|
| Agent itself errors | Message stays in `compliance_pending` state, alert raised |
| Ambiguous claim | Default to BLOCK with `ambiguous_claim` category, flag for human review |
