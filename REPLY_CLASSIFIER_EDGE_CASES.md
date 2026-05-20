# Reply Classifier - Edge Cases Coverage

**Purpose:** List ALL edge cases covered so you can identify gaps & add missing ones

**Format:** Edge Case Category → Specific Cases Covered → Example

---

## 1. EMPTY/MINIMAL REPLY EDGE CASES (8 covered)

### What's Covered:
- [ ] Completely empty reply (blank text)
- [ ] Single character ("?", ".", "!")
- [ ] Only whitespace/spaces
- [ ] Only punctuation (...)
- [ ] Single word ("Yes", "No", "Maybe")
- [ ] Two letter replies ("K", "OK", "Hi")
- [ ] Just signature, no message
- [ ] Just emoji, no text

**Decision:** → All classify as **AMBIGUOUS** with low confidence (30-50)

---

## 2. TYPO/GARBLED TEXT EDGE CASES (6 covered)

### What's Covered:
- [ ] Misspelled words ("Intrested", "Schdeule")
- [ ] Missing vowels ("Whns gd")
- [ ] Number substitution ("4 u" instead of "for you")
- [ ] Autocorrect failures ("wy" instead of "why")
- [ ] Multiple typos in one word
- [ ] Keyboard mash ("jkh@#$%")

**Decision:** → Classify as **AMBIGUOUS**, flag for review (40-55 confidence)

---

## 3. LANGUAGE/ENCODING EDGE CASES (4 covered)

### What's Covered:
- [ ] Non-English language (French, Spanish, Chinese, etc.)
- [ ] Mixed languages in one reply ("Hello, merci beaucoup")
- [ ] RTL languages (Arabic, Hebrew)
- [ ] Special characters/encoding issues

**Decision:** → Classify as **AMBIGUOUS** (20-40 confidence)

---

## 4. EMOJI/SYMBOL ONLY EDGE CASES (3 covered)

### What's Covered:
- [ ] Emoji only ("😀👍🙌")
- [ ] Mixed emoji + punctuation ("👎❌")
- [ ] Symbol only (">>>" or "<<<")

**Decision:** → Classify as **AMBIGUOUS** (25-45 confidence)

---

## 5. FORWARDING/CONTEXT EDGE CASES (5 covered)

### What's Covered:
- [ ] Multiple forwarding layers ("Fwd: Fwd: Fwd:")
- [ ] Forwarded message with no new reply
- [ ] Only quoted original email, no new text
- [ ] Forwarded + signature only
- [ ] Calendar invite with no accompanying message

**Decision:** → Classify as **AMBIGUOUS** (30-50 confidence)

---

## 6. CONFLICTING SIGNALS EDGE CASES (7 covered)

### What's Covered:
- [ ] Interest + Rejection ("Interested but not now")
- [ ] Positive + Negative ("Good idea but can't afford")
- [ ] Question + Rejection ("Why would we need this?")
- [ ] Meeting request + Out of Office ("Can we schedule? Currently out")
- [ ] Multiple intents mixed ("Tell me more but also remove me from list")
- [ ] Conditional interest + objection ("If affordable, but unlikely")
- [ ] Enthusiasm + but ("Sounds great but I'm leaving the company")

**Decision:** → Classify as **AMBIGUOUS**, requires human review (40-60 confidence)

---

## 7. INCOMPLETE/CONTEXTUAL EDGE CASES (6 covered)

### What's Covered:
- [ ] Reply with broken link/attachment reference
- [ ] "Can't read attachment, resend?"
- [ ] "Image didn't load"
- [ ] Reply implies prior context not visible
- [ ] "Similar to what you said" (ambiguous what context)
- [ ] "My bad, ignore previous email"

**Decision:** → Classify as **AMBIGUOUS** (35-55 confidence)

---

## 8. TIMING AMBIGUITY EDGE CASES (5 covered)

### What's Covered:
- [ ] "Eventually" (vague future)
- [ ] "We'll think about it" (procrastination vs interest)
- [ ] "Will review and get back" (no clear intent)
- [ ] "Let me check with team" (approval or rejection coming?)
- [ ] "Sometime this year" (unclear commitment)

**Decision:** → Classify as **AMBIGUOUS** (45-60 confidence)

---

## 9. BOUNDARY KEYWORD EDGE CASES (8 covered)

### What's Covered:
- [ ] Words containing other signals ("fried" contains "free")
- [ ] "Can't" vs "Can" (negation detection)
- [ ] Case variations ("INTERESTED" vs "interested")
- [ ] Punctuation placement ("Tell.me.more" vs "Tell me more")
- [ ] Hyphenated words ("out-of-office")
- [ ] Possessives ("What's" vs "What is")
- [ ] Contractions ("Can't", "Won't", "Shouldn't")
- [ ] Abbreviations ("ASAP", "BTW", "IMHO")

**Decision:** → Normalize & match with case-insensitive, punctuation-flexible matching

---

## 10. SENTIMENT MODIFIER EDGE CASES (6 covered)

### What's Covered:
- [ ] Sarcasm ("Oh wonderful, another vendor pitch")
- [ ] Negativity with positive words ("Fantastic that you reached out, too bad we can't help")
- [ ] Half-hearted agreement ("Sure, I guess")
- [ ] False enthusiasm ("Amazing! *said no one*")
- [ ] Passive aggressive ("That's nice")
- [ ] Backhanded compliment ("Interesting concept, but impractical")

**Decision:** → Classify based on overall signal weight, flag for manual review (50-65 confidence)

---

## 11. PERSON/DELEGATION EDGE CASES (5 covered)

### What's Covered:
- [ ] "Not my department, ask [person]"
- [ ] "Forwarding to [team]"
- [ ] "My boss will follow up"
- [ ] "I'll have [colleague] handle this"
- [ ] "Wrong person, try [company email]"

**Decision:** → Classify based on context:
- If forwarding = could be POSITIVE INTEREST (delegation)
- If wrong person = AMBIGUOUS (may need re-routing)

---

## 12. DEADLINE/URGENCY EDGE CASES (4 covered)

### What's Covered:
- [ ] "ASAP" in negative context ("Remove me ASAP")
- [ ] "URGENT" in spam context
- [ ] "Need this by Friday" (implied deadline without clear intent)
- [ ] Time pressure signals that could be positive or negative

**Decision:** → Parse context before deciding intent

---

## 13. SYSTEM/TECHNICAL ERROR EDGE CASES (7 covered)

### What's Covered:
- [ ] Email delivery NDR codes (550, 551, 552, 553, 554, etc.)
- [ ] Bounce messages with multiple error codes
- [ ] Partial delivery (some recipients worked, some failed)
- [ ] Generic system errors ("Something went wrong")
- [ ] Mail server response codes
- [ ] Rate limiting messages
- [ ] Quota exceeded messages

**Decision:** → Classify as **BOUNCE**, update prospect record

---

## 14. LENGTH EDGE CASES (4 covered)

### What's Covered:
- [ ] Extremely long reply (1000+ words)
- [ ] Very short reply (1-2 words)
- [ ] Reply longer than original message
- [ ] Multi-paragraph with mixed intents

**Decision:** → Parse each paragraph separately if needed, then aggregate intent

---

## 15. AUTO-REPLY EDGE CASES (7 covered)

### What's Covered:
- [ ] Standard OOO auto-reply
- [ ] OOO with return date
- [ ] OOO with delegation
- [ ] Limited access OOO
- [ ] Partial OOO (weekends only, evenings only)
- [ ] Auto-responder from system (non-human)
- [ ] "Unable to deliver" system bounce

**Decision:** → Classify as **OUT OF OFFICE**, extract return date, pause automation

---

## 16. CONDITIONAL/HYPOTHETICAL EDGE CASES (5 covered)

### What's Covered:
- [ ] "If you can do X, then interested"
- [ ] "Depends on pricing"
- [ ] "Would consider if you integrate with Y"
- [ ] "Maybe if budget allows"
- [ ] "Only if you can meet these requirements"

**Decision:** → Classify as **POSITIVE INTEREST** (conditional) with medium confidence (65-75)

---

## 17. NEGATIVE WITH REASON EDGE CASES (6 covered)

### What's Covered:
- [ ] "Not interested because already using X"
- [ ] "Can't afford" (budget reason)
- [ ] "Wrong person" (responsibility reason)
- [ ] "Not our industry" (fit reason)
- [ ] "Already have solution" (competitive reason)
- [ ] "Bad timing" (timing reason)

**Decision:** → Classify as **NEGATIVE**, log reason for insights

---

## 18. QUESTION AMBIGUITY EDGE CASES (5 covered)

### What's Covered:
- [ ] Rhetorical questions ("How is this even possible?")
- [ ] Questions as objections ("Why would we need this?")
- [ ] Questions as skepticism ("Do you actually have proof?")
- [ ] Single-word questions ("Cost?" "Timeline?")
- [ ] Questions with punctuation variations ("What the...?" "How???")

**Decision:** → Classify as **QUESTION** but note skepticism level

---

## 19. PREVIOUS INTERACTION CONTEXT EDGE CASES (4 covered)

### What's Covered:
- [ ] "As discussed in call yesterday"
- [ ] "Following up on previous conversation"
- [ ] "RE: RE: RE:" (deeply threaded)
- [ ] References to person/event not in current thread

**Decision:** → Classify as **AMBIGUOUS**, flag for context lookup (40-55 confidence)

---

## 20. MULTI-RECIPIENT EDGE CASES (3 covered)

### What's Covered:
- [ ] Reply to all (includes original recipient list)
- [ ] CC'd on reply but not direct recipient
- [ ] BCC'd but included in reply thread
- [ ] Group reply where intent ambiguous about which recipient

**Decision:** → Classify based on text alone, note recipient context

---

## 21. FORMATTING EDGE CASES (5 covered)

### What's Covered:
- [ ] ALL CAPS REPLY
- [ ] MixeD CaSe
- [ ] Multiple line breaks between words
- [ ] HTML entities in plain text (&quot;, &nbsp;, etc.)
- [ ] Markdown formatting (*bold*, _italic_, [links])

**Decision:** → Normalize before matching signals

---

## 22. ATTACHMENT-ONLY EDGE CASES (3 covered)

### What's Covered:
- [ ] Reply with attachment but no text
- [ ] "See attached" with no further explanation
- [ ] File name implies intent ("proposal.pdf", "contract.docx")
- [ ] Image/document as content vs attachment

**Decision:** → Classify as **AMBIGUOUS** (35-50 confidence), flag for manual review

---

## 23. SPAM/PHISHING EDGE CASES (4 covered)

### What's Covered:
- [ ] Obvious spam markers ("You've won!", "Claim your prize!")
- [ ] Phishing attempt patterns
- [ ] Reply from wrong domain (spoofed sender)
- [ ] Malicious links in reply

**Decision:** → Flag for security, classify as **AMBIGUOUS** (security risk)

---

## 24. SOCIAL SIGNAL EDGE CASES (4 covered)

### What's Covered:
- [ ] LinkedIn thumbs up/like only
- [ ] WhatsApp reaction emoji only (👍, ❤️, 😂)
- [ ] Check mark delivery indicator as reply
- [ ] "Seen" notification as engagement

**Decision:** → Classify as **AMBIGUOUS** (25-40 confidence)

---

## 25. REGULATORY/LEGAL EDGE CASES (4 covered)

### What's Covered:
- [ ] "This is harassment, cease and desist"
- [ ] Legal threat in reply
- [ ] "Reported to FTC/legal dept"
- [ ] Formal complaint language

**Decision:** → Classify as **NEGATIVE** (HARSH), escalate to legal team

---

## 26. DUPLICATE/REPETITION EDGE CASES (3 covered)

### What's Covered:
- [ ] Same message repeated multiple times
- [ ] "Please respond" repeated
- [ ] Copy-paste of original message as reply
- [ ] Accidental re-send of same reply

**Decision:** → Classify as **AMBIGUOUS**, note duplication (30-45 confidence)

---

## 27. METADATA MISMATCH EDGE CASES (3 covered)

### What's Covered:
- [ ] Reply says "yes" but subject says "RE: [negative topic]"
- [ ] Timestamp shows immediate reply (likely auto-reply) vs manual
- [ ] Recipient doesn't match sender domain expectations
- [ ] Time of day suggests auto-reply vs manual (e.g., 3am)

**Decision:** → Use metadata to confirm classification, flag conflicts

---

## 28. CHANNEL-SPECIFIC EDGE CASES (6 covered)

### What's Covered:
- [ ] WhatsApp: Only emoji reactions
- [ ] LinkedIn: "Endorsed" skill notification as reply
- [ ] Email: Delivery failure vs actual reply
- [ ] Email: Forward as new reply vs actual reply
- [ ] SMS: Character limit forcing incomplete sentences
- [ ] Different channel reply to different channel message

**Decision:** → Classify per channel norms

---

## Summary of Edge Cases Covered

```
✅ Empty/Minimal Replies:        8 cases
✅ Typos/Garbled Text:           6 cases
✅ Language/Encoding:            4 cases
✅ Emoji/Symbols:                3 cases
✅ Forwarding/Context:           5 cases
✅ Conflicting Signals:          7 cases
✅ Incomplete Context:           6 cases
✅ Timing Ambiguity:             5 cases
✅ Boundary Keywords:            8 cases
✅ Sentiment Modifiers:          6 cases
✅ Person/Delegation:            5 cases
✅ Deadline/Urgency:             4 cases
✅ System/Technical Errors:      7 cases
✅ Length Variations:            4 cases
✅ Auto-Reply:                   7 cases
✅ Conditional/Hypothetical:     5 cases
✅ Negative with Reason:         6 cases
✅ Question Ambiguity:           5 cases
✅ Previous Context:             4 cases
✅ Multi-Recipient:              3 cases
✅ Formatting:                   5 cases
✅ Attachment-Only:              3 cases
✅ Spam/Phishing:                4 cases
✅ Social Signals:               4 cases
✅ Regulatory/Legal:             4 cases
✅ Duplication:                  3 cases
✅ Metadata Mismatch:            3 cases
✅ Channel-Specific:             6 cases
─────────────────────────────────────
TOTAL: 28 CATEGORIES, 139+ EDGE CASES COVERED
```

---

## How to Use This

**Step 1:** Review each edge case category  
**Step 2:** Check ✅ which are covered  
**Step 3:** Identify gaps (not checked)  
**Step 4:** Add missing edge cases yourself  
**Step 5:** Share with team before API creation  

---

## GAPS YOU CAN FILL

**Add your own edge cases here:**

- [ ] [Your edge case 1]
- [ ] [Your edge case 2]
- [ ] [Your edge case 3]
- [ ] ...

---

**Once you review & add missing cases → We move to API creation!** 🚀

