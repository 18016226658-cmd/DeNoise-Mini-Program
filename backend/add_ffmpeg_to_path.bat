@echo off
REM 将 FFmpeg 添加到系统 PATH 环境变量
REM ============================================
REM 需要管理员权限运行
REM ============================================

chcp 65001 >nul
echo ========================================
echo FFmpeg PATH 配置脚本
echo ========================================
echo.

set "FFMPEG_BIN_PATH=C:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin"

REM 检查路径是否存在
echo [1] 检查 FFmpeg 路径...
if not exist "%FFMPEG_BIN_PATH%\ffmpeg.exe" (
    echo ✗ 错误: 路径不存在或找不到 ffmpeg.exe
    echo   路径: %FFMPEG_BIN_PATH%
    pause
    exit /b 1
)

echo ✓ FFmpeg 路径存在: %FFMPEG_BIN_PATH%
echo.

REM 使用 PowerShell 添加到用户 PATH
echo [2] 添加到用户 PATH...
powershell -Command "& {$currentPath = [Environment]::GetEnvironmentVariable('Path', 'User'); $binPath = '%FFMPEG_BIN_PATH%'; if ($currentPath -notlike '*'+$binPath+'*') { $newPath = $currentPath + ';' + $binPath; [Environment]::SetEnvironmentVariable('Path', $newPath, 'User'); Write-Host '✓ 已添加到用户 PATH' } else { Write-Host '✓ PATH 中已包含 FFmpeg 路径' }}"

REM 更新当前会话的 PATH
set "PATH=%PATH%;%FFMPEG_BIN_PATH%"

REM 验证
echo.
echo [3] 验证配置...
powershell -Command "& {$updatedPath = [Environment]::GetEnvironmentVariable('Path', 'User'); $binPath = '%FFMPEG_BIN_PATH%'; if ($updatedPath -like '*'+$binPath+'*') { Write-Host '✓ PATH 配置成功' } else { Write-Host '✗ PATH 配置失败'; exit 1 }}"

if %errorlevel% neq 0 (
    echo 配置失败，请检查权限
    pause
    exit /b 1
)

REM 测试 FFmpeg
echo.
echo [4] 测试 FFmpeg 命令...
"%FFMPEG_BIN_PATH%\ffmpeg.exe" -version | findstr /C:"ffmpeg version"

if %errorlevel% == 0 (
    echo.
    echo ========================================
    echo ✓ FFmpeg PATH 配置完成！
    echo ========================================
    echo.
    echo 重要提示：
    echo 1. 请关闭所有终端窗口
    echo 2. 重新打开新的终端窗口
    echo 3. 运行 'ffmpeg -version' 验证
    echo.
    echo 配置的路径: %FFMPEG_BIN_PATH%
) else (
    echo ⚠ 无法直接运行 FFmpeg（可能需要重启终端）
    echo.
    echo 配置的路径: %FFMPEG_BIN_PATH%
    echo 请关闭并重新打开终端后验证
)

pause
