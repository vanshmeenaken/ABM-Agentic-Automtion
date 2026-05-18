# 00 — Project Continuity, Scope Boundary, and Build Governance Charter

**Phase:** 0  
**Purpose:** Define continuity, scope boundaries, non-repetition rules, platform philosophy, build order, and acceptance criteria for all future PRDs.

---

## 1. Phase 0 purpose
Phase 0 is the continuity layer for the PRD library. It prevents the platform from becoming a scattered collection of disconnected automations and PRDs.

Phase 0 defines: platform vision, system boundaries, phase boundaries, technology stack, source-of-truth rule, campaign-based operating model, agentic model, governance principles, non-repetition rule, build order, and readiness criteria.

Phase 0 does NOT define: detailed database schema, detailed API contracts, detailed UI screens, detailed message templates, or detailed channel execution logic.

---

## 2. Existing reference context
**Existing WhatsApp + Pipedrive logic:** The existing integration template defines Pipedrive field usage (name, designation, company, report title, requirement, country) and persona logic for Marketing, Operations, Business/CXO, Investor, and Product/R&D. The platform must upgrade this — not reinvent it.

**Existing email workflow logic:** The existing n8n workflow demonstrates: scheduled trigger → Pipedrive lead fetch → label filtering → field cleaning → AI email generation → Outlook send → Google Sheets logging. The platform must convert this pattern into Django + Celery — not ignore it.

---

## 3. Core product philosophy
```
Workflows enforce.
Agents reason.
Governance approves.
Integrations execute.
Audit logs record.
Humans take over when needed.
```

**Anti-pattern (forbidden):**
Agent decides → agent sends → agent updates CRM → agent continues sequence

**Required pattern:**
Workflow checks state → agent generates/classifies → governance validates → approved integration executes → audit log records → human handoff when required

---

## 4. Source of truth rule
Pipedrive is the master CRM source of truth. Django owns operational/automation/audit state only. Django must never become a hidden competing CRM.

---

## 5. Technology stack
| Layer | Technology |
|-------|------------|
| Frontend | Next.js, React, Tailwind CSS, shadcn/ui |
| Backend | Python, Django, Django REST Framework |
| Background jobs | Celery + Redis/RabbitMQ + Celery Beat |
| Database | PostgreSQL |
| Local runtime | Docker Compose + VS Code |
| Future hosting | Azure / AWS / Railway / Render / Vercel (TBD) |

---

## 6. Master platform objects
Campaign, Account, Prospect, Persona, Message, Sequence, Touchpoint, Reply, Manual Handoff, Meeting, Audit Log, Integration Event, Agent Run, Skill, Workflow, User, Owner, Suppression Record.

These object names must not be renamed across any PRD, agent, or workflow file.

---

## 7. Non-repetition rule
Each PRD owns one part of the system and must not repeat deep detail from other PRDs.

Phase 0 owns: vision, scope, stack decision, system philosophy, object language, phase boundaries, build order, source-of-truth rule, non-repetition rule, continuity rule, high-level governance principles.

---

## 8. Phase boundary map (summary)
| Phase | Owns | Does not own |
|-------|------|--------------|
| 1 | Django project structure, DRF, Celery, auth, admin | Campaign logic, UI, channel execution |
| 2 | Core data model, state machine, audit log, suppression | UI, channel clients, enrichment |
| 3 | Next.js frontend shell, all UI pages | Backend logic, Celery |
| 4 | Pipedrive API integration, all CRM sync | Email/WA sending, message generation |
| 5 | Governance checks, all stop rules | Channel send implementation |
| 6 | Campaign object, lifecycle, approval, ownership | Channel execution, enrichment, analytics |
| 7 | Prospect import, enrichment, dedupe, persona classify | Message generation, reply classification |
| 8 | Message generation, all copy, compliance, approval | Actual sending, scheduling |
| 9 | MS Graph email send, tracking, reply detection | WhatsApp, message strategy |
| 10 | Periskope WhatsApp send, tracking, opt-out | Email, LinkedHelper |
| 11 | LinkedHelper webhook ingestion, event normalisation | Email/WA execution |
| 12 | Celery sequence timing, retries, dormant state | Channel clients, copywriting |
| 13 | Reply classification, handoff brief, owner notify | Meeting booking, analytics |
| 14 | Meeting booking, analytics, performance reporting | Core state machine, base Pipedrive sync |
| 15 | QA evals, security, deployment, monitoring | Business feature logic (defined in prior phases) |

---

## 9. Human-in-the-loop rule
Human approval required for: launching a campaign, approving the first message set, sending to high-value prospects, overriding governance blocks, resuming paused sequences, handling replies, marking DNC reversal, booking important meetings.

---

## 10. Stop automation principle (cross-phase invariant)
If a prospect replies on any channel → stop all automation across all channels.
If a human manually intervenes → stop.
If DNC is marked → stop permanently.
If meeting is booked → stop sequence.
If prospect becomes active sales conversation → stop.

---

## 11. Required format for all phase PRDs
Every phase PRD must contain these 20 sections:
1. Phase purpose
2. Phase ownership boundary
3. What this phase does not cover
4. Inputs from previous phase
5. Outputs to next phase
6. Users / actors
7. Functional requirements
8. Non-functional requirements
9. Data requirements
10. Workflow requirements
11. Agent requirements (if applicable)
12. Integration requirements (if applicable)
13. UI requirements (if applicable)
14. API requirements (if applicable)
15. Governance requirements
16. Error handling
17. Audit logging
18. Test cases
19. Acceptance criteria
20. Handoff notes

---

## 12. Phase 0 acceptance criteria
- [ ] Platform vision is clear
- [ ] Technology stack is finalised
- [ ] Pipedrive source-of-truth rule accepted
- [ ] Phase boundary map approved
- [ ] Non-repetition rule approved
- [ ] Master object language approved
- [ ] Build order approved
- [ ] MVP scope approved
- [ ] Full scope approved
- [ ] Future PRD template approved
