# 大整数分解系统 - 微信小程序 + Python 后端（精简版）

## 一、系统整体架构

本系统采用 **前后端分离** 架构：

- **前端：微信小程序（目录 `Wecaht/`）**
  - 负责界面展示、输入校验、发起 HTTP 请求、展示后端计算结果。
  - 不在前端执行大整数分解算法，所有实算逻辑全部由 Python 后端完成。

- **后端：Python Flask 服务（目录 `Wecaht/backend/`）**
  - 提供 RESTful API：
    - 用户登录 / 注册
    - 大整数分解
    - 历史记录查询 / 清空 / 统计
    - 管理员用户管理
    - 可视化分析（职业使用时间、用户偏好等）
  - 使用 MySQL 数据库存储用户信息和分解历史：
    - 数据库名：`xqq`
    - 用户名：`root`
    - 密码：`123456`

该结构非常适合在论文的“系统实现”和“系统部署”章节中描述为：**轻量前端 + 计算与数据后端中心**。

---

## 二、核心目录结构（精简说明）

```text
Wecaht/
├── app.js / app.json / app.wxss        # 小程序入口与全局配置
├── pages/
│   ├── login/                          # 登录 / 注册（调用 /api/auth/*）
│   ├── home/                           # 首页
│   ├── splitter/                       # 分解页（调用 /api/factorize/factorize）
│   ├── history/                        # 历史记录页（调用 /api/history/*）
│   ├── my/                             # 个人中心
│   └── admin/                          # 管理员页（调用 /api/admin/*）
│
├── utils/
│   ├── common.js                       # 公共工具：BASE_URL、requestApi、Toast、存储等
│   └── algorithms.js                   # 仅保留输入校验 validateInput（算法已迁移到后端）
│
└── backend/                            # Python 后端
    ├── app.py                          # Flask 入口，注册各个蓝图
    ├── config.py                       # 配置（含 MySQL 连接）
    ├── models.py                       # 数据模型：User、History
    ├── algorithms.py                   # 大整数分解算法（Pollard's Rho、Miller-Rabin 等）
    ├── api/
    │   ├── auth.py                     # /api/auth/*   用户登录 / 注册 / 当前用户
    │   ├── factorize.py                # /api/factorize/* 大整数分解
    │   ├── history.py                  # /api/history/*   历史记录
    │   ├── admin.py                    # /api/admin/*     管理员功能
    │   └── analysis.py                 # /api/analysis/*  可视化分析
    ├── requirements.txt                # 后端依赖声明
    ├── README.md                       # 后端详细说明
    └── 使用说明.md                     # 后端中文说明
```

---

## 三、后端部署与运行（系统部署重点）

### 1. 环境准备

- 操作系统：Windows / Linux / macOS 均可
- Python 版本：3.8+
- MySQL 版本：5.7+ 或兼容版本

### 2. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 3. 创建数据库

在 MySQL 中执行：

```sql
CREATE DATABASE xqq CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 初始化数据表与管理员账号

```bash
cd backend
python init_db.py
```

执行成功后会自动创建：

- 数据表：`users`、`histories`
- 默认管理员账号：
  - 用户名：`xqq`
  - 密码：`123456`

### 5. 启动 Flask 后端

```bash
cd backend
python app.py
```

默认监听地址：

- `http://127.0.0.1:5000`
- 在同一局域网内，可使用类似 `http://你的电脑IP:5000` 被真机访问。

---

## 四、小程序前端运行（系统实现 - 前端部分）

### 1. 配置后端地址

在 `utils/common.js` 中设置：

```js
// 开发阶段（本机模拟器）
const BASE_URL = 'http://127.0.0.1:5000';

// 真机 / 局域网测试时，改成你电脑在局域网中的 IP，例如：
// const BASE_URL = 'http://10.60.32.34:5000';
```

### 2. 用微信开发者工具运行

1. 打开 **微信开发者工具**
2. 选择“导入项目”，目录指向 `Wecaht/`
3. AppID 使用“测试号”或你的真实 AppID
4. 点击“编译”，在模拟器或真机调试中运行

前端所有与用户 / 分解 / 历史 / 管理相关的数据，都是通过 `requestApi` 调用后端 API 获得。

---

## 五、关键接口概览（论文中可直接引用）

### 1. 认证模块 `/api/auth`

- **POST `/api/auth/login`**
  - 请求：
    ```json
    { "username": "xqq", "password": "123456" }
    ```
  - 响应：
    ```json
    {
      "success": true,
      "data": {
        "user": { "...用户信息..." },
        "token": "xqq"
      }
    }
    ```

- **POST `/api/auth/register`**
  - 请求包含：用户名、密码、性别、出生年月日、职业等基本信息。
  - 响应同样返回 `user + token`，小程序将其保存为当前登录用户。

### 2. 分解模块 `/api/factorize`

- **POST `/api/factorize/factorize`**
  - Header：`Authorization: <用户名>`（小程序通过 `requestApi` 自动添加）
  - 请求示例：
    ```json
    {
      "number": "12345678901234567890",
      "mode": "standard"
    }
    ```
  - 响应示例：
    ```json
    {
      "success": true,
      "data": {
        "number": "12345678901234567890",
        "factors": [
          { "value": "2", "is_prime": true },
          { "value": "3", "is_prime": true }
        ],
        "formula": "2 × 3 × ...",
        "elapsed_time": 0.123,
        "number_type": "composite",
        "number_type_name": "合数",
        "factorization_level": "complete",
        "factorization_level_name": "完全分解"
      }
    }
    ```

### 3. 历史记录模块 `/api/history`

- **GET `/api/history/list`**
  - 查询当前登录用户的分解历史，支持分页参数：`page`、`per_page`。

- **GET `/api/history/stats`**
  - 返回该用户的历史统计信息（总次数、成功次数等）。

- **POST `/api/history/clear`**
  - 清空当前用户的分解历史记录。

### 4. 管理员模块 `/api/admin`

- **GET `/api/admin/users`**
  - 支持按等级筛选用户，例如：`?level=all`。

- **GET `/api/admin/users/{id}`**
  - 查询某个用户的详细信息。

- **PUT `/api/admin/users/{id}/level`**
  - 修改用户等级，示例请求：
    ```json
    { "level": "vip" }
    ```

### 5. 可视化分析模块 `/api/analysis`

（可在论文“系统功能扩展 / 数据分析”部分中使用）

- **GET `/api/analysis/job-usage-time`**
  - 分析不同职业在一天 24 小时内使用系统的时间分布，返回统计数据和可视化图（Base64 图片）。

- **GET `/api/analysis/user-preferences`**
  - 分析不同年龄段 / 职业对数字位数、分解模式等的偏好。

- **GET `/api/analysis/usage-statistics`**
  - 综合使用情况统计（总调用次数、成功率、峰值时段等）。

---

## 六、前后端分工总结（可直接写入“系统实现”章节）

- **前端（微信小程序）**
  - 负责：
    - 用户交互与界面展示
    - 基本输入校验（数字格式、位数限制）
    - 通过 `requestApi` 统一封装 HTTP 请求
  - 特点：
    - 无算法实现，仅作为“可视化交互层”
    - 状态（当前用户、基本历史）缓存于本地，方便用户体验

- **后端（Python Flask + MySQL）**
  - 负责：
    - 大整数分解核心算法计算（Pollard's Rho、Miller-Rabin 等）
    - 用户与历史记录的持久化存储
    - 管理员权限控制及用户等级管理
    - 数据分析与可视化图表生成
  - 特点：
    - 计算和数据的统一中心
    - 接口清晰，易于扩展（例如增加新分析维度、接入更多前端）

用一句话概括：**小程序是“界面 + 控制台”，Python 后端是“计算引擎 + 数据中心”**，这正是本项目在工程实现与论文写作上的核心设计思想。


