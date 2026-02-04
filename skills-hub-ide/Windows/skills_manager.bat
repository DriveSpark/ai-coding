@echo off
REM 设置控制台为 UTF-8 编码
chcp 65001 >nul

echo.
echo 正在启动 AI Skills 分发系统...
echo.

REM 使用 -Command 方式执行，先设置编码再运行脚本
PowerShell -NoProfile -ExecutionPolicy Bypass -Command "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; [Console]::InputEncoding = [System.Text.Encoding]::UTF8; & '%~dp0skills_manager.ps1'"

pause
