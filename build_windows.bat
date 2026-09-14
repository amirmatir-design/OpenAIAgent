@echo off
setlocal
echo Installing dependencies...
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
echo Building Desktop AI Agent...
py -m PyInstaller --noconfirm --clean --onefile --windowed --name DesktopAIAgent app.py
echo.
echo Build complete: dist\DesktopAIAgent.exe
pause
