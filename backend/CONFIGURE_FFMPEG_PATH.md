# 配置 FFmpeg 到系统 PATH

## 🚀 快速配置（推荐）

### 方法1：使用 PowerShell 脚本

1. **以管理员身份运行 PowerShell**
   - 按 `Win + X`
   - 选择"Windows PowerShell (管理员)"

2. **运行配置脚本**
   ```powershell
   cd D:\WxMinPro\WxMinPro\backend
   .\add_ffmpeg_to_path.ps1
   ```

3. **脚本会自动完成**：
   - ✅ 检查 FFmpeg 路径是否存在
   - ✅ 添加到用户 PATH 环境变量
   - ✅ 验证配置
   - ✅ 测试 FFmpeg 命令

### 方法2：使用批处理脚本

1. **以管理员身份运行 CMD**
   - 按 `Win + X`
   - 选择"命令提示符 (管理员)"

2. **运行配置脚本**
   ```cmd
   cd D:\WxMinPro\WxMinPro\backend
   add_ffmpeg_to_path.bat
   ```

---

## 📝 手动配置步骤

如果脚本无法运行，可以手动配置：

### 步骤1：打开环境变量设置

1. 按 `Win + R`
2. 输入 `sysdm.cpl`，回车
3. 点击"高级"选项卡
4. 点击"环境变量"按钮

### 步骤2：添加到用户 PATH

1. 在"用户变量"区域，找到 `Path` 变量
2. 点击"编辑"
3. 点击"新建"
4. 输入：`C:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin`
5. 点击"确定"保存所有更改

### 步骤3：验证配置

1. **关闭所有终端窗口**（重要！）
2. 打开新的 PowerShell 或 CMD
3. 运行：
   ```powershell
   ffmpeg -version
   ```
4. 如果看到版本信息，说明配置成功！

---

## 🔍 验证配置

运行以下命令验证：

```powershell
# 检查 FFmpeg 命令
ffmpeg -version

# 检查 PATH 环境变量
$env:Path -split ';' | Select-String "ffmpeg"

# 检查文件是否存在
Test-Path "C:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"
```

---

## ⚠️ 常见问题

### Q1: 脚本执行被阻止？

**解决方法**：
```powershell
# 临时允许执行（仅当前会话）
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

### Q2: 添加到 PATH 后仍然找不到？

**解决方法**：
1. **必须关闭所有终端窗口并重新打开**
2. 检查路径是否正确：`C:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin`
3. 尝试重启计算机
4. 或在配置文件中直接指定路径（见下方）

---

## 📝 备选方案：在配置文件中指定路径

如果环境变量配置有问题，可以在配置文件中直接指定：

1. 打开 `backend/config.py`
2. 找到第 114 行左右的 `FFMPEG_PATH`
3. 修改为：
   ```python
   FFMPEG_PATH = r"C:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"
   ```
4. 保存文件

**注意**：代码已经支持自动检测这个路径，所以即使环境变量有问题，也能正常工作。

---

## ✅ 配置完成后的验证

配置完成后，重启 Flask 应用：

```powershell
cd D:\WxMinPro\WxMinPro\backend
python .\app.py
```

你应该会看到：

```
[信息] 自动检测到 FFmpeg 路径: C:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe
[成功] FFmpeg 已配置: C:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe
[成功] 音频路由模块已注册
```

然后就可以处理所有格式的音频文件了！
