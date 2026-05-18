from fastapi import APIRouter
from pydantic import BaseModel

from config import get_public_settings, save_user_settings
from core.engine import engine as app_engine

router = APIRouter(prefix="/api/settings", tags=["settings"])


class SaveSettingsRequest(BaseModel):
    llm_api_key: str = ""
    llm_base_url: str = "https://open.bigmodel.cn/api/paas/v4"
    llm_model: str = "glm-4-plus"


@router.get("")
async def get_settings():
    return get_public_settings()


@router.post("")
async def save_settings(req: SaveSettingsRequest):
    result = save_user_settings(
        llm_api_key=req.llm_api_key,
        llm_base_url=req.llm_base_url,
        llm_model=req.llm_model,
    )
    # Refresh engine with new config immediately — no restart needed
    app_engine.refresh()
    return result
