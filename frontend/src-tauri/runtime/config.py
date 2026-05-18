import os
import json
from dotenv import load_dotenv

load_dotenv()

_BASE_DIR = os.path.dirname(__file__)
_CONTENTS_DIR = os.path.dirname(_BASE_DIR)
_RESOURCES_DIR = _CONTENTS_DIR if os.path.basename(_CONTENTS_DIR) == "Resources" else None
_USER_DATA_DIR = os.path.expanduser("~/Library/Application Support/Aible OS")
os.makedirs(_USER_DATA_DIR, exist_ok=True)
_DEFAULT_DB_PATH = os.path.join(_USER_DATA_DIR, "aible_os.db")
_SETTINGS_PATH = os.path.join(_USER_DATA_DIR, "config.json")


def _load_user_settings() -> dict:
    if not os.path.isfile(_SETTINGS_PATH):
        return {}
    try:
        with open(_SETTINGS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _get_setting(key: str, default: str = "") -> str:
    """Get a setting, checking: user config file > env var > default"""
    # First check: user config file (saved from settings page)
    user_settings = _load_user_settings()
    user_value = user_settings.get(key)
    if user_value not in (None, ""):
        return str(user_value)
    # Second check: env var (from .env file or system env)
    env_value = os.getenv(key)
    if env_value not in (None, ""):
        return env_value
    # Third: fallback to default
    return default


_raw_database_url = os.getenv("DATABASE_URL")
if _raw_database_url:
    DATABASE_URL = _raw_database_url
else:
    DATABASE_URL = f"sqlite+aiosqlite:////{_DEFAULT_DB_PATH}"

LLM_API_KEY = _get_setting("LLM_API_KEY", "")
LLM_BASE_URL = _get_setting("LLM_BASE_URL", "https://open.bigmodel.cn/api/paas/v4")
LLM_MODEL = _get_setting("LLM_MODEL", "glm-4-plus")
SECRET_KEY = os.getenv("SECRET_KEY", "aible-os-dev-secret-key-change-in-production")

if os.getenv("AIBLE_APPS_DIR"):
    APPS_DIR = os.getenv("AIBLE_APPS_DIR")
elif _RESOURCES_DIR:
    APPS_DIR = os.path.join(_RESOURCES_DIR, "apps")
else:
    APPS_DIR = os.path.join(_BASE_DIR, "..", "apps")


def get_public_settings() -> dict:
    """Read settings fresh from config file each time (not cached on startup)"""
    current_api_key = _get_setting("LLM_API_KEY", "")
    current_base_url = _get_setting("LLM_BASE_URL", "https://open.bigmodel.cn/api/paas/v4")
    current_model = _get_setting("LLM_MODEL", "glm-4-plus")
    return {
        "llm_configured": bool(current_api_key),
        "llm_api_key": current_api_key,  # return masked for UI display (frontend shows as ****)
        "llm_base_url": current_base_url,
        "llm_model": current_model,
        "settings_path": _SETTINGS_PATH,
    }


def save_user_settings(llm_api_key: str, llm_base_url: str, llm_model: str) -> dict:
    data = {
        "LLM_API_KEY": llm_api_key.strip(),
        "LLM_BASE_URL": llm_base_url.strip() or "https://open.bigmodel.cn/api/paas/v4",
        "LLM_MODEL": llm_model.strip() or "glm-4-plus",
    }
    with open(_SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return {
        "saved": True,
        "settings_path": _SETTINGS_PATH,
        "llm_configured": bool(data["LLM_API_KEY"]),
        "llm_api_key": data["LLM_API_KEY"],
        "llm_base_url": data["LLM_BASE_URL"],
        "llm_model": data["LLM_MODEL"],
    }
