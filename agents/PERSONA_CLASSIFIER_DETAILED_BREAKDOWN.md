# Persona Classifier Agent — Detailed Breakdown & Walkthrough

Let me walk you through **exactly** how this agent works, step-by-step, with real examples.

---

## Real-World Example: John from TechCorp

Let's trace ONE prospect through the entire agent step-by-step.

### INPUT:
```python
prospect = {
    "email": "john@techcorp.com",
    "designation": "VP of Engineering",
    "company_name": "TechCorp Inc",
    "company_size": "500-1000",
    "industry": "Software",
}

campaign_type = "Market Research"
target_personas = ["CXO", "Director", "Manager"]
```

---

## STEP 1: Seniority Extraction

**Question:** What seniority level is "VP of Engineering"?

### The Logic:

```
SENIORITY_LEVELS = {
    "C-Level": {
        "titles": ["ceo", "cto", "cfo", "cmo", "coo", "chro", "chief"],
        "keywords": ["chief", "president", "founder"],
        "level": 5,
    },
    "Executive": {
        "titles": ["evp", "svp", "vp"],  ← VP is here!
        "keywords": ["executive", "vp of", "vice president"],
        "level": 4,
    },
    "Director": {
        "titles": ["director", "head of", "lead"],
        "keywords": ["director of", "head of department"],
        "level": 3,
    },
    "Manager": {
        "titles": ["manager", "senior manager", "team lead"],
        "keywords": ["manager", "team lead", "lead"],
        "level": 2,
    },
    "Individual Contributor": {
        "titles": ["specialist", "coordinator", "analyst", "engineer"],
        "keywords": ["specialist", "analyst", "engineer", "architect"],
        "level": 1,
    },
}
```

### Processing John's Designation:

```
Input: "VP of Engineering"
Convert to lowercase: "vp of engineering"

Check each seniority level:

1. C-Level:
   - Is "vp of engineering" in ["ceo", "cto", ...]? NO
   - Is "chief", "president", "founder" in text? NO
   → NOT C-Level

2. Executive:
   - Is "vp of engineering" in ["evp", "svp", "vp"]? NO (exact match fails)
   - Is "vp" in the text? YES ✓
   → Found "vp" → EXECUTIVE LEVEL
   → Confidence = 95% (title match = 95%)
   → STOP HERE (don't check other levels)

RESULT:
  seniority = "Executive"
  confidence = 95%
```

### Why 95%?

Looking at code:
```python
# Check exact title matches
if any(title in designation_lower for title in config["titles"]):
    return seniority, 95  # ← Returns 95% for title match

# Check keyword matches (if no title match)
if any(kw in designation_lower for kw in config["keywords"]):
    return seniority, 85  # ← Would return 85% for keyword match
```

**VP is an EXACT title match in the "Executive" titles list → 95% confidence**

---

## STEP 2: Function Extraction

**Question:** What function is "VP of Engineering"?

### The Logic:

```
FUNCTION_TO_PERSONA = {
    "engineering": ["Engineering", "Manager", "CXO"],
    "marketing": ["Marketing", "Manager", "Director"],
    "sales": ["Sales", "Manager"],
    "operations": ["Operations", "Manager", "Director"],
    "finance": ["Finance", "Manager", "Director"],
    # ... etc
}
```

### Processing John's Designation:

```
Input: "VP of Engineering"
Convert to lowercase: "vp of engineering"

FOR each function in FUNCTION_TO_PERSONA:
    "engineering" in "vp of engineering"? YES ✓
    
    → Found function "engineering"
    → Confidence = 90%
    → Candidate Personas = ["Engineering", "Manager", "CXO"]
    → STOP

RESULT:
  function = "engineering"
  confidence = 90%
  candidate_personas = ["Engineering", "Manager", "CXO"]
```

**Why "Engineering" not "Manager"?**  
The first persona in the list is what the function maps to. So engineering function → Engineering persona first.

---

## STEP 3: Persona Matching

**Question:** Given Executive seniority + Engineering function, which persona?

### The Logic:

```
PERSONA_TO_SENIORITY = {
    "CXO": ["C-Level"],
    "Director": ["Director", "Executive"],  ← Executive is here!
    "Manager": ["Manager", "Director"],
    "Specialist": ["Individual Contributor", "Manager"],
    "Individual Contributor": ["Individual Contributor"],
}
```

### Processing:

```
Step A: Get candidate personas from function
  candidate_personas = ["Engineering", "Manager", "CXO"]

Step B: Filter to only TARGET personas
  target_personas = ["CXO", "Director", "Manager"]
  
  Which candidates are in target?
  - "Engineering" in target? NO ✗
  - "Manager" in target? YES ✓
  - "CXO" in target? YES ✓
  
  matching_personas = ["Manager", "CXO"]

Step C: Check seniority alignment
  seniority = "Executive"
  target_persona = "Manager" (first in matching_personas)
  
  Does "Manager" accept "Executive" seniority?
  PERSONA_TO_SENIORITY["Manager"] = ["Manager", "Director"]
  Is "Executive" in ["Manager", "Director"]? NO ✗
  
  Does "Director" accept "Executive" seniority?
  PERSONA_TO_SENIORITY["Director"] = ["Director", "Executive"]
  Is "Executive" in ["Director", "Executive"]? YES ✓
  
  → "Director" is better fit than "Manager"
  → primary_persona = "Director"

RESULT:
  primary_persona = "Director"
```

---

## STEP 4: Confidence Score Calculation

**Question:** How confident are we that John is a "Director"?

### The Formula:

```
confidence = AVERAGE of:
  1. Seniority alignment score
  2. Function alignment score
  3. Exact title match bonus (optional)
```

### Calculating John's Confidence:

```
seniority_conf = 95%  (from Step 1)
function_conf = 90%   (from Step 2)
primary_persona = "Director"

Step 1: Seniority alignment
  Does "Executive" match "Director" persona's accepted seniorities?
  PERSONA_TO_SENIORITY["Director"] = ["Director", "Executive"]
  "Executive" is in the list? YES ✓
  
  → Use full seniority_conf = 95%

Step 2: Function alignment
  Does "engineering" match "Director" persona's functions?
  FUNCTION_TO_PERSONA["engineering"] = ["Engineering", "Manager", "CXO"]
  
  Wait... "Director" is NOT in this list!
  → This is a MISMATCH
  → Apply penalty: function_conf - 10 = 90 - 10 = 80%

Step 3: Calculate average
  confidence = (95 + 80) / 2 = 87.5% → ROUND → 88%

RESULT:
  primary_persona = "Director"
  confidence_score = 88%
```

### Secondary Persona (if confidence < 80%):

```
Our confidence (88%) >= 80%
→ No secondary persona assigned
→ secondary_persona = None

(If confidence were 75%:)
  secondary_persona = {
    "persona": "Manager" (next in matching list),
    "confidence_score": 75 - 15 = 60%,
    "rationale": "Could also be Manager..."
  }
```

---

## STEP 5: Review Flagging

**Question:** Does this prospect need manual review?

### The Logic:

```
IF confidence_score < 60%:
    needs_review = TRUE
ELSE:
    needs_review = FALSE
```

### For John:

```
confidence_score = 88%
Is 88% < 60%? NO
→ needs_review = FALSE

(John is confident enough, no manual review needed)

(If someone had "Marketing Coordinator" with 45% confidence:)
  Is 45% < 60%? YES
  → needs_review = TRUE
  (Flag for human to verify)
```

---

## FINAL OUTPUT FOR JOHN:

```python
{
    "email": "john@techcorp.com",
    "designation": "VP of Engineering",
    "company_name": "TechCorp Inc",
    "primary_persona": {
        "persona": "Director",
        "confidence_score": 88,
        "rationale": "VP title matches Executive seniority (95%). Engineering function aligns with Director persona (80%). Overall confidence: 88%.",
    },
    "secondary_persona": None,  # Confidence >= 80%, so no secondary
    "seniority_level": "Executive",
    "function": "engineering",
    "needs_review": False,  # Confidence >= 60%
}
```

---

## Now Let's Compare: Jane (Different Role)

### INPUT:
```python
prospect = {
    "email": "jane@techcorp.com",
    "designation": "Marketing Specialist",
    "company_name": "TechCorp Inc",
}
```

### STEP 1: Seniority Extraction

```
Input: "Marketing Specialist"
Lowercase: "marketing specialist"

Check seniority levels:
- C-Level: "chief", "president", "founder" in text? NO
- Executive: "vp", "evp", "svp" in text? NO
- Director: "director", "head of", "lead" in text? NO
- Manager: "manager", "team lead", "lead" in text? NO
- Individual Contributor: "specialist", "analyst", "engineer" in text?
  YES! "specialist" found ✓
  
RESULT:
  seniority = "Individual Contributor"
  confidence = 95%
```

### STEP 2: Function Extraction

```
Input: "Marketing Specialist"
Lowercase: "marketing specialist"

FOR each function:
  "marketing" in "marketing specialist"? YES ✓
  
RESULT:
  function = "marketing"
  confidence = 90%
  candidate_personas = ["Marketing", "Manager", "Director"]
```

### STEP 3: Persona Matching

```
candidate_personas = ["Marketing", "Manager", "Director"]
target_personas = ["CXO", "Director", "Manager"]

Which candidates in target?
- "Marketing" in target? NO ✗
- "Manager" in target? YES ✓
- "Director" in target? YES ✓

matching_personas = ["Manager", "Director"]
primary_persona = "Manager" (first in list)

Check seniority alignment:
PERSONA_TO_SENIORITY["Manager"] = ["Manager", "Director"]
Is "Individual Contributor" in ["Manager", "Director"]? NO ✗

→ Seniority mismatch!
→ Apply penalty: seniority_conf - 20 = 95 - 20 = 75%
```

### STEP 4: Confidence Calculation

```
seniority_conf (with penalty) = 75%
function_conf = 90%
primary_persona = "Manager"

Confidence = (75 + 90) / 2 = 82.5% → 82%
```

### STEP 5: Review Flag

```
Is 82% < 60%? NO
→ needs_review = False
```

### FINAL OUTPUT FOR JANE:

```python
{
    "email": "jane@techcorp.com",
    "designation": "Marketing Specialist",
    "company_name": "TechCorp Inc",
    "primary_persona": {
        "persona": "Manager",
        "confidence_score": 82,
        "rationale": "Specialist title = IC seniority, but Manager persona accepts Manager/Director. Marketing function aligns with Manager (90%). Overall: 82%.",
    },
    "secondary_persona": {
        "persona": "Director",
        "confidence_score": 67,  # 82 - 15
        "rationale": "Could also be Director if leading marketing team.",
    },
    "seniority_level": "Individual Contributor",
    "function": "marketing",
    "needs_review": False,
}
```

---

## Third Example: Unknown Role (Low Confidence)

### INPUT:
```python
prospect = {
    "email": "unknown@company.com",
    "designation": "Business Coordinator",
    "company_name": "Company Inc",
}
target_personas = ["CXO", "Director"]  # Strict targets
```

### STEP 1: Seniority Extraction

```
Input: "Business Coordinator"
Lowercase: "business coordinator"

Check all seniority levels:
- None of the exact titles match
- None of the keywords match ("chief", "vp", "director", etc.)

→ No match found
→ DEFAULT to Individual Contributor
→ Confidence = 50% (default for unknown)

RESULT:
  seniority = "Individual Contributor"
  confidence = 50%
```

### STEP 2: Function Extraction

```
Input: "Business Coordinator"
Lowercase: "business coordinator"

Check functions:
- "engineering" in text? NO
- "marketing" in text? NO
- "sales" in text? NO
- "operations" in text? NO
- ... (none match)

→ No function found
→ DEFAULT to "Other"
→ Confidence = 40%

RESULT:
  function = "Other"
  confidence = 40%
  candidate_personas = []  # Empty!
```

### STEP 3: Persona Matching

```
candidate_personas = []  # Nothing!
target_personas = ["CXO", "Director"]

No candidates to match!

→ Use target_personas[0] as fallback
→ primary_persona = "CXO"

Check seniority alignment:
PERSONA_TO_SENIORITY["CXO"] = ["C-Level"]
Is "Individual Contributor" in ["C-Level"]? NO ✗

→ Major mismatch!
→ Seniority penalty: 50 - 20 = 30%
```

### STEP 4: Confidence Calculation

```
seniority_conf (with penalty) = 30%
function_conf (unknown) = 40%
primary_persona = "CXO"

Confidence = (30 + 40) / 2 = 35%
```

### STEP 5: Review Flag

```
Is 35% < 60%? YES
→ needs_review = True  ← FLAG FOR MANUAL REVIEW!
```

### FINAL OUTPUT:

```python
{
    "email": "unknown@company.com",
    "designation": "Business Coordinator",
    "company_name": "Company Inc",
    "primary_persona": {
        "persona": "CXO",
        "confidence_score": 35,
        "rationale": "Role 'Business Coordinator' is ambiguous. Cannot determine seniority or function. Assigned CXO (target) with low confidence. Manual review recommended.",
    },
    "secondary_persona": None,
    "seniority_level": "Individual Contributor",
    "function": "Other",
    "needs_review": True,  ← FLAGGED!
}
```

---

## Summary Statistics

When processing 3 prospects (John, Jane, Unknown):

```python
{
    "classified_prospects": [
        # John's output (88% confidence)
        # Jane's output (82% confidence)
        # Unknown's output (35% confidence, needs_review=True)
    ],
    "persona_distribution": {
        "Director": 1,  # John
        "Manager": 1,   # Jane
        "CXO": 1,       # Unknown
    },
    "average_confidence": int((88 + 82 + 35) / 3) = 68%,
    "low_confidence_count": 1,  # Unknown (35% < 60%)
    "unclassifiable_count": 0,  # All had email + designation
    "notes": "Classified 3 prospects. 1 flagged for review (low confidence).",
}
```

---

## Visual Flow Diagram

```
INPUT PROSPECT
    ↓
┌───────────────────────────────────────┐
│ STEP 1: EXTRACT SENIORITY             │
│ "VP of Engineering" → Executive (95%) │
└───────────────────────────────────────┘
    ↓
┌───────────────────────────────────────┐
│ STEP 2: EXTRACT FUNCTION              │
│ "VP of Engineering" → engineering(90%)│
└───────────────────────────────────────┘
    ↓
┌───────────────────────────────────────┐
│ STEP 3: GET CANDIDATES FROM FUNCTION  │
│ engineering → [Engineering, Manager]  │
│ Filter to target → [Manager, CXO]     │
└───────────────────────────────────────┘
    ↓
┌───────────────────────────────────────┐
│ STEP 4: CHECK SENIORITY ALIGNMENT     │
│ Executive aligns with Director? YES   │
│ Select: Director persona              │
└───────────────────────────────────────┘
    ↓
┌───────────────────────────────────────┐
│ STEP 5: CALCULATE CONFIDENCE          │
│ (95% seniority + 80% function) / 2    │
│ = 88% confidence                      │
└───────────────────────────────────────┘
    ↓
┌───────────────────────────────────────┐
│ STEP 6: FLAG FOR REVIEW?              │
│ Is 88% < 60%? NO                      │
│ needs_review = False                  │
└───────────────────────────────────────┘
    ↓
OUTPUT: ClassifiedProspect
  - persona: "Director"
  - confidence: 88%
  - needs_review: False
```

---

## Key Points to Understand

### 1. **Seniority is extracted from TITLES**
- Look for exact titles first (CEO, VP, Director, Manager, Specialist)
- If not found, look for keywords (Chief, Executive, Lead)
- Exact title match = 95%, keyword match = 85%, not found = 50%

### 2. **Function is extracted from JOB KEYWORDS**
- Look for function keywords (engineering, marketing, sales, etc.)
- Each function maps to candidate personas
- Not found = "Other" function, 40% confidence

### 3. **Persona is selected by SENIORITY ALIGNMENT**
- Candidate personas are filtered to target personas
- Primary persona = first matching persona that aligns with seniority
- Secondary persona = second candidate (if available and confidence < 80%)

### 4. **Confidence is AVERAGE of SENIORITIES + FUNCTIONS**
- Both seniority and function contribute equally
- Mismatch = penalty (reduce by 10-20%)
- Final score clamped 0-100

### 5. **needs_review = Confidence < 60%**
- Low confidence = ambiguous role = needs human verification
- High confidence = we're confident, ship it

---

## What Happens With Edge Cases?

### Missing Email:
```
prospect = {"designation": "CEO", "company": "X"}  # No email

→ SKIP this prospect
→ unclassifiable_count += 1
→ Not included in classified_prospects
```

### Missing Designation:
```
prospect = {"email": "john@x.com", "company": "X"}  # No designation

→ SKIP this prospect
→ unclassifiable_count += 1
→ Not included in classified_prospects
```

### Empty List:
```
cleaned_prospects = []

→ Return empty classified_prospects
→ All counts = 0
→ average_confidence = 0
```

---

## Ready to Test?

Use these 3 examples:
1. **John** (VP of Engineering) → Should be Director 88%
2. **Jane** (Marketing Specialist) → Should be Manager 82% + Director secondary
3. **Unknown** (Business Coordinator) → Should be CXO 35% + needs_review=True

Run them through the agent and verify outputs match what I showed above.

If they match, Agent 1 is ✅ APPROVED. If not, let me know what's different.

