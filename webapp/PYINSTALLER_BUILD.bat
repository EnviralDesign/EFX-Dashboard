@echo off
cd /d %~dp0
pyinstaller EFX_Dashboard.spec --noconfirm
pause