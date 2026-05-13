# 音频降噪系统

基于微信小程序的音频降噪系统，采用巴特沃斯滤波器算法进行高质量音频降噪处理。

## 📁 项目结构

```
WxMinPro/
├── wxminpro/          # 微信小程序前端 ⭐
├── backend/           # Python Flask 后端 ⭐
└── test/              # 测试代码
```

## 🚀 快速启动

### 1. 启动后端

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### 2. 启动前端

1. 打开微信开发者工具
2. 导入项目 → **选择 `wxminpro` 文件夹**
3. 点击编译运行

### 3. 配置（首次需要）

- **数据库**：修改 `backend/app.py` 中的数据库连接
- **微信工具路径**：修改 `backend/app.py` 中的 `WX_TEMP_DIR`

## 📖 详细文档

- **从这里开始**：`START_HERE.md` ⭐
- **快速启动**：`QUICK_START.md`
- **详细启动**：`STARTUP_GUIDE.md`
- **项目结构**：`PROJECT_STRUCTURE_NEW.md`
- **迁移报告**：`MIGRATION_COMPLETE.md`

## ✨ 主要功能

1. **用户管理**：注册、登录、信息维护
2. **音频降噪**：基于巴特沃斯滤波器算法
3. **音频分离**：分离人声、伴奏、鼓声、贝斯
4. **AI聊天**：ChatGPT和GPT实时聊天
5. **历史记录**：查看处理历史
6. **数据可视化**：多维度数据分析

## 🛠️ 技术栈

- **前端**：微信小程序
- **后端**：Python Flask
- **数据库**：MySQL
- **算法**：巴特沃斯滤波器（scipy）

## 📝 注意事项

1. 前端导入时必须选择 `wxminpro` 文件夹
2. 首次使用需要配置数据库和微信工具路径
3. 确保MySQL数据库已启动
4. 开发环境需勾选"不校验合法域名"

## 📚 更多信息

查看 `START_HERE.md` 开始使用！
