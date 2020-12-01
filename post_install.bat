@echo off
rem: Note %~dp0 get path of this batch file
set current_dir=%~dp0
set current_drive=%~d0
echo The platformIO installation process is being executed, it may take more than 10 minutes, please be patient...
%current_dir%python377x64/python.exe %current_dir%script.py %*
