# 后端崩溃问题修复指南

## 问题描述

直接运行 `app.py` 时出现崩溃，退出代码：`-1073741819 (0xC0000005)`

这是一个**访问违规错误**，通常由以下原因引起：

1. **音频处理库初始化问题**：`pydub` 需要 `ffmpeg`，如果未正确安装会导致崩溃
2. **matplotlib 后端问题**：matplotlib 在某些 Windows 环境下可能导致问题
3. **C扩展库冲突**：numpy、scipy 等库的版本不兼容

## 解决方案

### ✅ 方案1：使用 run.py 启动（推荐）

**不要直接运行 `app.py`，而是使用 `run.py`：**

```bash
cd D:\kksyc1\WxMinPro\backend
python -u run.py
```

`run.py` 提供了更好的错误处理和输出缓冲控制。

### ✅ 方案2：检查 ffmpeg 安装

`pydub` 需要 `ffmpeg` 才能正常工作。检查是否已安装：

```bash
ffmpeg -version
```

如果未安装，请：
1. 下载 ffmpeg：https://ffmpeg.org/download.html
2. 解压到某个目录（如 `C:\ffmpeg`）
3. 将 `C:\ffmpeg\bin` 添加到系统 PATH 环境变量
4. 重启终端并验证：`ffmpeg -version`

### ✅ 方案3：延迟导入音频处理库

如果必须直接运行 `app.py`，可以修改代码，延迟导入可能有问题的库：

```python
# 在函数内部导入，而不是在模块级别
def some_audio_function():
    from pydub import AudioSegment
    # ... 使用 AudioSegment
```

### ✅ 方案4：设置 matplotlib 后端

在导入 matplotlib 之前设置非 GUI 后端：

```python
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
```

## 已修复的问题

1. ✅ `app.py` 的 `if __name__ == '__main__'` 块添加了异常处理
2. ✅ 添加了 `use_reloader=False` 参数，避免重载导致的崩溃
3. ✅ 添加了提示信息，建议使用 `run.py`

## 推荐启动方式

**始终使用 `run.py` 启动服务器：**

```bash
cd D:\kksyc1\WxMinPro\backend
python -u run.py
```

这样可以：
- 获得更好的错误处理
- 看到完整的启动日志
- 避免某些库初始化问题

## 如果仍然崩溃

1. **检查依赖库版本**：
   ```bash
   pip list | findstr "pydub numpy scipy matplotlib"
   ```

2. **重新安装可能有问题的库**：
   ```bash
   pip uninstall pydub numpy scipy matplotlib
   pip install pydub numpy scipy matplotlib
   ```

3. **检查 Python 版本**：
   ```bash
   python --version
   ```
   建议使用 Python 3.8-3.11

4. **查看详细错误信息**：
   使用 `run.py` 启动可以看到更详细的错误信息

## 测试

启动后，在浏览器中访问：
```
http://127.0.0.1:5000/api/DeNoiseAudio
```

如果返回 405 Method Not Allowed（而不是 404），说明服务器正常运行。

