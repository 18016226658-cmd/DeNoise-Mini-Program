@echo off
chcp 65001 >nul
echo ============================================================
echo 重启后端服务器
echo ============================================================
echo.

echo [1/4] 正在停止所有Python进程...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM python3.11.exe 2>nul
if %errorlevel% equ 0 (
    echo    [成功] Python进程已停止
) else (
    echo    [信息] 没有找到运行中的Python进程
)
echo.

echo [2/4] 等待进程完全停止...
timeout /t 2 /nobreak >nul
echo.

echo [3/4] 检查端口5000状态...
netstat -ano | findstr :5000
if %errorlevel% equ 0 (
    echo    [警告] 端口5000仍被占用，尝试强制结束...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do (
        taskkill /F /PID %%a 2>nul
    )
    timeout /t 1 /nobreak >nul
) else (
    echo    [成功] 端口5000已释放
)
echo.

echo [4/4] 正在启动服务器...
cd /d %~dp0
python -u start.py

pause

