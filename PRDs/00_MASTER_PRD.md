# 00 — Master PRD: ABM Revenue Automation Platform

## Document purpose
Central reference for the entire platform. All phase PRDs derive from this document.

---

## 1. Executive summary
The ABM Revenue Automation Platform is a campaign-based outbound revenue OS for Ken Research. It replaces disconnected n8n automations with a governed Django + Next.js platform that builds prospect databases, generates persona-specific outreach, orchestrates Email + WhatsApp + LinkedIn sequences, detects replies, stops automation instantly, hands warm prospects to sales, and tracks meetings to revenue.

---

## 2. Product vision
One controlled platform where Ken Research runs every outbound ABM campaign — from ICP to meeting — without automation running unchecked.

---

## 3. Business problem
- Outbound runs across disconnected tools (n8n, manual Pipedrive, spreadsheets)
- No single view of prospect status across channels
- No governance gate before messages are sent
- Automation continues after human replies or manual intervention
- No structured handoff from automation to sales

---

## 4. Platform objectives
1. Replace fragmented automation with a single campaign-based platform
2. Enforce governance before every send
3. Stop all automation the moment a prospect engages
4. Give sales a complete handoff brief when a prospect is ready
5. Track campaign performance end-to-end

---

## 5. Core product philosophy
- Workflows enforce
- Agents reason
- Governance approves
- Integrations execute
- Audit logs record
- Humans take over when needed

---

## 6. Campaign-based operating model
Every automation must belong to a campaign. A campaign defines: target audience, ICP, industry, region, persona, offer, channel mix, sequence rules, approval requirement, owner, and success metric.

**Campaign types:** Market Research, Competition Benchmarking, Survey, Consulting, Expert Network, Webinar, Report Sales, Account Reactivation

**Campaign hierarchy:**
```
Campaign
  → Accounts
  → Prospects
  → Messages
  → Sequences
  → Touchpoints
  → Replies
  → Handoffs
  → Meetings
  → Outcomes
```

---

## 7. Source of truth rule
| System | Owns |
|--------|------|
| Pipedrive | CRM state, lead status, person/org records, owner, activities, DNC, meeting status |
| Django platform | Operational state, sequence state, audit logs, message history, agent runs |

Django must never become a competing CRM.

---

## 8. Architecture overview
```
Next.js Control Tower (frontend)
        ↓
Django REST API (business logic + governance)
        ↓
ABM Core Services (campaign, prospect, message, reply intelligence)
        ↓
Celery Workers (scheduling, webhooks, sync jobs)
        ↓
Integration Layer (Pipedrive, MS Graph, Periskope, LinkedHelper)
```

---

## 9. MVP scope
1. Django backend + Next.js frontend skeleton
2. PostgreSQL database + core models
3. Celery background jobs
4. Pipedrive integration
5. Microsoft Graph email (M1–M4)
6. Governance checks
7. Manual handoff
8. Basic dashboard

MVP excludes: full AI agent library, WhatsApp sequence, LinkedHelper ingestion, full analytics, full enrichment, full meeting automation.

---

## 10. Master acceptance criteria
- Campaign can be created, approved, paused, completed, archived
- Prospect can be imported, deduped, assigned, and marked eligible or blocked
- Generated message can be reviewed, approved, rejected, or edited before send
- Governance blocks sends for DNC, reply, manual intervention, duplicate, missing approval
- Email M1–M4 schedulable and trackable via Microsoft Graph
- WhatsApp M1–M4 schedulable and trackable via Periskope
- Any reply on any channel stops all automation for that contact
- Every action is audit logged
- Positive reply creates handoff and meeting booking readiness
- Dashboard shows campaign, channel, owner, reply, meeting, handoff performance

---

## 11. Key risks
| Risk | Mitigation |
|------|------------|
| Agents before workflow logic | Build deterministic workflows first |
| Platform DB vs Pipedrive conflict | Explicit sync rules; Django owns ops state only |
| Automation continues after reply | Cross-channel stop logic is mandatory |
| Overbuilding too early | MVP first, validate before expansion |
| Poor data quality | Dedupe + confidence scoring before scale |
| Unapproved messages | Compliance review + approval check before every send |
