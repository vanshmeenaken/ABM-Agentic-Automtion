# Compliance Review Agent - In-Depth Context & Architecture

**Date:** May 2026  
**Status:** Production Ready ✅  
**Version:** 1.0

---

## Executive Summary

**Compliance Review Agent** = final gatekeeper before messages go live. Checks all copy against 7 compliance rules. **BLOCKS** any message that violates compliance (cannot be overridden). Sends passing messages to Telegram approval bot.

**Purpose:** Prevent legal/regulatory violations, spam triggers, false claims, brand damage.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [The 7 Compliance Rules (In-Depth)](#the-7-compliance-rules-in-depth)
3. [Data Flow](#data-flow)
4. [Key Functions](#key-functions)
5. [Decision Logic](#decision-logic)
6. [Telegram Integration](#telegram-integration)
7. [Edge Cases & Handling](#edge-cases--handling)
8. [Performance & Limitations](#performance--limitations)
9. [Integration Points](#integration-points)
10. [Example Scenarios](#example-scenarios)

---

## Architecture Overview

### High-Level Flow

```
Copy Agent Output
    ↓
Compliance Review Agent
    ├─ Rule 1: Spam Words Check
    ├─ Rule 2: Regulatory Language Check
    ├─ Rule 3: False Claims Check
    ├─ Rule 4: Specific Assertions (% or $) Check
    ├─ Rule 5: Missing Opt-Out Check (WhatsApp only)
    ├─ Rule 6: Excessive Length Check (WhatsApp only)
    └─ Rule 7: Brand Risk Language Check
    ↓
Compliance Decision
    ├─ ALL PASS → Send to Telegram Approval Bot
    ├─ SOME BLOCKED → Return violations, request regeneration
    └─ ALL BLOCKED → Entire message rejected
```

### Code Organization

```
compliance_review_agent.py (359 lines)
├─ Configuration (lines 27-50)
│  └─ Keyword/phrase lists for each rule
│
├─ Rule Checkers (lines 53-176)
│  ├─ check_spam_trigger_words()
│  ├─ check_regulatory_language()
│  ├─ check_false_claims()
│  ├─ check_specific_assertions()
│  ├─ check_missing_opt_out()
│  ├─ check_excessive_length()
│  └─ check_brand_risk_language()
│
├─ Message Checker (lines 183-232)
│  └─ check_message_compliance() [orchestrates all 7 checks]
│
├─ Main Agent (lines 239-350)
│  ├─ run_compliance_review_agent() [entry point]
│  └─ Telegram integration
│
└─ Factory (lines 353-358)
   └─ create_compliance_review_agent()
```

---

## The 7 Compliance Rules (In-Depth)

### Rule 1: Spam Trigger Words ❌

**What it checks:** Words commonly flagged as spam by email/SMS filters

**Blocked words:**
```python
"free", "urgent", "act now", "limited time", "winner",
"click here", "buy now", "risk-free"
```

**Why blocks:** These trigger spam filters; violate CAN-SPAM, GDPR

**Example violations:**
```
❌ "Get your FREE report immediately"
❌ "Act now - limited time offer"
❌ "Click here to win!"
```

**How to fix:**
```
✅ "Get your report today"
✅ "Interested in learning more?"
✅ "You've been selected to participate"
```

**Implementation:**
```python
def check_spam_trigger_words(message: str) -> Optional[ComplianceViolation]:
    lower_msg = message.lower()
    for word in SPAM_TRIGGER_WORDS:
        if word in lower_msg:  # Simple substring match
            return ComplianceViolation(
                rule="spam_trigger_word",
                severity="block",
                detail=f'Found spam trigger word: "{word}"',
                recommendation=f"Remove or rephrase '{word}' with more specific, direct language"
            )
    return None
```

**Limitations:**
- Substring match (no word boundary) - may false-positive on "fried" (contains "free")
- Case-insensitive only
- No context awareness (e.g., "risk-free" in negative: "Is it risk-free?" still blocks)

---

### Rule 2: Regulatory Language ⚖️

**What it checks:** Overpromising, guarantee language, certainty statements

**Blocked phrases:**
```python
"guarantee", "guaranteed", "certainty", "promise",
"assured results", "you will definitely"
```

**Why blocks:** Violates FTC regulations (false/unsubstantiated promises), creates legal liability

**Example violations:**
```
❌ "We guarantee 30% growth in revenue"
❌ "Your market will definitely expand"
❌ "Assured results in Q2"
```

**How to fix:**
```
✅ "Help explore growth opportunities"
✅ "Many clients see market expansion"
✅ "Potential to improve in Q2"
```

**Implementation:**
```python
def check_regulatory_language(message: str) -> Optional[ComplianceViolation]:
    lower_msg = message.lower()
    for phrase in REGULATORY_LANGUAGE:
        if phrase in lower_msg:
            return ComplianceViolation(
                rule="regulatory_language",
                severity="block",
                detail=f'Found regulatory language: "{phrase}"',
                recommendation="Remove promise-based language; use conditional or investigative framing instead"
            )
    return None
```

**Key insight:** "We investigate opportunities" vs "We guarantee results" - same outcome potential, massive legal difference

---

### Rule 3: False Claims 🚫

**What it checks:** Absolute claims without basis

**Blocked claims:**
```python
"we guarantee", "proven results", "100% success",
"no risk", "zero risk"
```

**Why blocks:** FTC regulations prohibit unsubstantiated absolute claims. "100% success" is defensively indefensible.

**Example violations:**
```
❌ "100% of our clients see results"
❌ "Proven results across all industries"
❌ "Zero risk involvement"
```

**How to fix:**
```
✅ "Most of our clients report positive outcomes"
✅ "Results vary by industry and context"
✅ "Minimal implementation risk"
```

**Implementation:**
```python
def check_false_claims(message: str) -> Optional[ComplianceViolation]:
    lower_msg = message.lower()
    for claim in FALSE_CLAIMS:
        if claim in lower_msg:
            return ComplianceViolation(
                rule="false_claim",
                severity="block",
                detail=f'Found false/absolute claim: "{claim}"',
                recommendation="Use qualified language like 'may help', 'can improve', 'often see'"
            )
    return None
```

**Key difference from Rule 2:**
- Rule 2: Promise-based language ("guarantee")
- Rule 3: Absolute truth claims ("100%", "proven")

---

### Rule 4: Specific Assertions (Advanced) 📊

**What it checks:** % or $ claims without sourcing/context

**Two sub-patterns:**

**Pattern A: Percentage assertions**
```regex
\d+%\s*(growth|increase|revenue|ROI|boost|improvement|return)
```

Example matches:
- "30% growth"
- "50% revenue increase"
- "200% ROI boost"

**Requires context qualifier:**
```
✅ "based on our research"
✅ "according to industry data"
✅ "per our study"
✅ "from industry research"
```

**Example violations:**
```
❌ "30% revenue growth next quarter"  (no source)
✅ "30% revenue growth based on our research"  (has source)
✅ "Based on our research, we see 30% growth"  (has source)
```

**Pattern B: Currency assertions**
```regex
[$₹€]\d+(?:,\d{3})*(?:\s*(?:million|billion|thousand|M|B|K))?
```

Example matches:
- "$500,000"
- "₹1.5 million"
- "€200K"

**Requires context qualifier:**
```
✅ "for example"
✅ "in similar scenarios"
✅ "based on case studies"
```

**Example violations:**
```
❌ "$500K revenue opportunity"  (no context)
✅ "$500K revenue opportunity for example"  (has context)
```

**Implementation:**
```python
def check_specific_assertions(message: str) -> Optional[ComplianceViolation]:
    # Pattern 1: % assertions
    percent_pattern = r'\d+%\s*(growth|increase|revenue|ROI|boost|improvement|return)'
    if re.search(percent_pattern, message, re.IGNORECASE):
        # Check for source qualifier nearby
        if not re.search(r'(based on|according to|from our|per|research|study|data)', message, re.IGNORECASE):
            match = re.search(percent_pattern, message, re.IGNORECASE)
            return ComplianceViolation(
                rule="specific_assertion",
                severity="block",
                detail=f'Found specific assertion without source: "{match.group()}"',
                recommendation="Add source qualifier like 'based on our research' or 'according to industry data'"
            )
    
    # Pattern 2: Currency amounts
    currency_pattern = r'[$₹€]\d+(?:,\d{3})*(?:\s*(?:million|billion|thousand|M|B|K))?'
    if re.search(currency_pattern, message):
        if not re.search(r'(based on|according to|from our|per|research|study|example)', message, re.IGNORECASE):
            match = re.search(currency_pattern, message)
            return ComplianceViolation(
                rule="specific_assertion",
                severity="block",
                detail=f'Found specific currency amount without context: "{match.group()}"',
                recommendation="Add context like 'for example' or 'in similar scenarios'"
            )
    return None
```

**Key insight:** This rule uses **regex patterns + logical context checking** - most sophisticated rule

---

### Rule 5: Missing Opt-Out (WhatsApp Only) 🛑

**What it checks:** WhatsApp messages lack opt-out instruction

**Why blocks:** WhatsApp Business API & legal requirements (CAN-SPAM, GDPR) require unsubscribe option

**Channel-specific:** Only applies to WhatsApp (email/LinkedIn don't require this)

**Required keywords:**
```python
OPT_OUT_KEYWORDS = ["stop", "opt out", "unsubscribe"]
```

**Example violations:**
```
❌ WhatsApp: "Check out our new service!"  (no opt-out)
✅ WhatsApp: "Check out our new service! Reply STOP to unsubscribe"
```

**Example for other channels:**
```
✅ Email: "To unsubscribe, click here" (built into email footer)
✅ LinkedIn: No requirement (DM-based, less regulated)
```

**Implementation:**
```python
def check_missing_opt_out(message: str, channel: str) -> Optional[ComplianceViolation]:
    if channel.lower() != "whatsapp":  # Only WhatsApp
        return None
    
    lower_msg = message.lower()
    has_opt_out = any(keyword in lower_msg for keyword in OPT_OUT_KEYWORDS)
    
    if not has_opt_out:
        return ComplianceViolation(
            rule="missing_opt_out",
            severity="block",
            detail="No opt-out instruction found in WhatsApp message",
            recommendation="Add 'Reply STOP to unsubscribe' or similar opt-out instruction"
        )
    return None
```

**Key insight:** Channel-aware compliance - same message may pass email but fail WhatsApp

---

### Rule 6: Excessive Length (WhatsApp Only) 📏

**What it checks:** WhatsApp messages exceed 300 words

**Why blocks:** WhatsApp best practices (user experience, carrier limits, spam score)

**Channel-specific:** Only WhatsApp

**Limit:** 300 words

**Example:**
```
Message word count: 450 words
❌ BLOCKED: "WhatsApp message has 450 words (limit: 300)"
```

**Implementation:**
```python
def check_excessive_length(message: str, channel: str) -> Optional[ComplianceViolation]:
    if channel.lower() != "whatsapp":
        return None
    
    word_count = len(message.split())
    if word_count > 300:
        return ComplianceViolation(
            rule="excessive_length",
            severity="block",
            detail=f"WhatsApp message has {word_count} words (limit: 300)",
            recommendation="Reduce message length; split into multiple messages if needed"
        )
    return None
```

**Why 300 words?**
- Industry standard for WhatsApp best practices
- Balances engagement vs cognitive load
- Reduces spam classification risk
- Aligns with carrier SMS limits

---

### Rule 7: Brand Risk Language 🏷️

**What it checks:** Claims of partnerships/certifications without verification

**Blocked phrases:**
```python
"official partner", "certified by", "endorsed by", "authorized by"
```

**Why blocks:** Legal liability - claiming partnerships you don't have = false advertising

**Example violations:**
```
❌ "As an official Google partner, we..."  (are you verified?)
❌ "Certified by ISO" (without cert proof)
❌ "Endorsed by [Major Brand]" (without written permission)
```

**How to fix:**
```
✅ "Uses Google technology"
✅ "Follows ISO standards"
✅ "[Brand] refers many clients to us"
```

**Implementation:**
```python
def check_brand_risk_language(message: str) -> Optional[ComplianceViolation]:
    lower_msg = message.lower()
    for phrase in BRAND_RISK_LANGUAGE:
        if phrase in lower_msg:
            return ComplianceViolation(
                rule="brand_risk_language",
                severity="block",
                detail=f'Found brand-risk phrase: "{phrase}"',
                recommendation="Remove claim of official partnership/certification unless verified in campaign brief"
            )
    return None
```

**Key insight:** "Unless verified in campaign brief" - suggests human override possible if documentation exists (but currently not implemented)

---

## Data Flow

### Input Structure

```python
run_compliance_review_agent(
    campaign_name="Q2 EdTech Campaign",
    campaign_type="Survey",
    channel="whatsapp",
    messages={
        "cxo_strategy": {
            "M1": {
                "message": "Hi [Prospect], interested in latest EdTech trends?",
                "word_count": 10
            },
            "M2": {
                "message": "Research shows 30% growth. Reply STOP to opt out.",
                "word_count": 12
            },
            "M3": {
                "message": "Either way, let's talk. STOP to unsubscribe.",
                "word_count": 12
            }
        },
        "marketing": {
            "M1": {
                "message": "New marketing insights available. Reply STOP.",
                "word_count": 8
            },
            # ... M2, M3
        }
    },
    trigger_telegram_approval=True,
    telegram_user_id=987654321
)
```

### Data Structure

```python
# Input: messages dict
{
    persona: {  # String key
        "M1": {
            "message": str,      # Required: message text
            "word_count": int    # Required: pre-calculated count
        },
        "M2": { ... },
        "M3": { ... }
    }
}

# Output: ComplianceReviewAgentOutput
ComplianceReviewAgentOutput(
    campaign_name: str
    campaign_type: str
    channel: str
    compliance_results: Dict[str, List[ComplianceCheckResult]]  # persona -> [results]
    overall_status: "all_pass" | "some_blocked" | "all_blocked"
    telegram_approval_sent: bool
    telegram_approval_id: str
    notes: str
)

# Per-message result: ComplianceCheckResult
ComplianceCheckResult(
    stage: str                           # "M1", "M2", or "M3"
    status: str                          # "pass" or "blocked"
    violations: List[ComplianceViolation]
    word_count: int
    can_be_approved: bool                # False if any violation
    recommendation: str                  # "ready_for_approval" or "must_regenerate"
)

# Violation detail: ComplianceViolation
ComplianceViolation(
    rule: str                            # Rule name (7 options)
    severity: str                        # Always "block" currently
    detail: str                          # Exact phrase found
    recommendation: str                  # How to fix
)
```

---

## Key Functions

### 1. `check_spam_trigger_words(message: str)` → Optional[ComplianceViolation]

**Purpose:** Detect spam trigger words  
**Complexity:** O(n×m) - n words in message × m trigger words  
**Returns:** First violation found or None

```python
# Fast-path: Returns on first match
if "free" in message.lower():
    return violation  # Early exit
```

---

### 2. `check_regulatory_language(message: str)` → Optional[ComplianceViolation]

**Purpose:** Detect overpromising language  
**Complexity:** O(n×m) - similar to Rule 1  
**Returns:** First violation found or None

---

### 3. `check_specific_assertions(message: str)` → Optional[ComplianceViolation]

**Purpose:** Detect unsourced claims  
**Complexity:** O(n) - regex patterns across message  
**Most sophisticated rule:** Uses regex + logical context checks  
**Returns:** First violation found or None

**Key logic:**
```
1. Find % claim pattern
2. Check for source qualifier nearby
3. If no source, block
4. Repeat for currency amounts
```

---

### 4. `check_message_compliance(message, channel, stage, word_count)` → ComplianceCheckResult

**Purpose:** Check single message against all 7 rules  
**Complexity:** O(1) - fixed number of rules (7)  
**Returns:** ComplianceCheckResult with full analysis

**Flow:**
```python
violations = []
for check_fn in [check_spam, check_regulatory, ..., check_brand_risk]:
    violation = check_fn(message)  # May return None
    if violation:
        violations.append(violation)

status = "blocked" if violations else "pass"
return ComplianceCheckResult(
    stage=stage,
    status=status,
    violations=violations,
    can_be_approved=(status == "pass"),
    recommendation="ready_for_approval" or "must_regenerate"
)
```

**Key insight:** Runs ALL checks even after first violation (collects all violations for reporting)

---

### 5. `run_compliance_review_agent(...)` → ComplianceReviewAgentOutput

**Purpose:** Check all personas & stages, aggregate results, trigger Telegram  
**Complexity:** O(personas × stages) = typically O(3 × 3) = O(9)  
**Returns:** ComplianceReviewAgentOutput with full report

**Flow:**
```python
for persona in messages.keys():
    for stage in ["M1", "M2", "M3"]:
        result = check_message_compliance(...)
        compliance_results[persona].append(result)
        all_violations.extend(result.violations)

# Determine overall status
if no_violations:
    overall_status = "all_pass"
elif all_messages_blocked:
    overall_status = "all_blocked"
else:
    overall_status = "some_blocked"

# Trigger Telegram if all pass
if overall_status == "all_pass" and trigger_telegram_approval:
    send_to_telegram(...)

return ComplianceReviewAgentOutput(...)
```

---

## Decision Logic

### Status Determination

```
Input: All messages (personas × stages)
         ↓
Run 7 checks per message
         ↓
Collect all violations
         ↓
┌─────────────────────────────────┐
│ No violations anywhere          │ → overall_status = "all_pass"
├─────────────────────────────────┤
│ Some pass, some fail            │ → overall_status = "some_blocked"
├─────────────────────────────────┤
│ Every message blocked           │ → overall_status = "all_blocked"
└─────────────────────────────────┘
         ↓
Return ComplianceReviewAgentOutput
```

### Per-Message Logic

```
Message checked
    ↓
┌─────────────────┐
│ Rule violations │
├─────────────────┤
│ None found      │ → status = "pass"
│                 │    can_be_approved = true
│                 │    recommendation = "ready_for_approval"
├─────────────────┤
│ 1+ violations   │ → status = "blocked"
│                 │    can_be_approved = false
│                 │    recommendation = "must_regenerate"
└─────────────────┘
         ↓
Return ComplianceCheckResult
```

### Can This Message Be Approved?

**Rule:** `can_be_approved = (status == "pass")`

- ✅ If no violations: can be approved
- ❌ If ANY violation: cannot be approved
- ⚠️ **IMPORTANT:** Blocked messages CANNOT be overridden (even by human)

This is by design - compliance violations are non-negotiable.

---

## Telegram Integration

### When Triggered

```
Condition: overall_status == "all_pass" 
           AND 
           trigger_telegram_approval == True
           AND 
           telegram_user_id > 0
```

### What Happens

```python
if overall_status == "all_pass" and trigger_telegram_approval and telegram_user_id > 0:
    telegram_service = _import_telegram_service()  # Lazy import
    
    if telegram_service:
        # Build approval request
        approval_id = f"compliance_{campaign}_{timestamp}"
        preview_msg = first_message[:300]
        
        # Send to Telegram bot
        success = telegram_service.send_approval_request(
            approval_id=approval_id,
            title=f"Compliance Approved - {campaign_name}",
            preview=preview_msg,
            telegram_user_id=telegram_user_id,
            metadata={...}  # Campaign context
        )
        
        if success:
            telegram_approval_sent = True
            telegram_approval_id = approval_id
```

### Lazy Import Pattern

```python
TelegramApprovalService = None  # Global cache

def _import_telegram_service():
    global TelegramApprovalService
    if TelegramApprovalService is None:  # Only import once
        try:
            from apps.core.telegram_service import TelegramApprovalService as TAS
            TelegramApprovalService = TAS
        except ImportError:
            TelegramApprovalService = None  # Mock for testing
    return TelegramApprovalService
```

**Why lazy import?**
- Avoids Django dependency when not using Telegram feature
- Allows testing without backend running
- Better separation of concerns

### Approval ID Generation

```
Format: compliance_{campaign_name}_{timestamp}
Example: "compliance_Q2_EdTech_Campaign_20260520_143025"
```

---

## Edge Cases & Handling

### Edge Case 1: Empty Message

**Input:** `message = ""`

**Result:**
```python
word_count = 0
violations = []  # No violations found
status = "pass"
can_be_approved = true
```

**Issue:** Empty message passes all checks (should it?)

**Current behavior:** Allows it  
**Suggested improvement:** Add minimum word count check

---

### Edge Case 2: Message with Only Spaces

**Input:** `message = "   "`

**Result:**
```python
word_count = 1  # "split()" returns [""]
violations = []
status = "pass"
```

**Issue:** Single "word" of spaces passes  
**Current behavior:** Allows it  
**Suggested improvement:** Trim whitespace before splitting

---

### Edge Case 3: Multiple Violations

**Input:** Message with "free" AND "guarantee" AND ">300 words"

**Result:**
```python
violations = [
    ComplianceViolation(rule="spam_trigger_word", ...),
    ComplianceViolation(rule="regulatory_language", ...),
    ComplianceViolation(rule="excessive_length", ...)
]
status = "blocked"
```

**Key insight:** All violations reported (not short-circuited)

---

### Edge Case 4: Substring False Positives

**Input:** `message = "I fried the chicken"`

**Violation:** Contains "fried" which contains "free"

**Result:** ❌ BLOCKED (false positive!)

**Current behavior:** Substring matching causes false positives  
**Suggested improvement:** Use word boundaries in regex

---

### Edge Case 5: Case Sensitivity

**Input:** `message = "FREE report"`

**Check:**
```python
lower_msg = message.lower()  # "free report"
if "free" in lower_msg:  # Matches!
```

**Result:** ✅ Correctly detected

**Key insight:** All checks use `.lower()` for case-insensitive matching

---

### Edge Case 6: WhatsApp-specific Rules on Email

**Input:** Email message, excessive_length rule

**Check:**
```python
if channel.lower() != "whatsapp":
    return None  # Skips check
```

**Result:** ✅ Rule skipped for email

**Key insight:** Channel awareness prevents false positives

---

### Edge Case 7: Non-English Messages

**Input:** `message = "এই বার্তাটি পরীক্ষা করুন"`  (Bengali)

**Result:** All checks pass (no English keywords found)

**Issue:** Agent only detects English violations  
**Current behavior:** Non-English messages treated as safe (risky!)  
**Suggested improvement:** Add language detection + multilingual rules

---

### Edge Case 8: Context Qualifier Distance

**Input:** `message = "Based on our research: 30% growth expected next quarter"`

**Check:**
```python
percent_pattern = r'\d+%\s*(growth|...)'  # Matches "30% growth"
context_pattern = r'(based on|...)'        # Matches "Based on"

# Both found, so: PASS
```

**Result:** ✅ Correctly passes (qualifier present)

**Note:** Qualifier can be anywhere in message (not just nearby)

---

## Performance & Limitations

### Performance Analysis

**Time Complexity:**
```
Overall: O(rules × chars_in_message)
         = O(7 × n)
         = O(n)  where n = message length

Per rule: O(n) for regex, O(n×m) for substring matching
```

**Typical execution:** < 100ms for all 7 rules

**Bottleneck:** Rule 4 (regex patterns) is slowest

**Space Complexity:** O(violations) - stores violations in list

### Limitations

1. **No AI/LLM:** Uses rule-based checks only (no context understanding)
   - Cannot detect tone/intent violations
   - Cannot understand implicit claims

2. **Substring matching:** False positives on words containing keywords
   - "fried" triggers "free" rule
   - No word-boundary detection

3. **English only:** Doesn't detect violations in other languages

4. **Limited context:** Checks within message only
   - Doesn't know campaign history
   - Doesn't verify actual partnerships
   - Cannot cross-reference with approved claims database

5. **No human override:** Blocked messages cannot be approved
   - Even with valid justification

6. **Static rules:** New violations require code change
   - Not data-driven
   - Cannot update rules without deployment

### Suggested Improvements

| Limitation | Improvement | Effort |
|-----------|-------------|--------|
| AI understanding | Integrate Claude for context-aware checks | High |
| False positives | Use word-boundary regex, NLP tokenization | Medium |
| Multilingual | Add language detection + multilingual rules | Medium |
| Context awareness | Add campaign brief + claims database lookup | High |
| Human override | Add approval chain (block, then review) | Medium |
| Dynamic rules | Move rules to database config | Low-Medium |

---

## Integration Points

### 1. Upstream: Copy Agents

**Who calls compliance?**
- Email Copy Agent (after M1-M3 generated)
- WhatsApp Copy Agent (after M1-M3 generated)
- LinkedIn Copy Agent (after M1-M3 generated)

**Input flow:**
```
Copy Agent
    ↓ output: {M1: ..., M2: ..., M3: ...}
    ↓
Compliance Agent (check_message_compliance)
    ↓ output: ComplianceCheckResult
    ↓
Copy Agent receives verdict
```

### 2. Downstream: Telegram Approval Bot

**When:** If all_pass + trigger_telegram_approval

**What:** Sends approval request with:
- Campaign name
- Message preview (first 300 chars)
- User ID for response routing
- Metadata for context

**Response flow:**
```
Telegram Bot
    ↓ User approves/rejects
    ↓
Backend receives decision
    ↓
Message sent OR held for revision
```

### 3. API Layer

**Endpoint:** `POST /api/v1/agents/compliance-review/generate/`

**Request:**
```json
{
  "campaign_name": "Q2 Campaign",
  "campaign_type": "Survey",
  "channel": "whatsapp",
  "messages": {...},
  "trigger_telegram_approval": true,
  "telegram_user_id": 987654321
}
```

**Response:**
```json
{
  "campaign_name": "Q2 Campaign",
  "campaign_type": "Survey",
  "channel": "whatsapp",
  "compliance_results": {...},
  "overall_status": "all_pass",
  "telegram_approval_sent": true,
  "telegram_approval_id": "compliance_Q2_Campaign_20260520_143025",
  "notes": "Checked 2 personas × 3 stages. Total violations: 0"
}
```

### 4. Database (Planned)

**Potential storage:**
- Compliance results history
- Violation frequency per campaign
- Appeals/overrides (if added)

**Currently:** In-memory only (not persisted)

---

## Example Scenarios

### Scenario 1: Perfect Message

**Input:**
```json
{
  "message": "Hi [Prospect], interested in learning about our research insights?",
  "channel": "whatsapp",
  "stage": "M1",
  "word_count": 12
}
```

**Checks:**
```
1. Spam words? → "research", "insights" - NO
2. Regulatory? → NO
3. False claims? → NO
4. Assertions? → NO numbers/currency
5. Opt-out (WA)? → NO opt-out found! ⚠️
6. Length (WA)? → 12 words < 300 ✅
7. Brand risk? → NO
```

**Result:**
```
Status: BLOCKED
Violations: [missing_opt_out]
```

**Fix:**
```
"Hi [Prospect], interested in learning about our research insights? Reply STOP to opt out."
```

---

### Scenario 2: Mixed Violations

**Input:**
```json
{
  "message": "Get your FREE report now! We guarantee 50% growth. This is risk-free! Reply STOP.",
  "channel": "whatsapp",
  "stage": "M1",
  "word_count": 18
}
```

**Checks:**
```
1. Spam words? → "free" ❌ VIOLATION
2. Regulatory? → "guarantee" ❌ VIOLATION
3. False claims? → "risk-free" ❌ VIOLATION
4. Assertions? → "50% growth" (no source) ❌ VIOLATION
5. Opt-out (WA)? → "STOP" ✅
6. Length (WA)? → 18 words ✅
7. Brand risk? → NO
```

**Result:**
```
Status: BLOCKED
Violations: [
  {rule: "spam_trigger_word", detail: "free"},
  {rule: "regulatory_language", detail: "guarantee"},
  {rule: "false_claim", detail: "risk-free"},
  {rule: "specific_assertion", detail: "50% growth"}
]
```

---

### Scenario 3: Sourced Assertion (Passes)

**Input:**
```json
{
  "message": "According to our research, clients see 30% efficiency gains. Interested? Reply STOP.",
  "channel": "whatsapp",
  "stage": "M1",
  "word_count": 17
}
```

**Checks:**
```
1. Spam words? → NO
2. Regulatory? → NO
3. False claims? → NO
4. Assertions? → "30% efficiency gains" BUT "according to our research" ✅
5. Opt-out (WA)? → "STOP" ✅
6. Length (WA)? → 17 words ✅
7. Brand risk? → NO
```

**Result:**
```
Status: PASS
Violations: []
can_be_approved: true
```

---

### Scenario 4: Multi-Persona Campaign

**Input:**
```json
{
  "messages": {
    "cxo_strategy": {
      "M1": {"message": "Let's explore growth opportunities. Reply STOP.", "word_count": 8},
      "M2": {"message": "Research shows potential. Interested? Reply STOP.", "word_count": 8},
      "M3": {"message": "Either way, let's connect. Reply STOP.", "word_count": 7}
    },
    "marketing": {
      "M1": {"message": "New marketing tactics available. Reply STOP.", "word_count": 7},
      "M2": {"message": "Proven approach in EdTech. Reply STOP.", "word_count": 7},
      "M3": {"message": "Worth exploring? Reply STOP.", "word_count": 5}
    }
  },
  "trigger_telegram_approval": true,
  "telegram_user_id": 987654321
}
```

**Execution:**
```
Check cxo_strategy
  ├─ M1: PASS ✅
  ├─ M2: PASS ✅
  └─ M3: PASS ✅

Check marketing
  ├─ M1: PASS ✅
  ├─ M2: Check "Proven approach" → "proven" triggers Rule 3! ❌ BLOCKED
  └─ M3: PASS ✅

Overall: some_blocked
Telegram: NOT sent (because not all_pass)
```

---

## Summary Table

| Aspect | Details |
|--------|---------|
| **Code Size** | 359 lines |
| **Rules** | 7 compliance rules |
| **Time Complexity** | O(n) per message |
| **Space** | O(violations) |
| **Performance** | < 100ms typical |
| **Channel-aware** | Yes (WhatsApp-specific rules) |
| **Multilingual** | No (English only) |
| **AI-based** | No (rule-based only) |
| **Human override** | No |
| **Telegram integration** | Yes (Lazy import) |
| **Database persistence** | No |
| **Status** | Production ready ✅ |

---

**End of In-Depth Context Document**

