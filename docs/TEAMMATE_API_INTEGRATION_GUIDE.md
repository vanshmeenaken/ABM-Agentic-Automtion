# Teammate API Integration Guide

**ABM Agents REST API — Complete Integration Package**

Share this document with your teammate to integrate agents into their system.

---

## Quick Start (3 steps)

### Step 1: Start the Server

```bash
cd backend
python manage.py runserver 8000
```

Server runs at: `http://localhost:8000`

### Step 2: Get JWT Token

```bash
curl -X POST http://localhost:8000/api/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'
```

**Response:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Save the `access` value. Use in all requests:**
```
Authorization: Bearer <your_access_token>
```

### Step 3: Call Any Agent Endpoint

See sections below for examples.

---

## API Endpoints (5 Agents)

### 1. Persona Classifier

**What it does:** Classifies prospect into buyer persona (CXO, Marketing, Operations, etc.) with confidence score.

**Endpoint:** `POST /api/v1/agents/persona-classifier/classify/`

**Full URL:** `http://localhost:8000/api/v1/agents/persona-classifier/classify/`

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/agents/persona-classifier/classify/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "designation": "VP of Sales",
    "company_type": "SaaS",
    "industry": "EdTech",
    "seniority_signals": ["manages 10+ people"]
  }'
```

**Required fields:**
- `designation` (string): Job title (e.g., "VP of Sales", "CTO")

**Optional fields:**
- `company_type` (string): Company type (e.g., "SaaS", "Manufacturing")
- `industry` (string): Industry (e.g., "EdTech", "FinTech")
- `seniority_signals` (array): Additional context (e.g., ["5+ years", "manages team"])

**Response:**
```json
{
  "persona_tag": "cxo_strategy",
  "confidence_score": 92,
  "classification_reason": "VP title indicates senior executive level...",
  "low_confidence_flag": false,
  "secondary_persona_tag": null
}
```

**Persona tags:**
- `cxo_strategy` — C-level executives
- `marketing` — Marketing professionals
- `operations` — Operations/supply chain
- `product_rd` — Product & R&D teams
- `investor` — Investors/board members
- `procurement` — Procurement professionals
- `unknown` — Unclassifiable (needs human review)

---

### 2. Message Strategy

**What it does:** Generates market-aware messaging strategy per persona (pain points, value propositions, tone guidance, channel recommendations).

**Endpoint:** `POST /api/v1/agents/message-strategy/generate/`

**Full URL:** `http://localhost:8000/api/v1/agents/message-strategy/generate/`

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/agents/message-strategy/generate/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_name": "K-12 EdTech Sales 2026",
    "campaign_type": "Market Research",
    "offer": "Research on EdTech adoption trends in Indian schools",
    "target_industry": "K-12 Education",
    "target_personas": ["cxo_strategy", "operations"],
    "channel_mix": ["email", "whatsapp", "linkedin"]
  }'
```

**Required fields:**
- `campaign_name` (string): Campaign name
- `campaign_type` (string): One of:
  - `Market Research`
  - `Survey`
  - `Consulting`
  - `Expert Network`
  - `Webinar`
  - `Report Sales`
  - `Competition Benchmarking`
  - `Account Reactivation`
- `offer` (string): Campaign offer description
- `target_industry` (string): Target industry
- `target_personas` (array): One or more of: `cxo_strategy`, `marketing`, `operations`, `product_rd`, `investor`, `procurement`

**Optional fields:**
- `channel_mix` (array): Preferred channels — `email`, `whatsapp`, `linkedin`

**Response:**
```json
{
  "campaign_name": "K-12 EdTech Sales 2026",
  "tone": "consultative",
  "key_themes": [
    "learning outcomes",
    "EdTech adoption",
    "competitive positioning"
  ],
  "value_propositions": {
    "cxo_strategy": "Strategic framework to capture remote-learning market shift",
    "operations": "Practical implementation guide for EdTech integration"
  },
  "call_to_action": "Schedule 20-min call to discuss your EdTech strategy",
  "persona_specific_messages": {
    "cxo_strategy": {
      "primary_angle": "Competitive positioning in EdTech shift",
      "pain_points": [
        "Competitors adopting EdTech faster",
        "Enrollment pressure from tech-forward schools",
        "Budget constraints for EdTech infrastructure"
      ],
      "value_prop": "Market insights + peer benchmarks to accelerate positioning"
    },
    "operations": {
      "primary_angle": "Operational efficiency through EdTech",
      "pain_points": [
        "Integration complexity with existing systems",
        "Teacher training burden",
        "Maintenance and support costs"
      ],
      "value_prop": "Implementation roadmap to reduce complexity"
    }
  },
  "channel_guidance": {
    "email": "Data-driven, lead with trend insight (85% adoption...). Professional but warm.",
    "whatsapp": "Peer-to-peer tone. Share quick insight. Conversational.",
    "linkedin": "Thought leadership angle. Position as EdTech strategist."
  },
  "success_criteria": {
    "email_open_rate": "28-35%",
    "click_rate": "6-9%",
    "response_rate": "4-6%",
    "meeting_rate": "1-2%"
  }
}
```

**Use this output as input for Email, WhatsApp, and LinkedIn Copy agents.**

---

### 3. Email Copy

**What it does:** Generates M1-M4 email copy (cold → follow-up → proof → final) based on messaging strategy.

**Endpoint:** `POST /api/v1/agents/email-copy/generate/`

**Full URL:** `http://localhost:8000/api/v1/agents/email-copy/generate/`

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/agents/email-copy/generate/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "strategy_brief": {
      "primary_angle": "Competitive positioning in EdTech shift",
      "pain_points": [
        "Competitors adopting faster",
        "Enrollment pressure"
      ],
      "value_prop": "Market insights to accelerate positioning"
    },
    "persona_tag": "cxo_strategy",
    "prospect_name": "John Doe",
    "company_name": "Greenfield School District",
    "offer": "EdTech adoption research",
    "stage": "M1",
    "sender_name": "Sarah Chen",
    "prior_email_subjects": []
  }'
```

**Required fields:**
- `strategy_brief` (object): Output from Message Strategy Agent
- `persona_tag` (string): One of: `cxo_strategy`, `marketing`, `operations`, `product_rd`, `investor`, `procurement`
- `prospect_name` (string): Prospect name
- `company_name` (string): Company name
- `offer` (string): Campaign offer
- `stage` (string): One of: `M1`, `M2`, `M3`, `M4`
- `sender_name` (string): Name of email sender

**Optional fields:**
- `prior_email_subjects` (array): Previous subject lines (to avoid repetition)

**Response:**
```json
{
  "subject": "3 trends reshaping K-12 strategy in 2026",
  "body": "Hi John,\n\nNoticed Greenfield's focus on learning outcomes. As 85% of K-12 institutions accelerate EdTech adoption, schools focused on remote readiness are capturing enrollment growth and narrowing the competitive gap.\n\nWe've just completed research on how top-performing schools position EdTech competitively. Would you find a 20-minute call valuable to discuss your positioning?\n\nBest,\nSarah Chen",
  "word_count": 165,
  "stage": "M1",
  "cta": "Schedule 20-min call to discuss your EdTech positioning"
}
```

**Stage guidelines:**
- **M1** (cold): Value-forward, short (120–180 words), one clear CTA
- **M2** (follow-up): Reference M1, add proof point, warmer (100–150 words)
- **M3** (proof): Social proof or sector insight, soft urgency (100–130 words)
- **M4** (final): Low pressure, alternative CTA (80–100 words)

**Constraints:**
- Subject < 60 characters
- No spam trigger words
- Plain text only
- No repeated subjects M1–M4

---

### 4. WhatsApp Copy

**What it does:** Generates M1-M4 WhatsApp copy (mobile-first, conversational, includes opt-out).

**Endpoint:** `POST /api/v1/agents/whatsapp-copy/generate/`

**Full URL:** `http://localhost:8000/api/v1/agents/whatsapp-copy/generate/`

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/agents/whatsapp-copy/generate/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

**Required fields:**
- `strategy_brief` (object): Output from Message Strategy Agent
- `persona_tag` (string): One of: `cxo_strategy`, `marketing`, `operations`, `product_rd`, `investor`, `procurement`
- `prospect_name` (string): Prospect name
- `company_name` (string): Company name
- `offer` (string): Campaign offer
- `stage` (string): One of: `M1`, `M2`, `M3`, `M4`
- `sender_name` (string): Sender name

**Response:**
```json
{
  "body": "Hi Jane! 👋 Saw you're leading growth at Lakewood Academy. Quick insight: 85% of schools are adopting EdTech now — early movers capturing market share. We've mapped how top schools are positioning this competitively. Would love to share findings. Free 20-min call?\n\nReply STOP to opt out.",
  "word_count": 62,
  "stage": "M1",
  "opt_out_line": "Reply STOP to opt out",
  "cta": "Schedule 20-min call"
}
```

**Stage guidelines:**
- **M1**: Introduce + context + question (max 120 words)
- **M2**: Brief follow-up, reference M1 (max 100 words)
- **M3**: Value add (insight/data point), soft ask (max 90 words)
- **M4**: Final, very short (max 70 words)

**Constraints:**
- **MANDATORY:** Include opt-out line
- Conversational tone (not formal)
- Don't copy email verbatim
- No attachments or media instructions

---

### 5. LinkedIn Copy

**What it does:** Generates LinkedIn connection request + follow-up DM (2-part output).

**Endpoint:** `POST /api/v1/agents/linkedin-copy/generate/`

**Full URL:** `http://localhost:8000/api/v1/agents/linkedin-copy/generate/`

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/agents/linkedin-copy/generate/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

**Required fields:**
- `strategy_brief` (object): Output from Message Strategy Agent
- `persona_tag` (string): One of: `cxo_strategy`, `marketing`, `operations`, `product_rd`, `investor`, `procurement`
- `prospect_name` (string): Prospect name
- `company_name` (string): Company name
- `offer` (string): Campaign offer
- `sender_name` (string): Sender name

**Response:**
```json
{
  "connection_request": {
    "connection_request_note": "Hi Alice, noticed your EdTech leadership at NextGen Schools. Would love to connect on strategy.",
    "character_count": 102
  },
  "follow_up_message": {
    "follow_up_message": "Hi Alice, thanks for connecting! We just completed research on how top schools position EdTech competitively in a crowded market. Thought you might find it valuable. Quick call to share insights?",
    "word_count": 42,
    "optimal_delay_hours": 48,
    "cta": "Schedule call to discuss EdTech positioning"
  }
}
```

**Output parts:**
- **connection_request**: Send as LinkedIn connection note (max 300 characters, no sales pitch, no URLs)
- **follow_up_message**: Send 48h+ after connection accepted (max 300 words)

**Note:** Platform does NOT send via LinkedIn. Copy is prepared for LinkedHelper setup.

---

## API Reference Table

| Agent | Endpoint | Method | Purpose |
|-------|----------|--------|---------|
| Persona Classifier | `/api/v1/agents/persona-classifier/classify/` | POST | Classify prospect into persona |
| Message Strategy | `/api/v1/agents/message-strategy/generate/` | POST | Generate messaging strategy |
| Email Copy | `/api/v1/agents/email-copy/generate/` | POST | Generate M1-M4 email copy |
| WhatsApp Copy | `/api/v1/agents/whatsapp-copy/generate/` | POST | Generate M1-M4 WhatsApp copy |
| LinkedIn Copy | `/api/v1/agents/linkedin-copy/generate/` | POST | Generate LinkedIn connection + DM |

**Base URL:** `http://localhost:8000`

---

## Required Headers (All Requests)

```
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json
```

---

## Recommended Agent Call Flow

```
1. Prospect Data Input
   ↓
2. Persona Classifier
   (designation → persona_tag + confidence)
   ↓
3. Message Strategy
   (persona_tag + campaign context → strategy_brief)
   ↓
4. Email/WhatsApp/LinkedIn Copy Agents (parallel)
   (strategy_brief → email/WhatsApp/LinkedIn copy)
   ↓
5. Compliance Review (coming soon)
   (copy → approved/rejected)
   ↓
6. Send via channel
```

---

## Code Examples

### Python

```python
import requests
import json

BASE_URL = "http://localhost:8000"
TOKEN = "your_access_token_here"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# 1. Classify persona
response = requests.post(
    f"{BASE_URL}/api/v1/agents/persona-classifier/classify/",
    headers=HEADERS,
    json={
        "designation": "VP of Sales",
        "company_type": "SaaS",
        "industry": "EdTech"
    }
)
persona = response.json()
print(f"Persona: {persona['persona_tag']}")
print(f"Confidence: {persona['confidence_score']}%")

# 2. Get messaging strategy
response = requests.post(
    f"{BASE_URL}/api/v1/agents/message-strategy/generate/",
    headers=HEADERS,
    json={
        "campaign_name": "K-12 EdTech",
        "campaign_type": "Market Research",
        "offer": "EdTech adoption research",
        "target_industry": "K-12 Education",
        "target_personas": [persona['persona_tag']],
        "channel_mix": ["email", "whatsapp"]
    }
)
strategy = response.json()
print(f"Campaign tone: {strategy['tone']}")

# 3. Generate email copy
response = requests.post(
    f"{BASE_URL}/api/v1/agents/email-copy/generate/",
    headers=HEADERS,
    json={
        "strategy_brief": {
            "primary_angle": strategy['persona_specific_messages'][persona['persona_tag']]['primary_angle'],
            "pain_points": strategy['persona_specific_messages'][persona['persona_tag']]['pain_points'],
            "value_prop": strategy['persona_specific_messages'][persona['persona_tag']]['value_prop']
        },
        "persona_tag": persona['persona_tag'],
        "prospect_name": "John Doe",
        "company_name": "Acme Corp",
        "offer": strategy['call_to_action'],
        "stage": "M1",
        "sender_name": "You",
        "prior_email_subjects": []
    }
)
email = response.json()
print(f"Subject: {email['subject']}")
print(f"Body: {email['body']}")
```

### JavaScript

```javascript
const BASE_URL = "http://localhost:8000";
const TOKEN = "your_access_token_here";
const HEADERS = {
    "Authorization": `Bearer ${TOKEN}`,
    "Content-Type": "application/json"
};

// 1. Classify persona
async function classifyPersona(designation, companyType) {
    const response = await fetch(
        `${BASE_URL}/api/v1/agents/persona-classifier/classify/`,
        {
            method: "POST",
            headers: HEADERS,
            body: JSON.stringify({
                designation: designation,
                company_type: companyType
            })
        }
    );
    return response.json();
}

// 2. Generate strategy
async function generateStrategy(campaignName, campaignType, offer, industry, personas) {
    const response = await fetch(
        `${BASE_URL}/api/v1/agents/message-strategy/generate/`,
        {
            method: "POST",
            headers: HEADERS,
            body: JSON.stringify({
                campaign_name: campaignName,
                campaign_type: campaignType,
                offer: offer,
                target_industry: industry,
                target_personas: personas,
                channel_mix: ["email", "whatsapp"]
            })
        }
    );
    return response.json();
}

// 3. Generate email copy
async function generateEmailCopy(strategyBrief, persona, prospectName, companyName) {
    const response = await fetch(
        `${BASE_URL}/api/v1/agents/email-copy/generate/`,
        {
            method: "POST",
            headers: HEADERS,
            body: JSON.stringify({
                strategy_brief: strategyBrief,
                persona_tag: persona,
                prospect_name: prospectName,
                company_name: companyName,
                offer: "EdTech research",
                stage: "M1",
                sender_name: "You",
                prior_email_subjects: []
            })
        }
    );
    return response.json();
}

// Usage
(async () => {
    const persona = await classifyPersona("VP of Sales", "SaaS");
    console.log(`Persona: ${persona.persona_tag}`);
    
    const strategy = await generateStrategy(
        "K-12 EdTech", 
        "Market Research", 
        "EdTech research", 
        "K-12 Education", 
        [persona.persona_tag]
    );
    console.log(`Tone: ${strategy.tone}`);
    
    const email = await generateEmailCopy(
        strategy,
        persona.persona_tag,
        "John Doe",
        "Acme Corp"
    );
    console.log(`Subject: ${email.subject}`);
})();
```

### cURL (Terminal)

```bash
TOKEN="your_access_token_here"
BASE_URL="http://localhost:8000"

# 1. Persona Classifier
curl -X POST $BASE_URL/api/v1/agents/persona-classifier/classify/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"designation": "VP of Sales", "company_type": "SaaS"}'

# 2. Message Strategy
curl -X POST $BASE_URL/api/v1/agents/message-strategy/generate/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_name": "K-12 EdTech",
    "campaign_type": "Market Research",
    "offer": "Research",
    "target_industry": "K-12 Education",
    "target_personas": ["cxo_strategy"]
  }'

# 3. Email Copy
curl -X POST $BASE_URL/api/v1/agents/email-copy/generate/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "strategy_brief": {...},
    "persona_tag": "cxo_strategy",
    "prospect_name": "John Doe",
    "company_name": "Acme Corp",
    "offer": "Research",
    "stage": "M1",
    "sender_name": "You"
  }'
```

---

## Error Handling

### Status Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 200 | Success | Your request worked |
| 400 | Bad Request | Check input fields, missing required field |
| 401 | Unauthorized | Invalid/missing JWT token, get new one |
| 500 | Server Error | Check Django logs, contact backend |
| 503 | Service Unavailable | Agent module not found, ensure Claude CLI installed |

### Error Response Format

```json
{
  "error": "Error message explaining what went wrong"
}
```

### Common Errors

**Error: "Authentication credentials were not provided"**
- Missing `Authorization: Bearer` header
- **Solution:** Add header to all requests

**Error: "Invalid token or token is expired"**
- JWT token invalid or expired
- **Solution:** Get new token from `/api/v1/auth/token/`

**Error: "Agent module not found"**
- Claude CLI not installed or not found
- **Solution:** Run `npm install -g @anthropic-ai/claude`

---

## Postman Collection

**Import into Postman:**
1. Download Postman: https://www.postman.com/downloads/
2. File → Import
3. Select `postman_agents_collection.json`
4. Set variables:
   - `BASE_URL`: `http://localhost:8000`
   - `JWT_TOKEN`: Your token from step 2
5. Click Send on any request

---

## Full Documentation

For detailed information, see:
- `backend/API_AGENTS_README.md` — Complete API reference
- `backend/AGENTS_API_QUICKSTART.md` — 5-minute setup
- `postman_agents_collection.json` — Ready-to-import requests

---

## Support

**Questions or issues?**

Check:
1. Server is running (`python manage.py runserver 8000`)
2. JWT token is valid and included in Authorization header
3. Endpoint URL is correct (copy from table above)
4. Input fields match required schema
5. Django logs for detailed error messages

---

## Version Info

- **API Version:** 1.0
- **Django REST Framework:** 3.15.1
- **Python:** 3.8+
- **Database:** PostgreSQL (or SQLite for dev)

---

**Ready to integrate!** Start with Step 1: Start the Server above. 🚀
