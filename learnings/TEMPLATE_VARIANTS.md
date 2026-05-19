# Template Variants — M1 Strategy

Learned through Email, LinkedIn, WhatsApp agents. Each has 2 M1 variants to avoid repetition and test different hooks.

---

## Why Variants Matter

**Problem:** Sending identical M1 to thousands looks like broadcast, not research.

**Solution:** 2 M1 variants, randomly selected per generation.

**Result:** Same core pain point, different hook approach. Feels more natural. Tests two psychological angles.

---

## Email M1 Variants

### Variant 1: FOMO (Fear of Missing Out) Hook

**Opener:** "Most leaders missing: [pain_point]"

**Structure:**
```
Hi [first_name],

We recently finished a mandate on [Industry]. While reviewing the findings, we discovered something most leaders at [Company]'s level aren't tracking yet:

[PAIN_POINT_1]

The companies ahead? They're already moving on this. We walked competitors through what we found, and it shifted how they're positioning on [PAIN_POINT_2].

Would you be open to a 30-minute call? We walk you through the full picture, and you tell us if it maps to what you're seeing.

Looking forward to connecting.

Best
```

**Psychological Angle:** "Most leaders missing" = you're behind unless you act

**When to use:** When pain point is emerging or competitive gap is widening

---

### Variant 2: Scarcity Hook

**Opener:** "Window closing on [pain_point]"

**Structure:**
```
Hi [first_name],

We recently finished a mandate on [Industry]. Looking at the findings, there's a window closing on [PAIN_POINT_1].

The companies ahead? They moved fast on [PAIN_POINT_2]. We walked a few through what we found, and they immediately saw the risk.

Would you be open to a 30-minute call? We walk you through the full picture, and you tell us if it maps to what you're seeing.

Looking forward to connecting.

Best
```

**Psychological Angle:** "Window closing" = time-limited opportunity

**When to use:** When pain point is accelerating or trend-based

---

## LinkedIn M1 Variants

### Variant 1: Direct Insight Opener

**Structure:**
```
Hi [first_name], [PAIN_POINT_1].

We are conducting research on [Industry]. Our research addresses the gap between [PAIN_POINT_1] and [PAIN_POINT_2].

Would you be open to a 30-minute call? We walk you through what we found on how top performers approach this differently, and you tell us whether it maps to your [PAIN_POINT_2] at [Company].
```

**Psychological Angle:** Lead with the pain. Direct, confident.

**When to use:** When pain is immediately recognizable to their role

---

### Variant 2: Context-First Approach

**Structure:**
```
Hi [first_name], we're seeing [pain_point] become critical across [Industry].

We researched how [primary_angle]. The gap? [PAIN_POINT_2].

Would you be open to a 30-minute call to explore what we found and whether it maps to your approach at [Company]?
```

**Psychological Angle:** Establish research credibility first, then pain.

**When to use:** When building context helps (new market shift, less obvious pain)

---

## WhatsApp M1 Variants

### Variant 1: Direct Insight

**Structure:**
```
Hi [first_name], quick insight from our [context]:

[PAIN_POINT_1]

Would you be open to a quick 30-min call to explore? We walk through what we found.
```

**Follow-up 1:** "No pressure — just thought this mapped to [Company]."

**Follow-up 2:** "Still interested in a quick chat?"

**Psychological Angle:** Quick, punchy. Gets straight to insight.

**When to use:** When pain is immediately relevant to their role

---

### Variant 2: Context-First Approach

**Structure:**
```
Hi [first_name], we finished [context].

Most leaders at [Company]'s level aren't tracking: [PAIN_POINT_1]

Worth a 30-min call to walk through what we found?
```

**Follow-up 1:** "Companies ahead on this are already repositioning."

**Follow-up 2:** "Interested?"

**Psychological Angle:** Establish credibility + competitive threat.

**When to use:** When building context helps urgency

---

## How Variants Work in Code

**Random Selection:**
```python
variant = random.choice([1, 2])

if variant == 1:
    # Use Variant 1 template
else:
    # Use Variant 2 template
```

**Per-generation:** Each time agent runs, variant is randomly selected.

**Consistency:** Same persona always gets SAME variant in same run, but different personas might get different variants in same campaign generation.

---

## Testing Insights

**Variant 1 ("Most leaders missing" / "Direct insight"):**
- Higher engagement when pain is recognizable but uncommon knowledge
- Works when audience is C-suite (competitive anxiety)
- FOMO hook tests well with early movers

**Variant 2 ("Window closing" / "Context-first"):**
- Higher engagement when pain is new market shift
- Works when audience needs context (ops-level)
- Scarcity hook tests well with time-sensitive buyers

---

## Quality Checklist

- [ ] M1 has exactly 2 variants
- [ ] Variant 1 tested (FOMO/Direct Insight angle)
- [ ] Variant 2 tested (Scarcity/Context angle)
- [ ] Random selection working (varied messages per run)
- [ ] Both variants reference same pain points
- [ ] Both variants have same CTA + value exchange
- [ ] Both variants include follow-ups (Email: soft ask, LinkedIn/WhatsApp: in follow-ups)
- [ ] Variants differ in hook approach, not core message

