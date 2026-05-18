# Ken ABM Platform — Agent Framework

Complete agent framework with **Orchestrator** and **4 Logic-Based Agents**. Built for easy Anthropic API integration.

---

## Architecture Overview

```
Orchestrator (Main Engine)
├── Campaign Planner Agent (external - will be integrated)
├── Message Strategy Agent (logic-based)
├── Persona Classifier Agent (logic-based)
├── Email Copy Agent (logic-based)
└── WhatsApp Copy Agent (logic-based)
```

### Flow

```
1. Campaign Planner
   └─→ ICP definition, personas, channel plan

2. Message Strategy
   └─→ Tone, themes, value props, CTA

3. For Each Prospect:
   ├─→ Persona Classifier
   │   └─→ Primary persona, confidence, secondary persona
   ├─→ Email Copy Agent
   │   └─→ Subject, body, CTA, alternatives
   └─→ WhatsApp Copy Agent (with branching)
       └─→ Message, follow-ups, alternatives
       
   [Branching Logic]
   If phone exists → generate WhatsApp
   Else → skip WhatsApp, use Email/LinkedIn
```

---

## Current State

### ✅ Complete

- **Orchestrator** — Framework with agent registration, sequencing, branching logic
- **4 Agent Executors** — Logic-based implementations ready for Claude integration
- **Schemas** — Pydantic models for all inputs/outputs
- **JSON Registries** — Agent configs with system prompts and tool definitions
- **Stub Implementation** — Testable without API key

### 🔧 Ready for Integration

Each agent has clear placeholders where to add Anthropic SDK calls:

```python
# TODO: Replace with Anthropic API call
# 1. Load config from registry/[agent].json
# 2. Build user message with context
# 3. Call Anthropic API with system prompt + tool forcing
# 4. Parse tool response for structured output
```

---

## Quick Start

### Usage Without API Key

```python
from agents.orchestrator import run_orchestration
from agents.schemas import OrchestrationInput

# Define campaign and prospects
input_data = OrchestrationInput(
    campaign_name="Tech Market Research",
    target_industry="Technology",
    target_region="North America",
    offer="Market research report",
    campaign_type="Market Research",
    prospects=[
        {
            "email": "john@acmetech.com",
            "first_name": "John",
            "last_name": "Smith",
            "company_name": "Acme Tech",
            "designation": "VP of Engineering",
            "phone": "+1-555-0123",
        },
        {
            "email": "jane@acmetech.com",
            "first_name": "Jane",
            "company_name": "Acme Tech",
            "designation": "Senior Manager, Product",
            # No phone — will skip WhatsApp
        },
    ],
)

# Run orchestration (uses logic-based agents)
output = run_orchestration(input_data)

# View results
print(f"Processed: {output.execution_summary['total_prospects_processed']} prospects")
print(f"Email copies: {output.execution_summary['email_copies_generated']}")
print(f"WhatsApp messages: {output.execution_summary['whatsapp_copies_generated']}")
```

### Output Structure

```python
{
    "campaign_plan": {
        "campaign_draft": {...},
        "icp_definition": {...},
        "persona_map": [...],
        "channel_plan": {...},
    },
    "message_strategy": {
        "messaging_strategy": {
            "tone": "professional",
            "key_themes": [...],
            "value_propositions": {...},
            "call_to_action": "Schedule a call",
        },
        "persona_specific_messages": {...},
        "success_criteria": [...],
    },
    "prospect_messaging": [
        {
            "email": "john@acmetech.com",
            "persona_assignment": {
                "persona": "Director",
                "confidence_score": 88,
                "rationale": "VP maps to Director level",
            },
            "email_copy": {
                "primary_email": {
                    "subject": "Strategic opportunity for Acme Tech",
                    "body": "Hi John, ...",
                    "cta_text": "Schedule a call",
                },
                "alternative_variations": [...],
            },
            "whatsapp_copy": {
                "primary_message": {
                    "message": "Hi John, quick opportunity...",
                    "follow_up_messages": [...],
                },
            },
            "channels_used": ["email", "whatsapp", "linkedin"],
        },
        # ... more prospects
    ],
    "execution_summary": {
        "total_prospects_processed": 2,
        "email_copies_generated": 2,
        "whatsapp_copies_generated": 1,  // Skip if no phone
        "whatsapp_skipped_count": 1,
        "personas_assigned": ["Director", "Manager"],
    },
}
```

---

## Agents

### 1. Persona Classifier Agent

**Purpose:** Map prospects to buyer personas

**Input:**
- Prospect (email, name, designation, company)
- Target personas (from Campaign Planner)
- Campaign type

**Output:**
- Primary persona + confidence score
- Secondary persona (optional)
- Rationale for assignment

**File:** `agents/persona_classifier_agent.py`

**Logic:** Currently designation-based matching. Upgrade to Anthropic with system prompt `registry/persona_classifier.json`.

### 2. Message Strategy Agent

**Purpose:** Define messaging tone, themes, and value propositions

**Input:**
- Campaign name, type, offer
- Target personas
- Target industry
- Channel mix

**Output:**
- Tone (professional, consultative, urgent, etc.)
- Key themes
- Value props per persona
- Call-to-action
- Success criteria

**File:** `agents/message_strategy_agent.py`

**Logic:** Currently template-based. Upgrade to Anthropic with system prompt `registry/message_strategy.json`.

### 3. Email Copy Agent

**Purpose:** Generate email variations

**Input:**
- Persona
- Prospect (company, designation)
- Message strategy
- Campaign offer
- Tone

**Output:**
- Primary email (subject, preview, body, CTA)
- 2-3 alternative variations
- Personalization variables

**File:** `agents/email_copy_agent.py`

**Logic:** Currently template-based. Upgrade to Anthropic with system prompt `registry/email_copy.json`.

### 4. WhatsApp Copy Agent

**Purpose:** Generate conversational WhatsApp messages

**Input:**
- Persona
- Prospect (name, company, designation)
- Message strategy
- Campaign offer

**Output:**
- Primary message (< 160 chars)
- Follow-up messages (2-3)
- Alternative variations
- Personalization variables

**File:** `agents/whatsapp_copy_agent.py`

**Logic:** Currently template-based. Upgrade to Anthropic with system prompt `registry/whatsapp_copy.json`.

---

## Orchestrator API

### Registration

```python
from agents.orchestrator import get_orchestrator
from agents.persona_classifier_agent import agent as persona_classifier
from agents.message_strategy_agent import agent as message_strategy
from agents.email_copy_agent import agent as email_copy
from agents.whatsapp_copy_agent import agent as whatsapp_copy

orchestrator = get_orchestrator()

# Register agents
orchestrator.register_agent("persona_classifier", persona_classifier)
orchestrator.register_agent("message_strategy", message_strategy)
orchestrator.register_agent("email_copy", email_copy)
orchestrator.register_agent("whatsapp_copy", whatsapp_copy)
```

### Configuration

```python
orchestrator.config = {
    "skip_whatsapp_if_no_phone": True,  # Skip WhatsApp if phone missing
    "fallback_channels": ["email", "linkedin"],  # Fallback if WhatsApp fails
    "parallel_prospect_processing": False,  # Set to True for large batches (future)
}
```

### Execution Log

```python
output = run_orchestration(input_data)

# View execution log
for log_entry in output.execution_summary["execution_log"]:
    print(f"{log_entry['timestamp']} [{log_entry['level']}] {log_entry['message']}")
```

---

## Anthropic Integration Path

### Step 1: Implement Campaign Planner Agent

Once your team provides the agent, implement `run_campaign_planner()` in `agents/campaign_planner_agent.py`:

```python
from anthropic import Anthropic

def run_campaign_planner(input_data: Dict) -> Dict:
    config = load_agent_config("campaign_planner")
    client = Anthropic()
    
    user_message = f"""Generate campaign plan:
    Campaign: {input_data['campaign_name']}
    Industry: {input_data['target_industry']}
    ..."""
    
    response = client.messages.create(
        model=config["model"],
        system=config["system_prompt"],
        tools=config["tools"],
        messages=[{"role": "user", "content": user_message}],
    )
    
    # Extract tool use and parse output
    return parse_response(response)
```

### Step 2: Upgrade Message Strategy Agent

```python
def run_message_strategy(input_data: Dict) -> Dict:
    # Similar pattern:
    # 1. Load config["system_prompt"]
    # 2. Build user_message
    # 3. Call Anthropic API
    # 4. Parse tool response
```

### Step 3: Upgrade Email & WhatsApp Copy Agents

Same pattern for `email_copy_agent.py` and `whatsapp_copy_agent.py`.

### Step 4: No Changes to Orchestrator

The Orchestrator doesn't care if agents use logic or Anthropic — it just calls them. No refactoring needed!

---

## File Structure

```
agents/
├── __init__.py                           # Exports all agents
├── schemas.py                            # Pydantic models
├── orchestrator.py                       # Main orchestrator (NEW)
├── campaign_planner_agent.py             # (existing, will integrate)
├── persona_classifier_agent.py           # (NEW - logic-based)
├── message_strategy_agent.py             # (NEW - logic-based)
├── email_copy_agent.py                   # (NEW - logic-based)
├── whatsapp_copy_agent.py                # (NEW - logic-based)
├── prospect_research_agent.py            # (existing)
├── data_quality_agent.py                 # (existing)
├── README.md                             # This file
└── registry/
    ├── campaign_planner.json             # (existing)
    ├── persona_classifier.json           # (NEW)
    ├── message_strategy.json             # (NEW)
    ├── email_copy.json                   # (NEW)
    ├── whatsapp_copy.json                # (NEW)
    ├── prospect_research.json            # (existing)
    └── data_quality.json                 # (existing)
```

---

## Testing

### Test Without API Key

```python
from agents.orchestrator import run_orchestration
from agents.schemas import OrchestrationInput

# Run with stub implementations
output = run_orchestration(input_data)
assert len(output.prospect_messaging) > 0
assert output.execution_summary["email_copies_generated"] > 0
```

### Test with Mock Agents (When Ready)

```python
from unittest.mock import patch

with patch("agents.persona_classifier_agent.run_persona_classifier") as mock:
    mock.return_value = {"persona": "CXO", "confidence_score": 95, ...}
    output = run_orchestration(input_data)
    # Assertions
```

---

## Design Decisions

### ✅ Why This Architecture?

1. **Clean Separation** — Each agent is independent, testable, upgradeable
2. **Framework First** — Logic/stub implementations first, API integration later
3. **No Refactoring** — Orchestrator works with any agent implementation
4. **JSON Registries** — System prompts, tools, schemas in one place (easy to version)
5. **Branching Logic** — Built into orchestrator, not scattered in agents
6. **Extensible** — Add new agents by registering them, no code changes needed

### ✅ Why Logic-Based First?

- **No API key needed** — Ship today, integrate Anthropic tomorrow
- **Fast iteration** — Test orchestration flow immediately
- **Baseline quality** — Demonstrates what's possible with logic
- **Easy upgrade** — Swap logic with API calls without touching orchestrator

---

## Next Steps

1. **Test the orchestrator** with stub data
2. **Provide Campaign Planner Agent** — Will plug in directly
3. **Implement Anthropic integration** — One agent at a time
4. **Add to Django** — Orchestrator + agents as Django task or API

---

## Questions?

Refer to individual agent files (`persona_classifier_agent.py`, etc.) for:
- Input schema details
- Output structure
- Integration points for Anthropic API

---

**Status:** Framework complete. Logic-based agents ready. Anthropic integration path clear.
