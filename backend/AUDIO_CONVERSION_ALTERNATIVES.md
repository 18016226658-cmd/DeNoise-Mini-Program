# 音频格式转换备选方案（无需 FFmpeg）

## 概述

如果不想安装 FFmpeg，可以使用纯 Python 库来处理部分音频格式。但请注意，这种方法**仅支持有限格式**。

## 支持的格式

使用 `soundfile` 库可以处理：
- ✅ **OGG** (Ogg Vorbis)
- ✅ **FLAC** (无损音频)
- ✅ **WAV** (已原生支持)

**不支持**：
- ❌ MP3（需要 FFmpeg）
- ❌ AAC（需要 FFmpeg）
- ❌ M4A（需要 FFmpeg）

## 安装方法

### 方案1：仅安装 soundfile（推荐，如果只需要处理 OGG/FLAC）

```powershell
cd D:\WxMinPro\WxMinPro\backend
pip install soundfile
```

### 方案2：安装完整音频处理库套件

```powershell
cd D:\WxMinPro\WxMinPro\backend
pip install soundfile numpy scipy
```

## 工作原理

1. **优先尝试 FFmpeg**：如果系统已安装 FFmpeg，优先使用（支持所有格式）
2. **回退到 soundfile**：如果 FFmpeg 不可用，尝试使用 `soundfile` 处理支持的格式
3. **错误提示**：如果都不支持，会提示用户安装 FFmpeg 或转换为 WAV

## 使用限制

### soundfile 的限制

- **仅支持部分格式**：OGG、FLAC、WAV
- **不支持 MP3**：MP3 格式仍需要 FFmpeg
- **可能的功能限制**：某些高级音频处理功能可能不如 FFmpeg 完善

### 推荐方案

- **如果只需要处理 OGG/FLAC**：安装 `soundfile` 即可
- **如果需要处理 MP3/AAC/M4A**：必须安装 FFmpeg
- **如果处理多种格式**：建议安装 FFmpeg（最全面）

## 验证安装

安装 `soundfile` 后，重启应用，系统会自动检测并使用它。

## 代码自动处理

代码已经实现了自动回退机制：

1. 首先尝试使用 FFmpeg（如果可用）
2. 如果 FFmpeg 不可用，尝试使用 `soundfile`
3. 如果都不支持，返回友好的错误提示

## 总结

| 方案 | 安装方式 | 支持格式 | 推荐度 |
|------|---------|---------|--------|
| FFmpeg | 手动下载安装 | 所有格式 | ⭐⭐⭐⭐⭐ |
| soundfile | `pip install soundfile` | OGG, FLAC, WAV | ⭐⭐⭐ |
| 转换为 WAV | 在线工具/软件 | WAV | ⭐⭐ |

**建议**：如果可能，还是安装 FFmpeg 以获得最佳兼容性。
