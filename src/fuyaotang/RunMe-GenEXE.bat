@echo off
chcp 65001
pyinstaller -y -F .\app.py  -i fu.ico
pause();
 