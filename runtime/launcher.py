#!/usr/bin/env python3
"""Aible OS Backend - Single Entry Point for PyInstaller"""
import sys, os, argparse

# CRITICAL: When running as PyInstaller bundle, _MEIPASS has our files
_BASE = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _BASE)

# Find & set apps directory
for _path in [
    os.environ.get("AIBLE_APPS_DIR", ""),
    os.path.join(_BASE, "apps"),
    os.path.join(os.path.dirname(_BASE), "apps"),
]:
    if _path and os.path.isdir(os.path.join(_path, "built-in")):
        os.environ["AIBLE_APPS_DIR"] = _path
        break

# Now imports will work because _BASE is on sys.path
from main import app
import uvicorn

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--host", default="0.0.0.0")
    args = p.parse_args()
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")