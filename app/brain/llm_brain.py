from app.core.tool_router import tool_router
from app.config import Config
from typing import List, Dict, Any
import requests, json

class LLMBrian:
    def __init__(self):
        self.router = tool_router
        self.host = Config.get("llm.host")
        self.model = Config.get("llm.model")
        self.temperature = Config.get("llm.temperature", 0)
        self.max_tokens = Config.get("llm.max_tokens", 200)

    def plan(self, message: str) -> List[Dict[str, Any]]:
        try:
            prompt = f"""
            你是一个 AI Butler。根据用户指令生成工具调用列表。
            可用工具: {self.router.list_tools()}
            输出 JSON 数组，每个对象包含:
            - tool: 工具名称
            - args: 字典参数

            用户指令: "{message}"
            """

            payload = {
                "model": self.model,
                "prompt": prompt,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }
            response = requests.post(f"{self.host}/v1/completions", json=payload, timeout=10)
            response.raise_for_status()
            text = response.json()["completion"]

            # 尝试解析 JSON
            start = text.find("[")
            end = text.rfind("]") + 1
            tasks = json.loads(text[start:end])
            return tasks
        except Exception as e:
            print("[LLM ERROR]", e)
            return []

    def run(self, message: str):
        tasks = self.plan(message)
        results = []
        for task in tasks:
            tool_name = task.get("tool")
            args = task.get("args", {})
            if not tool_name:
                continue
            res = self.router.execute(tool_name, args)
            results.append({"tool": tool_name, "result": res})
        if not results:
            return {"message": "AI 暂时无法理解你的请求"}
        return {"tasks": results}

ai_brain = LLMBrian()