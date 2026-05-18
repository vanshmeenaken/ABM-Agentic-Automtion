# Message Strategy Agent — Complete Integration Guide

**Status:** ✅ Production Ready  
**Built by:** User  
**For Integration:** Your Teammate  
**Monday Delivery:** ✅ Complete

---

## What This Agent Does

Maps campaign type + industry + personas to comprehensive messaging strategy (tone, themes, value propositions, CTA, success metrics).

**Input:** Campaign details + target personas + channel mix  
**Output:** Messaging strategy with tone + themes + persona value props + CTA + success criteria

---

## Quick Start (For Your Teammate)

### 1. Import and Use

```python
from agents.message_strategy_agent import run_message_strategy
from agents.schemas import MessageStrategyOutput

# Define input
output = run_message_strategy(
    campaign_name="Tech Market Research Initiative",
    campaign_type="Market Research",
    offer="Comprehensive market research report on AI/ML adoption",
    target_personas=["CXO", "Director"],
    target_industry="Technology",
    channel_mix=["email", "whatsapp", "linkedin"],
)

# Access results
print(f"Tone: {output['messaging_strategy']['tone']}")
print(f"Themes: {output['messaging_strategy']['key_themes']}")
print(f"CTA: {output['messaging_strategy']['call_to_action']}")

for persona, value_prop in output['messaging_strategy']['value_propositions'].items():
    print(f"{persona}: {value_prop}")
```

### 2. Expected Output

```python
{
    "messaging_strategy": {
        "campaign_name": "Tech Market Research Initiative",
        "tone": "consultative",
        "key_themes": ["AI/ML adoption", "digital transformation", "competitive advantage"],
        "value_propositions": {
            "CXO": "Strategic insights on AI/ML ROI and competitive market positioning",
            "Director": "Practical guidance on implementing AI/ML initiatives within teams"
        },
        "call_to_action": "Access the full research findings"
    },
    "persona_specific_messages": {
        "CXO": {
            "primary_angle": "Strategic advantage",
            "pain_points": "Revenue growth, market position, shareholder value",
            "value_prop": "Strategic insights..."
        },
        "Director": {
            "primary_angle": "Team success",
            "pain_points": "Team productivity, budget optimization, performance metrics",
            "value_prop": "Practical guidance..."
        }
    },
    "channel_guidance": {
        "email": "Formal, consultative tone. Lead with value proposition...",
        "whatsapp": "Conversational, short messages. Warm and personal...",
        "linkedin": "Professional yet approachable. Highlight thought leadership..."
    },
    "success_criteria": {
        "email_open_rate": "25-30%",
        "email_click_rate": "5-7%",
        "response_rate": "3-5%",
        "conversion_rate": "1-2%"
    },
    "notes": "Strategy generated for Market Research campaign..."
}
```

---

## How Strategy Generation Works

### Step 1: Tone Selection

Campaign type determines base tone:

| Campaign Type | Tone | Rationale |
|---|---|---|
| **Market Research** | consultative | Advisory, question-focused |
| **Survey** | friendly | Approachable, low friction |
| **Consulting** | professional | Credible, results-driven |
| **Expert Network** | exclusive | Premium, curated access |
| **Webinar** | educational | Teaching, thought leadership |
| **Report Sales** | thought-leading | Authoritative, insights-based |
| **Competition Benchmarking** | competitive | FOMO, competitive advantage |
| **Account Reactivation** | personal | Warm, relationship-focused |

Tone shapes copy style, language choice, opening hook.

### Step 2: Theme Generation

Industry determines key themes addressing pain points:

| Industry | Themes |
|---|---|
| **Technology** | innovation, digital transformation, scalability, speed-to-market |
| **Finance** | risk management, compliance, ROI optimization, growth |
| **Healthcare** | patient outcomes, regulatory compliance, operational efficiency |
| **Manufacturing** | productivity, supply chain resilience, quality control |
| **Retail** | customer experience, conversion optimization, loyalty |
| **Pharmaceuticals** | clinical efficacy, regulatory pathways, market access |
| **Insurance** | underwriting efficiency, risk assessment, customer retention |
| **Telecom** | network optimization, customer acquisition, cost reduction |

Themes weave through email subject lines, body copy, value props.

### Step 3: Persona Value Propositions

Each persona gets role-specific value prop:

| Persona | Focus | Messaging Angle |
|---|---|---|
| **CXO** | Strategic impact, ROI, competitive advantage | Business transformation, strategic advantage |
| **Director** | Team efficiency, accountability, measurable outcomes | Team success, operational excellence |
| **Manager** | Process improvement, metrics, team empowerment | Practical solutions, quick wins |
| **Specialist** | Tool efficiency, task automation, skill development | Making their job easier |
| **Individual Contributor** | Day-to-day efficiency, skill building | Personal productivity, career growth |

Example:
- *CXO:* "Strategic insights on AI/ML ROI and market positioning"
- *Director:* "Practical guidance on implementing AI/ML within teams"
- *Manager:* "Process improvements and team productivity metrics"

### Step 4: Call-to-Action

Campaign-specific CTA aligned with offer:

| Campaign Type | CTA |
|---|---|
| Market Research | "Access the research findings" |
| Survey | "Participate in our quick survey" |
| Consulting | "Schedule a brief consultation" |
| Expert Network | "Get introduced to industry experts" |
| Webinar | "Register for the webinar" |
| Report Sales | "Download the full report" |

### Step 5: Success Criteria

Realistic metrics by campaign type and channel:

**Market Research** (25-30% open, 5-7% click, 3-5% response)  
**Survey** (20-25% open, 8-12% click, 5-10% response)  
**Consulting** (22-28% open, 6-10% click, 4-6% response)  
**Expert Network** (25-35% open, 7-12% click, 5-8% response)

### Step 6: Channel Guidance

Tone + messaging adapted per channel:

**Email:** Formal, structured. Lead with value. Include CTA. Personalize.  
**WhatsApp:** Conversational, brief. Build relationship first. Warm.  
**LinkedIn:** Professional + approachable. Thought leadership. Invite discussion.

---

## Integration Points

### Into Your Pipeline

**Previous Stage:** Orchestrator (campaign details from user input)  
**Your Agent:** Message Strategy  
**Next Stage:** Email Copy Agent + WhatsApp Copy Agent

```
Orchestrator (Campaign Details)
        ↓
Message Strategy Agent
        ↓
(messaging_strategy with tone, themes, value props, CTA)
        ↓
Email Copy Agent + WhatsApp Copy Agent
        ↓
(tailored copy for each prospect + persona)
```

### Data Contract

**Input from Orchestrator:**
```python
{
    "campaign_name": str,
    "campaign_type": str,          # Market Research, Survey, etc.
    "offer": str,
    "target_personas": List[str],   # ["CXO", "Director", "Manager"]
    "target_industry": str,
    "channel_mix": List[str],       # ["email", "whatsapp", "linkedin"]
}
```

**Output to Copy Agents:**
```python
{
    "messaging_strategy": {
        "tone": str,
        "key_themes": List[str],
        "value_propositions": Dict[str, str],  # {persona: value_prop}
        "call_to_action": str,
    },
    "persona_specific_messages": Dict,
    "channel_guidance": Dict[str, str],
    "success_criteria": Dict[str, str],
    "notes": str,
}
```

---

## Advanced Usage

### Override Default Tone

```python
# Strategy defaults to "professional" for unknown campaign_type
# To use different tone, modify output before passing to copy agents:
output = run_message_strategy(...)
output['messaging_strategy']['tone'] = 'urgent'  # Override
```

### Filter by Channel

```python
# Get only email guidance
email_guidance = output['channel_guidance'].get('email')

# Build email copy with this guidance
email_copy = generate_email_copy(
    persona=persona,
    message_strategy=output,
    channel='email',
)
```

### Access Persona Messaging Framework

```python
# Get detailed framework for each persona
for persona, framework in output['persona_specific_messages'].items():
    primary_angle = framework['primary_angle']
    pain_points = framework['pain_points_to_address']
    value_prop = framework['value_prop']
    
    print(f"{persona}: {primary_angle}")
    print(f"  Pain Points: {pain_points}")
    print(f"  Value Prop: {value_prop}")
```

### Batch Processing Campaigns

```python
campaigns = [
    {"campaign_name": "Campaign 1", "campaign_type": "Market Research", ...},
    {"campaign_name": "Campaign 2", "campaign_type": "Webinar", ...},
]

strategies = []
for campaign in campaigns:
    strategy = run_message_strategy(**campaign)
    strategies.append(strategy)
```

---

## Customization

### Add Custom Campaign Type

Edit `CAMPAIGN_TYPE_TO_TONE` dict in `message_strategy_agent.py`:

```python
CAMPAIGN_TYPE_TO_TONE = {
    # ... existing entries ...
    "Custom Campaign": "urgent",  # Add your custom type
}

CAMPAIGN_TYPE_TO_CTA = {
    # ... existing entries ...
    "Custom Campaign": "Take action now",
}
```

### Add Custom Industry

Edit `INDUSTRY_TO_THEMES` dict:

```python
INDUSTRY_TO_THEMES = {
    # ... existing entries ...
    "Legal Services": ["risk mitigation", "compliance", "efficiency", "client retention"],
}
```

### Adjust Tone Characteristics

Edit `TONE_CHARACTERISTICS` dict to change how tone is described:

```python
TONE_CHARACTERISTICS = {
    "your_custom_tone": {
        "keywords": ["keyword1", "keyword2", "keyword3"],
        "email_style": "Description of email style",
    }
}
```

### Customize Success Metrics

Edit `CAMPAIGN_TYPE_TO_SUCCESS_TARGETS` dict:

```python
CAMPAIGN_TYPE_TO_SUCCESS_TARGETS = {
    # ... existing entries ...
    "Your Campaign": {
        "email_open_rate": "30-35%",
        "email_click_rate": "10%",
        "response_rate": "5%",
        "conversion_rate": "2-3%",
    },
}
```

### Add Persona

Edit `PERSONA_VALUE_PROPOSITIONS` dict:

```python
PERSONA_VALUE_PROPOSITIONS = {
    # ... existing entries ...
    "VP of Sales": {
        "focus": "Revenue generation, quota attainment",
        "pain_points": "Pipeline velocity, team performance",
        "messaging_angle": "Revenue acceleration and quota success",
    },
}
```

---

## Error Handling

Agent gracefully handles:
- ✅ Unknown campaign_type (defaults to "professional" tone)
- ✅ Unknown industry (defaults to generic themes: innovation, growth, efficiency)
- ✅ Empty personas list (returns empty value_propositions)
- ✅ Missing channel_mix (returns empty channel_guidance)

```python
# Safe to call even with minimal data
output = run_message_strategy(
    campaign_name="Test Campaign",
    campaign_type="Unknown Type",  # Falls back to professional
    offer="Test offer",
    target_personas=[],  # Empty - returns empty value_propositions
    target_industry="Unknown Industry",  # Falls back to generic themes
    channel_mix=[],  # Empty - returns empty channel_guidance
)

# Results: Uses defaults gracefully, no errors
assert output['messaging_strategy']['tone'] == 'professional'
assert output['messaging_strategy']['key_themes'] == ["innovation", "growth", "efficiency"]
```

---

## Testing

### Run Unit Tests

```python
from agents.message_strategy_agent import run_message_strategy

# Test with sample campaign
output = run_message_strategy(
    campaign_name="Tech Research",
    campaign_type="Market Research",
    offer="AI/ML insights",
    target_personas=["CXO", "Director"],
    target_industry="Technology",
    channel_mix=["email", "whatsapp"],
)

# Assertions
assert output['messaging_strategy']['tone'] == 'consultative'
assert len(output['messaging_strategy']['key_themes']) >= 3
assert 'CXO' in output['messaging_strategy']['value_propositions']
assert 'Director' in output['messaging_strategy']['value_propositions']
assert output['messaging_strategy']['call_to_action'] is not None
assert 'email' in output['channel_guidance']
assert 'whatsapp' in output['channel_guidance']
assert output['success_criteria'] is not None
```

### Validate Campaign Type Coverage

```python
from agents.message_strategy_agent import CAMPAIGN_TYPE_TO_TONE, CAMPAIGN_TYPE_TO_CTA

campaign_types = [
    "Market Research",
    "Survey",
    "Consulting",
    "Expert Network",
    "Webinar",
    "Report Sales",
    "Competition Benchmarking",
    "Account Reactivation",
]

# Ensure all types have tone and CTA
for campaign_type in campaign_types:
    assert campaign_type in CAMPAIGN_TYPE_TO_TONE
    assert campaign_type in CAMPAIGN_TYPE_TO_CTA
```

### Validate Industry Coverage

```python
from agents.message_strategy_agent import INDUSTRY_TO_THEMES

# Test known industry
output = run_message_strategy(
    campaign_name="Finance Campaign",
    campaign_type="Market Research",
    offer="Risk management insights",
    target_personas=["CXO"],
    target_industry="Finance",
    channel_mix=["email"],
)

themes = output['messaging_strategy']['key_themes']
assert "risk management" in themes or "compliance" in themes
```

---

## Integration Checklist

When integrating into your pipeline:

- [ ] Import `run_message_strategy` from this module
- [ ] Pass campaign details from Orchestrator
- [ ] Validate campaign_type is in CAMPAIGN_TYPE_TO_TONE (log if not)
- [ ] Validate industry is in INDUSTRY_TO_THEMES (log if not)
- [ ] Ensure target_personas non-empty
- [ ] Pass output to Email Copy Agent
- [ ] Pass output to WhatsApp Copy Agent
- [ ] Log any missing tone/CTA/themes
- [ ] Validate output schema matches expectations
- [ ] Store strategy in database (optional) for audit trail

---

## Files Included

```
agents/
├── message_strategy_agent.py       ← Main agent (COMPLETE)
├── registry/
│   └── message_strategy.json       ← System prompt + config
└── MESSAGE_STRATEGY_GUIDE.md       ← This file
```

---

## What's Ready for Claude Integration

When you add Anthropic API:

1. **System Prompt:** Already in `registry/message_strategy.json` (1000+ chars)
2. **Tool Definition:** `define_message_strategy` tool with full schema
3. **Tool Forcing:** Return tool use response with strategy components
4. **Response Parsing:** Extract strategy from tool input
5. **Schema Validation:** Validate output matches expected structure

```python
# Future upgrade (with Anthropic SDK):
from anthropic import Anthropic

def run_message_strategy_with_api(
    campaign_name: str,
    campaign_type: str,
    offer: str,
    target_personas: List[str],
    target_industry: str,
    channel_mix: List[str],
):
    config = load_agent_config("message_strategy")
    client = Anthropic()
    
    user_message = f"""
    Campaign: {campaign_name}
    Type: {campaign_type}
    Offer: {offer}
    Target Personas: {', '.join(target_personas)}
    Industry: {target_industry}
    Channels: {', '.join(channel_mix)}
    
    Develop comprehensive messaging strategy.
    """
    
    response = client.messages.create(
        model=config["model"],
        system=config["system_prompt"],
        tools=config["tools"],
        messages=[{"role": "user", "content": user_message}],
    )
    
    # Extract tool use
    tool_use = response.content[0]  # Assuming tool use response
    strategy = tool_use.input
    
    # Return as-is (Anthropic will refine logic)
    return strategy
```

---

## Support

**Questions about usage?** Check examples above or review docstrings in `message_strategy_agent.py`.

**Want to customize?** Edit TONE/THEME/VALUE_PROP mappings in `message_strategy_agent.py`.

**Integration issues?** Ensure input matches schema and campaign_type/industry are recognized. Fall-back defaults handle unknowns gracefully.

---

## Next Agent

Once this is integrated, **Email Copy Agent** will take this output and generate email variations per prospect.

**Handoff:** `MessageStrategyOutput` → `Email Copy Agent Input`

---

**Built:** Thursday  
**Status:** ✅ Ready for Monday Delivery  
**Quality:** Production-Ready, Tested, Documented
