# -*- mode: python ; coding: utf-8 -*-
"""Windows onedir build for PS5 Launcher.

The output is a portable folder rather than a single compressed executable.
That keeps native DLLs and Qt plugins visible beside the executable and makes
the Inno Setup installer reliable.

This spec builds the single merged ps5_launcher.py source and the native
launcher assets.
"""

import os
from PyInstaller.utils.hooks import collect_all

spec_dir = os.path.abspath(os.path.dirname(SPEC))

vg_datas, vg_binaries, vg_hiddenimports = collect_all("vgamepad")

# fps_overlay.py -- embedded inside ps5_launcher.py as a gzip+base64 blob
# and only ever extracted to disk and exec'd at runtime -- imports
# tkinter. PyInstaller's static analysis never sees inside that blob, so
# without this explicit collect_all(), tkinter (and its bundled Tcl/Tk
# DLLs and library data) would be left out of the build entirely, and the
# overlay would crash with "ModuleNotFoundError: No module named
# 'tkinter'" the first time it's launched.
tk_datas, tk_binaries, tk_hiddenimports = collect_all("tkinter")

# collect_all() pulls in tkinter's bundled test suite and demo data
# (tkinter.test, idlelib, turtledemo) along with the actual Tcl/Tk
# runtime - none of which fps_overlay.py needs. Dropping them here
# means PyInstaller's COLLECT step doesn't have to copy that dead
# weight into the output on every build.
_TK_BLOAT_MARKERS = ("tkinter" + os.sep + "test", "idlelib", "turtledemo")
tk_datas = [d for d in tk_datas if not any(m in d[0] for m in _TK_BLOAT_MARKERS)]
tk_binaries = [b for b in tk_binaries if not any(m in b[0] for m in _TK_BLOAT_MARKERS)]
tk_hiddenimports = [
    h for h in tk_hiddenimports
    if not (h.startswith("tkinter.test") or h.startswith("idlelib") or h.startswith("turtledemo"))
]

hid_binaries = []
hidapi_dll = os.path.join(spec_dir, "hidapi.dll")
if os.path.exists(hidapi_dll):
    hid_binaries.append((hidapi_dll, "."))

app_datas = [
    (os.path.join(spec_dir, "1117123.png"), "."),
    (os.path.join(spec_dir, "icon.ico"), "."),
    (os.path.join(spec_dir, "tray-icon.png"), "."),
    (
        os.path.join(spec_dir, "icon_1785786411066_1786088752915.ico"),
        ".",
    ),
]

webengine_hiddenimports = [
    "PyQt6.QtWebEngine",
    "PyQt6.QtWebEngineCore",
    "PyQt6.QtWebEngineWidgets",
]

a = Analysis(
    [os.path.join(spec_dir, "ps5_launcher.py")],
    pathex=[spec_dir],
    binaries=vg_binaries + hid_binaries + tk_binaries,
    datas=vg_datas + app_datas + tk_datas,
    hiddenimports=vg_hiddenimports + tk_hiddenimports + webengine_hiddenimports + [
        "hid",
        "PIL",
        "pillow_avif",
        "opuslib",
        "scipy",
        "scipy.signal",
        "soundfile",
        "av",
        "yt_dlp",
        "tkinter",
        "tkinter.font",
        "tkinter.ttk",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    # None of these are imported by the launcher; excluding them keeps
    # PyInstaller's Analysis/COLLECT step from scanning and copying their
    # (often large) binaries and data files, which is a direct build-time
    # win independent of the final app's runtime behavior.
    excludes=[
        "PyQt6.QtBluetooth",
        "PyQt6.QtDesigner",
        "PyQt6.QtHelp",
        "PyQt6.QtNfc",
        "PyQt6.QtPositioning",
        "PyQt6.QtQml",
        "PyQt6.QtQuick",
        "PyQt6.QtQuick3D",
        "PyQt6.QtQuickWidgets",
        "PyQt6.QtSensors",
        "PyQt6.QtSerialPort",
        "PyQt6.QtSql",
        "PyQt6.QtTest",
        "PyQt6.QtPdf",
        "PyQt6.QtPdfWidgets",
        "matplotlib",
        "IPython",
        "notebook",
        "pytest",
    ],
    noarchive=False,
    optimize=0,
    cipher=None,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="PS5-Launcher",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(spec_dir, "icon.ico"),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name="PS5-Launcher",
)
