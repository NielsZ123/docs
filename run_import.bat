@echo off
echo Kordiam Excel Importer
echo =====================

REM Check if virtual environment exists
if not exist "venv" (
    echo Setting up virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

echo.

REM Check for required files
if not exist "kordiam_excel_importer.py" (
    echo Error: kordiam_excel_importer.py not found!
    pause
    exit /b 1
)

if not exist "kordiam_mapping.json" (
    echo Error: kordiam_mapping.json not found!
    pause
    exit /b 1
)

REM Get credentials if not set as environment variables
if "%KORDIAM_CLIENT_ID%"=="" (
    echo Enter your Kordiam OAuth2 credentials:
    set /p KORDIAM_CLIENT_ID="Client ID: "
)

if "%KORDIAM_CLIENT_SECRET%"=="" (
    set /p KORDIAM_CLIENT_SECRET="Client Secret: "
)

REM Get Excel file path
if "%1"=="" (
    echo.
    set /p EXCEL_FILE="Enter path to Excel file: "
) else (
    set EXCEL_FILE=%1
)

REM Check if Excel file exists
if not exist "%EXCEL_FILE%" (
    echo Error: Excel file '%EXCEL_FILE%' not found!
    pause
    exit /b 1
)

echo.
echo Configuration:
echo - Client ID: %KORDIAM_CLIENT_ID%
echo - Client Secret: [HIDDEN]
echo - Excel file: %EXCEL_FILE%
echo.

REM Ask for dry run
set /p DRY_RUN="Run in dry-run mode first? (y/n): "

echo.
echo Starting import...

if /i "%DRY_RUN%"=="y" (
    echo Running in DRY-RUN mode ^(no actual elements will be created^)...
    python kordiam_excel_importer.py "%EXCEL_FILE%" --client-id "%KORDIAM_CLIENT_ID%" --client-secret "%KORDIAM_CLIENT_SECRET%" --dry-run
    
    echo.
    set /p REAL_RUN="Dry run completed. Run actual import? (y/n): "
    
    if /i "!REAL_RUN!"=="y" (
        echo Running ACTUAL import...
        python kordiam_excel_importer.py "%EXCEL_FILE%" --client-id "%KORDIAM_CLIENT_ID%" --client-secret "%KORDIAM_CLIENT_SECRET%"
    ) else (
        echo Import cancelled.
    )
) else (
    echo Running ACTUAL import...
    python kordiam_excel_importer.py "%EXCEL_FILE%" --client-id "%KORDIAM_CLIENT_ID%" --client-secret "%KORDIAM_CLIENT_SECRET%"
)

echo Done!
pause