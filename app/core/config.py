"""

    example:
    from app.core.config import Config

    llm_host = Config.get("llm.host")
    llm_model = Config.get("llm.model")

"""


OLLAMA_URL = "http://192.168.0.216:11434/api/chat"

MODEL_NAME = "llama3.1-optimized"

ALLOWED_PATHS = [
    "~/Desktop",
    "~/Downloads"
]

# core/config.py
import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.yaml"

class Config:
    _config = None

    @classmethod
    def load(cls):
        if cls._config is None:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cls._config = yaml.safe_load(f)
        return cls._config

    @classmethod
    def get(cls, key_path, default=None):
        """
        支持点分隔路径获取配置，例如 'llm.host'
        """
        keys = key_path.split(".")
        val = cls.load()
        for k in keys:
            val = val.get(k, default)
            if val is default:
                break
        return val