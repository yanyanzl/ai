"""
llm_brain.py

AI Brain
负责：
1 理解用户输入
2 选择工具
3 调用 ToolRouter
"""

from app.core.tool_router import tool_router


class LLMBrian:

    def __init__(self):

        self.router = tool_router

    def think(self, message: str):
        """
        简单意图识别
        """

        message = message.lower()

        # 文件相关
        if "桌面" in message or "desktop" in message:
            return "scan_desktop"

        if "清理" in message or "垃圾" in message:
            return "clean_temp"

        if "金融" in message or "股票" in message:
            return "task_finance_example"

        if "demo" in message:
            return "demo_task"

        return None

    def run(self, message: str):

        tool = self.think(message)

        if not tool:
            return {
                "message": "暂时无法理解你的请求"
            }

        result = self.router.execute(tool)

        return {
            "tool": tool,
            "result": result
        }


# 单例
ai_brain = LLMBrian()