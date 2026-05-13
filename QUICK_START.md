# 快速启动指南

## 一、项目结构

项目已整理为三个主要文件夹：

```
WxMinPro/
├── wxminpro/     # 微信小程序前端（所有前端代码）
├── backend/      # Python Flask 后端（所有后端代码）
└── test/         # 测试代码
```

## 二、后端启动（Python Flask）

### 步骤1：进入后端目录
```bash
cd backend
```

### 步骤2：安装依赖
```bash
pip install -r requirements.txt
```

### 步骤3：配置数据库
1. 启动MySQL数据库
2. 创建数据库：`chatgpt`
3. 导入数据：
   ```bash
   mysql -u root -p chatgpt < database/users.sql
   ```
4. 修改 `app.py` 中的数据库连接配置

### 步骤4：启动后端服务
```bash
python app.py
```

**成功标志**：看到 `Running on http://127.0.0.1:5000`

## 三、前端启动（微信小程序）

### 步骤1：打开微信开发者工具
- 下载安装：https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html

### 步骤2：导入项目
1. 打开微信开发者工具
2. 选择"导入项目"
3. **项目目录选择**：`wxminpro` 文件夹（不是根目录！）
4. 输入AppID（或选择测试号）
5. 点击"导入"

### 步骤3：配置API地址
1. 打开 `wxminpro/config/api.js`
2. 确认 `baseURL` 为：`http://127.0.0.1:5000`

### 步骤4：启动项目
1. 点击"编译"按钮
2. 等待编译完成
3. 在模拟器中查看效果

### 步骤5：真机调试（可选）
1. 点击"预览"按钮
2. 使用微信扫码在手机上查看

## 四、主界面说明

小程序启动后会进入**首页（home）**，这是主界面，包含：

1. **功能菜单**：12个功能入口按钮
   - 音频降噪、音频分离、录音功能
   - ChatGPT、GPT聊天、创建对话
   - 电话功能、音频登录、音频注册
   - 历史记录等

2. **系统介绍**：功能说明和应用场景

3. **底部TabBar**：5个主要功能快速入口
   - 音频降噪
   - 历史记录
   - 数据分析
   - 用户管理
   - 我的

## 五、启动顺序

### 开发环境
1. ✅ 启动MySQL数据库
2. ✅ 启动后端服务（`python backend/app.py`）
3. ✅ 打开微信开发者工具，导入 `wxminpro` 项目
4. ✅ 点击编译运行

### 验证启动成功
- **后端**：访问 `http://127.0.0.1:5000/api/Login` 应该返回数据
- **前端**：在模拟器中看到首页界面

## 六、常见问题

### Q1: 前端无法连接后端
**解决**：
1. 检查后端是否启动（应该看到 `Running on http://127.0.0.1:5000`）
2. 检查 `wxminpro/config/api.js` 中的 `baseURL` 是否正确
3. 在微信开发者工具中：设置 → 项目设置 → 勾选"不校验合法域名"

### Q2: 数据库连接失败
**解决**：
1. 检查MySQL是否启动
2. 检查 `backend/app.py` 中的数据库配置
3. 检查数据库用户权限

### Q3: 页面空白
**解决**：
1. 检查控制台错误信息
2. 确认导入的是 `wxminpro` 文件夹，不是根目录
3. 检查所有文件是否完整

### Q4: 音频处理失败
**解决**：
1. 检查 `backend/Audio` 目录是否存在
2. 检查目录权限（确保可读写）
3. 检查依赖包是否安装完整

## 七、项目迁移

如果当前代码还在根目录，需要迁移到新结构：

**方法1：手动迁移**
参考 `MIGRATION_GUIDE.md` 中的详细步骤

**方法2：使用脚本（Windows PowerShell）**
```powershell
# 创建文件夹
New-Item -ItemType Directory -Path "wxminpro", "backend", "test" -Force

# 移动前端文件
Move-Item -Path "app.js", "app.json", "app.wxss", "project.config.json", "pages", "config", "utils", "static", "ec-canvas", "echarts-wordcloud", "images" -Destination "wxminpro\" -Force

# 移动后端文件
Move-Item -Path "app.py", "deNoise.py" -Destination "backend\" -Force
New-Item -ItemType Directory -Path "backend\database" -Force
Move-Item -Path "users.sql" -Destination "backend\database\" -Force
Move-Item -Path "Audio" -Destination "backend\" -Force
```

## 八、详细文档

- **启动指南**：`STARTUP_GUIDE.md` - 详细的启动说明
- **项目结构**：`PROJECT_STRUCTURE_NEW.md` - 新的项目结构说明
- **迁移指南**：`MIGRATION_GUIDE.md` - 代码迁移步骤
- **功能菜单**：`FUNCTION_MENU.md` - 功能说明

## 九、测试

### 测试后端API
```bash
cd test
python test_api.py
```

### 测试音频处理
```bash
cd test
python test_audio.py
```

## 十、下一步

1. ✅ 按照上述步骤启动前后端
2. ✅ 测试基本功能
3. ✅ 根据需要调整配置
4. ✅ 开始开发新功能

祝您使用愉快！

