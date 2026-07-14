# -*- mode: python ; coding: utf-8 -*-
# EZ_YT-DLP.spec
#
# Build with:
#   pyinstaller EZ_YT-DLP.spec
#
# Subsystem version 6.0 (Vista+) is patched automatically after the build.

# -*- mode: python ; coding: utf-8 -*-
# EZ_YT-DLP.spec
#
# Build with:
#   pyinstaller EZ_YT-DLP.spec
#
# Subsystem version 6.0 (Vista+) is patched automatically after the build.
#
# NOTE: We deliberately do NOT use collect_all('PySide6') here. That forces
# PyInstaller to bundle the entire PySide6 package -- every Qt module,
# including QtWebEngine (an embedded Chromium build), Qt3D, QtMultimedia,
# QtSql, QtBluetooth, etc. -- regardless of what the app actually imports.
# PyInstaller ships its own PySide6 hooks that automatically detect and
# bundle only the submodules referenced in download.py (QtCore, QtGui,
# QtWidgets), so nothing extra needs to be declared here.

block_cipher = None

a = Analysis(
    ['download.py'],
    pathex=[],
    binaries=[
        ('yt-dlp.exe',   '.'),  # extracted to _MEIPASS root at runtime
        ('ffmpeg.exe',   '.'),
        ('ffprobe.exe',  '.'),
    ],
    datas=[('icon.ico', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    # Belt-and-suspenders: explicitly exclude the heavyweight Qt modules the
    # app doesn't use, in case a future dependency accidentally pulls one in
    # as a transitive import.
    excludes=[
        'PySide6.QtWebEngineCore',
        'PySide6.QtWebEngineWidgets',
        'PySide6.QtWebEngineQuick',
        'PySide6.QtQml',
        'PySide6.QtQuick',
        'PySide6.QtQuick3D',
        'PySide6.QtQuickWidgets',
        'PySide6.QtQuickControls2',
        'PySide6.QtMultimedia',
        'PySide6.QtMultimediaWidgets',
        'PySide6.QtSql',
        'PySide6.QtBluetooth',
        'PySide6.QtNfc',
        'PySide6.QtSerialPort',
        'PySide6.QtSerialBus',
        'PySide6.QtSensors',
        'PySide6.QtPositioning',
        'PySide6.QtLocation',
        'PySide6.QtCharts',
        'PySide6.QtDataVisualization',
        'PySide6.QtGraphs',
        'PySide6.QtGraphsWidgets',
        'PySide6.Qt3DCore',
        'PySide6.Qt3DRender',
        'PySide6.Qt3DAnimation',
        'PySide6.Qt3DExtras',
        'PySide6.Qt3DInput',
        'PySide6.Qt3DLogic',
        'PySide6.QtPdf',
        'PySide6.QtPdfWidgets',
        'PySide6.QtHelp',
        'PySide6.QtHttpServer',
        'PySide6.QtRemoteObjects',
        'PySide6.QtScxml',
        'PySide6.QtStateMachine',
        'PySide6.QtSpatialAudio',
        'PySide6.QtTest',
        'PySide6.QtTextToSpeech',
        'PySide6.QtUiTools',
        'PySide6.QtWebChannel',
        'PySide6.QtWebSockets',
        'PySide6.QtWebView',
        'PySide6.QtDesigner',
        'PySide6.QtOpenGL',
        'PySide6.QtOpenGLWidgets',
        'PySide6.QtNetworkAuth',
        'PySide6.QtDBus',
        'PySide6.QtAxContainer',
        'PySide6.QtAsyncio',
    ],
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
    upx=True,                  # set to False if you don't have UPX installed
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',           # icon embedded here
)

