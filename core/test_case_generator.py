import json
from concurrent.futures import ThreadPoolExecutor
from core.model_client import ModelClient
from core.prompt_loader import PromptLoader
from config.settings import USE_STREAM


class TestCaseGenerator:
    def __init__(self):
        self.model_client = ModelClient()

    def generate_parallel(self, requirement, version, num_cases=2):
        prompt_data = PromptLoader.load(version)
        requirement_str = json.dumps(requirement, indent=2)

        def _generate(idx):
            template = prompt_data["template"].replace("{requirement}", requirement_str)
            template += f"\n\n⚡ Generate unique variation #{idx+1}."
            payload = {"model": self.model_client.model_name, "prompt": template, "stream": USE_STREAM}
            return self.model_client.call_streaming(payload) if USE_STREAM else self.model_client.call_once(payload)

        with ThreadPoolExecutor(max_workers=min(num_cases, 4)) as ex:
            return list(ex.map(_generate, range(num_cases)))

    def generate_batch(self, requirement, version):
        prompt_data = PromptLoader.load(version)
        requirement_str = json.dumps(requirement, indent=2)
        template = prompt_data["template"].replace("{requirement}", requirement_str)
        template += "\n\n⚡ Generate test cases in JSON array format."

        payload = {
            "model": self.model_client.model_name,
            "prompt": template,
            "format": "json",
            "stream": USE_STREAM
        }
        return self.model_client.call_streaming(payload) if USE_STREAM else self.model_client.call_once(payload)
