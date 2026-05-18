# Persona Classifier Agent — Testing Guide (Claude CLI Version)

**NEW VERSION: Uses Claude CLI, NOT keyword mapping**

---

## What Changed?

| Before | Now |
|---|---|
| Keyword mapping (dumb) | Claude intelligence (smart) |
| "CEO of my life" → C-Level ❌ | "CEO of my life" → Fake title ✅ |
| No context understanding | Claude understands nuance, context |
| Fast, limited | Slower, much smarter |

---

## Prerequisites

### 1. Claude CLI Installed

Check if you have it:
```bash
claude --version
```

If not, install:
```bash
npm install -g @anthropic-ai/claude
```

Or via Homebrew (Mac):
```bash
brew install anthropic/claude/claude-cli
```

### 2. Claude CLI Authenticated

Make sure you're logged in:
```bash
claude login
```

(Uses your Claude.ai account, no API key needed)

---

## How to Test

### Test 1: Single Prospect (John - VP of Engineering)

```bash
cd c:\Users\Vansh\ken-abm-platform

python -c "
from agents.persona_classifier_agent import run_persona_classifier

output = run_persona_classifier(
    cleaned_prospects=[
        {
            'email': 'john@techcorp.com',
            'designation': 'VP of Engineering',
            'company_name': 'TechCorp Inc',
            'company_size': '500-1000',
            'industry': 'Software',
        }
    ],
    campaign_type='Market Research',
    target_personas=['CXO', 'Director', 'Manager'],
)

import json
print(json.dumps(output, indent=2, default=str))
"
```

**Expected Output:**
```json
{
  "classified_prospects": [
    {
      "email": "john@techcorp.com",
      "designation": "VP of Engineering",
      "company_name": "TechCorp Inc",
      "primary_persona": {
        "persona": "Director",
        "confidence_score": 85-95,  // Claude decides confidence
        "rationale": "VP indicates Executive level seniority. Engineering function aligns with Director persona..."
      },
      "secondary_persona": {
        "persona": "CXO",
        "confidence_score": 70-80,
        "rationale": "VP can influence C-level strategic decisions"
      },
      "seniority_level": "Executive",
      "function": "engineering",
      "needs_review": false
    }
  ],
  "persona_distribution": {"Director": 1},
  "average_confidence": 90,
  "low_confidence_count": 0,
  "unclassifiable_count": 0,
  "notes": "Classified 1 prospect using Claude CLI..."
}
```

**What to Check:**
- ✅ Persona = "Director" (expected)
- ✅ Confidence >= 80% (high confidence for clear title)
- ✅ Secondary = "CXO" (VP can be C-level)
- ✅ needs_review = False (clear role)

---

### Test 2: Fake Title (CEO of my Life)

```bash
python -c "
from agents.persona_classifier_agent import run_persona_classifier

output = run_persona_classifier(
    cleaned_prospects=[
        {
            'email': 'fake@test.com',
            'designation': 'CEO of my life',
            'company_name': 'MyLife Inc',
        }
    ],
    campaign_type='Market Research',
    target_personas=['CXO', 'Director', 'Manager'],
)

import json
print(json.dumps(output, indent=2, default=str))
"
```

**Expected Output:**
Claude should recognize this as:
- Fake/joke title
- Low confidence (< 40%)
- needs_review = True ← **FLAGGED**

```json
{
  "classified_prospects": [
    {
      "email": "fake@test.com",
      "designation": "CEO of my life",
      "primary_persona": {
        "persona": "CXO",  // or Unknown
        "confidence_score": 15-35,  // Very low!
        "rationale": "Title appears to be a joke/fake ('CEO of my life'). Not a legitimate executive title. Needs manual review."
      },
      "seniority_level": "Unknown",
      "function": "Unknown",
      "needs_review": true  // ← FLAGGED FOR REVIEW
    }
  ],
  "low_confidence_count": 1,
  "unclassifiable_count": 0,
}
```

**What to Check:**
- ✅ Confidence is LOW (< 50%, ideally < 40%)
- ✅ needs_review = True (flagged for manual review)
- ✅ Rationale mentions "joke" or "fake"

**This is the big win over keyword mapping!**

---

### Test 3: Non-Standard Title (Head Chef)

```bash
python -c "
from agents.persona_classifier_agent import run_persona_classifier

output = run_persona_classifier(
    cleaned_prospects=[
        {
            'email': 'chef@restaurant.com',
            'designation': 'Head Chef',
            'company_name': 'Restaurant XYZ',
            'industry': 'Food & Beverage',
        }
    ],
    campaign_type='Market Research',
    target_personas=['CXO', 'Director', 'Manager'],
)

import json
print(json.dumps(output, indent=2, default=str))
"
```

**Expected Output:**
Claude should recognize:
- "Head Chef" = non-B2B role
- Low match to B2B personas
- Probably unclassifiable or very low confidence

```json
{
  "classified_prospects": [
    {
      "email": "chef@restaurant.com",
      "designation": "Head Chef",
      "primary_persona": {
        "persona": "Manager",  // Best guess
        "confidence_score": 25-40,  // Low
        "rationale": "Head Chef is a hospitality/food service role, not a typical B2B buyer persona. May not be a decision-maker for your offering. Recommend manual review."
      },
      "needs_review": true
    }
  ],
  "low_confidence_count": 1,
}
```

**What to Check:**
- ✅ Confidence is LOW
- ✅ needs_review = True
- ✅ Rationale explains why (non-B2B, hospitality)

---

### Test 4: Ambiguous Title (Growth Lead)

```bash
python -c "
from agents.persona_classifier_agent import run_persona_classifier

output = run_persona_classifier(
    cleaned_prospects=[
        {
            'email': 'lead@startup.com',
            'designation': 'Growth Lead',
            'company_name': 'Startup Co',
            'industry': 'Software',
        }
    ],
    campaign_type='Market Research',
    target_personas=['CXO', 'Director', 'Manager'],
)

import json
print(json.dumps(output, indent=2, default=str))
"
```

**Expected Output:**
Claude should handle ambiguity:
- "Lead" = could be Manager or Individual Contributor
- "Growth" = could be multiple functions
- Medium confidence (50-70%)

```json
{
  "classified_prospects": [
    {
      "primary_persona": {
        "persona": "Manager",
        "confidence_score": 55-70,
        "rationale": "Growth Lead suggests mid-level role managing initiatives. Could be Manager or Director depending on company stage. Confidence is moderate."
      },
      "secondary_persona": {
        "persona": "Director",
        "confidence_score": 50-60,
        "rationale": "In some startups, Growth Leads report to C-level or are director-equivalent"
      },
      "needs_review": false  // or true, depending on confidence
    }
  ],
}
```

**What to Check:**
- ✅ Both primary and secondary assigned
- ✅ Confidence 55-70% (medium, not high or low)
- ✅ Rationale explains ambiguity

---

### Test 5: Multiple Prospects (Batch)

```bash
python -c "
from agents.persona_classifier_agent import run_persona_classifier

prospects = [
    {'email': 'john@tech.com', 'designation': 'VP of Engineering', 'company_name': 'TechCorp'},
    {'email': 'jane@marketing.com', 'designation': 'Marketing Manager', 'company_name': 'MarketingCo'},
    {'email': 'fake@test.com', 'designation': 'CEO of my life', 'company_name': 'MyLife'},
    {'email': 'chef@rest.com', 'designation': 'Head Chef', 'company_name': 'Restaurant'},
    {'email': 'growth@startup.com', 'designation': 'Growth Lead', 'company_name': 'Startup'},
]

output = run_persona_classifier(
    cleaned_prospects=prospects,
    campaign_type='Market Research',
    target_personas=['CXO', 'Director', 'Manager'],
)

print(f\"Classified: {len(output.classified_prospects)}\")
print(f\"Average Confidence: {output.average_confidence}%\")
print(f\"Low Confidence Count: {output.low_confidence_count}\")
print(f\"Persona Distribution: {output.persona_distribution}\")
"
```

**Expected Output:**
```
Classified: 5
Average Confidence: 58%
Low Confidence Count: 2  // CEO of my life + Head Chef
Persona Distribution: {'Director': 1, 'Manager': 2, ...}
```

**What to Check:**
- ✅ All 5 prospects processed
- ✅ Average confidence around 55-70%
- ✅ 2 low-confidence prospects (fake title + non-B2B)
- ✅ Personas distributed across multiple types

---

## How to Read Claude's Response

Claude returns JSON with this structure:

```json
{
  "persona": "Director",  // Assigned persona
  "confidence_score": 88,  // 0-100 (higher = more confident)
  "seniority_level": "Executive",  // C-Level, Executive, Director, Manager, IC
  "function": "engineering",  // engineering, marketing, sales, operations, etc.
  "rationale": "VP title indicates executive seniority...",  // Why Claude chose this
  "needs_review": false,  // true if confidence < 60% or suspicious
  "secondary_persona": {
    "persona": "CXO",
    "confidence_score": 70,
    "rationale": "VP can influence C-level..."
  }
}
```

**Key Signals:**

| Signal | Meaning |
|---|---|
| **confidence > 80%** | High confidence, clear role |
| **confidence 60-80%** | Good match, reasonable confidence |
| **confidence 40-60%** | Ambiguous, might need secondary |
| **confidence < 40%** | Low confidence, probably needs review |
| **needs_review: true** | Always check manually |
| **secondary_persona exists** | Multiple valid personas |

---

## Troubleshooting

### Error: "Claude CLI not found"

```
RuntimeError: Claude CLI not found. Install with: npm install -g @anthropic-ai/claude
```

**Fix:**
```bash
npm install -g @anthropic-ai/claude
```

---

### Error: "Claude CLI call timed out"

Claude is taking > 30 seconds to respond. Try:
1. Check internet connection
2. Try again (might be temporary)
3. Simplify prompt (fewer prospects at once)

---

### Empty/Null Response from Claude

Claude returned invalid JSON. Try:
1. Check prospect data (email, designation format)
2. Test with simpler prompt
3. Restart Claude CLI: `claude logout` → `claude login`

---

## Success Criteria

✅ **Agent 1 (Persona Classifier) is APPROVED when:**

1. ✅ Real titles classified correctly (VP → Director, Manager → Manager)
2. ✅ Fake/joke titles flagged as low confidence (< 50%)
3. ✅ Non-B2B roles handled (Head Chef → low confidence + needs_review)
4. ✅ Ambiguous titles assigned with secondary personas
5. ✅ All output has required fields (persona, confidence, seniority, function, rationale, needs_review)
6. ✅ Statistics calculated correctly (average_confidence, low_confidence_count, persona_distribution)
7. ✅ Error handling works (missing email/designation → unclassifiable_count)

---

## What's Next?

Once you test and confirm all above work:

1. **Report:** "Persona Classifier Agent works" ✅
2. **Any issues?** Let me know what needs adjustment
3. **Then:** I'll build Agent 2 (Message Strategy) with same detailed testing guide

**Do NOT approve until you've tested thoroughly with your own data.**

