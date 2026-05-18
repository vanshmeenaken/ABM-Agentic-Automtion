# Email Copy Agent — Complete Integration Guide

**Status:** ✅ Production Ready  
**Built by:** User  
**For Integration:** Your Teammate  
**Monday Delivery:** ✅ Complete

---

## What This Agent Does

Generates personalized email variations (primary + alternatives) using tone/themes from message strategy and prospect details.

**Input:** Persona + prospect + message strategy + offer  
**Output:** Primary email + 3 alternatives + A/B test recommendations

---

## Quick Start (For Your Teammate)

### 1. Import and Use

```python
from agents.email_copy_agent import generate_email_copy

# Define inputs
prospect = {
    "first_name": "Sarah",
    "company_name": "TechCorp Inc",
    "designation": "VP of Marketing",
    "email": "sarah@techcorp.com",
}

message_strategy = {
    "messaging_strategy": {
        "tone": "consultative",
        "key_themes": ["digital transformation", "customer experience"],
        "value_propositions": {
            "Director": "Practical guidance on implementing transformation within teams"
        },
        "call_to_action": "Access the research findings",
    },
    "persona_specific_messages": {
        "Director": {
            "pain_points_to_address": "Team productivity, budget optimization, performance metrics"
        }
    }
}

# Generate email copy
output = generate_email_copy(
    persona="Director",
    prospect=prospect,
    message_strategy=message_strategy,
    campaign_name="Tech Market Research Initiative",
    offer="Comprehensive market research report on AI/ML adoption",
)

# Access results
print(f"Subject: {output['primary_email']['subject']}")
print(f"Preview: {output['primary_email']['preview']}")
print(f"Body:\n{output['primary_email']['body']}")
print(f"CTA: {output['primary_email']['cta_text']}")
print(f"\nAlternative Variations: {len(output['alternative_variations'])}")
for i, alt in enumerate(output['alternative_variations']):
    print(f"  {i+1}. {alt['test_variant']}: {alt['subject']}")
```

### 2. Expected Output

```python
{
    "primary_email": {
        "subject": "Sarah, quick insight on digital transformation at TechCorp",
        "preview": "Research on how peers handle DX...",
        "body": "Hi Sarah,\n\nI'm curious about how TechCorp is approaching digital transformation...\n\nHere's what makes this relevant to you as a Director:\n\n✓ Practical guidance...\n✓ Insights on digital transformation...\n✓ Research report\n\nI'd love to hear your perspective on this as well.",
        "cta_text": "Access the research findings",
        "estimated_read_time_seconds": 45,
    },
    "alternative_variations": [
        {
            "subject": "TechCorp's approach to customer experience transformation",
            "preview": "New insights on CX leaders...",
            "body": "...",
            "cta_text": "Access the research findings",
            "test_variant": "theme_variation"
        },
        {
            "subject": "Quick question for TechCorp, Sarah",
            "preview": "Two-minute read on digital transformation...",
            "body": "...",
            "cta_text": "Read more",
            "test_variant": "short_form"
        },
        {
            "subject": "Sarah, solving team productivity at TechCorp",
            "preview": "How peers handle productivity challenges...",
            "body": "...",
            "cta_text": "Let's talk",
            "test_variant": "pain_point_focus"
        }
    ],
    "personalization_variables": {
        "first_name": "Sarah",
        "company_name": "TechCorp Inc",
        "designation": "VP of Marketing",
        "email": "sarah@techcorp.com",
        "persona": "Director",
        "tone": "consultative",
        "themes": ["digital transformation", "customer experience"],
        "value_prop": "Practical guidance...",
    },
    "ab_test_recommendations": {
        "winner_metric": "open_rate",
        "test_duration_days": 7,
        "minimum_sample_size": 50,
    },
    "notes": "Email generated for Director at TechCorp Inc. Tone: consultative. Themes: digital transformation, customer experience.",
}
```

---

## How Email Generation Works

### Step 1: Extract Strategy Components

Takes tone, themes, value props, CTA from message strategy:

```python
tone = "consultative"  # From message strategy
themes = ["digital transformation", "customer experience"]
value_prop = "Practical guidance on implementing transformation..."
cta = "Access the research findings"
```

### Step 2: Generate Subject Line

Uses tone + persona + prospect details:

| Tone | Template |
|---|---|
| **professional** | "Strategic opportunity for {company_name}" |
| **consultative** | "Your perspective on {theme} — quick 2 min read" |
| **urgent** | "Limited slots: {offer_preview}" |
| **friendly** | "Quick thought on {theme} at {company_name}" |
| **educational** | "Must-read: {offer_preview}" |

Formula: Personalization + Power word + Company mention + Value hint

**Good subject:** "Sarah, quick insight on digital transformation at TechCorp" (54 chars)  
**Bad subject:** "Check this out" (no personalization, no value hint)

### Step 3: Generate Opening Hook

Tone-specific openings that grab attention:

**Professional:** "Hi Sarah,\n\nI came across TechCorp's work in digital transformation and wanted to reach out."

**Consultative:** "Hi Sarah,\n\nI'm curious about how TechCorp is approaching digital transformation."

**Urgent:** "Hi Sarah,\n\nLimited slots — wanted to make sure you saw this."

**Friendly:** "Hey Sarah,\n\nSaw you're at TechCorp and thought of you."

**Educational:** "Hi Sarah,\n\nJust released: insights on digital transformation for VPs at companies like TechCorp."

### Step 4: Generate Email Body

Body includes:
1. **Value statement:** "Here's what makes this relevant to you as a Director:"
2. **3 bullet benefits:** Uses persona value prop + themes + offer
3. **Tone-specific closing hook:** Vary by tone (consultative: ask for perspective, urgent: scarcity, educational: peer credibility)

**Example body:**
```
Hi Sarah,

I'm curious about how TechCorp is approaching digital transformation.

Here's what makes this relevant to you as a Director:

✓ Practical guidance on implementing transformation within teams
✓ Insights on digital transformation and customer experience
✓ Comprehensive market research report on AI/ML adoption

I'd love to hear your perspective on this as well. Would be great to connect briefly.
```

### Step 5: Personalization Variables

Maps all dynamic values for template insertion:

```python
{
    "first_name": "Sarah",
    "company_name": "TechCorp Inc",
    "designation": "VP of Marketing",
    "email": "sarah@techcorp.com",
    "persona": "Director",
    "tone": "consultative",
    "themes": ["digital transformation", "customer experience"],
    "value_prop": "Practical guidance...",
}
```

Use in templates: `Hi {{first_name}}, [message about {{company_name}}]...`

### Step 6: Alternative Variations

4 variations test different angles:

| Variation | Angle | When to Use |
|---|---|---|
| **Theme Variation** | Different theme from strategy | Test if second theme resonates better |
| **Short Form** | Concise 2-min read version | For time-constrained prospects |
| **Pain Point Focus** | Lead with pain + solution | When pain is highly relevant |
| **Relationship Focus** | Build rapport first | For relationship-based sales |

### Step 7: A/B Test Recommendations

Guidance for which metric to optimize:

- **open_rate** — Test subject lines + preview text
- **click_rate** — Test CTA copy + body hook strength
- **response_rate** — Test personalization depth + relevance
- **meeting_booked** — Test pain point alignment + urgency

Recommended test size: 50-100 per variation  
Test duration: 7 days minimum

---

## Integration Points

### Into Your Pipeline

**Previous Stage:** Message Strategy Agent  
**Your Agent:** Email Copy  
**Next Stage:** Email sending platform (or WhatsApp Copy Agent continues orchestration)

```
Message Strategy Agent
        ↓
(tone, themes, value props, CTA)
        ↓
Email Copy Agent (per prospect)
        ↓
(primary_email + 3 alternatives)
        ↓
Email Sending Platform
(insert personalizations, track opens/clicks)
```

### Data Contract

**Input from Message Strategy:**
```python
{
    "messaging_strategy": {
        "tone": str,
        "key_themes": List[str],
        "value_propositions": Dict[str, str],  # {persona: value_prop}
        "call_to_action": str,
    },
    "persona_specific_messages": Dict,  # {persona: {pain_points: ..., value_prop: ...}}
}
```

**Input from Orchestrator/Persona Classifier:**
```python
{
    "persona": str,  # CXO, Director, Manager, Specialist
    "prospect": {
        "first_name": str,
        "company_name": str,
        "designation": str,
        "email": str,
    }
}
```

**Output to Email Platform:**
```python
{
    "primary_email": {
        "subject": str,
        "preview": str,
        "body": str,
        "cta_text": str,
    },
    "alternative_variations": List[Dict],  # [4 variations with test_variant type]
    "personalization_variables": Dict,
    "ab_test_recommendations": Dict,
}
```

---

## Advanced Usage

### Override Primary Email

```python
output = generate_email_copy(...)
# Customize primary email if needed
output['primary_email']['subject'] = "Your custom subject"
output['primary_email']['cta_text'] = "Your custom CTA"
```

### Filter Variations by Test Type

```python
# Get only short form variation
short_variations = [
    v for v in output['alternative_variations']
    if v['test_variant'] == 'short_form'
]
```

### Extract Personalization for Template System

```python
vars = output['personalization_variables']
template_subject = f"Hi {{first_name}}, {some_message}"
# Replace with: subject.format(**vars)
```

### Batch Generate Emails for Campaign

```python
prospects = [
    {"first_name": "Sarah", "company_name": "TechCorp", ...},
    {"first_name": "John", "company_name": "FinanceInc", ...},
    # ... more prospects
]

email_outputs = []
for prospect in prospects:
    output = generate_email_copy(
        persona="Director",
        prospect=prospect,
        message_strategy=strategy,
        campaign_name=campaign_name,
        offer=offer,
    )
    email_outputs.append(output)

# Now have all email copy ready for sending
```

### Store in Database

```python
from campaigns.models import EmailCopy

output = generate_email_copy(...)

EmailCopy.objects.create(
    prospect=prospect_obj,
    persona=persona,
    primary_subject=output['primary_email']['subject'],
    primary_body=output['primary_email']['body'],
    primary_cta=output['primary_email']['cta_text'],
    alternatives=output['alternative_variations'],  # JSONField
    personalization_vars=output['personalization_variables'],  # JSONField
)
```

---

## Customization

### Add Email Template

Edit `EMAIL_SUBJECT_TEMPLATES` dict to add custom tone:

```python
EMAIL_SUBJECT_TEMPLATES = {
    # ... existing tones ...
    "aspirational": [
        "{first_name}, {company_name}'s next growth opportunity",
        "Imagine what {company_name} could achieve with {theme}",
    ],
}
```

### Adjust Opening Hooks

Edit `EMAIL_OPENING_HOOKS` to customize tone-specific openers:

```python
EMAIL_OPENING_HOOKS = {
    # ... existing tones ...
    "friendly": [
        "Hey {first_name},\n\nHope you're having an awesome week!",
        # ... more custom openings
    ],
}
```

### Add Persona Value Props

Edit `EMAIL_VALUE_PROP_HOOKS`:

```python
EMAIL_VALUE_PROP_HOOKS = {
    # ... existing personas ...
    "CISO": "Security and compliance implications of {theme} for enterprise governance",
}
```

### Customize Variation Logic

Modify `generate_email_copy()` function to add/remove variation types:

```python
# Add new variation type
new_variation = {
    "subject": "Your custom angle",
    "body": "Your custom body",
    "test_variant": "your_test_type",
}
alternative_variations.append(new_variation)
```

---

## Error Handling

Agent gracefully handles:
- ✅ Missing first_name (defaults to "there")
- ✅ Missing company_name (defaults to "your company")
- ✅ Missing themes (generates generic insights)
- ✅ Missing value_prop for persona (defaults to generic)
- ✅ Missing pain_points (uses generic challenges)

```python
# Safe to call even with incomplete data
output = generate_email_copy(
    persona="Director",
    prospect={
        "first_name": "Sarah",
        # Missing company_name, designation
    },
    message_strategy={
        # Minimal strategy
        "messaging_strategy": {
            "tone": "professional",
            "key_themes": [],
            "value_propositions": {},
            "call_to_action": "Learn more",
        }
    },
    campaign_name="Campaign",
    offer="Offer",
)

# Results: Uses defaults gracefully, no errors
assert output['primary_email']['subject'] is not None
assert output['personalization_variables']['company_name'] == 'your company'
```

---

## Testing

### Unit Test Primary Email

```python
from agents.email_copy_agent import generate_email_copy

output = generate_email_copy(
    persona="Director",
    prospect={
        "first_name": "Sarah",
        "company_name": "TechCorp",
        "designation": "VP Marketing",
        "email": "sarah@techcorp.com",
    },
    message_strategy={
        "messaging_strategy": {
            "tone": "consultative",
            "key_themes": ["digital transformation"],
            "value_propositions": {"Director": "Team efficiency"},
            "call_to_action": "Learn more",
        },
        "persona_specific_messages": {
            "Director": {"pain_points_to_address": "productivity"}
        }
    },
    campaign_name="Test Campaign",
    offer="Research Report",
)

# Assertions
assert output['primary_email']['subject'] is not None
assert len(output['primary_email']['subject']) <= 60
assert len(output['primary_email']['preview']) <= 50
assert "Sarah" in output['primary_email']['body']
assert "TechCorp" in output['primary_email']['body']
assert output['primary_email']['cta_text'] == "Learn more"
```

### Test Alternatives Generated

```python
assert len(output['alternative_variations']) >= 2
assert len(output['alternative_variations']) <= 4

# All variations have required fields
for alt in output['alternative_variations']:
    assert 'subject' in alt
    assert 'body' in alt
    assert 'test_variant' in alt
    assert alt['test_variant'] in ['theme_variation', 'short_form', 'pain_point_focus']

# All subjects <= 60 chars
for alt in output['alternative_variations']:
    assert len(alt['subject']) <= 60
```

### Test Personalization Variables

```python
vars = output['personalization_variables']
assert vars['first_name'] == 'Sarah'
assert vars['company_name'] == 'TechCorp'
assert vars['persona'] == 'Director'
assert vars['tone'] == 'consultative'
```

---

## Integration Checklist

When integrating into your pipeline:

- [ ] Import `generate_email_copy` from this module
- [ ] Ensure persona is one of: CXO, Director, Manager, Specialist, Individual Contributor
- [ ] Ensure prospect dict includes: first_name, company_name, designation, email
- [ ] Ensure message_strategy includes messaging_strategy + persona_specific_messages dicts
- [ ] Log subject line length (warn if > 60 chars)
- [ ] Log preview text length (warn if > 50 chars)
- [ ] Store primary_email + alternatives in database
- [ ] Set up A/B test based on recommendations
- [ ] Track which variation gets highest open_rate
- [ ] Use winner for follow-up sequences
- [ ] Validate personalization variables insert correctly

---

## Files Included

```
agents/
├── email_copy_agent.py              ← Main agent (COMPLETE)
├── registry/
│   └── email_copy.json              ← System prompt + config
└── EMAIL_COPY_GUIDE.md              ← This file
```

---

## What's Ready for Claude Integration

When you add Anthropic API:

1. **System Prompt:** In `registry/email_copy.json` (2000+ chars, comprehensive)
2. **Tool Definition:** `generate_email_copy` tool with full schema
3. **Tool Forcing:** Return tool use response with email variations
4. **Response Parsing:** Extract subject, body, alternatives from tool input

```python
# Future upgrade (with Anthropic SDK):
from anthropic import Anthropic

def generate_email_copy_with_api(
    persona: str,
    prospect: Dict,
    message_strategy: Dict,
    campaign_name: str,
    offer: str,
):
    config = load_agent_config("email_copy")
    client = Anthropic()
    
    user_message = f"""
    Generate email variations for:
    
    Persona: {persona}
    Prospect: {prospect['first_name']} at {prospect['company_name']} ({prospect['designation']})
    Campaign: {campaign_name}
    Offer: {offer}
    Tone: {message_strategy['messaging_strategy']['tone']}
    Themes: {', '.join(message_strategy['messaging_strategy']['key_themes'])}
    
    Generate compelling email copy.
    """
    
    response = client.messages.create(
        model=config["model"],
        system=config["system_prompt"],
        tools=config["tools"],
        messages=[{"role": "user", "content": user_message}],
    )
    
    # Extract tool use
    tool_use = response.content[0]
    return tool_use.input
```

---

## Support

**Questions about usage?** Check examples above or review docstrings in `email_copy_agent.py`.

**Subject line too long?** Try removing personalization or using shorter power words.

**CTA not converting?** Test multiple variations using A/B test recommendations.

**Integration issues?** Ensure personalization_variables match template placeholders.

---

## Next Agent

Once this is integrated, **WhatsApp Copy Agent** will take same inputs and generate short, conversational WhatsApp messages.

**Handoff:** `EmailCopyOutput` → same structure as input to WhatsApp Copy Agent

---

**Built:** Thursday  
**Status:** ✅ Ready for Monday Delivery  
**Quality:** Production-Ready, Tested, Documented
