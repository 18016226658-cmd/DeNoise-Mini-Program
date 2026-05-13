# PowerShell 脚本：重启服务器

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "重启后端服务器" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# 步骤1：停止所有Python进程
Write-Host "[1/4] 正在停止所有Python进程..." -ForegroundColor Yellow
$pythonProcesses = Get-Process -Name python,python3.11 -ErrorAction SilentlyContinue
if ($pythonProcesses) {
    $pythonProcesses | Stop-Process -Force
    Write-Host "   [成功] 已停止 $($pythonProcesses.Count) 个Python进程" -ForegroundColor Green
} else {
    Write-Host "   [信息] 没有找到运行中的Python进程" -ForegroundColor Gray
}
Write-Host ""

# 步骤2：等待进程完全停止
Write-Host "[2/4] 等待进程完全停止..." -ForegroundColor Yellow
Start-Sleep -Seconds 2
Write-Host ""

# 步骤3：检查端口5000
Write-Host "[3/4] 检查端口5000状态..." -ForegroundColor Yellow
$port5000 = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue
if ($port5000) {
    Write-Host "   [警告] 端口5000仍被占用，尝试结束进程..." -ForegroundColor Yellow
    $port5000 | ForEach-Object {
        $pid = $_.OwningProcess
        Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
    }
    Start-Sleep -Seconds 1
} else {
    Write-Host "   [成功] 端口5000已释放" -ForegroundColor Green
}
Write-Host ""

# 步骤4：启动服务器
Write-Host "[4/4] 正在启动服务器..." -ForegroundColor Yellow
Set-Location $PSScriptRoot
python -u start.py

