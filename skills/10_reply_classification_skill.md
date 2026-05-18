# Skill: Reply Classification

**Used by:** Reply Classifier Agent  
**Domain:** Inbound reply intent detection

---

## Purpose
Provides the intent category definitions, signal detection rules, confidence scoring guidance, and recommended next actions for classifying inbound replies across all channels.

---

## When to use
When any inbound reply is received on Email, WhatsApp, or LinkedIn.

---

## Intent category definitions

### `positive_interest`
Signals: expressions of curiosity, desire to learn more, positive acknowledgement.
Keywords: "interested", "tell me more", "sounds relevant", "would like to know", "good timing", "can you share".
Confidence: High if two or more signals present.

### `meeting_request`
Signals: direct asks for a call, meeting, demo, or conversation.
Keywords: "schedule", "call", "connect", "available", "calendar", "book", "meet", "chat".
Confidence: High if scheduling intent is explicit.

### `question`
Signals: interrogative reply, asking for clarification, asking who sent this.
Keywords: "what is this", "who are you", "can you explain", "what report", "which company".
Confidence: High if question mark present and no negative signals.

### `negative`
Signals: rejection, disinterest, wrong target, opt-out.
Keywords: "not interested", "remove me", "don't contact", "unsubscribe", "wrong person", "not relevant", "no thanks", "stop".
Confidence: High if any strong negative keyword present.

### `out_of_office`
Signals: automated reply format, return date mentioned, cover contact named.
Patterns: "I am currently out", "I will be back", "automatic reply", "out of office".

### `bounce`
Signals: delivery failure header, NDR format, mail system message.
Patterns: "Delivery failed", "Message undeliverable", "550", "554".

### `ambiguous`
Signals: reply is too short to classify, reply is in unexpected language, reply is a forward or FYI.

---

## Confidence scoring
- Two or more strong signals → 80–100
- One strong signal + context → 60–80
- One weak signal only → 40–60
- No clear signals → < 40 (flag as ambiguous)

---

## Rules
- Stop flag is issued before classification — always
- OOO replies do not create suppression records
- Bounce replies update prospect email validity, not suppression
- Low confidence (< 60) always flags for human review

---

## Failure cases
- Reply in a non-English language → translate, then classify; flag as translated
- Reply is a forwarded thread (no direct reply from prospect) → classify as ambiguous
