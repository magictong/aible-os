#!/bin/bash
# Build the bundled venv for Aible OS
# Run from aible-os/root directory: bash scripts/build-venv.sh

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
RUNTIME_DIR="$ROOT_DIR/runtime"
VENV_TARGET="$ROOT_DIR/frontend/src-tauri/resources/venv"

echo "=== Building bundled Python venv for Aible OS ==="
echo "Root:       $ROOT_DIR"
echo "Runtime:    $RUNTIME_DIR"
echo "Venv:       $VENV_TARGET"

# Clean old venv
rm -rf "$VENV_TARGET"

# Require python3.9+ (lowest that supports modern SQLAlchemy)
PYTHON=""
for py in python3.13 python3.12 python3.11 python3.10 python3.9 python3; do
    if ! command -v "$py" &>/dev/null; then continue; fi
    ver=$($py -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || true)
    if [ -z "$ver" ]; then continue; fi
    major=$(echo "$ver" | cut -d. -f1)
    minor=$(echo "$ver" | cut -d. -f2)
    if [ "$major" = "3" ] && [ "$minor" -ge 9 ]; then
        PYTHON="$py"
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo "Error: Python 3.9+ is required. Found:"
    for py in python3 python3.11 python3.12; do command -v "$py" && "$py" --version 2>/dev/null; done
    exit 1
fi

echo "Using: $($PYTHON --version)"

# Create venv
$PYTHON -m venv "$VENV_TARGET"
echo "Venv created at: $VENV_TARGET"

# Activate and install deps
source "$VENV_TARGET/bin/activate"

# Upgrade pip and install pinned deps
pip install --upgrade pip setuptools wheel

# Install from requirements.txt with pinned versions
echo "=== Installing Python dependencies ==="
pip install \
    fastapi==0.115.0 \
    uvicorn==0.30.6 \
    pydantic==2.9.2 \
    httpx==0.27.2 \
    python-dotenv==1.0.1 \
    sqlalchemy==2.0.35 \
    aiosqlite==0.20.0 \
    passlib==1.7.4 \
    python-jose==3.3.0 \
    pyyaml==6.0.2 \
    bcrypt==4.0.1 \
    sse-starlette==2.0.0 \
    greenlet==3.0.3

echo "=== Verifying import ==="
$PYTHON -c "
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from uvicorn import run
import sse_starlette
print('All imports OK')
"

echo "=== Venv size ==="
du -sh "$VENV_TARGET"

echo ""
echo "=== Build complete ==="
echo "Venv ready at: $VENV_TARGET"
echo "Next: run 'npx tauri build' in frontend/"