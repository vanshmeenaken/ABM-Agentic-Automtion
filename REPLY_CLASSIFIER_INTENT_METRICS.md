# Reply Classifier Agent - Intent Classification Metrics Framework

**Purpose:** Define all terms, signals, patterns, and triggers for each of the 7 intent categories

**Goal:** Build comprehensive classification rules before adding real-life replies

---

## Table of Contents

1. [Intent 1: Positive Interest](#intent-1-positive-interest)
2. [Intent 2: Meeting Request](#intent-2-meeting-request)
3. [Intent 3: Question](#intent-3-question)
4. [Intent 4: Negative](#intent-4-negative)
5. [Intent 5: Out of Office](#intent-5-out-of-office)
6. [Intent 6: Bounce](#intent-6-bounce)
7. [Intent 7: Ambiguous](#intent-7-ambiguous)
8. [Classification Decision Tree](#classification-decision-tree)

---

## Intent 1: Positive Interest

**Definition:** Prospect shows interest without committing to meeting immediately

**Trigger Condition:** Any signal showing engagement/curiosity/openness

### Direct Interest Signals

```
"Tell me more"
"Sounds interesting"
"Let's connect"
"I'm interested"
"This looks good"
"Worth exploring"
"Curious about"
"What else"
"How does this work"
"Intriguing"
"Could be useful"
"Might be relevant"
"Seems valuable"
"Good timing"
"Exactly what we need"
"Looking for something like this"
"This could help"
"Definitely interested"
"Very interested"
"Highly interested"
```

### Implicit Interest Signals

```
"Thanks for reaching out"
"Appreciate you contacting us"
"Good to hear from you"
"Happy to learn more"
"Would love to hear more"
"Keep me posted"
"Please send more info"
"Send details"
"What's next?"
"How do we proceed?"
"Love to discuss further"
"Would be great to explore"
"Seems like a fit"
"This aligns with our needs"
"Exactly what we've been looking for"
"Perfect timing"
"We've been considering this"
"This is what we need"
```

### Question + Interest Combo

```
"Tell me more about X"
"How would this help us?"
"What are the next steps?"
"What's the investment?"
"How does pricing work?"
"What's the timeline?"
"Can you share case studies?"
```

### Positive Sentiment Indicators

```
"Great"
"Excellent"
"Perfect"
"Love it"
"Fantastic"
"Wonderful"
"Amazing"
"Awesome"
"Cool idea"
"Brilliant"
"Well done"
"Impressive"
```

### Conditional Interest

```
"If it's affordable..."
"If the timeline works..."
"If you can do X..."
"Depends on..."
"Might work if..."
"Could be interested if..."
"Would consider if..."
```

### Engagement Actions

```
"Share the proposal"
"Send the deck"
"Show me the ROI"
"What's the catch?"
"Do you have references?"
"Can you prove it?"
"Show me examples"
"Any case studies?"
"Who else uses this?"
```

### Confidence Scoring

| Signal Type | Confidence | Example |
|------------|-----------|---------|
| Direct strong interest | 90-100 | "Definitely interested, tell me more" |
| Indirect interest | 75-85 | "Thanks for reaching out, send details" |
| Curious/exploratory | 65-75 | "What's the investment?" |
| Soft interest | 55-65 | "Could be relevant" |

---

## Intent 2: Meeting Request

**Definition:** Prospect explicitly wants to schedule meeting/call/demo

**Trigger Condition:** Clear request for synchronous engagement

### Direct Meeting Requests

```
"Can we schedule a call?"
"Are you available for a meeting?"
"Let's set up a time"
"When are you free?"
"Can we talk soon?"
"Let's schedule something"
"I'd like to discuss this"
"Can we connect?"
"Want to hop on a call?"
"Do you have time for a call?"
"Shall we schedule?"
"Let's plan a call"
"When works for you?"
"Can I get 15 minutes?"
"Can you call me?"
"Let's talk"
"Want to chat?"
"Can you meet?"
"Meeting request"
"Calendar invite?"
"What times work?"
```

### Meeting Type Specificity

```
"Quick call"
"30-minute meeting"
"Demo session"
"Product walkthrough"
"Strategy discussion"
"Planning session"
"Kickoff call"
"Initial consultation"
"Discovery call"
"Sales call"
"Technical demo"
"Pricing discussion"
"Proposal review"
```

### Time Proposals

```
"This week?"
"Next week?"
"Friday at 2pm?"
"Tomorrow afternoon?"
"Early next week?"
"ASAP"
"As soon as possible"
"At your earliest convenience"
"Tomorrow"
"This afternoon"
"Thursday works"
"Monday-Wednesday"
"After 3pm"
"Before noon"
```

### Action + Interest Combo

```
"Send me a time and I'll join"
"Pick a time that works"
"Just send the link"
"Add me to the calendar"
"Sounds good, let's talk"
"Great idea, when can we discuss?"
"Love this, let's connect"
```

### Meeting Readiness Signals

```
"I'll have my team join"
"My boss wants to join"
"Let me get back to you with times"
"I'll check my calendar"
"Forwarding to my manager"
"Cc'ing my team"
"Our leadership is interested"
"We'd like to present this to our team"
"Can you present to our group?"
"Budget approved, let's discuss timeline"
```

### Demo/Proof Requests (= Meeting)

```
"Can you demo?"
"Show me a demo"
"Demo would help"
"Let's see how it works"
"Can you show us?"
"Let me see it in action"
"Proof of concept?"
"Can you send a walkthrough video?"
"Live demo preferred"
"Can we screen share?"
```

### Confidence Scoring

| Signal Type | Confidence | Example |
|------------|-----------|---------|
| Explicit meeting request | 95-100 | "Can we schedule a call?" |
| Time commitment | 85-95 | "Tuesday at 2pm works" |
| Weak meeting signal | 70-80 | "Maybe we could chat sometime" |
| Implicit (demo = meeting) | 80-90 | "Can you show a demo?" |

---

## Intent 3: Question

**Definition:** Prospect seeks clarification/information (no buying signal yet)

**Trigger Condition:** Question mark present OR "what/how/why/when/who/where" signals

### Clarification Questions

```
"What is this?"
"What does this mean?"
"What's the difference between X and Y?"
"What are the requirements?"
"What's included?"
"What's not included?"
"What's the catch?"
"What are the limitations?"
"What's the cost?"
"What's the ROI?"
"What's the timeline?"
"What's the implementation process?"
"What support is included?"
```

### How Questions

```
"How does this work?"
"How would this help us?"
"How is it different from competitors?"
"How long does implementation take?"
"How much does it cost?"
"How do we get started?"
"How is data secured?"
"How do you handle X?"
"How often do updates happen?"
"How does pricing scale?"
"How do you measure success?"
"How do other clients use this?"
```

### Why Questions

```
"Why should we choose this?"
"Why is this better?"
"Why now?"
"Why us specifically?"
"Why this approach?"
"Why not use existing solution?"
"Why the price point?"
```

### Who Questions

```
"Who are your customers?"
"Who else uses this?"
"Who is the typical user?"
"Who would implement this?"
"Who pays for this?"
"Who are you?"
"Who do I contact?"
```

### Skeptical Questions

```
"How do I know this works?"
"Do you have proof?"
"Can you provide references?"
"What's your track record?"
"Who are your biggest clients?"
"Can I see case studies?"
"Do you have testimonials?"
"How long have you been around?"
"What's your success rate?"
```

### Technical Questions

```
"Is it compatible with X?"
"Does it integrate with Y?"
"What's the learning curve?"
"Can it handle our volume?"
"Is it cloud-based?"
"How's the uptime?"
"What about data privacy?"
"API available?"
"Customization options?"
```

### Business Questions

```
"What's the ROI?"
"How long until payback?"
"What's the implementation cost?"
"What are the hidden costs?"
"What's the contract length?"
"Can we cancel anytime?"
"What if we outgrow it?"
"Volume discounts?"
```

### Minimal/Lazy Questions

```
"?"
"Details?"
"Info?"
"Cost?"
"Timeline?"
"More info?"
"Process?"
```

### Confidence Scoring

| Signal Type | Confidence | Example |
|------------|-----------|---------|
| Genuine interested question | 75-85 | "How does this integrate with our system?" |
| Skeptical/vetting question | 65-75 | "Do you have references?" |
| Lazy/minimal question | 50-65 | "?" or "Cost?" |
| Objection disguised as question | 40-60 | "How do I know this works?" |

---

## Intent 4: Negative

**Definition:** Prospect explicitly rejects, unsubscribes, or terminates engagement

**Trigger Condition:** Any rejection, suppression, or opt-out signal

### Explicit Rejection

```
"Not interested"
"Not a fit"
"Wrong person"
"Wrong company"
"Not relevant"
"Not applicable"
"Doesn't apply to us"
"Not needed"
"Already have a solution"
"Using something else"
"No thanks"
"Pass"
"Not now"
"Not at this time"
"Maybe later"
"Not in our plans"
"Low priority"
"Wrong timing"
"Bad timing"
```

### Unsubscribe/Opt-Out

```
"Remove me"
"Unsubscribe"
"Stop emailing"
"Stop calling"
"Don't contact again"
"Please stop"
"Leave me alone"
"Stop bothering"
"Spam"
"Report spam"
"Don't send more"
"Remove from list"
"Block"
"Blocked"
"Unsubscribed"
```

### Negative Sentiment

```
"Waste of time"
"Irrelevant"
"Unwanted"
"Unsolicited"
"Junk"
"Garbage"
"Annoying"
"Irritating"
"Intrusive"
"Aggressive marketing"
"Too pushy"
"Not interested in cold calls"
```

### Competitive Rejection

```
"We already have this"
"Using X instead"
"Prefer Y solution"
"Built our own"
"Not switching vendors"
"Locked into contract"
"Happy with current provider"
"No plans to change"
"Satisfied with existing tool"
```

### Budget/Timing Rejection

```
"No budget"
"Budget frozen"
"Can't afford"
"Out of scope"
"Not in budget"
"Too expensive"
"Not approved"
"No funding"
"After next quarter"
"Next year maybe"
```

### Responsibility Rejection

```
"Not my department"
"Not my problem"
"Ask [other person]"
"Wrong contact"
"You need to talk to..."
"That's handled by..."
"Not my area"
```

### Harsh Rejection

```
"F*** off"
"Leave me alone"
"Never contact again"
"This is harassment"
"Reported to my company"
"Going to complain"
"Cease and desist"
"You're blacklisted"
```

### Soft Rejection (borderline)

```
"Maybe some other time"
"Not right now"
"Not urgent"
"Will think about it"
"Let me get back to you" (no follow-up)
"I'll reach out when ready"
(Then never responds)
```

### Confidence Scoring

| Signal Type | Confidence | Example |
|------------|-----------|---------|
| Explicit rejection | 95-100 | "Not interested, remove me" |
| Soft rejection | 70-85 | "Maybe later, wrong timing" |
| Competitive reason | 85-90 | "Already using X solution" |
| Harsh rejection | 100 | "F*** off" |

---

## Intent 5: Out of Office

**Definition:** Auto-reply or manual indication prospect is unavailable temporarily

**Trigger Condition:** OOO keywords + date signals

### Auto-Reply OOO Signals

```
"Out of office"
"Out of the office"
"Away from office"
"I'm away"
"I'm out"
"Currently out"
"Out on"
"Will be back"
"Back on [date]"
"Returning on [date]"
"Out until [date]"
"Out through [date]"
"I will return"
```

### OOO With Return Date

```
"Out of office until Friday"
"Back on Monday"
"Returning next week"
"Away until Dec 25"
"Out through the 15th"
"Return date: Jan 5"
"Back from vacation on..."
"I'll be back on..."
```

### Manual OOO Indication

```
"I'm on vacation"
"Taking time off"
"On leave"
"Sabbatical"
"Maternity leave"
"Paternity leave"
"Medical leave"
"Personal leave"
"Traveling"
"On a trip"
"Conference"
"Training"
"Team building"
```

### OOO + Delegation

```
"Out of office, contact [person]"
"I'm away, reach out to [email]"
"Out until Friday, [person] can help"
"On vacation, my colleague handles this"
"Out of office, forwarding to [team]"
"Will forward to team on return"
```

### OOO + Limited Access

```
"Out with limited email access"
"Out with no email access"
"Out but checking email"
"Limited connectivity"
"Spotty internet"
"May have delays responding"
```

### Partial/Temporary OOO

```
"Away for the rest of the week"
"Out Fridays"
"Half-day meetings"
"Limited availability"
"Reduced schedule"
"Working from home"
"Off-site"
```

### Confidence Scoring

| Signal Type | Confidence | Example |
|------------|-----------|---------|
| Clear auto-reply | 95-100 | "Out of office until Dec 25, returning Jan 5" |
| Manual indication with date | 90-95 | "On vacation, back next week" |
| Vague OOO | 75-85 | "I'm away for a bit" |
| Implied OOO | 70-80 | "No email access this week" |

**Action:** Do NOT suppress. Pause and resume on return date.

---

## Intent 6: Bounce

**Definition:** Email delivery failure, invalid contact, system error

**Trigger Condition:** NDR (Non-Delivery Report), delivery status codes, system errors

### Hard Bounce Signals

```
"Address rejected"
"Invalid recipient"
"User unknown"
"No such user"
"Account disabled"
"Mailbox not found"
"Invalid mailbox"
"Address does not exist"
"Recipient rejected"
"Mailbox unavailable"
"Mailbox closed"
"Mailbox retired"
```

### Soft Bounce Signals

```
"Mailbox full"
"Over quota"
"Temporary failure"
"Try again later"
"Service unavailable"
"Host unavailable"
"Connection timeout"
"Timeout"
"Temporary error"
```

### SMTP Error Codes (Standard)

```
550 - Mailbox unavailable
551 - User not local
552 - Mailbox storage exceeded
553 - Invalid mailbox name
554 - Transaction failed
421 - Service unavailable
450 - Temporary failure
451 - Server error
452 - Insufficient storage
```

### Email System Errors

```
"Delivery failed"
"Mail delivery failed"
"Message undeliverable"
"Unable to deliver"
"Return to sender"
"Returned mail"
"Non-delivery report"
"Delivery status notification"
"Undeliverable message"
"Delivery impossible"
```

### Authentication Failures

```
"Authentication failed"
"SPF failure"
"DKIM failure"
"DMARC failure"
"TLS required"
"Encryption required"
"Certificate error"
```

### Block/Filter Signals

```
"Blocked by filter"
"Rejected by filter"
"Spam filter"
"Content filter"
"Blacklist"
"Blocklist"
"Policy violation"
"Rejected by policy"
```

### Domain Issues

```
"Domain not found"
"DNS failure"
"MX record error"
"Invalid domain"
"Domain expired"
"Domain suspended"
"Domain does not exist"
```

### Special Cases

```
"Account closed"
"Account deleted"
"Person no longer with company"
"Employee terminated"
"Left the company"
"Forwarding loop"
"Recursive forwarding"
"Address is already a group"
```

### Confidence Scoring

| Signal Type | Confidence | Example |
|------------|-----------|---------|
| Hard bounce (clear) | 95-100 | "Address does not exist" (550) |
| Soft bounce | 70-80 | "Mailbox full, try later" |
| System error | 80-90 | "SMTP 554 Transaction failed" |
| Ambiguous bounce | 60-70 | "Temporary failure" |

**Action:** Do NOT create handoff. Update prospect contact validity.

---

## Intent 7: Ambiguous

**Definition:** Unclear intent, insufficient data, multiple possible interpretations

**Trigger Condition:** Any classification uncertainty or edge case

### Empty/Minimal Replies

```
""  (empty)
"..."
"."
"?"
"Yes"
"No"
"OK"
"K"
"Yep"
"Nope"
"Maybe"
"IDK"
"Not sure"
"Hmm"
"Interesting"
"Cool"
"Thanks"
"Got it"
"Understood"
"Will do"
```

### Single Word Replies

```
"Interested"
"Maybe"
"Later"
"When"
"Why"
"How"
"Cost"
"Timeline"
"Demo"
"Meeting"
"Call"
"Email"
"Info"
"Details"
```

### Conflicting Signals

```
"Interested but not now"
"Tell me more but busy"
"Sounds good but skeptical"
"Want to learn but no budget"
"Like it but already committed"
```

### Unclear Context

```
"This looks good 👍"  (what does good mean?)
"Hmm, interesting"  (interested or skeptical?)
"Will review and get back"  (intent unclear)
"Let me check with team"  (approval or rejection coming?)
"Similar to what we discussed"  (positive? negative? just noting?)
"Can't read attachment, resend"  (technical or disinterest?)
```

### Typos/Garbled Text

```
"Intrested"
"Schdeul a call"
"Whens good"
"Y sent this?"
"Unibale ti call"
```

### Non-English/Foreign Language

```
"Merci beaucoup"  (French - thanks, but interest level?)
"¿Cuando podemos hablar?"  (Spanish - meeting request?)
"😀👍🙌"  (Emoji only)
"[Chinese characters]"  (No context)
```

### Forwarded/Out-of-Context

```
"Fwd: Fwd: Fwd: [original message]"
(Reply with no message, just signature)
(Attachment only, no text)
(Calendar invite only, no message)
```

### Conditional/Unclear

```
"Depends..."
"If you can..."
"Might work"
"Could be"
"Possibly"
"Perhaps"
"We'll see"
"TBD"
"TBA"
"To be determined"
```

### Multi-Interpretation Signals

```
"Not bad"  (positive or lukewarm?)
"Interesting timing"  (good or bad timing?)
"We'll think about it"  (genuine interest or polite rejection?)
"Thanks for thinking of us"  (appreciation or dismissal?)
"Keep us in the loop"  (interest or courtesy?)
```

### System/Technical Issues

```
"Received corrupted"
"Unreadable format"
"Image didn't load"
"Video won't play"
"Link broken"
"Can't access"
"Download failed"
```

### Confidence Scoring

| Signal Type | Confidence | Example |
|------------|-----------|---------|
| Minimal reply | 30-50 | "?" or "Yes" |
| Conflicting signals | 40-60 | "Interested but busy" |
| Single word | 35-55 | "Cool" or "When" |
| Non-English | 20-40 | Foreign language or emoji |
| System error | 25-45 | "Corrupted file" |

**Rule:** ANY confidence < 60 → FLAG FOR HUMAN REVIEW

---

## Classification Decision Tree

```
Inbound Reply
    ↓
1. Is it a bounce/NDR/delivery error?
   YES → BOUNCE
   NO → continue
    ↓
2. Is prospect explicitly requesting meeting/call/demo/sync engagement?
   YES → MEETING REQUEST
   NO → continue
    ↓
3. Is prospect explicitly rejecting/unsubscribing/opting out?
   YES → NEGATIVE
   NO → continue
    ↓
4. Is it an OOO auto-reply or temporary unavailability?
   YES → OUT OF OFFICE
   NO → continue
    ↓
5. Is there a clear question (What/How/Why/Who/When/Where)?
   YES → QUESTION
   NO → continue
    ↓
6. Is there a clear positive interest signal without meeting request?
   YES → POSITIVE INTEREST
   NO → continue
    ↓
7. If none of above apply OR confidence < 60:
   DEFAULT → AMBIGUOUS (flag for human review)
```

---

## Classification Confidence Framework

### High Confidence (85-100)

- Clear, unambiguous signals
- Multiple confirming indicators
- Explicit language
- Standard format

**Examples:**
```
"Can we schedule a call?" → MEETING REQUEST (98)
"Not interested, remove me" → NEGATIVE (99)
"Out of office until Dec 25" → OOO (97)
"Address does not exist" → BOUNCE (96)
```

---

### Medium Confidence (60-85)

- Some ambiguity but leaning direction
- Single strong signal
- Minor language variations

**Examples:**
```
"Tell me more" → POSITIVE INTEREST (78)
"What's the cost?" → QUESTION (72)
"When works for you?" → MEETING REQUEST (80)
"Maybe some other time" → NEGATIVE (68)
```

---

### Low Confidence (40-60)

- Unclear intent
- Multiple possible interpretations
- Minimal content
- Requires clarification

**Examples:**
```
"Interesting" → Could be interest, question, or dismissal (52)
"Let me check with team" → Could be interest, approval, or delegation (58)
"Not bad" → Positive or lukewarm? (45)
"Will review and get back" → Interest or procrastination? (55)
```

---

### Flag for Human Review (< 60)

**Automatic human review triggered when:**

- Confidence score < 60
- Multiple conflicting signals
- Non-English/unclear language
- System errors in parsing
- Potential misclassification risk

---

## Next Steps: Real-Life Reply Corpus

**To enhance this framework:**

1. Provide real-life replies you receive
2. Classify them into these 7 categories
3. Identify any signals NOT in this list
4. Adjust confidence thresholds based on actual data
5. Build refined classification rules

**Format for real-life replies:**
```json
{
  "reply_text": "...",
  "channel": "email|whatsapp|linkedin",
  "actual_intent": "positive_interest|meeting_request|...",
  "why": "explanation of signals",
  "confidence_should_be": "X%"
}
```

---

**Ready to receive real-life replies for enhancement!**

