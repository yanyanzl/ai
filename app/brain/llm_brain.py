from app.core.tool_router import tool_router
from app.core.config import Config
from typing import List, Dict, Any
import requests
import re
import json5
from app.utils.logger import get_logger

logger = get_logger("llm_brain")


class LLMBrain:

    def __init__(self):

        self.router = tool_router

        self.host = Config.get("llm.host")
        self.model = Config.get("llm.model")

        self.temperature = Config.get("llm.temperature", 0)
        self.max_tokens = Config.get("llm.max_tokens", 200)
        self.max_retry = Config.get("llm.max_retry", 1)

        # 使用 Session 提高性能
        self.session = requests.Session()

    # ------------------------------------------------
    # 调用 LLM
    # ------------------------------------------------

    def call_llm(self, prompt: str) -> str:

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens
            }
        }

        try:

            response = self.session.post(
                f"{self.host}/api/generate",
                json=payload,
                timeout=120
            )

            response.raise_for_status()

            result = response.json().get("response", "")

            return result.strip()

        except Exception as e:

            logger.error(f"LLM call failed: {e}")

            return ""

    # ------------------------------------------------
    # 清理 LLM 输出
    # ------------------------------------------------

    def clean_llm_output(self, text: str) -> str:

        text = text.strip()

        # 去掉控制字符
        text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)

        # 统一引号
        text = text.replace("’", "'")
        text = text.replace("“", '"').replace("”", '"')

        # 去掉多余空格
        text = re.sub(r"\s+", " ", text)

        return text

    # ------------------------------------------------
    # AI 生成工具调用计划
    # ------------------------------------------------

    def plan(self, message: str) -> List[Dict[str, Any]]:

        available_tools = self.router.list_tools()

        prompt = f"""
你是一个 AI Butler。

任务:
根据用户指令生成工具调用计划。

可用工具:
{available_tools}

输出规则:

1 只输出 JSON
2 不允许任何解释
3 必须是 JSON 数组

格式:

[
 {{"tool":"tool_name","args":{{}}}}
]

用户指令:
{message}
"""

        logger.info(f"Planning for message: {message}")

        for attempt in range(self.max_retry + 1):

            try:

                text = self.call_llm(prompt)

                text = self.clean_llm_output(text)

                logger.debug(f"LLM raw output: {text}")

                # 提取 JSON 数组
                match = re.search(r"\[.*\]", text)

                if not match:

                    logger.warning("No JSON array found in LLM output")

                    if attempt < self.max_retry:
                        continue

                    return []

                json_text = match.group()

                tasks = json5.loads(json_text)

                # 过滤非法工具
                tasks = [
                    t for t in tasks
                    if t.get("tool") in available_tools
                ]

                logger.info(f"Plan generated: {tasks}")

                return tasks

            except Exception as e:

                logger.warning(
                    f"Plan parse failed ({attempt+1}/{self.max_retry+1}) : {e}"
                )

                if attempt >= self.max_retry:
                    return []

        return []

    # ------------------------------------------------
    # 执行工具
    # ------------------------------------------------

    def run(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

        results = []

        for task in tasks:

            tool_name = task.get("tool")
            args = task.get("args", {})

            if not tool_name:

                continue

            if tool_name not in self.router.list_tools():

                logger.warning(f"Tool not found: {tool_name}")

                results.append({
                    "tool": tool_name,
                    "result": f"工具 '{tool_name}' 不存在"
                })

                continue

            logger.info(f"Executing tool: {tool_name} args={args}")

            try:

                res = self.router.execute(tool_name, args)

            except Exception as e:

                logger.exception("Tool execution error")

                res = {"error": str(e)}

            results.append({
                "tool": tool_name,
                "result": res
            })

        return results

    # ------------------------------------------------
    # AI总结工具结果
    # ------------------------------------------------

    def summarize(self, message: str, results: List[Dict]) -> str:

        prompt = f"""
用户问题:
{message}

工具执行结果:
{results}

请总结并用自然语言回答用户。
"""

        summary = self.call_llm(prompt)

        return summary

    # ------------------------------------------------
    # 主入口
    # ------------------------------------------------

    def handle(self, message: str) -> Dict[str, Any]:

        logger.info(f"User message: {message}")

        tasks = self.plan(message)

        if not tasks:

            logger.info("No tool plan generated")

            # fallback 直接 AI 回复
            reply = self.call_llm(message)

            return {
                "message": reply
            }

        results = self.run(tasks)

        summary = self.summarize(message, results)

        return {
            "tasks": results,
            "summary": summary
        }


# 全局实例
agent_brain = LLMBrain()