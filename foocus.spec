# -*- mode: python ; coding: utf-8 -*-

import os
import glob
from PyInstaller.utils.hooks import collect_submodules

# === RECURSIVELY COLLECT RESOURCE FILES ===
def collect_data(folder):
    datas = []
    for path in glob.glob(os.path.join(folder, "**", "*.*"), recursive=True):
        if os.path.isfile(path):
            # Ensure subfolder structure is preserved
            datas.append((path, os.path.dirname(path)))
    return datas

# === RESOURCES TO INCLUDE ===
resource_files = (
    collect_data("resources/audio") +
    collect_data("resources/icons") +
    collect_data("resources/logos") +
    collect_data("resources/models") +
    [("style.qss", ".")] 
)

# === HIDDEN IMPORTS (if needed) ===
# hiddenimports = collect_submodules('PySide6')

# === MAIN ===
block_cipher = None

a = Analysis(
    ['foocus.py'],                   # Entry point of your app
    pathex=[],
    binaries=[],
    datas=resource_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='foocus',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/logos/foocus_logo.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='foocus'
)





