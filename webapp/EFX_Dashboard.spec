# -*- mode: python ; coding: utf-8 -*-
import shutil
import os
import glob
import zipfile

# Read the version number from version.txt
def read_version():
    with open("data/version.txt") as f:
        return f.read().strip()

__version__ = read_version()

a = Analysis(
    ['EFX_Dashboard.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('app.py', '.'),
        ('utils.py', '.'),
        ('menu.py', '.'),
        ('pages/*', 'pages'),
    ],
    hiddenimports=['streamlit'],
    hookspath=[os.path.abspath("hooks")],
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
    [],
    exclude_binaries=True,
    name='EFX_Dashboard',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='EFX_Dashboard',
)

# Post-processing hook to copy additional files or folders
def copy_additional_files():
    dist_dir = os.path.join(os.getcwd(), 'dist', f"EFX_Dashboard")
    
    # Define the zip filename
    temp_zip_filename = f"EFX_Dashboard_{__version__}.zip"
    
    # Delete any existing zip files in the dist directory that match the filename
    existing_zip_file = glob.glob(os.path.join(dist_dir, temp_zip_filename))
    for zip_file in existing_zip_file:
        os.remove(zip_file)
    
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

    # Create a zip file of the dist directory
    final_zip_filepath = os.path.join(os.getcwd(), 'dist', temp_zip_filename)

    with zipfile.ZipFile(final_zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dist_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, dist_dir))

# Call the post-processing function
copy_additional_files()