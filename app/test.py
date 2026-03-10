"""
test_client_report.py - Solo AI Platform v1.1 测试报告生成器

说明：
- 自动执行测试脚本
- 收集所有测试结果
- 输出 JSON 报告文件 report.json
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"
REPORT_FILE = "report.json"

# 存储测试结果
test_report = []

def log_and_record(title, data, request_info=None):
    """
    打印日志并记录到 report
    """
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{ts}] === {title} ===")
    print(json.dumps(data, indent=2, ensure_ascii=False))

    test_report.append({
        "timestamp": ts,
        "test": title,
        "request": request_info or {},
        "response": data
    })


# --------------------------
# 1. 健康检查
# --------------------------
def test_health():
    try:
        resp = requests.get(f"{BASE_URL}/")
        log_and_record("Health Check", resp.json(), {"method":"GET","endpoint":"/"})
    except Exception as e:
        log_and_record("Health Check", {"error": str(e)}, {"method":"GET","endpoint":"/"})


# --------------------------
# 2. 工具列表
# --------------------------
def test_tools():
    try:
        resp = requests.get(f"{BASE_URL}/tools")
        log_and_record("Tools List", resp.json(), {"method":"GET","endpoint":"/tools"})
    except Exception as e:
        log_and_record("Tools List", {"error": str(e)}, {"method":"GET","endpoint":"/tools"})


# --------------------------
# 3. 单工具调用
# --------------------------
def test_tool(tool_name, args=None):
    args = args or {}
    payload = {"tool": tool_name, "args": args}
    try:
        resp = requests.post(f"{BASE_URL}/chat", json=payload)
        log_and_record(f"Tool Call: {tool_name}", resp.json(), {"method":"POST","endpoint":"/chat","payload":payload})
    except Exception as e:
        log_and_record(f"Tool Call: {tool_name}", {"error": str(e)}, {"method":"POST","endpoint":"/chat","payload":payload})


# --------------------------
# 4. AI 自动规划工具
# --------------------------
def test_ai(message):
    payload = {"message": message}
    try:
        resp = requests.post(f"{BASE_URL}/chat", json=payload)
        log_and_record(f"AI Call: {message}", resp.json(), {"method":"POST","endpoint":"/chat","payload":payload})
    except Exception as e:
        log_and_record(f"AI Call: {message}", {"error": str(e)}, {"method":"POST","endpoint":"/chat","payload":payload})


# --------------------------
# 5. DevAgent 测试（修正版）
# --------------------------
def test_dev_agent():
    code = """
from app.tools.tool_decorator import tool

@tool('test_task')
def test_task():
    return {'message':'Test Task executed successfully'}
"""
    # 注意这里用 agent_name，而不是 name
    payload = {
        "tool": "generate_agent",
        "args": {
            "agent_name": "test_agent",  # 与 generate_agent 函数参数匹配
            "code": code
        }
    }
    try:
        resp = requests.post(f"{BASE_URL}/chat", json=payload)
        log_and_record("DevAgent Generate", resp.json(), {"method":"POST","endpoint":"/chat","payload":payload})

        # 等待 agent 注册到 router
        time.sleep(1)
        # 调用新生成的工具 test_task
        test_tool("test_task")
    except Exception as e:
        log_and_record("DevAgent Generate", {"error": str(e)}, {"method":"POST","endpoint":"/chat","payload":payload})


# --------------------------
# 6. FinanceAgent 测试
# --------------------------
def test_finance_agent():
    payload = {"tool":"task_finance_example"}
    try:
        resp = requests.post(f"{BASE_URL}/chat", json=payload)
        log_and_record("FinanceAgent Task", resp.json(), {"method":"POST","endpoint":"/chat","payload":payload})
    except Exception as e:
        log_and_record("FinanceAgent Task", {"error": str(e)}, {"method":"POST","endpoint":"/chat","payload":payload})


# --------------------------
# 7. Scheduler 测试提示
# --------------------------
def test_scheduler():
    print("\n=== Scheduler Test ===")
    print("请观察终端 Scheduler 输出日志，确认定时任务是否执行")


# --------------------------
# 8. 执行所有测试
# --------------------------
if __name__ == "__main__":
    test_health()
    test_tools()

    # 单工具调用
    test_tool("scan_desktop")
    test_tool("clean_temp")

    # AI 自动规划调用
    test_ai("帮我扫描桌面并清理临时文件")

    # DevAgent 测试
    test_dev_agent()

    # FinanceAgent 测试
    test_finance_agent()

    # Scheduler 测试
    test_scheduler()

    # 保存 JSON 报告
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(test_report, f, ensure_ascii=False, indent=2)

    print(f"\n=== 测试完成，报告已保存到 {REPORT_FILE} ===")