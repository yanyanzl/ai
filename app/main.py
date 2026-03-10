"""
main.py - Solo AI Platform v2

功能：
- 自动加载 Agent
- ToolRouter 初始化
- DevAgent 自动生成 demo_agent
- Scheduler 异步启动
- AI / Tool REST API
- 使用 FastAPI lifespan 生命周期
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager
import asyncio

from app.core.tool_router import tool_router
from app.core.agent_registry import load_agents
from app.workflow.scheduler import start_scheduler, add_jobs_from_config

from app.agents.file_agent import scan_desktop
from app.agents.system_agent import clean_temp
from app.agents.finance_agent import task_finance_example
from app.agents.dev_agent import generate_agent

from app.brain.llm_brain import agent_brain

from app.utils.logger import get_logger

logger = get_logger("main")

# --------------------------
# Tool Router
# --------------------------
router = tool_router


# --------------------------
# Scheduler 任务封装
# --------------------------
def wrap_task(func, name: str):
    """统一任务返回结构"""

    def wrapper():
        try:
            res = func()

            if not isinstance(res, dict):
                res = {"message": str(res)}

            if "error" in res:
                return {
                    "task": name,
                    "status": "error",
                    "result": res["error"],
                }

            return {
                "task": name,
                "status": "ok",
                "result": res.get("message", res),
            }

        except Exception as e:
            return {
                "task": name,
                "status": "error",
                "result": str(e),
            }

    return wrapper


# --------------------------
# Scheduler 任务
# --------------------------
task_funcs = {
    "demo_task": wrap_task(lambda: router.execute("demo_task"), "demo_task"),
    "scan_desktop": wrap_task(scan_desktop, "scan_desktop"),
    "clean_temp": wrap_task(clean_temp, "clean_temp"),
    "finance_example": wrap_task(task_finance_example, "finance_example"),
}


# --------------------------
# Scheduler 初始化
# --------------------------
def init_scheduler():

    add_jobs_from_config(task_funcs)

    start_scheduler()

    print("[INFO] Scheduler 已启动")


# --------------------------
# DevAgent 示例
# --------------------------
def init_dev_agent():

    demo_code = """
from app.tools.tool_decorator import tool

@tool('demo_task')
def demo_task():
    try:
        return {'message': 'Demo Task 执行成功'}
    except Exception as e:
        return {'error': str(e)}
"""

    res = generate_agent("demo_agent", demo_code)

    print("[DevAgent] demo_agent 生成结果:", res)

    try:

        from app.agents.demo_agent import demo_task

        router.register("demo_task", demo_task)

        print("[DevAgent] demo_task 注册成功")

    except Exception as e:

        print("[WARN] demo_task 注册失败:", e)


# --------------------------
# FastAPI 生命周期
# --------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):

    print("[INFO] Solo AI Platform 启动中...")

    # 加载 Agent
    load_agents()
    print("[INFO] Agents 已加载")

    # 初始化 DevAgent
    init_dev_agent()

    # 启动 Scheduler
    asyncio.create_task(asyncio.to_thread(init_scheduler))

    print("[INFO] Scheduler 初始化完成")

    yield

    print("[INFO] Solo AI Platform 正在关闭...")


# --------------------------
# FastAPI 初始化
# --------------------------
app = FastAPI(
    title="Solo AI Platform",
    lifespan=lifespan,
)


# --------------------------
# 请求结构
# --------------------------
class ChatRequest(BaseModel):

    message: Optional[str] = None

    tool: Optional[str] = None

    args: Optional[Dict[str, Any]] = None


# --------------------------
# 健康检查
# --------------------------
@app.get("/")
def home():
    return {"status": "AI Butler running"}

@app.get("/debug/tools")
def debug_tools():
    return tool_router.tools

# --------------------------
# 工具列表
# --------------------------
@app.get("/tools")
def tools():

    return router.list_tools()


# --------------------------
# AI / Tool API
# --------------------------
@app.post("/chat")
async def chat(data: ChatRequest):
    """
    调用模式：
    1. AI 对话模式：只传 message，AI 会生成任务并执行
    2. 单工具模式：传 tool 和可选 args，直接执行指定工具
    """
    try:
        # ------------------------------
        # 1. AI 对话模式
        # ------------------------------
        if data.message:
            logger.info(f"[CHAT] AI 模式 message={data.message}")
            # handle() 会 plan -> run
            result = agent_brain.handle(data.message)
            logger.info(f"[CHAT] AI 返回: {result}")
            return result

        # ------------------------------
        # 2. 单工具调用模式
        # ------------------------------
        if data.tool:
            tool_name = data.tool
            args = data.args or {}
            logger.info(f"[CHAT] Tool 模式 tool={tool_name} args={args}")

            if tool_name not in router.list_tools():
                logger.warning(f"[CHAT] 工具不存在: {tool_name}")
                return {"error": f"工具 '{tool_name}' 不存在"}

            try:
                res = router.execute(tool_name, args)
                logger.info(f"[CHAT] Tool 返回: {res}")
                return {"tool": tool_name, "result": res}
            except Exception as e:
                logger.error(f"[CHAT] Tool 执行错误: {e}")
                return {"error": f"工具执行错误: {e}"}

        # ------------------------------
        # 3. 无有效参数
        # ------------------------------
        logger.warning("[CHAT] 必须提供 message 或 tool")
        return {"error": "必须提供 message 或 tool"}

    except Exception as e:
        logger.error(f"[CHAT] API 异常: {e}")
        return {"error": f"API 异常: {e}"}