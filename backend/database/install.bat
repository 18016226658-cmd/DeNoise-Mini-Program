@echo off
chcp 65001 >nul
echo ========================================
echo MySQL 数据库安装脚本
echo ========================================
echo.

REM 检查 MySQL 是否在 PATH 中
where mysql >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 MySQL 命令，请确保 MySQL 已安装并添加到 PATH
    echo 或者使用完整路径，例如：C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe
    pause
    exit /b 1
)

echo [1/4] 检查 MySQL 服务状态...
sc query MySQL | find "RUNNING" >nul
if %errorlevel% neq 0 (
    echo [警告] MySQL 服务未运行，正在尝试启动...
    net start MySQL >nul 2>&1
    if %errorlevel% neq 0 (
        echo [错误] 无法启动 MySQL 服务，请手动启动
        echo 方法：Win + R -> services.msc -> 找到 MySQL 服务 -> 启动
        pause
        exit /b 1
    )
    echo [成功] MySQL 服务已启动
) else (
    echo [成功] MySQL 服务正在运行
)

echo.
echo [2/4] 创建数据库...
mysql -u root -p123456 -e "CREATE DATABASE IF NOT EXISTS `audio` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;" 2>nul
if %errorlevel% neq 0 (
    echo [错误] 数据库创建失败，可能是密码错误
    echo 请手动输入密码：
    mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS `audio` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"
    if %errorlevel% neq 0 (
        echo [错误] 数据库创建失败
        pause
        exit /b 1
    )
)
echo [成功] 数据库 'audio' 已创建

echo.
echo [3/4] 导入数据库脚本...
cd /d "%~dp0"
if not exist "zy.sql" (
    echo [错误] 未找到 zy.sql 文件
    echo 请确保脚本在 backend/database/ 目录下运行
    pause
    exit /b 1
)

mysql -u root -p123456 audio < zy.sql 2>nul
if %errorlevel% neq 0 (
    echo [错误] 导入失败，可能是密码错误
    echo 请手动输入密码：
    mysql -u root -p audio < zy.sql
    if %errorlevel% neq 0 (
        echo [错误] 导入失败
        pause
        exit /b 1
    )
)
echo [成功] 数据库脚本已导入

echo.
echo [4/4] 验证安装...
mysql -u root -p123456 -e "USE audio; SHOW TABLES;" 2>nul
if %errorlevel% neq 0 (
    echo [警告] 验证失败，但数据库可能已创建成功
) else (
    echo [成功] 数据库安装完成！
    echo.
    echo 已创建的表：
    mysql -u root -p123456 -e "USE audio; SHOW TABLES;" 2>nul
)

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 默认管理员账户：
echo   手机号：13685153598
echo   密码：123456
echo   用户名：SM
echo.
echo 下一步：
echo   1. 检查 backend/db_config.py 中的数据库配置
echo   2. 运行 python backend/db_config.py 测试连接
echo   3. 启动后端服务：python backend/run.py
echo.
pause

