# 01 — Django Backend Foundation

**Phase:** 1  
**Inputs from:** Phase 0 (governance charter, stack decisions, object language)  
**Outputs to:** Phase 2 (database + ABM control layer)

---

## 1. Phase purpose
Create the Django project skeleton, DRF API layer, PostgreSQL connection, Redis/Celery setup, environment configuration, authentication foundation, base app architecture, admin panel, and Docker Compose local setup.

## 2. Phase ownership boundary
This phase owns: Django project structure, DRF setup, PostgreSQL connection, Redis/Celery setup, environment config, authentication, API versioning, logging, Docker Compose.

This phase does NOT own: campaign business logic, channel execution, message generation, frontend UI.

---

## 3. Django apps to create (MVP)
| App | Responsibility |
|-----|----------------|
| `core` | Shared models, base classes, utilities |
| `campaigns` | Campaign object and lifecycle |
| `prospects` | Prospect and account models |
| `messages` | Message drafts, templates, approval state |
| `sequences` | Sequence state, touchpoints |
| `replies` | Inbound reply records |
| `handoffs` | Manual handoff objects |
| `governance` | DNC checks, suppression records, eligibility |
| `integrations` | Pipedrive, MS Graph, Periskope, LinkedHelper clients |
| `audit` | Audit log model and logging utilities |

---

## 4. Local Docker Compose services
| Service | Role |
|---------|------|
| `django-api` | Django backend + DRF API |
| `nextjs-web` | Next.js frontend |
| `postgres` | Primary database |
| `redis` | Celery broker + cache |
| `celery-worker` | Background job execution |
| `celery-beat` | Scheduled periodic jobs |

---

## 5. Setup commands
```bash
docker compose up
docker compose exec django-api python manage.py migrate
docker compose exec django-api python manage.py createsuperuser
cd frontend && npm run dev
```

---

## 6. Functional requirements
- Django project initialised with settings split (base/local/production)
- DRF installed with JWT authentication
- PostgreSQL configured as primary DB
- Redis configured as Celery broker
- Celery worker and Celery Beat configured
- Environment variables managed via `.env` file
- Django admin enabled with base superuser
- API versioned under `/api/v1/`
- Structured logging configured (JSON format for production)
- Health check endpoint at `/health/`

---

## 7. Governance requirements
- All API endpoints require authentication except `/health/`
- Role-based permissions: admin, campaign_manager, sales_owner, viewer
- No database write operations without an authenticated user context

---

## 8. Acceptance criteria
- [ ] `docker compose up` brings all services online
- [ ] Django admin accessible at `/admin/`
- [ ] `/api/v1/` returns 401 for unauthenticated requests
- [ ] Celery worker and beat start without errors
- [ ] PostgreSQL migrations run cleanly
- [ ] Health check returns 200
