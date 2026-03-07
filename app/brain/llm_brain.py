# brain/llm_brain.py
from app.core.tool_router import tool_router
from typing import Dict, Any
import openai  # 可替换成本地 LLM

class LLMBrian:
    def __init__(self):
        self.router = tool_router

    def plan(self, message: str) -> Dict[str, Any]:
        """
        调用 LLM 生成工具调用计划
        返回示例：
        [
            {"tool": "scan_desktop", "args": {}},
            {"tool": "clean_temp", "args": {}}
        ]
        """
        # TODO: 替换为本地 LLM 调用
        # 简单演示：
        tasks = []
        msg = message.lower()
        if "桌面" in msg:
            tasks.append({"tool": "scan_desktop", "args": {}})
        if "清理" in msg:
            tasks.append({"tool": "clean_temp", "args": {}})
        if "demo" in msg:
            tasks.append({"tool": "demo_task", "args": {}})
        return tasks

    def run(self, message: str):
        tasks = self.plan(message)
        results = []
        for task in tasks:
            res = self.router.execute(task["tool"], task.get("args", {}))
            results.append({"tool": task["tool"], "result": res})
        if not results:
            return {"message": f"AI 暂时无法理解你的请求. 当前可用的工具列表为:{tool_router.list_tools()}"}
        return {"tasks": results}

# 单例
ai_brain = LLMBrian()