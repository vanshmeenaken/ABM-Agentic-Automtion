# Skill: Manual Handoff

**Used by:** Sales Handoff Agent  
**Domain:** Sales-ready handoff brief generation

---

## Purpose
Provides the structure, required fields, and quality rules for generating a complete manual handoff brief that gives a sales owner everything they need to take over a prospect.

---

## When to use
When a reply is classified as `positive_interest`, `meeting_request`, or `question` and the Sales Handoff Agent is triggered.

---

## Handoff brief structure

```
═══════════════════════════════════════
PROSPECT BRIEF
═══════════════════════════════════════
Name: [First Last]
Title: [Designation]
Company: [Company name]
Persona: [Persona tag]
Campaign: [Campaign name]
Channel of reply: [Email / WhatsApp / LinkedIn]

═══════════════════════════════════════
OUTREACH HISTORY
═══════════════════════════════════════
M1 — [Date] — [Subject or first line] — [Delivery status]
M2 — [Date] — [Subject or first line] — [Delivery status]
M3 — [Date] — [Subject or first line] — [Delivery status]
M4 — [Date if sent] — [Subject or first line] — [Delivery status]

═══════════════════════════════════════
THEIR REPLY
═══════════════════════════════════════
[Full reply text]
Intent: [Category]
Confidence: [Score]

═══════════════════════════════════════
RECOMMENDED NEXT STEP
═══════════════════════════════════════
[Clear, specific action for the sales owner]

═══════════════════════════════════════
SUGGESTED RESPONSE
═══════════════════════════════════════
[Draft reply to prospect]

═══════════════════════════════════════
MEETING READY: [Yes / No]
═══════════════════════════════════════
```

---

## Quality rules
- Every section must be populated — no empty sections
- Outreach history must show actual M-stages sent (not generic "multiple emails sent")
- Suggested response must respond to the prospect's actual reply, not a template
- Talking points must reference the specific persona and offer

---

## Failure cases
- Touchpoint history missing → populate with "History unavailable — check Pipedrive" and flag
- Prospect record incomplete → populate with available fields, flag missing ones
