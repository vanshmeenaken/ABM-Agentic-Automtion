# Skill: Message Compliance

**Used by:** Compliance Review Agent  
**Domain:** Outbound message compliance checking

---

## Purpose
Defines the rule set for compliance checking of outbound messages across Email and WhatsApp channels. Provides violation categories, detection rules, and safe edit guidance.

---

## When to use
On every message draft before it enters the human approval queue.

---

## Violation categories and detection rules

### `false_claim`
Triggers when: message asserts specific statistics, client counts, revenue impacts, or outcomes without a verifiable source.

Examples:
- ❌ "We've helped 500+ companies in your sector" (if unverified)
- ❌ "Our research has driven 30% cost reduction for clients"
- ✅ "Our research covers 50+ markets across this sector"

### `regulatory_risk`
Triggers when: message implies guaranteed outcomes, ROI certainty, or investment returns.

Examples:
- ❌ "Guaranteed to improve your competitive position"
- ❌ "Certain to reduce procurement costs by 20%"
- ✅ "Companies using this data have seen improved sourcing outcomes"

### `spam_trigger`
Trigger words: free, urgent, act now, limited time, exclusive offer, click here, guarantee, no obligation, risk-free, buy now, earn money.

### `missing_opt_out` (WhatsApp only)
Triggers when: WhatsApp message does not contain "Reply STOP to opt out" or equivalent.

### `format_violation`
Email: Subject line > 60 characters, HTML detected in plain text body.
WhatsApp: Message > 300 words.

### `brand_risk`
Triggers when: message names a competitor, contains defamatory language, or makes legal claims.

### `ambiguous_claim`
Triggers when: claim is not clearly false but cannot be verified from campaign context. Default to BLOCK.

---

## Safe edit guidance
When issuing a BLOCK, the agent should provide a suggested rewrite that:
- Removes the violation
- Preserves the original intent
- Is shorter and more factually conservative

---

## Rules
- Every check must be run on every message — no shortcuts
- BLOCK cannot be overridden — message must be rewritten
- PASS is logged with all checks passed for audit trail

---

## Failure cases
- Agent cannot determine if claim is verifiable → BLOCK with `ambiguous_claim`
- Message is in a non-English language → translate first, then check
