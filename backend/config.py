# backend/config.py
# 后端配置文件

"""
配置文件
"""
import os

class Config:
    """应用配置"""
    # 数据库配置
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '123456')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'audio')
    
    # SQLAlchemy 配置
    SQLALCHEMY_DATABASE_URI = (
        f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}'
        f'@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # 设置为 True 可以看到 SQL 语句
    
    # 密钥（用于 session 等）
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # 文件上传配置
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 160 * 1024 * 1024  # 160MB
    
    # 可视化图片保存路径
    STATIC_FOLDER = 'static'
    ANALYSIS_IMAGES_FOLDER = os.path.join(STATIC_FOLDER, 'analysis')

# ============================================
# 音频文件存储路径配置
# ============================================
# 获取backend目录的绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 音频文件存储路径
AUDIO_BASE_DIR = os.path.join(BASE_DIR, 'Audio')

# 原始输入目录（兼容旧代码，不再作为上传目标）
AUDIO_INPUT_DIR = os.path.join(AUDIO_BASE_DIR, 'input')

# 业务目录
AUDIO_OUTPUT_DIR = os.path.join(AUDIO_BASE_DIR, 'output')
AUDIO_DOWNLOAD_DIR = os.path.join(AUDIO_BASE_DIR, 'download')
AUDIO_UPLOAD_DIR = os.path.join(AUDIO_BASE_DIR, 'uploads')

# 细分业务子目录
# 上传的原始音频（用户上传后首先落盘到这里）
AUDIO_UPLOAD_DENOISE_DIR = os.path.join(AUDIO_UPLOAD_DIR, 'DeNoise')
# 下载保存目录（用户点击“下载”后，服务端在此处保留一份）
AUDIO_DOWNLOAD_DENOISE_DIR = os.path.join(AUDIO_DOWNLOAD_DIR, 'DeNoise')
# 降噪临时文件目录（用于试听，未下载会被自动清理）
AUDIO_TRY_DIR = os.path.join(AUDIO_BASE_DIR, 'try')

# 录音相关目录
AUDIO_RECORD_BASE_DIR = os.path.join(AUDIO_BASE_DIR, 'record')
AUDIO_RECORD_TRY_DIR = os.path.join(AUDIO_RECORD_BASE_DIR, 'try')         # 录音试听文件
AUDIO_RECORD_DOWNLOAD_DIR = os.path.join(AUDIO_RECORD_BASE_DIR, 'download')  # 录音下载保存

# 分离音频下载目录（专门用于保存已下载的分离音频）
AUDIO_DOWNLOAD_SEPARATE_DIR = os.path.join(AUDIO_DOWNLOAD_DIR, 'Separate')

# 可视化图表静态图片目录
VISUALIZATION_BASE_DIR = os.path.join(BASE_DIR, 'static')
VISUALIZATION_IMAGE_DIR = os.path.join(VISUALIZATION_BASE_DIR, 'visualization')

# 创建必要的目录
os.makedirs(AUDIO_INPUT_DIR, exist_ok=True)              # 兼容老路径
os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)
os.makedirs(AUDIO_DOWNLOAD_DIR, exist_ok=True)
os.makedirs(AUDIO_UPLOAD_DIR, exist_ok=True)
os.makedirs(AUDIO_TRY_DIR, exist_ok=True)
os.makedirs(AUDIO_UPLOAD_DENOISE_DIR, exist_ok=True)
os.makedirs(AUDIO_DOWNLOAD_DENOISE_DIR, exist_ok=True)
os.makedirs(AUDIO_RECORD_BASE_DIR, exist_ok=True)
os.makedirs(AUDIO_RECORD_TRY_DIR, exist_ok=True)
os.makedirs(AUDIO_RECORD_DOWNLOAD_DIR, exist_ok=True)
os.makedirs(AUDIO_DOWNLOAD_SEPARATE_DIR, exist_ok=True)
os.makedirs(VISUALIZATION_BASE_DIR, exist_ok=True)
os.makedirs(VISUALIZATION_IMAGE_DIR, exist_ok=True)

# ============================================
# 兼容性配置（保持向后兼容）
# ============================================
# 为了保持与现有代码的兼容性，提供字典格式的配置
DB_CONFIG = {
    'host': Config.MYSQL_HOST,
    'port': Config.MYSQL_PORT,
    'user': Config.MYSQL_USER,
    'password': Config.MYSQL_PASSWORD,
    'database': Config.MYSQL_DATABASE,
    'charset': 'utf8mb4'
}

FLASK_CONFIG = {
    'MAX_CONTENT_LENGTH': Config.MAX_CONTENT_LENGTH,
    'DEBUG': True,  # 开发环境为True，生产环境为False
    'SECRET_KEY': Config.SECRET_KEY
}

# ============================================
# FFmpeg 配置（用于音频格式转换）
# ============================================
# 如果 FFmpeg 不在系统 PATH 中，可以在这里指定完整路径
# 例如：FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"
# 或者：FFMPEG_PATH = r"C:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"
# 如果为 None，则尝试从系统 PATH 中查找，或自动检测常见路径
FFMPEG_PATH = os.getenv('FFMPEG_PATH', None)  # 可以通过环境变量设置

# 自动检测 FFmpeg 路径（如果未在配置中指定）
if FFMPEG_PATH is None:
    # 尝试查找 C:\ffmpeg 下的所有子目录
    if os.path.exists(r"C:\ffmpeg"):
        try:
            # 先检查标准路径
            standard_path = r"C:\ffmpeg\bin\ffmpeg.exe"
            if os.path.exists(standard_path):
                FFMPEG_PATH = standard_path
                print(f"[信息] 自动检测到 FFmpeg 路径: {FFMPEG_PATH}")
            else:
                # 查找所有子目录中的 bin\ffmpeg.exe
                for item in os.listdir(r"C:\ffmpeg"):
                    potential_path = os.path.join(r"C:\ffmpeg", item, "bin", "ffmpeg.exe")
                    if os.path.exists(potential_path):
                        FFMPEG_PATH = potential_path
                        print(f"[信息] 自动检测到 FFmpeg 路径: {FFMPEG_PATH}")
                        break
        except Exception as e:
            print(f"[警告] 自动检测 FFmpeg 路径时出错: {e}")

# ============================================
# 微信开发者工具临时文件路径（已废弃）
# ============================================
# 注意：此配置已废弃，新代码已改为从 backend/Audio/input 读取文件
# 不再需要微信开发者工具的临时目录路径
# 如需保留历史记录，可取消下面的注释
# WX_TEMP_DIR = r'C:\Users\用户名\AppData\Local\微信开发者工具\User Data\...\wx小程序appid\'
