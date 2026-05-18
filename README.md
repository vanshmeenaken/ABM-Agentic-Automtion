# Ken ABM Revenue Automation Platform — Base Engine

## What this is
This folder is the base engine for the **Ken ABM Revenue Automation Platform** — a campaign-based outbound revenue operating system built on Django + Next.js + Celery + PostgreSQL.

It contains the PRD library, agent definitions, skill packs, and workflow blueprints that the platform runs on. Every file here is a buildable starting point — not a final spec — designed to be expanded at implementation time.

---

## Core operating principle
> Agents reason. Workflows enforce. Governance approves. Integrations execute. Audit logs record. Pipedrive is the CRM source of truth.

---

## Folder structure

```
ken-abm-platform/
├── README.md                        ← You are here
│
├── PRDs/                            ← 17 phase PRDs (master + 16 phases)
│   ├── 00_MASTER_PRD.md
│   ├── 00_PRD_PROJECT_CONTINUITY_CHARTER.md
│   ├── 01_PRD_DJANGO_BACKEND_FOUNDATION.md
│   ├── 02_PRD_DATABASE_AND_ABM_CONTROL_LAYER.md
│   ├── 03_PRD_NEXTJS_CONTROL_TOWER.md
│   ├── 04_PRD_PIPEDRIVE_INTEGRATION.md
│   ├── 05_PRD_GOVERNANCE_AND_STOP_AUTOMATION.md
│   ├── 06_PRD_CAMPAIGN_ENGINE.md
│   ├── 07_PRD_PROSPECT_DATABASE_BUILDER.md
│   ├── 08_PRD_MESSAGE_INTELLIGENCE_LAYER.md
│   ├── 09_PRD_EMAIL_OUTREACH_MICROSOFT_GRAPH.md
│   ├── 10_PRD_WHATSAPP_OUTREACH_PERISKOPE.md
│   ├── 11_PRD_LINKEDHELPER_EVENT_INGESTION.md
│   ├── 12_PRD_SEQUENCE_ORCHESTRATOR.md
│   ├── 13_PRD_REPLY_INTELLIGENCE_AND_MANUAL_HANDOFF.md
│   ├── 14_PRD_MEETING_BOOKING_AND_ANALYTICS.md
│   └── 15_PRD_QA_EVALS_SECURITY_DEPLOYMENT.md
│
├── agents/                          ← 10 MVP agent definitions
│   ├── 01_campaign_planner_agent.md
│   ├── 02_prospect_research_agent.md
│   ├── 03_data_quality_agent.md
│   ├── 04_persona_classifier_agent.md
│   ├── 05_message_strategy_agent.md
│   ├── 06_email_copy_agent.md
│   ├── 07_whatsapp_copy_agent.md
│   ├── 08_compliance_review_agent.md
│   ├── 09_reply_classifier_agent.md
│   └── 10_sales_handoff_agent.md
│
├── skills/                          ← 12 MVP skill packs
│   ├── 01_campaign_planning_skill.md
│   ├── 02_icp_definition_skill.md
│   ├── 03_b2b_persona_classification_skill.md
│   ├── 04_prospect_data_cleaning_skill.md
│   ├── 05_pipedrive_hygiene_skill.md
│   ├── 06_email_outreach_copy_skill.md
│   ├── 07_whatsapp_outreach_copy_skill.md
│   ├── 08_linkedin_drafting_skill.md
│   ├── 09_message_compliance_skill.md
│   ├── 10_reply_classification_skill.md
│   ├── 11_manual_handoff_skill.md
│   └── 12_meeting_booking_skill.md
│
└── workflows/                       ← 7 MVP workflow blueprints
    ├── 01_campaign_creation_workflow.md
    ├── 02_prospect_intake_dedupe_workflow.md
    ├── 03_message_generation_approval_workflow.md
    ├── 04_email_sequence_workflow.md
    ├── 05_whatsapp_sequence_workflow.md
    ├── 06_reply_detection_stop_automation_workflow.md
    └── 07_sales_handoff_meeting_booking_workflow.md
```

---

## Build order

Follow this sequence. Each phase unlocks the next.

| Order | Phase | PRD file |
|-------|-------|----------|
| 0 | Project continuity charter | 00_PRD_PROJECT_CONTINUITY_CHARTER.md |
| 1 | Django backend foundation | 01_PRD_DJANGO_BACKEND_FOUNDATION.md |
| 2 | Database + ABM control layer | 02_PRD_DATABASE_AND_ABM_CONTROL_LAYER.md |
| 3 | Next.js control tower | 03_PRD_NEXTJS_CONTROL_TOWER.md |
| 4 | Pipedrive integration | 04_PRD_PIPEDRIVE_INTEGRATION.md |
| 5 | Governance + stop automation | 05_PRD_GOVERNANCE_AND_STOP_AUTOMATION.md |
| 6 | Campaign engine | 06_PRD_CAMPAIGN_ENGINE.md |
| 7 | Prospect database builder | 07_PRD_PROSPECT_DATABASE_BUILDER.md |
| 8 | Message intelligence layer | 08_PRD_MESSAGE_INTELLIGENCE_LAYER.md |
| 9 | Email via Microsoft Graph | 09_PRD_EMAIL_OUTREACH_MICROSOFT_GRAPH.md |
| 10 | WhatsApp via Periskope | 10_PRD_WHATSAPP_OUTREACH_PERISKOPE.md |
| 11 | LinkedHelper event ingestion | 11_PRD_LINKEDHELPER_EVENT_INGESTION.md |
| 12 | Sequence orchestrator | 12_PRD_SEQUENCE_ORCHESTRATOR.md |
| 13 | Reply intelligence + handoff | 13_PRD_REPLY_INTELLIGENCE_AND_MANUAL_HANDOFF.md |
| 14 | Meeting booking + analytics | 14_PRD_MEETING_BOOKING_AND_ANALYTICS.md |
| 15 | QA, evals, security, deployment | 15_PRD_QA_EVALS_SECURITY_DEPLOYMENT.md |

---

## Master platform objects

All agents, skills, workflows, and PRDs use these object names consistently. Never rename them.

| Object | Description |
|--------|-------------|
| Campaign | The parent container for every outbound motion |
| Account | A target company or organisation |
| Prospect | An individual person targeted for outreach |
| Persona | Buyer role classification (CXO, Marketing, Ops, etc.) |
| Message | A single outreach message (M1–M4) |
| Sequence | The M1–M4 chain for a prospect |
| Touchpoint | A single send event within a sequence |
| Reply | An inbound response on any channel |
| Manual Handoff | A sales-ready transfer from automation to human |
| Meeting | A booked or pending sales meeting |
| Audit Log | A timestamped record of every system action |
| Integration Event | An inbound event from Pipedrive, MS Graph, Periskope, or LinkedHelper |
| Agent Run | A logged execution of any agent |
| Suppression Record | A permanent or temporary DNC record |

---

## Stop automation — the cross-cutting invariant

Any of the following events stops all automation for a prospect across all channels immediately:

- Reply received on any channel (Email, WhatsApp, LinkedIn)
- Manual activity logged in Pipedrive by a sales owner
- DNC marked (permanent — never restarts)
- Meeting booked
- Owner override triggered

This rule is enforced at the workflow level, not the agent level. No agent can bypass it.

---

## Tech stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js, React, Tailwind CSS, shadcn/ui |
| Backend | Python, Django, Django REST Framework |
| Background jobs | Celery + Redis/RabbitMQ + Celery Beat |
| Database | PostgreSQL |
| CRM | Pipedrive (source of truth) |
| Email | Microsoft Graph / Outlook |
| WhatsApp | Periskope API |
| LinkedIn events | LinkedHelper webhooks |
| Local runtime | Docker Compose + VS Code |
