import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from agents.linkedin_copy_agent import run_linkedin_copy_agent

persona_strategies = {
    "cxo_strategy": {
        "primary_angle": "K-12 Education: Survey insights for Cxo Strategy",
        "pain_points": [
            "Teacher turnover at 20-year high, creating curriculum continuity gaps",
            "Board pressure to prove ROI on retention initiatives",
            "Professional development budgets frozen or cut further"
        ],
        "value_prop": "Research findings - addressing teacher turnover..."
    }
}

messaging_strategy = {
    "tone": "consultative",
    "key_themes": ["k-12 education", "survey", "operational efficiency"],
    "value_propositions": {"cxo_strategy": "Research findings..."},
}

result = run_linkedin_copy_agent(
    campaign_name="K-12 Teacher Retention Research",
    campaign_type="Survey",
    persona_strategies=persona_strategies,
    messaging_strategy=messaging_strategy,
    channel_guidance={"linkedin": "Peer-to-peer, thought leadership"},
    target_personas=["cxo_strategy"],
    target_region="North America",
    prospect_name="Dr. Sarah Chen",
    company_name="Lincoln County Schools",
    sender_name="Education Research Team",
)

series = result.linkedin_series["cxo_strategy"]
print("M1 Full Message:")
print(series.M1.message)
print("\n" + "="*80)
print("\nM1 Check for timeframe:")
m1_lower = series.M1.message.lower()
print(f"  '30-minute' in message: {'30-minute' in m1_lower}")
print(f"  '30 minutes' in message: {'30 minutes' in m1_lower}")
print(f"  'hour' in message: {'hour' in m1_lower}")
