# 07 — Prospect Database Builder

**Phase:** 7  
**Inputs from:** Phase 6 (active campaign + ICP definition)  
**Outputs to:** Phase 8 (message intelligence uses enriched, classified prospects)

---

## 1. Phase purpose
Build the prospect import, enrichment, persona classification, deduplication, confidence scoring, and campaign assignment system.

---

## 2. Import sources
| Source | Method |
|--------|--------|
| CSV upload | Manual file upload via control tower UI |
| Pipedrive import | Fetch persons/leads from active Pipedrive filters |
| Enrichment tools | To be defined before Phase 7 implementation (open decision) |

> **Open decision:** Specific enrichment tool (Apollo, Clay, ZoomInfo, etc.) not yet selected. This must be resolved before Phase 7 PRD is expanded for implementation.

---

## 3. Prospect processing pipeline
```
Raw import → Field cleaning → Deduplication check → Enrichment → 
Persona classification → Confidence scoring → Outreach eligibility check → 
Campaign assignment
```

---

## 4. Deduplication logic
- Check by email (primary key)
- Check by phone + company name (secondary)
- Check against existing Pipedrive person records
- Flagged duplicates held for human review before campaign assignment

---

## 5. Confidence scoring
Each prospect receives a confidence score (0–100) based on:
- Email format validity (0–25)
- Phone number validity (0–15)
- Designation string clarity (0–20)
- Company name completeness (0–20)
- Persona classification confidence (0–20)

Prospects below score 40 are flagged for review before outreach eligibility is granted.

---

## 6. Persona tags
| Tag | Maps to designation patterns |
|-----|------------------------------|
| CXO / Strategy | CEO, MD, Founder, President, Director, VP Strategy |
| Marketing | CMO, Marketing Director, Brand Head, Growth |
| Operations | COO, Operations Director, Supply Chain, Logistics |
| Product / R&D | CPO, Product Manager, Innovation, R&D Head |
| Investor | Investment Director, PE/VC, Fund Manager, Asset Manager |
| Procurement | CPO (Procurement), Sourcing, Category Manager |

---

## 7. Acceptance criteria
- [ ] CSV upload imports and cleans records correctly
- [ ] Duplicate prospects flagged before campaign assignment
- [ ] Persona tag assigned to every prospect with confidence score
- [ ] Prospects below confidence 40 held for review
- [ ] Outreach eligibility flag correctly reflects suppression + confidence state
- [ ] Pipedrive import pulls matching person records and maps fields
