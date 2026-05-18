# Workflow: Prospect Intake + Dedupe

**Workflow ID:** WF-002  
**Agents involved:** Prospect Research Agent, Data Quality Agent, Persona Classifier Agent  
**Skills involved:** B2B Persona Classification, Prospect Data Cleaning, Pipedrive Hygiene  
**Phase:** Phase 7 (Prospect Database Builder)

---

## Purpose
Imports, cleans, enriches, deduplicates, and classifies prospect records before campaign assignment.

---

## Trigger
- User uploads CSV to campaign prospect page, OR
- User triggers Pipedrive import for a campaign, OR
- Prospect Research Agent completes a build run

---

## Pre-conditions
- Campaign status = active or pending_approval
- Pipedrive integration configured (for dedup check)
- Data source confirmed (CSV or Pipedrive)

---

## Workflow steps

```
Step 1: Receive raw records
  → CSV: parse and validate file format
  → Pipedrive: fetch persons matching ICP filter
  → Research agent: receive raw_prospects output
  → Count and log incoming records

Step 2: Run Data Quality Agent
  → Clean email, phone, company, designation for each record
  → Identify duplicates within batch (email primary key)
  → Score each record (0–100)
  → Flag duplicates and low-confidence records
  → Log corrections

Step 3: Run Pipedrive Hygiene Skill
  → Check each cleaned record against Pipedrive persons
  → Flag if DNC found → create SuppressionRecord
  → Flag if active deal found → skip record
  → Flag if weak match → queue for human review

Step 4: Run Persona Classifier Agent
  → Classify each clean, non-flagged record
  → Assign persona_tag + confidence_score
  → Flag unknown personas for human review

Step 5: Outreach eligibility gate
  → Set outreach_eligible = True if:
        confidence_score >= 40 AND
        persona_tag != unknown AND
        not suppressed AND
        not duplicate
  → All others: outreach_eligible = False, reason logged

Step 6: Campaign assignment
  → Assign eligible prospects to campaign
  → Create SequenceState records (status = new)
  → Log AuditLog: prospect_assigned

Step 7: Human review queue
  → Route flagged records (duplicates, low confidence, unknown persona) to review UI
  → Human resolves each flag: approve / reject / edit
```

---

## Governance gates
- DNC prospects are never assigned to any campaign — ever
- Active Pipedrive deal prospects are skipped automatically
- Outreach eligibility requires passing all 4 criteria (score, persona, suppression, duplicate)

---

## Stop path
- If all records fail eligibility → flag campaign for ICP refinement, notify owner

---

## Audit log events
| Event | Trigger |
|-------|---------|
| `prospects_imported` | Raw records received |
| `prospect_cleaned` | Data Quality Agent output |
| `prospect_suppressed` | DNC found in Pipedrive |
| `prospect_assigned` | Campaign assignment complete |
| `prospect_flagged` | Sent to human review queue |

---

## Acceptance criteria
- [ ] DNC prospects never assigned to campaign
- [ ] All corrections logged per record
- [ ] Unknown persona blocks outreach eligibility
- [ ] Human review queue populated with all flagged records
- [ ] AuditLog written at every step
