@echo off
echo Create virtual environment
python -m venv venv

if errorlevel 1 (
    echo Failed to create virtual environment.
    exit /b 1
)

echo Install requirements in virtual environment
venv\Scripts\pip install -r requirements.txt

if errorlevel 1 (
    echo Failed to install requirements.
    exit /b 1
)

echo Run server
venv\Scripts\python run.py

if errorlevel 1 (
    echo Server failed to start.
    exit /b 1
)

echo Server is running.
