@echo off
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is required but not found in PATH.
    pause
    exit /b 1
)

set "HOST_DIR=%~dp0"

:: Create launcher batch file
(
echo @echo off
echo python "%%~dp0ff_ytdl.py"
) > "%HOST_DIR%ff_ytdl.bat"

:: Build escaped path for JSON
set "BAT_PATH=%HOST_DIR%ff_ytdl.bat"
set "BAT_ESC=%BAT_PATH:\=\\%"

:: Create native messaging manifest
(
echo {"name":"ff_ytdl","description":"Launch yt-dlp","path":"%BAT_ESC%","type":"stdio","allowed_extensions":["ff-ytdl@local"]}
) > "%HOST_DIR%ff_ytdl.json"

:: Register with Firefox
reg add "HKCU\Software\Mozilla\NativeMessagingHosts\ff_ytdl" /ve /d "%HOST_DIR%ff_ytdl.json" /f

echo.
echo Installed successfully.
echo.
echo To load the extension in Firefox:
echo   1. Go to about:debugging#/runtime/this-firefox
echo   2. Click "Load Temporary Add-on..."
echo   3. Select manifest.json from the extension folder
echo.
pause
