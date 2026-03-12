"""
Module: context_builder

Purpose:
    Build system and agent identity context for LLM calls.

Features:
    - Loads SOUL.md (agent personality)
    - Loads USER.md (user profile/preferences)
    - Loads MEMORY.md (long-term memory)
    - Loads recent conversation logs
    - Handles missing or corrupt files gracefully
    - Generates a single context string for LLM injection
"""

from app.core.memory_manager import MemoryManager
from app.utils.logger import get_logger

logger = get_logger("context_builder")


class ContextBuilder:
    """
    Build identity and system context for LLM calls.

    Attributes:
        memory: MemoryManager instance for loading persistent files.
    """

    def __init__(self):
        self.memory = MemoryManager()
        logger.info("[ContextBuilder] Initialized")

    def build_identity_context(self) -> str:
        """
        Build the full identity context for the LLM session.

        Returns:
            str: Combined context including agent soul, user profile,
                 long-term memory, and recent logs.
        """
        soul = self._safe_load("SOUL", self.memory.load_soul)
        user = self._safe_load("USER", self.memory.load_user)
        memory = self._safe_load("MEMORY", self.memory.load_memory)
        logs = self._safe_load("RECENT_LOGS", self.memory.load_recent_logs)

        context_sections = [
            ("=== AGENT SOUL ===", soul),
            ("=== USER PROFILE ===", user),
            ("=== LONG TERM MEMORY ===", memory),
            ("=== RECENT LOGS ===", logs),
        ]

        context = "\n\n".join(f"{title}\n{content}" for title, content in context_sections)
        logger.info("[ContextBuilder] Identity context built successfully")
        return context

    def _safe_load(self, name: str, loader_func) -> str:
        """
        Load a component safely, catching exceptions.

        Args:
            name (str): Component name for logging.
            loader_func (Callable): MemoryManager method to call.

        Returns:
            str: Loaded content, or placeholder on error.
        """
        try:
            content = loader_func()
            if not content:
                logger.warning(f"[ContextBuilder] {name} is empty")
                return f"(empty {name})"
            return content
        except Exception as e:
            logger.exception(f"[ContextBuilder] Failed to load {name}")
            return f"(error loading {name}: {str(e)})"