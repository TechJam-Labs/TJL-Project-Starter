@echo off
setlocal enabledelayedexpansion

:: TJL Project Setup Tool - Windows Installer
:: Author: Ben Adenle
:: Email: ben@techjamlabs.com

:: Colors for output
set "BLUE=[94m"
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "RESET=[0m"

:: Header
echo %BLUE%=== TJL Project Setup Tool Installer ===%RESET%
echo.

:: Check Python installation
python --version > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo %RED%Error: Python is not installed or not in PATH%RESET%
    echo Please install Python 3.6 or higher from https://python.org
    exit /b 1
)
echo %GREEN%√ Python is installed%RESET%

:: Check Git installation
git --version > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo %RED%Error: Git is not installed or not in PATH%RESET%
    echo Please install Git from https://git-scm.com
    exit /b 1
)
echo %GREEN%√ Git is installed%RESET%

:: Create installation directory
set "INSTALL_DIR=%USERPROFILE%\TJLTools"
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
    echo %GREEN%√ Created installation directory%RESET%
) else (
    echo %YELLOW%! Installation directory already exists%RESET%
)

:: Copy files
echo %BLUE%Copying files...%RESET%
copy /Y "tjl-project.py" "%INSTALL_DIR%\" > nul
if %ERRORLEVEL% neq 0 (
    echo %RED%Error: Failed to copy tjl-project.py%RESET%
    exit /b 1
)

:: Create batch file
set "BATCH_FILE=%INSTALL_DIR%\tjl-project.bat"
echo @echo off > "%BATCH_FILE%"
echo python "%INSTALL_DIR%\tjl-project.py" %%* >> "%BATCH_FILE%"
echo %GREEN%√ Created batch file%RESET%

:: Add to PATH
echo %BLUE%Adding to PATH...%RESET%
set "PATH_KEY=HKCU\Environment"
set "PATH_NAME=Path"
for /f "tokens=2*" %%a in ('reg query "%PATH_KEY%" /v "%PATH_NAME%" 2^>nul') do set "CURRENT_PATH=%%b"

if not "!CURRENT_PATH!" == "" (
    echo !CURRENT_PATH! | find /i "%INSTALL_DIR%" > nul
    if !ERRORLEVEL! neq 0 (
        setx PATH "!CURRENT_PATH!;%INSTALL_DIR%"
        if !ERRORLEVEL! neq 0 (
            echo %RED%Error: Failed to update PATH%RESET%
            exit /b 1
        )
    ) else (
        echo %YELLOW%! Directory already in PATH%RESET%
    )
) else (
    setx PATH "%INSTALL_DIR%"
)
echo %GREEN%√ Updated PATH%RESET%

:: Create PowerShell profile integration
set "PS_PROFILE=%USERPROFILE%\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"
if not exist "%USERPROFILE%\Documents\WindowsPowerShell" mkdir "%USERPROFILE%\Documents\WindowsPowerShell"

echo function New-TJLProject { >> "%PS_PROFILE%"
echo     param($projectName) >> "%PS_PROFILE%"
echo     python "%INSTALL_DIR%\tjl-project.py" $projectName $args >> "%PS_PROFILE%"
echo } >> "%PS_PROFILE%"
echo Set-Alias tjl New-TJLProject >> "%PS_PROFILE%"
echo %GREEN%√ Added PowerShell integration%RESET%

echo.
echo %GREEN%Installation complete!%RESET%
echo.
echo Please restart your terminal or command prompt to use the tool.
echo.
echo Usage:
echo   tjl-project my-project
echo   tjl my-project ^(in PowerShell^)
echo.
echo For help:
echo   tjl-project --help
echo.

endlocal