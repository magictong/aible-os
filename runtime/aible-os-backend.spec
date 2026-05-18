# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = ['models', 'api.auth', 'api.apps', 'api.chat', 'core.app_loader', 'core.engine', 'core.session', 'models.app', 'sse_starlette', 'greenlet', 'aiosqlite', 'httpx', 'yaml', 'pydantic']
hiddenimports += collect_submodules('uvicorn')


a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=[('main.py', '.'), ('config.py', '.'), ('api', 'api'), ('core', 'core'), ('models', 'models')],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='aible-os-backend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
