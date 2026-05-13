# FFmpeg 自动安装脚本 (PowerShell)
# ============================================
# 功能：自动下载、解压和配置 FFmpeg
# ============================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "FFmpeg 自动安装脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 配置
$FFmpegVersion = "7.0"
$DownloadUrl = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
$InstallDir = "C:\ffmpeg"
$ZipFile = "$env:TEMP\ffmpeg-release-essentials.zip"
$ExtractDir = "$env:TEMP\ffmpeg-extract"

# 检查是否已安装
Write-Host "[1/5] 检查 FFmpeg 是否已安装..." -ForegroundColor Yellow
$ffmpegPath = Get-Command ffmpeg -ErrorAction SilentlyContinue
if ($ffmpegPath) {
    Write-Host "✓ FFmpeg 已安装: $($ffmpegPath.Source)" -ForegroundColor Green
    Write-Host ""
    Write-Host "验证安装..." -ForegroundColor Yellow
    & ffmpeg -version | Select-Object -First 3
    Write-Host ""
    $response = Read-Host "FFmpeg 已存在，是否重新安装？(y/N)"
    if ($response -ne 'y' -and $response -ne 'Y') {
        Write-Host "已取消安装。" -ForegroundColor Yellow
        exit 0
    }
}

# 检查安装目录
Write-Host "[2/5] 检查安装目录..." -ForegroundColor Yellow
if (Test-Path $InstallDir) {
    Write-Host "警告: 目录 $InstallDir 已存在" -ForegroundColor Yellow
    $response = Read-Host "是否删除并重新安装？(y/N)"
    if ($response -eq 'y' -or $response -eq 'Y') {
        Write-Host "删除旧目录..." -ForegroundColor Yellow
        Remove-Item -Path $InstallDir -Recurse -Force -ErrorAction SilentlyContinue
    } else {
        Write-Host "已取消安装。" -ForegroundColor Yellow
        exit 0
    }
}

# 下载 FFmpeg
Write-Host "[3/5] 下载 FFmpeg..." -ForegroundColor Yellow
Write-Host "下载地址: $DownloadUrl" -ForegroundColor Gray
Write-Host "保存到: $ZipFile" -ForegroundColor Gray
Write-Host ""

try {
    # 检查是否有 Invoke-WebRequest 或使用 System.Net.WebClient
    if ($PSVersionTable.PSVersion.Major -ge 3) {
        $ProgressPreference = 'Continue'
        Invoke-WebRequest -Uri $DownloadUrl -OutFile $ZipFile -UseBasicParsing
    } else {
        $webClient = New-Object System.Net.WebClient
        $webClient.DownloadFile($DownloadUrl, $ZipFile)
    }
    Write-Host "✓ 下载完成" -ForegroundColor Green
} catch {
    Write-Host "✗ 下载失败: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "请手动下载 FFmpeg:" -ForegroundColor Yellow
    Write-Host "1. 访问: https://www.gyan.dev/ffmpeg/builds/" -ForegroundColor Cyan
    Write-Host "2. 下载: ffmpeg-release-essentials.zip" -ForegroundColor Cyan
    Write-Host "3. 解压到: $InstallDir" -ForegroundColor Cyan
    Write-Host "4. 将 $InstallDir\bin 添加到系统 PATH" -ForegroundColor Cyan
    exit 1
}

# 解压文件
Write-Host "[4/5] 解压 FFmpeg..." -ForegroundColor Yellow
try {
    # 清理临时解压目录
    if (Test-Path $ExtractDir) {
        Remove-Item -Path $ExtractDir -Recurse -Force -ErrorAction SilentlyContinue
    }
    New-Item -ItemType Directory -Path $ExtractDir -Force | Out-Null
    
    # 解压 ZIP 文件
    Expand-Archive -Path $ZipFile -DestinationPath $ExtractDir -Force
    Write-Host "✓ 解压完成" -ForegroundColor Green
    
    # 查找解压后的文件夹（通常是 ffmpeg-7.0-essentials_build）
    $extractedFolders = Get-ChildItem -Path $ExtractDir -Directory
    if ($extractedFolders.Count -eq 0) {
        throw "解压后未找到文件夹"
    }
    
    $sourceFolder = $extractedFolders[0].FullName
    Write-Host "找到解压文件夹: $sourceFolder" -ForegroundColor Gray
    
    # 创建安装目录并移动文件
    New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
    Write-Host "移动文件到: $InstallDir" -ForegroundColor Gray
    Move-Item -Path "$sourceFolder\*" -Destination $InstallDir -Force
    
    # 清理临时文件
    Remove-Item -Path $ExtractDir -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path $ZipFile -Force -ErrorAction SilentlyContinue
    
    Write-Host "✓ 安装完成" -ForegroundColor Green
} catch {
    Write-Host "✗ 解压失败: $_" -ForegroundColor Red
    exit 1
}

# 添加到 PATH
Write-Host "[5/5] 配置系统 PATH..." -ForegroundColor Yellow
$binPath = Join-Path $InstallDir "bin"
if (-not (Test-Path $binPath)) {
    Write-Host "✗ 错误: 找不到 bin 目录: $binPath" -ForegroundColor Red
    exit 1
}

try {
    # 获取当前用户的环境变量 PATH
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    
    # 检查是否已存在
    if ($currentPath -split ';' -contains $binPath) {
        Write-Host "✓ PATH 中已包含 FFmpeg 路径" -ForegroundColor Green
    } else {
        # 添加到用户 PATH
        $newPath = $currentPath + ";" + $binPath
        [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
        Write-Host "✓ 已添加到用户 PATH" -ForegroundColor Green
        Write-Host "  路径: $binPath" -ForegroundColor Gray
    }
    
    # 同时更新当前会话的 PATH
    $env:Path += ";$binPath"
    
} catch {
    Write-Host "✗ 配置 PATH 失败: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "请手动添加 PATH:" -ForegroundColor Yellow
    Write-Host "1. 右键'此电脑' -> 属性 -> 高级系统设置 -> 环境变量" -ForegroundColor Cyan
    Write-Host "2. 在'用户变量'中找到 Path，点击编辑" -ForegroundColor Cyan
    Write-Host "3. 点击'新建'，添加: $binPath" -ForegroundColor Cyan
    Write-Host "4. 确定保存，重启终端" -ForegroundColor Cyan
}

# 验证安装
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "验证安装..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$ffmpegExe = Join-Path $binPath "ffmpeg.exe"
if (Test-Path $ffmpegExe) {
    Write-Host "✓ FFmpeg 可执行文件存在: $ffmpegExe" -ForegroundColor Green
    Write-Host ""
    Write-Host "FFmpeg 版本信息:" -ForegroundColor Yellow
    & $ffmpegExe -version | Select-Object -First 3
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✓ FFmpeg 安装成功！" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "注意: 如果当前终端无法识别 ffmpeg 命令，" -ForegroundColor Yellow
    Write-Host "      请关闭并重新打开终端，或重启计算机。" -ForegroundColor Yellow
} else {
    Write-Host "✗ 错误: 找不到 ffmpeg.exe" -ForegroundColor Red
    Write-Host "  预期路径: $ffmpegExe" -ForegroundColor Gray
    exit 1
}
