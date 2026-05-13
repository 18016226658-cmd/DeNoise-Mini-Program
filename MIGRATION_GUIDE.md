# 项目迁移指南

## 说明

本指南帮助您将现有项目代码整理到新的文件夹结构中。

## 目标结构

```
WxMinPro/
├── wxminpro/     # 微信小程序前端
├── backend/      # Python Flask 后端
└── test/         # 测试代码
```

## 迁移步骤

### 一、创建文件夹结构

在项目根目录下创建三个文件夹：

```bash
mkdir wxminpro
mkdir backend
mkdir test
```

### 二、迁移前端代码

#### 1. 移动小程序核心文件
```bash
# 移动核心文件
mv app.js wxminpro/
mv app.json wxminpro/
mv app.wxss wxminpro/
mv project.config.json wxminpro/
mv project.private.config.json wxminpro/
mv sitemap.json wxminpro/
```

#### 2. 移动页面和资源
```bash
# 移动页面
mv pages wxminpro/
mv config wxminpro/
mv utils wxminpro/
mv static wxminpro/
mv ec-canvas wxminpro/
mv echarts-wordcloud wxminpro/
mv images wxminpro/
```

### 三、迁移后端代码

#### 1. 移动Python文件
```bash
# 移动主应用文件
mv app.py backend/

# 移动降噪算法文件
mv deNoise.py backend/
mv deNoise-all.py backend/  # 如果使用

# 移动其他相关Python文件（根据需要）
# mv createDialo.py backend/
# mv csb.py backend/
```

#### 2. 创建requirements.txt
```bash
cd backend
# 已创建 requirements.txt
```

#### 3. 移动数据库文件
```bash
mkdir backend/database
mv users.sql backend/database/
mv chatgpt.sql backend/database/  # 如果存在
mv audio2.sql backend/database/   # 如果存在
```

#### 4. 移动音频文件目录
```bash
mv Audio backend/
```

### 四、创建测试文件夹

#### 1. 移动测试文件
```bash
# 移动测试Python文件
mv test*.py test/
mv t*.py test/  # 测试文件
```

#### 2. 创建测试数据目录
```bash
mkdir test/test_data
# 可以放入测试音频文件
```

### 五、清理不需要的文件

根据 `DELETE_FILES.md` 中的清单，删除不需要的文件。

### 六、更新路径引用

#### 1. 前端路径更新
- `wxminpro/config/api.js` - 确保API地址正确
- 检查所有页面中的相对路径引用

#### 2. 后端路径更新
- `backend/app.py` - 更新文件路径引用
  ```python
  # 更新音频文件路径
  TEMP_DIR = 'Audio/download'
  
  # 更新数据库连接（如果需要）
  ```

### 七、验证迁移

#### 1. 测试后端
```bash
cd backend
python app.py
# 检查是否正常启动
```

#### 2. 测试前端
- 使用微信开发者工具打开 `wxminpro` 文件夹
- 检查是否能正常编译
- 检查页面是否能正常显示

#### 3. 测试API连接
- 运行 `test/test_api.py`
- 检查API是否正常响应

## 注意事项

1. **备份**：迁移前请先备份整个项目
2. **路径**：确保所有路径引用都已更新
3. **依赖**：确保所有依赖包都已安装
4. **数据库**：确保数据库连接配置正确
5. **文件权限**：确保Audio目录有读写权限

## 快速迁移脚本（Windows PowerShell）

```powershell
# 创建文件夹
New-Item -ItemType Directory -Path "wxminpro", "backend", "test" -Force

# 移动前端文件
Move-Item -Path "app.js", "app.json", "app.wxss", "project.config.json", "project.private.config.json", "sitemap.json" -Destination "wxminpro\" -Force
Move-Item -Path "pages", "config", "utils", "static", "ec-canvas", "echarts-wordcloud", "images" -Destination "wxminpro\" -Force

# 移动后端文件
Move-Item -Path "app.py", "deNoise.py" -Destination "backend\" -Force
New-Item -ItemType Directory -Path "backend\database" -Force
Move-Item -Path "users.sql" -Destination "backend\database\" -Force
Move-Item -Path "Audio" -Destination "backend\" -Force

# 移动测试文件
Move-Item -Path "test*.py" -Destination "test\" -Force
```

## 迁移后检查清单

- [ ] 前端文件已移动到 `wxminpro/`
- [ ] 后端文件已移动到 `backend/`
- [ ] 测试文件已移动到 `test/`
- [ ] 数据库文件已移动到 `backend/database/`
- [ ] 音频文件目录已移动到 `backend/Audio/`
- [ ] API配置路径已更新
- [ ] 后端文件路径引用已更新
- [ ] 后端可以正常启动
- [ ] 前端可以正常编译
- [ ] API连接正常

完成迁移后，请按照 [STARTUP_GUIDE.md](./STARTUP_GUIDE.md) 中的说明启动项目。

