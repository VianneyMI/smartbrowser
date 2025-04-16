# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_data_files

gradio_client_datas = collect_data_files('gradio_client')
gradio_datas = collect_data_files('gradio')

a = Analysis(
    ['src\\smartbrowser\\main.py'],
    pathex=['venv/Scripts/Lib'],
    binaries=[],
    datas=gradio_client_datas + gradio_datas,
    hiddenimports=['pydantic', 'pydantic-core', 'pydantic.deprecated.decorator', 'gradio', 'gradio_client'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
    module_collection_mode={
        'gradio': 'py',  # Collect gradio package as source .py files
    }
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
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
