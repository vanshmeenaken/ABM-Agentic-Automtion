import subprocess
import json

claude_path = r'C:\Users\Vansh\AppData\Roaming\npm\claude.cmd'

campaign_name = "K-12 Teacher Retention Research"
campaign_type = "Survey"
target_industry = "K-12 Education"
offer = "Research findings on cost-effective teacher retention strategies"
target_personas = ["cxo_strategy", "operations"]
channel_mix = ["email", "linkedin", "whatsapp"]

prompt = f"""Generate messaging strategy for {campaign_name}.
Return ONLY valid JSON (no text, no explanations).

Campaign: {campaign_name} | Type: {campaign_type} | Industry: {target_industry}
Offer: {offer}
Personas: {', '.join(target_personas)}
Channels: {', '.join(channel_mix)}

For EACH persona, identify 3 SPECIFIC pain points in {target_industry} that {campaign_type} addresses.
Create messaging angles, value props, and tone appropriate for {campaign_type}.

JSON (replace ALL placeholders):
{{
    "messaging_tone": "professional",
    "key_themes": ["theme1", "theme2"],
    "call_to_action": "CTA for {campaign_type}",
    "success_criteria": {{"email_open_rate": "25-30%", "response_rate": "3-5%"}},
    "persona_strategies": {{
        {', '.join(f'"{p}": {{"primary_angle": "angle", "pain_points": ["pain1", "pain2", "pain3"], "value_prop": "value"}}' for p in target_personas)}
    }},
    "channel_guidance": {{{', '.join(f'"{ch}": "guidance"' for ch in channel_mix)}}},
    "market_context_rationale": "reason"
}}"""

print("Prompt length:", len(prompt))
print("\nCalling Claude CLI with Haiku...")

result = subprocess.run(
    [claude_path, "-p", prompt, "--model", "haiku"],
    capture_output=True,
    text=True,
    timeout=180
)

print(f"Return code: {result.returncode}")
print(f"Stdout length: {len(result.stdout)}")
print(f"\nStdout (first 1000 chars):\n{result.stdout[:1000]}")
print(f"\nStderr:\n{result.stderr[:500]}")

# Try to parse JSON
try:
    parsed = json.loads(result.stdout)
    print(f"\nJSON parsed successfully!")
    print(f"Keys: {list(parsed.keys())}")
except Exception as e:
    print(f"\nJSON parse error: {e}")
