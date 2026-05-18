# Persona Segmentation Guide — Complete Breakdown

**This shows EXACTLY how the Persona Classifier Agent segments all leads.**

---

## Overview: 5 Buyer Personas

The agent classifies all prospects into ONE of these 5 segments:

```
┌─────────────────────────────────────────────────┐
│         BUYER PERSONA HIERARCHY                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  1. CXO (C-Level Executive)                     │
│     └─ CEO, CTO, CFO, CMO, COO, CHRO           │
│                                                 │
│  2. DIRECTOR (Department Leader)                │
│     └─ Director, VP, SVP, EVP, Head of         │
│                                                 │
│  3. MANAGER (Team Lead)                         │
│     └─ Manager, Senior Manager, Team Lead      │
│                                                 │
│  4. SPECIALIST (Individual Contributor)         │
│     └─ Engineer, Analyst, Specialist, Architect│
│                                                 │
│  5. UNKNOWN (Unclassifiable)                    │
│     └─ Fake titles, non-B2B, ambiguous         │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## Detailed Persona Breakdown

### 1. CXO (C-Level Executive)

**What:** Chief-level executives with company-wide authority  
**Seniority:** C-Level (Highest)  
**Decision Authority:** Strategic, enterprise-wide decisions  
**Buying Power:** Highest — can approve large budgets  
**Risk:** Lower volume, longer sales cycles

#### Titles That Map to CXO:
```
- CEO / Chief Executive Officer
- CTO / Chief Technology Officer
- CFO / Chief Financial Officer
- CMO / Chief Marketing Officer
- COO / Chief Operating Officer
- CHRO / Chief Human Resources Officer
- Chief of Staff
- President (of company)
- Founder (of company)
```

#### Function Mapping:
```
CEO function → CXO persona ✓
CTO function → CXO persona ✓
CFO function → CXO persona ✓
CMO function → CXO persona ✓
COO function → CXO persona ✓
```

#### Decision-Making Profile:
- Makes strategic decisions for entire company
- Controls budget allocation
- Cares about: ROI, competitive advantage, board-level impact
- Sales cycle: 3-6+ months
- Deal size: Typically $100K+

#### Example Classifications:

**Real Title:**
```
Input: "Chief Technology Officer"
Claude Analysis: ✓ "Chief Technology Officer is a C-level executive. 
Authority over entire technology strategy. High seniority."
Output: {
  "persona": "CXO",
  "confidence_score": 98,
  "needs_review": false
}
```

**Fake Title (Still Flagged):**
```
Input: "CEO of my life"
Claude Analysis: ✗ "This is a joke title, not legitimate."
Output: {
  "persona": "CXO",  // or Unknown
  "confidence_score": 5,
  "needs_review": true  // ← FLAGGED
}
```

---

### 2. DIRECTOR (Department Leader)

**What:** Department or division leaders with team authority  
**Seniority:** Director, VP, SVP, EVP (executive level)  
**Decision Authority:** Department-level, can influence C-suite  
**Buying Power:** Medium-High — budget approval within department  
**Risk:** Good balance of volume + authority

#### Titles That Map to DIRECTOR:
```
- Director (any function)
  - Director of Engineering
  - Director of Sales
  - Director of Marketing
  - Director of Operations

- VP (Vice President)
  - VP of Engineering
  - VP of Sales
  - VP of Product
  
- SVP / EVP (Senior/Executive VP)
  - Senior Vice President
  - Executive Vice President
  
- Head of (Department)
  - Head of Engineering
  - Head of Product
  - Head of Marketing
  
- Lead (in some contexts)
  - Engineering Lead (large team)
  - Product Lead
```

#### Function Mapping:
```
VP of Engineering → engineering function → Director persona
Director of Marketing → marketing function → Director persona
Head of Sales → sales function → Director persona
```

#### Decision-Making Profile:
- Makes decisions for their department
- Has budget authority within domain
- Reports to C-level but drives strategy
- Cares about: Team efficiency, team growth, measurable outcomes
- Sales cycle: 2-4 months
- Deal size: Typically $25K-$100K

#### Example Classifications:

**Clear Title:**
```
Input: "VP of Engineering"
Claude Analysis: ✓ "VP indicates Executive seniority. Engineering function. 
Clear match to Director persona."
Output: {
  "persona": "Director",
  "confidence_score": 92,
  "secondary_persona": {
    "persona": "CXO",
    "confidence_score": 70
  },
  "needs_review": false
}
```

**Ambiguous Title:**
```
Input: "Head of Growth"
Claude Analysis: ✓ "Head of suggests director level. Growth is broad 
(could be Sales, Marketing, or Product). Moderate confidence."
Output: {
  "persona": "Director",
  "confidence_score": 65,
  "secondary_persona": {
    "persona": "Manager",
    "confidence_score": 60
  },
  "needs_review": false  // borderline but classifiable
}
```

---

### 3. MANAGER (Team Lead)

**What:** Individual team leaders managing people but not departments  
**Seniority:** Manager, Senior Manager, Team Lead  
**Decision Authority:** Team-level decisions, influences department  
**Buying Power:** Medium — budget for their team only  
**Risk:** Highest volume, but need manager-level messaging

#### Titles That Map to MANAGER:
```
- Manager (any function)
  - Marketing Manager
  - Sales Manager
  - Engineering Manager
  - Product Manager
  - Operations Manager
  
- Senior Manager
  - Senior Marketing Manager
  - Senior Product Manager
  
- Team Lead
  - Engineering Team Lead
  - Sales Team Lead
  
- Supervisor
  - Sales Supervisor
  - Operations Supervisor
```

#### Function Mapping:
```
Marketing Manager → marketing function → Manager persona
Sales Manager → sales function → Manager persona
Product Manager → product function → Manager persona
```

#### Decision-Making Profile:
- Makes decisions for their team (5-20 people typically)
- Can influence department but not set strategy
- Cares about: Team productivity, process improvement, quick wins
- Sales cycle: 1-2 months
- Deal size: Typically $5K-$25K

#### Example Classifications:

**Clear Title:**
```
Input: "Marketing Manager"
Claude Analysis: ✓ "Manager title indicates management level. 
Marketing function. Clear match to Manager persona."
Output: {
  "persona": "Manager",
  "confidence_score": 88,
  "secondary_persona": {
    "persona": "Director",
    "confidence_score": 68
  },
  "needs_review": false
}
```

**Manager → Director:**
```
Input: "Senior Manager, Product Development"
Claude Analysis: ✓ "Senior Manager can bridge to Director level 
depending on company. Product function. Moderate-high confidence."
Output: {
  "persona": "Manager",
  "confidence_score": 75,
  "secondary_persona": {
    "persona": "Director",
    "confidence_score": 70
  },
  "needs_review": false
}
```

---

### 4. SPECIALIST (Individual Contributor)

**What:** Individual contributors (no direct reports)  
**Seniority:** Specialist, Analyst, Engineer, Architect  
**Decision Authority:** Influences decisions within their domain  
**Buying Power:** Low — research/evaluation role, not decision-makers  
**Risk:** Hard to convert, influence chains unclear

#### Titles That Map to SPECIALIST:
```
- Engineer (any type)
  - Software Engineer
  - DevOps Engineer
  - Data Engineer
  - Solutions Engineer
  
- Analyst
  - Data Analyst
  - Business Analyst
  - Security Analyst
  
- Specialist
  - Marketing Specialist
  - Sales Specialist
  - Security Specialist
  
- Architect
  - Solutions Architect
  - Enterprise Architect
  - Cloud Architect
  
- Coordinator
  - Marketing Coordinator
  - Operations Coordinator
```

#### Function Mapping:
```
Software Engineer → engineering function → Specialist persona
Data Analyst → operations function → Specialist persona
Marketing Specialist → marketing function → Specialist persona
```

#### Decision-Making Profile:
- Influences but doesn't decide
- Usually researches solutions
- Reports to Manager/Director
- Cares about: Tool efficiency, skill development, solving problems
- Sales cycle: 3-6 weeks (just research phase)
- Deal size: Typically $0-$5K (research budget only)

#### Example Classifications:

**Clear Title:**
```
Input: "Senior Software Engineer"
Claude Analysis: ✓ "Engineer title indicates IC level. 
Engineering function. Clear match to Specialist persona."
Output: {
  "persona": "Specialist",
  "confidence_score": 90,
  "secondary_persona": null,
  "needs_review": false
}
```

**Ambiguous IC:**
```
Input: "Technical Lead"
Claude Analysis: ✓ "Technical Lead could be IC with mentoring 
or low-level manager. Ambiguous but likely IC."
Output: {
  "persona": "Specialist",
  "confidence_score": 60,
  "secondary_persona": {
    "persona": "Manager",
    "confidence_score": 55
  },
  "needs_review": false  // borderline
}
```

---

### 5. UNKNOWN (Unclassifiable)

**What:** Prospects that don't fit standard B2B profiles  
**Seniority:** Cannot determine  
**Decision Authority:** Unclear or non-existent  
**Buying Power:** Unknown (probably low/none)  
**Risk:** Don't contact without manual review

#### Cases That Map to UNKNOWN:

**Fake/Joke Titles:**
```
- "CEO of my life"
- "VP of Vibes"
- "Chief Awesome Officer"
- "Ninja Developer" (too vague)
- "Rock Star Marketer" (humorous, not real)
```

**Non-B2B Roles:**
```
- "Head Chef" (hospitality)
- "Flight Attendant"
- "Elementary School Teacher"
- "Hospital Nurse"
- "Retail Manager" (if consumer retail, not B2B)
```

**Completely Ambiguous:**
```
- "Executive" (which kind?)
- "Consultant" (who do they work for?)
- "Freelancer" (for which industry?)
- "Contractor" (unclear scope)
```

**Suspicious Patterns:**
```
- Job title is URL/link: "http://linkedin.com/in/john"
- Job title is number/symbol: "12345" or "***"
- Job title is single letter: "a" or "B"
- Job title is obviously fake test data: "Test User"
```

#### Decision-Making Profile:
- Do NOT contact without manual review
- Confidence < 50% (usually < 40%)
- Needs human verification
- Could be fake lead, data error, or non-target industry

#### Example Classifications:

**Fake Title:**
```
Input: "CEO of my life"
Claude Analysis: ✗ "This is clearly a joke title, not a legitimate 
executive position. Fake or spam lead."
Output: {
  "persona": "CXO",  // or "Unknown"
  "confidence_score": 8,
  "needs_review": true,  // ← FLAGGED
  "rationale": "Appears to be a fake/humorous title. Not a legitimate buyer."
}
```

**Non-B2B Role:**
```
Input: "Head Chef at Restaurant XYZ"
Claude Analysis: ✗ "Head Chef is a hospitality/food service role, 
not a B2B decision-maker. Likely not relevant for our B2B solution."
Output: {
  "persona": "Unknown",
  "confidence_score": 15,
  "needs_review": true,  // ← FLAGGED
  "rationale": "Hospitality role, not a typical B2B buyer. Recommend skipping."
}
```

**Suspicious Data:**
```
Input: "test user" or "123" or "***"
Claude Analysis: ✗ "This looks like test data, not a real prospect."
Output: {
  "persona": "Unknown",
  "confidence_score": 2,
  "needs_review": true,  // ← FLAGGED
  "rationale": "Appears to be test/placeholder data. Validate data quality."
}
```

---

## Segmentation Summary Table

| Persona | Seniority | Function | Confidence | Decision Authority | Deal Size | Sales Cycle |
|---|---|---|---|---|---|---|
| **CXO** | C-Level | Strategic | 90-100% | Company-wide | $100K+ | 3-6+ mo |
| **Director** | Exec/Dir | Department | 80-95% | Department | $25K-$100K | 2-4 mo |
| **Manager** | Manager | Team | 70-90% | Team + influence | $5K-$25K | 1-2 mo |
| **Specialist** | IC | Domain | 60-85% | Research/influence | $0-$5K | 3-6 wk |
| **Unknown** | N/A | N/A | <50% | None/unclear | $0 (skip) | Don't contact |

---

## How Prospects Flow Through Segmentation

```
PROSPECT INPUT
    ↓
Designation: "VP of Engineering"
Company: "TechCorp Inc"
    ↓
┌─────────────────────────────────────┐
│ CLAUDE CLI CLASSIFICATION           │
│                                     │
│ 1. Parse title: "VP of Engineering" │
│ 2. Analyze seniority: Executive     │
│ 3. Identify function: Engineering   │
│ 4. Check confidence alignment       │
│ 5. Assign persona + confidence      │
└─────────────────────────────────────┘
    ↓
OUTPUT SEGMENT: DIRECTOR
  - Persona: "Director"
  - Confidence: 92%
  - Secondary: "CXO" (70%)
  - needs_review: false
    ↓
EXPECTED BEHAVIOR:
  → High-priority outreach
  → Director-level messaging
  → 2-4 month sales cycle
  → $25K-$100K deal expected
```

---

## Real-World Examples by Segment

### CXO Segment (Act Now - High Priority)
```
John Smith, CEO of TechCorp Inc
  → Persona: CXO (98% confidence)
  → Messaging: Strategic impact, competitive advantage
  → Approach: Executive relationship building
  → Timeline: 3-6 months
  → Budget: $100K+

Sarah Johnson, CTO at InnovateTech
  → Persona: CXO (95% confidence)
  → Messaging: Technology roadmap alignment
  → Approach: Technical + strategic
  → Timeline: 4-6 months
  → Budget: $50K-$200K
```

### Director Segment (Act Soon - Medium Priority)
```
Mike Chen, VP of Sales at SalesForce
  → Persona: Director (88% confidence)
  → Secondary: CXO (70%)
  → Messaging: Team efficiency, quota achievement
  → Approach: Director + peer relationship
  → Timeline: 2-4 months
  → Budget: $25K-$100K

Lisa Park, Director of Marketing at MarketCo
  → Persona: Director (85% confidence)
  → Secondary: Manager (65%)
  → Messaging: Campaign effectiveness, ROI
  → Approach: Professional, results-driven
  → Timeline: 2-3 months
  → Budget: $20K-$75K
```

### Manager Segment (Nurture - Medium-Low Priority)
```
James Wilson, Marketing Manager at ContentCo
  → Persona: Manager (87% confidence)
  → Secondary: Director (68%)
  → Messaging: Team productivity, quick wins
  → Approach: Practical, implementation-focused
  → Timeline: 1-2 months
  → Budget: $5K-$25K

Rachel Davis, Product Manager at AppCorp
  → Persona: Manager (82% confidence)
  → Secondary: Director (72%)
  → Messaging: Feature delivery, team collaboration
  → Approach: Solution-oriented
  → Timeline: 1-3 months
  → Budget: $10K-$30K
```

### Specialist Segment (Long-Term Nurture - Low Priority)
```
Alex Rodriguez, Senior Software Engineer at DevCorp
  → Persona: Specialist (91% confidence)
  → Messaging: Developer experience, productivity tools
  → Approach: Technical, hands-on
  → Timeline: 3-6 weeks (research only)
  → Budget: $0-$5K (research phase)

Emma Taylor, Data Analyst at AnalyticsCo
  → Persona: Specialist (85% confidence)
  → Messaging: Data insights, tool efficiency
  → Approach: Technical + skill development
  → Timeline: 3-8 weeks
  → Budget: $0-$3K
```

### Unknown Segment (SKIP - High Priority to Filter)
```
"CEO of my life"
  → Persona: Unknown (5% confidence)
  → needs_review: TRUE ← FLAGGED FOR DELETION
  → Action: Do not contact, remove from list

"Head Chef at Restaurant ABC"
  → Persona: Unknown (12% confidence)
  → needs_review: TRUE ← FLAGGED
  → Action: Non-B2B, remove from list

"Test User 123"
  → Persona: Unknown (2% confidence)
  → needs_review: TRUE ← FLAGGED
  → Action: Data quality issue, remove
```

---

## How to Use Segmentation in Campaigns

### By Segment - Different Outreach:

**CXO Segment:**
- ✅ CEO/CTO/CFO outreach
- ✅ C-level messaging (strategic, ROI, competitive)
- ✅ 3-6 month nurture
- ✅ High-touch, relationship-based
- Budget: Prepare for $100K+ deals

**Director Segment:**
- ✅ VP/Director outreach
- ✅ Department-level messaging (efficiency, outcomes)
- ✅ 2-4 month nurture
- ✅ Medium-touch, professional
- Budget: Prepare for $25K-$100K deals

**Manager Segment:**
- ✅ Manager/Lead outreach
- ✅ Team-level messaging (quick wins, process)
- ✅ 1-2 month nurture
- ✅ Efficient, scalable
- Budget: Prepare for $5K-$25K deals

**Specialist Segment:**
- ✅ Technical buyer outreach
- ✅ Solution/tool messaging (productivity, ease)
- ✅ 3-6 week research support
- ✅ Hands-on, tutorial-based
- Budget: These usually don't buy alone

**Unknown Segment:**
- ❌ DO NOT OUTREACH
- ✅ Flag for manual review
- ✅ Clean data quality issues
- ✅ Remove fake/test data
- Budget: $0 (filter cost)

---

## Confidence Scoring by Segment

```
CXO PERSONA:
  ✓ CEO/CTO/CFO/CMO/COO/CHRO → 95-100%
  ✓ Chief of Staff → 85-95%
  ✓ President (company) → 90-95%
  ? President (other org) → 60-80% (ambiguous)
  ✗ "CEO of my life" → 5-15% (fake)

DIRECTOR PERSONA:
  ✓ VP of X → 90-98%
  ✓ Director of X → 90-98%
  ✓ Head of X → 85-95%
  ✓ SVP/EVP → 95-100%
  ? Senior Manager of X → 70-85% (could be Manager)
  ? Lead (large org) → 60-75% (could be Manager or Director)
  ✗ "VP of Vibes" → 10-20% (fake)

MANAGER PERSONA:
  ✓ Manager of X → 85-95%
  ✓ Senior Manager of X → 80-90%
  ✓ Team Lead of X → 80-90%
  ? Lead in startup → 60-75% (could be Director-equivalent)
  ? Product Manager → 70-85% (sometimes director-level)
  ✗ "Manager" (too generic) → 50-70%

SPECIALIST PERSONA:
  ✓ Engineer, Analyst, Architect → 85-95%
  ✓ Specialist of X → 85-95%
  ✓ Senior Engineer/Analyst → 80-90%
  ? Technical Lead → 60-75% (could be Manager)
  ? Coordinator → 70-85%
  ✗ "Ninja Developer" → 20-40% (too vague)

UNKNOWN PERSONA:
  Fake titles → 0-20%
  Non-B2B roles → 10-30%
  Test data → 0-10%
  Completely ambiguous → 20-50%
```

---

## Summary: Persona Segmentation

✅ **5 clear buyer segments** — CXO, Director, Manager, Specialist, Unknown  
✅ **Different messaging per segment** — Tailored to decision authority  
✅ **Confidence scoring** — Know when to flag for manual review  
✅ **Deal size expectations** — CXO = $100K+, Director = $25K-$100K, etc.  
✅ **Sales cycle timing** — CXO = 3-6 mo, Director = 2-4 mo, Manager = 1-2 mo  
✅ **Fake/spam filtering** — Unknown segment flags suspicious data  

**This is how the agent segments your leads into actionable categories.**

