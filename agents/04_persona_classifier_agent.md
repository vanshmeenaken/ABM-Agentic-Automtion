# Agent: Persona Classifier

**Category:** Prospect Intelligence  
**Version:** 1.0  
**Workflow:** Prospect Intake + Dedupe Workflow  
**Skills used:** B2B Persona Classification Skill

---

## Purpose
Maps each prospect's designation and company context to a standardised buyer persona tag with a confidence score. This tag drives message angle selection for all downstream copy agents.

---

## Trigger
Prospect record confirmed clean by Data Quality agent (compliance score >= 40).

---

## Input schema
| Field | Type | Required |
|-------|------|----------|
| designation | string | yes |
| company_type | string | no |
| industry | string | no |
| seniority_signals | list[string] | no |

---

## Reasoning logic
1. Parse designation string into function and seniority components
2. Match against persona tag patterns (see skill: B2B Persona Classification)
3. Apply company type and industry context to resolve ambiguous designations
4. Assign primary persona tag + confidence score
5. Assign secondary persona tag if designation spans two functions (e.g. "COO & CFO")
6. Flag low-confidence assignments (score < 60) for human review

---

## Output schema
| Field | Type | Description |
|-------|------|-------------|
| persona_tag | enum | Primary persona classification |
| secondary_persona_tag | enum or null | Secondary if applicable |
| confidence_score | int (0–100) | Classification confidence |
| classification_reason | string | Brief rationale |
| low_confidence_flag | bool | True if score < 60 |

---

## Persona tags
`cxo_strategy` · `marketing` · `operations` · `product_rd` · `investor` · `procurement` · `unknown`

---

## Rules
- Must assign a persona tag to every prospect — use `unknown` if truly unclassifiable
- `unknown` tag blocks outreach eligibility (requires human review)
- Never infer persona from company name alone — designation must be present
- Confidence score must reflect genuine uncertainty — do not inflate

---

## Failure modes
| Failure | Handling |
|---------|----------|
| Designation field empty | Assign `unknown`, flag for human review |
| Designation in non-English | Translate first, then classify; flag as translated |
| Conflicting signals | Assign lower-confidence primary, flag for review |
