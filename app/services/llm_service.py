import requests
from app.config import OLLAMA_URL, MODEL_NAME


class LLMService:

    def chat(self, messages, tools=None):

        payload = {
            "model": MODEL_NAME,
            "messages": messages,
            "stream": False
        }

        if tools:
            payload["tools"] = tools

        r = requests.post(OLLAMA_URL, json=payload)

        return r.json()