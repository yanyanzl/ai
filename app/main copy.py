"""
main.py

AI 数字管家 API

功能：
1 提供聊天接口
2 调用工具路由
3 统一错误处理
"""

from fastapi import FastAPI
from pydantic import BaseModel
from app.core.tool_router import ToolRouter
import traceback

app = FastAPI()

# 初始化工具路由
router = ToolRouter()


# -----------------------------
# 请求数据结构
# -----------------------------
class ChatRequest(BaseModel):
    message: str


# -----------------------------
# 健康检查
# -----------------------------
@app.get("/")
def home():
    return {"status": "AI Butler running"}


# -----------------------------
# Chat API
# -----------------------------
@app.post("/chat")
def chat(req: ChatRequest):

    try:

        user_msg = req.message.lower()

        # --------------------------------
        # 工具识别（简单版）
        # 后面会升级为 LLM Router
        # --------------------------------

        if "扫描桌面" in user_msg or "scan desktop" in user_msg:
            result = router.execute("scan_desktop")

        elif "大文件" in user_msg:
            result = router.execute("find_large_files")

        elif "整理桌面" in user_msg:
            result = router.execute("organize_desktop")

        elif "文件统计" in user_msg:
            result = router.execute("file_statistics")

        else:
            return {
                "type": "chat",
                "message": "我可以帮你：扫描桌面 / 找大文件 / 整理桌面 / 文件统计"
            }

        return {
            "type": "tool_result",
            "data": result
        }

    except Exception as e:

        # 打印完整错误
        traceback.print_exc()

        return {
            "error": str(e)
        }