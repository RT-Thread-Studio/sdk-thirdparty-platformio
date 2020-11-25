@echo off
rem: Note %~dp0 get path of this batch file
set current_dir=%~dp0
set current_drive=%~d0

%current_dir%python377x64/python.exe %current_dir%script.py %*
