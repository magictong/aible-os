# Aible OS Backend Entry Point
# This file is used by PyInstaller as the single entry point
import sys
import os
import argparse

# Ensure the runtime directory is on the path
RUNTIME_DIR = os.path.dirname(os.path.abspath(__file__))
if RUNTIME_DIR not in sys.path:
    sys.path.insert(0, RUNTIME_DIR)

# Make sure apps directory can be found
APPS_DIR = os.path.join(os.path.dirname(RUNTIME_DIR), "apps")
if not os.path.exists(APPS_DIR):
    # When running as PyInstaller bundle, apps/ is next to the binary
    APPS_DIR = os.path.join(os.path.dirname(sys.executable), "apps")
    if not os.path.exists(APPS_DIR):
        APPS_DIR = os.path.join(RUNTIME_DIR, "apps")

os.environ["AIBLE_APPS_DIR"] = APPS_DIR
os.environ["AIBLE_RUNTIME_DIR"] = RUNTIME_DIR

from main import app

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--host", type=str, default="0.0.0.0")
    args = parser.parse_args()

    import uvicorn
    uvicorn.run("main:app", host=args.host, port=args.port, reload=False)