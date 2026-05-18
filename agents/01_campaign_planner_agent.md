# Agent: Campaign Planner

**Category:** Campaign  
**Version:** 1.0  
**Workflow:** Campaign Creation Workflow  
**Skills used:** Campaign Planning Skill, ICP Definition Skill

---

## Purpose
Converts a raw campaign idea (name, target market, offer, channel preference) into a fully structured campaign plan including ICP definition, persona map, channel selection, sequence timing, and approval gates.

---

## Trigger
A user submits a new campaign request via the control tower with at minimum: campaign name, target industry, and offer/product.

---

## Input schema
| Field | Type | Required |
|-------|------|----------|
| campaign_name | string | yes |
| target_industry | string | yes |
| target_region | string | yes |
| offer | string | yes |
| campaign_type | enum | yes |
| preferred_channels | list[string] | no |
| notes | string | no |

---

## Reasoning logic
1. Parse campaign name and offer to identify market context
2. Apply ICP Definition Skill to generate firmographic ICP criteria (company size, industry sub-segments, revenue range, region, decision-maker seniority)
3. Map campaign type to default channel mix if no channel preference given
4. Apply B2B Persona Classification Skill to identify primary and secondary buyer personas for this campaign
5. Generate sequence timing recommendations (M1–M4 gaps) based on campaign type
6. Flag whether approval is recommended (always yes for new campaigns)
7. Output structured campaign draft for human review

---

## Output schema
| Field | Type | Description |
|-------|------|-------------|
| campaign_draft | object | Full campaign object ready for DB creation |
| icp_definition | object | Firmographic + behavioural ICP criteria |
| persona_map | list | Primary + secondary persona tags with rationale |
| channel_plan | object | Channel mix with sequence timing per channel |
| approval_flag | bool | Always true for first campaign run |
| confidence_notes | string | Agent notes on ICP assumptions made |

---

## Rules
- Must output at minimum one primary persona tag
- Must output at minimum one channel
- Cannot select a channel that is not configured in platform settings
- Must flag if ICP definition is ambiguous (low-confidence industries or regions)
- Cannot activate a campaign — only creates a draft

---

## Governance constraints
- Agent output is a draft only — no campaign activates without human approval
- Agent cannot write to Pipedrive directly
- All agent runs logged to AuditLog with input + output payload

---

## Failure modes
| Failure | Handling |
|---------|----------|
| Missing required fields | Return validation error, do not run |
| Campaign type not recognised | Default to Market Research, flag in output |
| No matching persona for industry | Output generic CXO/Strategy, flag low confidence |

---

## Evaluation examples
**Input:** `{campaign_name: "India EV Ecosystem Survey", target_industry: "Automotive", target_region: "India", offer: "Survey participation + sector report", campaign_type: "Survey"}`

**Expected output:** ICP targeting India-based automotive OEMs, EV component suppliers, and fleet operators. Primary persona: CXO/Strategy. Secondary: Operations. Channel: WhatsApp + Email. M1 immediately, M2 at day 3, M3 at day 7, M4 at day 12.
