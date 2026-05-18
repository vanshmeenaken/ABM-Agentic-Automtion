"""Prospect Research Agent — builds raw target account and contact list from approved sources."""

import json
from pathlib import Path
from typing import Dict, Any
from anthropic import Anthropic, APIError
from agents.schemas import ProspectResearchInput, ProspectResearchOutput


def load_agent_config(agent_id: str) -> Dict[str, Any]:
    """Load agent configuration from JSON registry."""
    registry_path = Path(__file__).parent / "registry" / f"{agent_id}.json"
    with open(registry_path) as f:
        return json.load(f)


def create_prospect_research_agent():
    """Factory function to create Prospect Research Agent from registry."""

    config = load_agent_config("prospect_research")
    client = Anthropic()

    def research_prospects(prospect_input: ProspectResearchInput) -> ProspectResearchOutput:
        """Run the Prospect Research Agent on a campaign request."""

        # Validate input using Pydantic
        validated_input = ProspectResearchInput(**prospect_input.model_dump())

        # Build user message with prospect research input
        user_message = f"""Build prospect list for campaign:

Campaign ID: {validated_input.campaign_id}
Target industry: {validated_input.icp_definition.positive.industries}
Target region: {validated_input.icp_definition.positive.regions}
Company size: {validated_input.icp_definition.positive.company_size}
Target personas: {[p.persona for p in validated_input.persona_map]}
Approved sources: {', '.join(validated_input.approved_sources)}
Max prospects: {validated_input.max_prospects}
Notes: {validated_input.notes if validated_input.notes else "None"}

Follow your reasoning steps and use the create_prospect_research_result tool to output the raw prospect list."""

        try:
            # Call Claude with system prompt cached
            response = client.messages.create(
                model=config["model"],
                max_tokens=4096,
                system=[
                    {
                        "type": "text",
                        "text": config["system_prompt"],
                        "cache_control": {"type": "ephemeral"},
                    }
                ],
                tools=config["tools"],
                messages=[{"role": "user", "content": user_message}],
            )

            # Extract tool use from response
            tool_use_block = None
            for block in response.content:
                if block.type == "tool_use":
                    tool_use_block = block
                    break

            if not tool_use_block:
                raise ValueError("Agent did not return create_prospect_research_result tool use")

            # Parse tool input as output schema
            output_data = tool_use_block.input
            prospect_output = ProspectResearchOutput(**output_data)

            return prospect_output

        except APIError as e:
            raise RuntimeError(f"Prospect Research Agent API error: {e}") from e
        except ValueError as e:
            raise ValueError(f"Output validation error: {e}") from e

    return research_prospects


# Convenience: create global agent instance
agent = create_prospect_research_agent()


def run_prospect_research(
    campaign_id: str,
    icp_definition: Dict,
    persona_map: list,
    approved_sources: list,
    max_prospects: int = 500,
    notes: str = None,
) -> ProspectResearchOutput:
    """Run Prospect Research Agent with raw arguments."""

    prospect_input = ProspectResearchInput(
        campaign_id=campaign_id,
        icp_definition=icp_definition,
        persona_map=persona_map,
        approved_sources=approved_sources,
        max_prospects=max_prospects,
        notes=notes,
    )

    return agent(prospect_input)
