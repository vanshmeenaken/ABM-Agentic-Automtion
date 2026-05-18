# Agents API Documentation

**Free REST API for ABM Agents — For Team Integration**

All 5 agents now callable via HTTP endpoints. No agent code knowledge required.

---

## Quick Start

### 1. Start Django Server (locally)

```bash
cd backend
python manage.py runserver 8000
```

Server runs at: `http://localhost:8000`

### 2. Get JWT Token (required for API calls)

All endpoints require authentication. Get token:

```bash
curl -X POST http://localhost:8000/api/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

Response:
```json
{
  "access": "eyJhbGciOiJIUzI1NiIs...",
  "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

Save the `access` token. Include it in all API requests as:
```
Authorization: Bearer <access_token>
```

### 3. Call Any Agent Endpoint

```bash
curl -X POST http://localhost:8000/api/v1/agents/persona-classifier/classify/ \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "designation": "VP of Sales",
    "company_type": "SaaS",
    "industry": "EdTech"
  }'
```

---

## API Endpoints (5 agents)

### 1. Persona Classifier

**Endpoint:** `POST /api/v1/agents/persona-classifier/classify/`

**What it does:** Classifies prospect into buyer persona with confidence score.

**Request example:**
```json
{
  "designation": "VP of Sales",
  "company_type": "SaaS",
  "industry": "EdTech",
  "seniority_signals": ["manages 10+ people", "5+ years experience"]
}
```

**Response example:**
```json
{
  "persona_tag": "cxo_strategy",
  "confidence_score": 92,
  "classification_reason": "VP title indicates senior executive level...",
  "low_confidence_flag": false,
  "secondary_persona_tag": null
}
```

**Persona tags:** `cxo_strategy`, `marketing`, `operations`, `product_rd`, `investor`, `procurement`, `unknown`

---

### 2. Message Strategy

**Endpoint:** `POST /api/v1/agents/message-strategy/generate/`

**What it does:** Generates market-aware messaging strategy per persona (pain points, value props, tone, channel guidance).

**Request example:**
```json
{
  "campaign_name": "K-12 EdTech Sales 2026",
  "campaign_type": "Market Research",
  "offer": "Research on EdTech adoption trends in Indian schools",
  "target_industry": "K-12 Education",
  "target_personas": ["cxo_strategy", "operations"],
  "channel_mix": ["email", "whatsapp", "linkedin"]
}
```

**Response example:**
```json
{
  "campaign_name": "K-12 EdTech Sales 2026",
  "tone": "consultative",
  "key_themes": ["learning outcomes", "EdTech adoption", "competitive positioning"],
  "value_propositions": {
    "cxo_strategy": "Strategic framework to capture remote-learning market shift",
    "operations": "Practical implementation guide for EdTech integration"
  },
  "call_to_action": "Schedule 20-min call to discuss EdTech strategy",
  "persona_specific_messages": {
    "cxo_strategy": {
      "primary_angle": "Competitive positioning in EdTech shift",
      "pain_points": [
        "Competitors adopting EdTech faster",
        "Enrollment pressure from tech-forward schools"
      ],
      "value_prop": "Market insights to accelerate EdTech positioning"
    }
  },
  "channel_guidance": {
    "email": "Data-driven, lead with trend insight. Professional but warm.",
    "whatsapp": "Peer-to-peer tone. Share quick insight. Conversational.",
    "linkedin": "Thought leadership angle. Position as strategist."
  },
  "success_criteria": {
    "email_open_rate": "28-35%",
    "click_rate": "6-9%",
    "response_rate": "4-6%",
    "meeting_rate": "1-2%"
  }
}
```

---

### 3. Email Copy

**Endpoint:** `POST /api/v1/agents/email-copy/generate/`

**What it does:** Generates M1-M4 email copy based on messaging strategy.

**Request example:**
```json
{
  "strategy_brief": {
    "primary_angle": "Competitive positioning in EdTech shift",
    "pain_points": ["Competitors adopting faster", "Enrollment pressure"],
    "value_prop": "Market insights to accelerate positioning"
  },
  "persona_tag": "cxo_strategy",
  "prospect_name": "John Doe",
  "company_name": "Greenfield School District",
  "offer": "EdTech adoption research",
  "stage": "M1",
  "sender_name": "Sarah Chen",
  "prior_email_subjects": []
}
```

**Response example:**
```json
{
  "subject": "3 trends reshaping K-12 strategy in 2026",
  "body": "Hi John,\n\nNoticed Greenfield's focus on learning outcomes. As 85% of K-12 institutions accelerate EdTech adoption, schools focused on remote readiness are capturing enrollment growth...",
  "word_count": 165,
  "stage": "M1",
  "cta": "Schedule 20-min call to discuss your EdTech positioning"
}
```

**Stages:** M1 (cold), M2 (follow-up), M3 (proof), M4 (final)

**Constraints:**
- Subject < 60 characters
- No spam trigger words (free, urgent, guaranteed)
- Plain text only
- Must not repeat subject across M1-M4

---

### 4. WhatsApp Copy

**Endpoint:** `POST /api/v1/agents/whatsapp-copy/generate/`

**What it does:** Generates M1-M4 WhatsApp copy (mobile-first, conversational).

**Request example:**
```json
{
  "strategy_brief": {
    "primary_angle": "Competitive positioning in EdTech",
    "pain_points": ["Falling behind competitors", "Budget constraints"],
    "value_prop": "Market data to accelerate positioning"
  },
  "persona_tag": "cxo_strategy",
  "prospect_name": "Jane Smith",
  "company_name": "Lakewood Academy",
  "offer": "EdTech adoption research",
  "stage": "M1",
  "sender_name": "Sarah Chen"
}
```

**Response example:**
```json
{
  "body": "Hi Jane! 👋 Saw you're leading growth at Lakewood Academy. Quick insight: 85% of schools are adopting EdTech now — early movers capturing market share. We've mapped how top schools are positioning this competitively. Would love to share findings. Free 20-min call?\n\nReply STOP to opt out.",
  "word_count": 62,
  "stage": "M1",
  "opt_out_line": "Reply STOP to opt out",
  "cta": "Schedule 20-min call"
}
```

**Constraints:**
- Max 120-70 words (decreasing per stage)
- MANDATORY opt-out line ("Reply STOP to opt out")
- Conversational tone
- No media instructions

---

### 5. LinkedIn Copy

**Endpoint:** `POST /api/v1/agents/linkedin-copy/generate/`

**What it does:** Generates LinkedIn connection request + follow-up DM (2-part output).

**Request example:**
```json
{
  "strategy_brief": {
    "primary_angle": "Peer-level thought leadership",
    "pain_points": ["Competitive gap", "EdTech readiness"],
    "value_prop": "Strategic insights for positioning"
  },
  "persona_tag": "cxo_strategy",
  "prospect_name": "Alice Rodriguez",
  "company_name": "NextGen Schools",
  "offer": "EdTech competitive insights",
  "sender_name": "Sarah Chen"
}
```

**Response example:**
```json
{
  "connection_request": {
    "connection_request_note": "Hi Alice, noticed your EdTech leadership at NextGen. Would love to connect on strategy.",
    "character_count": 102
  },
  "follow_up_message": {
    "follow_up_message": "Hi Alice, thanks for connecting! We just completed research on how top schools position EdTech competitively. Would love to share findings over a quick call.",
    "word_count": 42,
    "optimal_delay_hours": 48,
    "cta": "Schedule call to discuss EdTech positioning"
  }
}
```

**Output parts:**
- **connection_request:** Send to prospect (max 300 chars, no sales pitch)
- **follow_up_message:** Send 48h+ after connection accepted (max 300 words)

**Note:** Platform does NOT send via LinkedIn. Copy is prepared for LinkedHelper setup.

---

## How to Integrate into Your System

### Option 1: Direct HTTP Requests (any language)

```python
# Python example
import requests

TOKEN = "your_access_token"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Call Persona Classifier
response = requests.post(
    "http://localhost:8000/api/v1/agents/persona-classifier/classify/",
    headers=HEADERS,
    json={
        "designation": "VP of Sales",
        "company_type": "SaaS"
    }
)

result = response.json()
print(f"Persona: {result['persona_tag']}")
print(f"Confidence: {result['confidence_score']}%")
```

### Option 2: cURL (from terminal)

```bash
curl -X POST http://localhost:8000/api/v1/agents/persona-classifier/classify/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "designation": "VP of Sales",
    "company_type": "SaaS",
    "industry": "EdTech"
  }'
```

### Option 3: Postman or Insomnia

1. Import collection from `backend/postman_collection.json` (create one)
2. Set base URL: `http://localhost:8000`
3. Set JWT token in Authorization
4. Test endpoints one by one

---

## Agent Call Flow (Recommended sequence)

```
1. Prospect Data Input
   ↓
2. Persona Classifier
   (designation → persona_tag + confidence)
   ↓
3. Message Strategy
   (persona_tag + campaign context → strategy_brief)
   ↓
4. Email/WhatsApp/LinkedIn Copy Agents
   (strategy_brief → email/WhatsApp/LinkedIn copy)
   ↓
5. Compliance Review (next: Agent 8)
   (copy → approved/rejected)
   ↓
6. Send via channel
```

---

## Error Handling

**400 Bad Request:** Invalid input data
```json
{
  "field_name": ["This field is required."]
}
```

**401 Unauthorized:** Missing or invalid token
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**503 Service Unavailable:** Agent module not found
```json
{
  "error": "Agent module not found: No module named 'persona_classifier_agent'"
}
```

**500 Server Error:** Agent execution failed
```json
{
  "error": "Agent execution failed: Claude CLI error..."
}
```

---

## Free Hosting Options (to share with teammates)

If you want teammates to access from anywhere (not just localhost):

### Option 1: Render (free tier, ~100 hours/month)
1. Push repo to GitHub
2. Connect to Render.com
3. Deploy Django app
4. Free PostgreSQL included
5. Share public URL with teammates

### Option 2: Railway (free tier, $5 credit/month)
Similar to Render, easy Django deployment

### Option 3: Heroku alternative (Fly.io, Replit)
Check current free tiers

### Option 4: Local + ngrok (free tunnel)
```bash
pip install ngrok
ngrok http 8000
# Gives public URL like: https://abcd-1234.ngrok.io
# Share with teammates
```

---

## Required Setup

### Locally (development)

```bash
# Install dependencies
pip install -r requirements.txt

# Create superuser for API access
python manage.py createsuperuser

# Run server
python manage.py runserver 8000

# Get token (use superuser credentials above)
curl -X POST http://localhost:8000/api/v1/auth/token/ \
  -d "username=admin&password=yourpassword"
```

### Requirements (already in requirements.txt)

- Django 4.2.13
- djangorestframework 3.15.1
- djangorestframework-simplejwt 5.3.1
- psycopg2-binary (for PostgreSQL)
- anthropic (for Claude API)
- All other deps

---

## API Documentation (Auto-generated)

DRF provides built-in docs:

**Browse endpoints:**
```
http://localhost:8000/api/v1/agents/persona-classifier/
http://localhost:8000/api/v1/agents/message-strategy/
http://localhost:8000/api/v1/agents/email-copy/
http://localhost:8000/api/v1/agents/whatsapp-copy/
http://localhost:8000/api/v1/agents/linkedin-copy/
```

**Each endpoint shows:**
- Input/output schema
- Example requests
- Test the API live in browser

---

## Support & Troubleshooting

### Claude CLI not found

Error: `Claude CLI not found. Install with: npm install -g @anthropic-ai/claude`

**Fix:**
```bash
npm install -g @anthropic-ai/claude
# Or use your Claude Code CLI path
```

### Database connection error

Error: `connection to server at "localhost"...failed`

**Fix:**
- Ensure PostgreSQL is running
- Check `.env` POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB
- Or run with SQLite in development (change DATABASES in settings.py)

### Token expired

Error: `Token is invalid or expired`

**Fix:** Get a new token using the /api/v1/auth/token/ endpoint

---

## Next Steps

- ✅ API endpoints live
- ⏳ Add Compliance Review Agent (Agent 8)
- ⏳ Add Reply Classifier Agent (Agent 9)
- ⏳ Add webhook receivers for inbound replies
- ⏳ Deploy to free hosting (Render, Railway, Fly.io)
- ⏳ Share with teammates via public URL

---

**Built with:** Django REST Framework (free, open-source)  
**Authentication:** JWT (free)  
**Docs:** DRF built-in (free)  
**Cost:** Zero $ 🎉
