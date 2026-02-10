# FF yt-dlp

Firefox extension that adds a "Download with yt-dlp" option to the right-click context menu on videos, links, and pages.

## How it works

The extension uses Firefox's native messaging API to launch `yt-dlp.exe` locally with the page URL. A Python-based native messaging host bridges the browser and the executable.

## Requirements

- Firefox 55+
- Python 3
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) (in PATH or `C:\Program Files`)

## Installation

### 1. Register the native messaging host

Run `host\install.bat`. This generates the native messaging manifest and registers it in the Windows registry.

### 2. Load the extension

1. Open Firefox and go to `about:debugging#/runtime/this-firefox`
2. Click **Load Temporary Add-on...**
3. Select `extension\manifest.json`

## Usage

Right-click on a video, link, or page and select **Download with yt-dlp**.

Downloaded files and logs are saved to `Downloads\yt-dlp\`.
