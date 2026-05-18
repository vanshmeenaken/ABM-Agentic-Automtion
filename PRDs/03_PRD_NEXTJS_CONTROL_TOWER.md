# 03 — Next.js Control Tower

**Phase:** 3  
**Inputs from:** Phase 2 (data models + API contracts)  
**Outputs to:** All subsequent phases (UI shell used by all features)

---

## 1. Phase purpose
Build the Next.js frontend shell: navigation, all page routes, dashboard, campaign manager, prospect database view, message approval queue, sequence monitor, reply inbox, manual handoff queue, meeting panel, analytics, and settings.

## 2. Pages and modules

| Page | Route | Purpose |
|------|-------|---------|
| Dashboard | `/` | Campaign metrics, reply counts, handoffs pending, meetings booked |
| Campaigns | `/campaigns` | Create, view, filter, and manage campaigns |
| Campaign detail | `/campaigns/[id]` | Status, prospects, sequence config, messages |
| Prospects | `/prospects` | Import, filter, view all prospect records |
| Message approval | `/messages/approval` | Review, edit, approve, or reject generated messages |
| Sequence monitor | `/sequences` | Per-prospect M1–M4 stage, status, next action |
| Reply inbox | `/replies` | Unified inbox across Email, WhatsApp, LinkedIn |
| Handoffs | `/handoffs` | Sales owner queue with brief + suggested response |
| Meetings | `/meetings` | Book meetings, view call briefs |
| Analytics | `/analytics` | Campaign, channel, owner, conversion metrics |
| Settings | `/settings` | Integration config, sender limits, templates, DNC rules |

---

## 3. Design system
- Tailwind CSS utility classes
- shadcn/ui component system
- All data fetched via `/api/v1/` endpoints
- Auth via JWT stored in httpOnly cookie

---

## 4. Acceptance criteria
- [ ] All page routes accessible after auth
- [ ] Dashboard loads campaign and reply summary from API
- [ ] Message approval queue shows pending messages with approve/reject actions
- [ ] Sequence monitor shows correct stage per prospect
- [ ] Reply inbox shows unified replies with stop status indicator
- [ ] Settings page saves integration config
