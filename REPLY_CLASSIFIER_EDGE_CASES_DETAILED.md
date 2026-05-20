# Reply Classifier - All Edge Cases with Exact Examples

**Format:** Category → Specific Case (with example) → Classification → Confidence

---

## CATEGORY 1: EMPTY/MINIMAL REPLIES (8 cases)

### Case 1.1: Completely Empty Reply
**Example:** "" (blank message)
**What it is:** No text, no content
**Classification:** AMBIGUOUS
**Confidence:** 30%
**Handling:** Flag for human review, cannot determine intent

### Case 1.2: Single Punctuation Mark
**Examples:** "?", ".", "!", "...", "---", "***"
**What it is:** Only punctuation, no words
**Classification:** AMBIGUOUS
**Confidence:** 35%
**Handling:** Treat as minimal engagement, requires context

### Case 1.3: Only Whitespace
**Examples:** "   ", "\n\n\n", "\t\t\t"
**What it is:** Only spaces, tabs, or line breaks
**Classification:** AMBIGUOUS
**Confidence:** 25%
**Handling:** Treat same as empty, flag for review

### Case 1.4: Single Character Response
**Examples:** "Y", "N", "1", "0", "✓", "✗"
**What it is:** Single letter or symbol reply
**Classification:** AMBIGUOUS
**Confidence:** 40%
**Handling:** Could mean yes/no but unclear context

### Case 1.5: Generic Acknowledgment
**Examples:** "OK", "K", "Got it", "Sure", "Thanks"
**What it is:** Acknowledgment without intent clarity
**Classification:** AMBIGUOUS
**Confidence:** 45%
**Handling:** Acknowledgment only, intent unclear

### Case 1.6: Very Short Two-Word Reply
**Examples:** "Good timing", "Not interested", "Maybe later"
**What it is:** Two words, minimal context
**Classification:** Could be NEGATIVE, POSITIVE INTEREST, or AMBIGUOUS depending on words
**Confidence:** 50-65%
**Handling:** Parse words for intent signals

### Case 1.7: Just Signature Block
**Example:** 
```
--
John Smith
VP Sales
Acme Corp
john@acme.com
```
**What it is:** Signature only, no message body
**Classification:** AMBIGUOUS
**Confidence:** 20%
**Handling:** Original message stripped, flag for manual check

### Case 1.8: Empty Reply with Metadata Only
**Example:** Reply timestamp shows "Delivered", "Read" status but no text
**What it is:** System shows reply received but content missing
**Classification:** AMBIGUOUS
**Confidence:** 25%
**Handling:** Request resend or clarification

---

## CATEGORY 2: TYPOS/GARBLED TEXT (6 cases)

### Case 2.1: Single Word Misspelled
**Examples:** 
- "Intrested" (Interested)
- "Availble" (Available)
- "Experiance" (Experience)
**Classification:** AMBIGUOUS (if intent word misspelled)
**Confidence:** 50-60%
**Handling:** Fuzzy match against signal words

### Case 2.2: Multiple Words Misspelled in One Reply
**Example:** "Schdeule a meeting asap, intrested in this oferr"
**Classification:** AMBIGUOUS
**Confidence:** 45-55%
**Handling:** Normalize spelling using autocorrect, then classify

### Case 2.3: Missing Vowels
**Examples:**
- "Whts th cst?" (What's the cost?)
- "Whn cn w tlk?" (When can we talk?)
- "Snd dls" (Send details)
**Classification:** AMBIGUOUS (if unreadable)
**Confidence:** 35-50%
**Handling:** Attempt vowel reconstruction, flag if unclear

### Case 2.4: Number/Symbol Substitution
**Examples:**
- "L8r" (Later)
- "2day" (Today)
- "4 u" (For you)
- "ur" (Your)
- "$$$" (Money/cost related)
**Classification:** AMBIGUOUS → Try to decode
**Confidence:** 40-55%
**Handling:** Decode using common texting shortcuts

### Case 2.5: Autocorrect Gone Wrong
**Examples:**
- "I'm not interested, my ducking phone messed this up" (ducking → f-word)
- "Let's schedule a meeting at my local Starbucks" (should be Starbucks, not Star Bucks)
- "Can we discuss the penetration timeline?" (penetration → implementation)
**Classification:** Parse actual intent, ignore autocorrect
**Confidence:** 55-70%
**Handling:** Identify context, not just words

### Case 2.6: Keyboard Mash / Gibberish
**Examples:**
- "jkdhfjkh@#$%jkl"
- "asdfghjkl"
- "qwerty"
**Classification:** AMBIGUOUS
**Confidence:** 15%
**Handling:** Flag as potential accidental send or test

---

## CATEGORY 3: LANGUAGE/ENCODING (4 cases)

### Case 3.1: Entirely Non-English Reply
**Examples:**
- "Merci beaucoup pour cette opportunité" (French)
- "¿Cuándo podemos hablar?" (Spanish - When can we talk?)
- "Terima kasih atas penawaran ini" (Indonesian)
**Classification:** AMBIGUOUS
**Confidence:** 20-40%
**Handling:** Detect language, attempt translation, then classify

### Case 3.2: Mixed Language in Single Reply
**Example:** "Thanks for the info, pero no estamos interesados en este momento" (English + Spanish)
**Classification:** AMBIGUOUS
**Confidence:** 35-50%
**Handling:** Extract English portions, translate others, then classify

### Case 3.3: Right-to-Left Language
**Examples:**
- Arabic: "أنا مهتم بهذا" (I'm interested in this)
- Hebrew: "בואו נדבר על זה" (Let's talk about this)
**Classification:** AMBIGUOUS
**Confidence:** 15-30%
**Handling:** Require manual translation/review

### Case 3.4: Encoding/Character Issues
**Example:** "ÃƒÆ'Ã‚Â¬Ã… ß" (corrupted UTF-8)
**Classification:** AMBIGUOUS
**Confidence:** 20%
**Handling:** Attempt character set correction, flag if impossible

---

## CATEGORY 4: EMOJI/SYMBOLS ONLY (3 cases)

### Case 4.1: Pure Emoji Response
**Examples:**
- "👍"
- "😀👍🙌"
- "❤️💯✨"
- "👎❌"
**Classification:** AMBIGUOUS
**Confidence:** 25-40%
**Handling:** Thumbs up = mild positive, frowny = negative, heart = interest, but very low confidence

### Case 4.2: Emoji + Punctuation Only
**Examples:**
- "😀!"
- "👍👍👍"
- "❌❌❌"
**Classification:** AMBIGUOUS
**Confidence:** 30-45%
**Handling:** Emoji tone + emphasis (repetition), still ambiguous

### Case 4.3: Unicode Symbols Only
**Examples:**
- "✓✓✓" (check marks)
- "→→→" (arrows)
- "+++" (plus signs)
- "***" (asterisks)
**Classification:** AMBIGUOUS
**Confidence:** 20-35%
**Handling:** Context-dependent, usually low signal

---

## CATEGORY 5: FORWARDING/CONTEXT (5 cases)

### Case 5.1: Multiple Forwarding Layers
**Example:**
```
Fwd: Fwd: Fwd: Fwd: [Original Message]
> > > > [Your original message]
```
**What it is:** Deep forwarding chain, no new content added
**Classification:** AMBIGUOUS
**Confidence:** 30-40%
**Handling:** Extract innermost original message, classify that

### Case 5.2: Forwarded Message Without New Reply
**Example:**
```
---------- Forwarded message ---------
From: [Person A]
To: [Your Company]
Subject: Sales opportunity
[Original message content]

[No new message from Person B]
```
**What it is:** Just forwarding, not replying
**Classification:** AMBIGUOUS (may indicate interest = forwarding to relevant party)
**Confidence:** 45-60%
**Handling:** Could be positive if forwarding to decision maker

### Case 5.3: Quoted Original Message with No New Content
**Example:**
```
On Dec 5, 2024, you wrote:
> "Can we schedule a call?"
> "Tell me more about pricing"

[No new response from recipient]
```
**What it is:** Original message re-quoted, no acknowledgment
**Classification:** AMBIGUOUS
**Confidence:** 35-45%
**Handling:** May indicate no response needed or accidental send

### Case 5.4: Forwarded + Signature Only
**Example:**
```
Fwd: Fwd: [Original message about proposal]

--
John Smith
CEO, Acme Corp
[No additional commentary]
```
**What it is:** Forwarding with signature but no new content
**Classification:** AMBIGUOUS (likely delegating/forwarding to relevant person)
**Confidence:** 50-65%
**Handling:** Likely positive signal = escalation/forwarding

### Case 5.5: Calendar Invite as Reply (No Message)
**Example:**
```
[Calendar invite attached]
Subject: Meeting: Follow-up Discussion
[No email message body]
```
**What it is:** Prospect sends calendar invite instead of replying
**Classification:** MEETING REQUEST
**Confidence:** 85-95%
**Handling:** Clear intent - they're scheduling

---

## CATEGORY 6: CONFLICTING SIGNALS (7 cases)

### Case 6.1: Interest + Rejection Conflict
**Example:** "This is very interesting, but honestly we're not interested right now"
**Signal 1:** "very interesting" = POSITIVE INTEREST
**Signal 2:** "not interested" = NEGATIVE
**Classification:** AMBIGUOUS
**Confidence:** 50-60%
**Handling:** Flag both signals, needs manual review to determine primary intent

### Case 6.2: Positive + Budget Objection
**Example:** "Love the idea, but we have no budget for this quarter"
**Signal 1:** "Love the idea" = POSITIVE INTEREST
**Signal 2:** "no budget" = NEGATIVE (budget reason)
**Classification:** AMBIGUOUS (but leans POSITIVE INTEREST)
**Confidence:** 60-70%
**Handling:** Note as interested but blocked by budget

### Case 6.3: Question + Rejection Tone
**Example:** "Why would we ever need something like this?"
**Signal 1:** "Why" = QUESTION
**Signal 2:** Tone implies skepticism/rejection
**Classification:** QUESTION (but note skepticism)
**Confidence:** 65-75%
**Handling:** Classify as QUESTION, tag as skeptical/objection

### Case 6.4: Meeting Request + Out of Office
**Example:** "Can we schedule a call? I'm out this week but back Monday"
**Signal 1:** "Can we schedule" = MEETING REQUEST
**Signal 2:** "I'm out this week" = OUT OF OFFICE
**Classification:** MEETING REQUEST (with OOO context)
**Confidence:** 80-90%
**Handling:** Classify as MEETING REQUEST, note OOO timing

### Case 6.5: Multiple Competing Intents
**Example:** "Tell me more (INTEREST), how much does it cost (QUESTION), but also remove me from future emails (NEGATIVE)"
**Signal 1:** "Tell me more" = POSITIVE INTEREST
**Signal 2:** "how much" = QUESTION
**Signal 3:** "remove me" = NEGATIVE
**Classification:** AMBIGUOUS
**Confidence:** 35-50%
**Handling:** Flag for human review, requires clarification

### Case 6.6: Conditional Interest + Doubt
**Example:** "If it's affordable, we might be interested, but I'm skeptical it will work"
**Signal 1:** "if affordable, interested" = CONDITIONAL POSITIVE INTEREST
**Signal 2:** "skeptical it works" = QUESTION/Objection
**Classification:** AMBIGUOUS
**Confidence:** 50-60%
**Handling:** Conditional interest but skepticism noted

### Case 6.7: Enthusiasm + Rejection Reason
**Example:** "This sounds amazing! We'd love to use it, but our company just got acquired and everything is on hold"
**Signal 1:** "amazing", "love it" = POSITIVE INTEREST
**Signal 2:** "everything on hold" = NEGATIVE (timing)
**Classification:** NEGATIVE (but with note: high interest, poor timing)
**Confidence:** 75-85%
**Handling:** Classify as NEGATIVE (can't proceed now), note future potential

---

## CATEGORY 7: INCOMPLETE CONTEXT (6 cases)

### Case 7.1: Reply References Broken Link
**Example:** "I tried to open the link but it's broken. Can you resend?"
**What it is:** Technical issue, not intent issue
**Classification:** AMBIGUOUS (leaning POSITIVE INTEREST = asking for resend)
**Confidence:** 65-75%
**Handling:** Likely positive intent obscured by technical issue

### Case 7.2: Attachment Reference Without Content
**Example:** "I reviewed the attachment you sent"
**What it is:** References something but unclear what their reaction was
**Classification:** AMBIGUOUS
**Confidence:** 40-50%
**Handling:** Request follow-up on their thoughts

### Case 7.3: Image/Chart Didn't Load
**Example:** "The image didn't load properly. Can you send as a PDF?"
**What it is:** Technical issue, request for resend
**Classification:** AMBIGUOUS (leaning POSITIVE INTEREST)
**Confidence:** 65-75%
**Handling:** Technical blocker, likely interested but need to resolve

### Case 7.4: Vague Context Reference
**Example:** "Similar to what you mentioned before, but different timing"
**What it is:** References prior conversation not in current thread
**Classification:** AMBIGUOUS
**Confidence:** 30-45%
**Handling:** Requires looking up conversation history

### Case 7.5: Reply Implies Prior Context Unknown to Us
**Example:** "I'll check with my team about what we discussed"
**What it is:** References internal discussion we're not part of
**Classification:** AMBIGUOUS (likely POSITIVE INTEREST if escalating to team)
**Confidence:** 60-70%
**Handling:** Likely escalation = positive signal

### Case 7.6: Correction Reply
**Example:** "Sorry, my bad, ignore previous email"
**What it is:** Prospect is correcting prior message
**Classification:** Depends on what the correction is
**Confidence:** Varies
**Handling:** Look at corrected intent, not original

---

## CATEGORY 8: TIMING AMBIGUITY (5 cases)

### Case 8.1: Vague Future Reference
**Example 1:** "Eventually we might be interested"
**Example 2:** "Someday this could be useful"
**Classification:** AMBIGUOUS
**Confidence:** 40-55%
**Handling:** Insufficient timeline, may never happen

### Case 8.2: "We'll Think About It" (Procrastination Signal)
**Example 1:** "We'll think about it and get back to you"
**Example 2:** "Will review and get back" (with no timeline)
**Classification:** AMBIGUOUS
**Confidence:** 45-60%
**Handling:** Could be interest or polite rejection

### Case 8.3: Indefinite Timing
**Example:** "Let me check with my team"
**Classification:** AMBIGUOUS (leaning positive = escalation)
**Confidence:** 60-70%
**Handling:** Likely seeking internal approval = positive signal

### Case 8.4: Circular Response
**Example:** "Interesting timing, we were just discussing something similar"
**Classification:** AMBIGUOUS
**Confidence:** 50-65%
**Handling:** Shows interest but unclear next step

### Case 8.5: Timeline Too Far Out
**Example 1:** "Check back with us in 2 years"
**Example 2:** "Maybe after we're acquired"
**Classification:** AMBIGUOUS (borderline NEGATIVE)
**Confidence:** 60-70%
**Handling:** Unlikely timeline = low priority/interest

---

## CATEGORY 9: BOUNDARY KEYWORDS (8 cases)

### Case 9.1: Words Containing Signal Keywords
**Example:** "I fried the bacon" (contains "free" in "fried")
**Issue:** "free" is spam trigger, but context is cooking
**Classification:** False positive for SPAM TRIGGER
**Confidence:** Should NOT flag
**Handling:** Use word boundaries, not substring matching

### Case 9.2: Negation Before Keyword
**Example:** "I'm not interested" vs "I'm interested"
**Issue:** "not" changes meaning completely
**Classification:** NEGATIVE (with "not") vs POSITIVE INTEREST (without)
**Confidence:** Critical to detect
**Handling:** Check for "not", "can't", "won't" before keywords

### Case 9.3: Case Sensitivity
**Example 1:** "INTERESTED" (all caps)
**Example 2:** "interested" (lowercase)
**Example 3:** "InTeReStEd" (mixed case)
**Classification:** All should be recognized
**Confidence:** 100% confidence if matched
**Handling:** Convert to lowercase before matching

### Case 9.4: Hyphenated Words
**Example 1:** "out-of-office" vs "out of office"
**Example 2:** "self-interested" vs "self interested"
**Classification:** Both should be recognized
**Confidence:** Should match
**Handling:** Remove hyphens before matching

### Case 9.5: Possessives/Contractions
**Example 1:** "What's" vs "What is"
**Example 2:** "Can't" vs "Cannot"
**Example 3:** "Don't" vs "Do not"
**Classification:** Both forms should be recognized
**Confidence:** Should match
**Handling:** Expand contractions before matching

### Case 9.6: Abbreviations
**Example 1:** "ASAP" vs "As soon as possible"
**Example 2:** "FYI" vs "For your information"
**Example 3:** "BTW" vs "By the way"
**Classification:** Abbreviations should be recognized
**Confidence:** Should match
**Handling:** Maintain abbreviation list

### Case 9.7: Punctuation Variations
**Example 1:** "What?" vs "What"
**Example 2:** "No!!!" vs "No"
**Example 3:** "Really..." vs "Really"
**Classification:** Should recognize without punctuation
**Confidence:** Should match
**Handling:** Strip punctuation before matching

### Case 9.8: Whitespace Issues
**Example 1:** "not interested" (normal)
**Example 2:** "not  interested" (double space)
**Example 3:** "not\ninterested" (line break between)
**Classification:** Should recognize all variations
**Confidence:** Should match
**Handling:** Normalize whitespace before matching

---

## CATEGORY 10: SENTIMENT MODIFIERS (6 cases)

### Case 10.1: Sarcasm
**Example:** "Oh wonderful, another vendor pitch about how we're doing everything wrong"
**Surface Signal:** "wonderful" = positive
**Actual Intent:** NEGATIVE (sarcastic)
**Classification:** NEGATIVE
**Confidence:** 60-70%
**Handling:** Requires sentiment analysis, not just keyword matching

### Case 10.2: Fake Enthusiasm
**Example:** "Amazing! *said no one ever*"
**Surface Signal:** "Amazing" = POSITIVE INTEREST
**Actual Intent:** NEGATIVE (sarcasm)
**Classification:** NEGATIVE
**Confidence:** 75-85%
**Handling:** Detect sarcasm markers like "*said no one*"

### Case 10.3: Passive Aggressive
**Example:** "That's nice of you to reach out, but we're not interested"
**Surface Signal:** "nice" = positive tone
**Actual Intent:** NEGATIVE
**Classification:** NEGATIVE
**Confidence:** 70-80%
**Handling:** Look for "nice...but" or "lovely...however" patterns

### Case 10.4: Half-Hearted Agreement
**Example:** "Sure, I guess we could take a look"
**Surface Signal:** "Sure" = agreement
**Actual Intent:** AMBIGUOUS (lukewarm interest)
**Classification:** AMBIGUOUS (weak POSITIVE INTEREST)
**Confidence:** 50-60%
**Handling:** "I guess", "maybe", "could" = weak commitment

### Case 10.5: Backhanded Compliment
**Example:** "Interesting concept, but it will never work in our industry"
**Surface Signal:** "Interesting" = POSITIVE INTEREST
**Actual Intent:** NEGATIVE (dismissive)
**Classification:** NEGATIVE
**Confidence:** 70-80%
**Handling:** Detect "but" followed by rejection language

### Case 10.6: Obligatory Politeness
**Example:** "Thanks for thinking of us" followed by "we don't need this"
**Surface Signal:** "Thanks" = gratitude/interest
**Actual Intent:** NEGATIVE
**Classification:** NEGATIVE
**Confidence:** 80-90%
**Handling:** Look for "thanks...but" pattern

---

## CATEGORY 11: PERSON/DELEGATION (5 cases)

### Case 11.1: Wrong Person Identified
**Example:** "I think you have the wrong person, try [person@company.com]"
**What it is:** Prospect is forwarding to correct contact
**Classification:** AMBIGUOUS (but actionable - provides correct contact)
**Confidence:** 70-80%
**Handling:** Update contact, classify as POSITIVE signal (they're helping)

### Case 11.2: Forwarding to Team
**Example:** "I'm forwarding this to our procurement team"
**What it is:** Escalation to decision makers
**Classification:** POSITIVE INTEREST (implied escalation)
**Confidence:** 75-85%
**Handling:** Escalation to team = positive signal

### Case 11.3: Manager Will Respond
**Example:** "My boss will follow up with you"
**What it is:** Delegating to authority figure
**Classification:** POSITIVE INTEREST (escalation)
**Confidence:** 80-90%
**Handling:** Delegation to manager = strong positive signal

### Case 11.4: Colleague Handles This
**Example:** "I'll have [colleague] from our team handle this discussion"
**What it is:** Delegating to relevant person
**Classification:** POSITIVE INTEREST (escalation)
**Confidence:** 75-85%
**Handling:** Forwarding to relevant person = positive

### Case 11.5: Wrong Department/Team
**Example:** "This isn't our department, you need to talk to [other team]"
**What it is:** Redirecting to correct department
**Classification:** AMBIGUOUS (actionable - provides new contact)
**Confidence:** 65-75%
**Handling:** Update target, continue conversation with correct contact

---

## CATEGORY 12: DEADLINE/URGENCY (4 cases)

### Case 12.1: ASAP in Positive Context
**Example:** "We need this ASAP - tell me more!"
**What it is:** Urgency + interest
**Classification:** POSITIVE INTEREST (with urgency)
**Confidence:** 85-95%
**Handling:** Fast-track follow-up

### Case 12.2: ASAP in Negative Context
**Example:** "Remove me from your list ASAP - this is spam"
**What it is:** Urgency + rejection
**Classification:** NEGATIVE
**Confidence:** 95-100%
**Handling:** Immediate suppression, urgent

### Case 12.3: Deadline Without Clear Intent
**Example:** "We need this by Friday but [no commitment]"
**What it is:** Implied urgency but unclear if interested
**Classification:** AMBIGUOUS
**Confidence:** 50-65%
**Handling:** Requires clarification on interest level

### Case 12.4: Time Pressure as Objection
**Example:** "We're moving too fast, can we slow down?"
**What it is:** Time pressure as excuse/objection
**Classification:** NEGATIVE (or AMBIGUOUS)
**Confidence:** 60-70%
**Handling:** Likely procrastination signal

---

## CATEGORY 13: SYSTEM/TECHNICAL ERRORS (7 cases)

### Case 13.1: Hard Bounce - User Not Found (550 Error)
**Example:** "550 5.1.1 The email account that you tried to reach does not exist"
**What it is:** SMTP error, invalid recipient
**Classification:** BOUNCE
**Confidence:** 100%
**Handling:** Invalid contact, update prospect record

### Case 13.2: Soft Bounce - Mailbox Full (452 Error)
**Example:** "452 4.2.2 Try again later"
**What it is:** Temporary delivery failure
**Classification:** BOUNCE (soft)
**Confidence:** 95%
**Handling:** Retry later, not permanent failure

### Case 13.3: Multiple Error Codes
**Example:**
```
550 5.1.1 Invalid recipient
451 4.7.0 Temporary server failure
552 5.2.2 Over quota
```
**What it is:** Multiple failures in one bounce
**Classification:** BOUNCE (aggregate)
**Confidence:** 95-100%
**Handling:** Mark as bounced, flag for investigation

### Case 13.4: Mail Server Rejection
**Example:** "421 Service temporarily unavailable"
**What it is:** Server-side issue, not client issue
**Classification:** BOUNCE (soft, retry)
**Confidence:** 90%
**Handling:** Retry later, likely temporary

### Case 13.5: Authentication Failure
**Example:** "550 5.7.1 DKIM signature verification failed"
**What it is:** Email authentication issue
**Classification:** BOUNCE (infrastructure issue)
**Confidence:** 95%
**Handling:** Check email authentication setup

### Case 13.6: Rate Limiting
**Example:** "421 4.7.0 Please try again later"
**What it is:** Sender rate limited
**Classification:** BOUNCE (soft, retry)
**Confidence:** 90%
**Handling:** Respect limits, retry after delay

### Case 13.7: Domain/DNS Issue
**Example:** "550 5.1.2 Bad destination mailbox address"
**What it is:** Domain not found or misconfigured
**Classification:** BOUNCE
**Confidence:** 95%
**Handling:** Invalid contact, update prospect

---

## CATEGORY 14: LENGTH VARIATIONS (4 cases)

### Case 14.1: Extremely Long Reply (1000+ words)
**Example:** 
```
Thank you for reaching out... [1000+ word essay about their company, 
product roadmap, concerns, etc. with mixed signals throughout]
```
**What it is:** Very detailed reply with possibly multiple intents
**Classification:** Requires paragraph-by-paragraph analysis
**Confidence:** 30-50%
**Handling:** Parse each paragraph separately, aggregate intents

### Case 14.2: Very Short (1-2 words)
**Example 1:** "Interested"
**Example 2:** "Maybe"
**What it is:** Minimal content
**Classification:** AMBIGUOUS (could be any intent)
**Confidence:** 40-60%
**Handling:** Cannot determine intent from length alone

### Case 14.3: Reply Longer Than Original Message
**Example:**
```
Original: "Can we schedule a call?"
Reply: [5 paragraphs explaining why they can't, with conditions, 
alternatives, timeline, team structure, etc.]
```
**What it is:** Detailed response to simple question
**Classification:** Parse each paragraph
**Confidence:** 50-70%
**Handling:** Multiple intents possible, needs aggregation

### Case 14.4: Multi-Paragraph Mixed Intent
**Example:**
```
Paragraph 1: "This sounds interesting"  (POSITIVE INTEREST)
Paragraph 2: "How much does it cost?"  (QUESTION)
Paragraph 3: "We don't have budget"  (NEGATIVE)
Paragraph 4: "But let's talk in Q3"  (POSITIVE INTEREST conditional)
```
**What it is:** Each paragraph has different intent
**Classification:** AMBIGUOUS (aggregate: conditional interest)
**Confidence:** 50-65%
**Handling:** Determine dominant intent + secondary signals

---

## CATEGORY 15: AUTO-REPLY PATTERNS (7 cases)

### Case 15.1: Standard OOO Auto-Reply
**Example:**
```
I am currently out of the office with no email access and will return 
on December 10. For urgent matters, please contact [person].

Best regards,
John
```
**Classification:** OUT OF OFFICE
**Confidence:** 100%
**Handling:** Extract return date, pause automation, log for resume

### Case 15.2: OOO with Return Date
**Example:** "Out of office until Friday, December 8. Returning emails on December 9."
**Classification:** OUT OF OFFICE
**Confidence:** 100%
**Handling:** Extract date, set resume trigger

### Case 15.3: OOO with Delegation
**Example:** "Out until Dec 25. Contact Sarah (sarah@company.com) for urgent matters."
**Classification:** OUT OF OFFICE (with alternate contact)
**Confidence:** 100%
**Handling:** Log alternate contact, pause current contact

### Case 15.4: Limited Access OOO
**Example:** "Out with limited email access. Responses may be delayed."
**Classification:** OUT OF OFFICE (partial)
**Confidence:** 95%
**Handling:** Slower response expected, be patient

### Case 15.5: Partial OOO (Weekend/Evenings)
**Example:** "I don't check email on weekends"
**Classification:** OUT OF OFFICE (recurring pattern)
**Confidence:** 90%
**Handling:** Adjust expectations for response time

### Case 15.6: System Auto-Responder (Non-Human)
**Example:** 
```
[Auto-reply from [company.com](http://company.com) email system]
Your email has been received. We will respond within 24 hours.
```
**Classification:** OUT OF OFFICE (system)
**Confidence:** 100%
**Handling:** Not a real reply, wait for actual response

### Case 15.7: Delivery Failure (Looks Like OOO)
**Example:** "550 User is out of the office and not receiving mail"
**Classification:** BOUNCE (not OOO)
**Confidence:** 100%
**Handling:** Invalid contact, update prospect

---

## CATEGORY 16: CONDITIONAL/HYPOTHETICAL (5 cases)

### Case 16.1: Price-Conditional Interest
**Example:** "If it's under $500/month, we'd definitely be interested"
**What it is:** Interest exists but depends on pricing
**Classification:** POSITIVE INTEREST (conditional)
**Confidence:** 70-80%
**Handling:** Note condition, follow up with pricing

### Case 16.2: Feature-Conditional Interest
**Example:** "Would consider if you integrate with Salesforce"
**What it is:** Interest depends on specific feature
**Classification:** POSITIVE INTEREST (conditional)
**Confidence:** 70-80%
**Handling:** Note feature requirement, confirm integration, follow up

### Case 16.3: Timeline-Conditional Interest
**Example:** "Would be interested if we can implement before Q4"
**What it is:** Interest depends on implementation timeline
**Classification:** POSITIVE INTEREST (conditional)
**Confidence:** 70-80%
**Handling:** Confirm timeline, follow up

### Case 16.4: Approval-Conditional Interest
**Example:** "Need to get board approval first, but it looks good"
**What it is:** Interest exists but needs internal approval
**Classification:** POSITIVE INTEREST (conditional)
**Confidence:** 75-85%
**Handling:** Wait for approval, set follow-up reminder

### Case 16.5: Hypothetical Interest
**Example:** "In theory, this could work, but [doubt]"
**What it is:** Theoretical interest, lots of doubt
**Classification:** AMBIGUOUS (leaning negative)
**Confidence:** 50-60%
**Handling:** Note skepticism, may need overcomes objections

---

## CATEGORY 17: NEGATIVE WITH REASON (6 cases)

### Case 17.1: Already Using Competitor
**Example:** "We're already using X solution for this"
**What it is:** Competitive reason for rejection
**Classification:** NEGATIVE
**Confidence:** 95%
**Handling:** Note competitor, may follow up later for switch

### Case 17.2: Budget Constraint
**Example:** "We don't have budget allocated for this"
**What it is:** Financial reason for rejection
**Classification:** NEGATIVE
**Confidence:** 90%
**Handling:** Note timing, may revisit next budget cycle

### Case 17.3: Wrong Person/Department
**Example:** "You need to talk to procurement, not me"
**What it is:** Responsibility reason
**Classification:** NEGATIVE (for this person) but actionable
**Confidence:** 85%
**Handling:** Update contact routing

### Case 17.4: Wrong Industry Fit
**Example:** "This doesn't apply to our industry"
**What it is:** Use case reason for rejection
**Classification:** NEGATIVE
**Confidence:** 95%
**Handling:** Note unfitness, don't retry same prospect

### Case 17.5: Timing Issue
**Example:** "Great solution, but terrible timing - we're in the middle of a major overhaul"
**What it is:** Timing reason for rejection
**Classification:** NEGATIVE (now) but may revisit later
**Confidence:** 85%
**Handling:** Set follow-up for better time

### Case 17.6: Bad Previous Experience
**Example:** "We tried something similar from another vendor and it didn't work"
**What it is:** Past experience reason
**Classification:** NEGATIVE
**Confidence:** 85%
**Handling:** May need to overcome past objection

---

## CATEGORY 18: QUESTION AMBIGUITY (5 cases)

### Case 18.1: Rhetorical Question (Negative Intent)
**Example:** "How is this even possible? It's never worked before!"
**What it is:** Question format but implied rejection
**Classification:** NEGATIVE (disguised as question)
**Confidence:** 75-85%
**Handling:** Detect rhetoric patterns, classify as negative

### Case 18.2: Question as Objection
**Example:** "Why would we switch vendors in the middle of a contract?"
**What it is:** Question format but contains objection
**Classification:** QUESTION + NEGATIVE
**Confidence:** 70-80%
**Handling:** Note both signals

### Case 18.3: Skeptical Vetting Question
**Example:** "Do you actually have proof this works, or is this all marketing?"
**What it is:** Question format but expresses skepticism
**Classification:** QUESTION (skeptical)
**Confidence:** 60-70%
**Handling:** Requires evidence, not just answer

### Case 18.4: Single-Word Question
**Example 1:** "Cost?"
**Example 2:** "Timeline?"
**What it is:** Minimal question, requires context
**Classification:** QUESTION
**Confidence:** 70-80%
**Handling:** Provide answer, may lead to further questions

### Case 18.5: Question with Excessive Punctuation
**Example:** "Why would we do this???? Make it make sense!!!"
**What it is:** Question but with emotional punctuation
**Classification:** QUESTION (skeptical/negative tone)
**Confidence:** 60-75%
**Handling:** Tone suggests skepticism, not genuine inquiry

---

## CATEGORY 19: PREVIOUS CONTEXT (4 cases)

### Case 19.1: Reference to Discussion Not in Thread
**Example:** "As we discussed in our call yesterday..."
**What it is:** References prior conversation we can't see
**Classification:** AMBIGUOUS (context dependent)
**Confidence:** 30-50%
**Handling:** Look up call notes/context from CRM

### Case 19.2: Follow-Up to Earlier Email
**Example:** "Following up on your email from last month..."
**What it is:** References prior message in different thread
**Classification:** AMBIGUOUS
**Confidence:** 40-60%
**Handling:** Look up previous email chain

### Case 19.3: Deep Reply Chain (RE: RE: RE: RE:)
**Example:**
```
From: Original Email Date
To: Reply 1 (3 days later)
To: Reply 2 (1 week later)
To: Reply 3 (2 weeks later)
To: Current reply (1 month later)
[Long conversation history]
```
**What it is:** Long conversation with significant time gaps
**Classification:** AMBIGUOUS (depends on current message)
**Confidence:** Varies
**Handling:** Classify current message, note conversation history

### Case 19.4: Mentions Person Not in Current Conversation
**Example:** "I'll have Steve from our technical team review this"
**What it is:** References person outside current email chain
**Classification:** AMBIGUOUS (delegation signal)
**Confidence:** 65-75%
**Handling:** Likely positive = escalation to specialist

---

## CATEGORY 20: MULTI-RECIPIENT (3 cases)

### Case 20.1: Reply-All with Distribution List
**Example:**
```
To: sales-team@company.com, marketing-team@company.com
From: [prospect]
```
**What it is:** Reply goes to multiple recipients at our company
**Classification:** AMBIGUOUS (intention unclear)
**Confidence:** 40-60%
**Handling:** May indicate urgency/importance (reply-all)

### Case 20.2: CC'd but Not Direct Recipient
**Example:**
```
To: sales@company.com
CC: marketing@company.com
From: [prospect]
```
**What it is:** Prospect CC's additional recipients
**Classification:** AMBIGUOUS
**Confidence:** 45-65%
**Handling:** May indicate escalation or information sharing

### Case 20.3: BCC'd Response Visible
**Example:** Prospect replies to an email chain where they were BCC'd, reveals they're engaged
**What it is:** Unexpected response from BCC'd recipient
**Classification:** POSITIVE INTEREST (implicit)
**Confidence:** 75-85%
**Handling:** Strong engagement signal

---

## CATEGORY 21: FORMATTING ISSUES (5 cases)

### Case 21.1: ALL CAPS REPLY
**Example:** "THIS IS INTERESTING! CAN WE DISCUSS PRICING?"
**What it is:** All caps = shouting/emphasis
**Classification:** QUESTION (but with emphasis)
**Confidence:** 70-80%
**Handling:** Normalize to normal case, note emotional intensity

### Case 21.2: MixeD CaSe
**Example:** "ThIs Is InTeReStInG"
**What it is:** Erratic capitalization
**Classification:** AMBIGUOUS or intent signal depending on words
**Confidence:** 50-70%
**Handling:** Normalize case before parsing

### Case 21.3: Multiple Line Breaks Between Words
**Example:**
```
Tell


me


more
```
**What it is:** Words separated by multiple breaks
**Classification:** AMBIGUOUS
**Confidence:** 30-45%
**Handling:** Normalize whitespace, may indicate formatting issue

### Case 21.4: HTML Entities in Plain Text
**Example:** "Tell me more &quot; about pricing &nbsp; &amp; terms"
**What it is:** HTML-encoded text in email
**Classification:** AMBIGUOUS or intent signal
**Confidence:** 50-65%
**Handling:** Decode HTML entities before parsing

### Case 21.5: Markdown Formatting in Email
**Example:** "**Tell me more** about *pricing* and [timeline](link)"
**What it is:** Markdown syntax in plain email
**Classification:** AMBIGUOUS or intent signal
**Confidence:** 50-70%
**Handling:** Extract text, ignore markdown syntax

---

## CATEGORY 22: ATTACHMENT-ONLY (3 cases)

### Case 22.1: Attachment Without Message Body
**Example:**
```
[Attachment: signed_contract.pdf]
[No email message body]
```
**What it is:** Document sent but no context
**Classification:** AMBIGUOUS (likely POSITIVE INTEREST = action taken)
**Confidence:** 70-80%
**Handling:** Attachment suggests action, likely positive

### Case 22.2: Filename Implies Intent
**Example:**
```
[Attachment: lets_schedule_a_demo.docx]
OR
[Attachment: not_interested_reasons.pdf]
```
**What it is:** Filename indicates intent
**Classification:** Depends on filename (MEETING REQUEST vs NEGATIVE)
**Confidence:** 65-80%
**Handling:** Extract intent from filename as fallback

### Case 22.3: Image/Screenshot as Reply
**Example:** [Attachment: screenshot.png showing calendar with time slots]
**What it is:** Prospect sends image instead of text
**Classification:** Likely MEETING REQUEST (proposing times)
**Confidence:** 70-85%
**Handling:** Requires OCR/manual review to extract intent

---

## CATEGORY 23: SPAM/PHISHING (4 cases)

### Case 23.1: Obvious Spam
**Example:** "You've won! Claim your prize now! Click here: [malicious link]"
**What it is:** Spam reply
**Classification:** NEGATIVE / SECURITY FLAG
**Confidence:** 100%
**Handling:** Block, report as spam, security alert

### Case 23.2: Phishing Attempt
**Example:** "Verify your password: [fake login link]"
**What it is:** Phishing email masquerading as reply
**Classification:** SECURITY FLAG
**Confidence:** 100%
**Handling:** Security alert, do not click, block sender

### Case 23.3: Spoofed Sender
**Example:** 
```
From: support@company.com (but actually from attacker@malicious.com)
Subject: RE: Your purchase
```
**What it is:** Sender address spoofed
**Classification:** SECURITY FLAG
**Confidence:** 90-100%
**Handling:** Verify sender domain, security alert

### Case 23.4: Malicious Link in Reply
**Example:** "Great! Let's continue: [bit.ly/very-short-url-hiding-malware]"
**What it is:** Reply contains hidden malicious link
**Classification:** SECURITY FLAG
**Confidence:** 95-100%
**Handling:** URL scan, block if malicious, security alert

---

## CATEGORY 24: SOCIAL SIGNALS (4 cases)

### Case 24.1: LinkedIn Reaction Only
**Example:** Prospect sends 👍 or 💯 reaction on LinkedIn message
**What it is:** Social platform reaction, not text reply
**Classification:** AMBIGUOUS (weak POSITIVE INTEREST)
**Confidence:** 40-60%
**Handling:** Likely low engagement, acknowledge but follow up with text

### Case 24.2: WhatsApp Emoji Reaction
**Example:** Prospect sends 👍 reaction to message
**What it is:** WhatsApp emoji reaction
**Classification:** AMBIGUOUS (weak POSITIVE INTEREST)
**Confidence:** 50-65%
**Handling:** Acknowledge, follow up for clarity

### Case 24.3: Thumbs Down Reaction
**Example:** 👎 or ❌ reaction
**What it is:** Negative reaction
**Classification:** AMBIGUOUS NEGATIVE
**Confidence:** 70-80%
**Handling:** May indicate disinterest, follow up

### Case 24.4: "Read Receipt" Without Reply
**Example:** Email shows "read" status but no reply text
**What it is:** Engagement signal but not explicit intent
**Classification:** AMBIGUOUS
**Confidence:** 30-40%
**Handling:** May indicate review in progress, set follow-up

---

## CATEGORY 25: REGULATORY/LEGAL (4 cases)

### Case 25.1: Cease and Desist
**Example:** "Cease and desist all contact immediately or we will pursue legal action"
**What it is:** Legal threat
**Classification:** NEGATIVE / LEGAL FLAG
**Confidence:** 100%
**Handling:** Suppress contact, legal review, escalate

### Case 25.2: Harassment Claim
**Example:** "This constitutes harassment. I'm reporting this to our legal department"
**What it is:** Prospect claiming harassment
**Classification:** NEGATIVE / LEGAL FLAG
**Confidence:** 95%
**Handling:** Suppress, legal review, cease contact

### Case 25.3: GDPR/Privacy Complaint
**Example:** "You're violating GDPR. Unsubscribe me and delete my data immediately"
**What it is:** Privacy/compliance complaint
**Classification:** NEGATIVE / COMPLIANCE FLAG
**Confidence:** 100%
**Handling:** Immediate compliance, suppress, legal review

### Case 25.4: FTC Complaint Reference
**Example:** "I'm reporting this to the FTC as false advertising"
**What it is:** Regulatory complaint threat
**Classification:** NEGATIVE / COMPLIANCE FLAG
**Confidence:** 100%
**Handling:** Compliance review, suppress, escalate

---

## CATEGORY 26: DUPLICATION (3 cases)

### Case 26.1: Repeated Word/Message
**Example:** "Please respond, please respond, please respond"
**What it is:** Same message repeated
**Classification:** AMBIGUOUS (emphasis unclear)
**Confidence:** 40-55%
**Handling:** Note repetition, may indicate urgency or error

### Case 26.2: Duplicate Reply
**Example:** Same reply received twice (possibly copy-paste error)
**What it is:** Accidental or system duplication
**Classification:** AMBIGUOUS
**Confidence:** 30-40%
**Handling:** Treat as single reply, ignore duplicate

### Case 26.3: Copy-Paste of Original Message
**Example:** Prospect replies with original message repeated verbatim
**What it is:** No new content, just echoing
**Classification:** AMBIGUOUS
**Confidence:** 25-35%
**Handling:** No new intent, may need to resend original

---

## CATEGORY 27: METADATA MISMATCH (3 cases)

### Case 27.1: Subject vs Body Mismatch
**Example:**
```
Subject: RE: Budget Approval
Body: "Not interested, remove me"
```
**What it is:** Subject indicates one thing, body another
**Classification:** Trust body over subject
**Confidence:** 60-75%
**Handling:** Classify based on body content

### Case 27.2: Timestamp Indicates Auto-Reply
**Example:** Reply received at 3:47 AM (likely auto-responder, not manual)
**What it is:** Timing suggests automation
**Classification:** May be auto-reply
**Confidence:** 70-80%
**Handling:** Flag as possible auto-reply, may not represent human decision

### Case 27.3: Recipient Mismatch
**Example:** Reply intended for [person A] accidentally sent to [person B]
**What it is:** Wrong recipient
**Classification:** AMBIGUOUS (may be forwarding or error)
**Confidence:** 50-70%
**Handling:** Determine if forwarding (positive) or error (ignore)

---

## CATEGORY 28: CHANNEL-SPECIFIC (6 cases)

### Case 28.1: WhatsApp Emoji Reaction (Channel-Specific)
**Example:** 👍 emoji reaction in WhatsApp
**What it is:** WhatsApp-specific reaction
**Classification:** AMBIGUOUS (weak positive)
**Confidence:** 40-60%
**Handling:** Different from email; lower confidence than text reply

### Case 28.2: LinkedIn "Just Viewed"
**Example:** Prospect viewed your profile but didn't message
**What it is:** LinkedIn engagement, not reply
**Classification:** Not a reply, just engagement signal
**Confidence:** 20-30%
**Handling:** Log engagement, send follow-up message

### Case 28.3: LinkedIn InMail Reply
**Example:** Prospect replies to LinkedIn InMail vs regular message
**What it is:** Channel-specific: InMail (paid premium) vs message
**Classification:** Depends on content
**Confidence:** Varies
**Handling:** Treat as standard reply, note higher likelihood of read

### Case 28.4: SMS/Text Message Reply
**Example:** Prospect replies via SMS vs email
**What it is:** Channel-specific: character limit affects message length
**Classification:** Depends on content
**Confidence:** Varies
**Handling:** SMS may have typos/abbreviations due to length limits

### Case 28.5: Slack/Direct Message Reply
**Example:** Prospect replies via Slack DM vs email
**What it is:** Channel-specific: casual medium
**Classification:** May be less formal
**Confidence:** Varies
**Handling:** Slack replies may be quicker but less official

### Case 28.6: WhatsApp Business Reply
**Example:** Prospect replies via WhatsApp Business Account
**What it is:** Channel-specific: business account often official response
**Classification:** May carry more weight
**Confidence:** Varies
**Handling:** Business account replies may indicate official decision

---

## SUMMARY: ALL 139+ EDGE CASES BY CATEGORY

```
Category 1:  Empty/Minimal (8 cases)
Category 2:  Typos/Garbled (6 cases)
Category 3:  Language/Encoding (4 cases)
Category 4:  Emoji/Symbols (3 cases)
Category 5:  Forwarding/Context (5 cases)
Category 6:  Conflicting Signals (7 cases)
Category 7:  Incomplete Context (6 cases)
Category 8:  Timing Ambiguity (5 cases)
Category 9:  Boundary Keywords (8 cases)
Category 10: Sentiment Modifiers (6 cases)
Category 11: Person/Delegation (5 cases)
Category 12: Deadline/Urgency (4 cases)
Category 13: System/Technical (7 cases)
Category 14: Length Variations (4 cases)
Category 15: Auto-Reply Patterns (7 cases)
Category 16: Conditional/Hypothetical (5 cases)
Category 17: Negative with Reason (6 cases)
Category 18: Question Ambiguity (5 cases)
Category 19: Previous Context (4 cases)
Category 20: Multi-Recipient (3 cases)
Category 21: Formatting Issues (5 cases)
Category 22: Attachment-Only (3 cases)
Category 23: Spam/Phishing (4 cases)
Category 24: Social Signals (4 cases)
Category 25: Regulatory/Legal (4 cases)
Category 26: Duplication (3 cases)
Category 27: Metadata Mismatch (3 cases)
Category 28: Channel-Specific (6 cases)
─────────────────────────────────────
TOTAL: 28 categories, 139 specific edge cases
```

---

**NOW you can review each exact case, identify gaps, and add missing ones!** ✅

