# build_engine_python.ps1
# Chay file nay tai thu muc goc project Python, noi co engine.py
# Vi du: C:\Users\3601183\Documents\Python\new_tool_auto_report

$ErrorActionPreference = "Stop"

Write-Host "=== BUILD ENGINE PYTHON ===" -ForegroundColor Cyan
Write-Host "Working dir: $(Get-Location)"

if (-not (Test-Path ".\engine.py")) {
    throw "Khong tim thay .\engine.py. Hay chay script nay tai thu muc goc project Python."
}

if (-not (Test-Path ".\Config")) {
    throw "Khong tim thay folder .\Config. Ban noi folder config ten la Config, hay dat dung: .\Config\config.yml"
}

# Clean output cu
Remove-Item ".\build" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item ".\dist" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item ".\EnginePython\*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item ".\EnginePython.spec" -Force -ErrorAction SilentlyContinue

# Tao folder output cuoi
New-Item -ItemType Directory -Path ".\EnginePython" -Force | Out-Null

# Build bang uv + PyInstaller
uv run pyinstaller `
  --noconfirm `
  --clean `
  --onedir `
  --name EnginePython `
  --console `
  --collect-binaries polars `
  --collect-data polars `
  --collect-all fastexcel `
  --collect-submodules win32com `
  --hidden-import pythoncom `
  --hidden-import pywintypes `
  --hidden-import win32timezone `
  --hidden-import win32event `
  --hidden-import win32con `
  --hidden-import win32com.client `
  --hidden-import xlwings `
  --hidden-import yaml `
  --hidden-import msoffcrypto `
  --hidden-import pydantic `
  --exclude-module polars.testing `
  --exclude-module hypothesis `
  --exclude-module fastapi `
  --exclude-module starlette `
  --exclude-module anyio `
  --exclude-module pygame `
  --exclude-module keyboard `
  --exclude-module pynput `
  --exclude-module pywinauto `
  --exclude-module rich `
  --exclude-module questionary `
  --exclude-module watchdog `
  --exclude-module prompt_toolkit `
  --exclude-module pygments `
  .\engine.py

# Copy output tu dist ve folder EnginePython final
Copy-Item ".\dist\EnginePython\*" ".\EnginePython" -Recurse -Force

# Copy folder Config vao chung cho voi exe
# Ket qua: .\EnginePython\Config\config.yml
Copy-Item ".\Config" ".\EnginePython\Config" -Recurse -Force

Write-Host "" 
Write-Host "=== DONE ===" -ForegroundColor Green
Write-Host "Exe:    .\EnginePython\EnginePython.exe"
Write-Host "Config: .\EnginePython\Config"
Write-Host "Test config exists:"
Test-Path ".\EnginePython\Config\config.yml"
