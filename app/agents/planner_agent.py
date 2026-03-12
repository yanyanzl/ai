"""
Module: planner_agent_v2

Purpose:
    Intelligent task planner for Solo AI Platform (Phase-3).

Responsibilities:
    - Understand user goal
    - Break goal into executable steps
    - Validate tools and plugins
    - Produce task plan compatible with TaskGraphV2
"""

from typing import List, Dict, Any
import json5
from app.utils.logger import get_logger

logger = get_logger("planner_agent_v2")


class PlannerAgent:

    def __init__(self, brain):
        """
        Args:
            brain: LLMBrain instance
        """
        self.brain = brain

    # ------------------------------------------------
    # Build planning prompt
    # ------------------------------------------------
    def build_prompt(self, goal: str, tools: List[str], plugins: List[str]) -> str:
        prompt = f"""
你是 AI 任务规划专家。

用户目标:
{goal}

可用工具:
{tools}

可用插件:
{plugins}

任务:
将目标拆解为多个可执行步骤。

输出规则:
- JSON数组
- 每个步骤必须包含 tool, args，可选 plugin
- 不要解释，不允许文本以外的内容
- 如果无法生成任务，请返回空数组 []

示例:

[
  {{
    "tool": "search",
    "args": {{"query":"weather london"}}
  }},
  {{
    "tool": "summarize",
    "args": {{"text":"result"}},
    "plugin": "text_tools"
  }}
]
"""
        return prompt

    # ------------------------------------------------
    # Plan tasks
    # ------------------------------------------------
    def plan(self, goal: str) -> List[Dict[str, Any]]:
        tools = self.brain.router.list_tools()
        plugins = list(self.brain.plugin_manager.plugins.keys())

        prompt = self.build_prompt(goal, tools, plugins)
        logger.info(f"[PlannerAgent] Planning goal: {goal}")

        text = self.brain.call_llm(prompt)
        if not text:
            logger.warning("[PlannerAgent] LLM planning failed, returning empty list")
            return []

        # 尝试解析 LLM 输出
        try:
            raw_tasks = json5.loads(text)
        except Exception as e:
            logger.warning(f"[PlannerAgent] Failed to parse plan: {e}")
            return []

        # 标准化并过滤不可用工具/插件
        validated_tasks = []
        for t in raw_tasks:
            if not isinstance(t, dict):
                logger.warning(f"[PlannerAgent] Invalid task format: {t}")
                continue

            tool = t.get("tool")
            args = t.get("args") or {}
            plugin = t.get("plugin")

            if plugin and plugin not in plugins:
                logger.warning(f"[PlannerAgent] Plugin not available: {plugin}")
                continue

            if not plugin and tool not in tools:
                logger.warning(f"[PlannerAgent] Tool not available: {tool}")
                continue

            validated_tasks.append({
                "tool": tool,
                "args": args,
                "plugin": plugin
            })

        logger.info(f"[PlannerAgent] Generated {len(validated_tasks)} validated tasks")
        return validated_tasks