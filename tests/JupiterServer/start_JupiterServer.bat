@ECHO OFF

SET PYTHONPATH=%~dp0\..\..

SET dbfile=%~dp0\db.sqlite3

SET logfile=%~dp0\JS.log

cd %~dp0\..\..\src\JupiterServer\web
C:\python34\python manage.py runserver 127.0.0.1:8091

pause



