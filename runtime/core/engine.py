import json
import sys
import os
from typing import AsyncGenerator

class AppEngine:
    """AI App 执行引擎"""
    
    def __init__(self):
        self._load_config()
    
    def _load_config(self):
        """每次调用时从最新配置读取，不缓存"""
        from config import _get_setting
        self.llm_api_key = _get_setting("LLM_API_KEY", "")
        self.llm_base_url = _get_setting("LLM_BASE_URL", "https://open.bigmodel.cn/api/paas/v4")
        self.llm_model = _get_setting("LLM_MODEL", "glm-4-plus")
    
    def refresh(self):
        """外部主动刷新配置（保存设置后调用）"""
        self._load_config()
    
    async def run_app(
        self, 
        app_id: str, 
        app_entry: str, 
        app_dir: str,
        message: str,
        history: list[dict] = None
    ) -> AsyncGenerator[str, None]:
        """运行 AI App，返回流式响应"""
        
        if history is None:
            history = []
            
        # 构建提示
        system_prompt = self._get_system_prompt(app_id, app_dir)
        messages = [{"role": "system", "content": system_prompt}]
        
        for h in history[-10:]:  # 最多保留 10 轮历史
            messages.append(h)
        
        messages.append({"role": "user", "content": message})
        
        # 调用 LLM
        async for chunk in self._call_llm(messages):
            yield chunk
    
    def _get_system_prompt(self, app_id: str, app_dir: str) -> str:
        """从 App 目录加载系统提示"""
        prompt_file = os.path.join(app_dir, "prompt.txt")
        manifest_file = os.path.join(app_dir, "manifest.yaml")
        
        if os.path.exists(prompt_file):
            with open(prompt_file, "r") as f:
                return f.read()
        else:
            return f"你是一个 AI 助手，擅长处理 {app_id} 相关任务。"
    
    async def _call_llm(self, messages: list) -> AsyncGenerator[str, None]:
        """调用 LLM API（流式）"""
        import httpx
        
        headers = {
            "Authorization": f"Bearer {self.llm_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.llm_model,
            "messages": messages,
            "stream": True,
            "temperature": 0.7,
            "max_tokens": 2048
        }
        
        url = f"{self.llm_base_url}/chat/completions"
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream("POST", url, json=payload, headers=headers) as response:
                    if response.status_code != 200:
                        error_text = await response.aread()
                        yield f"⚠️ API 调用失败 ({response.status_code}): {error_text[:200]}"
                        return
                    
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data_str = line[6:].strip()
                            if data_str == "[DONE]":
                                break
                            try:
                                data = json.loads(data_str)
                                choices = data.get("choices", [])
                                if choices:
                                    delta = choices[0].get("delta", {})
                                    content = delta.get("content", "")
                                    if content:
                                        yield content
                            except json.JSONDecodeError:
                                continue
        except Exception as e:
            yield f"⚠️ 连接错误: {str(e)}"
            # 如果 API 不可用，用模拟回复
            yield f"\n\n---\n*💡 提示：当前 LLM API 未配置或连接失败。如需真实 AI 回复，请在设置中配置 LLM API。*"


# Global engine instance, shared by chat and settings modules
engine = AppEngine()
