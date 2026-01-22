@echo off
setlocal

echo 🚀 Start py-xygraph...

REM 1. Check Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.
    pause
    exit /b 1
)

python --version

REM 2. Check and Create Virtual Environment
set VENV_DIR=myenv

if not exist "%VENV_DIR%" (
    echo 📦 Creating virtual environment...
    python -m venv %VENV_DIR%
    echo ✅ Virtual environment created.
) else (
    echo ✅ Virtual environment already exists.
)

REM 3. Activate Virtual Environment
call %VENV_DIR%\Scripts\activate

REM 4. Install Dependencies
echo 📥 Checking dependencies...

if not exist "deps.txt" (
    echo matplotlib > deps.txt
    echo numpy >> deps.txt
)

pip install -r deps.txt

REM 5. Run Application
echo 🎨 Launching application...
python main.py

pause
