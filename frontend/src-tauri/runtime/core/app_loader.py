import os
import yaml
from typing import Optional

APP_MANIFEST_FILE = "manifest.yaml"
APP_PROMPT_FILE = "prompt.txt"
APP_SCRIPT_FILE = "app.py"

class AppInfo:
    def __init__(self, app_id: str, name: str, tagline: str, description: str,
                 icon: str, category: str, color: str, author: str,
                 app_dir: str, capabilities: list = None):
        self.app_id = app_id
        self.name = name
        self.tagline = tagline
        self.description = description
        self.icon = icon
        self.category = category
        self.color = color
        self.author = author
        self.app_dir = app_dir
        self.capabilities = capabilities or []

class AppLoader:
    """加载 AI App 定义"""
    
    def __init__(self, apps_dir: str = None):
        # 优先使用环境变量中的路径
        self.apps_dir = apps_dir or os.environ.get("AIBLE_APPS_DIR", "")
        if not self.apps_dir:
            # 默认: 相对于 runtime/ 的上级目录的 apps/
            self.apps_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "apps"
            )
    
    def list_apps(self) -> list[AppInfo]:
        """扫描 apps 目录下所有 App"""
        apps = []
        builtin_dir = os.path.join(self.apps_dir, "built-in")
        
        if not os.path.exists(builtin_dir):
            return apps
        
        for entry in os.listdir(builtin_dir):
            app_dir = os.path.join(builtin_dir, entry)
            if not os.path.isdir(app_dir):
                continue
            
            manifest = self._load_manifest(app_dir)
            if manifest:
                manifest["app_dir"] = app_dir
                manifest["app_id"] = manifest.get("app_id", entry)
                apps.append(AppInfo(**manifest))
        
        return apps
    
    def get_app(self, app_id: str) -> Optional[AppInfo]:
        """获取单个 App"""
        for app in self.list_apps():
            if app.app_id == app_id:
                return app
        return None
    
    def _load_manifest(self, app_dir: str) -> Optional[dict]:
        """加载 App 的 manifest.yaml"""
        manifest_path = os.path.join(app_dir, APP_MANIFEST_FILE)
        if not os.path.exists(manifest_path):
            return None
        
        with open(manifest_path, "r") as f:
            manifest = yaml.safe_load(f)
        
        # 确保必填字段
        manifest["app_dir"] = app_dir
        
        # 可选的 prompt 内容
        prompt_path = os.path.join(app_dir, APP_PROMPT_FILE)
        if not os.path.exists(prompt_path):
            # 从 manifest 的 description 生成默认 prompt
            with open(prompt_path, "w") as f:
                f.write(f"你是一个 AI 助手，专门处理 {manifest.get('name', app_dir)} 相关任务。\n\n{manifest.get('description', '')}")
        
        return manifest
