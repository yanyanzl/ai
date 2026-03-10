"""
system_agent.py

系统维护 Agent

提供工具：

clean_temp
"""

import tempfile
import os

from app.tools.tool_decorator import tool
from app.utils.logger import get_logger

logger = get_logger("system_agent")


@tool("clean_temp")
def clean_temp():
    """
    清理系统临时文件
    """

    try:

        temp_dir = tempfile.gettempdir()

        logger.info(f"Cleaning temp directory: {temp_dir}")

        files = os.listdir(temp_dir)

        deleted = 0

        for f in files:

            path = os.path.join(temp_dir, f)

            try:

                if os.path.isfile(path):

                    os.remove(path)

                    deleted += 1

            except Exception:
                pass

        return {
            "deleted": deleted
        }

    except Exception as e:

        logger.exception("clean_temp failed")

        return {
            "error": str(e)
        }