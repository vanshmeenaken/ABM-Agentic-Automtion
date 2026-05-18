import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from agents.linkedin_copy_agent import generate_linkedin_series

result = generate_linkedin_series(
    campaign_name="Test Campaign",
    campaign_type="Market Research",
    persona="cxo_strategy",
    primary_angle="Test angle",
    pain_points=["Pain 1", "Pain 2"],
    value_prop="Value prop",
    tone="professional",
    channel_guidance="LinkedIn guidance",
)

print("Result keys:", result.keys())
print("M1 key exists:", "M1" in result)
print("Full result:")
import json
print(json.dumps(result, indent=2))
