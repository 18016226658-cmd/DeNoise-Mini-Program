# 数据库建库脚本说明

## 文件说明

### zy.sql（推荐使用）⭐
**统一建库脚本**，整合了所有功能所需的表结构：
- ✅ `users` - 用户表（带配额管理）
- ✅ `denoisetable` - 音频降噪历史记录表
- ✅ `sepaudiotable` - 音频分离历史记录表
- ✅ `chattable` - 聊天记录表

**特点：**
- 统一字符集：utf8mb4
- 包含完整注释
- 添加了索引优化
- 包含默认管理员账户

### 其他文件（参考用）
- `users.sql` - 旧版用户表（无配额字段，不推荐单独使用）
- `audio2.sql` - 音频相关表（包含历史数据）
- `chatgpt.sql` - 聊天相关表（包含历史数据）

## 快速开始

### 方法1：使用 zy.sql（推荐）

```bash
# 1. 登录MySQL
mysql -u root -p

# 2. 创建数据库
CREATE DATABASE IF NOT EXISTS `audio` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `audio`;

# 3. 执行建库脚本
source backend/database/zy.sql;
```

或者直接执行：

```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS audio DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"
mysql -u root -p audio < backend/database/zy.sql
```

### 方法2：在MySQL客户端中执行

1. 打开MySQL客户端（Navicat、MySQL Workbench等）
2. 创建数据库：`audio`
3. 打开 `zy.sql` 文件
4. 执行脚本

## 验证安装

```sql
-- 查看所有表
SHOW TABLES;

-- 应该看到4个表：
-- users, denoisetable, sepaudiotable, chattable

-- 查看表结构
DESCRIBE users;
DESCRIBE denoisetable;
DESCRIBE sepaudiotable;
DESCRIBE chattable;

-- 查看默认管理员账户
SELECT * FROM users WHERE Phone = '13685153598';
```

## 表结构说明

### 1. users（用户表）
- **主键**：UserID（自增）
- **唯一索引**：Phone（手机号）
- **配额字段**：MaxSepTimes, CurSepTimes, MaxNoiseTimes, CurNoiseTimes

### 2. denoisetable（降噪历史表）
- **主键**：id（自增）
- **索引**：UserID, DeNoiseTime
- **关键字段**：AudioName, Extension, FileSize, Duration, N_channels, BOrder

### 3. sepaudiotable（分离历史表）
- **主键**：id（自增）
- **索引**：UserID, SepTime
- **关键字段**：MxName（模型名）, AudioName, Extension, FileSize, Duration

### 4. chattable（聊天记录表）
- **主键**：id（自增）
- **索引**：UserID, ChatTime
- **关键字段**：Question, Answer

## 导入历史数据（可选）

如果需要导入历史数据：

```bash
# 1. 先执行 zy.sql 创建表结构
mysql -u root -p audio < backend/database/zy.sql

# 2. 导入历史数据（只导入INSERT语句）
# 从 audio2.sql 中提取 INSERT 语句导入
# 从 chatgpt.sql 中提取 INSERT 语句导入
```

## 配置后端连接

在 `backend/app.py` 中配置数据库连接：

```python
# 数据库配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',  # 修改为实际密码
    'database': 'audio',  # 或 'chatgpt'
    'charset': 'utf8mb4'
}
```

## 默认账户

脚本会自动创建一个默认管理员账户：
- **手机号**：13685153598
- **密码**：123456
- **用户名**：SM
- **类型**：管理员（UserType=1）
- **配额**：999999次（分离和降噪）

**⚠️ 生产环境请立即修改默认密码！**

## 注意事项

1. **字符集**：统一使用 utf8mb4，支持emoji和特殊字符
2. **外键约束**：脚本中已注释，如需启用请取消注释
3. **索引优化**：已为常用查询字段添加索引
4. **数据备份**：生产环境请定期备份数据库

## 问题排查

### 问题1：字符集错误
```sql
-- 检查数据库字符集
SHOW CREATE DATABASE audio;

-- 如果不对，重新创建：
DROP DATABASE audio;
CREATE DATABASE audio DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

### 问题2：表已存在
```sql
-- 删除旧表（谨慎操作！）
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS denoisetable;
DROP TABLE IF EXISTS sepaudiotable;
DROP TABLE IF EXISTS chattable;

-- 然后重新执行 zy.sql
```

### 问题3：外键约束错误
如果启用外键后出现错误，检查：
- UserID字段类型是否一致（varchar(11)）
- 是否存在孤立数据

## 更新日志

- **2025-01-07**：创建统一建库脚本 zy.sql
  - 整合所有表结构
  - 统一字符集为utf8mb4
  - 添加索引优化
  - 包含默认管理员账户

