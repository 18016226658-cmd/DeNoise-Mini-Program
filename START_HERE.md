# 🚀 从这里开始

## 项目迁移完成 ✅

项目文件已成功迁移到新的文件夹结构中！

## 📁 新的项目结构

```
WxMinPro/
├── wxminpro/     # 微信小程序前端 ⭐
├── backend/      # Python Flask 后端 ⭐
└── test/         # 测试代码
```

## 🎯 快速启动（4步）

### 第0步：安装数据库（首次需要）⭐

**方法1：使用自动安装脚本（推荐）**
```bash
# Windows PowerShell
cd backend/database
.\install.ps1

# Windows CMD
cd backend/database
install.bat
```

**方法2：手动安装**
```bash
# 1. 启动 MySQL 服务
net start MySQL  # Windows
# 或 sudo systemctl start mysql  # Linux/Mac

# 2. 创建数据库并导入
mysql -u root -p123456 -e "CREATE DATABASE IF NOT EXISTS audio DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"
mysql -u root -p123456 audio < backend/database/zy.sql
```

**详细说明：** 查看 `backend/database/安装指南.md`

### 第1步：启动后端
```bash
cd backend
pip install -r requirements.txt
python run.py
```
看到 `Running on http://127.0.0.1:5000` 表示成功 ✅

### 第2步：启动前端
1. 打开微信开发者工具
2. 导入项目 → **选择 `wxminpro` 文件夹**（重要！）
3. 点击编译

### 第3步：配置（首次需要）
1. **数据库配置**：检查 `backend/db_config.py` 中的数据库连接（默认已配置）
2. **测试连接**：运行 `python backend/db_config.py` 验证数据库连接

## 📖 详细文档

- **数据库安装**：`backend/database/安装指南.md` - MySQL安装与导入详细说明 ⭐
- **快速启动**：`QUICK_START.md` - 最简明的启动步骤
- **详细启动**：`STARTUP_GUIDE.md` - 完整的启动说明
- **迁移报告**：`MIGRATION_COMPLETE.md` - 迁移完成详情
- **项目结构**：`PROJECT_STRUCTURE_NEW.md` - 详细的项目结构

## ⚠️ 重要提示

1. **数据库安装**：首次使用必须先安装数据库（见第0步）
2. **前端导入**：必须选择 `wxminpro` 文件夹，不是根目录！
3. **后端路径**：所有路径已更新为相对路径
4. **数据库配置**：默认配置为 `root/123456`，如需修改请编辑 `backend/db_config.py`

## ✅ 迁移完成清单

- [x] 前端文件已迁移到 `wxminpro/`
- [x] 后端文件已迁移到 `backend/`
- [x] 测试文件已迁移到 `test/`
- [x] 路径引用已更新
- [x] 数据库安装脚本已创建（`backend/database/install.bat` 和 `install.ps1`）
- [ ] 数据库安装（需要手动执行，见第0步）
- [ ] 数据库配置验证（运行 `python backend/db_config.py`）

## 🎉 开始使用

按照上述步骤启动项目，如有问题请查看详细文档！

