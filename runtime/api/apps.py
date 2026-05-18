from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func, select
from typing import Optional
import os

from models import get_session
from models.app import InstalledApp
from core.app_loader import AppLoader
from config import APPS_DIR, DATABASE_URL, LLM_API_KEY, LLM_BASE_URL, LLM_MODEL
from .auth import require_auth

router = APIRouter(prefix="/api/apps", tags=["apps"])
loader = AppLoader(APPS_DIR)

@router.get("/catalog")
async def list_catalog():
    """列出商店中所有可用的 App"""
    apps = loader.list_apps()
    return [
        {
            "app_id": a.app_id,
            "name": a.name,
            "tagline": a.tagline,
            "description": a.description,
            "icon": a.icon,
            "category": a.category,
            "color": a.color,
            "author": a.author,
            "is_builtin": True,
        }
        for a in apps
    ]

@router.get("/catalog/{app_id}")
async def get_catalog_app(app_id: str):
    """获取单个 App 详情"""
    app = loader.get_app(app_id)
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    return {
        "app_id": app.app_id,
        "name": app.name,
        "tagline": app.tagline,
        "description": app.description,
        "icon": app.icon,
        "category": app.category,
        "color": app.color,
        "author": app.author,
        "is_builtin": True,
    }

@router.get("/installed")
async def list_installed(user_id: int = Depends(require_auth)):
    """列出用户已安装的 App"""
    session = next(get_session())
    try:
        result = session.execute(select(InstalledApp).where(InstalledApp.user_id == user_id))
        installed = result.scalars().all()

        apps = []
        for inst in installed:
            app_info = loader.get_app(inst.app_id)
            if app_info:
                apps.append({
                    "id": inst.id,
                    "app_id": inst.app_id,
                    "display_name": inst.display_name or app_info.name,
                    "icon": app_info.icon,
                    "category": app_info.category,
                    "color": app_info.color,
                    "installed_at": inst.installed_at.isoformat() if inst.installed_at else "",
                })
        return apps
    finally:
        session.close()

@router.post("/install")
async def install_app(
    app_id: str,
    user_id: int = Depends(require_auth),
):
    """安装 App"""
    app_info = loader.get_app(app_id)
    if not app_info:
        raise HTTPException(status_code=404, detail="App not found")

    session = next(get_session())
    try:
        result = session.execute(
            select(InstalledApp).where(
                InstalledApp.user_id == user_id,
                InstalledApp.app_id == app_id
            )
        )
        if result.scalar_one_or_none():
            return {"status": "already_installed"}

        installed = InstalledApp(
            user_id=user_id,
            app_id=app_id,
            display_name=app_info.name,
        )
        session.add(installed)
        session.commit()
        return {"status": "ok", "message": f"{app_info.name} 安装成功"}
    finally:
        session.close()

@router.post("/uninstall")
async def uninstall_app(
    app_id: str,
    user_id: int = Depends(require_auth),
):
    """卸载 App"""
    session = next(get_session())
    try:
        result = session.execute(
            select(InstalledApp).where(
                InstalledApp.user_id == user_id,
                InstalledApp.app_id == app_id
            )
        )
        inst = result.scalar_one_or_none()
        if not inst:
            return {"status": "not_installed"}

        session.delete(inst)
        session.commit()
        return {"status": "ok", "message": "卸载成功"}
    finally:
        session.close()

@router.get("/diagnostics")
async def diagnostics():
    """返回运行时诊断信息（屏蔽敏感值）"""
    built_in_dir = os.path.join(APPS_DIR, "built-in")
    builtin_entries = []
    if os.path.isdir(built_in_dir):
        builtin_entries = sorted([
            name for name in os.listdir(built_in_dir)
            if os.path.isdir(os.path.join(built_in_dir, name))
        ])

    session = next(get_session())
    try:
        installed_count = session.scalar(select(func.count()).select_from(InstalledApp)) or 0
    except Exception as e:
        installed_count = f"error: {e}"
    finally:
        session.close()

    catalog_apps = loader.list_apps()

    return {
        "database_url": DATABASE_URL,
        "apps_dir": APPS_DIR,
        "built_in_dir": built_in_dir,
        "built_in_exists": os.path.isdir(built_in_dir),
        "built_in_entries": builtin_entries,
        "catalog_count": len(catalog_apps),
        "catalog_ids": [a.app_id for a in catalog_apps],
        "installed_count": installed_count,
        "llm": {
            "configured": bool(LLM_API_KEY),
            "base_url": LLM_BASE_URL,
            "model": LLM_MODEL,
        },
    }