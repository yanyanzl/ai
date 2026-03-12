"""
Module: task_graph_v2

Purpose:
    Execute multi-step task plans with:
    - sequential execution
    - error tolerance
    - detailed logging
    - execution metadata
"""

from typing import List, Dict, Any
import time
from app.utils.logger import get_logger

logger = get_logger("task_graph_v2")


class TaskGraph:
    """
    TaskGraph executes a sequence of tasks produced by PlannerAgent.
    """

    def __init__(self, tasks: List[Dict[str, Any]], brain):
        """
        Args:
            tasks: list of planned tasks, each with 'tool', optional 'args' and 'plugin'
            brain: reference to LLMBrain for executing tools/plugins
        """
        self.tasks = tasks
        self.brain = brain

    def execute(self) -> List[Dict[str, Any]]:
        """
        Execute all tasks sequentially.
        Returns:
            List of dicts containing:
                - step
                - tool
                - plugin (optional)
                - args
                - result or error
                - executed_at (timestamp)
                - duration (seconds)
        """
        results = []

        for idx, task in enumerate(self.tasks, start=1):
            tool_name = task.get("tool")
            args = task.get("args", {})
            plugin_name = task.get("plugin")
            start_time = time.time()

            logger.info(f"[TaskGraph] Executing step {idx}/{len(self.tasks)}: {tool_name}, plugin={plugin_name}")

            try:
                if plugin_name:
                    plugin_data = self.brain.plugin_manager.plugins.get(plugin_name, {})
                    plugin = plugin_data.get("instance")
                    if not plugin:
                        msg = f"Plugin {plugin_name} not loaded"
                        logger.warning(f"[TaskGraph] {msg}")
                        res = msg
                    else:
                        res = plugin.execute(tool_name, args)
                else:
                    if tool_name not in self.brain.router.list_tools():
                        msg = f"Tool {tool_name} not found"
                        logger.warning(f"[TaskGraph] {msg}")
                        res = msg
                    else:
                        res = self.brain.router.execute(tool_name, args)

                results.append({
                    "step": idx,
                    "tool": tool_name,
                    "plugin": plugin_name,
                    "args": args,
                    "result": res,
                    "executed_at": start_time,
                    "duration": time.time() - start_time
                })

            except Exception as e:
                logger.exception(f"[TaskGraph] Error executing task {tool_name} plugin={plugin_name}")
                results.append({
                    "step": idx,
                    "tool": tool_name,
                    "plugin": plugin_name,
                    "args": args,
                    "result": {"error": str(e)},
                    "executed_at": start_time,
                    "duration": time.time() - start_time
                })

        logger.info(f"[TaskGraph] All tasks executed, total={len(results)}")
        return results