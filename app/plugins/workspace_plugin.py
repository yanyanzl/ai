# app/plugins/workspace_plugin.py

import os, json, subprocess
from typing import Dict, Any
from app.utils.logger import get_logger

logger = get_logger("WorkspacePlugin")

class WorkspacePlugin:
    """
    WorkspacePlugin 提供安全的文件和 shell 操作接口。
    
    支持功能:
        - 文件读写
        - 列目录
        - 安全执行 shell 命令（仅允许白名单）
    """

    SAFE_COMMANDS = ["ls", "cat", "echo", "pwd", "mkdir", "touch"]  # 可扩展

    def __init__(self, base_dir: str = "./workspace"):
        self.base_dir = os.path.abspath(base_dir)
        os.makedirs(self.base_dir, exist_ok=True)
        logger.info(f"[WorkspacePlugin] Initialized at {self.base_dir}")

    # -----------------------------
    # 文件读写接口
    # -----------------------------
    def read_file(self, path: str) -> str:
        abs_path = os.path.join(self.base_dir, path)
        try:
            with open(abs_path, "r", encoding="utf-8") as f:
                content = f.read()
            logger.info(f"[WorkspacePlugin] Read file: {abs_path}")
            return content
        except Exception as e:
            logger.exception(f"[WorkspacePlugin] Failed to read file {abs_path}")
            return f"Error: {str(e)}"

    def write_file(self, path: str, content: str) -> str:
        abs_path = os.path.join(self.base_dir, path)
        try:
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            with open(abs_path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info(f"[WorkspacePlugin] Wrote file: {abs_path}")
            return f"File {path} written successfully"
        except Exception as e:
            logger.exception(f"[WorkspacePlugin] Failed to write file {abs_path}")
            return f"Error: {str(e)}"

    # -----------------------------
    # 列目录接口
    # -----------------------------
    def list_dir(self, path: str = "") -> list:
        abs_path = os.path.join(self.base_dir, path)
        try:
            files = os.listdir(abs_path)
            logger.info(f"[WorkspacePlugin] Listed directory: {abs_path}")
            return files
        except Exception as e:
            logger.exception(f"[WorkspacePlugin] Failed to list dir {abs_path}")
            return [f"Error: {str(e)}"]

    # -----------------------------
    # 安全执行 shell 命令
    # -----------------------------
    def run_command(self, cmd: str) -> str:
        """
        仅允许执行 SAFE_COMMANDS 白名单命令
        """
        if not any(cmd.strip().startswith(c) for c in self.SAFE_COMMANDS):
            msg = f"Command not allowed: {cmd}"
            logger.warning(f"[WorkspacePlugin] {msg}")
            return msg
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, cwd=self.base_dir, timeout=10
            )
            output = result.stdout.strip() or result.stderr.strip()
            logger.info(f"[WorkspacePlugin] Executed command: {cmd}")
            return output
        except Exception as e:
            logger.exception(f"[WorkspacePlugin] Command execution failed: {cmd}")
            return f"Error: {str(e)}"

    # -----------------------------
    # 插件统一入口
    # -----------------------------
    def execute(self, tool_name: str, args: Dict[str, Any]) -> Any:
        """
        调用统一入口, 由 LLMBrain.run() 调用
        """
        if tool_name == "read_file":
            return self.read_file(args.get("path", ""))
        elif tool_name == "write_file":
            return self.write_file(args.get("path", ""), args.get("content", ""))
        elif tool_name == "list_dir":
            return self.list_dir(args.get("path", ""))
        elif tool_name == "run_command":
            return self.run_command(args.get("cmd", ""))
        else:
            msg = f"Unknown tool: {tool_name}"
            logger.warning(f"[WorkspacePlugin] {msg}")
            return msg