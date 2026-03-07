"""
智能自我增强 DevAgent
- 能分析现有工具
- 自动组合生成新工具
- 自动注册 Scheduler
- 全面容错 + 日志
"""

import ast
import importlib
from pathlib import Path
from app.tools.tool_decorator import tool
from app.core.agent_registry import load_agents
from app.workflow.scheduler import add_job
# from app.core.tool_router import TOOL_REGISTRY
from app.core.tool_router import tool_router
AGENT_DIR = Path(__file__).parent

# --------------------------
# 安全检查
# --------------------------
def is_safe_code(code: str) -> bool:
    """静态检查危险操作"""
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if hasattr(node.func, "attr") and node.func.attr in ["system", "popen"]:
                    return False
        return True
    except Exception:
        return False

# --------------------------
# 工具调用辅助
# --------------------------
def import_tool_and_execute(tool_name: str):

    result = tool_router.execute(tool_name)

    if "error" in result:
        print("[DEV AGENT ERROR]", result["error"])
    else:
        print("[DEV AGENT RESULT]", result)

    return result


# --------------------------
# 核心生成函数
# --------------------------
@tool("generate_agent_with_task")
def generate_agent_with_task(agent_name: str, code: str, schedule: dict = None):
    """
    生成 Agent + 自动注册 + 可选 Scheduler
    """
    safe_name = agent_name.lower()
    if safe_name in ["file_agent", "system_agent", "dev_agent", "finance_agent"]:
        return {"error": f"禁止覆盖核心 Agent: {safe_name}"}

    if not is_safe_code(code):
        return {"error": "代码存在危险操作"}

    file_path = AGENT_DIR / f"{safe_name}.py"
    if file_path.exists():
        return {"error": f"Agent 文件已存在: {file_path}"}

    try:
        # 写入文件
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)

        # 自动导入
        importlib.import_module(f"app.agents.{safe_name}")
        print(f"[INFO] 新 Agent '{safe_name}' 自动加载成功")

        # 注册 Scheduler
        if schedule:
            tool_names = [name for name in code.split("@tool(") if name]
            for t in tool_names:
                t_name = t.split("'")[1]
                func = lambda tn=t_name: import_tool_and_execute(tn)
                add_job(func, **schedule)
            print(f"[INFO] Scheduler 任务已注册: {schedule}")

        return {"success": f"Agent '{safe_name}' 生成、加载成功"}
    except Exception as e:
        return {"error": str(e)}

# --------------------------
# 自我增强函数
# --------------------------
@tool("auto_enhance_agent")
def auto_enhance_agent(new_agent_name: str, tool_sequence: list, schedule: dict = None):
    """
    自动生成组合工具
    :param new_agent_name: 新 Agent 名
    :param tool_sequence: 要组合调用的工具名列表
    :param schedule: Scheduler 参数
    """
    try:
        # 生成组合工具代码
        tools_code = "\n    ".join([f"res = tool_router.tools.get('{t}')()\n    print('工具 {t} 结果:', res)" for t in tool_sequence])
        code = f"""
from app.tools.tool_decorator import tool
from app.core.tool_router import tool_router

@tool('{new_agent_name}_task')
def {new_agent_name}_task():
    try:
        {tools_code}
        return {{'message': '组合工具 {new_agent_name}_task 执行完成'}}
    except Exception as e:
        return {{'error': str(e)}}
"""
        # 调用生成函数
        return generate_agent_with_task(new_agent_name, code, schedule)
    except Exception as e:
        return {"error": str(e)}
    


@tool("generate_agent")
def generate_agent(agent_name: str, code: str):
    """
    生成新的 Agent 并自动注册
    参数:
        agent_name: str, 文件名（不带 .py）
        code: str, Python 代码
    返回:
        dict
    """
    try:
        safe_name = agent_name.lower()
        # 核心 agent 禁止覆盖
        if safe_name in ["file_agent", "system_agent", "dev_agent", "finance_agent"]:
            return {"error": f"禁止覆盖核心 Agent: {safe_name}"}

        file_path = AGENT_DIR / f"{safe_name}.py"
        if file_path.exists():
            return {"error": f"Agent 文件已存在: {file_path}"}

        # 写入文件
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)

        # 自动加载新 Agent
        try:
            importlib.import_module(f"app.agents.{safe_name}")
            print(f"[INFO] 新 Agent '{safe_name}' 加载成功")
        except Exception as e:
            return {"error": f"生成成功，但加载失败: {e}"}

        return {"success": f"Agent '{safe_name}' 生成并加载成功"}
    except Exception as e:
        return {"error": str(e)}