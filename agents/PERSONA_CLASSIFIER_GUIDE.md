# Persona Classifier Agent — Complete Integration Guide

**Status:** ✅ Production Ready  
**Built by:** User  
**For Integration:** Your Teammate  
**Monday Delivery:** ✅ Complete

---

## What This Agent Does

Maps prospect records to buyer personas based on job designation, function, and seniority level.

**Input:** List of cleaned prospects + target personas + campaign type  
**Output:** Classified prospects with persona assignments + confidence scores + statistics

---

## Quick Start (For Your Teammate)

### 1. Import and Use

```python
from agents.persona_classifier_agent import run_persona_classifier
from agents.schemas import PersonaClassifierInput, PersonaClassifierOutput

# Define input
input_data = PersonaClassifierInput(
    cleaned_prospects=[
        {
            "email": "john@company.com",
            "designation": "VP of Engineering",
            "company_name": "TechCorp Inc",
            "company_size": "500-1000",
            "industry": "Software",
        },
        {
            "email": "jane@company.com",
            "designation": "Marketing Manager",
            "company_name": "TechCorp Inc",
            "company_size": "500-1000",
            "industry": "Software",
        },
    ],
    campaign_type="Market Research",
    target_personas=["CXO", "Director", "Manager"],
)

# Run agent
output = run_persona_classifier(
    cleaned_prospects=input_data.cleaned_prospects,
    campaign_type=input_data.campaign_type,
    target_personas=input_data.target_personas,
)

# Access results
for prospect in output.classified_prospects:
    print(f"{prospect.email}: {prospect.primary_persona.persona} ({prospect.primary_persona.confidence_score}%)")

print(f"\nStatistics:")
print(f"  Average Confidence: {output.average_confidence}%")
print(f"  Low Confidence (<60): {output.low_confidence_count}")
print(f"  Unclassifiable: {output.unclassifiable_count}")
print(f"  Persona Distribution: {output.persona_distribution}")
```

### 2. Expected Output

```python
PersonaClassifierOutput(
    classified_prospects=[
        ClassifiedProspect(
            email="john@company.com",
            designation="VP of Engineering",
            company_name="TechCorp Inc",
            primary_persona=PersonaAssignment(
                persona="Director",
                confidence_score=92,
                rationale="VP title + Engineering function maps to Director level.",
            ),
            secondary_persona=PersonaAssignment(
                persona="CXO",
                confidence_score=70,
                rationale="VP often influences C-level decisions.",
            ),
            seniority_level="Executive",
            function="engineering",
            needs_review=False,
        ),
        # ... more prospects
    ],
    persona_distribution={"Director": 1, "Manager": 1},
    average_confidence=90,
    low_confidence_count=0,
    unclassifiable_count=0,
    notes="Classified 2 prospects...",
)
```

---

## How the Classification Works

### Seniority Extraction

| Level | Titles | Keywords | Level Code |
|-------|--------|----------|-----------|
| **C-Level** | CEO, CTO, CFO, CMO, COO, CHRO, Chief | Chief, President, Founder | 5 |
| **Executive** | EVP, SVP, VP | Executive, VP of | 4 |
| **Director** | Director, Head of | Director of, Head of Department | 3 |
| **Manager** | Manager, Senior Manager, Team Lead | Manager, Team Lead, Lead | 2 |
| **Individual Contributor** | Specialist, Analyst, Engineer, Architect | Specialist, Analyst, Engineer | 1 |

### Function Extraction

```python
C-Level Functions:
  - CEO, CTO, CFO, CMO, COO → CXO persona

Marketing Functions:
  - Marketing, Demand Generation, Product Marketing → Marketing persona

Sales Functions:
  - Sales, Account Executive, Sales Development → Sales persona

Operations Functions:
  - Operations, Finance, Procurement → Operations persona

Engineering Functions:
  - Engineering, Product, IT, Infrastructure → Engineering persona

Strategy Functions:
  - Strategy, Business Development → Business Development persona
```

### Confidence Scoring

Confidence is calculated from:
1. **Seniority alignment** with persona (40%)
2. **Function alignment** with persona (40%)
3. **Exact title match** boost (20%)

```python
Example:
  Designation: "VP of Engineering"
  → Seniority: Executive (95% confidence)
  → Function: Engineering (90% confidence)
  → Seniority matches Director persona ✓
  → Function matches Engineering ✓
  → Primary: Director (92% confidence)
  → Secondary: CXO (70% confidence)
```

### Review Flags

Prospects flagged for manual review (`needs_review=True`) when:
- Confidence score < 60%
- Ambiguous designation
- No matching function
- Missing seniority indicators

---

## Integration Points

### Into Your Pipeline

**Previous Stage:** Data Quality Agent  
**Your Agent:** Persona Classifier  
**Next Stage:** Message Strategy Agent

```
Data Quality Agent
        ↓
(cleaned_prospects with quality scores)
        ↓
Persona Classifier Agent
        ↓
(classified_prospects with persona assignments)
        ↓
Message Strategy Agent
```

### Data Contract

**Input from Data Quality:**
```python
{
    "email": str,
    "first_name": str,
    "last_name": str,
    "designation": str,          # REQUIRED
    "company_name": str,
    "company_size": str,
    "industry": str,
    "confidence_score": int,     # Quality score (optional)
    "is_duplicate": bool,        # Optional
    "corrections_made": List[str],  # Optional
}
```

**Output to Message Strategy:**
```python
{
    "email": str,
    "designation": str,
    "company_name": str,
    "primary_persona": {
        "persona": str,
        "confidence_score": int,
        "rationale": str,
    },
    "secondary_persona": {  # Optional
        "persona": str,
        "confidence_score": int,
        "rationale": str,
    },
    "seniority_level": str,
    "function": str,
    "needs_review": bool,
}
```

---

## Advanced Usage

### Filter by Confidence

```python
# Get only high-confidence classifications
high_confidence = [
    p for p in output.classified_prospects
    if p.primary_persona.confidence_score >= 80
]

# Get prospects flagged for review
needs_review = [
    p for p in output.classified_prospects
    if p.needs_review
]
```

### Access Statistics

```python
# Overall metrics
avg_confidence = output.average_confidence
low_conf_count = output.low_confidence_count
unclassifiable = output.unclassifiable_count

# Persona distribution
for persona, count in output.persona_distribution.items():
    print(f"{persona}: {count} prospects")

# Quality indicator
quality_pct = (len(output.classified_prospects) / (len(output.classified_prospects) + unclassifiable)) * 100
print(f"Classification success rate: {quality_pct:.1f}%")
```

### Batch Processing

```python
from typing import List

def classify_large_batch(
    prospects: List[Dict],
    campaign_type: str,
    target_personas: List[str],
    batch_size: int = 100,
):
    """Process large prospect lists in batches."""
    all_classified = []
    
    for i in range(0, len(prospects), batch_size):
        batch = prospects[i:i+batch_size]
        output = run_persona_classifier(batch, campaign_type, target_personas)
        all_classified.extend(output.classified_prospects)
    
    return all_classified
```

---

## Customization

### Add Custom Personas

Edit `FUNCTION_TO_PERSONA` dict in `persona_classifier_agent.py`:

```python
FUNCTION_TO_PERSONA = {
    # ... existing entries ...
    "custom_function": ["CustomPersona", "Director"],  # Add your custom
}
```

### Adjust Confidence Thresholds

Edit the `classify_prospect()` function to change how confidence is calculated:

```python
# Currently: <60% = needs_review
# Change to:
needs_review = primary_confidence < 70  # Stricter
```

### Add Seniority Levels

Edit `SENIORITY_LEVELS` dict:

```python
SENIORITY_LEVELS = {
    # ... existing entries ...
    "Partner": {  # New level
        "titles": ["partner", "principal"],
        "keywords": ["partner", "principal"],
        "level": 3.5,
    },
}
```

---

## Error Handling

The agent gracefully handles:
- ✅ Missing designation (skips prospect, counts as unclassifiable)
- ✅ Missing email (skips prospect)
- ✅ Unknown function (defaults to function="Other", lower confidence)
- ✅ No matching target personas (uses first target persona)
- ✅ Empty prospect list (returns empty output with 0 statistics)

```python
# Safe to call even with incomplete data
output = run_persona_classifier(
    cleaned_prospects=[
        {"email": "john@company.com"},  # Missing designation
        {"designation": "VP Engineering"},  # Missing email
        {"email": "valid@company.com", "designation": "CEO"},  # Good
    ],
    campaign_type="Survey",
    target_personas=["CXO", "Director"],
)

# Results: 1 classified, 2 unclassifiable
assert output.unclassifiable_count == 2
assert len(output.classified_prospects) == 1
```

---

## Testing

### Run Unit Tests

```python
# Test with sample prospects
from agents.persona_classifier_agent import run_persona_classifier

test_data = [
    {
        "email": "ceo@company.com",
        "designation": "Chief Executive Officer",
        "company_name": "Company",
    },
    {
        "email": "eng@company.com",
        "designation": "Senior Software Engineer",
        "company_name": "Company",
    },
]

output = run_persona_classifier(test_data, "Survey", ["CXO", "Manager"])

# Assertions
assert len(output.classified_prospects) == 2
assert output.classified_prospects[0].primary_persona.persona == "CXO"
assert output.classified_prospects[0].primary_persona.confidence_score >= 85
assert output.classified_prospects[1].primary_persona.persona == "Manager"
assert output.average_confidence > 70
```

### Validate Output Schema

```python
from agents.schemas import PersonaClassifierOutput

# This validates that output matches schema
output = run_persona_classifier(prospects, campaign_type, target_personas)

# Type hints ensure integration compatibility
def next_stage(output: PersonaClassifierOutput):
    # Your code here
    pass

next_stage(output)  # Type-safe
```

---

## Integration Checklist

When integrating into your pipeline:

- [ ] Import `run_persona_classifier` from this module
- [ ] Provide cleaned prospects from Data Quality Agent
- [ ] Provide target personas from Campaign Planner Agent
- [ ] Provide campaign type from Campaign Plan
- [ ] Handle `needs_review=True` cases (manual approval step?)
- [ ] Log low confidence classifications (>10% of batch)
- [ ] Pass output to Message Strategy Agent
- [ ] Validate output schema matches expectations

---

## Files Included

```
agents/
├── persona_classifier_agent.py          ← Main agent (COMPLETE)
├── registry/
│   └── persona_classifier.json          ← System prompt + config
└── PERSONA_CLASSIFIER_GUIDE.md          ← This file
```

---

## What's Ready for Claude Integration

When you add the Anthropic API:

1. **System Prompt:** Already in `registry/persona_classifier.json`
2. **Tool Definition:** Add tool for `classify_prospect_persona`
3. **Tool Forcing:** Return tool use response with persona assignments
4. **Response Parsing:** Extract persona assignments from tool input
5. **Schema Validation:** Pydantic models validate output

```python
# Future upgrade (with Anthropic SDK):
from anthropic import Anthropic

def run_persona_classifier_with_api(input_data: PersonaClassifierInput):
    config = load_agent_config("persona_classifier")
    client = Anthropic()
    
    response = client.messages.create(
        model=config["model"],
        system=config["system_prompt"],
        tools=config["tools"],  # Tool definition in JSON
        messages=[{"role": "user", "content": f"Classify: {input_data}"}],
    )
    
    # Extract tool use and parse
    tool_use = response.content[0]  # Assuming tool use response
    output_dict = tool_use.input
    
    # Validate with Pydantic
    return PersonaClassifierOutput(**output_dict)
```

---

## Support

**Questions about usage?** Check the examples above or review the docstrings in `persona_classifier_agent.py`.

**Want to customize?** Edit the classification logic in `classify_prospect()` function.

**Integration issues?** Ensure input data matches the schema and call `run_persona_classifier()` with exact parameter names.

---

## Next Agent

Once this is integrated, the **Message Strategy Agent** will take this output and generate messaging strategy based on persona assignments.

**Handoff:** `PersonaClassifierOutput` → `Message Strategy Agent Input`

---

**Built:** Friday  
**Status:** ✅ Ready for Monday Delivery  
**Quality:** Production-Ready, Tested, Documented
