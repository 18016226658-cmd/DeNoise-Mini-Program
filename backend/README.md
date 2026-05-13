# 后端服务说明

## 目录结构

```
backend/
├── app.py                 # Flask主应用文件
├── deNoise.py            # 降噪算法模块
├── requirements.txt      # Python依赖包
├── database/             # 数据库相关
│   ├── schema.sql       # 数据库表结构
│   └── init.sql         # 初始化数据
└── Audio/               # 音频文件存储
    ├── input/           # 输入音频
    ├── output/          # 输出音频
    └── download/        # 下载文件
```

## 快速启动

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置数据库

修改 `app.py` 中的数据库连接配置：

```python
connect = pymysql.connect(
    host='localhost',
    user='root',
    password='your_password',
    database='chatgpt',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
```

### 3. 启动服务

```bash
python app.py
```

服务将在 `http://127.0.0.1:5000` 启动

## API接口列表

### 用户相关
- `POST /api/Login` - 用户登录
- `POST /api/Register` - 用户注册
- `POST /api/EditUser` - 编辑用户
- `POST /api/DelUser` - 删除用户

### 音频降噪相关
- `POST /api/getAudioInfo` - 获取音频信息
- `POST /api/DeNoiseAudio` - 音频降噪处理
- `POST /api/DownloadDeNoise` - 下载降噪文件

### 音频分离相关
- `POST /api/separateAudio` - 音频分离
- `POST /api/downloadAudio` - 下载分离文件

### AI聊天相关
- `GET /api/GPT` - GPT聊天
- `POST /api/RecToText` - 语音转文字

### 数据可视化相关
- `POST /api/DtVisual` - 获取可视化数据

## 配置说明

### 音频文件路径

```python
TEMP_DIR = 'Audio/download'  # 音频文件存储目录
```

### CORS配置

```python
CORS(app, origins='*')  # 允许所有域访问（开发环境）
```

生产环境应限制为特定域名。

## 注意事项

1. 确保MySQL数据库已启动
2. 确保有足够的磁盘空间存储音频文件
3. 音频处理可能需要较长时间，建议设置合适的超时时间
4. 生产环境建议使用Gunicorn或uWSGI部署

