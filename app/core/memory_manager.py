"""
Module: memory_manager

Purpose:
    Persistent memory manager for Solo AI Platform Agent.

Responsibilities:
    - Load USER profile
    - Load Agent SOUL configuration
    - Maintain long-term MEMORY.md
    - Maintain daily session logs
    - Support additional files like HEARTBEAT.md
    - Provide safe file access utilities
    - Query memory by keyword
    - Clear old logs or memory files

Design Goals:
    - Human-readable memory files
    - Simple persistence
    - High fault tolerance
    - Clear logging
    - Unified interface for all memory operations
"""

import os
import datetime
from typing import List
from app.utils.logger import get_logger
import json

logger = get_logger("memory_manager")


class MemoryManager:
    """
    MemoryManager handles persistent text-based memory storage.

    Storage Structure:
        app/memory/
            USER.md
            SOUL.md
            MEMORY.md
            HEARTBEAT.md
            daily_logs/YYYY-MM-DD.md
    """

    BASE_DIR = "app/memory"
    DAILY_DIR = os.path.join(BASE_DIR, "daily_logs")

    def __init__(self):
        """Initialize memory directories."""
        try:
            os.makedirs(self.BASE_DIR, exist_ok=True)
            os.makedirs(self.DAILY_DIR, exist_ok=True)
            logger.info("[MemoryManager] Initialized memory directories")
        except Exception:
            logger.exception("[MemoryManager] Failed to initialize memory directories")

    # ------------------------------------------------
    # Safe file read/write/append
    # ------------------------------------------------
    def read_file(self, filename: str) -> str:
        """Read a memory file safely."""
        path = os.path.join(self.BASE_DIR, filename)
        try:
            if not os.path.exists(path):
                logger.warning(f"[MemoryManager] File not found: {filename}")
                return ""
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            logger.info(f"[MemoryManager] Read file: {filename}")
            return content
        except Exception:
            logger.exception(f"[MemoryManager] Failed to read file: {filename}")
            return ""

    def write_file(self, filename: str, content: str) -> bool:
        """Write content to memory file (overwrite)."""
        path = os.path.join(self.BASE_DIR, filename)
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info(f"[MemoryManager] Written file: {filename}")
            return True
        except Exception:
            logger.exception(f"[MemoryManager] Failed to write file: {filename}")
            return False

    def append_file(self, filename: str, text: str) -> bool:
        """Append text to memory file safely."""
        path = os.path.join(self.BASE_DIR, filename)
        try:
            with open(path, "a", encoding="utf-8") as f:
                f.write(text + "\n")
            logger.info(f"[MemoryManager] Appended to file: {filename}")
            return True
        except Exception:
            logger.exception(f"[MemoryManager] Failed to append to file: {filename}")
            return False

    def clear_file(self, filename: str) -> bool:
        """Clear memory file content safely."""
        path = os.path.join(self.BASE_DIR, filename)
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("")
            logger.info(f"[MemoryManager] Cleared file: {filename}")
            return True
        except Exception:
            logger.exception(f"[MemoryManager] Failed to clear file: {filename}")
            return False

    # ------------------------------------------------
    # Daily logs
    # ------------------------------------------------
    def append_daily_log(self, text: str) -> bool:
        """Append interaction log to today's memory file."""
        try:
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            path = os.path.join(self.DAILY_DIR, f"{today}.md")

            if isinstance(text, dict):
                text = json.dumps(text, ensure_ascii=False)

            text = f"[{today}] {text}"

            with open(path, "a", encoding="utf-8") as f:
                f.write(text + "\n")
            logger.info(f"[MemoryManager] Appended daily log: {today}.md")
            return True
        except Exception:
            logger.exception("[MemoryManager] Failed to append daily log")
            return False

    def load_recent_logs(self, days: int = 2) -> str:
        """Load recent daily logs for context."""
        logs: List[str] = []
        try:
            for i in range(days):
                day = datetime.datetime.now() - datetime.timedelta(days=i)
                filename = day.strftime("%Y-%m-%d") + ".md"
                path = os.path.join(self.DAILY_DIR, filename)
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        logs.append(f.read())
            logger.info(f"[MemoryManager] Loaded recent logs ({days} days)")
            return "\n".join(logs)
        except Exception:
            logger.exception("[MemoryManager] Failed to load recent logs")
            return ""

    def clear_daily_logs(self, older_than_days: int = 0) -> bool:
        """
        Clear daily logs older than N days.
        If older_than_days=0, clear all logs.
        """
        try:
            now = datetime.datetime.now()
            files = os.listdir(self.DAILY_DIR)
            for file in files:
                if not file.endswith(".md"):
                    continue
                date_str = file.replace(".md", "")
                file_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                if older_than_days == 0 or (now - file_date).days >= older_than_days:
                    os.remove(os.path.join(self.DAILY_DIR, file))
                    logger.info(f"[MemoryManager] Cleared daily log: {file}")
            return True
        except Exception:
            logger.exception("[MemoryManager] Failed to clear daily logs")
            return False

    # ------------------------------------------------
    # Identity & long-term memory
    # ------------------------------------------------
    def load_user(self) -> str:
        """Load USER.md profile."""
        return self.read_file("USER.md")

    def load_soul(self) -> str:
        """Load SOUL.md configuration."""
        return self.read_file("SOUL.md")

    def load_memory(self) -> str:
        """Load MEMORY.md content."""
        return self.read_file("MEMORY.md")

    def load_heartbeat(self) -> str:
        """Load HEARTBEAT.md content."""
        return self.read_file("HEARTBEAT.md")

    # ------------------------------------------------
    # Memory Query
    # ------------------------------------------------
    def query_memory(self, keyword: str, recent_days: int = 2) -> str:
        """
        Search MEMORY.md and recent logs for keyword.

        Args:
            keyword: string to search
            recent_days: include N days of daily logs

        Returns:
            Matched lines joined by newline
        """
        try:
            memory_text = self.load_memory()
            logs_text = self.load_recent_logs(days=recent_days)
            combined = memory_text + "\n" + logs_text
            matches = [line for line in combined.splitlines() if keyword.lower() in line.lower()]
            logger.info(f"[MemoryManager] Found {len(matches)} matches for '{keyword}'")
            return "\n".join(matches)
        except Exception:
            logger.exception(f"[MemoryManager] Memory query failed for '{keyword}'")
            return ""

    # ------------------------------------------------
    # Utilities
    # ------------------------------------------------
    def list_daily_logs(self) -> List[str]:
        """List all daily log filenames."""
        try:
            files = sorted(os.listdir(self.DAILY_DIR))
            logger.info(f"[MemoryManager] Found {len(files)} daily logs")
            return files
        except Exception:
            logger.exception("[MemoryManager] Failed to list daily logs")
            return []