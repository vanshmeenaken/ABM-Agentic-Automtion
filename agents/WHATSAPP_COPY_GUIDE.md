# WhatsApp Copy Agent — Complete Integration Guide

**Status:** ✅ Production Ready  
**Built by:** User  
**For Integration:** Your Teammate  
**Monday Delivery:** ✅ Complete

---

## What This Agent Does

Generates short, conversational WhatsApp messages (< 160 chars) + follow-ups for prospect persistence.

**Input:** Prospect + persona + message strategy + offer  
**Output:** Primary message + follow-up sequence + alternatives

---

## Quick Start (For Your Teammate)

### 1. Import and Use

```python
from agents.whatsapp_copy_agent import generate_whatsapp_copy

prospect = {
    "first_name": "Sarah",
    "company_name": "TechCorp Inc",
    "designation": "VP of Marketing",
}

message_strategy = {
    "messaging_strategy": {
        "tone": "friendly",
        "key_themes": ["digital transformation"],
    }
}

output = generate_whatsapp_copy(
    prospect=prospect,
    persona="Director",
    message_strategy=message_strategy,
    campaign_name="Tech Research Initiative",
    offer="Market research report",
)

print(f"Message: {output['primary_message']['message']}")
print(f"Chars: {output['primary_message']['character_count']}")
print(f"Day 3 Follow-up: {output['primary_message']['follow_up_messages'][0]}")
```

### 2. Expected Output

```python
{
    "primary_message": {
        "message": "Hey Sarah! Quick thought on digital transformation at TechCorp. Chat?",
        "character_count": 70,
        "follow_up_messages": [
            "Still interested in exploring this?",
            "Final check-in: would this help your team?"
        ],
        "timing": {
            "day_1": "Send immediately",
            "day_3": "Still interested in exploring this?",
            "day_7": "Final check-in: would this help your team?"
        }
    },
    "alternative_variations": [
        {
            "message": "Sarah, saw TechCorp doing great work. Worth a chat?",
            "follow_up_messages": ["Checking in!", "Happy to help"],
            "test_variant": "theme_variation",
            "character_count": 54
        }
    ],
    "personalization_variables": {
        "first_name": "Sarah",
        "company_name": "TechCorp Inc",
        "persona": "Director",
        "tone": "friendly",
    },
    "whatsapp_best_practices": {
        "send_time": "Tue-Thu 9am-5pm local time",
        "avoid_late_night": True,
        "use_emoji": True,
        "keep_conversational": True,
    }
}
```

---

## How WhatsApp Generation Works

### Step 1: Understanding WhatsApp Sales

WhatsApp is personal, warm, conversational. NOT email 2.0.

| Email | WhatsApp |
|---|---|
| Formal, structured | Casual, conversational |
| 45+ second read time | 10-15 second read time |
| Multiple paragraphs | 1-2 short sentences |
| CTA button prominent | Soft question or request |
| Can be salesy | MUST feel peer-to-peer |

### Step 2: Message Structure

**Good:** "Hey Sarah! Quick thought on digital transformation at TechCorp. Chat?"
- Uses first name
- Warm greeting
- References company + theme
- Soft CTA
- 70 chars (natural SMS length)

**Bad:** "Hi Sarah, I wanted to reach out regarding a strategic opportunity at TechCorp that could help your team with digital transformation. Please let me know if you'd like to schedule a call."
- Too formal for WhatsApp
- Too long (150+ chars, feels like forwarded email)
- Salesy ("strategic opportunity")

### Step 3: Tone-Specific Approaches

| Tone | Opening | CTA Example |
|---|---|---|
| **Professional** | "Hi {first_name}, thought of you..." | "Worth 15 mins?" |
| **Consultative** | "{first_name}, curious about..." | "Your take?" |
| **Urgent** | "{first_name}, limited slots..." | "Can I send details?" |
| **Friendly** | "Hey {first_name}! Quick thought..." | "Chat?" |
| **Educational** | "Just released: {theme} insights" | "Interested?" |

### Step 4: Follow-Up Sequence

WhatsApp strength is persistence without being pushy.

**Day 1 (Immediate):**
Primary message opens door, builds curiosity.

**Day 3 (Follow-up):**
Soft check-in shows you respect their time. "Checking in" or "Still interested?" — natural, not desperate.

**Day 7 (Final):**
Last attempt. Acknowledge it's final but stay warm. "Final check-in: would this help your team?"

### Step 5: Character Count Matters

SMS standard = 160 chars. WhatsApp can go longer but:
- < 100 chars: Maximum impact, immediate read
- 100-160: Comfortable, still SMS-like
- > 160: Feels like forwarded content, loses WhatsApp vibe

### Step 6: Personalization Variables

Must personalize with:
- **first_name:** Always use (never generic "there")
- **company_name:** Reference company, not just "team"
- **designation:** Implicit in tone, not stated

Variables for template insertion:
```python
{
    "first_name": "Sarah",
    "company_name": "TechCorp Inc",
    "persona": "Director",
    "tone": "friendly",
    "themes": ["digital transformation"],
}
```

### Step 7: Alternative Variations

3-4 tests for different angles:

| Variation | Angle | When to Use |
|---|---|---|
| **Theme Variation** | Different industry theme | If primary underperforms |
| **Short Form** | Ultra-concise (< 100 chars) | High-volume prospecting |
| **Relationship First** | Build rapport before pitch | Relationship-based sales |
| **Urgency Angle** | Time-sensitive approach | Webinar/event closing |

---

## Integration Points

### Into Your Pipeline

**Previous Stage:** Message Strategy Agent (+ Email Copy in parallel)  
**Your Agent:** WhatsApp Copy  
**Next Stage:** WhatsApp sending platform (or fallback to email)

```
Message Strategy Agent
        ↓
Email Copy Agent (email variation)
WhatsApp Copy Agent (WhatsApp variation)  ← Parallel
        ↓
Email Platform + WhatsApp Platform
```

### Branching Logic

From Orchestrator:

```python
if prospect.phone and "whatsapp" in channel_mix:
    whatsapp_output = generate_whatsapp_copy(...)
    # Send WhatsApp messages
else:
    # Skip WhatsApp, fallback to email/linkedin
```

### Data Contract

**Input from Message Strategy:**
```python
{
    "messaging_strategy": {
        "tone": str,
        "key_themes": List[str],
    }
}
```

**Input from Persona Classifier:**
```python
{
    "persona": str,
    "prospect": {
        "first_name": str,
        "company_name": str,
        "designation": str,
        "phone": str,  # Required for WhatsApp
    }
}
```

**Output to WhatsApp Platform:**
```python
{
    "primary_message": {
        "message": str,  # < 200 chars
        "follow_up_messages": List[str],  # 2-3 messages
    },
    "alternative_variations": List[Dict],
    "personalization_variables": Dict,
    "whatsapp_best_practices": Dict,
}
```

---

## Advanced Usage

### Send Follow-Ups Programmatically

```python
from datetime import timedelta
from django.utils import timezone

output = generate_whatsapp_copy(...)
prospect_obj = Prospect.objects.get(email=prospect['email'])

# Send Day 1 (immediately)
send_whatsapp(
    prospect_obj.phone,
    output['primary_message']['message'],
    scheduled_for=timezone.now(),
)

# Schedule Day 3
send_whatsapp(
    prospect_obj.phone,
    output['primary_message']['follow_up_messages'][0],
    scheduled_for=timezone.now() + timedelta(days=3),
)

# Schedule Day 7
send_whatsapp(
    prospect_obj.phone,
    output['primary_message']['follow_up_messages'][1],
    scheduled_for=timezone.now() + timedelta(days=7),
)
```

### Test Multiple Variations

```python
variations_to_test = [
    output['primary_message'],  # Primary
    *output['alternative_variations'],  # Alternatives
]

for i, variation in enumerate(variations_to_test):
    segment = prospects[i % len(variations_to_test)]
    send_whatsapp(
        segment.phone,
        variation['message'],
        test_variant=variation.get('test_variant', 'primary'),
    )
```

### Best Time to Send

```python
best_practices = output['whatsapp_best_practices']
# Respect send_time recommendation
send_time = "Tue-Thu 9am-5pm local time"
# Extract hour from best_practices and schedule appropriately
```

### Store in Database

```python
from campaigns.models import WhatsAppCopy

output = generate_whatsapp_copy(...)

WhatsAppCopy.objects.create(
    prospect=prospect_obj,
    persona=persona,
    primary_message=output['primary_message']['message'],
    follow_ups=output['primary_message']['follow_up_messages'],
    alternatives=output['alternative_variations'],  # JSONField
    character_count=output['primary_message']['character_count'],
    test_variant='primary',
)
```

---

## Customization

### Add Custom Tone

Edit `WHATSAPP_OPENINGS` dict:

```python
WHATSAPP_OPENINGS = {
    # ... existing tones ...
    "playful": [
        "Hey {first_name}! Got a sec to chat about {company_name}'s {theme}?",
        "{first_name}, quick thought (seriously, just 10 mins)...",
    ],
}
```

### Add Custom Follow-Up Message

Edit `WHATSAPP_FOLLOW_UPS`:

```python
WHATSAPP_FOLLOW_UPS = {
    # ... existing tones ...
    "friendly": [
        "Checking in! Still game for a chat?",
        "Would love to get your thoughts when you're free.",
        # Add custom follow-up
    ],
}
```

### Adjust Character Limits

If your WhatsApp provider supports longer messages:

```python
# In generate_whatsapp_message():
MAX_CHAR = 240  # Instead of 160
if len(message) > MAX_CHAR:
    message = message[:MAX_CHAR-3] + "..."
```

---

## Best Practices

### ✅ DO

- Use first name always
- Keep under 160 chars (160 is ideal SMS length)
- Reference company + specific theme
- Soft CTA ("Chat?" "Thoughts?" "Worth 10 mins?")
- Send during business hours (Tue-Thu, 9am-5pm)
- Space follow-ups: Day 1, Day 3, Day 7
- Test different themes and angles
- Be warm and conversational

### ❌ DON'T

- Generic messages (no personalization)
- Emoji overload (max 1-2 if tone allows)
- Salesy language ("excited to connect," "synergy")
- Multiple messages same day
- Late night sends (9pm-8am)
- Forward email copy to WhatsApp
- Pushy CTAs ("CLICK HERE" "SCHEDULE NOW")
- Ignore unresponsive leads (give them space)

---

## Error Handling

Agent gracefully handles:
- ✅ Missing phone number (returns empty, orchestrator fallback to email)
- ✅ Missing themes (generates generic message)
- ✅ Missing tone (defaults to friendly)
- ✅ Missing persona (generates neutral message)

```python
# Safe even with minimal data
output = generate_whatsapp_copy(
    prospect={"first_name": "Sarah"},  # Missing company_name
    persona="Director",
    message_strategy={"messaging_strategy": {"tone": "friendly", "key_themes": []}},
    campaign_name="Campaign",
    offer="Offer",
)

# Results: Uses defaults gracefully
assert output['primary_message']['message'] is not None
```

---

## Testing

### Unit Test Message Generation

```python
from agents.whatsapp_copy_agent import generate_whatsapp_copy

output = generate_whatsapp_copy(
    prospect={
        "first_name": "Sarah",
        "company_name": "TechCorp",
        "designation": "VP Marketing",
    },
    persona="Director",
    message_strategy={
        "messaging_strategy": {
            "tone": "friendly",
            "key_themes": ["digital transformation"],
        }
    },
    campaign_name="Test",
    offer="Report",
)

# Assertions
assert output['primary_message']['message'] is not None
assert output['primary_message']['character_count'] <= 200
assert len(output['primary_message']['follow_up_messages']) >= 2
assert output['primary_message']['character_count'] > 0
```

### Test Character Count

```python
msg = output['primary_message']['message']
assert len(msg) <= 200, f"Message too long: {len(msg)} chars"
assert len(msg) > 10, f"Message too short: {len(msg)} chars"
assert "Sarah" in msg, "Must personalize with first name"
```

### Test Variations Exist

```python
assert len(output['alternative_variations']) >= 1
for alt in output['alternative_variations']:
    assert 'test_variant' in alt
    assert alt['character_count'] <= 200
```

---

## Integration Checklist

When integrating into your pipeline:

- [ ] Ensure prospect has phone number (non-empty)
- [ ] Extract phone and validate format
- [ ] Generate WhatsApp copy ONLY if "whatsapp" in channel_mix
- [ ] Respect send_time best practices (Tue-Thu, 9am-5pm)
- [ ] Schedule follow-ups: Day 1, Day 3, Day 7
- [ ] Track which variation was sent
- [ ] Monitor response rate (target: 5-8%)
- [ ] Test different variations against each other
- [ ] Use winner for future campaigns
- [ ] Have fallback to email if WhatsApp fails
- [ ] Log opt-outs and respect DND rules

---

## Files Included

```
agents/
├── whatsapp_copy_agent.py           ← Main agent (COMPLETE)
├── registry/
│   └── whatsapp_copy.json           ← System prompt + config
└── WHATSAPP_COPY_GUIDE.md           ← This file
```

---

## What's Ready for Claude Integration

When you add Anthropic API:

1. **System Prompt:** In `registry/whatsapp_copy.json` (2000+ chars)
2. **Tool Definition:** `generate_whatsapp_copy` tool with schema
3. **Tool Forcing:** Return tool use response with messages
4. **Response Parsing:** Extract primary_message + alternatives

---

## Support

**Message too long?** Trim to < 100 chars or test short_form variation.

**Low response rate?** Test alternative variations, adjust timing.

**Phone validation?** Ensure prospect.phone non-empty before calling agent.

**Integration issues?** Verify branching logic in orchestrator checks for phone first.

---

## Next Agent

**Compliance Review Agent** — Final gate ensuring messages comply with regulations (GDPR, TCPA, CAN-SPAM).

---

**Built:** Thursday  
**Status:** ✅ Ready for Monday Delivery  
**Quality:** Production-Ready, Tested, Documented
