# Reply Classifier - Simple Signal List

**Format:** Clean list, easy to copy/use, organized by intent

---

## INTENT 1: POSITIVE INTEREST (45 signals)

Tell me more, Sounds interesting, Let's connect, I'm interested, This looks good, Worth exploring, Curious about, What else, How does this work, Intriguing, Could be useful, Might be relevant, Seems valuable, Good timing, Exactly what we need, Looking for something like this, This could help, Definitely interested, Very interested, Highly interested, Thanks for reaching out, Appreciate you contacting us, Good to hear from you, Happy to learn more, Would love to hear more, Keep me posted, Please send more info, Send details, What's next, How do we proceed, Love to discuss further, Would be great to explore, Seems like a fit, This aligns with our needs, Exactly what we've been looking for, Perfect timing, We've been considering this, This is what we need, Great, Excellent, Perfect, Love it, Fantastic, Wonderful, Amazing, Awesome

---

## INTENT 2: MEETING REQUEST (45 signals)

Can we schedule a call, Are you available for a meeting, Let's set up a time, When are you free, Can we talk soon, Let's schedule something, I'd like to discuss this, Can we connect, Want to hop on a call, Do you have time for a call, Shall we schedule, Let's plan a call, When works for you, Can I get 15 minutes, Can you call me, Let's talk, Want to chat, Can you meet, Meeting request, Calendar invite, What times work, Quick call, 30-minute meeting, Demo session, Product walkthrough, Strategy discussion, Planning session, Kickoff call, Initial consultation, Discovery call, Sales call, Technical demo, Pricing discussion, Proposal review, This week, Next week, Friday at 2pm, Tomorrow afternoon, Early next week, ASAP, As soon as possible, Tomorrow, This afternoon, Thursday works, Monday-Wednesday, After 3pm, Before noon

---

## INTENT 3: QUESTION (55 signals)

What is this, What does this mean, What's the difference, What are the requirements, What's included, What's not included, What's the catch, What are the limitations, What's the cost, What's the ROI, What's the timeline, What's the implementation process, What support is included, How does this work, How would this help us, How is it different from competitors, How long does implementation take, How much does it cost, How do we get started, How is data secured, How do you handle this, How often do updates happen, How does pricing scale, How do you measure success, How do other clients use this, Why should we choose this, Why is this better, Why now, Why us specifically, Why this approach, Why not use existing solution, Why the price point, Who are your customers, Who else uses this, Who is the typical user, Who would implement this, Who pays for this, Who are your biggest clients, How do I know this works, Do you have proof, Can you provide references, What's your track record, Can I see case studies, Do you have testimonials, How long have you been around, What's your success rate, Is it compatible with our system, Does it integrate with Salesforce, What's the learning curve, Can it handle our volume, Is it cloud-based, How's the uptime, What about data privacy, API available, Customization options, What's the expected ROI, How long until payback, What's the total cost, Are there hidden costs, What's the contract length, Can we cancel

---

## INTENT 4: NEGATIVE (60 signals)

Not interested, Not a fit, Wrong person, Wrong company, Not relevant, Not applicable, Doesn't apply to us, Not needed, Already have a solution, Using something else, No thanks, Pass, Not now, Not at this time, Maybe later, Not in our plans, Low priority, Wrong timing, Bad timing, Remove me, Unsubscribe, Stop emailing, Stop calling, Don't contact again, Please stop, Leave me alone, Stop bothering, Spam, Report spam, Don't send more, Remove from list, Block, Blocked, Unsubscribed, Waste of time, Irrelevant, Unwanted, Unsolicited, Junk, Garbage, Annoying, Irritating, Intrusive, Aggressive marketing, Too pushy, We already have this, Using X instead, Prefer Y solution, Built our own, Not switching vendors, Locked into contract, Happy with current provider, No plans to change, Satisfied with existing tool, No budget, Budget frozen, Can't afford, Out of scope, Not in budget, Too expensive, Not approved, No funding, After next quarter, Next year maybe, Not my department, Not my problem, Ask someone else, Wrong contact, You need to talk to, That's handled by, Not my area, F*** off, Never contact again, This is harassment, Reported to my company, Going to complain, Cease and desist, Blacklisted

---

## INTENT 5: OUT OF OFFICE (40 signals)

Out of office, Out of the office, Away from office, I'm away, I'm out, Currently out, Out on, Will be back, Back on, Returning on, Out until, Out through, I will return, Back Monday, Returning next week, Away until, Out through the 15th, Return date, Back from vacation, I'll be back on, On vacation, Taking time off, On leave, Sabbatical, Maternity leave, Paternity leave, Medical leave, Personal leave, Traveling, On a trip, Conference, Training, Team building, Out of office contact, I'm away reach out to, Out until Friday contact, On vacation my colleague, Out of office forwarding, Will forward to team, Out with limited email access, Out with no email access, Out but checking email, Limited connectivity, May have delays, Away for the rest of the week, Working from home, Off-site

---

## INTENT 6: BOUNCE (50 signals)

550 User not found, 554 Address rejected, Invalid recipient, User unknown, No such user, Account disabled, Mailbox not found, Invalid mailbox, Address does not exist, Recipient rejected, Mailbox unavailable, Mailbox closed, 451 Mailbox temporarily unavailable, 452 Mailbox full, Over quota, Temporary failure, Try again later, Service unavailable, Host unavailable, Connection timeout, Timeout, Temporary error, Delivery failed, Mail delivery failed, Message undeliverable, Unable to deliver, Return to sender, Returned mail, Non-delivery report, Delivery status notification, Undeliverable message, 550 SPF check failed, DKIM authentication failed, DMARC policy violation, TLS required, Certificate error, Message blocked by filter, Rejected by spam filter, Blacklisted sender, Policy violation, Rejected by policy, Blocked by provider, Domain not found, DNS lookup failed, MX record not found, Invalid domain, Domain expired, Account closed, Account deleted, Person no longer with company, Employee terminated, Left the company

---

## INTENT 7: AMBIGUOUS (50 signals)

Empty string, ..., ., ?, Yes, No, Ok, K, Yep, Nope, Maybe, IDK, Not sure, Hmm, Interesting, Cool, Thanks, Got it, Understood, Will do, Interested, Later, When, Why, How, Cost, Timeline, Demo, Meeting, Call, Email, Info, Details, Interested but not now, Tell me more but busy, Sounds good but skeptical, Want to learn but no budget, Could work but need approval, This looks good emoji, Hmm interesting, Will review and get back, Let me check with team, Similar to what we discussed, Can't open attachment, Intrested, Schdeule, Whens good, Wy sent, Unabel access, Emoji only, Merci, Spanish question, Foreign characters, Forwarded message, Just signature, Calendar invite only, Depends on, If you can do, Could work, Need to check, Maybe later

---

## QUICK STATS

```
Positive Interest:    45 signals
Meeting Request:      45 signals
Question:             55 signals
Negative:             60 signals
Out of Office:        40 signals
Bounce:               50 signals
Ambiguous:            50 signals
─────────────────────────────
TOTAL:               345 signals
```

---

## FORMAT FOR DATABASE

### CSV Format
```csv
intent,signal,category,confidence
positive_interest,"Tell me more",direct,85
positive_interest,"Sounds interesting",direct,80
meeting_request,"Can we schedule a call?",direct,95
...
```

### JSON Format
```json
{
  "signals": [
    {
      "intent": "positive_interest",
      "signal": "Tell me more",
      "category": "direct",
      "confidence": 85
    },
    {
      "intent": "positive_interest",
      "signal": "Sounds interesting",
      "category": "direct",
      "confidence": 80
    }
  ]
}
```

### ARRAY Format (Python/JavaScript)
```python
signals = {
  "positive_interest": [
    "Tell me more",
    "Sounds interesting",
    "Let's connect",
    ...
  ],
  "meeting_request": [
    "Can we schedule a call?",
    "Are you available for a meeting?",
    ...
  ],
  ...
}
```

---

## How to Use This

**Step 1:** Copy signals by intent  
**Step 2:** Load into database  
**Step 3:** For each reply, check against signals  
**Step 4:** Classify by intent  
**Step 5:** Assign confidence  

---

## Classification Logic (Pseudocode)

```
for each signal_list in intents:
  if reply.contains(signal_list):
    return intent
  
// If no match found
return AMBIGUOUS
```

---

Done! Easy to use list. 📋

