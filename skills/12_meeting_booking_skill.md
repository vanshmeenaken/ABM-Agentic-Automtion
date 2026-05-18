# Skill: Meeting Booking

**Used by:** Sales Handoff Agent, Meeting Booking Module (Phase 14)  
**Domain:** Meeting facilitation and call brief generation

---

## Purpose
Provides the structure for meeting readiness assessment, slot suggestion, meeting brief generation, and Pipedrive meeting activity creation.

---

## When to use
When Sales Handoff Agent sets meeting_ready = True, or when a sales owner confirms they want to book a meeting from the handoff queue.

---

## Meeting readiness criteria
Meeting_ready = True when reply intent is `positive_interest` or `meeting_request`.
Meeting_ready = False when intent is `question` (handoff first, meeting after question resolved).

---

## Meeting brief structure

```
═══════════════════════════════════════
MEETING BRIEF
═══════════════════════════════════════
Prospect: [Name], [Title], [Company]
Persona: [Tag]
Meeting type: Discovery / Follow-up / Demo
Duration: 30 minutes (recommended)

═══════════════════════════════════════
CONTEXT
═══════════════════════════════════════
[2–3 sentence summary of the outreach and reply context]

═══════════════════════════════════════
SUGGESTED OPENING
═══════════════════════════════════════
[One sentence opening to anchor the meeting]

═══════════════════════════════════════
KEY DISCUSSION POINTS
═══════════════════════════════════════
1. [Discovery question aligned to persona]
2. [Relevance question: how this offer applies to their context]
3. [Next step question: what would make this valuable for them]

═══════════════════════════════════════
OFFER CONTEXT
═══════════════════════════════════════
[One paragraph on the specific campaign offer and what to present]
═══════════════════════════════════════
```

---

## Pipedrive activity fields
| Field | Value |
|-------|-------|
| Activity type | Meeting |
| Subject | `Meeting with [Name] — [Campaign name]` |
| Due date | As set by sales owner |
| Owner | Campaign owner |
| Associated lead | Prospect's Pipedrive lead ID |
| Note | Meeting brief text |

---

## Rules
- Meeting brief must be generated before Pipedrive activity is created
- Discussion points must be persona-specific — not generic discovery questions
- Pipedrive activity must be assigned to the campaign owner, not a system user
