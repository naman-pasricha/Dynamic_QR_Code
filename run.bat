@echo off
echo Starting QRFlow Dynamic QR Code Generator...
echo Checking dependencies...
python -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Error installing dependencies. Please ensure Python is installed and in your PATH.
    pause
    exit /b
)
echo Starting Flask Server...
python app.py
pause
