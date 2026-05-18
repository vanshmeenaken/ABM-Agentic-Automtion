"""
Orchestrator for Ken ABM Platform.

Chains all agents in sequence:
1. Campaign Planner Agent
2. Message Strategy Agent
3. Persona Classifier Agent (per prospect)
4. Email Copy Agent (per prospect)
5. WhatsApp Copy Agent (per prospect, with branching logic)

This is a framework-level orchestrator. Agent implementations are plugged in via:
- orchestrator.register_agent() to add agent executors
- orchestrator.run() to execute the full pipeline

Ready for Anthropic SDK integration: just implement the agent executors.
"""

from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
from agents.schemas import OrchestrationInput, OrchestrationOutput


class Orchestrator:
    """
    Main orchestration engine that chains all agents.

    Supports:
    - Sequential agent execution
    - Branching logic (e.g., skip WhatsApp if no phone)
    - Error handling and fallback routing
    - Execution summary and reporting
    """

    def __init__(self):
        """Initialize orchestrator with empty agent registry."""
        self.agents = {}  # agent_name -> executor function
        self.execution_log = []
        self.config = {
            "skip_whatsapp_if_no_phone": True,
            "fallback_channels": ["email", "linkedin"],  # If WhatsApp fails
            "parallel_prospect_processing": False,  # Set to True for production
        }

    def register_agent(self, agent_name: str, executor: Callable) -> None:
        """
        Register an agent executor.

        Args:
            agent_name: Name of agent (campaign_planner, message_strategy, etc.)
            executor: Callable that takes input and returns output
        """
        self.agents[agent_name] = executor
        self._log(f"Agent registered: {agent_name}")

    def _log(self, message: str, level: str = "info") -> None:
        """Log execution event."""
        timestamp = datetime.now().isoformat()
        self.execution_log.append({
            "timestamp": timestamp,
            "level": level,
            "message": message,
        })

    def run(self, input_data: OrchestrationInput) -> OrchestrationOutput:
        """
        Run full orchestration pipeline.

        Flow:
        1. Campaign Planner Agent → campaign plan
        2. Message Strategy Agent → messaging strategy
        3. For each prospect:
           a. Persona Classifier Agent → persona assignment
           b. Email Copy Agent → email variations
           c. WhatsApp Copy Agent (with branching) → whatsapp variations
        4. Aggregate results into OrchestrationOutput

        Args:
            input_data: OrchestrationInput with campaign and prospect info

        Returns:
            OrchestrationOutput with all generated content
        """
        self._log(f"Starting orchestration for campaign: {input_data.campaign_name}")

        try:
            # Step 1: Campaign Planner Agent
            campaign_plan = self._run_campaign_planner(input_data)
            if not campaign_plan:
                raise RuntimeError("Campaign Planner Agent failed")

            # Step 2: Message Strategy Agent
            message_strategy = self._run_message_strategy(
                campaign_plan, input_data
            )
            if not message_strategy:
                raise RuntimeError("Message Strategy Agent failed")

            # Step 3: Process each prospect
            prospect_messaging = self._process_prospects(
                input_data.prospects,
                campaign_plan,
                message_strategy,
            )

            # Step 4: Generate execution summary
            execution_summary = self._generate_summary(
                campaign_plan,
                message_strategy,
                prospect_messaging,
            )

            # Build output
            output = OrchestrationOutput(
                campaign_plan=campaign_plan,
                message_strategy=message_strategy,
                prospect_messaging=prospect_messaging,
                execution_summary=execution_summary,
                notes=f"Orchestration completed at {datetime.now().isoformat()}",
            )

            self._log("Orchestration completed successfully", "info")
            return output

        except Exception as e:
            self._log(f"Orchestration failed: {str(e)}", "error")
            raise

    def _run_campaign_planner(self, input_data: OrchestrationInput) -> Optional[Dict]:
        """
        Run Campaign Planner Agent.

        Input: campaign name, industry, region, offer, type
        Output: campaign plan with ICP, personas, channels

        Currently a stub. Implement by:
        1. Call agent executor: self.agents["campaign_planner"](input)
        2. Return structured output
        """
        self._log("Running Campaign Planner Agent...")

        if "campaign_planner" not in self.agents:
            self._log("Campaign Planner Agent not registered (stub mode)", "warning")
            # Return stub output for testing
            return {
                "campaign_draft": {
                    "name": input_data.campaign_name,
                    "campaign_type": input_data.campaign_type,
                    "target_industry": input_data.target_industry,
                    "target_region": input_data.target_region,
                    "offer": input_data.offer,
                },
                "icp_definition": {
                    "positive": {
                        "industries": [input_data.target_industry],
                        "regions": [input_data.target_region],
                        "seniority_levels": ["C-level", "Director", "Manager"],
                    },
                    "negative": {
                        "excluded_industries": [],
                    },
                },
                "persona_map": [
                    {"persona": "CXO", "persona_type": "primary", "rationale": "Decision maker"},
                    {"persona": "Operations", "persona_type": "secondary", "rationale": "Implementation"},
                ],
                "channel_plan": {
                    "channels": input_data.preferred_channels or ["email", "linkedin"],
                    "sequence_timing": {"M1": 0, "M2": 3, "M3": 7, "M4": 12},
                },
                "confidence_notes": "Stub mode - replace with real agent output",
            }

        try:
            result = self.agents["campaign_planner"](input_data.model_dump())
            self._log("Campaign Planner Agent completed successfully")
            return result
        except Exception as e:
            self._log(f"Campaign Planner Agent failed: {str(e)}", "error")
            return None

    def _run_message_strategy(
        self, campaign_plan: Dict, input_data: OrchestrationInput
    ) -> Optional[Dict]:
        """
        Run Message Strategy Agent.

        Input: campaign plan, personas, industry
        Output: messaging strategy with tone, themes, value props

        Currently a stub. Implement by:
        1. Extract personas from campaign_plan
        2. Call agent executor: self.agents["message_strategy"](input)
        3. Return structured output
        """
        self._log("Running Message Strategy Agent...")

        if "message_strategy" not in self.agents:
            self._log("Message Strategy Agent not registered (stub mode)", "warning")
            # Return stub output for testing
            personas = [p["persona"] for p in campaign_plan.get("persona_map", [])]
            return {
                "messaging_strategy": {
                    "tone": "professional",
                    "key_themes": ["innovation", "industry leadership"],
                    "value_propositions": {p: f"Tailored solution for {p}" for p in personas},
                    "call_to_action": "Schedule a 15-minute discovery call",
                },
                "persona_specific_messages": {p: f"Personalized message for {p}" for p in personas},
                "success_criteria": ["20% open rate", "5% click rate"],
                "notes": "Stub mode - replace with real agent output",
            }

        try:
            strategy_input = {
                "campaign_name": input_data.campaign_name,
                "campaign_type": input_data.campaign_type,
                "offer": input_data.offer,
                "target_personas": [p["persona"] for p in campaign_plan.get("persona_map", [])],
                "target_industry": input_data.target_industry,
                "channel_mix": campaign_plan.get("channel_plan", {}).get("channels", []),
            }
            result = self.agents["message_strategy"](strategy_input)
            self._log("Message Strategy Agent completed successfully")
            return result
        except Exception as e:
            self._log(f"Message Strategy Agent failed: {str(e)}", "error")
            return None

    def _process_prospects(
        self,
        prospects: List[Dict],
        campaign_plan: Dict,
        message_strategy: Dict,
    ) -> List[Dict]:
        """
        Process each prospect through persona classification and copy generation.

        For each prospect:
        1. Run Persona Classifier Agent → assign to persona
        2. Run Email Copy Agent → generate email variations
        3. Run WhatsApp Copy Agent (with branching) → generate WhatsApp (if phone exists)

        Returns list of prospects with all generated content.
        """
        self._log(f"Processing {len(prospects)} prospects...")

        prospect_messaging = []

        for i, prospect in enumerate(prospects):
            self._log(f"Processing prospect {i+1}/{len(prospects)}: {prospect.get('email', 'unknown')}")

            prospect_data = self._process_single_prospect(
                prospect,
                campaign_plan,
                message_strategy,
            )

            if prospect_data:
                prospect_messaging.append(prospect_data)

        self._log(f"Completed processing {len(prospect_messaging)} prospects")
        return prospect_messaging

    def _process_single_prospect(
        self,
        prospect: Dict,
        campaign_plan: Dict,
        message_strategy: Dict,
    ) -> Optional[Dict]:
        """
        Process a single prospect through the pipeline.

        Returns: Prospect with persona assignment + email + whatsapp copy (if applicable)
        """
        try:
            # Get target personas from campaign plan
            personas = [p["persona"] for p in campaign_plan.get("persona_map", [])]

            # Step 1: Persona Classifier
            persona_assignment = self._run_persona_classifier(
                prospect, personas, campaign_plan
            )
            if not persona_assignment:
                self._log(
                    f"Skipping prospect {prospect.get('email')} - persona classification failed",
                    "warning",
                )
                return None

            # Step 2: Email Copy
            email_copy = self._run_email_copy(
                prospect, persona_assignment, message_strategy, campaign_plan
            )

            # Step 3: WhatsApp Copy (with branching logic)
            whatsapp_copy = None
            whatsapp_channel = campaign_plan.get("channel_plan", {}).get("channels", [])

            has_phone = bool(prospect.get("phone") or prospect.get("phone_number"))
            should_generate_whatsapp = "whatsapp" in whatsapp_channel and has_phone

            if should_generate_whatsapp:
                whatsapp_copy = self._run_whatsapp_copy(
                    prospect, persona_assignment, message_strategy, campaign_plan
                )

                # Branching logic: if WhatsApp generation fails, note it but don't fail
                if not whatsapp_copy and self.config["skip_whatsapp_if_no_phone"]:
                    self._log(
                        f"WhatsApp copy failed for {prospect.get('email')} - falling back to {self.config['fallback_channels']}",
                        "warning",
                    )

            return {
                "email": prospect.get("email"),
                "first_name": prospect.get("first_name", ""),
                "last_name": prospect.get("last_name", ""),
                "company_name": prospect.get("company_name", ""),
                "designation": prospect.get("designation", ""),
                "phone": prospect.get("phone", ""),
                "persona_assignment": persona_assignment,
                "email_copy": email_copy,
                "whatsapp_copy": whatsapp_copy,
                "channels_used": [
                    "email",
                    "whatsapp" if whatsapp_copy else None,
                    "linkedin",
                ],
            }

        except Exception as e:
            self._log(f"Error processing prospect: {str(e)}", "error")
            return None

    def _run_persona_classifier(
        self,
        prospect: Dict,
        target_personas: List[str],
        campaign_plan: Dict,
    ) -> Optional[Dict]:
        """
        Run Persona Classifier Agent.

        Input: prospect info, target personas, campaign type
        Output: primary persona + confidence, secondary persona (optional)

        Currently a stub. Implement by:
        1. Call agent executor: self.agents["persona_classifier"](input)
        2. Return structured output
        """
        if "persona_classifier" not in self.agents:
            # Stub: assign first persona
            return {
                "persona": target_personas[0] if target_personas else "Unknown",
                "confidence_score": 75,
                "rationale": "Stub assignment based on designation",
                "secondary_persona": target_personas[1] if len(target_personas) > 1 else None,
            }

        try:
            classifier_input = {
                "prospect": prospect,
                "target_personas": target_personas,
                "campaign_type": campaign_plan.get("campaign_draft", {}).get("campaign_type"),
            }
            result = self.agents["persona_classifier"](classifier_input)
            return result
        except Exception as e:
            self._log(f"Persona Classifier failed for {prospect.get('email')}: {str(e)}", "error")
            return None

    def _run_email_copy(
        self,
        prospect: Dict,
        persona_assignment: Dict,
        message_strategy: Dict,
        campaign_plan: Dict,
    ) -> Optional[Dict]:
        """
        Run Email Copy Agent.

        Input: prospect, persona, message strategy
        Output: primary email + alternatives with subject, body, CTA

        Currently a stub. Implement by:
        1. Call agent executor: self.agents["email_copy"](input)
        2. Return structured output
        """
        if "email_copy" not in self.agents:
            # Stub: generate basic email
            persona = persona_assignment.get("persona", "Decision Maker")
            return {
                "primary_email": {
                    "subject": f"Opportunity for {prospect.get('company_name', 'your company')}",
                    "preview_text": "A tailored solution for your team",
                    "body": f"Hi {prospect.get('first_name', 'there')},\n\nWe have an opportunity...",
                    "cta_text": "Schedule a call",
                    "personalization_vars": {
                        "first_name": prospect.get("first_name", ""),
                        "company_name": prospect.get("company_name", ""),
                    },
                },
                "alternative_variations": [],
                "notes": "Stub email - replace with real agent output",
            }

        try:
            email_input = {
                "persona": persona_assignment.get("persona"),
                "company_name": prospect.get("company_name"),
                "designation": prospect.get("designation"),
                "message_strategy": message_strategy,
                "campaign_offer": campaign_plan.get("campaign_draft", {}).get("offer"),
                "tone": message_strategy.get("messaging_strategy", {}).get("tone", "professional"),
            }
            result = self.agents["email_copy"](email_input)
            return result
        except Exception as e:
            self._log(f"Email Copy Agent failed for {prospect.get('email')}: {str(e)}", "error")
            return None

    def _run_whatsapp_copy(
        self,
        prospect: Dict,
        persona_assignment: Dict,
        message_strategy: Dict,
        campaign_plan: Dict,
    ) -> Optional[Dict]:
        """
        Run WhatsApp Copy Agent.

        Input: prospect, persona, message strategy
        Output: primary WhatsApp message + alternatives (shorter, conversational)

        Currently a stub. Implement by:
        1. Call agent executor: self.agents["whatsapp_copy"](input)
        2. Return structured output
        """
        if "whatsapp_copy" not in self.agents:
            # Stub: generate basic WhatsApp
            return {
                "primary_message": {
                    "message": "Hi! Quick opportunity for your team...",
                    "follow_up_messages": ["Just checking in!", "Would love to chat"],
                    "personalization_vars": {
                        "first_name": prospect.get("first_name", ""),
                    },
                },
                "alternative_variations": [],
                "notes": "Stub WhatsApp - replace with real agent output",
            }

        try:
            whatsapp_input = {
                "persona": persona_assignment.get("persona"),
                "first_name": prospect.get("first_name", ""),
                "company_name": prospect.get("company_name"),
                "designation": prospect.get("designation"),
                "message_strategy": message_strategy,
                "campaign_offer": campaign_plan.get("campaign_draft", {}).get("offer"),
                "tone": "conversational",
            }
            result = self.agents["whatsapp_copy"](whatsapp_input)
            return result
        except Exception as e:
            self._log(f"WhatsApp Copy Agent failed for {prospect.get('email')}: {str(e)}", "error")
            return None

    def _generate_summary(
        self,
        campaign_plan: Dict,
        message_strategy: Dict,
        prospect_messaging: List[Dict],
    ) -> Dict:
        """
        Generate execution summary.

        Shows: what was generated, what was skipped, any failures.
        """
        whatsapp_count = sum(1 for p in prospect_messaging if p.get("whatsapp_copy"))
        email_count = sum(1 for p in prospect_messaging if p.get("email_copy"))

        return {
            "total_prospects_processed": len(prospect_messaging),
            "email_copies_generated": email_count,
            "whatsapp_copies_generated": whatsapp_count,
            "whatsapp_skipped_count": len(prospect_messaging) - whatsapp_count,
            "personas_assigned": list(set(
                p["persona_assignment"]["persona"] for p in prospect_messaging
            )),
            "execution_log": self.execution_log,
        }


# Global orchestrator instance
_orchestrator_instance = None


def get_orchestrator() -> Orchestrator:
    """Get or create global orchestrator instance."""
    global _orchestrator_instance
    if _orchestrator_instance is None:
        _orchestrator_instance = Orchestrator()
    return _orchestrator_instance


def run_orchestration(input_data: OrchestrationInput) -> OrchestrationOutput:
    """
    Convenience function to run full orchestration.

    Example:
        from agents.orchestrator import run_orchestration
        from agents.schemas import OrchestrationInput

        input_data = OrchestrationInput(
            campaign_name="Tech Market Research",
            target_industry="Technology",
            target_region="North America",
            offer="Market research data",
            campaign_type="Market Research",
            prospects=[...]
        )

        output = run_orchestration(input_data)
    """
    orchestrator = get_orchestrator()
    return orchestrator.run(input_data)
