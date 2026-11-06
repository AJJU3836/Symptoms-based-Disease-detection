@ECHO OFF
cd /d "%~dp0"
venv\Scripts\python manage.py runserver
pause
