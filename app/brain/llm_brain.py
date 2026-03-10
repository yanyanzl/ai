from app.core.tool_router import tool_router
from app.core.config import Config
from app.utils.logger import get_logger
from app.core.plugin_manager import PluginManager
from typing import List, Dict, Any
import requests, re, json5, time, math

logger = get_logger("llm_brain")


class LLMBrainV3:

    def __init__(self):

        self.router = tool_router
        self.plugin_manager = PluginManager(self.router)
        self.plugin_manager.load_plugins()  # 加载所有插件

        self.host = Config.get("llm.host")
        self.model = Config.get("llm.model")
        self.temperature = Config.get("llm.temperature", 0)
        self.max_tokens = Config.get("llm.max_tokens", 200)
        self.max_retry = Config.get("llm.max_retry", 2)
        self.session = requests.Session()
        self.timeout = (10, 60)
        self.conversations: Dict[str, List[Dict[str, str]]] = {}

        # -------- LLM Circuit Breaker --------
        self.llm_fail_count = 0
        self.llm_fail_threshold = 5
        self.llm_disable_until = 0

    # ------------------------------------------------
    # LLM 是否可用
    # ------------------------------------------------
    def llm_available(self) -> bool:
        return time.time() >= self.llm_disable_until

    # ------------------------------------------------
    # 调用 LLM（指数退避 + 容错）
    # ------------------------------------------------
    def call_llm(self, prompt: str, context: List[Dict[str, str]] = None) -> str | None:
        if not self.llm_available():
            logger.warning("LLM disabled by circuit breaker")
            return None

        full_prompt = ""
        if context:
            for msg in context:
                full_prompt += f"{msg['role']}: {msg['content']}\n"
        full_prompt += f"user: {prompt}\nassistant:"

        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {"temperature": self.temperature, "num_predict": self.max_tokens}
        }

        for attempt in range(self.max_retry + 1):
            try:
                resp = self.session.post(
                    f"{self.host}/api/generate",
                    json=payload,
                    timeout=self.timeout
                )
                resp.raise_for_status()
                text = resp.json().get("response", "")
                self.llm_fail_count = 0
                return self.clean_llm_output(text)
            except Exception as e:
                wait = math.pow(2, attempt)
                logger.warning(
                    f"LLM request failed ({attempt+1}/{self.max_retry+1}), retry in {wait}s: {e}"
                )
                time.sleep(wait)

        self.llm_fail_count += 1
        logger.error("LLM call failed after retries")
        if self.llm_fail_count >= self.llm_fail_threshold:
            self.llm_disable_until = time.time() + 120
            logger.error("LLM disabled for 120 seconds")
        return None

    # ------------------------------------------------
    # 清理输出
    # ------------------------------------------------
    def clean_llm_output(self, text: str) -> str:
        # 去掉不可见控制字符
        text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
        # 替换中文引号为英文引号
        text = text.replace("’", "'").replace("“", '"').replace("”", '"')
        # 多空格合并为一个空格，并去掉首尾空格
        return re.sub(r'\s+', ' ', text.strip())

    # ------------------------------------------------
    # 生成工具计划（支持插件）
    # ------------------------------------------------
    def plan(self, message: str, context: List[Dict[str, str]] = None) -> List[Dict[str, Any]]:
        available_tools = self.router.list_tools()
        available_plugins = self.plugin_manager.list_plugins()
        full_context = context or []
        context_text = "\n".join([f"{m['role']}: {m['content']}" for m in full_context])

        prompt = f"""
你是 AI Butler。
参考对话上下文:
{context_text}
用户请求:
{message}
可用工具:
{available_tools}
可用插件:
{available_plugins}
任务:
生成工具调用计划。
输出规则:
- JSON 数组
- 每个对象包含 tool, args, 可选 plugin
- 不允许解释
"""
        logger.info(f"Planning for message: {message}")

        text = self.call_llm(prompt)
        if not text:
            logger.warning("LLM planning failed, fallback empty tasks")
            return []

        try:
            raw_tasks = json5.loads(text)
        except Exception as e:
            logger.warning(f"Plan parse failed: {e}")
            return []

        fixed_tasks = []
        for t in raw_tasks:
            # 支持 ["tool", {}] 或 {"tool":..., "args":..., "plugin":...}
            if isinstance(t, dict) and "tool" in t:
                fixed_tasks.append(t)
            elif isinstance(t, list) and len(t) >= 1:
                fixed_tasks.append({
                    "tool": t[0],
                    "args": t[1] if len(t) > 1 and isinstance(t[1], dict) else {}
                })
            else:
                logger.warning(f"[PLAN] invalid task: {t}")

        # 过滤不可用工具 / 插件
        tasks = []
        for t in fixed_tasks:
            tool_name = t.get("tool")
            plugin_name = t.get("plugin")
            if plugin_name and plugin_name not in available_plugins:
                logger.warning(f"[PLAN] plugin not available: {plugin_name}")
                continue
            if not plugin_name and tool_name not in available_tools:
                logger.warning(f"[PLAN] tool not available: {tool_name}")
                continue
            tasks.append(t)

        logger.info(f"Plan generated: {tasks}")
        return tasks

    # ------------------------------------------------
    # 执行工具（支持插件）
    # ------------------------------------------------
    def run(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for task in tasks:
            tool_name = task.get("tool")
            args = task.get("args") or {}
            plugin_name = task.get("plugin")

            if plugin_name:
                plugin = self.plugin_manager.plugins.get(plugin_name, {}).get("instance")
                if not plugin:
                    results.append({"tool": tool_name, "plugin": plugin_name,
                                    "result": f"Plugin {plugin_name} not loaded"})
                    continue
                try:
                    res = plugin.execute(tool_name, args)
                except Exception as e:
                    logger.exception(f"[RUN] plugin tool error: {tool_name} ({plugin_name})")
                    res = {"error": str(e)}
                results.append({"tool": tool_name, "plugin": plugin_name, "result": res})
            else:
                if tool_name not in self.router.list_tools():
                    results.append({"tool": tool_name, "result": f"Tool {tool_name} not found"})
                    continue
                try:
                    res = self.router.execute(tool_name, args)
                except Exception as e:
                    logger.exception(f"[RUN] tool error: {tool_name}")
                    res = {"error": str(e)}
                results.append({"tool": tool_name, "result": res})
        return results

    # ------------------------------------------------
    # 汇总
    # ------------------------------------------------
    def summarize(self, context: List[Dict[str, str]], results: List[Dict[str, Any]]) -> str:
        context_text = "\n".join([f"{m['role']}: {m['content']}" for m in context])
        prompt = f"""
参考对话:
{context_text}
工具执行结果:
{results}
请总结并自然语言回答用户。
"""
        summary = self.call_llm(prompt)
        if not summary:
            return "任务已执行，但 AI 总结不可用（LLM 离线）"
        return summary

    # ------------------------------------------------
    # 主入口
    # ------------------------------------------------
    def handle(self, message: str, session_id: str = "default") -> Dict[str, Any]:
        if session_id not in self.conversations:
            self.conversations[session_id] = []

        self.conversations[session_id].append({"role": "user", "content": message})

        tasks = self.plan(message, context=self.conversations[session_id])
        if not tasks:
            reply = self.call_llm(message, context=self.conversations[session_id]) or \
                    "AI 当前不可用，请稍后再试。"
            self.conversations[session_id].append({"role": "assistant", "content": reply})
            return {"message": reply}

        results = self.run(tasks)
        summary = self.summarize(self.conversations[session_id], results)
        self.conversations[session_id].append({"role": "assistant", "content": summary})

        return {"tasks": results, "summary": summary}


agent_brain = LLMBrainV3()