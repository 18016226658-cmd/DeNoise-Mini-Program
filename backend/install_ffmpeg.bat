@echo off
REM FFmpeg 自动安装脚本 (批处理)
REM ============================================
REM 功能：自动下载、解压和配置 FFmpeg
REM ============================================

chcp 65001 >nul
echo ========================================
echo FFmpeg 自动安装脚本
echo ========================================
echo.

set "INSTALL_DIR=C:\ffmpeg"
set "DOWNLOAD_URL=https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
set "TEMP_ZIP=%TEMP%\ffmpeg-release-essentials.zip"
set "TEMP_EXTRACT=%TEMP%\ffmpeg-extract"

REM 检查是否已安装
echo [1/5] 检查 FFmpeg 是否已安装...
where ffmpeg >nul 2>&1
if %errorlevel% == 0 (
    echo ✓ FFmpeg 已安装
    ffmpeg -version | findstr /C:"ffmpeg version"
    echo.
    set /p REINSTALL="FFmpeg 已存在，是否重新安装？(y/N): "
    if /i not "%REINSTALL%"=="y" (
        echo 已取消安装。
        exit /b 0
    )
)

REM 检查安装目录
echo [2/5] 检查安装目录...
if exist "%INSTALL_DIR%" (
    echo 警告: 目录 %INSTALL_DIR% 已存在
    set /p DELETE="是否删除并重新安装？(y/N): "
    if /i "%DELETE%"=="y" (
        echo 删除旧目录...
        rmdir /s /q "%INSTALL_DIR%" 2>nul
    ) else (
        echo 已取消安装。
        exit /b 0
    )
)

REM 下载 FFmpeg
echo [3/5] 下载 FFmpeg...
echo 下载地址: %DOWNLOAD_URL%
echo 保存到: %TEMP_ZIP%
echo.

REM 尝试使用 PowerShell 下载
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%DOWNLOAD_URL%' -OutFile '%TEMP_ZIP%' -UseBasicParsing}"

if not exist "%TEMP_ZIP%" (
    echo ✗ 下载失败
    echo.
    echo 请手动下载 FFmpeg:
    echo 1. 访问: https://www.gyan.dev/ffmpeg/builds/
    echo 2. 下载: ffmpeg-release-essentials.zip
    echo 3. 解压到: %INSTALL_DIR%
    echo 4. 将 %INSTALL_DIR%\bin 添加到系统 PATH
    pause
    exit /b 1
)

echo ✓ 下载完成

REM 解压文件
echo [4/5] 解压 FFmpeg...
if exist "%TEMP_EXTRACT%" rmdir /s /q "%TEMP_EXTRACT%" 2>nul
mkdir "%TEMP_EXTRACT%" 2>nul

powershell -Command "Expand-Archive -Path '%TEMP_ZIP%' -DestinationPath '%TEMP_EXTRACT%' -Force"

REM 查找解压后的文件夹
for /d %%d in ("%TEMP_EXTRACT%\*") do (
    set "SOURCE_FOLDER=%%d"
    goto :found
)
:found

if not defined SOURCE_FOLDER (
    echo ✗ 解压失败: 未找到解压文件夹
    pause
    exit /b 1
)

echo 找到解压文件夹: %SOURCE_FOLDER%

REM 创建安装目录并移动文件
mkdir "%INSTALL_DIR%" 2>nul
echo 移动文件到: %INSTALL_DIR%
xcopy /E /I /Y "%SOURCE_FOLDER%\*" "%INSTALL_DIR%\"

REM 清理临时文件
rmdir /s /q "%TEMP_EXTRACT%" 2>nul
del "%TEMP_ZIP%" 2>nul

echo ✓ 安装完成

REM 添加到 PATH
echo [5/5] 配置系统 PATH...
set "BIN_PATH=%INSTALL_DIR%\bin"

if not exist "%BIN_PATH%\ffmpeg.exe" (
    echo ✗ 错误: 找不到 bin 目录: %BIN_PATH%
    pause
    exit /b 1
)

REM 使用 PowerShell 添加到用户 PATH
powershell -Command "& {$currentPath = [Environment]::GetEnvironmentVariable('Path', 'User'); $binPath = '%BIN_PATH%'; if ($currentPath -notlike '*'+$binPath+'*') { $newPath = $currentPath + ';' + $binPath; [Environment]::SetEnvironmentVariable('Path', $newPath, 'User'); Write-Host '✓ 已添加到用户 PATH' } else { Write-Host '✓ PATH 中已包含 FFmpeg 路径' }}"

REM 更新当前会话的 PATH
set "PATH=%PATH%;%BIN_PATH%"

REM 验证安装
echo.
echo ========================================
echo 验证安装...
echo ========================================

if exist "%BIN_PATH%\ffmpeg.exe" (
    echo ✓ FFmpeg 可执行文件存在: %BIN_PATH%\ffmpeg.exe
    echo.
    echo FFmpeg 版本信息:
    "%BIN_PATH%\ffmpeg.exe" -version | findstr /C:"ffmpeg version"
    echo.
    echo ========================================
    echo ✓ FFmpeg 安装成功！
    echo ========================================
    echo.
    echo 注意: 如果当前终端无法识别 ffmpeg 命令，
    echo       请关闭并重新打开终端，或重启计算机。
) else (
    echo ✗ 错误: 找不到 ffmpeg.exe
    echo   预期路径: %BIN_PATH%\ffmpeg.exe
    pause
    exit /b 1
)

pause
