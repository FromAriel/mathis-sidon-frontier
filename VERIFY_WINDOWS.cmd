@echo off
setlocal
cd /d "%~dp0"

echo Sidon Frontier R9 - exact certificate verification
echo.

where py >nul 2>nul
if not errorlevel 1 (
    py -3 verify.py CERTIFICATE.json
    set "VERIFY_EXIT=%ERRORLEVEL%"
    goto finished
)

where python >nul 2>nul
if not errorlevel 1 (
    python verify.py CERTIFICATE.json
    set "VERIFY_EXIT=%ERRORLEVEL%"
    goto finished
)

where python3 >nul 2>nul
if not errorlevel 1 (
    python3 verify.py CERTIFICATE.json
    set "VERIFY_EXIT=%ERRORLEVEL%"
    goto finished
)

echo VERIFICATION COULD NOT START
echo Python 3.9 or newer was not found on PATH.
set "VERIFY_EXIT=2"

:finished
echo.
if "%VERIFY_EXIT%"=="0" (
    echo Verification completed successfully.
) else (
    echo Verification failed with exit code %VERIFY_EXIT%.
)
echo.
echo Press any key to close this window.
pause >nul
exit /b %VERIFY_EXIT%
