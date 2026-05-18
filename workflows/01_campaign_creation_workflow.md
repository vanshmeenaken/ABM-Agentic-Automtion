# Workflow: Campaign Creation

**Workflow ID:** WF-001  
**Agents involved:** Campaign Planner Agent  
**Skills involved:** Campaign Planning Skill, ICP Definition Skill  
**Phase:** Phase 6 (Campaign Engine)

---

## Purpose
Creates a structured campaign draft from a user request, runs the Campaign Planner Agent, and routes the output through the approval gate before the campaign can activate.

---

## Trigger
User submits a new campaign form in the control tower with at minimum: name, type, industry, region, offer.

---

## Pre-conditions
- User is authenticated with `campaign_manager` role or higher
- At least one channel integration is configured in settings
- At least one sender account is configured

---

## Workflow steps

```
Step 1: Validate inputs
  → Check required fields present
  → Check campaign type is valid
  → If validation fails → return error to UI, halt

Step 2: Run Campaign Planner Agent
  → Input: campaign form data
  → Output: campaign draft + ICP + persona map + channel plan
  → Log Agent Run to AuditLog

Step 3: Save campaign draft to DB
  → Status = draft
  → Link ICP definition to campaign record

Step 4: Route to approval
  → If requires_approval = True → status = pending_approval → notify approver
  → If requires_approval = False → status = active → enable Celery scheduling

Step 5: Notify campaign owner
  → Push notification in control tower
  → Log AuditLog entry: campaign_created
```

---

## Governance gates
- No campaign activates without a valid ICP definition
- No campaign activates without at least one confirmed persona tag
- No campaign activates without at least one configured channel
- If requires_approval = True → no campaign activates without explicit human approval

---

## Stop path
- If Campaign Planner Agent fails → save partial draft, flag for human review, do not activate

---

## Failure path
- Validation failure → return error, halt, no DB write
- Agent failure → save draft with agent_run_id, alert admin

---

## Audit log events
| Event | Trigger |
|-------|---------|
| `campaign_created` | Draft saved to DB |
| `campaign_pending_approval` | Sent to approver |
| `campaign_approved` | Approved by user |
| `campaign_rejected` | Rejected by user |
| `campaign_activated` | Status = active |

---

## Acceptance criteria
- [ ] Invalid inputs return error before agent runs
- [ ] Campaign draft created with all required fields
- [ ] requires_approval = True prevents activation without human step
- [ ] AuditLog entry written at each state change
