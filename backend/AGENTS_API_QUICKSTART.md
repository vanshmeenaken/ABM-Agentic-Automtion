# Agents API — Quick Start (5 minutes)

Get the API running locally + share with teammates.

---

## Step 1: Setup Django Backend (2 min)

```bash
# Navigate to backend
cd backend

# Install dependencies (if not done)
pip install -r requirements.txt

# Create superuser (for API auth)
python manage.py createsuperuser
# Follow prompts (username: admin, password: anything)

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver 8000
```

**Server running at:** `http://localhost:8000`

---

## Step 2: Get JWT Token (1 min)

API requires authentication. Get token:

```bash
curl -X POST http://localhost:8000/api/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "your_superuser_password"
  }'
```

**Response:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIs...",
  "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Copy the `access` value** — use in all API calls as:
```
Authorization: Bearer <access_token>
```

---

## Step 3: Test One Endpoint (2 min)

```bash
TOKEN="your_access_token_from_step_2"

curl -X POST http://localhost:8000/api/v1/agents/persona-classifier/classify/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "designation": "VP of Sales",
    "company_type": "SaaS",
    "industry": "EdTech"
  }'
```

**Should return:**
```json
{
  "persona_tag": "cxo_strategy",
  "confidence_score": 92,
  "classification_reason": "...",
  "low_confidence_flag": false
}
```

✅ **API working!**

---

## Share with Teammates

### Option A: Postman (easiest)

1. Download Postman (free): https://www.postman.com/downloads/
2. Import collection: `backend/postman_agents_collection.json`
3. Set `BASE_URL` variable to `http://localhost:8000`
4. Set `JWT_TOKEN` variable to your token
5. Click "Send" on any request

### Option B: Python

```python
import requests

TOKEN = "your_access_token"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Persona Classifier
response = requests.post(
    "http://localhost:8000/api/v1/agents/persona-classifier/classify/",
    headers=HEADERS,
    json={"designation": "VP of Sales", "company_type": "SaaS"}
)
print(response.json())

# Message Strategy
response = requests.post(
    "http://localhost:8000/api/v1/agents/message-strategy/generate/",
    headers=HEADERS,
    json={
        "campaign_name": "K-12 EdTech",
        "campaign_type": "Market Research",
        "offer": "Research study",
        "target_industry": "K-12 Education",
        "target_personas": ["cxo_strategy"],
        "channel_mix": ["email"]
    }
)
print(response.json())
```

### Option C: cURL (terminal)

All examples in `API_AGENTS_README.md`

---

## Endpoints (copy/paste ready)

| Agent | Method | Endpoint |
|-------|--------|----------|
| Persona Classifier | POST | `/api/v1/agents/persona-classifier/classify/` |
| Message Strategy | POST | `/api/v1/agents/message-strategy/generate/` |
| Email Copy | POST | `/api/v1/agents/email-copy/generate/` |
| WhatsApp Copy | POST | `/api/v1/agents/whatsapp-copy/generate/` |
| LinkedIn Copy | POST | `/api/v1/agents/linkedin-copy/generate/` |

Full endpoint: `http://localhost:8000` + endpoint

---

## Share API with Teammates (Public URL)

If teammates need access from outside your network:

### Option 1: ngrok (free, 2 min)

```bash
pip install ngrok
# Or: npm install -g ngrok

ngrok http 8000
```

**Output:**
```
Forwarding                    https://abc123-456.ngrok.io -> http://localhost:8000
```

**Share URL:** `https://abc123-456.ngrok.io`

Teammates use this URL instead of `localhost:8000`

### Option 2: Deploy to Free Hosting

See `API_AGENTS_README.md` → "Free Hosting Options"

- Render.com (free tier)
- Railway (free tier)
- Fly.io (free tier)

---

## Troubleshooting

**Error: "Claude CLI not found"**
```bash
npm install -g @anthropic-ai/claude
```

**Error: Database connection failed**
- Ensure PostgreSQL running
- Or edit `backend/config/settings/local.py` to use SQLite for dev

**Error: "Authentication credentials not provided"**
- Missing `Authorization: Bearer <token>` header
- Token expired? Get new one from `/api/v1/auth/token/`

---

## API Documentation (Auto)

DRF includes browsable API:
```
http://localhost:8000/api/v1/agents/persona-classifier/
http://localhost:8000/api/v1/agents/message-strategy/
http://localhost:8000/api/v1/agents/email-copy/
http://localhost:8000/api/v1/agents/whatsapp-copy/
http://localhost:8000/api/v1/agents/linkedin-copy/
```

Visit in browser (with token), see docs + test live.

---

## Next: Teammate Integration

Share with teammate:

```
1. Server URL: http://localhost:8000 (or public ngrok/hosted URL)
2. JWT token: eyJhbGciOiJIUzI1NiIs...
3. Postman collection: backend/postman_agents_collection.json
4. Docs: backend/API_AGENTS_README.md
```

Teammate can now:
- Use any language (Python, JavaScript, Go, etc.)
- Call agents via REST endpoints
- No need to understand agent code
- No need to run Claude CLI themselves

---

**Setup complete!** ✅

API live. Endpoints ready. Teammates can integrate.
