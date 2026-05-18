import sys
import os
import argparse

# 确保能找到模块
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager

from models import init_db
from api.auth import router as auth_router
from api.apps import router as apps_router
from api.chat import router as chat_router
from api.settings import router as settings_router

_STATIC_DIR = os.path.join(current_dir, "static")

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Aible OS API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(apps_router)
app.include_router(chat_router)
app.include_router(settings_router)

@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}

@app.get("/")
async def serve_spa():
    for d in [_STATIC_DIR, os.path.join(os.path.dirname(current_dir), "static")]:
        p = os.path.join(d, "index.html")
        if os.path.isfile(p):
            return FileResponse(p)
    from fastapi.responses import HTMLResponse
    return HTMLResponse("""<!DOCTYPE html><html><head><meta charset=\"UTF-8\"><title>Aible OS</title></head>
<body style=\"font-family:-apple-system,sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;background:#fff\">
<div style=\"text-align:center\"><h1>Aible OS</h1><p>静态文件未找到</p><p style=\"color:#999\">请检查 static/index.html</p></div>
</body></html>""")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--host", type=str, default="0.0.0.0")
    args = parser.parse_args()

    import uvicorn
    uvicorn.run("main:app", host=args.host, port=args.port, reload=False)
