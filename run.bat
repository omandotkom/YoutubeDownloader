@echo off
TITLE YouTube Downloader
CLS

echo ========================================================
echo       YouTube Downloader - Starting Up
echo ========================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not found. Please install Python and add it to PATH.
    pause
    exit
)

echo [1/2] Checking and installing dependencies...
pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Could not install dependencies. Trying to run anyway...
)

echo.
echo [2/2] Starting Flask Server...
echo.
echo ========================================================
echo    Open this URL in your browser:
echo    http://127.0.0.1:5000
echo.
echo    Press CTRL+C to stop the server.
echo ========================================================
echo.

python app.py

pause
