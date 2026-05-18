#!/usr/bin/env python3
"""Aible OS Backend Entry Point"""
import sys, os, argparse

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

# Find apps directory
_apps = os.environ.get("AIBLE_APPS_DIR", "")
if not _apps or not os.path.isdir(os.path.join(_apps, "built-in")):
    _apps = os.path.join(os.path.dirname(_DIR), "apps")  # Resources/apps
if _apps and os.path.isdir(os.path.join(_apps, "built-in")):
    os.environ["AIBLE_APPS_DIR"] = _apps

from main import app
import uvicorn

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--host", default="0.0.0.0")
    args = p.parse_args()
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")