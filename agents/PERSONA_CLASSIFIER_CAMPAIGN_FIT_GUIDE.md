# Persona Classifier Agent — Campaign-Aware Bifurcation Guide

## Overview

Agent 1 now performs **three-level segmentation** in a single pass:

1. **Seniority Classification** — Who are they? (C-Level, Executive, Manager, etc.)
2. **Function Extraction** — What do they do? (Engineering, Marketing, Sales, etc.)
3. **Campaign Fit Validation** — Are they relevant to THIS campaign? (fit_score 0-100)

Before: Prospects classified into 5 personas only.
Now: Prospects classified into 5 personas + validated for campaign relevance.

---

## Key Concept: Campaign Fit Scoring

**Campaign Fit Score (0-100):** How well does this prospect's function/role align with the campaign's goals?

**Campaign Fit Valid (true/false):** Is this prospect worth targeting? (True if fit_score >= 70)

### Example: K-12 Education Campaign

| Prospect | Persona | Function | Fit Score | Fit Valid | Why |
|----------|---------|----------|-----------|-----------|-----|
| VP Curriculum | Director | Education/Curriculum | 95% | ✓ | Core to education institutions |
| Finance Director | Director | Finance | 45% | ✗ | High seniority BUT wrong function |
| Head of Instruction | Director | Education/Instruction | 98% | ✓ | Perfect alignment |
| HR Manager | Manager | Human Resources | 30% | ✗ | Right org level, wrong function |
| EdTech Coordinator | Manager | Education Tech | 92% | ✓ | Strong alignment with EdTech focus |
| Principal | Director | School Admin | 96% | ✓ | Key decision-maker |

**Bifurcation Result:**
- **High Fit (5):** Target with full campaign
- **Low Fit (2):** Skip or handle separately

---

## How to Use: Step by Step

### Step 1: Define Campaign Context

When calling the Persona Classifier, provide:

```python
from agents import run_persona_classifier

output = run_persona_classifier(
    cleaned_prospects=[
        {'email': 'alice@school.edu', 'designation': 'VP of Curriculum Development', ...},
        {'email': 'bob@school.edu', 'designation': 'Finance Director', ...},
        {'email': 'carol@school.edu', 'designation': 'Head of Instruction & Learning', ...},
    ],
    campaign_type='Market Research',
    target_personas=['CXO', 'Director', 'Manager'],
    # NEW: Campaign context for fit validation
    target_industry='K-12 Education',
    target_functions=['Curriculum', 'Instruction', 'Education Technology', 'School Administration'],
)
```

### Step 2: Interpret Output

Each prospect now has:

```json
{
  "email": "alice@school.edu",
  "designation": "VP of Curriculum Development",
  "company_name": "Jefferson High School",
  "primary_persona": {
    "persona": "Director",
    "confidence_score": 94,
    "rationale": "VP of Curriculum is a key decision-maker in K-12 education."
  },
  "secondary_persona": null,
  "seniority_level": "Executive",
  "function": "Education/Curriculum",
  "needs_review": false,
  
  // NEW: Campaign Fit Validation
  "campaign_fit_score": 95,
  "campaign_fit_valid": true,
  "campaign_fit_rationale": "Perfect fit for K-12 education campaign. Curriculum development is core to education institutions."
}
```

### Step 3: Bifurcate Prospects

Filter by `campaign_fit_valid` and `campaign_fit_score`:

```python
# Tier 1: High Fit (score >= 80 AND valid=true)
high_fit = [
    p for p in output.classified_prospects
    if p.campaign_fit_score >= 80 and p.campaign_fit_valid
]

# Tier 2: Medium Fit (score 60-79 AND valid=true)
medium_fit = [
    p for p in output.classified_prospects
    if 60 <= p.campaign_fit_score < 80 and p.campaign_fit_valid
]

# Tier 3: Low/No Fit (score < 60 OR valid=false)
low_fit = [
    p for p in output.classified_prospects
    if p.campaign_fit_score < 60 or not p.campaign_fit_valid
]
```

**Action per tier:**
- **Tier 1 (High Fit):** Send full campaign messaging
- **Tier 2 (Medium Fit):** Send with secondary messaging or education
- **Tier 3 (Low Fit):** Skip from campaign or handle separately

---

## Real-World Example: K-12 Education Campaign

### Campaign Setup

```
Campaign: "K-12 Learning Solutions"
Target Industry: K-12 Education
Preferred Functions: Curriculum, Instruction, Education Technology, School Administration
```

### Prospect List

1. alice@school.edu — VP of Curriculum Development, Jefferson High School
2. bob@school.edu — Finance Director, Lincoln Middle School
3. carol@school.edu — Head of Instruction & Learning, Roosevelt Elementary
4. david@district.edu — Chief Learning Officer, County School District
5. emma@school.edu — HR Manager, Madison High School
6. frank@school.edu — Educational Technology Coordinator, Washington Academy
7. grace@school.edu — Principal, Adams High School

### Agent Output

#### Prospect 1: Alice (VP Curriculum)
```
Primary Persona: Director (94%)
Seniority: Executive
Function: Education/Curriculum
Campaign Fit Score: 95%
Campaign Fit Valid: ✓ YES
Rationale: "Perfect fit. Curriculum development is core to education institutions."
Action: Tier 1 — HIGH FIT → Send priority outreach
```

#### Prospect 2: Bob (Finance Director)
```
Primary Persona: Director (90%)
Seniority: Executive
Function: Finance
Campaign Fit Score: 45%
Campaign Fit Valid: ✗ NO
Rationale: "While Director-level, Finance function is not primary target for K-12. Focus on curriculum/instruction roles."
Action: Tier 3 — LOW FIT → Skip from campaign
```

#### Prospect 3: Carol (Head of Instruction)
```
Primary Persona: Director (92%)
Seniority: Executive
Function: Education/Instruction
Campaign Fit Score: 98%
Campaign Fit Valid: ✓ YES
Rationale: "Excellent fit. Instruction/learning is core function for K-12."
Action: Tier 1 — HIGH FIT → Send priority outreach
```

#### Prospect 4: David (CLO)
```
Primary Persona: CXO (96%)
Seniority: C-Suite
Function: Education/Strategy
Campaign Fit Score: 99%
Campaign Fit Valid: ✓ YES
Rationale: "Perfect fit. CLO directly responsible for education strategy."
Action: Tier 1 — HIGH FIT → Send C-level outreach
```

#### Prospect 5: Emma (HR Manager)
```
Primary Persona: Manager (85%)
Seniority: Manager
Function: Human Resources
Campaign Fit Score: 30%
Campaign Fit Valid: ✗ NO
Rationale: "HR function not aligned. Focus on curriculum/instruction/learning roles."
Action: Tier 3 — LOW FIT → Skip from campaign
```

#### Prospect 6: Frank (EdTech Coordinator)
```
Primary Persona: Manager (78%)
Seniority: Manager
Function: Education Technology
Campaign Fit Score: 92%
Campaign Fit Valid: ✓ YES
Rationale: "Strong fit. EdTech adoption key to modern education solutions."
Action: Tier 1 — HIGH FIT → Send campaign outreach
```

#### Prospect 7: Grace (Principal)
```
Primary Persona: Director (88%)
Seniority: Executive
Function: School Administration
Campaign Fit Score: 96%
Campaign Fit Valid: ✓ YES
Rationale: "Excellent fit. Principal is key decision-maker for school operations."
Action: Tier 1 — HIGH FIT → Send priority outreach
```

### Campaign Penetration Summary

```
Total Prospects: 7
├─ Tier 1 (High Fit):   5 prospects (71%)
│  └─ CXO: 1 → $100K+ deal
│  └─ Director: 3 → $25K-$100K deals
│  └─ Manager: 1 → $5K-$25K deal
├─ Tier 2 (Medium Fit): 0 prospects (0%)
└─ Tier 3 (Low Fit):    2 prospects (29%)
   ├─ Bob (Finance Director) → Skip
   └─ Emma (HR Manager) → Skip

Campaign Actionable Rate: 71% (5 of 7)
```

---

## How Campaign Fit is Evaluated

Claude analyzes:

1. **Function Alignment**
   - Does their role typically make decisions in this area?
   - Is their function on the preferred list?
   - Example: "Curriculum VP" → 95% fit for K-12 education (core function)

2. **Industry Context**
   - Does the campaign target their industry?
   - Are they in a relevant vertical?
   - Example: "Finance Director" in school → 45% fit (not core to education solutions, even though in right org)

3. **Decision-Making Authority**
   - Can they approve/influence decisions?
   - Do they control relevant budgets?
   - Example: "Principal" → 96% fit (controls school operations budget)

4. **Relevance Score Calculation**
   ```
   campaign_fit_score = (
       function_alignment_score × 0.50 +    // Does their job match what we need? (50% weight)
       industry_relevance_score × 0.30 +    // Are they in the right industry? (30% weight)
       decision_authority_score × 0.20      // Can they say yes? (20% weight)
   )
   ```

---

## Campaign Fit Thresholds

| Score Range | Interpretation | Action |
|---|---|---|
| 90-100% | Perfect fit | Tier 1: Priority outreach |
| 80-89% | Strong fit | Tier 1: Standard outreach |
| 70-79% | Good fit | Tier 2: Secondary outreach |
| 60-69% | Moderate fit | Tier 2: Educational nurture |
| 50-59% | Weak fit | Tier 3: Skip or special handling |
| 0-49% | Poor fit | Tier 3: Exclude from campaign |

---

## Different Campaign Examples

### Campaign 1: K-12 Education Solutions
```
Target Industry: K-12 Education
Target Functions: [Curriculum, Instruction, EdTech, School Admin]
Avoid: Finance, HR (unless budget authority)

Results:
- VP of Curriculum → 95% fit ✓
- Finance Director → 45% fit ✗
- Principal → 96% fit ✓
```

### Campaign 2: HR Software
```
Target Industry: Any
Target Functions: [Human Resources, Talent Acquisition, Payroll, People Operations]
Avoid: Finance (unless payroll-related)

Results:
- HR Manager → 92% fit ✓
- Finance Director → 35% fit ✗
- VP of People → 98% fit ✓
```

### Campaign 3: Manufacturing ERP
```
Target Industry: Manufacturing
Target Functions: [Operations, Supply Chain, Manufacturing, Finance, Planning]
Avoid: Marketing, Sales

Results:
- VP of Operations → 96% fit ✓
- Marketing Manager → 25% fit ✗
- Supply Chain Director → 98% fit ✓
```

---

## Output Fields Reference

### ClassifiedProspect Schema

```python
{
    # Basic info
    "email": str,
    "designation": str,
    "company_name": str,

    # Persona Classification
    "primary_persona": PersonaAssignment {
        "persona": str,                    # CXO, Director, Manager, etc.
        "confidence_score": int,           # 0-100
        "rationale": str
    },
    "secondary_persona": Optional[PersonaAssignment],
    
    # Seniority & Function
    "seniority_level": str,               # C-Level, Executive, Director, Manager, IC
    "function": str,                      # Engineering, Marketing, Sales, HR, etc.
    
    # Review Flag
    "needs_review": bool,                 # True if confidence < 60% or suspicious

    # NEW: Campaign Fit Validation
    "campaign_fit_score": int,            # 0-100 how relevant to campaign
    "campaign_fit_valid": bool,           # True if score >= 70
    "campaign_fit_rationale": str         # Why/why not they fit the campaign
}
```

### PersonaClassifierInput Schema

```python
{
    # Existing
    "cleaned_prospects": List[Dict],
    "campaign_type": str,
    "target_personas": List[str],

    # NEW: Campaign Context
    "target_industry": str,               # e.g., "K-12 Education"
    "target_functions": List[str]         # e.g., ["Curriculum", "Instruction", "EdTech"]
}
```

---

## Integration Points

### Data Flow

```
Raw Prospects
    ↓
[Data Quality Agent]
    ↓
Cleaned Prospects + Campaign Context
    ↓
[Persona Classifier Agent] ← NEW: Campaign-Aware Bifurcation
    ↓
Classified + Fit-Validated Prospects
    ├─ Tier 1 (High Fit) → Message Strategy Agent
    ├─ Tier 2 (Medium Fit) → Educational nurture sequence
    └─ Tier 3 (Low Fit) → Archive or separate handling
```

### Calling the Agent

**Before (Without Campaign Context):**
```python
output = run_persona_classifier(
    cleaned_prospects=prospects,
    campaign_type='Market Research',
    target_personas=['CXO', 'Director', 'Manager'],
)
```

**Now (With Campaign Context):**
```python
output = run_persona_classifier(
    cleaned_prospects=prospects,
    campaign_type='Market Research',
    target_personas=['CXO', 'Director', 'Manager'],
    target_industry='K-12 Education',                                    # NEW
    target_functions=['Curriculum', 'Instruction', 'EdTech', 'Admin'],   # NEW
)
```

---

## Bifurcation Summary

Agent 1 now answers THREE questions:

1. **WHO is this person?** (Persona + Seniority)
   - VP of Curriculum → Director-level executive

2. **WHAT do they do?** (Function)
   - Education/Curriculum development

3. **ARE THEY RIGHT FOR THIS CAMPAIGN?** (Campaign Fit)
   - K-12 education campaign → 95% fit ✓

Result: Smart segmentation into actionable tiers.

---

## Testing

See `TEST_PERSONA_CLASSIFIER_MOCK.py` for:
- **MODE 1:** 15 generic persona classification tests
- **MODE 2:** 7 K-12 education campaign fit tests

Run:
```bash
cd c:\Users\Vansh\ken-abm-platform
python agents/TEST_PERSONA_CLASSIFIER_MOCK.py
```

Expected output:
- All classifications correct
- Campaign fit scores accurate
- High-fit prospects identified
- Low-fit prospects filtered

---

## Success Criteria

✅ **Agent 1 (Persona Classifier) is APPROVED when:**

1. ✅ Real titles classified correctly (VP → Director)
2. ✅ Fake titles flagged as low confidence
3. ✅ Non-B2B roles handled appropriately
4. ✅ **NEW:** Campaign fit scores accurate (0-100)
5. ✅ **NEW:** High-fit prospects correctly identified
6. ✅ **NEW:** Low-fit prospects correctly filtered
7. ✅ Bifurcation working (Tier 1/2/3 segmentation)
8. ✅ All output fields populated correctly

---

## Next Steps

Once Agent 1 is approved:

1. **Data feeds in:** Raw prospects from sources
2. **Data Quality filters:** Duplicates, invalid emails
3. **Persona Classifier bifurcates:** 3 tiers by campaign fit
4. **Tiers routed differently:**
   - Tier 1 → Message Strategy + Email/WhatsApp copy
   - Tier 2 → Educational nurture sequence
   - Tier 3 → Archive/separate handling

Then: Build Agent 2 (Message Strategy) using same pattern.
