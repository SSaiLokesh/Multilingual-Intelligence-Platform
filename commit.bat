@echo off
setlocal

echo.
set /p "message=Enter commit message: "

if "%message%"=="" (
    echo Commit message cannot be empty.
    pause
    exit /b 1
)

echo Adding all changes...
git add .

echo.
echo Committing changes...
git commit -m "%message%"

echo.
