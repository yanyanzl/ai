"""
main.py - Solo AI Platform v1 完整演示

功能：
- 自动加载 Agent
- 初始化 ToolRouter
- 启动 Scheduler
- DevAgent 自动生成 demo_agent
- 执行 Demo Task 和 Finance 示例任务
"""
from pydantic import BaseModel
from fastapi import FastAPI, Request
from app.core.tool_router import tool_router
from app.core.agent_registry import load_agents
from app.workflow.scheduler import add_job, start_scheduler
from app.agents.file_agent import scan_desktop
from app.agents.system_agent import clean_temp
from app.agents.finance_agent import task_finance_example
from app.agents.dev_agent import generate_agent
import asyncio

app = FastAPI(title="Solo AI Platform v1")
router = tool_router

# 自动加载所有 Agent
load_agents()


# -----------------------------
# 请求数据结构
# -----------------------------
class ChatRequest(BaseModel):
    message: str

# --------------------------
# DevAgent 示例：生成 demo_agent
# --------------------------
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
print(res)



# -----------------------------
# 健康检查
# -----------------------------
@app.get("/")
def home():
    return {"status": "AI Butler running"}



# --------------------------
# REST API: 调用工具
# --------------------------
@app.post("/chat")
async def chat(request: Request):
    """
    请求 JSON:
    {
        "tool": "scan_desktop",
        "args": {"param": "value"}
    }
    """
    try:
        data = await request.json()
        tool_name = data.get("tool")
        args = data.get("args", {})

        if not tool_name:
            return {"error": "必须提供 tool 字段"}

        result = router.execute(tool_name, args)
        return result
    except Exception as e:
        return {"error": str(e)}

# --------------------------
# Scheduler 任务
# --------------------------
def task_demo():
    res = router.execute("demo_task")
    if "error" in res:
        print(f"[TASK ERROR] demo_task: {res['error']}")
    else:
        print(f"[TASK] demo_task 执行结果: {res['message']}")

def task_scan():
    res = scan_desktop()
    if "error" in res:
        print(f"[TASK ERROR] scan_desktop: {res['error']}")
    else:
        print(f"[TASK] 桌面文件数量: {res.get('total', 0)}")

def task_clean():
    res = clean_temp()
    if "error" in res:
        print(f"[TASK ERROR] clean_temp: {res['error']}")
    else:
        print(f"[TASK] 删除临时文件数量: {res.get('deleted', 0)}")

# --------------------------
# Scheduler 初始化
# --------------------------
def init_scheduler():
    # 每1分钟执行 Demo Task
    add_job(task_demo, trigger="interval", minutes=1)
    # 每2分钟执行桌面扫描
    add_job(task_scan, trigger="interval", minutes=2)
    # 每3分钟执行清理临时文件
    add_job(task_clean, trigger="interval", minutes=3)
    # 每4分钟执行金融任务示例
    add_job(task_finance_example, trigger="interval", minutes=4)
    # 启动 Scheduler
    start_scheduler()

# --------------------------
# FastAPI 启动事件
# --------------------------
@app.on_event("startup")
async def startup_event():
    print("[INFO] Solo AI Platform v1 启动中...")
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, init_scheduler)
    print("[INFO] Scheduler 初始化完成")