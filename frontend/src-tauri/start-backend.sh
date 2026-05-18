#!/bin/bash
# Aible OS Backend Launcher (Sidecar for Tauri)
# Uses the bundled venv in Resources/venv/

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONTENTS_DIR="$(dirname "$SCRIPT_DIR")"
RESOURCES_DIR="$CONTENTS_DIR/Resources"
RUNTIME_DIR="$RESOURCES_DIR/runtime"
APPS_DIR="$RESOURCES_DIR/apps"
VENV_DIR="$RESOURCES_DIR/venv"

# Determine which python to use from bundled venv
PYTHON=""
if [ -f "$VENV_DIR/bin/python3" ]; then
    PYTHON="$VENV_DIR/bin/python3"
elif [ -f "$VENV_DIR/bin/python" ]; then
    PYTHON="$VENV_DIR/bin/python"
fi

# Fallback: try system python only if bundled venv is not found
if [ -z "$PYTHON" ]; then
    echo "Bundled venv not found at $VENV_DIR, falling back to system python3" >&2
    for py in python3 /usr/bin/python3 /usr/local/bin/python3; do
        if command -v "$py" &>/dev/null; then
            PYTHON="$py"
            break
        fi
    done
fi

if [ -z "$PYTHON" ]; then
    echo "Error: python3 not found" >&2
    exit 1
fi

# Ensure greenlet is available in the venv (Tauri sometimes misses .so files during bundle)
if ! "$PYTHON" -c "import greenlet" 2>/dev/null; then
    echo "greenlet not found, installing..." >&2
    pip3 install greenlet 2>/dev/null || "$PYTHON" -m pip install greenlet 2>/dev/null || true
fi

export AIBLE_APPS_DIR="$APPS_DIR"
export AIBLE_RUNTIME_DIR="$RUNTIME_DIR"

exec "$PYTHON" "$RUNTIME_DIR/standalone.py" --port 8765