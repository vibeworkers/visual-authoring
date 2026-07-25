@echo off
setlocal EnableExtensions

set "PYTHON_BIN="
if not "%VISUAL_AUTHORING_PYTHON%"=="" (
  "%VISUAL_AUTHORING_PYTHON%" -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 9) else 1)" >nul 2>nul && set "PYTHON_BIN=%VISUAL_AUTHORING_PYTHON%"
) else (
  py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 9) else 1)" >nul 2>nul && set "PYTHON_BIN=py -3"
  if "%PYTHON_BIN%"=="" python3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 9) else 1)" >nul 2>nul && set "PYTHON_BIN=python3"
  if "%PYTHON_BIN%"=="" python -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 9) else 1)" >nul 2>nul && set "PYTHON_BIN=python"
)

if not "%PYTHON_BIN%"=="" goto :run
if "%VISUAL_AUTHORING_AUTO_INSTALL_PYTHON%"=="0" (
  echo {"status":"blocked_missing_python","auto_install_attempted":false,"reason":"Python 3.9 or later is required and automatic installation is disabled"} 1>&2
  exit /b 1
)

where winget >nul 2>nul || (
  echo {"status":"blocked_missing_python","auto_install_attempted":false,"reason":"winget is required for automatic Python installation on this Windows host"} 1>&2
  exit /b 1
)
winget install --exact --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements || (
  echo {"status":"blocked_missing_python","auto_install_attempted":true,"reason":"winget could not install Python"} 1>&2
  exit /b 1
)
py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 9) else 1)" >nul 2>nul && set "PYTHON_BIN=py -3"
if "%PYTHON_BIN%"=="" (
  echo {"status":"blocked_missing_python","auto_install_attempted":true,"reason":"Python installation finished without a discoverable Python 3.9 or later command"} 1>&2
  exit /b 1
)

:run
if /I "%~1"=="run" (
  shift
  if "%~1"=="" (
    echo usage: visual-authoring-runtime.cmd run ^<python-script^> [args...] 1>&2
    exit /b 2
  )
  %PYTHON_BIN% "%~1" %*
  exit /b %ERRORLEVEL%
)
%PYTHON_BIN% "%~dp0portable_visual_runtime.py" %*
exit /b %ERRORLEVEL%
