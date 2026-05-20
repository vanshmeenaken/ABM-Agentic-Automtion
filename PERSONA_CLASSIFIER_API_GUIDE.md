# Persona Classifier Agent - Complete API Guide & Local Setup

**Updated:** May 2026  
**Version:** 2.0 - Local Setup Ready  
**Status:** Production Ready ✅

---

## Quick Start (30 seconds)

```bash
# 1. Start server
python manage.py runserver

# 2. Test API (in another terminal)
curl -X POST http://localhost:8000/api/v1/agents/persona-classifier/classify/ \
  -H "Content-Type: application/json" \
  -d '{"designation": "VP of Sales"}'

# 3. Get response
# {
#   "persona_tag": "cxo_strategy",
#   "confidence_score": 92,
#   ...
# }
```

---

## Table of Contents

1. [Overview](#overview)
2. [Local Environment Setup](#local-environment-setup)
3. [API Details](#api-details)
4. [Request Format](#request-format)
5. [Response Format](#response-format)
6. [Code Examples](#code-examples)
7. [How to Integrate](#how-to-integrate)
8. [Testing Guide](#testing-guide)
9. [Error Handling](#error-handling)
10. [Troubleshooting](#troubleshooting)
11. [Team Integration](#team-integration)

---

## Overview

### What It Does
Maps prospect job titles + company context → standardized buyer personas with confidence scores.

**Example:**
- **Input:** `designation: "VP of Sales", company_type: "SaaS"`
- **Output:** `persona: "cxo_strategy", confidence: 92%`

### Key Features
✅ AI-powered persona classification using Claude  
✅ Confidence scoring (0-100)  
✅ Secondary persona detection  
✅ Low-confidence flags for human review  
✅ No external services required (Claude CLI local)  
✅ No authentication needed for local setup  

### Supported Personas
```
cxo_strategy        → C-level, VP, strategic roles
marketing           → Marketing leaders, growth
operations          → COO, operations leadership
product_rd          → Product, engineering, R&D
investor            → Investors, board members
procurement         → Procurement, sourcing
unknown             → Unclassifiable (needs review)
```

---

## Local Environment Setup

### Prerequisites

**What you need:**
```
✓ Python 3.9+
✓ Django 4.0+
✓ Django REST Framework
✓ Claude CLI installed
✓ Git
```

### Step 1: Install Dependencies

```bash
# Navigate to project
cd c:\Users\Vansh\ken-abm-platform

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### Step 2: Configure Django

```bash
# Create .env file (if using environment variables)
touch .env

# Run migrations
python manage.py migrate

# Create superuser (optional, for admin panel)
python manage.py createsuperuser
```

### Step 3: Install Claude CLI

```bash
# Install Claude CLI globally
npm install -g @anthropic-ai/claude

# Verify installation
claude --version
```

### Step 4: Start Development Server

```bash
# From project root
python manage.py runserver

# Server runs at: http://localhost:8000
# Press Ctrl+C to stop
```

**Expected output:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Step 5: Verify Setup

```bash
# Test endpoint is available
curl http://localhost:8000/api/v1/agents/persona-classifier/

# Should return 200 with endpoint info
```

---

## API Details

### Endpoint
```
POST /api/v1/agents/persona-classifier/classify/
```

### Full URL (Local)
```
http://localhost:8000/api/v1/agents/persona-classifier/classify/
```

### HTTP Method
```
POST
```

### Content-Type
```
application/json
```

### Authentication
```
✅ NONE - No JWT or API key required for local setup
```

### Response Time
```
⏱️ Typical: 2-5 seconds
⏱️ Max: 10 seconds (Claude CLI timeout)
```

---

## Request Format

### Parameters

| Field | Type | Required | Max Length | Example |
|-------|------|----------|-----------|---------|
| `designation` | string | **Yes** | 200 chars | `"VP of Sales"` |
| `company_type` | string | No | 100 chars | `"SaaS"` |
| `industry` | string | No | 100 chars | `"EdTech"` |
| `seniority_signals` | array | No | - | `["5+ years", "10+ team"]` |

### Examples

**Minimal Request (only required field):**
```json
{
  "designation": "Chief Technology Officer"
}
```

**Full Request (all fields):**
```json
{
  "designation": "VP of Marketing",
  "company_type": "SaaS",
  "industry": "EdTech",
  "seniority_signals": [
    "manages 15+ people",
    "5+ years marketing leadership",
    "B2B focus"
  ]
}
```

**Real-world Examples:**
```json
{
  "designation": "Director of Sales",
  "company_type": "Manufacturing",
  "industry": "Logistics",
  "seniority_signals": ["manages regional team", "10+ years"]
}
```

```json
{
  "designation": "Head of Product",
  "company_type": "FinTech",
  "industry": "Digital Banking"
}
```

---

## Response Format

### Success Response (HTTP 200)

```json
{
  "persona_tag": "cxo_strategy",
  "secondary_persona_tag": null,
  "confidence_score": 92,
  "classification_reason": "VP-level title indicates strategic executive role with P&L responsibility.",
  "low_confidence_flag": false
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `persona_tag` | enum | Primary persona (see Supported Personas) |
| `secondary_persona_tag` | enum\|null | Secondary persona if applicable |
| `confidence_score` | int (0-100) | Classification confidence |
| `classification_reason` | string | Why this classification was chosen |
| `low_confidence_flag` | bool | `true` if score < 60 (needs review) |

### Confidence Score Meaning

| Score | Level | Action |
|-------|-------|--------|
| 90-100 | Very High | Use as-is |
| 70-89 | High | Use with light validation |
| 60-69 | Medium | Review before use |
| < 60 | Low | **Flag for human review** |

### Example Responses

**High Confidence:**
```json
{
  "persona_tag": "cxo_strategy",
  "secondary_persona_tag": null,
  "confidence_score": 95,
  "classification_reason": "CEO title is unambiguous C-level executive role.",
  "low_confidence_flag": false
}
```

**Medium Confidence with Secondary Persona:**
```json
{
  "persona_tag": "cxo_strategy",
  "secondary_persona_tag": "operations",
  "confidence_score": 78,
  "classification_reason": "COO title spans both strategic and operational functions.",
  "low_confidence_flag": false
}
```

**Low Confidence - Needs Review:**
```json
{
  "persona_tag": "unknown",
  "secondary_persona_tag": null,
  "confidence_score": 25,
  "classification_reason": "Designation 'Growth Manager' is ambiguous - could be marketing or operations.",
  "low_confidence_flag": true
}
```

---

## Code Examples

### Python (requests)

```python
import requests
import json

# Setup
API_URL = "http://localhost:8000/api/v1/agents/persona-classifier/classify/"

# Prospect data
prospect = {
    "designation": "VP of Sales",
    "company_type": "SaaS",
    "industry": "EdTech",
    "seniority_signals": [
        "manages 20+ people",
        "8+ years sales experience"
    ]
}

# Make request
response = requests.post(API_URL, json=prospect, timeout=30)

# Handle response
if response.status_code == 200:
    result = response.json()
    print(f"✓ Persona: {result['persona_tag']}")
    print(f"✓ Confidence: {result['confidence_score']}%")
    print(f"✓ Reason: {result['classification_reason']}")
    
    if result['low_confidence_flag']:
        print("⚠️ NEEDS HUMAN REVIEW")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
```

### JavaScript (axios)

```javascript
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1/agents/persona-classifier/classify/';

const prospect = {
  designation: 'Chief Product Officer',
  company_type: 'FinTech',
  industry: 'Digital Banking',
  seniority_signals: ['manages 30+ engineers', 'reports to CEO']
};

axios.post(API_URL, prospect, { timeout: 30000 })
  .then(response => {
    const result = response.data;
    console.log(`Persona: ${result.persona_tag}`);
    console.log(`Confidence: ${result.confidence_score}%`);
    if (result.low_confidence_flag) console.warn('⚠️ Needs review');
  })
  .catch(error => console.error('Error:', error.response?.data || error.message));
```

### cURL (Command Line)

```bash
# Simple request
curl -X POST http://localhost:8000/api/v1/agents/persona-classifier/classify/ \
  -H "Content-Type: application/json" \
  -d '{"designation": "Director of Marketing"}'

# Full request with context
curl -X POST http://localhost:8000/api/v1/agents/persona-classifier/classify/ \
  -H "Content-Type: application/json" \
  -d '{
    "designation": "VP of Operations",
    "company_type": "Manufacturing",
    "industry": "Logistics",
    "seniority_signals": ["manages 50+ team", "10+ years ops"]
  }'
```

### Node.js (fetch)

```javascript
const API_URL = 'http://localhost:8000/api/v1/agents/persona-classifier/classify/';

const prospect = {
  designation: 'Head of Sales',
  company_type: 'SaaS',
  industry: 'EdTech'
};

const response = await fetch(API_URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(prospect)
});

const result = await response.json();
console.log('Classification:', result.persona_tag);
console.log('Confidence:', result.confidence_score);
```

### Batch Processing (Python)

```python
import requests
import csv
import json
from datetime import datetime

API_URL = "http://localhost:8000/api/v1/agents/persona-classifier/classify/"

# Load prospects from CSV
prospects = []
with open('prospects.csv') as f:
    reader = csv.DictReader(f)
    prospects = list(reader)

# Classify all
results = []
for i, prospect in enumerate(prospects, 1):
    response = requests.post(API_URL, json=prospect, timeout=30)
    if response.status_code == 200:
        result = response.json()
        result['input_designation'] = prospect['designation']
        results.append(result)
        print(f"✓ {i}/{len(prospects)} - {prospect['designation']} → {result['persona_tag']}")
    else:
        print(f"✗ {i}/{len(prospects)} - Error: {response.status_code}")

# Save results
with open('classifications.json', 'w') as f:
    json.dump(results, f, indent=2)

# Stats
print(f"\n📊 Summary:")
print(f"Total: {len(results)}")
avg_confidence = sum(r['confidence_score'] for r in results) / len(results)
print(f"Average Confidence: {avg_confidence:.1f}%")
low_conf = sum(1 for r in results if r['low_confidence_flag'])
print(f"Needs Review: {low_conf}")
```

---

## How to Integrate

### For Backend/API Integrations

```python
# In your Django view or service
import requests

def classify_prospect(designation, company_type=None, industry=None):
    """Classify a prospect and return persona."""
    
    payload = {
        "designation": designation,
        "company_type": company_type,
        "industry": industry
    }
    
    response = requests.post(
        "http://localhost:8000/api/v1/agents/persona-classifier/classify/",
        json=payload,
        timeout=30
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Classification failed: {response.text}")

# Usage
result = classify_prospect("VP of Sales", "SaaS", "EdTech")
print(result['persona_tag'])  # "cxo_strategy"
```

### For Frontend/Web Apps

```javascript
// In your React/Vue/Angular component
async function classifyProspect(designation, companyType, industry) {
  try {
    const response = await fetch(
      'http://localhost:8000/api/v1/agents/persona-classifier/classify/',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          designation,
          company_type: companyType,
          industry
        })
      }
    );
    
    if (!response.ok) throw new Error('Classification failed');
    
    const result = await response.json();
    return result;
  } catch (error) {
    console.error('Error:', error);
    return null;
  }
}

// Usage in component
const result = await classifyProspect('CEO', 'SaaS', 'EdTech');
if (result?.low_confidence_flag) {
  console.warn('Needs human review');
}
```

### For Downstream Agents

Use `persona_tag` with Message Strategy Agent:

```python
# After classification
classification = classify_prospect(designation, company_type, industry)
persona = classification['persona_tag']

# Pass to Message Strategy Agent
from message_strategy_agent import run_message_strategy

strategy = run_message_strategy(
    campaign_name="Q2 Campaign",
    target_personas=[persona],  # Use classification
    # ... other params
)
```

---

## Testing Guide

### Unit Test Scenarios

#### Test 1: Clear Executive Title
```bash
curl -X POST http://localhost:8000/api/v1/agents/persona-classifier/classify/ \
  -H "Content-Type: application/json" \
  -d '{"designation": "Chief Executive Officer"}'
```
**Expected:** `persona_tag: "cxo_strategy"`, `confidence_score: 95+`

#### Test 2: Ambiguous Title with Context
```bash
curl -X POST http://localhost:8000/api/v1/agents/persona-classifier/classify/ \
  -H "Content-Type: application/json" \
  -d '{
    "designation": "Manager",
    "company_type": "Manufacturing",
    "industry": "Logistics",
    "seniority_signals": ["manages plant operations"]
  }'
```
**Expected:** `confidence_score: 60+`, clear persona

#### Test 3: Low Confidence Case
```bash
curl -X POST http://localhost:8000/api/v1/agents/persona-classifier/classify/ \
  -H "Content-Type: application/json" \
  -d '{"designation": "Growth Manager"}'
```
**Expected:** `low_confidence_flag: true` OR medium confidence

#### Test 4: Unclassifiable
```bash
curl -X POST http://localhost:8000/api/v1/agents/persona-classifier/classify/ \
  -H "Content-Type: application/json" \
  -d '{"designation": "CEO of my life"}'
```
**Expected:** `persona_tag: "unknown"`, `low_confidence_flag: true`

### Manual Testing Workflow

```bash
#!/bin/bash
# save as test_api.sh

API="http://localhost:8000/api/v1/agents/persona-classifier/classify/"

echo "Testing Persona Classifier API..."
echo "=================================="

# Test 1
echo "Test 1: CEO"
curl -s -X POST $API -H "Content-Type: application/json" -d '{"designation":"CEO"}' | python -m json.tool

# Test 2
echo "\nTest 2: VP with context"
curl -s -X POST $API -H "Content-Type: application/json" -d '{
  "designation":"VP of Sales",
  "company_type":"SaaS",
  "industry":"EdTech"
}' | python -m json.tool

# Test 3
echo "\nTest 3: Unknown title"
curl -s -X POST $API -H "Content-Type: application/json" -d '{"designation":"Ninja Developer"}' | python -m json.tool

echo "\nDone!"
```

Run with: `bash test_api.sh`

### Test Coverage Checklist

- [ ] Single designation only (no context)
- [ ] Full context (all fields)
- [ ] High-confidence classifications (CEO, CTO)
- [ ] Medium-confidence classifications (Director, Manager)
- [ ] Low-confidence classifications (ambiguous titles)
- [ ] Unknown persona (unclassifiable)
- [ ] Secondary persona assignments
- [ ] Response time < 10 seconds
- [ ] JSON validation
- [ ] Error handling (bad JSON, missing fields)
- [ ] Batch processing (10+ requests)

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Fix |
|------|---------|-----|
| 200 | Success ✅ | Use response |
| 400 | Bad Request | Check JSON format, verify required fields |
| 404 | Not Found | Check URL is correct, server running |
| 500 | Server Error | Check server logs, retry in 10 seconds |
| 503 | Service Unavailable | Claude CLI not working, restart server |

### Common Errors & Fixes

**Error: Connection refused**
```
Error: Failed to connect to http://localhost:8000
```
**Fix:**
```bash
# Start server
python manage.py runserver

# Or check if already running
netstat -tuln | grep 8000
```

**Error: Missing required field**
```json
{
  "designation": ["This field is required."]
}
```
**Fix:**
```python
# Ensure designation is always included
payload = {
    "designation": prospect_title,  # REQUIRED
    "company_type": optional_company_type
}
```

**Error: Agent module not found**
```json
{
  "error": "Agent module not found: No module named 'persona_classifier_agent'"
}
```
**Fix:**
```bash
# Ensure agent files exist
ls -la agents/persona_classifier_agent.py

# Add agents to Python path if needed
export PYTHONPATH="${PYTHONPATH}:/path/to/agents"
```

**Error: Claude CLI timeout**
```json
{
  "error": "Agent execution failed: Claude CLI call timed out after 30 seconds"
}
```
**Fix:**
```bash
# Verify Claude CLI works
claude ask "test prompt"

# Increase timeout in views.py if needed
timeout=60  # Increase from 30
```

---

## Troubleshooting

### Server Won't Start

**Issue:** `Address already in use`

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -tuln | grep 8000  # Windows

# Kill process
kill -9 <PID>

# Or use different port
python manage.py runserver 8001
```

### API Returns 404

**Issue:** `Not Found at /api/v1/agents/persona-classifier/classify/`

**Solutions:**
1. Check URL spelling exactly
2. Verify server is running: `python manage.py runserver`
3. Check Django URLs are configured correctly

### Slow Responses (> 10 seconds)

**Possible Causes:**
- Claude CLI hanging
- Slow network
- Server overloaded

**Solutions:**
```python
# Increase timeout
response = requests.post(
    url,
    json=data,
    timeout=60  # Increase from 30
)

# Check Claude is responsive
claude ask "what is 2+2?"  # Should respond in seconds
```

### Claude CLI Not Found

**Error:** `Claude CLI not found`

**Solution:**
```bash
# Install Claude CLI
npm install -g @anthropic-ai/claude

# Verify
which claude  # macOS/Linux
where claude  # Windows
claude --version

# If still not found, check Node.js is installed
node --version
npm --version
```

### All Requests Return "unknown" Persona

**Possible Causes:**
- Claude CLI not working
- Agent not configured
- Server issues

**Solution:**
```bash
# Test Claude CLI directly
claude ask "The person is a CEO. What buyer persona?"

# Check agent file exists and imports work
python -c "from agents.persona_classifier_agent import run_persona_classifier"

# Check server logs for errors
# Look at terminal where you started: python manage.py runserver
```

---

## Team Integration

### Share with Team

**Step 1: Ensure server is running**
```bash
python manage.py runserver
```

**Step 2: Share API URL**
```
http://localhost:8000/api/v1/agents/persona-classifier/classify/
```

**Step 3: Share example request**
```json
{
  "designation": "VP of Sales",
  "company_type": "SaaS",
  "industry": "EdTech"
}
```

**Step 4: Share this documentation**
```
PERSONA_CLASSIFIER_API_GUIDE.md (this file)
```

### Team Usage Instructions

**For Non-Technical Team Members:**
1. Ask engineer for server URL
2. Use Postman or REST client
3. Send POST request with prospect data
4. Get classification result
5. Use persona for messaging strategy

**For Developers:**
1. Read this guide
2. Use code examples (Python, JavaScript, cURL)
3. Integrate into your system
4. Test with provided scenarios

**For Data/Analytics Teams:**
1. Export prospect list
2. Use batch processing script (see Code Examples)
3. Get classifications for all prospects
4. Export results to CSV/JSON
5. Analyze patterns by persona

---

## Support & Troubleshooting

### Quick Checklist

- [ ] Python 3.9+ installed
- [ ] Claude CLI installed: `claude --version`
- [ ] Django running: `python manage.py runserver`
- [ ] Can reach `http://localhost:8000`
- [ ] Can call API endpoint (try cURL example)
- [ ] Getting valid responses

### If Something Breaks

**Step 1:** Check Django server logs (terminal where you started it)

**Step 2:** Verify Claude works:
```bash
claude ask "hello"
```

**Step 3:** Test API directly:
```bash
curl http://localhost:8000/api/v1/agents/persona-classifier/classify/ \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"designation":"CEO"}'
```

**Step 4:** Check agent file exists:
```bash
ls -la agents/persona_classifier_agent.py
```

**Step 5:** Restart everything
```bash
# Ctrl+C to stop server
# Stop any Claude processes
pkill -f claude

# Restart
python manage.py runserver
```

### Contact

**For Issues:**
- Check Troubleshooting section above
- Check Django server logs
- Verify all prerequisites installed

---

## GitHub References

**Source Code:**
- [Agent Implementation](https://github.com/vanshmeenaken/ABM-Agentic-Automtion/blob/master/agents/persona_classifier_agent.py)
- [API Views](https://github.com/vanshmeenaken/ABM-Agentic-Automtion/blob/master/backend/apps/agents_api/views.py)
- [URL Routing](https://github.com/vanshmeenaken/ABM-Agentic-Automtion/blob/master/backend/apps/agents_api/urls.py)
- [Serializers](https://github.com/vanshmeenaken/ABM-Agentic-Automtion/blob/master/backend/apps/agents_api/serializers.py)

---

## Summary

| What | Where |
|------|-------|
| **Start Server** | `python manage.py runserver` |
| **API URL** | `http://localhost:8000/api/v1/agents/persona-classifier/classify/` |
| **Auth Required** | ❌ No |
| **Typical Response Time** | 2-5 seconds |
| **Typical Timeout** | 30 seconds max |
| **Free to Use** | ✅ Yes (local) |
| **Setup Time** | ~5 minutes |

---

**Status:** ✅ Production Ready  
**Last Updated:** May 2026  
**Ready to Share:** Yes!
