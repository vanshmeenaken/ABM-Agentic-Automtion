# Skill: Campaign Planning

**Used by:** Campaign Planner Agent  
**Domain:** Campaign strategy

---

## Purpose
Converts a campaign idea into a structured campaign plan: ICP, persona, channel mix, sequence timing, and approval rules.

---

## When to use
When a new campaign request is submitted and a Campaign Planner Agent run is initiated.

---

## Input schema
```
campaign_name: string
target_industry: string
target_region: string
offer: string
campaign_type: enum
preferred_channels: list (optional)
```

---

## Output schema
```
icp_criteria: object
persona_map: list
channel_plan: object
sequence_timing: object
approval_recommendation: bool
```

---

## Domain logic

### Campaign type → default channel mix
| Type | Default channels |
|------|-----------------|
| Market Research | Email + WhatsApp |
| Survey | WhatsApp + Email |
| Consulting | Email + LinkedIn |
| Expert Network | LinkedIn + Email |
| Webinar | Email + WhatsApp |
| Report Sales | Email |
| Competition Benchmarking | Email |
| Account Reactivation | WhatsApp + Email |

### Default sequence timing
| Stage | Delay |
|-------|-------|
| M1 | Day 0 |
| M2 | Day 3 |
| M3 | Day 7 |
| M4 | Day 12 |

---

## Rules
- Every campaign must have at least one channel
- Approval is always recommended for first-run campaigns
- Campaign type must map to a recognised type — default to Market Research if unrecognised

---

## Failure cases
- If industry is too broad (e.g. "Technology") → request sub-industry refinement
- If offer is a single word → request expansion before planning

---

## Evaluation examples
**Good:** "India EV Ecosystem Survey targeting automotive OEMs" → WhatsApp + Email, CXO + Operations persona, Survey type
**Bad:** Generating a campaign plan for "everything" with no ICP constraints
