"""Data Quality Agent — cleans raw prospect records and flags duplicates/low-confidence."""

import json
from pathlib import Path
from typing import Dict, Any, List
from anthropic import Anthropic, APIError
from agents.schemas import DataQualityInput, DataQualityOutput


def load_agent_config(agent_id: str) -> Dict[str, Any]:
    """Load agent configuration from JSON registry."""
    registry_path = Path(__file__).parent / "registry" / f"{agent_id}.json"
    with open(registry_path) as f:
        return json.load(f)


def create_data_quality_agent():
    """Factory function to create Data Quality Agent from registry."""

    config = load_agent_config("data_quality")
    client = Anthropic()

    def clean_prospects(quality_input: DataQualityInput) -> DataQualityOutput:
        """Run the Data Quality Agent on raw prospects."""

        # Validate input using Pydantic
        validated_input = DataQualityInput(**quality_input.model_dump())

        # Build user message
        user_message = f"""Clean and validate prospect records:

Campaign ID: {validated_input.campaign_id}
Deduplication scope: {validated_input.dedup_scope}
Number of raw prospects: {len(validated_input.raw_prospects)}

Follow your reasoning steps and use the create_data_quality_result tool to output cleaned prospects with quality scores and flags."""

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
                raise ValueError("Agent did not return create_data_quality_result tool use")

            # Parse tool input as output schema
            output_data = tool_use_block.input
            quality_output = DataQualityOutput(**output_data)

            return quality_output

        except APIError as e:
            raise RuntimeError(f"Data Quality Agent API error: {e}") from e
        except ValueError as e:
            raise ValueError(f"Output validation error: {e}") from e

    return clean_prospects


# Convenience: create global agent instance
agent = create_data_quality_agent()


def run_data_quality(
    raw_prospects: List[Dict],
    campaign_id: str,
    dedup_scope: str = "platform",
) -> DataQualityOutput:
    """Run Data Quality Agent with raw arguments."""

    quality_input = DataQualityInput(
        raw_prospects=raw_prospects,
        campaign_id=campaign_id,
        dedup_scope=dedup_scope,
    )

    return agent(quality_input)
