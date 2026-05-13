# 重启服务器指南

## 重要提示

**如果修改了后端代码，必须重启服务器才能生效！**

## 重启步骤

### 1. 停止当前服务器

**方法1：在运行服务器的终端窗口按 `Ctrl+C`**

**方法2：结束Python进程**
```bash
# 查看Python进程
tasklist | findstr python

# 结束进程（替换PID为实际进程ID）
taskkill /F /PID <进程ID>
```

### 2. 重新启动服务器

```bash
cd D:\kksyc1\WxMinPro\backend
python -u start.py
```

或者使用：

```bash
python -u run_server.py
```

## 验证服务器已重启

### 检查端口

```bash
netstat -ano | findstr :5000
```

应该只看到一个 `LISTENING` 进程。

### 测试API

运行测试脚本：

```bash
python check_server.py
```

## 常见问题

### 1. 端口被占用

如果启动时提示端口被占用：
- 先停止所有Python进程
- 等待几秒后重新启动

### 2. 修改代码后没有生效

- 确认服务器已重启
- 检查是否有多个服务器实例在运行
- 确认修改的文件已保存

### 3. 路由返回404

- 确认服务器已重启
- 检查路由是否正确注册
- 查看后端控制台的错误信息

## 快速重启命令

```bash
# 停止所有Python进程（谨慎使用）
taskkill /F /IM python.exe

# 等待2秒
timeout /t 2

# 重新启动
cd D:\kksyc1\WxMinPro\backend
python -u start.py
```

