# 快速修复指南

## 🎯 目标
在最短时间内修复最关键的问题，确保项目可以正常运行并适合毕业设计展示。

---

## ⚡ 30分钟快速修复

### 1. 统一API调用（推荐优先级：⭐⭐⭐⭐⭐）

**问题**：27个文件硬编码API地址

**快速修复步骤**：

1. **更新 `config/api.js`**，确保包含所有接口：
```javascript
endpoints: {
  // 用户相关
  login: '/api/Login',
  loginAudio: '/api/LoginAudio',
  register: '/api/Register',
  registerAudio: '/api/RegisterAudio',
  editUser: '/api/EditUser',
  delUser: '/api/DelUser',
  receiveFaceImg: '/api/ReceiveFaceImg',
  
  // 音频相关
  getAudioInfo: '/api/getAudioInfo',
  deNoiseAudio: '/api/DeNoiseAudio',
  downloadDeNoise: '/api/DownloadDeNoise',
  separateAudio: '/api/separateAudio',
  downloadAudio: '/api/downloadAudio',
  
  // AI相关
  gpt: '/api/GPT',
  recToText: '/api/RecToText',
  createDialo: '/api/CreateDialo',
  editCsb: '/api/EditCsb',
  
  // 数据相关
  dtVisual: '/api/DtVisual',
  formPost: '/api/FormPost'
}
```

2. **使用 `utils/request.js`**（已存在，只需推广使用）

**示例改造**：
```javascript
// ❌ 旧代码
wx.request({
  url: 'http://127.0.0.1:5000/api/EditUser',
  method: 'POST',
  // ...
})

// ✅ 新代码
const { post } = require('../../utils/request.js')
post('/api/EditUser', {}, {
  showLoading: true,
  loadingText: '加载中...'
}).then(res => {
  // 处理响应
}).catch(err => {
  // 错误已自动处理
})
```

---

## 🔒 1小时安全修复

### 2. 修复SQL注入风险

**查找所有使用字符串格式化的SQL**：
```bash
# 在backend目录下搜索
grep -r "execute.*%" backend/app.py
```

**修复示例**：
```python
# ❌ 有风险
sql = "INSERT INTO users(...) VALUES ('%s', '%s')"
cursor.execute(sql % data)

# ✅ 安全
sql = "INSERT INTO users(...) VALUES (%s, %s)"
cursor.execute(sql, data)
```

**需要修复的位置**：
- `RegisterAudio` 接口（已部分修复）
- 其他使用字符串格式化的SQL语句

### 3. 限制CORS（5分钟）

```python
# backend/app.py
import os

# 开发环境
if os.getenv('FLASK_ENV') == 'development':
    CORS(app, origins=['http://127.0.0.1:5000', 'http://localhost:5000'])
else:
    # 生产环境
    CORS(app, origins=['https://your-domain.com'])
```

---

## 📦 代码重构建议（可选，1-2天）

### 4. 拆分后端代码

**创建文件结构**：
```
backend/
├── app.py
├── routes/
│   ├── __init__.py
│   ├── user.py      # 用户相关接口
│   ├── audio.py     # 音频处理接口
│   ├── ai.py        # AI聊天接口
│   └── data.py      # 数据可视化接口
└── services/
    ├── __init__.py
    └── db_service.py  # 数据库操作封装
```

**示例：`routes/user.py`**
```python
from flask import Blueprint, request, jsonify
from services.db_service import get_db_connection

user_bp = Blueprint('user', __name__)

@user_bp.route('/api/LoginAudio', methods=['POST'])
def login_audio():
    # 登录逻辑
    pass

@user_bp.route('/api/RegisterAudio', methods=['POST'])
def register_audio():
    # 注册逻辑
    pass
```

**在 `app.py` 中注册**：
```python
from routes.user import user_bp
app.register_blueprint(user_bp)
```

---

## 🛠️ 实用工具脚本

### 批量替换API地址脚本

创建 `fix_api_urls.js`：
```javascript
// 用于批量查找硬编码的API地址
// 在项目根目录运行：node fix_api_urls.js

const fs = require('fs');
const path = require('path');

function findHardcodedUrls(dir) {
  const files = fs.readdirSync(dir);
  files.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory() && !file.startsWith('.') && file !== 'node_modules') {
      findHardcodedUrls(filePath);
    } else if (file.endsWith('.js')) {
      const content = fs.readFileSync(filePath, 'utf8');
      if (content.includes('http://127.0.0.1:5000')) {
        console.log(`找到硬编码URL: ${filePath}`);
      }
    }
  });
}

findHardcodedUrls('./wxminpro');
```

---

## ✅ 检查清单

### 修复前检查
- [ ] 备份当前代码
- [ ] 确认数据库配置正确
- [ ] 确认后端服务可以正常启动

### 修复后检查
- [ ] 所有API调用使用统一配置
- [ ] 所有SQL使用参数化查询
- [ ] CORS配置正确
- [ ] 前端可以正常调用后端接口
- [ ] 用户注册/登录功能正常
- [ ] 音频处理功能正常

---

## 📝 修复优先级

### 必须修复（影响功能）
1. ✅ 统一API调用配置
2. ✅ 修复SQL注入风险
3. ✅ 确保数据库连接正常

### 应该修复（影响安全）
4. ✅ 限制CORS来源
5. ✅ 使用环境变量存储敏感信息

### 建议修复（影响维护）
6. ⚠️ 拆分后端代码
7. ⚠️ 统一错误处理
8. ⚠️ 添加日志系统

---

## 🎓 毕业设计建议

### 论文中可以强调
1. **架构设计**：前后端分离，模块化设计
2. **安全性**：参数化查询，CORS限制
3. **可维护性**：统一配置，错误处理
4. **用户体验**：现代化UI，友好提示

### 演示建议
1. 展示用户注册/登录流程
2. 演示音频降噪功能
3. 展示数据可视化
4. 演示AI聊天功能

---

**预计修复时间**：
- 快速修复：30分钟 - 1小时
- 完整修复：1-2天
- 代码重构：3-5天（可选）

