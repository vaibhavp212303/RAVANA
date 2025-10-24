import json
from config.settings import PROMPTS_FILE

class PromptLoader:
    @staticmethod
    def load(version: str):
        with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            if item["version"] == version:
                return item
        raise ValueError(f"Prompt version '{version}' not found.")
