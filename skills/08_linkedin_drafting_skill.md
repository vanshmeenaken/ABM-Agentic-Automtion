# Skill: LinkedIn Drafting

**Used by:** Message Intelligence Layer (future: LinkedIn Copy Agent)  
**Domain:** LinkedIn message and connection request copy

---

## Purpose
Provides format, tone, and content rules for LinkedIn connection request notes and follow-up messages in the context of ABM campaigns.

---

## When to use
When LinkedIn-channel messages are added to a campaign. Note: LinkedIn sending is handled by LinkedHelper, not the platform. This skill produces draft copy for LinkedHelper campaign setup.

---

## Connection request note
- Max 300 characters (LinkedIn hard limit)
- Personalised opening (name + company or shared context)
- One-line reason for connecting
- No sales pitch in connection request
- No URLs

**Template pattern:**
"Hi [Name], noticed your work at [Company] in [industry context]. Would love to connect."

---

## Follow-up message (post-connection)
- Max 300 words
- Wait at least 48h after connection accepted before sending
- Reference the connection context
- One clear value proposition
- Soft CTA (reply or call)
- No aggressive pitching on first message

---

## Persona tone guidelines
| Persona | LinkedIn tone |
|---------|--------------|
| CXO / Strategy | Peer-level, industry insight angle |
| Marketing | Collaborative, insight-sharing angle |
| Operations | Efficiency + benchmark angle |
| Product / R&D | Innovation + technology trend angle |
| Investor | Market signal + opportunity angle |

---

## Rules
- LinkedIn messages are not sent by the platform — copy is prepared for LinkedHelper setup
- Connection request must never include pricing or service offerings
- Follow-up message must reference the specific connection context

---

## Failure cases
- Connection request over 300 chars → trim to 280 chars with buffer
- Follow-up sent same day as connection → flag timing violation
