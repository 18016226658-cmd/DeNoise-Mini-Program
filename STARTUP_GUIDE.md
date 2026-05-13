# 项目启动指南

## 项目结构

```
WxMinPro/
├── wxminpro/              # 微信小程序前端
│   ├── app.js
│   ├── app.json
│   ├── app.wxss
│   ├── pages/
│   ├── config/
│   ├── utils/
│   └── static/
├── backend/               # Python Flask 后端
│   ├── app.py
│   ├── deNoise.py
│   ├── requirements.txt
│   ├── database/
│   └── Audio/
└── test/                  # 测试代码
    ├── test_api.py
    └── test_audio.py
```

## 一、前端启动（微信小程序）

### 1. 环境准备

1. **安装微信开发者工具**
   - 下载地址：https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html
   - 安装并登录微信开发者账号

2. **获取小程序AppID**
   - 登录微信公众平台：https://mp.weixin.qq.com/
   - 注册小程序账号
   - 获取AppID

### 2. 项目配置

1. **打开项目**
   - 打开微信开发者工具
   - 选择"导入项目"
   - 选择 `wxminpro` 文件夹
   - 输入AppID（或选择测试号）

2. **配置API地址**
   - 打开 `wxminpro/config/api.js`
   - 修改 `baseURL` 为后端服务器地址：
   ```javascript
   development: {
     baseURL: 'http://127.0.0.1:5000',  // 本地开发
     timeout: 30000
   },
   production: {
     baseURL: 'https://your-domain.com',  // 生产环境
     timeout: 30000
   }
   ```

3. **配置项目设置**
   - 在微信开发者工具中：
     - 设置 → 项目设置
     - 勾选"不校验合法域名"（开发环境）
     - 勾选"不校验TLS版本"

### 3. 启动项目

1. **编译运行**
   - 点击微信开发者工具的"编译"按钮
   - 等待编译完成
   - 在模拟器中查看效果

2. **真机调试**
   - 点击"预览"按钮
   - 使用微信扫码在手机上查看
   - 或点击"真机调试"进行调试

### 4. 主界面说明

小程序启动后会进入登录页面（`pages/login/login`），登录成功后跳转到首页（`pages/home/home`）。

首页包含：
- 功能菜单（12个功能入口）
- 系统介绍
- 应用场景说明

## 二、后端启动（Python Flask）

### 1. 环境准备

1. **安装Python**
   - Python 3.7 或更高版本
   - 下载地址：https://www.python.org/downloads/

2. **安装依赖包**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

   或手动安装：
   ```bash
   pip install flask flask-cors pymysql pandas scipy pydub numpy mutagen jieba snownlp matplotlib requests
   ```

### 2. 数据库配置

1. **安装MySQL**
   - 下载并安装MySQL数据库
   - 创建数据库（如：`chatgpt`）

2. **导入数据库**
   ```bash
   mysql -u root -p chatgpt < users.sql
   ```

3. **配置数据库连接**
   - 打开 `backend/app.py`
   - 修改数据库连接配置：
   ```python
   connect = pymysql.connect(
       host='localhost',      # 数据库地址
       user='root',           # 用户名
       password='your_password',  # 密码
       database='chatgpt',   # 数据库名
       charset='utf8mb4',
       cursorclass=pymysql.cursors.DictCursor
   )
   ```

### 3. 配置其他参数

1. **音频文件路径**
   - 在 `backend/app.py` 中修改：
   ```python
   TEMP_DIR = 'Audio/download'  # 音频文件存储目录
   WX_TEMP_DIR = r'你的微信开发者工具路径'  # 小程序临时文件路径
   ```

2. **API密钥配置**（如果需要）
   - OpenAI API密钥（在代码中配置）
   - 百度AIP密钥（语音识别）

### 4. 启动后端服务

#### Windows系统
```bash
cd backend
python app.py
```

#### Linux/Mac系统
```bash
cd backend
python3 app.py
```

#### 使用虚拟环境（推荐）
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py
```

### 5. 验证后端启动

启动成功后，应该看到类似输出：
```
 * Running on http://127.0.0.1:5000
 * Debug mode: off
```

访问 `http://127.0.0.1:5000/api/Login` 测试接口是否正常。

## 三、测试代码

### 1. 测试API接口

```bash
cd test
python test_api.py
```

### 2. 测试音频处理

```bash
cd test
python test_audio.py
```

## 四、常见问题

### 1. 前端问题

**问题：无法连接后端**
- 检查后端是否启动
- 检查API地址配置是否正确
- 检查网络连接
- 在微信开发者工具中勾选"不校验合法域名"

**问题：页面空白**
- 检查控制台错误信息
- 检查页面路径配置是否正确
- 检查文件是否完整

### 2. 后端问题

**问题：数据库连接失败**
- 检查MySQL是否启动
- 检查数据库连接配置
- 检查数据库用户权限

**问题：音频处理失败**
- 检查音频文件路径
- 检查文件权限
- 检查依赖包是否安装完整

**问题：端口被占用**
- 修改 `app.py` 中的端口：
  ```python
  app.run(port=5001)  # 使用其他端口
  ```

### 3. 跨域问题

如果遇到跨域问题，确保：
- `backend/app.py` 中已配置CORS：
  ```python
  from flask_cors import CORS
  CORS(app, origins='*')
  ```

## 五、开发流程

### 1. 开发环境启动顺序

1. **启动MySQL数据库**
   ```bash
   # Windows (以管理员身份运行)
   net start mysql
   
   # Linux/Mac
   sudo systemctl start mysql
   ```

2. **启动后端服务**
   ```bash
   cd backend
   python app.py
   ```

3. **启动前端**
   - 打开微信开发者工具
   - 导入 `wxminpro` 项目
   - 点击编译

### 2. 调试技巧

1. **前端调试**
   - 使用微信开发者工具的调试器
   - 查看Console输出
   - 使用Network查看请求

2. **后端调试**
   - 使用print语句输出日志
   - 使用Flask的debug模式：
     ```python
     app.run(debug=True)
     ```

## 六、生产环境部署

### 1. 后端部署

1. **使用Gunicorn**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **使用Nginx反向代理**
   - 配置Nginx转发请求到Flask应用

### 2. 前端部署

1. **上传代码**
   - 在微信开发者工具中点击"上传"
   - 填写版本号和项目备注

2. **提交审核**
   - 登录微信公众平台
   - 提交审核

3. **发布**
   - 审核通过后发布

## 七、项目文件说明

### 前端主要文件
- `app.js` - 小程序入口文件
- `app.json` - 全局配置
- `config/api.js` - API配置
- `utils/request.js` - 请求工具
- `pages/home/home` - 首页

### 后端主要文件
- `app.py` - Flask主应用
- `deNoise.py` - 降噪算法
- `requirements.txt` - Python依赖
- `database/` - 数据库相关文件

### 测试文件
- `test/test_api.py` - API测试
- `test/test_audio.py` - 音频处理测试

## 八、联系支持

如遇到问题，请检查：
1. 项目文档：`README.md`
2. 项目结构：`PROJECT_STRUCTURE.md`
3. 功能菜单：`FUNCTION_MENU.md`

