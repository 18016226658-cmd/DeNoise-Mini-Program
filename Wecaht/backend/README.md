# 大整数分解系统 - Python 后端

## 项目简介

基于 Flask 的大整数分解系统后端，提供 RESTful API 接口，支持用户管理、大整数分解、历史记录存储和可视化分析功能。

## 功能特性

- 🔐 用户认证（登录、注册）
- 🔢 大整数分解（Pollard's Rho + Miller-Rabin）
- 📝 历史记录存储和查询
- 👥 用户管理（管理员功能）
- 📊 可视化分析（职业使用时间、用户偏好等）

## 环境要求

- Python 3.8+
- MySQL 5.7+ 或 MariaDB 10.3+
- pip

## 安装步骤

### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 2. 配置数据库

确保 MySQL 服务已启动，并创建数据库：

```sql
CREATE DATABASE xqq CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. 配置环境变量（可选）

可以设置环境变量来覆盖默认配置：

```bash
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_USER=root
export MYSQL_PASSWORD=123456
export MYSQL_DATABASE=xqq
```

### 4. 运行应用

```bash
python app.py
```

应用将在 `http://localhost:5000` 启动。

## API 文档

### 认证相关 (`/api/auth`)

- `POST /api/auth/login` - 用户登录
- `POST /api/auth/register` - 用户注册
- `GET /api/auth/user` - 获取当前用户信息
- `POST /api/auth/logout` - 用户登出

### 分解相关 (`/api/factorize`)

- `POST /api/factorize/factorize` - 分解大整数
- `POST /api/factorize/validate` - 验证输入数字

### 历史记录 (`/api/history`)

- `GET /api/history/list` - 获取历史记录列表
- `GET /api/history/<id>` - 获取历史记录详情
- `POST /api/history/clear` - 清空历史记录
- `GET /api/history/stats` - 获取历史记录统计

### 管理员 (`/api/admin`)

- `GET /api/admin/users` - 获取用户列表
- `GET /api/admin/users/<id>` - 获取用户详情
- `PUT /api/admin/users/<id>/level` - 修改用户等级

### 可视化分析 (`/api/analysis`)

- `GET /api/analysis/job-usage-time` - 不同职业的使用时间分布
- `GET /api/analysis/user-preferences` - 用户偏好分析
- `GET /api/analysis/usage-statistics` - 使用统计信息

## 请求示例

### 登录

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "xqq", "password": "123456"}'
```

### 分解数字

```bash
curl -X POST http://localhost:5000/api/factorize/factorize \
  -H "Content-Type: application/json" \
  -H "Authorization: xqq" \
  -d '{"number": "123456789"}'
```

### 获取历史记录

```bash
curl -X GET http://localhost:5000/api/history/list \
  -H "Authorization: xqq"
```

## 数据库结构

### users 表

- id: 主键
- username: 用户名（唯一）
- password: 密码
- level: 用户等级（normal, vip, svip, admin）
- level_name: 等级名称
- max_digits: 最大分解位数
- gender: 性别
- birth_year, birth_month, birth_day: 出生日期
- age: 年龄
- job: 职业
- create_time, last_login_time, update_time: 时间戳

### histories 表

- id: 主键
- user_id: 用户ID（外键）
- number: 原数
- factors: 因子列表（JSON字符串）
- formula: 分解式
- number_type: 数字类型
- factorization_level: 分解程度
- elapsed_time: 耗时（秒）
- digit_count: 数字位数
- create_time: 创建时间

## 默认管理员账户

- 用户名: `xqq`
- 密码: `123456`

## 注意事项

1. 生产环境请修改默认密码和密钥
2. 建议使用 JWT 进行身份认证
3. 密码应该使用哈希存储（如 bcrypt）
4. 建议使用 HTTPS
5. 定期备份数据库

## 开发说明

### 项目结构

```
backend/
├── app.py              # 主程序入口
├── config.py           # 配置文件
├── models.py           # 数据库模型
├── algorithms.py       # 分解算法
├── requirements.txt    # 依赖列表
├── api/                # API 路由
│   ├── auth.py        # 认证相关
│   ├── factorize.py   # 分解相关
│   ├── history.py     # 历史记录
│   ├── admin.py       # 管理员功能
│   └── analysis.py    # 可视化分析
└── README.md          # 说明文档
```

## 许可证

本项目为毕业设计项目，仅供学习和研究使用。

