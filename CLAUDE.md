# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

FF_ytdl is a Firefox extension that adds a "Download with yt-dlp" context menu item on videos, links, and pages. It launches yt-dlp.exe locally via a native messaging host.

## Architecture

- `extension/` — Firefox WebExtension (Manifest V2)
  - `manifest.json` — extension manifest with `contextMenus` and `nativeMessaging` permissions
  - `background.js` — creates the context menu item and sends the URL to the native host
- `host/` — Native messaging bridge (Python)
  - `ff_ytdl.py` — reads URL from the extension via stdin (native messaging protocol), finds and launches yt-dlp.exe in a new console window
  - `install.bat` — generates `ff_ytdl.bat` + `ff_ytdl.json`, registers the host in `HKCU\Software\Mozilla\NativeMessagingHosts\ff_ytdl`

## Data flow

Extension context menu click → `sendNativeMessage("ff_ytdl", {url})` → Firefox launches `ff_ytdl.bat` → Python reads 4-byte length + JSON from stdin → `subprocess.Popen([yt-dlp, url], CREATE_NEW_CONSOLE)`

## Setup

1. Run `host\install.bat` (requires Python in PATH)
2. Load extension via `about:debugging#/runtime/this-firefox` → "Load Temporary Add-on" → select `extension\manifest.json`

## Dependencies

- Python 3
- yt-dlp.exe (searched in PATH, then `%PROGRAMFILES%\yt-dlp.exe`, then `%PROGRAMFILES%\yt-dlp\yt-dlp.exe`)
- Firefox 55+
