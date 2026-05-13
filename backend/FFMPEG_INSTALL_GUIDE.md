# FFmpeg 安装指南（Windows）

## 问题说明

当上传非 WAV 格式的音频文件（如 MP3、OGG 等）时，系统需要 FFmpeg 来进行格式转换。如果未安装 FFmpeg，会出现以下错误：

```
FFmpeg 不可用，无法转换 ogg 格式
```

## 解决方案

### 方案1：安装 FFmpeg 到系统 PATH（推荐）

#### 步骤1：下载 FFmpeg

1. 访问：https://www.gyan.dev/ffmpeg/builds/
2. 下载 **ffmpeg-release-essentials.zip**（约 100MB）
   - 或者访问官方下载：https://ffmpeg.org/download.html

#### 步骤2：解压 FFmpeg

1. 解压下载的 zip 文件
2. 将解压后的文件夹重命名为 `ffmpeg`
3. 移动到 `C:\ffmpeg`（或其他位置，如 `D:\ffmpeg`）

#### 步骤3：添加到系统 PATH

1. 右键点击"此电脑"（或"我的电脑"）
2. 选择"属性"
3. 点击"高级系统设置"
4. 点击"环境变量"按钮
5. 在"系统变量"区域，找到 `Path` 变量，点击"编辑"
6. 点击"新建"
7. 输入 FFmpeg 的 bin 目录路径，例如：`C:\ffmpeg\bin`
8. 点击"确定"保存所有更改

#### 步骤4：验证安装

1. **关闭当前所有终端窗口**（重要！）
2. 打开新的 PowerShell 或 CMD 窗口
3. 运行命令：
   ```powershell
   ffmpeg -version
   ```
4. 如果看到版本信息，说明安装成功

#### 步骤5：重启应用

重启 Flask 应用，系统会自动检测到 FFmpeg。

---

### 方案2：在配置文件中指定 FFmpeg 路径

如果不想添加到系统 PATH，可以在配置文件中直接指定路径：

1. 打开 `backend/config.py`
2. 找到 `FFMPEG_PATH` 配置项（约第 115 行）
3. 修改为：
   ```python
   FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"  # 替换为你的实际路径
   ```
4. 保存文件并重启应用

---

### 方案3：使用 WAV 格式（无需 FFmpeg）

如果暂时无法安装 FFmpeg，可以：

1. 将音频文件转换为 WAV 格式后再上传
2. 使用在线转换工具：https://convertio.co/zh/audio-converter/
3. 或使用音频编辑软件（如 Audacity）导出为 WAV 格式

---

## 快速检查

运行以下命令检查 FFmpeg 是否已正确安装：

```powershell
# 检查 FFmpeg 是否在 PATH 中
ffmpeg -version

# 如果不在 PATH 中，检查常见安装位置
Test-Path "C:\ffmpeg\bin\ffmpeg.exe"
Test-Path "D:\ffmpeg\bin\ffmpeg.exe"
```

---

## 常见问题

### Q: 添加 PATH 后仍然找不到 FFmpeg？

**A:** 确保：
1. 已关闭所有终端窗口并重新打开
2. PATH 路径正确（指向 `bin` 目录，不是 `ffmpeg` 根目录）
3. 使用方案2，直接在配置文件中指定完整路径

### Q: 如何确认 FFmpeg 路径？

**A:** 在文件资源管理器中，找到 `ffmpeg.exe` 文件，右键 -> 属性 -> 查看"位置"路径

### Q: 可以使用其他版本的 FFmpeg 吗？

**A:** 可以，只要确保是 Windows 版本即可。推荐使用 essentials 版本（体积较小）。

---

## 安装完成后

安装完成后，重启 Flask 应用，你应该会看到：

```
[成功] FFmpeg 已配置: C:\ffmpeg\bin\ffmpeg.exe
```

然后就可以正常上传和处理非 WAV 格式的音频文件了！
