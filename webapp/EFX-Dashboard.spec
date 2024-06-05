# -*- mode: python ; coding: utf-8 -*-
import shutil
import os
import glob

a = Analysis(
    ['EFX-Dashboard.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('app.py','.'),
        ('utils.py','.'),
        ('menu.py','.'),
        ('pages/*','pages'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='EFX-Dashboard',
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


# Post-processing hook to copy additional files or folders
def copy_additional_files():
    dist_dir = os.path.join(os.getcwd(), 'dist')
    
    # Define the source and destination paths
    additional_files = [
        ('data', os.path.join(dist_dir, 'data')),
        ('.streamlit', os.path.join(dist_dir, '.streamlit')),
    ]
    
    for src, dst in additional_files:
        if os.path.isdir(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy(src, dst)

# Call the post-processing function
copy_additional_files()