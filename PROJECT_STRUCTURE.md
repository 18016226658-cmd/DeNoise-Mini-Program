# 音频降噪系统 - 项目结构说明

## 一、项目概述

本项目是一个基于微信小程序的音频降噪系统，采用前后端分离架构：
- **前端**：微信小程序（WxMinPro）
- **后端**：Python Flask + MySQL

## 二、核心功能

1. **用户注册与登录**：支持用户ID、用户名、出生日期、头像、性别等信息管理
2. **音频降噪处理**：基于巴特沃斯滤波器算法进行高质量降噪
3. **在线对比试听**：支持降噪前后音频文件的在线对比播放
4. **文件上传下载**：支持音频文件上传和降噪后文件下载
5. **使用历史记录**：显示用户音频降噪的使用历史
6. **数据可视化**：对音频降噪数据进行可视化分析
7. **用户管理**：用户信息维护、降噪次数统计等功能

## 三、项目结构

```
WxMinPro/
├── app.js                    # 小程序入口文件
├── app.json                  # 小程序全局配置
├── app.wxss                  # 小程序全局样式
├── config/                   # 配置文件目录
│   └── api.js               # API配置（统一管理接口地址）
├── utils/                    # 工具类目录
│   ├── request.js           # 统一请求工具
│   ├── storage.js           # 统一存储工具
│   ├── userInfo.js          # 用户信息工具
│   └── chartsOption.js      # 图表配置
├── pages/                    # 页面目录
│   ├── home/                # 首页（系统介绍）
│   ├── login/               # 登录页
│   ├── register/            # 注册页
│   ├── DeNoise/             # 音频降噪核心页面
│   ├── history/             # 历史记录页面
│   ├── DtLine/              # 数据可视化页面
│   ├── chat/                # 用户管理页面
│   ├── EditUser/            # 编辑用户页面
│   ├── DelUser/             # 删除用户页面
│   └── loginout/            # 注销页面
├── static/                   # 静态资源目录
│   ├── icon/                # 图标资源
│   └── image/               # 图片资源
├── ec-canvas/                # ECharts图表组件
└── echarts-wordcloud/        # 词云图组件
```

## 四、后端结构（Python Flask）

```
backend/
├── app.py                    # Flask主应用文件
├── deNoise.py               # 降噪算法实现（巴特沃斯滤波器）
├── requirements.txt         # Python依赖包
└── database/
    └── schema.sql           # 数据库表结构
```

## 五、核心页面说明

### 1. 首页（home）
- 系统功能介绍
- 应用场景说明
- 技术特点介绍
- 注销账号功能

### 2. 登录页（login）
- 手机号登录
- 密码验证
- 用户信息保存

### 3. 注册页（register）
- 用户信息注册
- 头像上传
- 信息验证

### 4. 音频降噪页（DeNoise）
- 音频文件选择
- 音频信息显示
- 原始音频播放
- 降噪处理
- 降噪后音频播放
- 文件下载
- 降噪前后对比试听

### 5. 历史记录页（history）
- 降噪历史列表
- 播放原始/降噪音频
- 下载降噪文件
- 下拉刷新

### 6. 数据可视化页（DtLine）
- 按日期统计
- 按星期统计
- 按小时统计
- 按性别统计
- 按年龄统计
- 词云图分析

### 7. 用户管理页（chat）
- 用户列表
- 用户信息查看
- 跳转编辑/删除

## 六、API接口说明

### 用户相关
- `POST /api/Login` - 用户登录
- `POST /api/Register` - 用户注册
- `POST /api/EditUser` - 编辑用户信息
- `POST /api/DelUser` - 删除用户

### 音频降噪相关
- `POST /api/getAudioInfo` - 获取音频信息
- `POST /api/DeNoiseAudio` - 音频降噪处理
- `POST /api/DownloadDeNoise` - 下载降噪文件
- `POST /api/getDeNoiseHistory` - 获取降噪历史记录

### 数据可视化相关
- `POST /api/DtVisual` - 获取可视化数据

## 七、技术栈

### 前端
- 微信小程序框架
- ECharts（数据可视化）
- 微信小程序API（文件上传、音频播放等）

### 后端
- Python 3.x
- Flask（Web框架）
- MySQL（数据库）
- scipy（巴特沃斯滤波器）
- pydub（音频处理）
- numpy（数值计算）

## 八、降噪算法

### 巴特沃斯滤波器
- **算法类型**：带通滤波器
- **阶数**：5阶（可配置）
- **特点**：
  - 通带内频率响应平坦
  - 滚降特性陡峭
  - 相位失真小
  - 适合去除工频干扰、高频嘶嘶声等噪声

### 处理流程
1. 读取音频文件
2. 提取音频数据
3. 设计巴特沃斯滤波器
4. 应用滤波器处理
5. 保存降噪后音频

## 九、数据库设计

### users表（用户表）
- UserID（用户ID）
- Phone（手机号，主键）
- UserName（用户名）
- Password（密码）
- Gender（性别）
- Birthday（出生日期）
- FaceImg（头像路径）
- UserType（用户类型：1-管理员，2-VIP，3-普通）
- RegisterTime（注册时间）

### denoise_history表（降噪历史表）
- ID（主键）
- UserID（用户ID）
- orgFileName（原始文件名）
- filename（处理后的文件名）
- fileSize（文件大小）
- duration（时长）
- n_channels（声道数）
- originalPath（原始文件路径）
- deNoisePath（降噪后文件路径）
- createTime（创建时间）

## 十、部署说明

### 前端部署
1. 使用微信开发者工具打开项目
2. 配置appid
3. 修改`config/api.js`中的后端地址
4. 上传代码并提交审核

### 后端部署
1. 安装Python依赖：`pip install -r requirements.txt`
2. 配置数据库连接
3. 运行Flask应用：`python app.py`
4. 配置Nginx反向代理（生产环境）

## 十一、注意事项

1. **API地址配置**：所有API地址统一在`config/api.js`中配置
2. **存储方式**：使用微信小程序存储API，不再使用文件系统
3. **错误处理**：统一使用`utils/request.js`进行请求，自动处理错误
4. **用户信息**：使用`utils/userInfo.js`统一管理用户信息
5. **音频格式**：支持WAV、MP3、OGG等格式
6. **文件大小**：建议单文件不超过50MB

## 十二、待删除的文件/文件夹

以下文件/文件夹可以删除（已不再使用）：
- `pages/AudioSep/` - 音频分离功能（不需要）
- `pages/separateAudio/` - 音频分离功能（不需要）
- `pages/chatGPT/` - ChatGPT聊天（不需要）
- `pages/GPT/` - GPT聊天（不需要）
- `pages/CreateDialo/` - 创建对话（不需要）
- `pages/EditCsb/` - 编辑模型参数（不需要）
- `pages/upload/` - 上传页面（功能已整合到DeNoise）
- `pages/telphone/` - 电话相关（不需要）
- `pages/My/` - 我的页面（功能已整合到home）
- `pages/LoginAudio/` - 音频登录（不需要）
- `pages/registerAudio/` - 音频注册（不需要）
- `pages/soundRecord/` - 录音功能（不需要）

## 十三、开发规范

1. **命名规范**：使用驼峰命名法
2. **代码注释**：关键功能添加注释
3. **错误处理**：统一使用try-catch和错误提示
4. **代码复用**：公共功能抽取到utils目录
5. **配置管理**：统一在config目录管理

## 十四、更新日志

### v1.0.0 (2024-12-28)
- 项目重构，聚焦音频降噪功能
- 删除音频分离、ChatGPT聊天等不相关功能
- 优化项目结构
- 统一API配置和请求工具
- 新增历史记录页面
- 优化降噪前后对比试听功能

