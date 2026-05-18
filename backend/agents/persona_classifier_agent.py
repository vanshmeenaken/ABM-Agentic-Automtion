"""Persona Classifier Agent — maps designations to buyer personas with confidence scoring."""

import json
from pathlib import Path
from typing import Dict, Any, List
from anthropic import Anthropic, APIError
from agents.schemas import PersonaClassifierInput, PersonaClassifierOutput


def load_agent_config(agent_id: str) -> Dict[str, Any]:
    """Load agent configuration from JSON registry."""
    registry_path = Path(__file__).parent / "registry" / f"{agent_id}.json"
    with open(registry_path) as f:
        return json.load(f)


def create_persona_classifier_agent():
    """Factory function to create Persona Classifier Agent from registry."""

    config = load_agent_config("persona_classifier")
    client = Anthropic()

    def classify_personas(classifier_input: PersonaClassifierInput) -> PersonaClassifierOutput:
        """Run the Persona Classifier Agent on cleaned prospects."""

        # Validate input using Pydantic
        validated_input = PersonaClassifierInput(**classifier_input.model_dump())

        # Build user message
        user_message = f"""Classify prospects by buyer persona:

Campaign type: {validated_input.campaign_type}
Target personas: {', '.join(validated_input.target_personas)}
Number of prospects: {len(validated_input.cleaned_prospects)}

Follow your reasoning steps and use the create_persona_classification_result tool to output persona assignments with confidence scores."""

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
                raise ValueError("Agent did not return create_persona_classification_result tool use")

            # Parse tool input as output schema
            output_data = tool_use_block.input
            classifier_output = PersonaClassifierOutput(**output_data)

            return classifier_output

        except APIError as e:
            raise RuntimeError(f"Persona Classifier Agent API error: {e}") from e
        except ValueError as e:
            raise ValueError(f"Output validation error: {e}") from e

    return classify_personas


# Convenience: create global agent instance
agent = create_persona_classifier_agent()


def run_persona_classifier(
    cleaned_prospects: List[Dict],
    campaign_type: str,
    target_personas: List[str],
) -> PersonaClassifierOutput:
    """Run Persona Classifier Agent with raw arguments."""

    classifier_input = PersonaClassifierInput(
        cleaned_prospects=cleaned_prospects,
        campaign_type=campaign_type,
        target_personas=target_personas,
    )

    return agent(classifier_input)
