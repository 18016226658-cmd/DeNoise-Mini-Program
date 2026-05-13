# 项目结构说明（新版本）

## 项目目录结构

```
WxMinPro/
├── wxminpro/                    # 微信小程序前端
│   ├── app.js                   # 小程序入口文件
│   ├── app.json                 # 全局配置
│   ├── project.config.json      # 项目配置
│   ├── sitemap.json             # 站点地图
│   │
│   ├── pages/                   # 页面目录（20个页面）
│   │   ├── home/                # 首页（功能菜单）
│   │   ├── login/               # 登录页
│   │   ├── register/            # 注册页
│   │   ├── DeNoise/             # 音频降噪
│   │   ├── AudioSep/            # 音频分离
│   │   ├── separateAudio/       # 分离音频
│   │   ├── soundRecord/         # 录音功能
│   │   ├── chatGPT/             # ChatGPT聊天
│   │   ├── GPT/                 # GPT聊天
│   │   ├── CreateDialo/         # 创建对话
│   │   ├── EditCsb/             # 模型参数
│   │   ├── telphone/            # 电话功能
│   │   ├── LoginAudio/          # 音频登录
│   │   ├── registerAudio/       # 音频注册
│   │   ├── history/             # 历史记录
│   │   ├── DtLine/              # 数据可视化
│   │   ├── chat/                # 用户管理
│   │   ├── EditUser/            # 编辑用户
│   │   ├── DelUser/             # 删除用户
│   │   └── loginout/            # 注销
│   │
│   ├── config/                  # 配置文件
│   │   └── api.js               # API配置
│   │
│   ├── utils/                   # 工具类
│   │   ├── request.js           # 请求工具
│   │   ├── storage.js           # 存储工具
│   │   ├── userInfo.js          # 用户信息工具
│   │   └── chartsOption.js      # 图表配置
│   │
│   ├── static/                  # 静态资源
│   │   ├── icon/                # 图标
│   │   └── image/               # 图片
│   │
│   ├── ec-canvas/               # ECharts组件
│   └── echarts-wordcloud/       # 词云组件
│
├── backend/                     # Python Flask 后端
│   ├── app.py                   # Flask主应用
│   ├── deNoise.py               # 降噪算法
│   ├── deNoise-all.py           # 降噪算法（备用）
│   ├── config.py                # 配置文件（新增）
│   ├── requirements.txt         # Python依赖
│   ├── README.md                # 后端说明
│   │
│   ├── database/                # 数据库相关
│   │   ├── users.sql            # 用户表结构
│   │   ├── chatgpt.sql          # 数据库结构
│   │   └── audio2.sql           # 音频表结构
│   │
│   └── Audio/                   # 音频文件存储
│       ├── input/               # 输入音频
│       ├── output/              # 输出音频
│       ├── download/            # 下载文件
│       └── uploads/             # 上传文件
│
└── test/                        # 测试代码
    ├── test_api.py              # API测试
    ├── test_audio.py            # 音频处理测试
    ├── README.md                # 测试说明
    └── test_data/               # 测试数据
```

## 文件说明

### 前端文件（wxminpro/）

#### 核心文件
- `app.js` - 小程序入口，定义全局数据
- `app.json` - 全局配置，页面路径、tabBar等
- `project.config.json` - 微信开发者工具项目配置

#### 配置文件
- `config/api.js` - 统一管理API地址和接口端点

#### 工具类
- `utils/request.js` - 统一请求工具，包含错误处理
- `utils/storage.js` - 统一存储管理
- `utils/userInfo.js` - 用户信息管理
- `utils/chartsOption.js` - 图表配置

#### 页面
每个页面包含4个文件：
- `*.js` - 页面逻辑
- `*.wxml` - 页面结构
- `*.wxss` - 页面样式
- `*.json` - 页面配置

### 后端文件（backend/）

#### 核心文件
- `app.py` - Flask主应用，包含所有API接口
- `deNoise.py` - 降噪算法实现（巴特沃斯滤波器）
- `config.py` - 统一配置文件（新增）
- `requirements.txt` - Python依赖包列表

#### 数据库
- `database/users.sql` - 用户表结构
- `database/chatgpt.sql` - 数据库结构
- `database/audio2.sql` - 音频表结构

#### 音频存储
- `Audio/input/` - 用户上传的原始音频
- `Audio/output/` - 处理后的音频文件
- `Audio/download/` - 可供下载的文件
- `Audio/uploads/` - 上传临时文件

### 测试文件（test/）

- `test_api.py` - API接口测试脚本
- `test_audio.py` - 音频处理功能测试
- `test_data/` - 测试用的音频文件

## 启动流程

### 1. 后端启动
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### 2. 前端启动
- 使用微信开发者工具打开 `wxminpro` 文件夹
- 配置AppID
- 点击编译运行

### 3. 测试
```bash
cd test
python test_api.py
python test_audio.py
```

## 注意事项

1. **路径配置**：确保前后端的路径配置正确
2. **数据库**：确保MySQL数据库已启动并配置正确
3. **端口**：默认后端运行在5000端口，前端API配置需对应
4. **文件权限**：确保Audio目录有读写权限
5. **微信开发者工具路径**：需要在 `backend/app.py` 或 `backend/config.py` 中配置

## 配置说明

### 后端配置

1. **数据库配置**：修改 `backend/app.py` 中的数据库连接
2. **微信开发者工具路径**：修改 `backend/app.py` 中的 `WX_TEMP_DIR`
3. **音频文件路径**：已自动使用相对路径，无需修改

### 前端配置

1. **API地址**：在 `wxminpro/config/api.js` 中配置
2. **开发环境**：在微信开发者工具中勾选"不校验合法域名"

## 迁移说明

文件迁移已完成，详细说明请查看：
- `MIGRATION_COMPLETE.md` - 迁移完成报告
- `MIGRATION_GUIDE.md` - 迁移指南

详细启动说明请查看 [STARTUP_GUIDE.md](./STARTUP_GUIDE.md)
