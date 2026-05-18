# 02 — Database and ABM Control Layer

**Phase:** 2  
**Inputs from:** Phase 1 (Django project, DRF, Celery, auth)  
**Outputs to:** Phase 3 (Next.js control tower), Phase 5 (governance), Phase 6 (campaign engine)

---

## 1. Phase purpose
Define and implement all core platform data models, the prospect state machine, stop logic at data level, audit trail, and suppression record system.

## 2. Core models

### Campaign
```
id, name, campaign_type, target_industry, target_region,
target_persona, offer, channel_mix (JSON), sequence_length,
requires_approval (bool), owner (FK User), status,
created_at, updated_at
```
Status values: `draft`, `pending_approval`, `active`, `paused`, `completed`, `archived`

### Account
```
id, company_name, industry, region, website, pipedrive_org_id,
employee_count, revenue_range, created_at
```

### Prospect
```
id, first_name, last_name, email, phone, whatsapp_number,
designation, persona_tag, confidence_score,
account (FK Account), campaign (FK Campaign),
pipedrive_person_id, outreach_eligible (bool),
suppressed (bool), suppression_reason, created_at
```

### SequenceState
```
id, prospect (FK), campaign (FK), channel,
current_stage (M1/M2/M3/M4/replied/paused/dormant/stopped/completed),
next_action_at, last_touchpoint_at, stop_reason, created_at
```

### Touchpoint
```
id, sequence_state (FK), stage, channel, message (FK),
sent_at, delivery_status, opened_at, clicked_at
```

### Message
```
id, prospect (FK), campaign (FK), channel, stage,
subject (email only), body, compliance_status (pending/pass/block),
compliance_reason, approval_status (pending/approved/rejected/edited),
approved_by (FK User), approved_at, created_at
```

### Reply
```
id, prospect (FK), campaign (FK), channel, raw_content,
intent_category, confidence_score, stop_triggered (bool),
classified_at, created_at
```

### ManualHandoff
```
id, prospect (FK), campaign (FK), owner (FK User),
handoff_brief (text), suggested_response (text),
meeting_ready (bool), status (pending/in_progress/completed),
created_at
```

### AuditLog
```
id, actor_user (FK nullable), actor_system (str),
campaign (FK nullable), prospect (FK nullable),
channel, action, status, payload (JSON), failure_reason,
created_at
```

### SuppressionRecord
```
id, email, phone, whatsapp_number, reason,
suppressed_by (FK User nullable), is_permanent (bool),
expires_at (nullable), created_at
```

---

## 3. State machine — prospect sequence states

```
new → eligible → sequence_active → (M1 → M2 → M3 → M4)
                                         ↓ at any point
                                      replied / stopped / paused / dormant / completed
```

Stop is triggered from any state. Once stopped, the sequence cannot auto-restart.

---

## 4. Governance requirements at data layer
- No Touchpoint can be created if SequenceState is stopped or suppressed
- No Message with compliance_status=block can be approved
- No send can occur if approval_status != approved
- AuditLog must be written for every state transition

---

## 5. Acceptance criteria
- [ ] All models migrate cleanly
- [ ] State machine transitions enforced at model level
- [ ] Stop logic prevents any new Touchpoint after stop
- [ ] AuditLog writes on every significant action
- [ ] SuppressionRecord checked before any outreach eligibility is granted
