@echo off
"E:\PostgreSQL\16\bin\pg_ctl.exe" stop -D "E:\PostgreSQL\16\data" -m fast 2>nul
"E:\PostgreSQL\16\bin\pg_ctl.exe" register -N postgresql-x64-16 -D "E:\PostgreSQL\16\data" -w -S auto
if %ERRORLEVEL% EQU 0 (
    echo Service registered successfully
    net start postgresql-x64-16
) else (
    echo Register failed with code %ERRORLEVEL%
)
pause
