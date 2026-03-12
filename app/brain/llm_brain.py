from app.core.tool_router import tool_router
from app.core.config import Config
from app.utils.logger import get_logger
from app.core.plugin_manager import PluginManager
from app.core.context_builder import ContextBuilder
from app.core.memory_manager import MemoryManager
from app.agents.planner_agent import PlannerAgent
from app.agents.task_graph import TaskGraph

from typing import List, Dict, Any
import requests, re, json5, time, math

logger = get_logger("llm_brain")


class LLMBrain:
    """
    Phase-2 升级版 LLM Brain
    功能：
        - 支持 PlannerAgent 生成任务计划
        - TaskGraph 执行任务（插件/工具兼容）
        - LLM 输出总结（summarize）
        - Memory JSON 日志化
        - 个性化身份上下文（SOUL.md / USER.md）
        - 容错与 fallback 机制
        - 统一日志输出
    """

    def __init__(self):
        self.router = tool_router
        self.plugin_manager = PluginManager(self.router)
        self.plugin_manager.load_plugins()

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

        # 上下文 / memory / planner
        self.context_builder = ContextBuilder()
        self.memory = MemoryManager()
        self.planner = PlannerAgent(self)

    # ---------------------------
    # LLM 是否可用
    # ---------------------------
    def llm_available(self) -> bool:
        return time.time() >= self.llm_disable_until

    # ---------------------------
    # 构建 prompt（注入人格化上下文）
    # ---------------------------
    def build_prompt(self, message: str, context: List[Dict[str, str]] = None) -> str:
        """
        构建 LLM prompt，包含：
        - 对话上下文
        - 用户消息
        - SOUL.md / USER.md 个性化信息
        """
        context_text = ""
        if context:
            context_text = "\n".join([f"{m['role']}: {m['content']}" for m in context])
        try:
            identity_context = self.context_builder.build_identity_context()
        except Exception as e:
            logger.exception(f"[PROMPT] Failed to load identity context: {e}")
            identity_context = ""

        full_prompt = f"{identity_context}\n{context_text}\nuser: {message}\nassistant:"
        return full_prompt

    # ---------------------------
    # 调用 LLM（指数退避 + 容错）
    # ---------------------------
    def call_llm(self, prompt: str, context: List[Dict[str, str]] = None) -> str | None:
        if not self.llm_available():
            logger.warning("LLM disabled by circuit breaker")
            return None

        full_prompt = self.build_prompt(prompt, context)

        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {"temperature": self.temperature, "num_predict": self.max_tokens}
        }

        for attempt in range(self.max_retry + 1):
            try:
                logger.info(f"call_llm sending request to {self.host}. the message is: \n {payload}")
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

    # ---------------------------
    # 清理 LLM 输出
    # ---------------------------
    def clean_llm_output(self, text: str) -> str:
        text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
        text = text.replace("’", "'").replace("“", '"').replace("”", '"')
        return re.sub(r'\s+', ' ', text.strip())

    # ---------------------------
    # 执行任务（TaskGraph / 插件 / 工具）
    # ---------------------------
    def run(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        执行任务计划（支持插件及本地工具）
        返回每步执行结果及 meta 信息
        """
        results = []
        for idx, task in enumerate(tasks, start=1):
            tool_name = task.get("tool")
            args = task.get("args") or {}
            plugin_name = task.get("plugin")
            start_time = time.time()

            logger.info(f"[RUN] Executing task {idx}/{len(tasks)}: {tool_name}, plugin={plugin_name}")
            try:
                if plugin_name:
                    plugin_data = self.plugin_manager.plugins.get(plugin_name, {})
                    plugin = plugin_data.get("instance")
                    if not plugin:
                        msg = f"Plugin {plugin_name} not loaded"
                        logger.warning(f"[RUN] {msg}")
                        results.append({"tool": tool_name, "plugin": plugin_name, "result": msg})
                        continue
                    res = plugin.execute(tool_name, args)
                else:
                    if tool_name not in self.router.list_tools():
                        msg = f"Tool {tool_name} not found"
                        logger.warning(f"[RUN] {msg}")
                        results.append({"tool": tool_name, "result": msg})
                        continue
                    res = self.router.execute(tool_name, args)

                results.append({
                    "tool": tool_name,
                    "plugin": plugin_name,
                    "result": res,
                    "executed_at": time.time(),
                    "duration": time.time() - start_time
                })

            except Exception as e:
                logger.exception(f"[RUN] Error executing task {tool_name} plugin={plugin_name}")
                results.append({
                    "tool": tool_name,
                    "plugin": plugin_name,
                    "result": {"error": str(e)},
                    "executed_at": time.time(),
                    "duration": time.time() - start_time
                })

        logger.info(f"[RUN] All tasks executed, total={len(results)}")
        return results

    # ---------------------------
    # 汇总任务结果
    # ---------------------------
    def summarize(self, context: List[Dict[str, str]], results: List[Dict[str, Any]]) -> str:
        """
        将任务执行结果和对话上下文总结为自然语言回复
        """
        try:
            context_text = "\n".join([f"{m['role']}: {m['content']}" for m in context])
            results_text = json5.dumps(results, indent=2, ensure_ascii=False)

            prompt = f"""
参考对话:
{context_text}

任务执行结果:
{results_text}

请用自然语言总结，并向用户友好反馈：
- 核心结论
- 已执行操作
- 如有需要的下一步建议
"""
            summary = self.call_llm(prompt)
            if not summary:
                logger.warning("[SUMMARIZE] LLM returned empty summary")
                return "任务已执行，但 AI 总结不可用（LLM 离线）"

            logger.info("[SUMMARIZE] Summary generated successfully")
            return summary

        except Exception as e:
            logger.exception(f"[SUMMARIZE] Failed to summarize: {e}")
            return "任务执行完成，但 AI 总结不可用（内部错误）"

    # ---------------------------
    # 主入口
    # ---------------------------
    def handle(self, message: str, session_id: str = "default") -> Dict[str, Any]:
        """
        Main entry point for processing a user message.
        Workflow:
            1. Load session conversation
            2. Inject identity context (首次)
            3. Append user message
            4. Memory log
            5. PlannerAgent generate task plan
            6. Execute TaskGraph
            7. Summarize results
            8. Append assistant response to conversation + memory
        """
        if session_id not in self.conversations:
            self.conversations[session_id] = []

            # ===== 首次注入身份上下文 =====
            try:
                identity_context = self.context_builder.build_identity_context()
                self.conversations[session_id].append({
                    "role": "system",
                    "content": identity_context
                })
                logger.info(f"[HANDLE] Loaded identity context for session {session_id}")
            except Exception as e:
                logger.exception(f"[HANDLE] Failed to load identity context: {e}")

        # ===== Append user message =====
        self.conversations[session_id].append({"role": "user", "content": message})
        logger.info(f"[HANDLE] Received user message: {message}")

        # ===== Memory log =====
        try:
            self.memory.append_daily_log({"role": "user", "content": message})
        except Exception:
            logger.exception("[HANDLE] Memory logging failed for user message")

        # ===== PlannerAgent: generate task plan =====
        try:
            tasks = self.planner.plan(message)
            logger.info(f"[HANDLE] Planner generated {len(tasks)} tasks")
        except Exception as e:
            logger.exception(f"[HANDLE] PlannerAgent failed: {e}")
            tasks = []

        # ===== 如果没有任务，fallback 到直接 LLM 回复 =====
        if not tasks:
            try:
                reply = self.call_llm(message, context=self.conversations[session_id]) or \
                        "AI 当前不可用，请稍后再试。"
            except Exception as e:
                logger.exception(f"[HANDLE] Fallback LLM call failed: {e}")
                reply = "AI 当前不可用，请稍后再试。"

            self.conversations[session_id].append({"role": "assistant", "content": reply})
            try:
                self.memory.append_daily_log({"role": "assistant", "content": reply})
            except Exception:
                logger.exception("[HANDLE] Memory logging failed for assistant fallback")

            return {"message": reply}

        # ===== Execute TaskGraph =====
        try:
            graph = TaskGraph(tasks, self)
            results = graph.execute()
            logger.info(f"[HANDLE] TaskGraph executed {len(results)} steps")
        except Exception as e:
            logger.exception(f"[HANDLE] TaskGraph execution failed: {e}")
            results = self.run(tasks)  # fallback to run()

        # ===== Summarize results =====
        try:
            summary = self.summarize(self.conversations[session_id], results)
        except Exception as e:
            logger.exception(f"[HANDLE] Summarization failed: {e}")
            summary = "任务执行完成，但 AI 总结不可用"

        # ===== Append assistant response =====
        self.conversations[session_id].append({"role": "assistant", "content": summary})
        try:
            self.memory.append_daily_log({"role": "assistant", "content": summary})
        except Exception:
            logger.exception("[HANDLE] Memory logging failed for assistant summary")

        return {"tasks": results, "summary": summary}


# 初始化全局 agent
agent_brain = LLMBrain()