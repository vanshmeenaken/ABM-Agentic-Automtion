# 06 — Campaign Engine

**Phase:** 6  
**Inputs from:** Phase 2 (campaign model), Phase 5 (governance)  
**Outputs to:** Phase 7 (prospect builder), Phase 8 (message intelligence)

---

## 1. Phase purpose
Build the campaign object business logic: creation, approval workflow, status lifecycle, campaign type configuration, channel mix selection, sequence settings, and ownership assignment.

---

## 2. Campaign lifecycle
```
draft → pending_approval → active → paused ↔ active → completed → archived
```
- Campaign cannot go active without approval
- Paused campaign can be resumed (reactivated)
- Completed campaign is read-only
- Archived campaign is hidden from active views

---

## 3. Campaign types and default channel mixes
| Campaign type | Default channel mix |
|---------------|---------------------|
| Market Research | Email + WhatsApp |
| Competition Benchmarking | Email |
| Survey | WhatsApp + Email |
| Consulting | Email + LinkedIn |
| Expert Network | LinkedIn + Email |
| Webinar | Email + WhatsApp |
| Report Sales | Email |
| Account Reactivation | WhatsApp + Email |

---

## 4. Campaign creation fields
- Name, campaign type, target industry, target region, target persona
- Offer / product being promoted
- Channel mix selection
- Sequence length (M1–M4 or custom)
- Approval requirement (yes/no)
- Owner (sales/marketing user)
- Success metric (meeting booked / positive reply / qualified opportunity / revenue)

---

## 5. Approval workflow
If `requires_approval = True`:
1. Campaign creator submits draft
2. Status moves to `pending_approval`
3. Approver reviews and approves or rejects
4. On approval → status = `active`, Celery jobs enabled
5. On rejection → status = `draft`, rejection note added

---

## 6. Acceptance criteria
- [ ] Campaign cannot activate without approval if requires_approval=True
- [ ] Channel mix selection validates against available integrations
- [ ] Campaign status transitions enforced (no skipping states)
- [ ] Owner receives notification when campaign is approved
- [ ] Paused campaign stops all Celery sequence tasks immediately
