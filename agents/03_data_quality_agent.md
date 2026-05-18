# Agent: Data Quality

**Category:** Prospect Intelligence  
**Version:** 1.0  
**Workflow:** Prospect Intake + Dedupe Workflow  
**Skills used:** Prospect Data Cleaning Skill, Pipedrive Hygiene Skill

---

## Purpose
Cleans raw prospect records — company names, designation strings, email formats, phone numbers. Flags duplicate risks and scores each record's reliability before it enters the sequence or Pipedrive.

---

## Trigger
Raw prospect import batch received from Prospect Research agent or CSV upload.

---

## Input schema
| Field | Type | Required |
|-------|------|----------|
| raw_prospects | list | yes |
| campaign_id | uuid | yes |
| dedup_scope | enum (campaign/platform/pipedrive) | yes |

---

## Reasoning logic
1. Normalise email addresses (lowercase, trim whitespace, remove invalid formats)
2. Normalise phone numbers (E.164 format, country code completion based on region)
3. Clean company names (remove Inc/Ltd/Pvt suffixes for matching, preserve for display)
4. Clean designation strings (standardise common variants: "MD" → "Managing Director", "VP Mktg" → "VP Marketing")
5. Run deduplication check: email match (primary), phone + company match (secondary), Pipedrive person record match (tertiary)
6. Score each record (0–100) based on field completeness and format validity
7. Flag records below score threshold for human review
8. Return cleaned list with duplicate flags and confidence scores

---

## Output schema
| Field | Type | Description |
|-------|------|-------------|
| cleaned_prospects | list | Records with normalised fields |
| duplicate_flags | list | Records flagged as potential duplicates |
| low_confidence_flags | list | Records below score 40 |
| field_corrections | object | Summary of corrections made |
| confidence_score_distribution | object | Score histogram for review |

---

## Confidence scoring
| Field | Max points |
|-------|------------|
| Valid email format | 25 |
| Valid phone number | 15 |
| Designation string clarity | 20 |
| Company name completeness | 20 |
| Field completeness overall | 20 |

---

## Rules
- Never discard a record — flag it instead
- Duplicates must be reviewed by a human before campaign assignment
- Correction log must be written for every field modification

---

## Failure modes
| Failure | Handling |
|---------|----------|
| All records below score 40 | Flag entire batch for human review, halt campaign assignment |
| >30% duplicate rate | Flag for ICP refinement review |
