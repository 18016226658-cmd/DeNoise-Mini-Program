# 前后端修复说明

## 修复内容

### 1. 前端API配置统一 ✅

**问题**：前端代码中硬编码了API地址 `http://127.0.0.1:5000`

**修复**：
- 修改 `wxminpro/pages/DeNoise/DeNoise.js`
- 统一使用 `config/api.js` 中的配置
- 所有API调用改为：`apiConfig.baseURL + apiConfig.endpoints.xxx`

**修改位置**：
- `getAudioInfo` API调用
- `DeNoiseAudio` API调用  
- `DownloadDeNoise` API调用

### 2. 后端数据库配置统一 ✅

**问题**：数据库配置分散在多个地方，硬编码

**修复**：
- 创建 `backend/db_config.py` 统一管理数据库配置
- 修改 `backend/app.py` 导入并使用统一配置
- 所有数据库连接使用 `DB_CONFIG`

**配置项**：
```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123456',  # ⚠️ 请修改为实际密码
    'database': 'audio',
    'charset': 'utf8mb4'
}
```

### 3. 数据库连接优化 ✅

**修改**：
- 统一字符集为 `utf8mb4`（支持emoji和特殊字符）
- 统一数据库名为 `audio`（根据实际情况可修改）

### 4. 前端页面完整性 ✅

**检查结果**：
- ✅ `DeNoise.wxml` - 页面结构完整
- ✅ `DeNoise.wxss` - 样式完整美观
- ✅ `DeNoise.js` - 功能逻辑完整

## 使用说明

### 1. 配置数据库

编辑 `backend/db_config.py`：
```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'your_password',  # 修改为实际密码
    'database': 'audio',  # 或 'chatgpt'
    'charset': 'utf8mb4'
}
```

### 2. 创建数据库

```bash
# 使用统一建库脚本
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS audio DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"
mysql -u root -p audio < backend/database/zy.sql
```

### 3. 启动后端

```bash
cd backend
python app.py
```

### 4. 启动前端

- 使用微信开发者工具打开 `wxminpro` 文件夹
- 确保API地址正确（`config/api.js` 中配置）
- 在开发者工具中勾选"不校验合法域名"（开发环境）

## 注意事项

1. **数据库密码**：务必修改 `backend/db_config.py` 中的密码
2. **微信工具路径**：如果音频处理失败，检查 `backend/app.py` 中的 `WX_TEMP_DIR`
3. **API地址**：确保前端 `config/api.js` 中的 `baseURL` 与后端一致
4. **数据库名称**：确保 `db_config.py` 中的 `database` 与建库脚本一致

## 验证步骤

1. ✅ 后端启动成功：`Running on http://127.0.0.1:5000`
2. ✅ 前端编译成功：无错误提示
3. ✅ 数据库连接：后端日志无连接错误
4. ✅ API调用：前端能正常调用后端接口

## 后续优化建议

1. **环境变量**：将敏感配置（密码等）移到环境变量
2. **错误处理**：增强前后端错误提示
3. **日志系统**：添加详细的日志记录
4. **API文档**：生成API接口文档

