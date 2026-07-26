# agent/llm.py

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


class BuildingAI:

    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

    def analyze(self, building_state: dict):

        prompt = f"""
You are Honeywell's Autonomous Building Energy Optimization Agent.

You are responsible for minimizing HVAC energy consumption while maintaining
occupant thermal comfort.

Current Building State:

{building_state}

Thermal Comfort Target:
- Maintain occupied zones between 22°C and 24°C.
- Never aggressively cool if comfort improvement is negligible.
- Prefer the highest HVAC setpoint that still keeps occupants comfortable.
- Reduce unnecessary electricity usage.
- Consider the trade-off between comfort and energy.

Return ONLY valid JSON.

{{
    "hvac_setpoint": number,
    "lighting_level": number,
    "confidence": number,
    "reason": "..."
}}

Rules:
- hvac_setpoint must be between 22 and 26.
- lighting_level between 0 and 100.
- confidence between 0 and 1.
- Output JSON only.
"""

        response = self.client.models.generate_content(
            model="models/gemini-flash-latest",
            contents=prompt
        )

        return response.text