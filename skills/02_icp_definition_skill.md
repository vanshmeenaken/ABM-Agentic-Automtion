# Skill: ICP Definition

**Used by:** Campaign Planner Agent  
**Domain:** Ideal Customer Profile construction

---

## Purpose
Generates a structured Ideal Customer Profile (ICP) from campaign inputs, including firmographic, behavioural, and environmental criteria, plus Negative ICP signals.

---

## When to use
During Campaign Planner Agent execution, after basic campaign parameters are confirmed.

---

## Input schema
```
target_industry: string
target_region: string
campaign_type: string
offer: string
persona_preference: list (optional)
```

---

## Output schema
```
icp_positive:
  industries: list
  sub_segments: list
  company_size: object (min/max employees or revenue)
  regions: list
  seniority_levels: list
  decision_maker_functions: list
  buying_signals: list

icp_negative:
  excluded_company_types: list
  excluded_industries: list
  excluded_regions: list
  excluded_company_sizes: list
```

---

## Domain logic

### Seniority mapping by campaign type
| Campaign type | Target seniority |
|---------------|-----------------|
| Market Research | C-suite, VP, Director |
| Survey | Manager+, Director+ |
| Consulting | C-suite, VP |
| Expert Network | Senior Manager+ |
| Report Sales | Manager, Director, VP |

### Negative ICP signals
Always exclude:
- Competitors of Ken Research
- Companies already in active sales pipeline (Pipedrive active deals)
- Companies marked DNC in suppression records
- Freelancers and sole traders (company size = 1)

---

## Rules
- Always define both Positive and Negative ICP
- Sub-segments must be more specific than the top-level industry
- Never define a Negative ICP that contradicts the Positive ICP

---

## Failure cases
- Industry too vague → flag and request sub-segment clarification
- Region not mapped to a timezone → default to business hours UTC+5:30 for India

---

## Evaluation examples
**Input:** Industry: Automotive, Region: India, Type: Survey
**Output ICP positive:** India-based automotive OEMs, EV component suppliers, fleet operators (500+ employees, Director+)
**Output ICP negative:** Solo consultants, companies with active Ken Research deals, competitors
