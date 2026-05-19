# Ken ABM Platform — Django Backend Setup Guide

Complete end-to-end Django implementation for the Campaign Planner Agent. This guide covers setup, testing, and verification of the backend system.

---

## Quick Start

### Prerequisites
- Docker & Docker Compose installed
- ANTHROPIC_API_KEY environment variable set (for agent testing)

### Setup (5 minutes)

```bash
# 1. Initialize environment
cp .env.example .env

# 2. Edit .env and add your API key
# ANTHROPIC_API_KEY=your-actual-key-here

# 3. Build and start services
make init

# This will:
# - Build Docker images
# - Start 5 services (django-api, postgres, redis, celery-worker, celery-beat)
# - Apply migrations
# - Create superuser (prompts for username/password)

# 4. Check system is ready
make health

# 5. Open browser
# Admin: http://localhost:8000/admin/
# API: http://localhost:8000/api/v1/
```

---

## Project Structure

```
backend/
├── config/                 # Django configuration
│   ├── settings/
│   │   ├── base.py        # Shared settings
│   │   ├── local.py       # Development settings
│   │   └── production.py  # Production settings
│   ├── celery.py          # Celery app configuration
│   ├── urls.py            # Root URL routing
│   └── wsgi.py            # WSGI app
├── apps/                   # Django applications
│   ├── core/              # Base models, permissions, exceptions
│   ├── audit/             # Audit logging
│   ├── campaigns/         # Campaign management (main app)
│   ├── prospects/         # Prospects (stub)
│   ├── messages/          # Messages (stub)
│   ├── sequences/         # Sequences (stub)
│   ├── replies/           # Replies (stub)
│   ├── handoffs/          # Handoffs (stub)
│   ├── governance/        # Governance (stub)
│   └── integrations/      # Integrations (stub)
├── agents/                # Moved from root — Campaign Planner Agent
│   ├── campaign_planner_agent.py
│   ├── prospect_research_agent.py
│   ├── data_quality_agent.py
│   ├── persona_classifier_agent.py
│   ├── schemas.py
│   ├── registry/          # Agent JSON configurations
│   │   ├── campaign_planner.json
│   │   ├── prospect_research.json
│   │   ├── data_quality.json
│   │   └── persona_classifier.json
│   └── __init__.py
├── requirements.txt       # Python dependencies
├── manage.py              # Django CLI
├── Dockerfile             # Container image
└── .env                   # Environment variables (copy from .env.example)
```

---

## Key Features Implemented

### 1. Campaign Model with State Machine
- **Status transitions**: draft → pending_approval → active → paused → completed → archived
- **Workflow**: Create, approve, reject, pause, resume
- **Audit logging**: Every action logged to AuditLog
- **Agent integration**: Campaign Planner Agent output stored in icp_definition, persona_map, channel_plan

### 2. WF-001 Campaign Creation Workflow
```
1. User submits campaign creation request
2. Campaign Planner Agent generates ICP, personas, channel plan
3. Campaign saved as DRAFT with agent output
4. Route to approval (if requires_approval=true)
   - PENDING_APPROVAL status
   - Awaits approver action
5. Approver approves → ACTIVE (triggers sequence generation)
   OR rejects → back to DRAFT (with rejection note)
6. Owner can pause/resume ACTIVE campaigns
7. Completed campaigns → ARCHIVED
```

### 3. Role-Based Permissions
- **campaign_manager**: Create, edit, pause, resume campaigns
- **approver**: Approve/reject campaigns
- **viewer**: Read-only access
- **admin**: All access

### 4. Audit Logging
Every action is logged:
- User who performed action
- Campaign affected
- Action type (campaign_created, campaign_approved, etc.)
- Status (success/failure)
- Failure reason (if applicable)
- Payload (additional context)

### 5. API Endpoints

#### Campaign Management
```
GET    /api/v1/campaigns/                  # List campaigns
POST   /api/v1/campaigns/                  # Create campaign
GET    /api/v1/campaigns/{id}/             # Get campaign detail
PATCH  /api/v1/campaigns/{id}/             # Update campaign
DELETE /api/v1/campaigns/{id}/             # Delete campaign (soft)
```

#### Campaign Workflow Actions
```
POST   /api/v1/campaigns/{id}/approve/     # Approve pending campaign
POST   /api/v1/campaigns/{id}/reject/      # Reject campaign
POST   /api/v1/campaigns/{id}/pause/       # Pause active campaign
POST   /api/v1/campaigns/{id}/resume/      # Resume paused campaign
```

#### Authentication
```
POST   /api/v1/auth/token/                 # Get JWT token
POST   /api/v1/auth/token/refresh/         # Refresh token
```

#### System
```
GET    /health/                            # Health check
GET    /admin/                             # Django admin
```

---

## Testing the System

### 1. Run All Tests
```bash
make test
```

### 2. Run Specific Test Suite
```bash
# Campaign model tests
make test-campaigns

# Audit logging tests
make test-audit

# With verbose output
make test-verbose

# With coverage report
make test-coverage
```

### 3. Test Campaign Creation Workflow (Manual)

#### Step 1: Get JWT Token
```bash
curl -X POST http://localhost:8000/api/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "your-password"
  }'

# Returns: {"access": "token...", "refresh": "token..."}
# Use access token in Authorization header
```

#### Step 2: Create Campaign
```bash
curl -X POST http://localhost:8000/api/v1/campaigns/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_name": "India EV Ecosystem Survey",
    "target_industry": "Automotive",
    "target_region": "India",
    "offer": "Survey participation + sector report",
    "campaign_type": "Survey",
    "preferred_channels": ["email", "linkedin"],
    "notes": "Focus on EV component suppliers",
    "success_metric": "50% response rate",
    "requires_approval": true
  }'

# Returns: Campaign object with id, status=pending_approval
```

#### Step 3: Get Campaign Detail
```bash
curl http://localhost:8000/api/v1/campaigns/{campaign_id}/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# Returns: Full campaign with agent output (icp_definition, persona_map, etc.)
```

#### Step 4: Approve Campaign (as approver user)
```bash
curl -X POST http://localhost:8000/api/v1/campaigns/{campaign_id}/approve/ \
  -H "Authorization: Bearer APPROVER_TOKEN" \
  -H "Content-Type: application/json"

# Returns: Campaign with status=active
```

#### Step 5: Pause Campaign
```bash
curl -X POST http://localhost:8000/api/v1/campaigns/{campaign_id}/pause/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"

# Returns: Campaign with status=paused
```

---

## Makefile Commands

```bash
# Infrastructure
make build              # Build Docker images
make up                 # Start services
make down               # Stop services
make logs               # Follow logs

# Setup
make migrate            # Apply migrations
make superuser          # Create admin user
make init               # Full initialization (build + up + migrate + superuser)

# Development
make shell              # Django shell
make test               # Run tests
make test-verbose       # Tests with verbose output
make health             # Check system health

# Cleanup
make clean              # Stop containers and remove volumes

# Quick workflows
make ready              # Start and prepare for testing
make dev                # Start development environment
```

---

## Environment Configuration

### Local Development (.env)
```
DJANGO_SETTINGS_MODULE=config.settings.local
SECRET_KEY=django-insecure-dev-key
DEBUG=True

POSTGRES_DB=ken_abm
POSTGRES_USER=ken_abm_user
POSTGRES_PASSWORD=localpassword
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

REDIS_URL=redis://redis:6379/0
ANTHROPIC_API_KEY=your-key-here
CORS_ALLOW_ALL_ORIGINS=True
```

### Production (.env)
```
DJANGO_SETTINGS_MODULE=config.settings.production
SECRET_KEY=your-strong-secret-key-here
DEBUG=False

POSTGRES_DB=ken_abm_prod
POSTGRES_USER=ken_abm_prod_user
POSTGRES_PASSWORD=strong-password-here
POSTGRES_HOST=your-db-host
POSTGRES_PORT=5432

REDIS_URL=redis://your-redis-host:6379/0
ANTHROPIC_API_KEY=your-key-here
ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://api.yourdomain.com
```

---

## Database Schema

### Campaign Model
```sql
campaigns_campaign (
  id UUID PRIMARY KEY,
  name VARCHAR(255),
  campaign_type VARCHAR(50),
  target_industry VARCHAR(100),
  target_region VARCHAR(100),
  target_persona VARCHAR(100),
  offer TEXT,
  channel_mix JSONB,
  sequence_length INTEGER,
  success_metric VARCHAR(100),
  requires_approval BOOLEAN,
  status VARCHAR(30),
  owner_id BIGINT (FK: auth_user),
  approved_by_id BIGINT (FK: auth_user, nullable),
  icp_definition JSONB,
  persona_map JSONB,
  channel_plan JSONB,
  confidence_notes TEXT,
  agent_run_id UUID,
  approved_at TIMESTAMP,
  rejection_note TEXT,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
```

### AuditLog Model
```sql
audit_auditlog (
  id BIGINT PRIMARY KEY,
  action VARCHAR(100),
  status VARCHAR(20),
  actor_user_id BIGINT (FK: auth_user, nullable),
  actor_system VARCHAR(100),
  campaign_id UUID (FK: campaigns_campaign, nullable),
  prospect_id UUID (FK: prospects_prospect, nullable),
  channel VARCHAR(50),
  payload JSONB,
  failure_reason TEXT,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
```

---

## Celery Tasks

### Available Tasks
1. **run_campaign_planner_task** — Async agent execution (placeholder)
2. **enable_campaign_sequences** — Called when campaign activated (placeholder for Phase 12)
3. **disable_campaign_sequences** — Called when campaign paused
4. **check_pending_campaigns** — Periodic task (every 4 hours via Beat)

### View Running Tasks
```bash
# Connect to Celery worker
docker compose exec celery-worker celery -A config inspect active

# View registered tasks
docker compose exec celery-worker celery -A config inspect registered
```

---

## Admin Interface

Access at http://localhost:8000/admin/

### Available Models
- **Campaigns** — Full campaign management with status filtering
  - Status color-coded (draft=orange, active=green, paused=red, etc.)
  - Bulk actions: mark as active, mark as paused
  - Readonly fields for agent output

- **Audit Logs** — Complete action history
  - Filter by action, status, actor, campaign
  - Search by action name, username, error messages
  - JSON payload inspection

- **Users & Groups** — User management with role-based groups
  - Create groups: campaign_manager, approver, viewer
  - Assign users to groups for permissions

---

## Troubleshooting

### "Address already in use" Error
```bash
# Kill process using port 8000
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Or just use Docker Compose
make down
make up
```

### Database Connection Error
```bash
# Check postgres is healthy
make health-db

# Recreate database
make clean
make init
```

### Import Errors for Agents
```bash
# Verify agents are in backend/agents/
ls -la backend/agents/

# Restart Django container
make restart-api
```

### Agent API Failures
```bash
# Check ANTHROPIC_API_KEY is set
grep ANTHROPIC_API_KEY .env

# View logs
make logs-api

# Manually test agent
docker compose exec django-api python manage.py shell
# >>> from agents.campaign_planner_agent import run_campaign_planner
# >>> run_campaign_planner(...)
```

---

## Next Steps

### Phase 02: Prospect Research Agent
- Implement ProspectResearchAgent in Django
- Create Prospect model
- Build prospect research API endpoint
- Integrate with Campaign model (FK relationship)

### Phase 03: Data Quality Agent
- Implement DataQualityAgent
- Create data cleaning pipeline
- Add duplicate detection
- Scoring and flagging system

### Phase 12: Sequence Orchestrator
- Implement Sequence model
- Build sequence generation engine
- Celery-based scheduler for touch timing
- Message queue management

---

## Code Quality

### Format Code
```bash
make format  # Black + isort
```

### Lint Code
```bash
make lint    # flake8
```

### Run Tests with Coverage
```bash
make test-coverage
```

---

## API Documentation

For full API documentation, see the README.md at project root.

---

## Support

For issues or questions:
1. Check logs: `make logs`
2. Check health: `make health`
3. Run tests: `make test`
4. Review audit logs in admin interface

---

## License

Part of Ken ABM Platform (Internal Use)
