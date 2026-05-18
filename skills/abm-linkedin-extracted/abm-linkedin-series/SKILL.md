---
name: abm-linkedin-series
description: Generate a 3-message LinkedIn ABM outreach series and a companion ABM Master Document for any completed Ken Research industry report. ALWAYS trigger this skill when Namit or any Ken Research team member wants to run a LinkedIn ABM campaign for a completed report, wants to draft outreach messages for a new report, mentions "ABM messages", "LinkedIn sequence", "message series", "ABM campaign", "LinkedIn outreach for [report title]", or wants to convert a completed study into a demand-generation campaign. Also trigger when a report brief or ABM Master Doc is pasted alongside a request to create messages, campaign content, or a target outreach series. Produces: (1) a 3-message LinkedIn DM series with A/B opening hook variants and send-timing guidance, and (2) a structured ABM Master Document as a Word DOCX file covering project summary, TG analysis, differentiators, pain points, and illustrative talking points.
---

# ABM LinkedIn Series — Ken Research

## What This Skill Does

Takes a completed Ken Research report title and/or brief and produces:

1. **3-Message LinkedIn DM Series** — casual, human-voice outreach across ice-breaker, sample share, and FOMO messages, with A/B opening hook variants and recommended send timing
2. **ABM Master Document** — always generated as a Word DOCX file, covering project summary, TG definition, persona pain points, differentiators, and illustrative talking points

---

## Step 1: Clarifying Questions

Before generating, ask Namit these questions if not already answered in the brief:

**Required inputs:**
- Report title (always required)
- One-line description of what the report covers (if not in brief)
- The "hero number" or headline stat — if the report has one (e.g., "57 projects", "SAR 206 Bn CAPEX"). If not available, messaging leads with a hook instead.
- Broad TG designations (e.g., CXOs, VPs Sales, Regional Heads) — infer company types from the market title, but confirm if ambiguous
- Any specific timing hook for the FOMO message (e.g., "FY2026 tender window is open") — optional, skill will infer if not provided
- Is there a sample / illustrative to attach for Message 2? If yes, note as confirmed. If not, flag as placeholder.

**Do not ask if already inferable from:**
- The report title (geography, sector, TG company type)
- The ABM Master Doc pasted by the user
- The report brief pasted by the user

---

## Step 2: Generate the ABM Master Document as DOCX

The ABM Master Document is always produced as a Word DOCX file. Generate it every time, without waiting to be asked.

Use the docx npm library. Install if needed: `npm install -g docx`

### Formatting Standard
- Font: Arial throughout
- Page size: US Letter (12240 x 15840 DXA), 1-inch margins (1440 DXA each side), content width 9360 DXA
- Colour palette: deep purple #4B2E83 (headers, borders, accents), light purple #7B5EA7 (subheadings), pale purple #EDE7F6 (table header fills, callout backgrounds), white #FFFFFF (body cells)
- Tables: always set both columnWidths on the table AND width on each cell using WidthType.DXA. Never use WidthType.PERCENTAGE.
- Cell shading: always ShadingType.CLEAR, never SOLID
- Borders: BorderStyle.SINGLE, size 1, color BDBDBD for standard table borders
- Cell margins: top 80, bottom 80, left 140, right 140 (DXA)
- Header: Ken Research branding line, purple, with bottom border
- Footer: "Confidential | Ken Research" left, page note right, purple, with top border
- No em dashes, no hyphens used as dashes anywhere in the document. Use colons or restructure the sentence.

### ABM Master Document Structure

Produce four sections in order:

#### SECTION 1 — Project Summary

**1.1 What Is This Project?**
Describe what was delivered as a specific intelligence product, not a generic market report. Emphasise primary research or project-level nature. Pull from the brief or infer from report title.

**1.2 What the Intelligence Covers**
Two-column table:
- Left column header: Report-Level Data Points
- Right column header: Sector-Specific Data Points
- 5-6 rows covering methodology, segmentation, competitive landscape, demand drivers, stakeholder mapping, and forward outlook

**1.3 Why This Matters — Business Context**
2-3 sentences on the macro driver and why the timing is commercially relevant for the TG.

**Campaign Objective callout box:**
Purple left border, pale purple background. Text: book qualified meetings and run need-discovery conversations. Do not assume productisation intent unless Namit mentions it.

---

#### SECTION 2 — ABM Framework

**2.1 Target Group Definition**
Three-column table: Company Type | Profile | Examples
- 4-5 company types inferred from market title and sector
- Real company names where known; flag all as "[confirm before use]"

**2.2 Target Designations for LinkedIn Outreach**
Three-column table: Primary Targets (Decision Makers) | Secondary Targets (Influencers) | Geography Filter
- Primary: VP/Director and above in Sales, BD, Strategy, or relevant function
- Secondary: Manager level in BD, Marketing, Tendering, Account Management
- Geography: infer from report market; always include HQ geographies of likely manufacturers alongside target market

**2.3 Need, Desire and Pain Point**
Single-row three-column table: NEED | DESIRE | PAIN POINT

Then a two-column table: Persona | Core Pain Point
- 4-5 personas, each with a verbatim-style first-person quote capturing their core frustration

**2.4 Differentiator — What Makes This Different**
Three-column table: What Others Offer | What This Offers | Why It Matters
- 5 rows minimum
- Always contrast generic market data vs. Ken Research's primary research or project-level output

**2.5 Illustrative — Sample Proof of Value**
Bullet list of what the Message 2 attachment should show (5 items).

Key Illustrative Talking Point callout box: the single insight that makes a VP of Sales sit up.

Red-bordered manual input box: "Confirm illustrative / sample dashboard is prepared and approved before Message 2 send."

---

#### SECTION 3 — LinkedIn Message Series

Present all three messages formatted in pale purple callout boxes.

For Message 1: show Hook Selection label first (hook type + one-line hook), then Variant A, then Variant B.
For Message 2 and Message 3: single version each, with the manual input placeholder for Message 2 inside the callout box.

---

#### SECTION 4 — Send Timing and Manual Input Checklist

**4.1 Send Timing Summary**
Three-column table: Message | Recommended Send Day | Notes

**4.2 Manual Input Checklist**
Numbered list of all items requiring confirmation before campaign goes live.

Footer disclaimer: "This document is prepared by Ken Research for internal campaign planning purposes. All company examples marked [confirm before use] require verification before LinkedIn outreach commences."

---

### DOCX Output
Save to `/mnt/user-data/outputs/[ReportTitle]_ABM_MasterDoc.docx`
Validate with: `python scripts/office/validate.py [filepath]`
Present to Namit using the present_files tool after validation passes.

---

## Step 3: Generate the 3-Message LinkedIn DM Series

### Voice and Style Rules

- Casual, human-voice LinkedIn DM register
- Minimal grammar correction only — preserve cadence, short punchy lines, natural pauses
- "let's" not "lets" — applied consistently
- No em dashes anywhere. No hyphens used as dashes anywhere. Zero tolerance.
- If a sentence would use a dash, rewrite it: use a colon, split into two sentences, or restructure
- No formal openers, no sign-offs, no "I hope this finds you well"
- No hollow adjectives ("comprehensive", "cutting-edge", "robust")
- No AI-style preamble
- Maintain professional power balance — write as a peer, not a vendor
- One CTA per message. Never stack two asks.

**Dash check before output:** Read every message character by character. If any dash character appears (hyphen used as a pause, en dash, em dash), rewrite that sentence before presenting.

---

### Message 1 — Ice Breaker

**Goal:** Establish relevance, signal credibility, earn a reply or connection.
**Send timing:** Day 1 of campaign

**Hook Selection — Do This First:**
Before drafting Message 1, identify the strongest hook the report data supports. Pick exactly one:

- **Whitespace hook:** An underserved segment, geography, or customer type the market has not yet moved into at scale. Use when the report reveals a gap no one is filling yet.
- **Sweet spot hook:** The specific band, tier, corridor, or segment where the economics work best. Use when the report reveals a high-return pocket within a larger market.
- **Emerging niche hook:** A trend, behaviour shift, or regulatory tailwind creating a new demand pocket not yet on most competitors' radars. Use when the report reveals something early-stage and directionally significant.

State the hook type and the one-line hook before generating variants. If the report has a hero number, embed it inside whichever variant it strengthens. Do not let the hero number replace the hook.

**Format:**
- 3 short paragraphs maximum
- Paragraph 1: the hook, delivered as an observation not a pitch. No dashes of any kind.
- Paragraph 2: one sentence on what the study covers, specific not generic. One sentence on timing relevance.
- Paragraph 3: CTA only. Propose a specific time slot ("around [time] GST tomorrow" or "this week").

**A/B Variants:**
Both use the same hook. Difference is framing angle only:

- **Variant A — Analytical Framing:** Hook delivered as a structural market observation. Tone: "we found something worth knowing." No urgency language.
- **Variant B — Competitive Urgency Framing:** Same hook framed as a window narrowing. Early movers are acting. Tone: "the companies moving on this now are ahead." Mild urgency, no pressure.

Generate both variants in full.

---

### Message 2 — Sample Share

**Goal:** Move from interest to tangibility. Get them to consume the sample.
**Send timing:** Day 3-4 after Message 1 (or after a reply, whichever comes first)

**Format:**
- 2-3 lines only, intentionally minimal
- No dashes of any kind
- Reference Message 1 lightly without restating it
- Signal the attachment
- One soft CTA: "let's connect after you've had a look"

**[MANUAL INPUT NEEDED: Sample / illustrative dashboard to be attached before send]**

---

### Message 3 — FOMO / Fallback

**Goal:** Re-engage non-responders. Create urgency without desperation. Leave on a networking note.
**Send timing:** Day 7-10 after Message 2

**Format:**
- 3 short paragraphs
- No dashes of any kind
- Paragraph 1: release follow-up pressure explicitly ("no follow-up needed on the sample")
- Paragraph 2: if timing hook exists, surface the window as a heads-up not a sales push. If no timing hook, use the hook from Message 1 (whitespace / sweet spot / emerging niche) as a useful observation.
- Paragraph 3: fallback CTA. Offer to connect on how they are currently tracking the relevant metric or planning for the market. Peer-to-peer framing.

---

## Step 4: Output Format

Present in this order:

1. **ABM Master Document DOCX** — generated and presented via present_files
2. **Hook Selection** — one line: hook type chosen and the hook itself
3. **Message Series** — clearly labelled:
   - Message 1: Variant A / Variant B
   - Message 2
   - Message 3
4. **Send Timing Summary** — 3-row table: Message | Recommended Send Day | Notes
5. **Manual Input Checklist** — bullet list of items to confirm before go-live

---

## Quality Checks Before Output

- No em dashes anywhere in messages or Master Doc
- No hyphens used as dashes anywhere in messages or Master Doc. Colons or sentence breaks only.
- Message 1: hook is in the opening line of both variants, not buried
- Message voice: if any message reads like a sales email, rewrite as a DM
- Hero number: if available, present in at least one of the three messages
- FOMO message: ends on peer-to-peer networking note, not a hard close
- All placeholder data marked with [BRACKETS]
- TG company examples flagged for confirmation

---

## Reference Examples

### Voice Benchmark

**Message 1 Variant A (sweet spot hook, analytical framing, no dashes):**
> Hi [First Name], most operators in Kuwait's car rental and leasing market are still fleet-heavy on the short-term side. The margin story sits almost entirely in long-term corporate and government leasing: the segment growing faster, contracting better, and attracting the larger GCC players first.
>
> We just wrapped a market intelligence study that maps the operator landscape, fleet economics, and demand segmentation across both segments. Built from primary research, not a top-down model.
>
> Worth a quick look. Let's connect over a call around 12:00 PM GST time tomorrow?

**Message 1 Variant B (same hook, competitive urgency framing, no dashes):**
> Hi [First Name], the larger GCC rental operators are already moving into Kuwait's corporate leasing segment. It is the sweet spot where contract tenure, utilisation, and margins are strongest, and the companies repositioning their fleet mix toward it now will be in a very different place in 18 months.
>
> We just completed a market intelligence study covering the Kuwait operator landscape, segment economics, and fleet demand by customer type. If this market is on your radar, it is worth having the data before the window tightens.
>
> Let's connect over a call. Are you free around 12:00 PM GST tomorrow?

**Message 2 (no dashes):**
> Hey [First Name], sharing a quick sample from the Kuwait study for your reference. Covers the operator landscape, segment split, and pricing benchmarks.
>
> Let's connect once you've had a look through it. [MANUAL INPUT: Attach sample before send]

**Message 3 (no dashes):**
> Hey [First Name], no follow-up needed on the sample. Timing may just not be right.
>
> One thing worth flagging: the Q3 to Q4 corporate fleet renewal cycle is the primary procurement window for leasing contracts in Kuwait, and a few of the larger operators are already in vendor conversations for next year. Companies that go into that window with a structured view of the competitive landscape tend to close contracts faster.
>
> Either way, let's connect once and compare notes on how you are tracking fleet demand and planning your Kuwait positioning for the next cycle.

Use these as the benchmark for cadence and register. Do not copy them. Generate fresh versions calibrated to the specific report.
