# Skill: B2B Persona Classification

**Used by:** Persona Classifier Agent, Campaign Planner Agent  
**Domain:** Buyer persona mapping

---

## Purpose
Maps a prospect's designation and company context to a standardised Ken Research buyer persona tag.

---

## When to use
When processing any prospect record that requires persona assignment.

---

## Input schema
```
designation: string
company_type: string (optional)
industry: string (optional)
```

---

## Output schema
```
persona_tag: enum
secondary_persona_tag: enum or null
confidence_score: int (0–100)
classification_reason: string
```

---

## Persona tag definitions

| Tag | Designation patterns |
|-----|---------------------|
| `cxo_strategy` | CEO, MD, Managing Director, Founder, President, COO, CSO, Director General, VP Strategy, Head of Strategy, Country Manager |
| `marketing` | CMO, Chief Marketing Officer, VP Marketing, Marketing Director, Brand Director, Growth Head, Digital Marketing Head |
| `operations` | COO, Operations Director, VP Operations, Supply Chain Director, Head of Logistics, Plant Head, Manufacturing Director |
| `product_rd` | CPO, Product Director, VP Product, Head of Innovation, R&D Director, Technology Head, CTO (product context) |
| `investor` | Investment Director, Portfolio Manager, Fund Manager, VC Partner, PE Director, Asset Manager, CIO (investment) |
| `procurement` | CPO (Procurement), Sourcing Director, Head of Procurement, Category Manager, Supply Chain Manager |
| `unknown` | Designation absent, unrecognisable, or genuinely ambiguous |

---

## Domain logic

### Confidence scoring
- Exact pattern match → 90–100
- Partial pattern match (one word) → 60–80
- Context inference (company type + seniority but unclear function) → 40–60
- Truly ambiguous → < 40

### Ambiguity resolution rules
- "Director" alone → check company type; FMCG = Marketing; Logistics = Operations; Finance = CXO
- "CFO" → CXO/Strategy (financial leadership, not procurement)
- "CTO" → check context; product company = Product/R&D; IT services = Operations or CXO
- "Partner" at a consulting firm → CXO/Strategy

---

## Rules
- Never classify based on company name alone
- `unknown` must be used when genuinely unclassifiable — do not force a low-confidence assignment
- Designation in non-English must be translated before classification

---

## Failure cases
- Blank designation → always `unknown`
- "Manager" alone with no context → `unknown` (too generic)
- Dual roles ("COO & CFO") → classify primary function + secondary function

---

## Evaluation examples
| Designation | Expected tag | Confidence |
|-------------|-------------|------------|
| "Managing Director" | cxo_strategy | 95 |
| "VP Marketing, APAC" | marketing | 92 |
| "Director" (no context) | unknown | 35 |
| "Head of Supply Chain" | operations | 88 |
| "Portfolio Manager, PE Fund" | investor | 91 |
