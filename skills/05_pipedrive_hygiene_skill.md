# Skill: Pipedrive Hygiene

**Used by:** Data Quality Agent  
**Domain:** CRM deduplication against Pipedrive records

---

## Purpose
Checks platform prospect records against existing Pipedrive persons/leads to detect conflicts, duplicates, and DNC records before campaign assignment.

---

## When to use
During prospect processing, after local deduplication check, as the final pre-assignment gate.

---

## Input schema
```
email: string
phone: string
company_name_normalised: string
pipedrive_api_token: string (from settings)
```

---

## Output schema
```
pipedrive_match_found: bool
pipedrive_person_id: string or null
match_type: enum (email/phone/company_name/none)
existing_label: string or null
is_dnc: bool
is_active_deal: bool
recommended_action: enum (import/skip/review)
```

---

## Domain logic

### Match priority
1. Email exact match → definitive match
2. Phone exact match → strong match, flag for review
3. Company name + last name match → weak match, flag for review

### Recommended action logic
| Condition | Action |
|-----------|--------|
| No match found | `import` — proceed to campaign assignment |
| Match found, no active deal, no DNC | `review` — human decides |
| Match found, active deal | `skip` — prospect already in pipeline |
| Match found, DNC label | `skip` — create SuppressionRecord, block permanently |

---

## Rules
- DNC detection is non-negotiable — never import a DNC prospect
- Active deal detection prevents automation from running on warm prospects
- All Pipedrive checks logged in AuditLog

---

## Failure cases
- Pipedrive API unavailable → defer check, flag for retry, do not import
- Multiple Pipedrive matches → flag all for human review
