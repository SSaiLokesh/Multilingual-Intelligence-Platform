@echo off
setlocal

echo ==============================
echo Running commit.bat...
echo ==============================
call commit.bat


echo.
echo ==============================
echo Pushing to remote...
echo ==============================
git push

if errorlevel 1 (
    echo.
    echo Push failed.
    pause
    exit /b 1
)

echo.
echo Push completed successfully.
