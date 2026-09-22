@echo off
@REM  setlocal enabledelayedexpansion

set "OUTPUT=snapshot.txt"

echo Creating Python project snapshot...
echo.

> "%OUTPUT%" echo ============================================================
>>"%OUTPUT%" echo MULTILINGUAL INTELLIGENCE PLATFORM - PYTHON SNAPSHOT
>>"%OUTPUT%" echo Generated: %date% %time%
>>"%OUTPUT%" echo Root: %CD%
>>"%OUTPUT%" echo ============================================================
>>"%OUTPUT%" echo.

for /r %%F in (*.py) do (
    set "FILE=%%F"

    rem Skip venv and __pycache__ directories
    echo !FILE! | findstr /i /c:"\venv\" /c:"\__pycache__\" >nul

    if errorlevel 1 (
        echo Processing: %%F

        >>"%OUTPUT%" echo.
        >>"%OUTPUT%" echo ============================================================
        >>"%OUTPUT%" echo FILE: %%F
        >>"%OUTPUT%" echo ============================================================
        >>"%OUTPUT%" echo.

        type "%%F" >>"%OUTPUT%"

        >>"%OUTPUT%" echo.
        >>"%OUTPUT%" echo.
    )
)

echo.
echo Snapshot created successfully:
echo %CD%\%OUTPUT%
echo.
