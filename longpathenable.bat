%1 %2
@echo off
ver|find "5.">nul&&goto :admin
mshta vbscript:createobject("shell.application").shellexecute("%~s0","goto :admin","","runas",1)(window.close)&goto :eof
:admin
reg add HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\FileSystem /v LongPathsEnabled /t REG_DWORD  /f /d 1
:eof

