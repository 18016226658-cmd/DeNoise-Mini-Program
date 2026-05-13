# 需要删除的文件和文件夹清单

## 说明
以下文件和文件夹是项目重构后不再需要的，可以安全删除。

## 一、页面文件（pages目录下）

### 1. 音频分离相关（不需要）
- `pages/AudioSep/` - 整个文件夹
- `pages/separateAudio/` - 整个文件夹

### 2. ChatGPT聊天相关（不需要）
- `pages/chatGPT/` - 整个文件夹
- `pages/GPT/` - 整个文件夹
- `pages/CreateDialo/` - 整个文件夹
- `pages/EditCsb/` - 整个文件夹（编辑聊天模型参数）

### 3. 其他不需要的页面
- `pages/upload/` - 上传页面（功能已整合到DeNoise）
- `pages/telphone/` - 电话相关页面
- `pages/My/` - 我的页面（功能已整合到home）
- `pages/LoginAudio/` - 音频登录页面
- `pages/registerAudio/` - 音频注册页面
- `pages/soundRecord/` - 录音功能页面

## 二、Python后端文件（根目录）

### 1. 测试文件和备份文件
- `app - 副本.py`
- `app-2024-03-10.py`
- `app-2024-12-29).py`
- `app-2024-2-2-01.py`
- `createDialo - 副本.py`
- `movies-tf17-backup.py`

### 2. 音频分离相关
- `deNoise-1.py`（如果与deNoise.py重复）
- `deNoise-all.py`（如果与deNoise.py重复）

### 3. ChatGPT相关
- `test-gpt.py`
- `Talk_chatGPT.py`
- `mp3totxt-gpt.py`
- `mp3totxt.py`（如果只是用于GPT）

### 4. 其他测试文件
- `test.py`
- `test-wc.py`
- `testcreateTime.py`
- `test-打印等腰三角形.py`
- `t00.py`
- `T99.py`
- `tttt.py`
- `ttttt.py`
- `ttttttttt.py`
- `tttt-0002.py`
- `tttt3.py`
- `xxxx.py`
- `sen.py`
- `csb.py`（如果只是用于聊天模型）

### 5. 对话分析相关（如果不需要）
- `AnalDialo.py`
- `AnalDialo-back.py`
- `createDialo.py`
- `createDate.py`

### 6. 其他工具文件（根据实际需要决定）
- `Remote_Run.py`（远程运行，如果不需要）
- `movies-tf17.py`（电影推荐，如果不需要）
- `2-1-py-create-class-jar.py`
- `2-2-Py-call-Java-jar.py`

## 三、其他文件

### 1. Excel文件（如果不需要）
- `Dialo.xlsx`
- `Dialo-2024-1.xlsx`
- `Dialo-ok.xlsx`
- `Dialo.xlsx---`
- `Dialo2.xlsx`
- `~$Dialo.xlsx`（临时文件）

### 2. HTML文件（如果不需要）
- `Answer_词云图.html`
- `Question_词云图.html`
- `myEcharts_词云图.html`

### 3. 文本文件（如果不需要）
- `zhddline_1000.txt`
- `zhddline_10000.txt`
- `zhddline_2000.txt`
- `zhddline_2000 - 副本.txt`
- `zhddline_lines.txt`
- `WCDict.txt`
- `stoplist.txt`

### 4. 压缩文件
- `ec-canvas.rar`

### 5. 其他
- `chatgpt.sql`（如果不需要）
- `users.sql`（如果数据库已建立，可以删除）
- `pycall.c`
- `pycall.exe`
- `PyCallJava.jar`
- `PyCallJava.jar-bak`
- `java/`（如果不需要Java调用）

## 四、删除命令（Windows PowerShell）

```powershell
# 删除页面文件夹
Remove-Item -Recurse -Force pages\AudioSep
Remove-Item -Recurse -Force pages\separateAudio
Remove-Item -Recurse -Force pages\chatGPT
Remove-Item -Recurse -Force pages\GPT
Remove-Item -Recurse -Force pages\CreateDialo
Remove-Item -Recurse -Force pages\EditCsb
Remove-Item -Recurse -Force pages\upload
Remove-Item -Recurse -Force pages\telphone
Remove-Item -Recurse -Force pages\My
Remove-Item -Recurse -Force pages\LoginAudio
Remove-Item -Recurse -Force pages\registerAudio
Remove-Item -Recurse -Force pages\soundRecord

# 删除Python测试文件
Remove-Item app` -`副本.py
Remove-Item app-2024-03-10.py
Remove-Item app-2024-12-29).py
Remove-Item app-2024-2-2-01.py
Remove-Item test*.py
Remove-Item t*.py
Remove-Item xxxx.py
# ... 其他文件
```

## 五、注意事项

1. **备份**：删除前请先备份整个项目
2. **确认**：删除前确认这些文件确实不再需要
3. **数据库**：如果数据库已建立，SQL文件可以删除
4. **测试**：删除后需要测试所有功能是否正常

## 六、保留的核心文件

### 前端核心文件
- `app.js`, `app.json`, `app.wxss`
- `pages/home/` - 首页
- `pages/login/` - 登录
- `pages/register/` - 注册
- `pages/DeNoise/` - 降噪核心功能
- `pages/history/` - 历史记录
- `pages/DtLine/` - 数据可视化
- `pages/chat/` - 用户管理
- `pages/EditUser/` - 编辑用户
- `pages/DelUser/` - 删除用户
- `pages/loginout/` - 注销
- `config/` - 配置文件
- `utils/` - 工具类
- `static/` - 静态资源
- `ec-canvas/` - ECharts组件
- `echarts-wordcloud/` - 词云组件

### 后端核心文件
- `app.py` - Flask主应用
- `deNoise.py` - 降噪算法（或整合到app.py中）

