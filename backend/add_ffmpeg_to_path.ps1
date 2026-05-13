# 将 FFmpeg 添加到系统 PATH 环境变量
# ============================================
# 需要管理员权限运行
# ============================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "FFmpeg PATH 配置脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$ffmpegBinPath = "C:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin"

# 检查路径是否存在
Write-Host "[1] 检查 FFmpeg 路径..." -ForegroundColor Yellow
if (-not (Test-Path $ffmpegBinPath)) {
    Write-Host "✗ 错误: 路径不存在: $ffmpegBinPath" -ForegroundColor Red
    Write-Host ""
    Write-Host "请确认 FFmpeg 已正确解压到该路径。" -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Path "$ffmpegBinPath\ffmpeg.exe")) {
    Write-Host "✗ 错误: 找不到 ffmpeg.exe: $ffmpegBinPath\ffmpeg.exe" -ForegroundColor Red
    exit 1
}

Write-Host "✓ FFmpeg 路径存在: $ffmpegBinPath" -ForegroundColor Green
Write-Host ""

# 检查是否已存在
Write-Host "[2] 检查 PATH 环境变量..." -ForegroundColor Yellow
$currentUserPath = [Environment]::GetEnvironmentVariable("Path", "User")
$currentSystemPath = [Environment]::GetEnvironmentVariable("Path", "Machine")

$pathExists = $false
if ($currentUserPath -like "*$ffmpegBinPath*") {
    Write-Host "✓ 已在用户 PATH 中找到 FFmpeg 路径" -ForegroundColor Green
    $pathExists = $true
}
if ($currentSystemPath -like "*$ffmpegBinPath*") {
    Write-Host "✓ 已在系统 PATH 中找到 FFmpeg 路径" -ForegroundColor Green
    $pathExists = $true
}

if ($pathExists) {
    Write-Host ""
    Write-Host "FFmpeg 路径已在 PATH 中，无需重复添加。" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "如果仍然无法识别 ffmpeg 命令，请：" -ForegroundColor Yellow
    Write-Host "1. 关闭所有终端窗口" -ForegroundColor Cyan
    Write-Host "2. 重新打开新的终端窗口" -ForegroundColor Cyan
    Write-Host "3. 运行: ffmpeg -version" -ForegroundColor Cyan
    exit 0
}

# 添加到用户 PATH（推荐，不需要管理员权限）
Write-Host "[3] 添加到用户 PATH..." -ForegroundColor Yellow
try {
    if ($currentUserPath) {
        $newUserPath = $currentUserPath + ";" + $ffmpegBinPath
    } else {
        $newUserPath = $ffmpegBinPath
    }
    
    [Environment]::SetEnvironmentVariable("Path", $newUserPath, "User")
    Write-Host "✓ 已添加到用户 PATH" -ForegroundColor Green
    Write-Host "  路径: $ffmpegBinPath" -ForegroundColor Gray
    
    # 更新当前会话的 PATH
    $env:Path += ";$ffmpegBinPath"
    
} catch {
    Write-Host "✗ 添加到用户 PATH 失败: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "请尝试以管理员身份运行此脚本，或手动添加 PATH。" -ForegroundColor Yellow
    exit 1
}

# 验证
Write-Host ""
Write-Host "[4] 验证配置..." -ForegroundColor Yellow
$updatedPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($updatedPath -like "*$ffmpegBinPath*") {
    Write-Host "✓ PATH 配置成功" -ForegroundColor Green
} else {
    Write-Host "✗ PATH 配置失败" -ForegroundColor Red
    exit 1
}

# 测试 FFmpeg 命令
Write-Host ""
Write-Host "[5] 测试 FFmpeg 命令..." -ForegroundColor Yellow
try {
    $ffmpegExe = Join-Path $ffmpegBinPath "ffmpeg.exe"
    $result = & $ffmpegExe -version 2>&1 | Select-Object -First 3
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ FFmpeg 可以正常运行" -ForegroundColor Green
        Write-Host ""
        Write-Host "版本信息:" -ForegroundColor Yellow
        $result | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
    }
} catch {
    Write-Host "⚠ 无法直接运行 FFmpeg（可能需要重启终端）" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✓ FFmpeg PATH 配置完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "重要提示：" -ForegroundColor Yellow
Write-Host "1. 请关闭所有终端窗口" -ForegroundColor Cyan
Write-Host "2. 重新打开新的终端窗口" -ForegroundColor Cyan
Write-Host "3. 运行 'ffmpeg -version' 验证" -ForegroundColor Cyan
Write-Host ""
Write-Host "配置的路径: $ffmpegBinPath" -ForegroundColor Gray
