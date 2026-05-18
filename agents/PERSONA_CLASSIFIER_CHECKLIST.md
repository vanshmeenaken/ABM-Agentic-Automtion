# Persona Classifier Agent — Detailed Functionality Checklist

**Test this agent FIRST. Once approved, we build Agent 2.**

---

## Core Logic Overview

Agent takes prospect **designation** (job title) and extracts:
1. **Seniority Level** (C-Level, Executive, Director, Manager, Individual Contributor)
2. **Function** (Engineering, Marketing, Sales, Operations, Finance, Strategy, Product)
3. **Persona Assignment** (CXO, Director, Manager, Specialist, etc.)
4. **Confidence Score** (0-100%, how confident in the match)

---

## Input Schema

Agent accepts:
```python
cleaned_prospects = [
    {
        "email": "john@company.com",
        "designation": "VP of Engineering",  # REQUIRED
        "company_name": "TechCorp Inc",
        "company_size": "500-1000",
        "industry": "Software",
    },
    {
        "email": "jane@company.com",
        "designation": "Senior Marketing Manager",
        "company_name": "MarketingCo",
        # ... more fields
    }
]

campaign_type = "Market Research"  # Influences matching
target_personas = ["CXO", "Director", "Manager"]  # What we're looking for
```

---

## Step 1: Seniority Extraction Logic

### Seniority Levels Defined:

| Level | Priority Titles | Keywords | Confidence |
|---|---|---|---|
| **C-Level (5)** | CEO, CTO, CFO, CMO, COO, CHRO, Chief | Chief, President, Founder | 95% |
| **Executive (4)** | EVP, SVP, VP | Executive, VP of, Vice President | 95% |
| **Director (3)** | Director, Head of, Lead | Director of, Head of Department | 95% |
| **Manager (2)** | Manager, Senior Manager, Team Lead | Manager, Team Lead, Lead | 95% |
| **Individual Contributor (1)** | Specialist, Analyst, Engineer, Architect | Specialist, Analyst, Engineer, Architect | 95% |

### Logic:
```
IF designation contains (case-insensitive):
  - "CEO" OR "CTO" OR "CFO" OR "CMO" OR "COO" OR "CHRO" OR "Chief"
    → Seniority = "C-Level", Confidence = 95%
  
  - "EVP" OR "SVP" OR "VP" OR "Vice President"
    → Seniority = "Executive", Confidence = 95%
  
  - "Director" OR "Head of"
    → Seniority = "Director", Confidence = 95%
  
  - "Manager" OR "Senior Manager" OR "Team Lead"
    → Seniority = "Manager", Confidence = 95%
  
  - "Specialist" OR "Analyst" OR "Engineer" OR "Architect"
    → Seniority = "Individual Contributor", Confidence = 95%

ELSE
  → Seniority = "Individual Contributor", Confidence = 50%
```

**Test Cases for Step 1:**

| Input | Expected Seniority | Confidence |
|---|---|---|
| "CEO" | C-Level | 95% |
| "VP of Engineering" | Executive | 95% |
| "Director of Marketing" | Director | 95% |
| "Senior Manager" | Manager | 95% |
| "Software Engineer" | Individual Contributor | 95% |
| "Unknown Job" | Individual Contributor | 50% |

---

## Step 2: Function Extraction Logic

### Functions Defined:

| Function | Keywords | Maps to Personas |
|---|---|---|
| **CEO** | ceo | CXO |
| **CTO** | cto | CXO |
| **CFO** | cfo | CXO |
| **CMO** | cmo | CXO |
| **Marketing** | marketing, demand generation, martech, product marketing | Marketing, Manager, Director |
| **Sales** | sales, account executive, sales development, sales manager | Sales, Manager |
| **Operations** | operations, finance, procurement | Operations, Manager, Director |
| **Engineering** | engineering, product, it, infrastructure | Engineering, Manager, CXO |
| **Strategy** | strategy, business development, partnerships | Director, CXO, Business Development |

### Logic:
```
FOR each function IN FUNCTION_TO_PERSONA:
  IF designation contains function (case-insensitive):
    → Function = function, Confidence = 90%
    → Candidate Personas = FUNCTION_TO_PERSONA[function]
    BREAK

IF no function found:
  → Function = "Other", Confidence = 40%
  → Candidate Personas = []
```

**Test Cases for Step 2:**

| Input | Expected Function | Confidence |
|---|---|---|
| "VP of Engineering" | engineering | 90% |
| "Marketing Manager" | marketing | 90% |
| "Account Executive" | sales | 90% |
| "Chief Financial Officer" | cfo | 90% |
| "Random Title" | Other | 40% |

---

## Step 3: Persona Matching Logic

### Persona-Seniority Alignment:

```python
PERSONA_TO_SENIORITY = {
    "CXO": ["C-Level"],
    "Director": ["Director", "Executive"],
    "Manager": ["Manager", "Director"],
    "Specialist": ["Individual Contributor", "Manager"],
    "Individual Contributor": ["Individual Contributor"],
}
```

### Matching Algorithm:

```
1. Extract seniority + function from designation

2. Get candidate personas from FUNCTION_TO_PERSONA[function]
   
3. Filter candidates to only target_personas (from input)
   
4. Calculate confidence for PRIMARY persona:
   - Seniority alignment score: 95% if seniority matches, 75% if partial
   - Function alignment score: 90% if function matches, 70% if partial
   - Exact title match bonus: +100% if designation matches target
   - FINAL = Average of all scores, clamped 0-100

5. If PRIMARY confidence >= 60%:
   - needs_review = FALSE
   ELSE:
   - needs_review = TRUE (flag for manual review)

6. Secondary persona (if available and confidence < 80%):
   - Use second candidate persona
   - Confidence = PRIMARY confidence - 15%
```

**Test Cases for Step 3:**

| Designation | Target Personas | Primary | Primary Conf | Secondary | Needs Review |
|---|---|---|---|---|---|
| "VP of Engineering" | ["CXO", "Director"] | Director | 92% | CXO (70%) | NO |
| "Marketing Specialist" | ["Director", "Manager"] | Manager | 65% | — | NO |
| "Unknown Title" | ["Director", "CXO"] | Director | 50% | — | YES |
| "CEO" | ["CXO"] | CXO | 100% | — | NO |

---

## Step 4: Output Structure

```python
ClassifiedProspect = {
    "email": str,  # From input
    "designation": str,  # From input
    "company_name": str,  # From input
    "primary_persona": {
        "persona": str,  # CXO, Director, Manager, Specialist
        "confidence_score": int,  # 0-100
        "rationale": str,  # Why this persona
    },
    "secondary_persona": {  # Optional
        "persona": str,
        "confidence_score": int,
        "rationale": str,
    } OR None,
    "seniority_level": str,  # C-Level, Executive, Director, Manager, Individual Contributor
    "function": str,  # engineering, marketing, sales, operations, finance, strategy
    "needs_review": bool,  # TRUE if confidence < 60%
}

PersonaClassifierOutput = {
    "classified_prospects": List[ClassifiedProspect],
    "persona_distribution": {  # {persona: count}
        "CXO": 2,
        "Director": 5,
        "Manager": 3,
    },
    "average_confidence": int,  # Average of all primary confidences
    "low_confidence_count": int,  # Count where confidence < 60%
    "unclassifiable_count": int,  # Prospects missing email or designation
    "notes": str,  # Summary
}
```

---

## Step 5: Error Handling

| Scenario | Behavior |
|---|---|
| **Missing email** | Skip prospect, increment unclassifiable_count |
| **Missing designation** | Skip prospect, increment unclassifiable_count |
| **Unknown seniority** | Default to "Individual Contributor", confidence = 50% |
| **Unknown function** | Default to "Other", candidate_personas = [] |
| **Unknown persona in target** | Use first target_persona in list |
| **Empty target_personas** | Use ["Other"] as fallback |
| **Empty prospect list** | Return empty output with 0 statistics |

**Test Cases for Error Handling:**

| Input | Expected Behavior |
|---|---|
| `{"email": "john@test.com"}` (no designation) | Skip, unclassifiable_count += 1 |
| `{"designation": "CEO"}` (no email) | Skip, unclassifiable_count += 1 |
| `{"email": "x", "designation": "Unknown Job"}` | Classify with low confidence (50%) |
| `[]` (empty list) | Return empty classified_prospects, all counts = 0 |

---

## Complete Test Suite

### Test Case 1: Basic Classification (2 prospects)

**Input:**
```python
cleaned_prospects = [
    {
        "email": "john@techcorp.com",
        "designation": "VP of Engineering",
        "company_name": "TechCorp Inc",
    },
    {
        "email": "jane@techcorp.com",
        "designation": "Marketing Manager",
        "company_name": "TechCorp Inc",
    },
]
campaign_type = "Market Research"
target_personas = ["CXO", "Director", "Manager"]
```

**Expected Output:**
```python
{
    "classified_prospects": [
        {
            "email": "john@techcorp.com",
            "designation": "VP of Engineering",
            "primary_persona": {
                "persona": "Director",
                "confidence_score": 92,  # (95 + 90) / 2 = 92.5 → 92
                "rationale": "VP title maps to Executive/Director level. Engineering function aligns with Director persona.",
            },
            "secondary_persona": {
                "persona": "CXO",
                "confidence_score": 77,  # 92 - 15
                "rationale": "VP can influence C-level decisions.",
            },
            "seniority_level": "Executive",
            "function": "engineering",
            "needs_review": False,
        },
        {
            "email": "jane@techcorp.com",
            "designation": "Marketing Manager",
            "primary_persona": {
                "persona": "Manager",
                "confidence_score": 88,
                "rationale": "Manager title maps to Manager level. Marketing function aligns.",
            },
            "secondary_persona": None,
            "seniority_level": "Manager",
            "function": "marketing",
            "needs_review": False,
        },
    ],
    "persona_distribution": {
        "Director": 1,
        "Manager": 1,
    },
    "average_confidence": 90,  # (92 + 88) / 2
    "low_confidence_count": 0,
    "unclassifiable_count": 0,
    "notes": "Classified 2 prospects. 0 flagged for review.",
}
```

### Test Case 2: With Low Confidence

**Input:**
```python
cleaned_prospects = [
    {
        "email": "unknown@company.com",
        "designation": "Special Coordinator",  # Ambiguous
        "company_name": "Company Inc",
    },
]
campaign_type = "Survey"
target_personas = ["CXO", "Director"]
```

**Expected Output:**
```python
{
    "classified_prospects": [
        {
            "email": "unknown@company.com",
            "designation": "Special Coordinator",
            "primary_persona": {
                "persona": "CXO",  # Default to first target
                "confidence_score": 45,  # Low (seniority 50% + function 40%) / 2
                "rationale": "Designation 'Special Coordinator' is ambiguous...",
            },
            "secondary_persona": None,
            "seniority_level": "Individual Contributor",
            "function": "Other",
            "needs_review": True,  # Confidence < 60%
        },
    ],
    "persona_distribution": {"CXO": 1},
    "average_confidence": 45,
    "low_confidence_count": 1,  # ← This prospect needs review
    "unclassifiable_count": 0,
    "notes": "Classified 1 prospect. 1 flagged for review.",
}
```

### Test Case 3: With Errors

**Input:**
```python
cleaned_prospects = [
    {"email": "valid@test.com", "designation": "CEO"},  # Good
    {"designation": "VP Sales"},  # Missing email → skip
    {"email": "no_title@test.com"},  # Missing designation → skip
    {},  # Both missing → skip
]
campaign_type = "Webinar"
target_personas = ["CXO"]
```

**Expected Output:**
```python
{
    "classified_prospects": [
        {
            "email": "valid@test.com",
            "designation": "CEO",
            "primary_persona": {
                "persona": "CXO",
                "confidence_score": 100,  # CEO exact match
            },
            # ... rest of fields
        },
    ],
    "persona_distribution": {"CXO": 1},
    "average_confidence": 100,
    "low_confidence_count": 0,
    "unclassifiable_count": 3,  # ← 3 skipped due to errors
    "notes": "Classified 1 prospect. 3 unclassifiable.",
}
```

---

## Functionality Checklist

### ✅ MUST IMPLEMENT

- [ ] **Seniority Extraction:** Correctly identify seniority from designation
  - [ ] C-Level titles → 95% confidence
  - [ ] Executive (VP, SVP, EVP) → 95% confidence
  - [ ] Director → 95% confidence
  - [ ] Manager → 95% confidence
  - [ ] Individual Contributor → 95% confidence
  - [ ] Unknown → 50% confidence, default to IC

- [ ] **Function Extraction:** Identify function from designation
  - [ ] Engineering, Product, IT, Infrastructure → engineering
  - [ ] Marketing, Demand Gen, Martech → marketing
  - [ ] Sales, AE, SDR → sales
  - [ ] Operations, Finance, Procurement → operations/finance
  - [ ] Strategy, Business Development → strategy
  - [ ] Unknown → "Other", 40% confidence

- [ ] **Persona Matching:** Map extracted seniority + function to personas
  - [ ] Filter candidate personas to only target_personas
  - [ ] Calculate confidence (avg of seniority + function alignment)
  - [ ] Assign primary persona with confidence score
  - [ ] Optionally assign secondary persona if available

- [ ] **Confidence Scoring:**
  - [ ] Primary confidence = average of alignments, clamped 0-100
  - [ ] Secondary confidence = primary - 15
  - [ ] Clamp all scores to 0-100 range

- [ ] **Review Flagging:**
  - [ ] Flag needs_review = TRUE if confidence < 60%
  - [ ] Flag needs_review = FALSE if confidence >= 60%

- [ ] **Error Handling:**
  - [ ] Skip prospects missing email
  - [ ] Skip prospects missing designation
  - [ ] Continue processing on errors (don't crash)
  - [ ] Count unclassifiable prospects

- [ ] **Statistics Calculation:**
  - [ ] persona_distribution: count per persona
  - [ ] average_confidence: mean of all confidences
  - [ ] low_confidence_count: count < 60%
  - [ ] unclassifiable_count: count of skipped

- [ ] **Output Validation:**
  - [ ] All classified prospects have email, designation, company_name
  - [ ] All have primary_persona with confidence 0-100
  - [ ] All have seniority_level from defined list
  - [ ] All have function from defined list
  - [ ] All have needs_review boolean
  - [ ] Output dict has all required fields

---

## How to Test (On Your End)

### Step 1: Run the Agent

```bash
cd c:\Users\Vansh\ken-abm-platform
python -c "
from agents.persona_classifier_agent import run_persona_classifier

output = run_persona_classifier(
    cleaned_prospects=[
        {
            'email': 'john@company.com',
            'designation': 'VP of Engineering',
            'company_name': 'TechCorp Inc',
        }
    ],
    campaign_type='Market Research',
    target_personas=['CXO', 'Director', 'Manager'],
)

import json
print(json.dumps(output, indent=2, default=str))
"
```

### Step 2: Validate Output

Check against checklist:
- [ ] Seniority extracted correctly?
- [ ] Function extracted correctly?
- [ ] Persona assigned matches expectation?
- [ ] Confidence score makes sense?
- [ ] needs_review flag correct?
- [ ] Statistics calculated correctly?

### Step 3: Test Edge Cases

Run Test Cases 1, 2, 3 above and verify outputs match expected.

### Step 4: Report Results

Share with me:
- What worked ✅
- What needs fixing ❌
- What to adjust 🔧

---

## Once You Approve This Agent

You'll confirm:
- "Persona Classifier works as expected"
- Any adjustments needed
- Then I build Agent 2 (Message Strategy)

**Do NOT approve until you've tested thoroughly.**

