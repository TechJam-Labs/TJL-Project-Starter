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

:: Installation directories
set "INSTALL_DIR=%USERPROFILE%\TJLTools"
set "BIN_DIR=%INSTALL_DIR%\bin"
set "LIB_DIR=%INSTALL_DIR%\lib"
set "TEMPLATES_DIR=%INSTALL_DIR%\templates"
set "DOCS_DIR=%INSTALL_DIR%\docs"
set "COMPLETION_DIR=%INSTALL_DIR%\completion"

:: Header
echo %BLUE%=== TJL Project Setup Tool Installer ===%RESET%
echo.

:: Check administrative privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo %RED%Error: Administrative privileges required%RESET%
    echo Please run this installer as Administrator
    exit /b 1
)

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

:: Create installation directories
echo %BLUE%Creating installation directories...%RESET%
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
if not exist "%BIN_DIR%" mkdir "%BIN_DIR%"
if not exist "%LIB_DIR%" mkdir "%LIB_DIR%"
if not exist "%TEMPLATES_DIR%" mkdir "%TEMPLATES_DIR%"
if not exist "%DOCS_DIR%" mkdir "%DOCS_DIR%"
if not exist "%COMPLETION_DIR%" mkdir "%COMPLETION_DIR%"

:: Create template directories
echo %BLUE%Creating template directories...%RESET%
for %%t in (basic microservice webapp library) do (
    if not exist "%TEMPLATES_DIR%\%%t" (
        mkdir "%TEMPLATES_DIR%\%%t"
        echo %GREEN%√ Created template directory: %%t%RESET%
    )
)

:: Install Python dependencies
echo %BLUE%Installing Python dependencies...%RESET%
python -m pip install --upgrade pip
pip install colorama click jinja2 pyyaml

:: Copy files
echo %BLUE%Copying files...%RESET%

:: Copy main script
echo %BLUE%Copying main script...%RESET%
copy /Y "src\tjl-project.py" "%BIN_DIR%\tjl-project.py" > nul
if %ERRORLEVEL% neq 0 (
    echo %RED%Error: Failed to copy main script%RESET%
    echo Please ensure you're running the installer from the project root directory
    echo Current directory: %CD%
    echo Expected file: %CD%\src\tjl-project.py
    exit /b 1
)
echo %GREEN%√ Copied main script%RESET%

:: Copy templates
echo %BLUE%Copying template directories...%RESET%
xcopy /E /I /Y "templates\basic" "%TEMPLATES_DIR%\basic" > nul
xcopy /E /I /Y "templates\microservice" "%TEMPLATES_DIR%\microservice" > nul
xcopy /E /I /Y "templates\webapp" "%TEMPLATES_DIR%\webapp" > nul
xcopy /E /I /Y "templates\library" "%TEMPLATES_DIR%\library" > nul
if %ERRORLEVEL% neq 0 (
    echo %RED%Error: Failed to copy templates%RESET%
    exit /b 1
)
echo %GREEN%√ Copied templates%RESET%

:: Copy documentation
echo %BLUE%Copying documentation...%RESET%
xcopy /E /I /Y "docs\*" "%DOCS_DIR%" > nul
if %ERRORLEVEL% neq 0 (
    echo %RED%Error: Failed to copy documentation%RESET%
    exit /b 1
)
echo %GREEN%√ Copied documentation%RESET%

:: Copy completion scripts
echo %BLUE%Copying completion scripts...%RESET%
copy /Y "completion\tjl-project.bash" "%COMPLETION_DIR%\" > nul
copy /Y "completion\tjl-project.zsh" "%COMPLETION_DIR%\" > nul

:: Copy utility scripts
echo %BLUE%Copying utility scripts...%RESET%
copy /Y "scripts\switch_env.sh" "%BIN_DIR%\" > nul
copy /Y "scripts\deploy.sh" "%BIN_DIR%\" > nul
if %ERRORLEVEL% neq 0 (
    echo %RED%Error: Failed to copy utility scripts%RESET%
    exit /b 1
)
echo %GREEN%√ Copied utility scripts%RESET%

:: Copy example files
echo %BLUE%Copying example projects...%RESET%
xcopy /E /I /Y "examples\basic-example" "%INSTALL_DIR%\examples\basic" > nul
xcopy /E /I /Y "examples\microservice-example" "%INSTALL_DIR%\examples\microservice" > nul
xcopy /E /I /Y "examples\webapp-example" "%INSTALL_DIR%\examples\webapp" > nul
xcopy /E /I /Y "examples\library-example" "%INSTALL_DIR%\examples\library" > nul
if %ERRORLEVEL% neq 0 (
    echo %RED%Error: Failed to copy example projects%RESET%
    exit /b 1
)
echo %GREEN%√ Copied example projects%RESET%

:: Create batch wrapper
set "BATCH_FILE=%BIN_DIR%\tjl-project.bat"
(
    echo @echo off
    echo setlocal
    echo set "PYTHONPATH=%LIB_DIR%;%%PYTHONPATH%%"
    echo python "%BIN_DIR%\tjl-project.py" %%*
    echo endlocal
) > "%BATCH_FILE%"
echo %GREEN%√ Created batch wrapper%RESET%

:: Add to PATH
echo %BLUE%Adding to PATH...%RESET%
set "PATH_KEY=HKCU\Environment"
set "PATH_NAME=Path"
for /f "tokens=2*" %%a in ('reg query "%PATH_KEY%" /v "%PATH_NAME%" 2^>nul') do set "CURRENT_PATH=%%b"

if not "!CURRENT_PATH!" == "" (
    echo !CURRENT_PATH! | find /i "%BIN_DIR%" > nul
    if !ERRORLEVEL! neq 0 (
        setx PATH "!CURRENT_PATH!;%BIN_DIR%"
        if !ERRORLEVEL! neq 0 (
            echo %RED%Error: Failed to update PATH%RESET%
            exit /b 1
        )
    ) else (
        echo %YELLOW%! Path already in PATH%RESET%
    )
) else (
    setx PATH "%BIN_DIR%"
)
echo %GREEN%√ Updated PATH%RESET%

:: Create PowerShell integration
echo %BLUE%Setting up PowerShell integration...%RESET%
set "PS_PROFILE_DIR=%USERPROFILE%\Documents\WindowsPowerShell"
set "PS_PROFILE=%PS_PROFILE_DIR%\Microsoft.PowerShell_profile.ps1"

if not exist "%PS_PROFILE_DIR%" mkdir "%PS_PROFILE_DIR%"

:: Add PowerShell functions and completion
(
    echo function New-TJLProject {
    echo     param($projectName, $template = "basic", $path = $null, $environments = "local,dev,staging,prod")
    echo     $cmd = "src/tjl-project.py $projectName"
    echo     if ($template) { $cmd += " --template $template" }
    echo     if ($path) { $cmd += " --path $path" }
    echo     if ($environments) { $cmd += " --environments $environments" }
    echo     & python "%BIN_DIR%\$cmd"
    echo }
    echo Set-Alias tjl New-TJLProject
    echo 
    echo # TJL Project completion
    echo Register-ArgumentCompleter -CommandName tjl -ScriptBlock {
    echo     param($wordToComplete, $commandAst, $cursorPosition)
    echo     $templates = @('basic', 'microservice', 'webapp', 'library')
    echo     $templates | Where-Object { $_ -like "$wordToComplete*" } | ForEach-Object {
    echo         [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterValue', $_)
    echo     }
    echo }
) > "%PS_PROFILE%"
echo %GREEN%√ Created PowerShell integration%RESET%

:: Create shell completion for Command Prompt
echo %BLUE%Setting up command completion...%RESET%
set "COMPLETION_FILE=%COMPLETION_DIR%\tjl-completion.bat"
(
    echo @echo off
    echo setlocal enabledelayedexpansion
    echo set "templates=basic microservice webapp library"
    echo set "commands=new help version"
    echo for %%%%t in (!templates!^) do (
    echo     if "%%%%t" == "%%1" (
    echo         echo %%%%t
    echo     ^)
    echo ^)
) > "%COMPLETION_FILE%"
echo %GREEN%√ Created command completion%RESET%

:: Verify installation
echo %BLUE%Verifying installation...%RESET%
call tjl-project --version > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo %RED%Error: Installation verification failed%RESET%
    echo Please ensure the installation directory is in your PATH
    exit /b 1
)
echo %GREEN%√ Installation verified%RESET%

echo.
echo %GREEN%Installation complete!%RESET%
echo.
echo Please restart your terminal or command prompt to use the tool.
echo.
echo Usage:
echo   tjl-project my-project
echo   tjl my-project (in PowerShell^)
echo.
echo For help:
echo   tjl-project --help
echo.

endlocal