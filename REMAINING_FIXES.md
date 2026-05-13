# 剩余修复工作指南

## 📋 待修复文件清单

### 前端API统一化（13个文件）

#### 1. `wxminpro/subpackages/other/pages/telphone/telphone.js`
```javascript
// 添加
const { post } = require('../../../../utils/request.js')
const apiConfig = require('../../../../config/api.js')

// 替换
url: 'http://127.0.0.1:5000/api/FormPost'
// 改为
post(apiConfig.endpoints.formPost, {...})
```

#### 2. `wxminpro/subpackages/ai/pages/EditCsb/EditCsb.js`
```javascript
// 添加
const { post } = require('../../../../utils/request.js')
const apiConfig = require('../../../../config/api.js')

// 替换
url: 'http://127.0.0.1:5000/api/EditCsb'
// 改为
post(apiConfig.endpoints.editCsb, {...})
```

#### 3. `wxminpro/subpackages/ai/pages/CreateDialo/createDialo.js`
```javascript
// 添加
const { post } = require('../../../../utils/request.js')
const apiConfig = require('../../../../config/api.js')

// 替换
url: "http://127.0.0.1:5000/api/CreateDialo"
// 改为
post(apiConfig.endpoints.createDialo, {})
```

#### 4. `wxminpro/pages/DtLine/DtLine.js`
```javascript
// 添加
const { post } = require('../../utils/request.js')
const apiConfig = require('../../config/api.js')

// 替换
url: "http://127.0.0.1:5000/api/DtVisual"
// 改为
post(apiConfig.endpoints.dtVisual, {})
```

#### 5-13. 其他文件
按照相同模式修复：
- `wxminpro/subpackages/user/pages/register/register.js`
- `wxminpro/subpackages/audio/pages/AudioSep/AudioSep.js`
- `wxminpro/subpackages/ai/pages/chatGPT/chatGPT.js`
- `wxminpro/subpackages/user/pages/login/login.js`
- `wxminpro/subpackages/audio/pages/soundRecord/soundRecord.js`
- `wxminpro/subpackages/user/pages/EditUser/EditUser.js`
- `wxminpro/subpackages/user/pages/DelUser/DelUser.js`
- 其他相关文件

---

## 🔧 修复模板

### 标准POST请求
```javascript
// 1. 导入
const { post } = require('../../utils/request.js')  // 调整路径
const apiConfig = require('../../config/api.js')    // 调整路径

// 2. 替换
post(apiConfig.endpoints.xxx, data, {
  showLoading: true,
  loadingText: '加载中...',
  header: {
    'content-type': 'application/json'  // 或 'application/x-www-form-urlencoded'
  }
}).then(res => {
  // 处理响应
}).catch(err => {
  // 错误已自动处理
})
```

### 文件上传
```javascript
const { uploadFile } = require('../../utils/request.js')
const apiConfig = require('../../config/api.js')

uploadFile(filePath, apiConfig.endpoints.receiveFaceImg, formData, options)
  .then(res => {...})
  .catch(err => {...})
```

---

## 🎯 优先级建议

### 高优先级（立即修复）
1. ✅ 已修复：My.js, LoginAudio.js, registerAudio.js
2. ⚠️ 待修复：CreateDialo.js, EditCsb.js, DtLine.js（核心功能）

### 中优先级（1-2天内）
3. ⚠️ 待修复：chatGPT.js, AudioSep.js, soundRecord.js（主要功能）

### 低优先级（有时间再修复）
4. ⚠️ 待修复：其他辅助页面

---

## ✅ 已完成的修复

1. ✅ API配置完善（config/api.js）
2. ✅ 请求工具改进（utils/request.js）
3. ✅ 3个关键文件已修复
4. ✅ CORS安全性修复
5. ✅ SQL注入防护
6. ✅ 后端路由框架创建

---

**预计剩余工作量**：2-3小时

