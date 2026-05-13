# backend/api/audio.py
# ============================================
# 音频处理相关接口路由模块
# ============================================
"""
音频处理模块
功能：处理音频降噪、音频分离、音频信息获取等
"""

from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import pymysql
from datetime import datetime
from pydub import AudioSegment
from pydub.utils import which
from mutagen import File as MutagenFile
from mutagen.id3 import ID3NoHeaderError
import subprocess
import shutil
import uuid

from config import (
    AUDIO_INPUT_DIR,
    AUDIO_OUTPUT_DIR,
    AUDIO_UPLOAD_DIR,
    AUDIO_DOWNLOAD_DIR,
    AUDIO_TRY_DIR,
    AUDIO_UPLOAD_DENOISE_DIR,
    AUDIO_DOWNLOAD_DENOISE_DIR,
    AUDIO_RECORD_TRY_DIR,
    AUDIO_RECORD_DOWNLOAD_DIR,
    AUDIO_DOWNLOAD_SEPARATE_DIR,
    FFMPEG_PATH,
)
from db_config import DB_CONFIG
from deNoise import DeNoise_all

# 创建蓝图
audio_bp = Blueprint('audio', __name__)

# 允许的音频文件扩展名
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'aac', 'flac', 'm4a'}

# 全局变量存储声道数
n_channels = 0

# ============================================
# 辅助函数：检查 FFmpeg 是否可用
# ============================================
def get_ffmpeg_path():
    """获取 FFmpeg 可执行文件路径"""
    # 1. 优先使用配置文件中的路径
    if FFMPEG_PATH and os.path.exists(FFMPEG_PATH):
        return FFMPEG_PATH
    
    # 2. 尝试从系统 PATH 中查找
    ffmpeg_path = which("ffmpeg")
    if ffmpeg_path:
        return ffmpeg_path
    
    # 3. 尝试常见的安装路径
    common_paths = [
        r"C:\ffmpeg\bin\ffmpeg.exe",  # 标准安装路径
        r"C:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe",  # 解压后的默认路径
        r"C:\ffmpeg\ffmpeg-7.0-essentials_build\bin\ffmpeg.exe",  # 其他版本
        r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
        r"D:\ffmpeg\bin\ffmpeg.exe",
        r"D:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe",
        r"D:\Program Files\ffmpeg\bin\ffmpeg.exe",
    ]
    # 也尝试查找 C:\ffmpeg 下的所有子目录
    if os.path.exists(r"C:\ffmpeg"):
        try:
            for item in os.listdir(r"C:\ffmpeg"):
                potential_bin = os.path.join(r"C:\ffmpeg", item, "bin", "ffmpeg.exe")
                if os.path.exists(potential_bin):
                    common_paths.insert(0, potential_bin)  # 优先使用找到的路径
        except:
            pass
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    return None

def check_ffmpeg_available():
    """检查 FFmpeg 是否已安装并可用"""
    return get_ffmpeg_path() is not None

def configure_pydub_ffmpeg():
    """配置 pydub 使用指定的 FFmpeg 路径"""
    ffmpeg_path = get_ffmpeg_path()
    if ffmpeg_path:
        # 设置 pydub 使用指定的 FFmpeg 路径
        # 如果是目录，需要指定 ffmpeg.exe
        if os.path.isdir(ffmpeg_path):
            AudioSegment.converter = os.path.join(ffmpeg_path, "ffmpeg.exe")
        elif ffmpeg_path.endswith("ffmpeg") or ffmpeg_path.endswith("ffmpeg.exe"):
            AudioSegment.converter = ffmpeg_path
        else:
            # 如果路径指向目录但没有 .exe，尝试添加
            if os.path.isdir(ffmpeg_path):
                AudioSegment.converter = os.path.join(ffmpeg_path, "ffmpeg.exe")
            else:
                AudioSegment.converter = ffmpeg_path
        print(f"[信息] 已配置 FFmpeg 路径: {AudioSegment.converter}")
        return True
    return False

def get_ffmpeg_error_message():
    """获取 FFmpeg 相关的错误提示信息"""
    if not check_ffmpeg_available():
        return (
            "系统未检测到 FFmpeg。\n"
            "FFmpeg 是处理非 WAV 格式音频文件（如 MP3、OGG 等）所必需的工具。\n\n"
            "【解决方案1：安装 FFmpeg 到系统 PATH】（推荐）\n"
            "1. 下载 FFmpeg：https://www.gyan.dev/ffmpeg/builds/\n"
            "   选择 ffmpeg-release-essentials.zip 下载\n"
            "2. 解压到某个目录（如 C:\\ffmpeg）\n"
            "3. 将 FFmpeg 的 bin 目录（如 C:\\ffmpeg\\bin）添加到系统 PATH 环境变量：\n"
            "   - 右键\"此电脑\" -> 属性 -> 高级系统设置 -> 环境变量\n"
            "   - 在\"系统变量\"中找到 Path，点击编辑\n"
            "   - 点击\"新建\"，添加 C:\\ffmpeg\\bin\n"
            "   - 确定保存，重启终端\n"
            "4. 验证：在命令行运行 'ffmpeg -version'\n\n"
            "【解决方案2：在配置文件中指定 FFmpeg 路径】\n"
            "在 backend/config.py 中设置 FFMPEG_PATH = r'C:\\ffmpeg\\bin\\ffmpeg.exe'\n\n"
            "【解决方案3：使用 WAV 格式】\n"
            "直接上传 WAV 格式的音频文件，无需 FFmpeg。"
        )
    return None

# 在模块加载时尝试配置 FFmpeg（延迟到 AudioSegment 导入后）
def _init_ffmpeg():
    """初始化 FFmpeg 配置"""
    try:
        if configure_pydub_ffmpeg():
            return True
    except Exception as e:
        print(f"[警告] 配置 FFmpeg 时出错: {e}")
    return False

# 延迟初始化，确保 AudioSegment 已导入
_init_ffmpeg()
# ============================================
# 0. 录音文件上传与播放/下载
# ============================================
@audio_bp.route('/SoundRecordFile', methods=['POST'])
def upload_sound_record_file():
    """
    上传录音文件
    - 前端通过 wx.uploadFile 提交，字段名为 file
    - 文件保存到 backend/Audio/record/try 目录（用于试听）
    - 返回可用于后续试听和下载的文件名
    """
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "error": "没有上传文件"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "error": "文件名为空"}), 400

        # 检查扩展名
        filename = secure_filename(file.filename)
        extension = os.path.splitext(filename)[1][1:].lower()
        if extension not in ALLOWED_EXTENSIONS:
            return jsonify({
                "success": False,
                "error": f"不支持的文件格式: {extension}"
            }), 400

        # 生成唯一文件名并保存到录音试听目录
        file_uuid = str(uuid.uuid4())
        unique_filename = f"{file_uuid}.{extension}"
        os.makedirs(AUDIO_RECORD_TRY_DIR, exist_ok=True)
        save_path = os.path.join(AUDIO_RECORD_TRY_DIR, unique_filename)
        file.save(save_path)

        # 返回录音文件信息和后续可用的播放/下载路径
        return jsonify({
            "success": True,
            "filename": unique_filename,
            "playUrl": f"/api/audio/playRecord/{unique_filename}",
            "downloadUrl": f"/api/DownloadRecord?filename={unique_filename}"
        }), 200
    except Exception as e:
        print(f"上传录音文件失败: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": f"上传录音失败: {str(e)}"}), 500



# ============================================
# 1. 上传音频文件接口
# ============================================
@audio_bp.route('/uploadAudio', methods=['POST'])
def upload_audio():
    """
    上传音频文件到服务器
    文件保存到 backend/Audio/uploads/DeNoise 目录
    """
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "error": "没有上传文件"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "error": "文件名为空"}), 400
        
        # 检查文件扩展名
        filename = secure_filename(file.filename)
        extension = os.path.splitext(filename)[1][1:].lower()
        
        if extension not in ALLOWED_EXTENSIONS:
            return jsonify({
                "success": False,
                "error": f"不支持的文件格式: {extension}。支持的格式: {', '.join(ALLOWED_EXTENSIONS)}"
            }), 400
        
        # 生成唯一文件名（使用UUID避免文件名冲突）
        file_uuid = str(uuid.uuid4())
        unique_filename = f"{file_uuid}.{extension}"
        # 上传统一保存到 Audio/uploads/DeNoise
        file_path = os.path.join(AUDIO_UPLOAD_DENOISE_DIR, unique_filename)
        
        # 保存文件
        file.save(file_path)
        
        # 获取文件大小
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
        
        # 获取音频信息
        try:
            # 对于非 WAV 格式，检查 FFmpeg 是否可用
            if extension != 'wav':
                ffmpeg_error = get_ffmpeg_error_message()
                if ffmpeg_error:
                    print(f"警告: FFmpeg 不可用，无法获取 {extension.upper()} 格式的音频信息")
                    # 仍然允许上传，但音频信息无法获取
                    duration_seconds = 0
                    duration_str = "00:00:00"
                    n_channels = 0
                else:
                    audio = AudioSegment.from_file(file_path)
                    duration_seconds = len(audio) / 1000.0  # 秒
                    duration_str = f"{int(duration_seconds // 3600):02d}:{int((duration_seconds % 3600) // 60):02d}:{int(duration_seconds % 60):02d}"
                    n_channels = audio.channels
            else:
                audio = AudioSegment.from_file(file_path)
                duration_seconds = len(audio) / 1000.0  # 秒
                duration_str = f"{int(duration_seconds // 3600):02d}:{int((duration_seconds % 3600) // 60):02d}:{int(duration_seconds % 60):02d}"
                n_channels = audio.channels
        except FileNotFoundError as e:
            print(f"获取音频信息失败（文件未找到或 FFmpeg 不可用）: {e}")
            duration_seconds = 0
            duration_str = "00:00:00"
            n_channels = 0
        except Exception as e:
            print(f"获取音频信息失败: {e}")
            import traceback
            traceback.print_exc()
            duration_seconds = 0
            duration_str = "00:00:00"
            n_channels = 0
        
        # 获取元数据
        title = ""
        artist = ""
        album = ""
        try:
            audio_file = MutagenFile(file_path)
            if audio_file:
                title = str(audio_file.get('title', [''])[0]) if audio_file.get('title') else ""
                artist = str(audio_file.get('artist', [''])[0]) if audio_file.get('artist') else ""
                album = str(audio_file.get('album', [''])[0]) if audio_file.get('album') else ""
        except Exception as e:
            print(f"读取音频元数据失败: {e}")
        
        return jsonify({
            "success": True,
            "filename": unique_filename,
            "orgFileName": filename,
            "extension": extension,
            "fileSize": round(file_size, 2),
            "duration": duration_str,
            "durationSeconds": round(duration_seconds, 2),
            "n_channels": n_channels,
            "title": title,
            "artist": artist,
            "album": album
        }), 200
        
    except Exception as e:
        print(f"上传音频文件失败: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": f"上传失败: {str(e)}"}), 500


# ============================================
# 2. 获取音频信息接口
# ============================================
@audio_bp.route('/getAudioInfo', methods=['POST'])
def get_audio_info():
    """
    获取音频文件信息
    优先从 backend/Audio/uploads/DeNoise 目录读取音频文件信息
    （兼容逻辑：如果找不到，再回退到 Audio/input）
    """
    try:
        # 获取请求参数
        if request.is_json:
            data = request.get_json()
            filename = data.get("filename") or data.get("orgFileName")
            extension = data.get("extension", "")
        else:
            filename = request.form.get("filename") or request.form.get("orgFileName")
            extension = request.form.get("extension", "")
        
        if not filename:
            return jsonify({"error": "缺少文件名参数"}), 400
        
        # 处理文件扩展名
        if not os.path.splitext(filename)[1]:
            if extension:
                filename = f"{filename}.{extension}"
        
        # 在 AUDIO_UPLOAD_DENOISE_DIR 中查找文件（新的默认上传目录）
        file_path = os.path.join(AUDIO_UPLOAD_DENOISE_DIR, filename)
        
        # 如果文件不存在，尝试不区分大小写查找（uploads/DeNoise）
        if not os.path.exists(file_path):
            search_dirs = [AUDIO_UPLOAD_DENOISE_DIR, AUDIO_INPUT_DIR]
            base_name = os.path.splitext(filename)[0].lower()
            for search_dir in search_dirs:
                if os.path.exists(search_dir):
                    all_files = os.listdir(search_dir)
                    for f in all_files:
                        if os.path.splitext(f)[0].lower() == base_name:
                            file_path = os.path.join(search_dir, f)
                            filename = f
                            break
                    if os.path.exists(file_path):
                        break
        
        if not os.path.exists(file_path):
            # 仅返回新目录下的部分文件名用于调试
            available_files = os.listdir(AUDIO_UPLOAD_DENOISE_DIR) if os.path.exists(AUDIO_UPLOAD_DENOISE_DIR) else []
            return jsonify({
                "error": f"音频文件未找到: {filename}",
                "searched_path": AUDIO_UPLOAD_DENOISE_DIR,
                "available_files": available_files[:10]
            }), 404
        
        # 获取文件大小
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
        
        # 使用 pydub 获取音频信息
        try:
            audio = AudioSegment.from_file(file_path)
            duration_seconds = len(audio) / 1000.0  # 秒
            duration_str = f"{int(duration_seconds // 3600):02d}:{int((duration_seconds % 3600) // 60):02d}:{int(duration_seconds % 60):02d}"
            n_channels = audio.channels
            frame_rate = audio.frame_rate
        except Exception as e:
            print(f"使用 pydub 读取音频信息失败: {e}")
            duration_seconds = 0
            duration_str = "00:00:00"
            n_channels = 0
            frame_rate = 0
        
        # 使用 mutagen 获取元数据
        title = ""
        artist = ""
        album = ""
        try:
            audio_file = MutagenFile(file_path)
            if audio_file:
                title = str(audio_file.get('title', [''])[0]) if audio_file.get('title') else ""
                artist = str(audio_file.get('artist', [''])[0]) if audio_file.get('artist') else ""
                album = str(audio_file.get('album', [''])[0]) if audio_file.get('album') else ""
        except Exception as e:
            print(f"读取音频元数据失败: {e}")
        
        # 返回音频信息
        return jsonify({
            "success": True,
            "filename": filename,
            "fileSize": round(file_size, 2),
            "duration": duration_str,
            "durationSeconds": round(duration_seconds, 2),
            "n_channels": n_channels,
            "frameRate": frame_rate,
            "title": title,
            "artist": artist,
            "album": album,
            "extension": os.path.splitext(filename)[1][1:] if os.path.splitext(filename)[1] else ""
        }), 200
        
    except Exception as e:
        print(f"获取音频信息失败: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"获取音频信息失败: {str(e)}"}), 500


# ============================================
# 2. 音频降噪接口
# ============================================
@audio_bp.route('/DeNoiseAudio', methods=['POST'])
def denoise_audio():
    """
    音频降噪处理
    从 backend/Audio/input 读取文件，处理后保存到 backend/Audio/uploads
    """
    global n_channels
    try:
        data = request.get_json()
        orgFileName = data.get("orgFileName")
        filename = data.get("filename")
        extension = data.get("extension")
        fileSize = data.get("fileSize", 0)
        duration = data.get("duration", "00:00:00")
        title = data.get("title", "")
        artist = data.get("artist", "")
        album = data.get("album", "")
        UserID = data.get("UserID", "")
        UserName = data.get("UserName", "")
        Gender = data.get("Gender", "")
        Birthday = data.get("Birthday", "")
        
        # 构建输入文件路径
        # 优先使用服务器返回的唯一文件名（filename），如果没有则使用原始文件名
        if filename and not filename.startswith('http://'):
            # filename 是服务器返回的唯一文件名（如：uuid.wav）
            input_file_name = filename
        elif orgFileName:
            # 使用原始文件名，需要从 input 目录查找
            input_file_name = orgFileName
        else:
            return jsonify({"success": False, "message": "缺少文件名信息"}), 400
        
        # 新逻辑：从上传目录 Audio/uploads/DeNoise 中读取源文件
        input_file = os.path.join(AUDIO_UPLOAD_DENOISE_DIR, input_file_name)
        
        # 兼容旧逻辑：如果上传目录中未找到，再回退到 Audio/input
        if not os.path.exists(input_file):
            legacy_input_file = os.path.join(AUDIO_INPUT_DIR, input_file_name)
            if os.path.exists(legacy_input_file):
                input_file = legacy_input_file
        
        if not os.path.exists(input_file):
            msg = (
                f"音频文件未找到。请确保文件 '{input_file_name}' "
                f"存在于 '{AUDIO_UPLOAD_DENOISE_DIR}' 或 '{AUDIO_INPUT_DIR}' 目录中。"
            )
            return jsonify({
                "success": False,
                "message": msg,
                "files": ""
            }), 200
        
        # 如果是非 wav 格式（如 mp3/ogg），先转换为临时 wav 再做降噪
        temp_converted_file = None
        input_for_denoise = input_file
        try:
            ext_lower = (extension or os.path.splitext(input_file_name)[1][1:]).lower()
        except Exception:
            ext_lower = ''
        
        if ext_lower and ext_lower != 'wav':
            # 使用统一的音频转换器进行格式转换
            try:
                # 尝试导入音频转换器模块
                try:
                    import sys
                    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                    from utils.audio_converter import get_audio_converter
                    
                    converter = get_audio_converter()
                    temp_converted_file = os.path.splitext(input_file)[0] + '_converted.wav'
                    
                    print(f"检测到非WAV格式({ext_lower})，开始转换为临时WAV用于降噪...")
                    success, message, output_path = converter.convert_to_wav(
                        input_file, 
                        temp_converted_file, 
                        format_hint=ext_lower
                    )
                    
                    if success and output_path and os.path.exists(output_path):
                        input_for_denoise = output_path
                        print(f"✓ {message}")
                    else:
                        # 转换失败，返回错误信息
                        return jsonify({
                            "success": False,
                            "message": message,
                            "files": ""
                        }), 200
                except ImportError:
                    # 如果转换器模块不存在，使用原有逻辑
                    print("音频转换器模块未找到，使用原有转换逻辑...")
                    conversion_success = False
                    
                    # 方案1：尝试使用 pydub + FFmpeg（如果可用）
                    if check_ffmpeg_available():
                        try:
                            print(f"检测到非WAV格式({ext_lower})，使用 FFmpeg 转换为临时WAV用于降噪...")
                            if not os.path.exists(input_file):
                                return jsonify({
                                    "success": False,
                                    "message": f"输入文件不存在: {input_file}",
                                    "files": ""
                                }), 200
                            
                            audio_src = AudioSegment.from_file(input_file)
                            temp_converted_file = os.path.splitext(input_file)[0] + '_converted.wav'
                            os.makedirs(os.path.dirname(temp_converted_file), exist_ok=True)
                            audio_src.export(temp_converted_file, format='wav')
                            input_for_denoise = temp_converted_file
                            conversion_success = True
                            print(f"已生成临时WAV文件: {temp_converted_file}")
                        except Exception as e:
                            print(f"使用 FFmpeg 转换失败: {e}")
                            import traceback
                            traceback.print_exc()
                    
                    # 方案2：尝试使用 soundfile（如果已安装）
                    if not conversion_success:
                        try:
                            import soundfile as sf
                            print(f"尝试使用 soundfile 转换 {ext_lower} 格式（无需 FFmpeg）...")
                            if ext_lower in ['flac', 'ogg']:
                                data, samplerate = sf.read(input_file)
                                temp_converted_file = os.path.splitext(input_file)[0] + '_converted.wav'
                                os.makedirs(os.path.dirname(temp_converted_file), exist_ok=True)
                                sf.write(temp_converted_file, data, samplerate, format='WAV')
                                input_for_denoise = temp_converted_file
                                conversion_success = True
                                print(f"✓ 已使用 soundfile 成功转换 {ext_lower} 格式为 WAV: {temp_converted_file}")
                            else:
                                print(f"soundfile 不支持 {ext_lower} 格式，需要 FFmpeg")
                        except ImportError:
                            print("soundfile 未安装。可以运行 'pip install soundfile' 来支持 OGG/FLAC 格式（无需 FFmpeg）")
                        except Exception as e:
                            print(f"使用 soundfile 转换失败: {e}")
                            import traceback
                            traceback.print_exc()
                    
                    # 如果所有转换方案都失败
                    if not conversion_success:
                        ffmpeg_error = get_ffmpeg_error_message()
                        error_msg = (
                            f"无法处理 {ext_lower.upper()} 格式的音频文件。\n\n"
                            f"{ffmpeg_error if ffmpeg_error else ''}\n\n"
                            f"【快速解决方案】\n"
                            f"1. 安装 FFmpeg（推荐）：按照 backend/FFMPEG_INSTALL_GUIDE.md 中的说明安装\n"
                            f"2. 或安装 Python 库：pip install soundfile（仅支持部分格式）\n"
                            f"3. 或转换为 WAV 格式后再上传（最简单）"
                        )
                        return jsonify({
                            "success": False,
                            "message": error_msg,
                            "files": ""
                        }), 200
            except Exception as e:
                print(f"音频格式转换过程出错: {e}")
                import traceback
                traceback.print_exc()
                return jsonify({
                    "success": False,
                    "message": f"音频格式转换失败: {str(e)}",
                    "files": ""
                }), 200
        
        # 创建输出目录（使用try目录作为临时存储）
        output_dir_denoise = AUDIO_TRY_DIR
        os.makedirs(output_dir_denoise, exist_ok=True)
        
        # 构建输出文件名
        # 注意：DeNoise_all函数会基于输入文件路径生成输出文件名
        # 它会去掉扩展名，然后根据声道数添加 -stereo.wav 或 -mono.wav
        new_filename_base = os.path.splitext(input_file_name)[0]
        
        # 获取音频信息以确定声道数（基于用于降噪的输入文件）
        try:
            audio = AudioSegment.from_file(input_for_denoise)
            n_channels = audio.channels
        except Exception as e:
            print(f"获取音频声道数失败: {e}")
            n_channels = 2  # 默认立体声
        
        # DeNoise_all函数会基于输入文件路径生成输出文件
        # 它会在输入文件路径基础上，去掉扩展名，然后添加 -stereo.wav 或 -mono.wav
        # 所以我们需要传入一个基础路径，让函数生成正确的文件名
        # 使用输出目录 + 基础文件名（不含扩展名）作为输出路径
        output_file_base = os.path.join(output_dir_denoise, new_filename_base)
        
        # 调用降噪函数
        try:
            res = DeNoise_all(input_for_denoise, output_file_base)
        finally:
            # 删除临时转换文件
            if temp_converted_file and os.path.exists(temp_converted_file):
                try:
                    os.remove(temp_converted_file)
                    print(f"已删除临时转换文件: {temp_converted_file}")
                except Exception as e:
                    print(f"删除临时转换文件失败: {e}")
        
        if res == 200:
            # DeNoise_all函数会根据声道数生成文件名
            # 立体声：{base}-stereo.wav
            # 单声道：{base}-mono.wav
            if n_channels == 2:
                output_filename = f"{new_filename_base}-stereo.wav"
                output_path = os.path.join(output_dir_denoise, output_filename)
            else:
                output_filename = f"{new_filename_base}-mono.wav"
                output_path = os.path.join(output_dir_denoise, output_filename)
            
            # 验证文件是否真的存在
            if not os.path.exists(output_path):
                print(f"警告：降噪函数返回成功，但文件不存在: {output_path}")
                # 尝试查找实际生成的文件
                if os.path.exists(output_dir_denoise):
                    all_files = os.listdir(output_dir_denoise)
                    matching_files = [f for f in all_files if new_filename_base in f]
                    if matching_files:
                        print(f"找到匹配的文件: {matching_files}")
                        output_filename = matching_files[0]
                        output_path = os.path.join(output_dir_denoise, output_filename)
                    else:
                        return jsonify({
                            "success": False,
                            "message": f"降噪处理完成，但输出文件未找到。预期路径: {output_path}",
                            "files": ""
                        }), 200
                else:
                    return jsonify({
                        "success": False,
                        "message": f"输出目录不存在: {output_dir_denoise}",
                        "files": ""
                    }), 200
            
            print(f"降噪成功，文件已保存: {output_path}")
            print(f"文件大小: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB")
            
            # 保存降噪数据到数据库
            # 优先使用 UserID；如果为空则使用 Phone 作为唯一标识，确保历史记录按手机号可查询
            try:
                user_identifier = UserID or data.get("Phone") or ""
                save_denoise_data(
                    UserID=user_identifier,
                    UserName=UserName,
                    Gender=Gender,
                    Birthday=Birthday,
                    AudioName=orgFileName or filename,
                    Extension=extension or os.path.splitext(input_file_name)[1][1:],
                    FileSize=fileSize,
                    Duration=duration,
                    N_channels=n_channels
                )
            except Exception as e:
                print(f"保存降噪数据到数据库失败: {e}")
            
            return jsonify({
                "success": True,
                "files": output_filename,
                "message": "降噪成功"
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "降噪处理失败",
                "files": ""
            }), 200
            
    except Exception as e:
        print(f"降噪处理异常: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": f"降噪处理失败: {str(e)}",
            "files": ""
        }), 500


# ============================================
# 3. 保存降噪数据到数据库
# ============================================
def save_denoise_data(UserID, UserName, Gender, Birthday, AudioName, Extension, FileSize, Duration, N_channels, BOrder=5):
    """保存降噪数据到 denoisetable 表"""
    try:
        connect = pymysql.Connect(**DB_CONFIG)
        cursor = connect.cursor()
        
        # 转换时长格式（从 "HH:MM:SS" 转为秒数）
        duration_seconds = 0
        if Duration and ":" in str(Duration):
            parts = str(Duration).split(":")
            if len(parts) == 3:
                duration_seconds = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        
        sql = """
            INSERT INTO denoisetable 
            (UserID, UserName, DeNoiseTime, Gender, Birthday, AudioName, Extension, FileSize, Duration, N_channels, BOrder)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            UserID, UserName, datetime.now(), Gender, Birthday if Birthday else None,
            AudioName, Extension, FileSize, duration_seconds, N_channels, BOrder
        ))
        connect.commit()
        connect.close()
        print("降噪数据已保存到数据库")
    except Exception as e:
        print(f"保存降噪数据失败: {e}")
        raise


# ============================================
# 7. 获取降噪历史记录接口
# ============================================
@audio_bp.route('/getDeNoiseHistory', methods=['POST'])
def get_denoise_history():
    """
    获取降噪历史记录
    根据用户ID或手机号查询降噪历史
    """
    try:
        data = request.get_json() if request.is_json else request.form.to_dict()
        UserID = data.get("UserID") or data.get("Phone")
        UserType = data.get("UserType") or data.get("userType")  # 1=管理员
        
        # 非管理员必须提供 UserID；管理员可以查看全部
        if not UserID and str(UserType) != "1":
            return jsonify({
                "success": False,
                "message": "缺少用户ID参数",
                "data": []
            }), 400
        
        # 连接数据库
        connect = pymysql.Connect(**DB_CONFIG)
        cursor = connect.cursor()
        
        # 查询降噪历史记录
        if str(UserType) == "1":
            # 管理员：查看所有用户最近 200 条记录
            sql = """
                SELECT 
                    ID, UserID, UserName, DeNoiseTime, Gender, Birthday,
                    AudioName, Extension, FileSize, Duration, N_channels, BOrder
                FROM denoisetable 
                WHERE AudioName IS NOT NULL
                ORDER BY DeNoiseTime DESC
                LIMIT 200
            """
            cursor.execute(sql)
        else:
            # 普通用户：只看自己的记录
            sql = """
                SELECT 
                    ID, UserID, UserName, DeNoiseTime, Gender, Birthday,
                    AudioName, Extension, FileSize, Duration, N_channels, BOrder
                FROM denoisetable 
                WHERE UserID = %s AND AudioName IS NOT NULL
                ORDER BY DeNoiseTime DESC
                LIMIT 100
            """
            cursor.execute(sql, (UserID,))
        results = cursor.fetchall()
        connect.close()
        
        # 构建历史记录列表
        history_list = []
        for row in results:
            # 格式化时间
            denoise_time = row[3] if len(row) > 3 and row[3] else None
            formatted_time = ""
            if denoise_time:
                try:
                    # 如果是 datetime 对象，格式化为字符串
                    if hasattr(denoise_time, 'strftime'):
                        formatted_time = denoise_time.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        # 如果是字符串，尝试解析并格式化
                        from datetime import datetime as dt
                        if isinstance(denoise_time, str):
                            # 尝试多种时间格式
                            for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"]:
                                try:
                                    parsed_time = dt.strptime(denoise_time.split('.')[0], fmt)
                                    formatted_time = parsed_time.strftime("%Y-%m-%d %H:%M:%S")
                                    break
                                except:
                                    continue
                            if not formatted_time:
                                formatted_time = str(denoise_time)
                        else:
                            formatted_time = str(denoise_time)
                except Exception as e:
                    print(f"格式化时间失败: {e}")
                    formatted_time = str(denoise_time) if denoise_time else ""
            
            # 根据数据库表结构提取字段
            history_item = {
                "id": row[0] if len(row) > 0 else None,
                "UserID": row[1] if len(row) > 1 else UserID,
                "UserName": row[2] if len(row) > 2 else "",
                "DeNoiseTime": formatted_time,  # 格式化后的时间
                "createTime": formatted_time,  # 兼容前端字段名
                "Gender": row[4] if len(row) > 4 else "",
                "Birthday": str(row[5]) if len(row) > 5 and row[5] else "",
                "AudioName": row[6] if len(row) > 6 else "",
                "Extension": row[7] if len(row) > 7 else "",
                "FileSize": float(row[8]) if len(row) > 8 and row[8] else 0,
                "Duration": row[9] if len(row) > 9 else 0,
                "N_channels": row[10] if len(row) > 10 else 0,
                "BOrder": row[11] if len(row) > 11 else 5
            }
            
            # 构建文件名（用于播放和下载）
            if history_item["AudioName"]:
                # 尝试构建降噪后的文件名
                base_name = history_item["AudioName"]
                if history_item["N_channels"] == 2:
                    filename = f"{base_name}-stereo.wav"
                else:
                    filename = f"{base_name}-mono.wav"
                
                history_item["filename"] = filename
                history_item["deNoisePath"] = f"/api/audio/play/{filename}"
                history_item["originalPath"] = f"/api/audio/play/{base_name}.{history_item['Extension']}"
            
            history_list.append(history_item)
        
        return jsonify({
            "success": True,
            "data": history_list
        }), 200
        
    except Exception as e:
        print(f"获取降噪历史记录失败: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": f"获取历史记录失败: {str(e)}",
            "data": []
        }), 500


# ============================================
# 4. 音频分离接口
# ============================================
def run_demucs(input_file, output_dir, model="htdemucs", device="cpu"):
    """
    运行 demucs 进行音频分离
    """
    command = [
        "demucs",
        "-n", model,
        "--out", output_dir,
        "--device", device,
        input_file
    ]
    
    try:
        result = subprocess.run(command, check=True)
        print("Demucs 运行成功!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"运行 Demucs 失败: {e}")
        raise
    except FileNotFoundError:
        print("错误: 未找到 demucs 命令，请确保已安装 demucs")
        raise


@audio_bp.route('/separateAudio', methods=['POST'])
def separate_audio():
    """
    音频分离处理
    从 backend/Audio/input 读取文件，处理后保存到 backend/Audio/uploads
    """
    try:
        data = request.get_json()
        filePath = data.get("filePath", "")
        filename = data.get("filename", "")
        extension = data.get("extension", "")
        # 兼容前端字段名 org_FileName / orgFileName
        orgFileName = data.get("orgFileName") or data.get("org_FileName") or ""
        fileSize = data.get("fileSize", 0)
        duration = data.get("duration", "00:00:00")
        title = data.get("title", "")
        artist = data.get("artist", "")
        album = data.get("album", "")
        
        # 确定输入文件路径
        # 优先使用服务器返回的唯一文件名（filename），如果没有则使用原始文件名
        if filename and not str(filename).startswith('http'):
            # filename 是服务器返回的唯一文件名（通常已经包含扩展名，如 uuid.wav）
            input_file_name = filename
        elif orgFileName:
            # 使用原始文件名
            input_file_name = orgFileName
        elif filename and extension:
            # 兜底：如果 filename 不带扩展名，则手动补上
            base, ext = os.path.splitext(filename)
            if not ext and extension:
                input_file_name = f"{filename}.{extension}"
            else:
                input_file_name = filename
        else:
            return jsonify({"error": "缺少文件名参数"}), 400
        
        # 新逻辑：优先从 Audio/uploads/DeNoise 读取文件
        input_file = os.path.join(AUDIO_UPLOAD_DENOISE_DIR, input_file_name)
        if not os.path.exists(input_file):
            # 兼容旧逻辑：回退到 Audio/input
            legacy_input_file = os.path.join(AUDIO_INPUT_DIR, input_file_name)
            if os.path.exists(legacy_input_file):
                input_file = legacy_input_file
        
        if not os.path.exists(input_file):
            return jsonify({"error": "文件未找到"}), 404
        
        # 创建输出目录
        output_dir = os.path.join(AUDIO_UPLOAD_DIR, 'separated')
        os.makedirs(output_dir, exist_ok=True)
        
        # 运行 demucs 分离
        try:
            run_demucs(input_file, output_dir)
        except Exception as e:
            return jsonify({"error": f"音频分离失败: {str(e)}"}), 500
        
        # 构建分离后的文件路径
        base_name = os.path.splitext(input_file_name)[0]
        model_dir = os.path.join(output_dir, "htdemucs", base_name)
        
        vocals_path = os.path.join(model_dir, "vocals.wav")
        other_path = os.path.join(model_dir, "other.wav")
        drums_path = os.path.join(model_dir, "drums.wav")
        bass_path = os.path.join(model_dir, "bass.wav")
        
        # 检查文件是否存在
        if not os.path.exists(vocals_path):
            return jsonify({"error": "分离后的文件未找到"}), 404
        
        # 返回分离结果（同时提供下载 URL，指向新的下载接口目录）
        return jsonify({
            "success": True,
            "files": output_dir,
            "vocalsPath": f"/api/download/separated/htdemucs/{base_name}/vocals.wav",
            "otherPath": f"/api/download/separated/htdemucs/{base_name}/other.wav",
            "drumsPath": f"/api/download/separated/htdemucs/{base_name}/drums.wav",
            "bassPath": f"/api/download/separated/htdemucs/{base_name}/bass.wav"
        }), 200
        
    except Exception as e:
        print(f"音频分离异常: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"音频分离失败: {str(e)}"}), 500


# ============================================
# 5. 文件下载接口
# ============================================
@audio_bp.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    """
    下载文件
    支持下载降噪后的文件和分离后的文件
    """
    try:
        # 尝试从 uploads/DeNoise 目录下载
        denoise_path = os.path.join(AUDIO_UPLOAD_DIR, 'DeNoise', filename)
        if os.path.exists(denoise_path):
            return send_file(denoise_path, as_attachment=True)
        
        # 尝试从 uploads/separated 目录下载
        separated_path = os.path.join(AUDIO_UPLOAD_DIR, 'separated', filename)
        if os.path.exists(separated_path):
            return send_file(separated_path, as_attachment=True)
        
        # 尝试从 input 目录下载
        input_path = os.path.join(AUDIO_INPUT_DIR, filename)
        if os.path.exists(input_path):
            return send_file(input_path, as_attachment=True)
        
        return jsonify({"error": "文件未找到"}), 404
        
    except Exception as e:
        print(f"下载文件失败: {e}")
        return jsonify({"error": f"下载文件失败: {str(e)}"}), 500


@audio_bp.route('/download/separated/<path:filepath>', methods=['GET'])
def download_separated(filepath):
    """
    下载分离后的音频文件
    - 源文件位于 Audio/uploads/separated
    - 下载时复制到 Audio/download/Separate 中保存一份
    """
    try:
        # 源文件完整路径（保持子目录结构）
        source_path = os.path.join(AUDIO_UPLOAD_DIR, 'separated', filepath)
        if not os.path.exists(source_path):
            return jsonify({"error": "文件未找到"}), 404

        # 在下载目录中保持相同的子目录结构
        download_path = os.path.join(AUDIO_DOWNLOAD_SEPARATE_DIR, filepath)
        download_dir = os.path.dirname(download_path)
        os.makedirs(download_dir, exist_ok=True)

        # 复制文件到下载目录（如果不存在或源文件较新）
        try:
            if (not os.path.exists(download_path) or
                os.path.getmtime(source_path) > os.path.getmtime(download_path)):
                shutil.copy2(source_path, download_path)
                print(f"已将分离文件复制到下载目录: {download_path}")
        except Exception as e:
            print(f"复制分离文件到下载目录失败: {e}")
            # 复制失败时直接从源路径返回
            download_path = source_path

        filename = os.path.basename(filepath)
        return send_file(download_path, as_attachment=True, download_name=filename)
    except Exception as e:
        print(f"下载分离文件失败: {e}")
        return jsonify({"error": f"下载文件失败: {str(e)}"}), 500


# ============================================
# 6. 下载降噪后的音频文件（统一接口）
# ============================================
@audio_bp.route('/DownloadDeNoise', methods=['GET', 'POST'])
def download_denoise_file():
    """
    下载降噪后的音频文件
    支持 GET 和 POST 两种方式
    """
    try:
        # 获取文件名参数（必选）和自定义下载名（可选）
        if request.method == 'GET':
            filename = request.args.get('filename')
            custom_name = request.args.get('customName')
        else:
            if request.is_json:
                json_data = request.get_json()
                filename = json_data.get('filename')
                custom_name = json_data.get('customName')
            else:
                filename = request.form.get('filename')
                custom_name = request.form.get('customName')
        
        if not filename:
            return jsonify({"error": "缺少文件名参数"}), 400
        
        source_path = None
        should_delete_try = False
        
        # 尝试从多个目录查找源文件
        # 1. 优先从 try 目录查找（临时文件，下载后需要删除）
        try_path = os.path.join(AUDIO_TRY_DIR, filename)
        if os.path.exists(try_path):
            source_path = try_path
            should_delete_try = True  # 标记为需要删除
        
        # 2. 从 uploads/DeNoise 目录查找（新的上传目录）
        if not source_path:
            upload_denoise_path = os.path.join(AUDIO_UPLOAD_DENOISE_DIR, filename)
            if os.path.exists(upload_denoise_path):
                source_path = upload_denoise_path
        
        # 3. 从 output/DeNoise 目录查找（兼容旧输出）
        if not source_path:
            output_path = os.path.join(AUDIO_OUTPUT_DIR, 'DeNoise', filename)
            if os.path.exists(output_path):
                source_path = output_path
        
        # 4. 从 uploads/separated 目录查找（兼容分离后的文件）
        if not source_path:
            separated_path = os.path.join(AUDIO_UPLOAD_DIR, 'separated', filename)
            if os.path.exists(separated_path):
                source_path = separated_path
        
        if not source_path:
            return jsonify({"error": "文件未找到"}), 404
        
        # 确保下载保存目录 Audio/download/DeNoise 存在
        os.makedirs(AUDIO_DOWNLOAD_DENOISE_DIR, exist_ok=True)
        # 如果前端传了自定义文件名，则在下载目录中使用该文件名保存
        final_name = custom_name if custom_name else filename
        download_save_path = os.path.join(AUDIO_DOWNLOAD_DENOISE_DIR, final_name)
        
        # 将文件复制到下载目录（如果还不在该目录，或者文件名不同）
        if os.path.abspath(source_path) != os.path.abspath(download_save_path):
            try:
                shutil.copy2(source_path, download_save_path)
                print(f"已将文件复制到下载目录: {download_save_path}")
            except Exception as e:
                print(f"复制文件到下载目录失败: {e}")
                # 如果复制失败，仍然从源路径直接发送文件
                download_save_path = source_path
        
        # 发送文件（从下载目录或源路径），下载名使用 final_name，确保与前端自定义一致
        response = send_file(download_save_path, as_attachment=True, download_name=final_name)
        
        # 如果源文件在 try 目录中，下载成功后删除临时文件
        if should_delete_try:
            try:
                # 延迟删除，确保文件已发送
                import threading
                def delete_file_after_delay():
                    import time
                    time.sleep(2)  # 等待2秒确保文件已发送
                    try:
                        if os.path.exists(source_path):
                            os.remove(source_path)
                            print(f"已删除临时文件: {source_path}")
                    except Exception as e:
                        print(f"删除临时文件失败: {e}")
                
                threading.Thread(target=delete_file_after_delay, daemon=True).start()
            except Exception as e:
                print(f"启动删除线程失败: {e}")
        
        return response
        
    except Exception as e:
        print(f"下载文件失败: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"下载文件失败: {str(e)}"}), 500


@audio_bp.route('/DownloadRecord', methods=['GET'])
def download_record_file():
    """
    下载录音文件
    - 优先从录音试听目录 record/try 中查找
    - 如有需要，将文件复制到 record/download 目录后返回
    """
    try:
        filename = request.args.get('filename')
        if not filename:
            return jsonify({"error": "缺少文件名参数"}), 400

        source_path = os.path.join(AUDIO_RECORD_TRY_DIR, filename)
        if not os.path.exists(source_path):
            # 如果试听目录中没有，可以从下载目录中读取（兼容）
            download_path = os.path.join(AUDIO_RECORD_DOWNLOAD_DIR, filename)
            if os.path.exists(download_path):
                return send_file(download_path, as_attachment=True, download_name=filename)
            return jsonify({"error": "录音文件未找到"}), 404

        # 确保下载目录存在
        os.makedirs(AUDIO_RECORD_DOWNLOAD_DIR, exist_ok=True)
        download_save_path = os.path.join(AUDIO_RECORD_DOWNLOAD_DIR, filename)

        # 复制一份到下载目录
        try:
            shutil.copy2(source_path, download_save_path)
            print(f"已将录音文件复制到下载目录: {download_save_path}")
        except Exception as e:
            print(f"复制录音文件到下载目录失败: {e}")
            download_save_path = source_path

        return send_file(download_save_path, as_attachment=True, download_name=filename)
    except Exception as e:
        print(f"下载录音文件失败: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"下载录音文件失败: {str(e)}"}), 500


# ============================================
# 7. 获取降噪后音频的播放URL（用于试听）
# ============================================
@audio_bp.route('/getAudioUrl/<path:filename>', methods=['GET'])
def get_audio_url(filename):
    """
    获取音频文件的访问URL（用于试听）
    返回可以直接播放的URL
    """
    try:
        # 尝试从多个目录查找文件
        # 1. try目录（最优先）
        try_path = os.path.join(AUDIO_TRY_DIR, filename)
        if os.path.exists(try_path):
            return jsonify({
                "success": True,
                "url": f"/api/audio/play/{filename}",
                "filename": filename
            }), 200
        
        # 2. uploads/DeNoise
        denoise_path = os.path.join(AUDIO_UPLOAD_DIR, 'DeNoise', filename)
        if os.path.exists(denoise_path):
            return jsonify({
                "success": True,
                "url": f"/api/audio/play/{filename}",
                "filename": filename
            }), 200
        
        # 3. output/DeNoise
        output_path = os.path.join(AUDIO_OUTPUT_DIR, 'DeNoise', filename)
        if os.path.exists(output_path):
            return jsonify({
                "success": True,
                "url": f"/api/audio/play/{filename}",
                "filename": filename
            }), 200
        
        # 4. separated
        separated_path = os.path.join(AUDIO_UPLOAD_DIR, 'separated', filename)
        if os.path.exists(separated_path):
            return jsonify({
                "success": True,
                "url": f"/api/audio/play/{filename}",
                "filename": filename
            }), 200
        
        return jsonify({"error": "文件未找到"}), 404
        
    except Exception as e:
        print(f"获取音频URL失败: {e}")
        return jsonify({"error": f"获取音频URL失败: {str(e)}"}), 500


# ============================================
# 8. 播放音频文件（用于试听）
# ============================================
@audio_bp.route('/audio/play/<path:filename>', methods=['GET'])
def play_audio(filename):
    """
    播放音频文件（用于试听）
    返回音频文件流，支持在线播放
    """
    try:
        print(f"尝试播放音频文件: {filename}")
        
        # 尝试从多个目录查找文件
        # 1. try目录（最优先，降噪后的临时文件在这里）
        try_path = os.path.join(AUDIO_TRY_DIR, filename)
        if os.path.exists(try_path):
            print(f"找到文件: {try_path}")
            return send_file(try_path, mimetype='audio/wav')
        
        # 2. uploads/DeNoise（兼容旧路径）
        denoise_path = os.path.join(AUDIO_UPLOAD_DIR, 'DeNoise', filename)
        if os.path.exists(denoise_path):
            print(f"找到文件: {denoise_path}")
            return send_file(denoise_path, mimetype='audio/wav')
        
        # 3. output/DeNoise
        output_path = os.path.join(AUDIO_OUTPUT_DIR, 'DeNoise', filename)
        if os.path.exists(output_path):
            print(f"找到文件: {output_path}")
            return send_file(output_path, mimetype='audio/wav')
        
        # 4. separated（分离后的文件）
        separated_path = os.path.join(AUDIO_UPLOAD_DIR, 'separated', filename)
        if os.path.exists(separated_path):
            print(f"找到文件: {separated_path}")
            return send_file(separated_path, mimetype='audio/wav')
        
        # 5. input（原始文件）
        input_path = os.path.join(AUDIO_INPUT_DIR, filename)
        if os.path.exists(input_path):
            print(f"找到文件: {input_path}")
            return send_file(input_path, mimetype='audio/wav')
        
        # 如果都没找到，列出可用文件用于调试
        print(f"文件未找到: {filename}")
        print(f"搜索路径:")
        print(f"  - {try_path}")
        print(f"  - {denoise_path}")
        print(f"  - {output_path}")
        print(f"  - {separated_path}")
        print(f"  - {input_path}")
        
        # 列出try目录中的文件
        if os.path.exists(AUDIO_TRY_DIR):
            files = os.listdir(AUDIO_TRY_DIR)
            print(f"try目录中的文件: {files[:10]}")
        
        return jsonify({
            "error": "文件未找到",
            "filename": filename,
            "searched_paths": [
                try_path,
                denoise_path,
                output_path,
                separated_path,
                input_path
            ]
        }), 404
        
    except Exception as e:
        print(f"播放音频文件失败: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"播放音频文件失败: {str(e)}"}), 500


@audio_bp.route('/audio/playRecord/<path:filename>', methods=['GET'])
def play_record_audio(filename):
    """
    播放录音文件（用于试听）
    从 Audio/record/try 或 Audio/record/download 目录中读取
    """
    try:
        # 1. 试听目录
        try_path = os.path.join(AUDIO_RECORD_TRY_DIR, filename)
        if os.path.exists(try_path):
            # 根据扩展名选择合适的 MIME 类型
            ext = os.path.splitext(filename)[1].lower()
            mimetype = 'audio/mpeg' if ext == '.mp3' else 'audio/wav'
            return send_file(try_path, mimetype=mimetype)

        # 2. 下载目录
        download_path = os.path.join(AUDIO_RECORD_DOWNLOAD_DIR, filename)
        if os.path.exists(download_path):
            ext = os.path.splitext(filename)[1].lower()
            mimetype = 'audio/mpeg' if ext == '.mp3' else 'audio/wav'
            return send_file(download_path, mimetype=mimetype)

        return jsonify({"error": "录音文件未找到"}), 404
    except Exception as e:
        print(f"播放录音文件失败: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"播放录音文件失败: {str(e)}"}), 500

