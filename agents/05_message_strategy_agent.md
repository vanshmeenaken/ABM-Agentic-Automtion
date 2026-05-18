# Agent: Message Strategy

**Category:** Message Intelligence  
**Version:** 1.0  
**Workflow:** Message Generation + Approval Workflow  
**Skills used:** Email Outreach Copy Skill, WhatsApp Outreach Copy Skill

---

## Purpose
Decides the outreach angle and relevance narrative before any copy is written. Outputs a strategy brief that drives both Email Copy and WhatsApp Copy agents.

---

## Trigger
Prospect marked outreach-eligible by governance checks, campaign active, message generation job dispatched by Celery.

---

## Input schema
| Field | Type | Required |
|-------|------|----------|
| prospect_id | uuid | yes |
| campaign_id | uuid | yes |
| persona_tag | enum | yes |
| offer | string | yes |
| target_industry | string | yes |
| company_name | string | yes |
| prior_touchpoints | list | no |

---

## Reasoning logic
1. Match persona tag to angle library (see skill)
2. Select 2–3 proof points relevant to industry + persona + offer
3. Determine tone: formal (CXO/Investor), conversational (Marketing/Product), data-led (Operations/Procurement)
4. Determine channel priority based on campaign channel mix + persona preference
5. Generate one-paragraph strategy brief summarising angle, proof points, tone, and CTA direction
6. Pass brief to Email Copy and WhatsApp Copy agents

---

## Output schema
| Field | Type | Description |
|-------|------|-------------|
| strategy_brief | string | One-paragraph outreach strategy |
| primary_angle | string | Core relevance narrative |
| proof_points | list[string] | 2–3 supporting points |
| tone_guidance | enum | formal/conversational/data-led |
| channel_priority | list | Ordered channel preference |
| cta_direction | string | What action the message should drive |

---

## Rules
- Must use persona tag as the primary driver of angle selection
- Cannot use generic, industry-agnostic angles for personalised outreach
- Strategy brief must reference the specific offer — not a generic service description
- Prior touchpoints must influence M2–M4 strategy (escalating proof, not repetition)

---

## Failure modes
| Failure | Handling |
|---------|----------|
| Unknown persona tag | Use generic professional angle, flag low confidence |
| Offer description too vague | Request clarification from campaign owner before generating |
