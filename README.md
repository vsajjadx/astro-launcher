# Astro Launcher

A Windows desktop launcher for **PS5 Remote Play**, built with PyQt6.

## Features

- Game library view with cover art (IGDB / RAWG integration)
- Virtual gamepad passthrough (via `vgamepad`) so a physical controller is forwarded into Remote Play
- Raw HID controller access via `hidapi`
- Optional in-game FPS overlay (lightweight Tk-based overlay, embedded and extracted at runtime)
- Audio pipeline using `soundfile` / `opuslib` for low-latency sound handling
- Built-in helper to fetch the official Microsoft Visual C++ Redistributable from Microsoft's own servers (no third-party mirrors)
- Config export that automatically redacts sensitive fields (tokens, secrets, API keys) before sharing

## Project layout

```
ps5_launcher.py       # main application source
ps5_launcher.spec     # PyInstaller build spec (onedir Windows build)
requirements.txt      # Python dependencies
icon.ico, tray-icon.png, 1117123.png   # app/tray icons and artwork
hidapi.dll, hidapi.lib                 # native HID bindings used by the build
```

## Building from source (Windows)

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pyinstaller ps5_launcher.spec
```

The build output is a portable `PS5-Launcher` folder under `dist/` (onedir build, so native DLLs and Qt plugins stay next to the executable).

## Automated builds

This repo includes a GitHub Actions workflow (`.github/workflows/build.yml`) that builds the Windows executable on every push and uploads it as a downloadable artifact — no local Windows machine required. Check the **Actions** tab after pushing, or trigger it manually from there.

## Requirements

- Python 3.13+
- Windows 10/11 (the build targets Windows; PyQt6 + `hidapi` + `vgamepad` are Windows-oriented)
