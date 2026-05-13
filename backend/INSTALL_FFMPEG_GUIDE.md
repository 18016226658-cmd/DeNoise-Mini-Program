# FFmpeg 自动安装指南

## 快速安装（推荐）

### 方法1：使用 PowerShell 脚本（推荐）

1. **以管理员身份运行 PowerShell**
   - 右键点击"开始"菜单
   - 选择"Windows PowerShell (管理员)"

2. **运行安装脚本**
   ```powershell
   cd D:\WxMinPro\WxMinPro\backend
   .\install_ffmpeg.ps1
   ```

3. **按照提示操作**
   - 脚本会自动下载、解压和配置 FFmpeg
   - 安装完成后，关闭并重新打开终端验证

### 方法2：使用批处理脚本

1. **以管理员身份运行命令提示符 (CMD)**
   - 右键点击"开始"菜单
   - 选择"命令提示符 (管理员)"

2. **运行安装脚本**
   ```cmd
   cd D:\WxMinPro\WxMinPro\backend
   install_ffmpeg.bat
   ```

## 手动安装步骤

如果自动脚本无法运行，可以手动安装：

### 步骤1：下载 FFmpeg

1. 访问：https://www.gyan.dev/ffmpeg/builds/
2. 下载 **ffmpeg-release-essentials.zip**（约 100MB）
   - 或者直接访问：https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-7.0-essentials_build.zip

### 步骤2：解压 FFmpeg

1. 解压下载的 zip 文件
2. 将解压后的文件夹重命名为 `ffmpeg`
3. 移动到 `C:\ffmpeg`（或其他位置，如 `D:\ffmpeg`）

### 步骤3：添加到系统 PATH

#### 方法A：通过图形界面

1. 右键点击"此电脑"（或"我的电脑"）
2. 选择"属性"
3. 点击"高级系统设置"
4. 点击"环境变量"按钮
5. 在"用户变量"区域，找到 `Path` 变量，点击"编辑"
6. 点击"新建"
7. 输入 FFmpeg 的 bin 目录路径：`C:\ffmpeg\bin`
8. 点击"确定"保存所有更改

#### 方法B：通过 PowerShell（管理员）

```powershell
# 添加到用户 PATH
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
$ffmpegPath = "C:\ffmpeg\bin"
if ($currentPath -notlike "*$ffmpegPath*") {
    $newPath = $currentPath + ";" + $ffmpegPath
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "✓ 已添加到 PATH"
} else {
    Write-Host "PATH 中已包含 FFmpeg"
}
```

### 步骤4：验证安装

1. **关闭当前所有终端窗口**（重要！）
2. 打开新的 PowerShell 或 CMD 窗口
3. 运行命令：
   ```powershell
   ffmpeg -version
   ```
4. 如果看到版本信息，说明安装成功

### 步骤5：重启应用

重启 Flask 应用，系统会自动检测到 FFmpeg。

## 验证安装

运行以下命令验证 FFmpeg 是否已正确安装：

```powershell
# 检查 FFmpeg 是否在 PATH 中
ffmpeg -version

# 检查常见安装位置
Test-Path "C:\ffmpeg\bin\ffmpeg.exe"
Test-Path "D:\ffmpeg\bin\ffmpeg.exe"
```

## 常见问题

### Q: 脚本执行被阻止？

**A:** PowerShell 执行策略限制。解决方法：

```powershell
# 临时允许执行脚本（仅当前会话）
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

# 然后运行脚本
.\install_ffmpeg.ps1
```

### Q: 下载速度慢或失败？

**A:** 
1. 检查网络连接
2. 尝试使用浏览器手动下载
3. 使用下载工具（如 IDM）下载后手动安装

### Q: 添加到 PATH 后仍然找不到 FFmpeg？

**A:** 
1. 确保已关闭所有终端窗口并重新打开
2. 检查 PATH 路径是否正确（指向 `bin` 目录）
3. 尝试重启计算机
4. 在配置文件中手动指定路径（见下方）

## 在配置文件中指定路径（备选方案）

如果不想添加到系统 PATH，可以在配置文件中直接指定：

1. 打开 `backend/config.py`
2. 找到 `FFMPEG_PATH` 配置项（约第 114 行）
3. 修改为：
   ```python
   FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"  # 替换为你的实际路径
   ```
4. 保存文件并重启应用

## 安装完成后

安装完成后，重启 Flask 应用，你应该会看到：

```
[成功] FFmpeg 已配置: C:\ffmpeg\bin\ffmpeg.exe
```

然后就可以正常上传和处理所有格式的音频文件了！

## 支持的格式

安装 FFmpeg 后，可以处理：
- ✅ MP3
- ✅ OGG
- ✅ AAC
- ✅ M4A
- ✅ FLAC
- ✅ WAV
- ✅ 以及其他 FFmpeg 支持的格式
