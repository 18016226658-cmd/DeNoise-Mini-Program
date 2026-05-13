# 重启服务器详细步骤

## 步骤1：停止所有 Python 进程

### 方法1：使用任务管理器（推荐，最安全）

1. 按 `Ctrl + Shift + Esc` 打开任务管理器
2. 找到所有 `python.exe` 或 `python3.11.exe` 进程
3. 右键点击 → 结束任务
4. 或者选中后点击"结束任务"按钮

### 方法2：使用命令行（快速但需谨慎）

**在 PowerShell 或 CMD 中运行：**

```bash
# 查看所有 Python 进程
tasklist | findstr python

# 停止所有 Python 进程（谨慎使用，会停止所有Python程序）
taskkill /F /IM python.exe
taskkill /F /IM python3.11.exe
```

**注意：** 这会停止所有 Python 程序，包括其他正在运行的 Python 脚本。

### 方法3：只停止占用端口5000的进程（推荐）

```bash
# 1. 查找占用端口5000的进程ID
netstat -ano | findstr :5000

# 2. 从输出中找到 PID（最后一列的数字）
# 例如：TCP    0.0.0.0:5000   0.0.0.0:0   LISTENING   12345
# PID 就是 12345

# 3. 结束该进程（替换 12345 为实际的PID）
taskkill /F /PID 12345
```

## 步骤2：验证进程已停止

```bash
# 检查是否还有 Python 进程
tasklist | findstr python

# 检查端口5000是否已释放
netstat -ano | findstr :5000
```

如果命令没有输出，说明进程已停止。

## 步骤3：重新启动服务器

```bash
# 1. 进入后端目录
cd D:\kksyc1\WxMinPro\backend

# 2. 启动服务器
python -u start.py
```

**或者使用：**

```bash
python -u run_server.py
```

## 步骤4：确认只有一个服务器进程在运行

### 方法1：检查端口

```bash
netstat -ano | findstr :5000
```

**应该只看到一行输出，类似：**
```
TCP    0.0.0.0:5000   0.0.0.0:0   LISTENING   12345
```

如果看到多行，说明有多个进程在运行。

### 方法2：检查 Python 进程

```bash
tasklist | findstr python
```

**应该只看到一个或两个 python 进程**（一个是服务器，一个是启动脚本）。

### 方法3：测试服务器

```bash
cd D:\kksyc1\WxMinPro\backend
python check_server.py
```

应该显示服务器正在运行。

## 完整的一键脚本

创建一个批处理文件 `restart_server.bat`：

```batch
@echo off
echo 正在停止所有Python进程...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM python3.11.exe 2>nul
timeout /t 2 /nobreak >nul
echo 等待进程完全停止...
timeout /t 1 /nobreak >nul
echo.
echo 检查端口5000状态...
netstat -ano | findstr :5000
echo.
echo 正在启动服务器...
cd /d D:\kksyc1\WxMinPro\backend
python -u start.py
```

保存为 `restart_server.bat`，双击运行即可。

