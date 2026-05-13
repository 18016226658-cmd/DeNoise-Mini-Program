# FFmpeg 快速安装指南

## 🚀 方法1：使用自动安装脚本（最简单）

### PowerShell 脚本

1. **以管理员身份运行 PowerShell**
   - 按 `Win + X`
   - 选择"Windows PowerShell (管理员)"

2. **运行安装脚本**
   ```powershell
   cd D:\WxMinPro\WxMinPro\backend
   .\install_ffmpeg.ps1
   ```

3. **脚本会自动完成**：
   - ✅ 下载 FFmpeg
   - ✅ 解压到 C:\ffmpeg
   - ✅ 添加到系统 PATH
   - ✅ 验证安装

### 批处理脚本（如果 PowerShell 无法运行）

1. **以管理员身份运行 CMD**
   - 按 `Win + X`
   - 选择"命令提示符 (管理员)"

2. **运行安装脚本**
   ```cmd
   cd D:\WxMinPro\WxMinPro\backend
   install_ffmpeg.bat
   ```

---

## 📥 方法2：手动安装（如果脚本失败）

### 步骤1：下载 FFmpeg

**方式A：浏览器下载（推荐）**

1. 打开浏览器，访问：**https://www.gyan.dev/ffmpeg/builds/**
2. 找到 **"ffmpeg-release-essentials.zip"** 并下载
   - 文件大小：约 100MB
   - 这是 Windows 版本，已经编译好，无需编译

**方式B：直接下载链接**

如果上面的页面无法访问，可以尝试：
- https://github.com/BtbN/FFmpeg-Builds/releases
- 下载 `ffmpeg-master-latest-win64-gpl.zip`

### 步骤2：解压 FFmpeg

1. 找到下载的 `ffmpeg-release-essentials.zip` 文件
2. 右键点击 → "解压到当前文件夹" 或使用解压软件解压
3. 解压后会得到一个文件夹，例如：`ffmpeg-7.0-essentials_build`
4. 将这个文件夹**重命名**为 `ffmpeg`
5. 将 `ffmpeg` 文件夹**移动**到 `C:\` 目录下
   - 最终路径应该是：`C:\ffmpeg\bin\ffmpeg.exe`

### 步骤3：添加到系统 PATH

#### 方法A：图形界面（推荐）

1. 按 `Win + R`，输入 `sysdm.cpl`，回车
2. 点击"高级"选项卡
3. 点击"环境变量"按钮
4. 在"用户变量"区域，找到 `Path` 变量
5. 点击"编辑"
6. 点击"新建"
7. 输入：`C:\ffmpeg\bin`
8. 点击"确定"保存所有更改

#### 方法B：PowerShell 命令

```powershell
# 以管理员身份运行 PowerShell，然后执行：
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

1. **关闭所有终端窗口**（重要！）
2. 打开新的 PowerShell 或 CMD
3. 运行：
   ```powershell
   ffmpeg -version
   ```
4. 如果看到版本信息，说明安装成功！

### 步骤5：重启应用

重启 Flask 应用，系统会自动检测到 FFmpeg。

---

## 🔍 验证安装

运行以下命令检查：

```powershell
# 检查 FFmpeg 命令
ffmpeg -version

# 检查文件是否存在
Test-Path "C:\ffmpeg\bin\ffmpeg.exe"

# 检查 PATH
$env:Path -split ';' | Select-String "ffmpeg"
```

---

## ⚠️ 常见问题

### Q1: 脚本执行被阻止？

**解决方法**：
```powershell
# 临时允许执行（仅当前会话）
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

### Q2: 下载速度慢？

**解决方法**：
- 使用浏览器直接下载
- 或使用下载工具（如 IDM、迅雷）
- 下载后手动解压和配置

### Q3: 添加到 PATH 后仍然找不到？

**解决方法**：
1. 确保已关闭所有终端并重新打开
2. 检查路径是否正确：`C:\ffmpeg\bin`（不是 `C:\ffmpeg`）
3. 尝试重启计算机
4. 或在配置文件中手动指定路径（见下方）

---

## 📝 备选方案：在配置文件中指定路径

如果不想添加到系统 PATH，可以在配置文件中直接指定：

1. 打开 `backend/config.py`
2. 找到第 114 行左右的 `FFMPEG_PATH`
3. 修改为：
   ```python
   FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"
   ```
4. 保存并重启应用

---

## ✅ 安装完成后的验证

安装完成后，重启 Flask 应用，应该会看到：

```
[成功] FFmpeg 已配置: C:\ffmpeg\bin\ffmpeg.exe
```

然后就可以处理所有格式的音频文件了！

---

## 📚 相关文档

- `FFMPEG_INSTALL_GUIDE.md` - 详细安装指南
- `INSTALL_FFMPEG_GUIDE.md` - 完整安装说明
- `AUDIO_CONVERSION_ALTERNATIVES.md` - 备选方案（soundfile）
