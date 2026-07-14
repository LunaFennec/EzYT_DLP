# -*- mode: python ; coding: utf-8 -*-
# EZ_YT-DLP.spec
#
# Build with:
#   pyinstaller EZ_YT-DLP.spec
#
# Subsystem version 6.0 (Vista+) is patched automatically after the build.

from PyInstaller.utils.hooks import collect_all

block_cipher = None

pyside6_binaries, pyside6_datas, pyside6_hiddenimports = collect_all('PySide6')

a = Analysis(
    ['download.py'],
    pathex=[],
    binaries=[
        ('yt-dlp.exe',   '.'),  # extracted to _MEIPASS root at runtime
        ('ffmpeg.exe',   '.'),
        ('ffprobe.exe',  '.'),
    ] + pyside6_binaries,
    datas=[('icon.ico', '.')] + pyside6_datas,
    hiddenimports=pyside6_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='EZ_YT-DLP',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
)

