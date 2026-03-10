from app.core.tool_router import tool_router
from app.core.config import Config
from typing import List, Dict, Any
import requests, re, json5, time
from app.utils.logger import get_logger

logger = get_logger("llm_brain")


class LLMBrain:

    def __init__(self):

        self.router = tool_router

        self.host = Config.get("llm.host")
        self.model = Config.get("llm.model")

        self.temperature = Config.get("llm.temperature", 0)
        self.max_tokens = Config.get("llm.max_tokens", 200)

        self.max_retry = Config.get("llm.max_retry", 2)

        # HTTP Session
        self.session = requests.Session()

        # timeout (connect, read)
        self.timeout = (10, 60)

        # session_id -> history
        self.conversations: Dict[str, List[Dict[str, str]]] = {}

        # -------- LLM Circuit Breaker --------
        self.llm_fail_count = 0
        self.llm_fail_threshold = 5
        self.llm_disable_until = 0

    # ------------------------------------------------
    # LLM 是否可用
    # ------------------------------------------------
    def llm_available(self) -> bool:

        if time.time() < self.llm_disable_until:
            return False

        return True

    # ------------------------------------------------
    # 调用 LLM（增强容错版）
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
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens
            }
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

                logger.warning(
                    f"LLM request failed ({attempt+1}/{self.max_retry+1}): {e}"
                )

                time.sleep(1)

        # 所有 retry 失败
        self.llm_fail_count += 1

        logger.error("LLM call failed after retries")

        # circuit breaker
        if self.llm_fail_count >= self.llm_fail_threshold:
            self.llm_disable_until = time.time() + 120
            logger.error("LLM disabled for 120 seconds")

        return None

    # ------------------------------------------------
    # 清理 LLM 输出
    # ------------------------------------------------
    def clean_llm_output(self, text: str) -> str:

        text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)

        text = text.replace("’", "'") \
            .replace("“", '"') \
            .replace("”", '"')

        return re.sub(r'\s+', ' ', text.strip())

    # ------------------------------------------------
    # 生成工具计划
    # ------------------------------------------------
    def plan(self, message: str, context: List[Dict[str, str]] = None) -> List[Dict[str, Any]]:

        available_tools = self.router.list_tools()

        full_context = context or []

        context_text = "\n".join(
            [f"{m['role']}: {m['content']}" for m in full_context]
        )

        prompt = f"""
你是 AI Butler。

参考对话上下文:
{context_text}

用户请求:
{message}

可用工具:
{available_tools}

任务:
生成工具调用计划。

输出规则:
- 只输出 JSON 数组
- 每个对象包含 tool 和 args
- 不要解释
"""

        logger.info(f"Planning for message: {message}")

        for attempt in range(self.max_retry + 1):

            try:

                text = self.call_llm(prompt)

                if not text:
                    logger.warning("LLM planning failed, fallback empty tasks")
                    return []

                logger.debug(f"LLM plan raw: {text}")

                raw_tasks = json5.loads(text)

                # 兼容 ["tool",{}]
                if isinstance(raw_tasks, list) and len(raw_tasks) == 2 and isinstance(raw_tasks[0], str):

                    raw_tasks = [{
                        "tool": raw_tasks[0],
                        "args": raw_tasks[1] if isinstance(raw_tasks[1], dict) else {}
                    }]

                fixed_tasks = []

                for t in raw_tasks:

                    if isinstance(t, dict) and "tool" in t:

                        fixed_tasks.append(t)

                    elif isinstance(t, list) and len(t) >= 1:

                        tool_name = t[0]

                        args = t[1] if len(t) > 1 and isinstance(t[1], dict) else {}

                        fixed_tasks.append({
                            "tool": tool_name,
                            "args": args
                        })

                    else:
                        logger.warning(f"[PLAN] invalid task: {t}")

                tasks = [
                    t for t in fixed_tasks
                    if t.get("tool") in available_tools
                ]

                logger.info(f"Plan generated: {tasks}")

                return tasks

            except Exception as e:

                logger.warning(
                    f"Plan parse failed ({attempt+1}/{self.max_retry+1}): {e}"
                )

        return []

    # ------------------------------------------------
    # 执行工具
    # ------------------------------------------------
    def run(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

        results = []

        for task in tasks:

            tool_name = task.get("tool")
            args = task.get("args")

            if not isinstance(args, dict):
                logger.warning(f"[RUN] args invalid, auto fix")
                args = {}

            if tool_name not in self.router.list_tools():

                results.append({
                    "tool": tool_name,
                    "result": f"工具不存在: {tool_name}"
                })

                continue

            logger.info(f"[RUN] tool={tool_name} args={args}")

            try:

                res = self.router.execute(tool_name, args)

            except Exception as e:

                logger.exception(f"[RUN] tool error: {tool_name}")

                res = {"error": str(e)}

            results.append({
                "tool": tool_name,
                "result": res
            })

        return results

    # ------------------------------------------------
    # 汇总结果
    # ------------------------------------------------
    def summarize(self, context: List[Dict[str, str]], results: List[Dict[str, Any]]) -> str:

        context_text = "\n".join(
            [f"{m['role']}: {m['content']}" for m in context]
        )

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

        self.conversations[session_id].append({
            "role": "user",
            "content": message
        })

        tasks = self.plan(message, context=self.conversations[session_id])

        if not tasks:

            reply = self.call_llm(
                message,
                context=self.conversations[session_id]
            )

            if not reply:
                reply = "AI 当前不可用，请稍后再试。"

            self.conversations[session_id].append({
                "role": "assistant",
                "content": reply
            })

            return {"message": reply}

        results = self.run(tasks)

        summary = self.summarize(
            self.conversations[session_id],
            results
        )

        self.conversations[session_id].append({
            "role": "assistant",
            "content": summary
        })

        return {
            "tasks": results,
            "summary": summary
        }


agent_brain = LLMBrain()