# 08 — Message Intelligence Layer

**Phase:** 8  
**Inputs from:** Phase 7 (enriched + classified prospect), Phase 6 (campaign offer + persona)  
**Outputs to:** Phase 9 (Email), Phase 10 (WhatsApp), approval queue in Phase 3 (UI)

---

## 1. Phase purpose
Build the agent-driven message generation layer: message strategy, Email M1–M4 copy, WhatsApp M1–M4 copy, LinkedIn draft messages, compliance review, and approval-ready message output.

---

## 2. Agent execution order
```
Message Strategy Agent
        ↓
Email Copy Agent + WhatsApp Copy Agent (run in parallel)
        ↓
Compliance Review Agent (blocks before human approval queue)
        ↓
Human approval queue (via Next.js control tower)
```

---

## 3. Message stages
| Stage | Purpose | Tone |
|-------|---------|------|
| M1 | Cold first touch | Professional, value-forward |
| M2 | First follow-up | Slightly warmer, add proof point |
| M3 | Second follow-up | Social proof or urgency |
| M4 | Final nudge | Alternative CTA, low pressure |

---

## 4. Persona-based message angles
| Persona | Message angle |
|---------|--------------|
| CXO / Strategy | Market positioning, strategic risk, growth signal |
| Marketing | Brand intelligence, competitive insight, campaign data |
| Operations | Efficiency benchmarks, cost data, supply chain insight |
| Product / R&D | Innovation landscape, technology adoption, competitor features |
| Investor | Market sizing, growth projections, sector opportunity |
| Procurement | Supplier intelligence, pricing benchmarks, sourcing data |

---

## 5. Compliance review rules
A message is BLOCKED if it contains:
- False or unverifiable claims
- Overly specific revenue or growth assertions without source
- Regulatory risk language (guarantees, certainties)
- Spam trigger words (free, urgent, act now, limited time)
- Brand risk language
- Missing opt-out language (WhatsApp)
- Excessive length for channel (WhatsApp > 300 words)

---

## 6. Approval states
`pending` → `approved` / `rejected` / `edited_and_approved`

A compliance BLOCK cannot be overridden by a human approver — it must be regenerated or manually rewritten and re-submitted for compliance review.

---

## 7. Acceptance criteria
- [ ] Message strategy output drives email and WhatsApp copy correctly
- [ ] M1–M4 copy generated for both channels per prospect
- [ ] Compliance review runs before any message enters approval queue
- [ ] BLOCK messages cannot be sent under any condition
- [ ] Approved messages are linked to the correct sequence stage
- [ ] Approval state changes are audit logged
