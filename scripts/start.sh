#!/bin/bash
# Aible OS - 启动脚本
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Aible OS 启动中 ==="

# 1. 安装后端依赖
echo "[1/3] 安装后端依赖..."
cd "$PROJECT_DIR/runtime"
pip3 install -r requirements.txt -q 2>/dev/null || true
pip3 install sse-starlette greenlet -q 2>/dev/null || true

# 2. 安装前端依赖
echo "[2/3] 安装前端依赖..."
cd "$PROJECT_DIR/frontend"
npm install --silent 2>/dev/null || npm install 2>&1 | tail -3

# 3. 启动服务
echo "[3/3] 启动服务..."
# 后端
cd "$PROJECT_DIR/runtime"
python3 -m uvicorn main:app --host 0.0.0.0 --port 8765 --reload &
BACKEND_PID=$!

# 前端
cd "$PROJECT_DIR/frontend"
npx next dev -p 3000 &
FRONTEND_PID=$!

echo ""
echo "=== Aible OS 已启动 ==="
echo "前端: http://localhost:3000"
echo "后端: http://localhost:8765"
echo "API 文档: http://localhost:8765/docs"
echo ""
echo "按 Ctrl+C 停止所有服务"
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" SIGINT SIGTERM
wait
