# Message Strategy Agent — Comprehensive Guide (Agent 2)

## Overview

Agent 2 generates **campaign-aware, market-intelligent messaging strategy** for each campaign.

**Key Difference from Logic-Based Approach:**
- NOT generic persona mappings (e.g., "CXO cares about ROI")
- YES deep market analysis (e.g., "In K-12 EdTech, CXOs specifically care about capturing remote-learning shift before competitors lock in partnerships")

Uses Claude CLI to intelligently extract REAL market pain points and map them to persona-specific value propositions.

---

## What Agent 2 Does

**Input:**
- Campaign name, type, offer, industry
- Target personas (CXO, Director, Manager, Specialist)
- Channel mix (email, WhatsApp, LinkedIn)

**Output:**
```json
{
  "messaging_strategy": {
    "campaign_name": "K-12 Learning Solutions 2026",
    "tone": "consultative",
    "key_themes": ["learning outcomes", "EdTech adoption", "remote learning shift"],
    "value_propositions": {
      "CXO": "Strategic framework to capture remote-learning market shift before competitors",
      "Director": "Practical implementation guide for EdTech integration in schools",
      "Manager": "Quick-win improvements to student engagement with EdTech"
    },
    "call_to_action": "Schedule a 20-min call to discuss your EdTech strategy"
  },
  "persona_specific_messages": {
    "CXO": {
      "primary_angle": "Competitive positioning in EdTech shift",
      "pain_points": [
        "Remote learning adoption outpacing internal readiness",
        "Fear of losing students to EdTech-forward schools",
        "Budget constraints for EdTech infrastructure"
      ],
      "value_prop": "Market insights + peer benchmarks to accelerate EdTech positioning"
    },
    "Director": {
      "primary_angle": "Operational efficiency through EdTech",
      "pain_points": [
        "Student engagement declining with traditional methods",
        "Teacher training burden for new platforms",
        "Integration complexity with existing systems"
      ],
      "value_prop": "Implementation roadmap + training guidance to smoothly adopt EdTech"
    }
  },
  "channel_guidance": {
    "email": "Data-driven, lead with trend insight (85% of schools adopting hybrid...). Professional but warm.",
    "whatsapp": "Peer-to-peer tone. Share quick insight (\"3 of 5 schools in your district...\"). Conversational.",
    "linkedin": "Thought leadership angle. Position as EdTech strategist. Share best practices."
  },
  "success_criteria": {
    "email_open_rate": "28-35%",
    "email_click_rate": "6-9%",
    "response_rate": "4-6%",
    "meeting_rate": "1-2%"
  }
}
```

---

## How It Works (Step by Step)

### Step 1: Campaign Context Analysis

Agent 2 receives:
```python
run_message_strategy(
    campaign_name="K-12 Learning Solutions",
    campaign_type="Market Research",
    offer="Research study on EdTech adoption in Indian schools",
    target_industry="K-12 Education",
    target_personas=["CXO", "Director", "Manager"],
    channel_mix=["email", "whatsapp", "linkedin"]
)
```

### Step 2: Claude CLI Deep Dive

Agent 2 calls Claude with detailed prompt:
- "Analyze the K-12 Education market deeply"
- "What are REAL pain points CXOs in Indian schools face?"
- "How does this EdTech research solve their specific pain?"
- "What primary angle resonates with each persona?"

### Step 3: Claude Returns Market-Aware Strategy

Claude analyzes:
1. Industry dynamics (remote learning shift, EdTech adoption rates, peer pressure)
2. Persona-specific pain (CXOs: competitive positioning; Directors: operational integration; Managers: team capability)
3. How the research offer solves EACH pain point specifically
4. Messaging angles tailored to each persona + industry

### Step 4: Integration with Message Series

Agent 2 output feeds into:
- **Message Series Pattern Selection** (Market Research → Claude skill, Survey → logic pattern, etc.)
- **Email Copy Agent** (uses value_prop + pain_points + angle)
- **WhatsApp Copy Agent** (uses channel_guidance for tone)

---

## Real-World Examples

### Campaign 1: K-12 Education Market Research

**Input:**
```
Campaign: K-12 Learning Solutions
Industry: K-12 Education
Offer: Research on EdTech adoption trends
Personas: CXO, Director, Manager
```

**Claude Analysis:**
- Market context: Remote learning is accelerating adoption; schools fear falling behind
- CXO pain: "Competitors adopting EdTech faster; losing enrollment to tech-forward schools"
- Director pain: "Teacher training burden; integration complexity with existing systems"
- Manager pain: "Student engagement declining; need quick wins"

**Output:**

| Persona | Primary Angle | Pain Points | Value Prop |
|---------|---|---|---|
| **CXO** | Competitive positioning in EdTech shift | Fear of falling behind, Budget constraints, Enrollment pressure | Market data + peer benchmarks to accelerate positioning |
| **Director** | Operational efficiency through EdTech | Integration complexity, Teacher readiness, System compatibility | Implementation roadmap + training guide for smooth adoption |
| **Manager** | Team capability & quick wins | Student engagement down, Teacher capability gaps, Time constraints | Quick assessment of EdTech readiness + quick-win recommendations |

---

### Campaign 2: Cold Chain Logistics Competition Benchmarking

**Input:**
```
Campaign: Cold Chain Kings - Thailand
Industry: Temperature Controlled Logistics
Offer: Competitive benchmarking study
Personas: VP Operations, Director of Supply Chain
```

**Claude Analysis:**
- Market context: Utilization fluctuating; cost pressures rising; operators differentiating on efficiency
- VP Ops pain: "Small efficiency differences = big margin impact; don't know if we're competitive"
- Director pain: "Reefer fleet optimization complex; unclear optimal duration mix"

**Output:**

| Persona | Primary Angle | Pain Points | Value Prop |
|---------|---|---|---|
| **VP Operations** | Competitive margin benchmarking | Margin erosion, Uncertainty on peer performance, Cost pressure | Benchmarking shows where you stand vs competitors on cost/efficiency |
| **Director** | Fleet optimization & utilization | Temperature zone complexity, Utilization gaps, Duration mix uncertainty | Industry benchmarks on optimal fleet mix + duration strategy |

---

## Integration Points

### With Agent 1 (Persona Classifier)

Agent 2 uses `campaign_fit_valid` from Agent 1:
- **Tier 1 prospects** (high fit): Get full strategy
- **Tier 2 prospects** (medium fit): Get simplified/educational angle
- **Tier 3 prospects** (low fit): Skip or special handling

### With Message Series Patterns

**Market Research:**
```
run_message_strategy(campaign_type="Market Research", ...)
  ↓
Triggers: Claude skill (abm-linkedin-series)
  ↓
Generates: 3-msg LinkedIn series + ABM Master Doc
```

**Survey:**
```
run_message_strategy(campaign_type="Survey", ...)
  ↓
Triggers: Logic-based 3-message pattern
  ↓
Generates: Credibility-driven message sequence
```

**Competition Benchmarking:**
```
run_message_strategy(campaign_type="Competition Benchmarking", ...)
  ↓
Triggers: Contextual pattern selection (Battery Boom / India EV / Cold Chain style)
  ↓
Generates: Matching message sequence
```

### With Email Copy Agent (Agent 3)

Message Strategy output feeds Email Copy Agent:
```
Email Copy Agent receives:
- value_prop (from persona strategy)
- pain_points (from persona strategy)
- primary_angle (from persona strategy)
- tone (from messaging strategy)
- channel_guidance (email-specific)

Generates: M1, M2, M3, M4 email copy per persona
```

### With WhatsApp Copy Agent (Agent 4)

```
WhatsApp Copy Agent receives:
- Same persona strategy fields
- Channel_guidance (whatsapp-specific)

Generates: M1, M2, M3, M4 WhatsApp messages per persona
```

---

## Testing Agent 2

### Test Scenario 1: K-12 Education Campaign

```python
from agents import run_message_strategy

output = run_message_strategy(
    campaign_name="K-12 Learning Solutions 2026",
    campaign_type="Market Research",
    offer="Research study on EdTech adoption trends in Indian schools",
    target_industry="K-12 Education",
    target_personas=["CXO", "Director", "Manager"],
    channel_mix=["email", "whatsapp", "linkedin"]
)

# Check output
assert output.messaging_strategy["tone"] in ["consultative", "professional", "educational"]
assert len(output.persona_specific_messages) == 3
assert "pain_points" in output.persona_specific_messages["CXO"]
assert "primary_angle" in output.persona_specific_messages["CXO"]
assert "value_prop" in output.persona_specific_messages["CXO"]
```

**Expected Output Structure:**
```
Messaging Strategy:
  Tone: consultative / educational
  Themes: EdTech adoption, Learning outcomes, Remote learning shift
  CTA: Schedule discussion about EdTech strategy
  Success: 28-35% email open, 1-2% meeting rate

Persona Strategies:
  CXO:
    Angle: Competitive positioning in EdTech shift
    Pains: [falling behind, budget, enrollment pressure]
    Value: Market data to accelerate positioning
  Director:
    Angle: Operational efficiency through EdTech
    Pains: [integration complexity, teacher readiness, compatibility]
    Value: Implementation roadmap for smooth adoption
  Manager:
    Angle: Team capability & quick wins
    Pains: [engagement down, capability gaps, time constraints]
    Value: Quick EdTech readiness assessment

Channel Guidance:
  Email: Data-driven, lead with trend insight
  WhatsApp: Peer-to-peer, quick insights, conversational
  LinkedIn: Thought leadership, best practices
```

---

## Success Criteria

✅ **Agent 2 is APPROVED when:**

1. ✅ Analyzes market deeply (not generic)
2. ✅ Extracts REAL pain points per persona (not template)
3. ✅ Pain points are specific to industry + campaign type
4. ✅ Primary angles resonate with personas in that market
5. ✅ Value props solve specific pain points (not generic benefits)
6. ✅ Tone appropriate to campaign type
7. ✅ Channel guidance includes email/WhatsApp/LinkedIn specific rules
8. ✅ Success criteria match campaign type expectations
9. ✅ Integrates with message series patterns correctly
10. ✅ Output structure matches MessageStrategyOutput schema

---

## Next Steps

Once Agent 2 approved:
1. Build Agent 3 (Email Copy Agent) using same Claude CLI pattern
2. Build Agent 4 (WhatsApp Copy Agent)
3. Integrate all agents into orchestrator
4. Test full flow: Prospect → Classification → Strategy → Copy → Approval

---

## Fields Reference

### Messaging Strategy Output

```python
{
    "campaign_name": str,
    "tone": str,                          # consultative, professional, urgent, friendly, educational, exclusive, competitive, personal
    "key_themes": List[str],              # 3-4 themes addressing industry pain points
    "value_propositions": Dict[str, str], # {persona: value_prop}
    "call_to_action": str,                # Specific CTA for campaign type
}
```

### Persona-Specific Messages

```python
{
    "primary_angle": str,      # Messaging hook that resonates with THIS persona in THIS market
    "pain_points": List[str],  # 2-4 REAL pain points THIS persona faces
    "value_prop": str,         # How offer solves THIS pain point specifically
}
```

### Channel Guidance

```python
{
    "email": str,       # Professional, data-driven tone rules
    "whatsapp": str,    # Conversational, warm tone rules
    "linkedin": str,    # Thought leadership, professional tone rules
}
```

### Success Criteria

```python
{
    "email_open_rate": "28-35%",
    "email_click_rate": "6-9%",
    "response_rate": "4-6%",
    "meeting_rate": "1-2%",
}
```

---

## Troubleshooting

### Error: Claude CLI not found

```
RuntimeError: Claude CLI not found. Install with: npm install -g @anthropic-ai/claude
```

**Fix:**
```bash
npm install -g @anthropic-ai/claude
claude login
```

### Empty/Null Pain Points from Claude

Claude returned generic pain points instead of market-specific ones.

**Cause:** Prompt may not have enough industry context.

**Fix:** Ensure `offer` and `target_industry` are detailed enough for Claude to analyze.

### Pain Points Don't Match Campaign Type

Pain points are generic (e.g., "revenue growth") instead of campaign-specific (e.g., "need data on remote-learning adoption to compete").

**Cause:** Campaign context not specific enough.

**Fix:** Include campaign offer specifics in the input (e.g., "Research on EdTech adoption trends" not just "research").

---
