import json
import requests
from config.settings import MODEL_API_URL, MODEL_NAME


class ModelClient:
    def __init__(self, model_name=MODEL_NAME, api_url=MODEL_API_URL):
        self.model_name = model_name
        self.api_url = api_url

    def call_streaming(self, payload):
        response_text = ""
        with requests.post(self.api_url, json=payload, stream=True, timeout=600) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if not line:
                    continue
                try:
                    data = json.loads(line.decode("utf-8"))
                    chunk = data.get("response", "")
                    if chunk:
                        print(chunk, end="", flush=True)
                        response_text += chunk
                except json.JSONDecodeError:
                    continue
        print("\n")
        return response_text

    def call_once(self, payload):
        response = requests.post(self.api_url, json=payload, timeout=600)
        response.raise_for_status()
        return response.json().get("response", "").strip()
