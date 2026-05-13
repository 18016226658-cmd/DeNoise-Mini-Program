# 数据库安装指南

## 问题：No database selected

如果遇到 `[3D000][1046] No database selected` 错误，说明没有先选择数据库。

## 解决方案

### 方法1：命令行执行（推荐）✅

```bash
# 1. 创建数据库
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS audio DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"

# 2. 导入表结构（会自动选择数据库）
mysql -u root -p audio < zy.sql
```

### 方法2：MySQL客户端（Navicat/MySQL Workbench等）

**步骤1：创建数据库**
```sql
CREATE DATABASE IF NOT EXISTS `audio` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

**步骤2：选择数据库**
```sql
USE `audio`;
```

**步骤3：执行脚本**
- 打开 `zy.sql` 文件
- 执行整个脚本

### 方法3：修改脚本（如果使用方法2）

如果使用MySQL客户端直接执行脚本，需要确保：
1. 先创建数据库
2. 在客户端中选择数据库
3. 然后执行脚本

或者修改 `zy.sql` 文件，将 `USE audio;` 改为你实际的数据库名。

## 验证安装

执行以下SQL验证：

```sql
USE audio;

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

## 常见问题

### Q1: 数据库已存在怎么办？
A: 如果数据库已存在，直接执行 `USE audio;` 然后运行脚本即可。脚本会先删除旧表再创建新表。

### Q2: 想使用其他数据库名？
A: 修改 `zy.sql` 文件中的 `USE audio;` 为你的数据库名，例如 `USE chatgpt;`

### Q3: 导入后没有数据？
A: 检查脚本末尾的 `INSERT INTO users` 语句是否执行成功。如果失败，可以手动执行：
```sql
INSERT INTO `users` (`Phone`, `UserName`, `Password`, `RegisterTime`, `Gender`, `Birthday`, `FaceImg`, `UserType`, `MaxSepTimes`, `CurSepTimes`, `MaxNoiseTimes`, `CurNoiseTimes`) 
VALUES 
('13685153598', 'SM', '123456', NOW(), '男', '1964-09-04', '/static/image/header.png', 1, 999999, 0, 999999, 0);
```

## 下一步

安装完成后，配置 `backend/db_config.py`：

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'your_password',  # 修改为实际密码
    'database': 'audio',  # 确保与创建的数据库名一致
    'charset': 'utf8mb4'
}
```

