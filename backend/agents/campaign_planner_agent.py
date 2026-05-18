"""Campaign Planner Agent — converts raw campaign ideas into structured plans."""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
from anthropic import Anthropic, APIError
from agents.schemas import CampaignPlannerInput, CampaignPlannerOutput


def load_agent_config() -> Dict[str, Any]:
    """Load agent configuration from JSON registry."""
    registry_path = Path(__file__).parent / "registry" / "campaign_planner.json"
    with open(registry_path) as f:
        return json.load(f)


def create_campaign_planner_agent():
    """Factory function to create Campaign Planner Agent from registry."""

    config = load_agent_config()
    client = Anthropic()

    def plan_campaign(campaign_input: CampaignPlannerInput) -> CampaignPlannerOutput:
        """Run the Campaign Planner Agent on a campaign request."""

        # Validate input using Pydantic
        validated_input = CampaignPlannerInput(**campaign_input.model_dump())

        # Build user message with campaign input
        user_message = f"""Plan this campaign:

Campaign name: {validated_input.campaign_name}
Target industry: {validated_input.target_industry}
Target region: {validated_input.target_region}
Offer: {validated_input.offer}
Campaign type: {validated_input.campaign_type}
Preferred channels: {validated_input.preferred_channels if validated_input.preferred_channels else "None — use defaults"}
Notes: {validated_input.notes if validated_input.notes else "None"}

Follow your reasoning steps and use the create_campaign_draft tool to output the structured plan."""

        try:
            # Call Claude with system prompt cached
            response = client.messages.create(
                model=config["model"],
                max_tokens=2048,
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
                raise ValueError("Agent did not return create_campaign_draft tool use")

            # Parse tool input as output schema
            output_data = tool_use_block.input
            campaign_output = CampaignPlannerOutput(**output_data)

            return campaign_output

        except APIError as e:
            raise RuntimeError(f"Campaign Planner Agent API error: {e}") from e
        except ValueError as e:
            raise ValueError(f"Output validation error: {e}") from e

    return plan_campaign


# Convenience: create global agent instance
agent = create_campaign_planner_agent()


def run_campaign_planner(
    campaign_name: str,
    target_industry: str,
    target_region: str,
    offer: str,
    campaign_type: str,
    preferred_channels: Optional[list] = None,
    notes: Optional[str] = None,
) -> CampaignPlannerOutput:
    """Run Campaign Planner Agent with raw arguments."""

    campaign_input = CampaignPlannerInput(
        campaign_name=campaign_name,
        target_industry=target_industry,
        target_region=target_region,
        offer=offer,
        campaign_type=campaign_type,
        preferred_channels=preferred_channels,
        notes=notes,
    )

    return agent(campaign_input)
