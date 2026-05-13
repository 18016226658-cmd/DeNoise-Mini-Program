# MySQL 数据库安装脚本 (PowerShell)
# 使用方法：在 PowerShell 中运行：.\install.ps1

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "MySQL 数据库安装脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 MySQL 是否在 PATH 中
$mysqlPath = Get-Command mysql -ErrorAction SilentlyContinue
if (-not $mysqlPath) {
    Write-Host "[错误] 未找到 MySQL 命令，请确保 MySQL 已安装并添加到 PATH" -ForegroundColor Red
    Write-Host "或者使用完整路径，例如：C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -ForegroundColor Yellow
    Read-Host "按 Enter 退出"
    exit 1
}

# 步骤1：检查 MySQL 服务状态
Write-Host "[1/4] 检查 MySQL 服务状态..." -ForegroundColor Yellow
$mysqlService = Get-Service -Name "MySQL*" -ErrorAction SilentlyContinue | Where-Object { $_.Status -eq "Running" }
if (-not $mysqlService) {
    Write-Host "[警告] MySQL 服务未运行，正在尝试启动..." -ForegroundColor Yellow
    try {
        $service = Get-Service -Name "MySQL*" -ErrorAction Stop | Select-Object -First 1
        Start-Service -Name $service.Name
        Write-Host "[成功] MySQL 服务已启动" -ForegroundColor Green
    } catch {
        Write-Host "[错误] 无法启动 MySQL 服务，请手动启动" -ForegroundColor Red
        Write-Host "方法：Win + R -> services.msc -> 找到 MySQL 服务 -> 启动" -ForegroundColor Yellow
        Read-Host "按 Enter 退出"
        exit 1
    }
} else {
    Write-Host "[成功] MySQL 服务正在运行" -ForegroundColor Green
}

Write-Host ""

# 步骤2：创建数据库
Write-Host "[2/4] 创建数据库..." -ForegroundColor Yellow
$password = "123456"
$createDbCmd = "CREATE DATABASE IF NOT EXISTS `audio` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"

try {
    $env:MYSQL_PWD = $password
    mysql -u root -e $createDbCmd 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "创建数据库失败"
    }
    Write-Host "[成功] 数据库 'audio' 已创建" -ForegroundColor Green
} catch {
    Write-Host "[错误] 数据库创建失败，可能是密码错误" -ForegroundColor Red
    Write-Host "请手动输入密码：" -ForegroundColor Yellow
    $securePassword = Read-Host "请输入 MySQL root 密码" -AsSecureString
    $password = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword))
    $env:MYSQL_PWD = $password
    mysql -u root -e $createDbCmd
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[错误] 数据库创建失败" -ForegroundColor Red
        Read-Host "按 Enter 退出"
        exit 1
    }
    Write-Host "[成功] 数据库 'audio' 已创建" -ForegroundColor Green
} finally {
    Remove-Item Env:\MYSQL_PWD -ErrorAction SilentlyContinue
}

Write-Host ""

# 步骤3：导入数据库脚本
Write-Host "[3/4] 导入数据库脚本..." -ForegroundColor Yellow
$scriptPath = Join-Path $PSScriptRoot "zy.sql"
if (-not (Test-Path $scriptPath)) {
    Write-Host "[错误] 未找到 zy.sql 文件" -ForegroundColor Red
    Write-Host "请确保脚本在 backend/database/ 目录下运行" -ForegroundColor Yellow
    Read-Host "按 Enter 退出"
    exit 1
}

try {
    $env:MYSQL_PWD = $password
    Get-Content $scriptPath | mysql -u root audio 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "导入失败"
    }
    Write-Host "[成功] 数据库脚本已导入" -ForegroundColor Green
} catch {
    Write-Host "[错误] 导入失败，可能是密码错误" -ForegroundColor Red
    Write-Host "请手动输入密码：" -ForegroundColor Yellow
    $securePassword = Read-Host "请输入 MySQL root 密码" -AsSecureString
    $password = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword))
    $env:MYSQL_PWD = $password
    Get-Content $scriptPath | mysql -u root audio
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[错误] 导入失败" -ForegroundColor Red
        Read-Host "按 Enter 退出"
        exit 1
    }
    Write-Host "[成功] 数据库脚本已导入" -ForegroundColor Green
} finally {
    Remove-Item Env:\MYSQL_PWD -ErrorAction SilentlyContinue
}

Write-Host ""

# 步骤4：验证安装
Write-Host "[4/4] 验证安装..." -ForegroundColor Yellow
try {
    $env:MYSQL_PWD = $password
    $tables = mysql -u root audio -e "SHOW TABLES;" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[成功] 数据库安装完成！" -ForegroundColor Green
        Write-Host ""
        Write-Host "已创建的表：" -ForegroundColor Cyan
        Write-Host $tables
    } else {
        Write-Host "[警告] 验证失败，但数据库可能已创建成功" -ForegroundColor Yellow
    }
} catch {
    Write-Host "[警告] 验证失败，但数据库可能已创建成功" -ForegroundColor Yellow
} finally {
    Remove-Item Env:\MYSQL_PWD -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "安装完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "默认管理员账户：" -ForegroundColor Yellow
Write-Host "  手机号：13685153598" -ForegroundColor White
Write-Host "  密码：123456" -ForegroundColor White
Write-Host "  用户名：SM" -ForegroundColor White
Write-Host ""
Write-Host "下一步：" -ForegroundColor Yellow
Write-Host "  1. 检查 backend/db_config.py 中的数据库配置" -ForegroundColor White
Write-Host "  2. 运行 python backend/db_config.py 测试连接" -ForegroundColor White
Write-Host "  3. 启动后端服务：python backend/run.py" -ForegroundColor White
Write-Host ""
Read-Host "按 Enter 退出"

