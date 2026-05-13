# 功能验证清单

## 后端检查 ✅

### 1. 核心API接口
- [x] `/api/uploadAudio` (POST) - 上传音频文件 ✅ **已添加**
- [x] `/api/getAudioInfo` (POST) - 获取音频信息 ✅
- [x] `/api/DeNoiseAudio` (POST) - 音频降噪 ✅
- [x] `/api/separateAudio` (POST) - 音频分离 ✅
- [x] `/api/DownloadDeNoise` (GET/POST) - 下载降噪文件 ✅
- [x] `/api/download/separated/<path>` (GET) - 下载分离文件 ✅
- [x] `/api/audio/play/<filename>` (GET) - 播放音频 ✅

### 2. 路由注册
- [x] `api.audio` 蓝图已注册 ✅
- [x] `routes.user` 蓝图已注册 ✅
- [x] `routes.statistics` 蓝图已注册 ✅

### 3. 目录结构
- [x] `backend/Audio/input` - 输入目录 ✅
- [x] `backend/Audio/output` - 输出目录 ✅
- [x] `backend/Audio/uploads` - 上传目录 ✅
- [x] `backend/Audio/download` - 下载目录 ✅

## 前端检查 ✅

### 1. 页面配置
- [x] `app.json` 配置正确 ✅
- [x] tabBar配置正确（5个tab） ✅
- [x] 主包页面已配置 ✅

### 2. 核心功能页面
- [x] `pages/DeNoise/DeNoise.js` - 降噪页面 ✅
- [x] `subpackages/audio/pages/AudioSep/AudioSep.js` - 分离页面 ✅
- [x] `pages/UserInfo/UserInfo.js` - 用户信息页面 ✅
- [x] `pages/AdminVisualization/AdminVisualization.js` - 可视化页面 ✅

### 3. API调用
- [x] 降噪页面调用 `/api/uploadAudio` ✅
- [x] 降噪页面调用 `/api/DeNoiseAudio` ✅
- [x] 分离页面调用 `/api/uploadAudio` ✅
- [x] 分离页面调用 `/api/separateAudio` ✅

## 功能测试步骤

### 测试1: 音频降噪功能

1. **启动后端**
   ```bash
   cd backend
   python app.py
   ```

2. **打开小程序**
   - 在微信开发者工具中打开 `wxminpro` 项目
   - 登录系统（管理员：18016226658 / zy6658）

3. **测试降噪**
   - 点击底部"音频降噪"tab
   - 点击"选择音频文件"
   - 选择音频文件（wav/mp3/ogg等）
   - 等待上传完成
   - 点击"开始降噪"
   - 等待处理完成
   - 试听降噪后的音频
   - 下载降噪后的文件

**预期结果**: ✅ 所有步骤成功完成

### 测试2: 音频分离功能

1. **确保后端运行**

2. **测试分离**
   - 从首页点击"音频分离"
   - 选择音频文件
   - 等待上传完成
   - 点击"开始分离"
   - 等待处理完成（可能需要几分钟）
   - 试听各个音轨（人声、伴奏、鼓、贝斯）
   - 下载各个音轨文件

**预期结果**: ✅ 所有步骤成功完成

**注意**: 分离功能需要安装 demucs
```bash
pip install demucs
```

## 已知问题和解决方案

### 问题1: ERR_CONNECTION_REFUSED
**解决方案**: 确保后端服务已启动
```bash
cd backend
python app.py
```

### 问题2: 上传失败
**检查项**:
- 后端服务是否运行
- 文件格式是否支持（wav, mp3, ogg, aac, flac, m4a）
- 文件大小是否合理（建议 < 50MB）

### 问题3: 降噪/分离失败
**检查项**:
- 查看后端日志
- 检查音频文件格式
- 检查磁盘空间
- 对于分离：确保已安装 demucs

## 系统状态总结

✅ **后端**: 所有核心接口已实现并注册
✅ **前端**: 所有核心页面已配置
✅ **上传功能**: 接口已添加
✅ **降噪功能**: 前后端对接正常
✅ **分离功能**: 前后端对接正常

**系统已就绪，可以正常使用！**


