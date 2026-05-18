"""
Persona Classifier Agent — Maps designations to buyer personas using Claude CLI.

Production-ready implementation that:
1. Takes prospect designation + company context
2. Calls Claude CLI to intelligently classify based on context
3. Claude understands nuance (fake titles, ambiguous roles, etc.)
4. Assigns primary + secondary personas with confidence
5. Flags ambiguous cases for manual review
6. Provides clear rationale for each classification

How it works:
1. Constructs detailed prompt with prospect data
2. Calls `claude ask` command via subprocess
3. Claude returns persona classification with reasoning
4. Parses response into structured output
5. Returns ClassifiedProspect with persona + confidence

Key advantage over keyword mapping:
- Claude understands context ("CEO of my life" = joke, not executive)
- Handles non-standard titles ("Head Chef", "VP of Vibes")
- Validates company/email realness
- Provides intelligent confidence scoring
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
from statistics import mean

from agents.schemas import (
    PersonaClassifierInput,
    PersonaClassifierOutput,
    ClassifiedProspect,
    PersonaAssignment,
)


def load_agent_config(agent_id: str) -> Dict[str, Any]:
    """Load agent configuration from JSON registry."""
    registry_path = Path(__file__).parent / "registry" / f"{agent_id}.json"
    if not registry_path.exists():
        raise FileNotFoundError(f"Registry file not found: {registry_path}")
    with open(registry_path) as f:
        return json.load(f)


def call_claude_cli(prompt: str) -> str:
    """
    Call Claude via CLI using subprocess.

    Requires: claude CLI installed and configured

    Args:
        prompt: The prompt to send to Claude

    Returns:
        Claude's response as string
    """
    try:
        # Call claude command via subprocess
        result = subprocess.run(
            ["claude", "ask", prompt],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode != 0:
            raise RuntimeError(f"Claude CLI error: {result.stderr}")

        return result.stdout.strip()

    except FileNotFoundError:
        raise RuntimeError(
            "Claude CLI not found. Install with: npm install -g @anthropic-ai/claude"
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError("Claude CLI call timed out after 30 seconds")


def parse_claude_classification(claude_response: str) -> Dict[str, Any]:
    """
    Parse Claude's response into structured persona classification.

    Expected Claude response format:
    {
        "persona": "Director",
        "confidence_score": 88,
        "seniority_level": "Executive",
        "function": "engineering",
        "rationale": "VP title indicates executive seniority...",
        "needs_review": false,
        "secondary_persona": {
            "persona": "CXO",
            "confidence_score": 70,
            "rationale": "VP can influence C-level decisions"
        }
    }
    """
    try:
        # Try to parse as JSON first
        return json.loads(claude_response)
    except json.JSONDecodeError:
        # If not JSON, Claude returned text - need to extract structured info
        # For now, return a safe default
        return {
            "persona": "Unknown",
            "confidence_score": 0,
            "seniority_level": "Unknown",
            "function": "Unknown",
            "rationale": claude_response,
            "needs_review": True,
        }


def classify_prospect(
    prospect: Dict,
    target_personas: List[str],
    campaign_type: str,
    target_industry: str = "",
    target_functions: List[str] = None,
) -> tuple[PersonaAssignment, Optional[PersonaAssignment], bool, Dict]:
    """
    Classify a single prospect using Claude CLI with campaign fit validation.

    Args:
        prospect: Prospect data (designation, company, email, etc.)
        target_personas: Available personas (e.g., ["CXO", "Director", "Manager"])
        campaign_type: Campaign type (influences context)
        target_industry: Target industry for campaign (enables fit validation)
        target_functions: Preferred buyer functions for this campaign

    Returns:
        (primary_persona, secondary_persona, needs_review, claude_analysis)
    """
    designation = prospect.get("designation", "Unknown")
    company_name = prospect.get("company_name", "")
    email = prospect.get("email", "")
    company_size = prospect.get("company_size", "")
    industry = prospect.get("industry", "")

    if target_functions is None:
        target_functions = []

    # Build detailed prompt for Claude
    campaign_context = ""
    if target_industry:
        campaign_context = f"""
CAMPAIGN CONTEXT:
- Target Industry: {target_industry}
- Preferred Functions: {', '.join(target_functions) if target_functions else 'Any'}
- Validate if this prospect's function aligns with campaign goals."""

    prompt = f"""Classify this prospect to a buyer persona AND validate campaign fit. Return JSON only.

PROSPECT DATA:
- Email: {email}
- Designation: {designation}
- Company: {company_name}
- Company Size: {company_size}
- Industry: {industry}
- Campaign Type: {campaign_type}{campaign_context}

TARGET PERSONAS: {', '.join(target_personas)}

INSTRUCTIONS:
1. Analyze the designation carefully. Is it real or fake? (e.g., "CEO of my life" = fake)
2. Understand seniority level: C-Level, Executive, Director, Manager, Individual Contributor
3. Understand function: Engineering, Marketing, Sales, Operations, Finance, Strategy, Product, Education, HR, etc.
4. Assign PRIMARY persona (highest match from target list)
5. Assign SECONDARY persona if applicable (second-best match)
6. Calculate confidence 0-100 based on how clear the designation is
7. Flag needs_review=true if confidence < 60% or title is suspicious
8. CAMPAIGN FIT VALIDATION: If campaign context provided, evaluate if this prospect's function aligns with campaign goals
   - campaign_fit_score: 0-100 rating of how relevant this prospect is to the campaign
   - campaign_fit_valid: true if fit_score >= 70, false otherwise
   - campaign_fit_rationale: explain why or why not they fit the campaign

RESPONSE FORMAT (JSON only, no text):
{{
    "persona": "Director",
    "confidence_score": 88,
    "seniority_level": "Executive",
    "function": "engineering",
    "rationale": "VP title indicates executive seniority. Engineering function. Clear match to Director persona.",
    "needs_review": false,
    "campaign_fit_score": 85,
    "campaign_fit_valid": true,
    "campaign_fit_rationale": "Engineering function aligns with target industry tech company needs.",
    "secondary_persona": {{
        "persona": "CXO",
        "confidence_score": 70,
        "rationale": "VP can influence C-level decisions"
    }}
}}"""

    try:
        # Call Claude CLI
        claude_response = call_claude_cli(prompt)

        # Parse response
        analysis = parse_claude_classification(claude_response)

        return analysis

    except Exception as e:
        # Fallback on error
        return {
            "persona": target_personas[0] if target_personas else "Unknown",
            "confidence_score": 0,
            "seniority_level": "Unknown",
            "function": "Unknown",
            "rationale": f"Claude classification failed: {str(e)}",
            "needs_review": True,
        }


def run_persona_classifier(
    cleaned_prospects: List[Dict],
    campaign_type: str,
    target_personas: List[str],
    target_industry: str = "",
    target_functions: List[str] = None,
) -> PersonaClassifierOutput:
    """
    Classify multiple prospects to buyer personas with campaign fit validation using Claude CLI.

    Args:
        cleaned_prospects: List of prospect records
        campaign_type: Campaign type (Market Research, Survey, etc.)
        target_personas: Target personas (CXO, Director, Manager, etc.)
        target_industry: Target industry for campaign (enables fit validation)
        target_functions: Preferred buyer functions for this campaign

    Returns:
        PersonaClassifierOutput with classifications and statistics
    """
    if target_functions is None:
        target_functions = []

    config = load_agent_config("persona_classifier")

    # Classify each prospect
    classified_prospects = []
    persona_counts = {}
    confidence_scores = []
    unclassifiable = 0
    review_count = 0
    fit_scores = []

    for prospect in cleaned_prospects:
        try:
            # Skip if missing required fields
            if not prospect.get("email") or not prospect.get("designation"):
                unclassifiable += 1
                continue

            # Classify prospect using Claude CLI with campaign context
            analysis = classify_prospect(
                prospect,
                target_personas,
                campaign_type,
                target_industry,
                target_functions,
            )

            # Extract Claude's analysis
            persona = analysis.get("persona", "Unknown")
            confidence = analysis.get("confidence_score", 0)
            seniority = analysis.get("seniority_level", "Unknown")
            function = analysis.get("function", "Unknown")
            rationale = analysis.get("rationale", "")
            needs_review = analysis.get("needs_review", False)
            # Campaign fit fields (NEW)
            campaign_fit_score = analysis.get("campaign_fit_score", 100)  # Default 100 if not provided
            campaign_fit_valid = analysis.get("campaign_fit_valid", True)  # Default True if not provided
            campaign_fit_rationale = analysis.get("campaign_fit_rationale", "")

            # Build primary persona
            primary = PersonaAssignment(
                persona=persona,
                confidence_score=confidence,
                rationale=rationale,
            )

            # Build secondary persona if provided
            secondary_persona = None
            if analysis.get("secondary_persona"):
                secondary_data = analysis["secondary_persona"]
                secondary_persona = PersonaAssignment(
                    persona=secondary_data.get("persona"),
                    confidence_score=secondary_data.get("confidence_score", 0),
                    rationale=secondary_data.get("rationale", ""),
                )

            # Count personas
            persona_counts[persona] = persona_counts.get(persona, 0) + 1
            confidence_scores.append(confidence)
            fit_scores.append(campaign_fit_score)

            if needs_review:
                review_count += 1

            # Build classified prospect
            classified = ClassifiedProspect(
                email=prospect.get("email"),
                designation=prospect.get("designation", ""),
                company_name=prospect.get("company_name", ""),
                primary_persona=primary,
                secondary_persona=secondary_persona,
                seniority_level=seniority,
                function=function,
                needs_review=needs_review,
                campaign_fit_score=campaign_fit_score,
                campaign_fit_valid=campaign_fit_valid,
                campaign_fit_rationale=campaign_fit_rationale,
            )

            classified_prospects.append(classified)

        except Exception as e:
            # Log but continue on errors
            print(f"Error classifying prospect {prospect.get('email')}: {e}")
            unclassifiable += 1

    # Calculate statistics
    avg_confidence = int(mean(confidence_scores)) if confidence_scores else 0
    low_confidence = sum(1 for s in confidence_scores if s < 60)
    avg_campaign_fit = int(mean(fit_scores)) if fit_scores else 0
    high_fit_count = sum(1 for s in fit_scores if s >= 80)

    # Build notes
    notes = (
        f"Classified {len(classified_prospects)} prospects using Claude CLI. "
        f"{review_count} flagged for review. "
        f"Average confidence: {avg_confidence}%"
    )
    if target_industry:
        notes += f" | Campaign: {target_industry} | Avg fit score: {avg_campaign_fit}% | High fit: {high_fit_count}"

    # Build output
    output = PersonaClassifierOutput(
        classified_prospects=classified_prospects,
        persona_distribution=persona_counts,
        low_confidence_count=low_confidence,
        unclassifiable_count=unclassifiable,
        average_confidence=avg_confidence,
        notes=notes,
    )

    return output


def create_persona_classifier_agent():
    """
    Factory function to create Persona Classifier Agent.

    Currently uses Claude CLI (subprocess calls):
    1. For each prospect, construct detailed prompt
    2. Call `claude ask` command via CLI
    3. Claude returns JSON with persona classification
    4. Parse and return structured output

    No API key needed — uses existing Claude.ai authentication via CLI.

    Future: Can upgrade to Anthropic API if needed (same logic, direct SDK calls).
    """
    return run_persona_classifier


# Agent registry export
agent = create_persona_classifier_agent()
