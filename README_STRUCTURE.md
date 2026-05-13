# 项目结构整理说明

## 目标结构

项目已整理为三个主要文件夹，便于管理和维护：

```
WxMinPro/
├── wxminpro/          # 微信小程序前端
│   ├── app.js
│   ├── app.json
│   ├── pages/
│   ├── config/
│   ├── utils/
│   └── static/
│
├── backend/           # Python Flask 后端
│   ├── app.py
│   ├── deNoise.py
│   ├── requirements.txt
│   ├── database/
│   └── Audio/
│
└── test/              # 测试代码
    ├── test_api.py
    └── test_audio.py
```

## 一、前端（wxminpro/）

### 包含内容
- 所有微信小程序相关文件
- 页面代码（pages/）
- 配置文件（config/）
- 工具类（utils/）
- 静态资源（static/）

### 启动方式
1. 使用微信开发者工具打开 `wxminpro` 文件夹
2. 配置AppID
3. 点击编译运行

### 主界面
- **启动页面**：`pages/home/home`（首页）
- **功能**：包含12个功能入口按钮，系统介绍等
- **访问**：小程序启动后自动进入，或通过底部TabBar的"我的"按钮访问

## 二、后端（backend/）

### 包含内容
- Flask主应用（app.py）
- 降噪算法（deNoise.py）
- Python依赖（requirements.txt）
- 数据库文件（database/）
- 音频文件存储（Audio/）

### 启动方式
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### 服务地址
- 默认：`http://127.0.0.1:5000`
- 可在 `app.py` 中修改端口

## 三、测试（test/）

### 包含内容
- API接口测试（test_api.py）
- 音频处理测试（test_audio.py）
- 测试数据（test_data/）

### 运行方式
```bash
cd test
python test_api.py
python test_audio.py
```

## 四、启动流程

### 完整启动步骤

1. **启动后端**
   ```bash
   cd backend
   python app.py
   ```
   看到 `Running on http://127.0.0.1:5000` 表示成功

2. **启动前端**
   - 打开微信开发者工具
   - 导入 `wxminpro` 文件夹
   - 点击编译

3. **验证**
   - 后端：访问 `http://127.0.0.1:5000/api/Login`
   - 前端：在模拟器中看到首页

## 五、文件迁移

如果代码还在根目录，需要迁移：

### 快速迁移（Windows PowerShell）

```powershell
# 1. 创建文件夹
New-Item -ItemType Directory -Path "wxminpro", "backend", "test" -Force

# 2. 移动前端文件
Move-Item -Path "app.js", "app.json", "app.wxss" -Destination "wxminpro\" -Force
Move-Item -Path "pages", "config", "utils", "static" -Destination "wxminpro\" -Force
Move-Item -Path "ec-canvas", "echarts-wordcloud", "images" -Destination "wxminpro\" -Force
Move-Item -Path "project.config.json", "project.private.config.json", "sitemap.json" -Destination "wxminpro\" -Force

# 3. 移动后端文件
Move-Item -Path "app.py", "deNoise.py" -Destination "backend\" -Force
New-Item -ItemType Directory -Path "backend\database" -Force
Move-Item -Path "users.sql" -Destination "backend\database\" -Force
Move-Item -Path "Audio" -Destination "backend\" -Force

# 4. 创建requirements.txt（已创建）
# 5. 创建测试文件（已创建）
```

### 手动迁移

参考 `MIGRATION_GUIDE.md` 中的详细步骤

## 六、重要提示

1. **前端导入**：微信开发者工具导入时，必须选择 `wxminpro` 文件夹，不是根目录
2. **API配置**：前端API地址在 `wxminpro/config/api.js` 中配置
3. **数据库**：后端数据库配置在 `backend/app.py` 中
4. **路径引用**：迁移后需要检查所有路径引用是否正确

## 七、文档说明

- **快速启动**：`QUICK_START.md` - 最简明的启动步骤
- **详细启动**：`STARTUP_GUIDE.md` - 完整的启动说明
- **项目结构**：`PROJECT_STRUCTURE_NEW.md` - 详细的项目结构
- **迁移指南**：`MIGRATION_GUIDE.md` - 代码迁移步骤

## 八、主界面说明

小程序启动后会进入 **首页（home）**，这是主界面：

### 功能菜单
- 12个功能入口按钮，4列网格布局
- 点击按钮即可进入对应功能

### 系统介绍
- 功能介绍
- 应用场景
- 技术特点

### 底部TabBar
- 5个主要功能快速入口
- 音频降噪、历史记录、数据分析、用户管理、我的

## 九、下一步

1. ✅ 按照结构整理代码（参考迁移指南）
2. ✅ 启动后端服务
3. ✅ 启动前端小程序
4. ✅ 测试功能
5. ✅ 开始开发

如有问题，请查看相关文档或检查控制台错误信息。

