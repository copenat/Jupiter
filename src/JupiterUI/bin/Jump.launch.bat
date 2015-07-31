@ECHO OFF

SET PYTHONPATH=%~dp0\..\..;%~dp0\..\..\PythonRequests

%~dp0\..\..\PythonWindows\python %~dp0\..\lib\JupiterUI.py %~dp0\..\lib

rem c:\python34\python %~dp0\..\lib\JupiterUI.py %~dp0\..\lib
pause
