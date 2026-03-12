# ------------------------------
# workspace_manager.py
# ------------------------------
"""
Module: workspace_manager

Purpose:
    Provide safe and controlled file and shell operations for the agent workspace.

Workspace Restrictions:
    - All operations restricted to app/workspace
    - Prevent access outside sandbox
"""

import os
import subprocess
from typing import List, Dict
from app.utils.logger import get_logger

logger = get_logger("workspace_manager")


class WorkspaceManager:
    BASE_DIR = "app/workspace"

    def __init__(self):
        """Initialize workspace directory."""
        try:
            os.makedirs(self.BASE_DIR, exist_ok=True)
            logger.info("[WorkspaceManager] Initialized workspace")
        except Exception:
            logger.exception("[WorkspaceManager] Workspace initialization failed")

    # ------------------------------
    # Path Security
    # ------------------------------
    def _safe_path(self, path: str) -> str:
        """
        Ensure path is inside workspace sandbox.

        Args:
            path: relative path
        Returns:
            Absolute safe path
        Raises:
            ValueError if path escapes workspace
        """
        full = os.path.abspath(os.path.join(self.BASE_DIR, path))
        if not full.startswith(os.path.abspath(self.BASE_DIR)):
            raise ValueError("Unsafe path detected")
        return full

    # ------------------------------
    # File Operations
    # ------------------------------
    def read_file(self, path: str) -> str:
        """Read a file safely."""
        try:
            full = self._safe_path(path)
            with open(full, "r", encoding="utf-8") as f:
                content = f.read()
            logger.info(f"[WorkspaceManager] Read file: {path}")
            return content
        except Exception:
            logger.exception(f"[WorkspaceManager] Failed to read file: {path}")
            return ""

    def write_file(self, path: str, content: str) -> bool:
        """Write content to file (overwrite)."""
        try:
            full = self._safe_path(path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info(f"[WorkspaceManager] Written file: {path}")
            return True
        except Exception:
            logger.exception(f"[WorkspaceManager] Failed to write file: {path}")
            return False

    def delete_file(self, path: str) -> bool:
        """Delete a file safely."""
        try:
            full = self._safe_path(path)
            if os.path.exists(full):
                os.remove(full)
                logger.info(f"[WorkspaceManager] Deleted file: {path}")
            return True
        except Exception:
            logger.exception(f"[WorkspaceManager] Failed to delete file: {path}")
            return False

    def list_files(self, dir_path: str = "") -> List[str]:
        """List files in directory inside workspace."""
        try:
            full_dir = self._safe_path(dir_path)
            files = os.listdir(full_dir)
            logger.info(f"[WorkspaceManager] Listed files in {dir_path}: {len(files)} items")
            return files
        except Exception:
            logger.exception(f"[WorkspaceManager] Failed to list files in {dir_path}")
            return []

    def make_dir(self, dir_path: str) -> bool:
        """Create directory safely."""
        try:
            full_dir = self._safe_path(dir_path)
            os.makedirs(full_dir, exist_ok=True)
            logger.info(f"[WorkspaceManager] Directory created: {dir_path}")
            return True
        except Exception:
            logger.exception(f"[WorkspaceManager] Failed to create directory: {dir_path}")
            return False

    # ------------------------------
    # Shell Execution
    # ------------------------------
    def run_shell(self, command: str) -> Dict[str, str]:
        """
        Execute shell command in workspace safely.

        Returns:
            dict: { "stdout": ..., "stderr": ..., "status": int }
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.BASE_DIR
            )
            logger.info(f"[WorkspaceManager] Executed shell: {command}")
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "status": result.returncode
            }
        except Exception:
            logger.exception(f"[WorkspaceManager] Shell execution failed: {command}")
            return {"stdout": "", "stderr": "shell error", "status": -1}