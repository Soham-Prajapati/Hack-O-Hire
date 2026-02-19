@echo off
setlocal enabledelayedexpansion

REM ============================================================
REM SAR Narrative Generator — Windows Startup Script
REM ============================================================

echo.
echo ============================================================
echo 🚀 Launching SAR Generator System
echo ============================================================
echo.

REM 1. Check for Virtual Environment
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo Please run 'setup.bat all' first.
    pause
    exit /b
)

REM 2. Start Backend in a new window
echo 🐍 Starting Backend API (Port 8000)...
start "SAR Backend" cmd /k ".venv\Scripts\activate.bat && cd backend && uvicorn app.main:app --reload --port 8000"

REM 3. Wait a bit for backend to boot
echo    Waiting 5 seconds for backend...
timeout /t 5 /nobreak >nul

REM 4. Start Frontend in a new window
echo 🎨 Starting Frontend Dashboard (Port 8501)...
start "SAR Frontend" cmd /k ".venv\Scripts\activate.bat && cd frontend && streamlit run app.py"

echo.
echo ============================================================
echo ✅ System Launch Initiated!
echo.
echo - Backend Docs: http://localhost:8000/docs
echo - Frontend UI:  http://localhost:8501
echo.
echo Keep this window open or close it, the servers are running in separate windows.
echo ============================================================
pause
