# backend/utils/audio_converter.py
# ============================================
# 音频格式转换工具模块
# ============================================
"""
音频格式转换工具
功能：提供多种方案将音频文件转换为 WAV 格式
支持：自动选择最佳转换方案，支持多种格式
"""

import os
import logging
from typing import Optional, Tuple

# 尝试导入配置
try:
    from config import FFMPEG_PATH
except ImportError:
    FFMPEG_PATH = None

logger = logging.getLogger(__name__)

# 支持的格式映射
FORMAT_SUPPORT = {
    'wav': {'ffmpeg': True, 'soundfile': True, 'wave': True, 'scipy': True},
    'ogg': {'ffmpeg': True, 'soundfile': True, 'wave': False, 'scipy': False},
    'flac': {'ffmpeg': True, 'soundfile': True, 'wave': False, 'scipy': False},
    'mp3': {'ffmpeg': True, 'soundfile': False, 'wave': False, 'scipy': False},
    'aac': {'ffmpeg': True, 'soundfile': False, 'wave': False, 'scipy': False},
    'm4a': {'ffmpeg': True, 'soundfile': False, 'wave': False, 'scipy': False},
}


class AudioConverter:
    """音频格式转换器，自动选择最佳方案"""
    
    def __init__(self):
        self.available_converters = self._detect_available_converters()
        logger.info(f"可用的音频转换器: {self.available_converters}")
    
    def _detect_available_converters(self) -> dict:
        """检测可用的转换器"""
        converters = {
            'ffmpeg': False,
            'soundfile': False,
            'wave': True,  # Python 标准库
            'scipy': False,
        }
        
        # 检测 FFmpeg
        try:
            from pydub.utils import which
            
            # 1. 优先使用配置文件中的路径
            if FFMPEG_PATH and os.path.exists(FFMPEG_PATH):
                converters['ffmpeg'] = True
                logger.info(f"从配置中检测到 FFmpeg: {FFMPEG_PATH}")
            else:
                # 2. 尝试从系统 PATH 中查找
                ffmpeg_path = which("ffmpeg")
                if ffmpeg_path:
                    converters['ffmpeg'] = True
                    logger.info(f"从系统 PATH 中检测到 FFmpeg: {ffmpeg_path}")
                else:
                    # 3. 检查常见路径（包括自动检测 C:\ffmpeg 下的子目录）
                    common_paths = [
                        r"C:\ffmpeg\bin\ffmpeg.exe",
                        r"C:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe",
                        r"C:\ffmpeg\ffmpeg-7.0-essentials_build\bin\ffmpeg.exe",
                        r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
                        r"D:\ffmpeg\bin\ffmpeg.exe",
                        r"D:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe",
                    ]
                    
                    # 自动检测 C:\ffmpeg 下的所有子目录
                    if os.path.exists(r"C:\ffmpeg"):
                        try:
                            for item in os.listdir(r"C:\ffmpeg"):
                                potential_path = os.path.join(r"C:\ffmpeg", item, "bin", "ffmpeg.exe")
                                if os.path.exists(potential_path):
                                    common_paths.insert(0, potential_path)
                        except:
                            pass
                    
                    for path in common_paths:
                        if os.path.exists(path):
                            converters['ffmpeg'] = True
                            logger.info(f"从常见路径检测到 FFmpeg: {path}")
                            break
        except Exception as e:
            logger.warning(f"检测 FFmpeg 时出错: {e}")
        
        # 检测 soundfile
        try:
            import soundfile as sf
            converters['soundfile'] = True
        except ImportError:
            pass
        
        # 检测 scipy
        try:
            from scipy.io import wavfile
            converters['scipy'] = True
        except ImportError:
            pass
        
        return converters
    
    def convert_to_wav(
        self, 
        input_file: str, 
        output_file: Optional[str] = None,
        format_hint: Optional[str] = None
    ) -> Tuple[bool, str, Optional[str]]:
        """
        将音频文件转换为 WAV 格式
        
        Args:
            input_file: 输入文件路径
            output_file: 输出文件路径（如果为 None，自动生成）
            format_hint: 格式提示（如 'mp3', 'ogg' 等）
        
        Returns:
            (success, message, output_path)
            - success: 是否成功
            - message: 消息
            - output_path: 输出文件路径（如果成功）
        """
        if not os.path.exists(input_file):
            return False, f"输入文件不存在: {input_file}", None
        
        # 自动生成输出文件名
        if output_file is None:
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}_converted.wav"
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
        
        # 检测文件格式
        detected_format = format_hint or self._detect_format(input_file)
        if not detected_format:
            detected_format = os.path.splitext(input_file)[1][1:].lower()
        
        logger.info(f"检测到音频格式: {detected_format}, 输入文件: {input_file}")
        
        # 如果已经是 WAV，直接复制或验证
        if detected_format == 'wav':
            try:
                # 验证 WAV 文件是否有效
                import wave
                with wave.open(input_file, 'rb') as wf:
                    wf.getparams()  # 验证文件格式
                # 如果输出路径不同，复制文件
                if os.path.abspath(input_file) != os.path.abspath(output_file):
                    import shutil
                    shutil.copy2(input_file, output_file)
                return True, "文件已经是 WAV 格式", output_file
            except Exception as e:
                logger.warning(f"WAV 文件验证失败，尝试重新转换: {e}")
        
        # 尝试多种转换方案
        conversion_methods = [
            ('ffmpeg', self._convert_with_ffmpeg),
            ('soundfile', self._convert_with_soundfile),
            ('scipy', self._convert_with_scipy),
        ]
        
        for method_name, converter_func in conversion_methods:
            if not self.available_converters.get(method_name, False):
                continue
            
            # 检查该方法是否支持该格式
            format_support = FORMAT_SUPPORT.get(detected_format, {})
            if not format_support.get(method_name, False):
                continue
            
            try:
                logger.info(f"尝试使用 {method_name} 转换 {detected_format} 格式...")
                success, message = converter_func(input_file, output_file, detected_format)
                if success:
                    logger.info(f"✓ 使用 {method_name} 成功转换: {output_file}")
                    return True, message, output_file
            except Exception as e:
                logger.warning(f"使用 {method_name} 转换失败: {e}")
                continue
        
        # 所有方案都失败
        error_msg = self._generate_error_message(detected_format)
        return False, error_msg, None
    
    def _detect_format(self, file_path: str) -> Optional[str]:
        """检测音频文件格式（通过文件头）"""
        try:
            with open(file_path, 'rb') as f:
                header = f.read(12)
                
            # WAV: RIFF...WAVE
            if header[:4] == b'RIFF' and header[8:12] == b'WAVE':
                return 'wav'
            
            # MP3: ID3 标签或 MP3 帧头
            if header[:3] == b'ID3' or header[:2] == b'\xff\xfb':
                return 'mp3'
            
            # OGG: OggS
            if header[:4] == b'OggS':
                return 'ogg'
            
            # FLAC: fLaC
            if header[:4] == b'fLaC':
                return 'flac'
            
            # M4A/AAC: ftyp
            if header[4:8] == b'ftyp':
                return 'm4a'
            
        except Exception as e:
            logger.debug(f"格式检测失败: {e}")
        
        return None
    
    def _convert_with_ffmpeg(
        self, 
        input_file: str, 
        output_file: str, 
        format_hint: str
    ) -> Tuple[bool, str]:
        """使用 FFmpeg 转换（优先使用 subprocess 直接调用，fallback 到 pydub）"""
        import subprocess
            
        # 获取 FFmpeg 路径（使用与 audio.py 相同的逻辑）
        ffmpeg_path = None
        
        # 1. 优先使用配置文件中的路径
        if FFMPEG_PATH and os.path.exists(FFMPEG_PATH):
            ffmpeg_path = FFMPEG_PATH
        else:
            # 2. 尝试从系统 PATH 中查找
            try:
                from pydub.utils import which
                ffmpeg_path = which("ffmpeg")
            except:
                pass
            
            if not ffmpeg_path:
                # 3. 检查常见路径（包括自动检测 C:\ffmpeg 下的子目录）
                common_paths = [
                    r"C:\ffmpeg\bin\ffmpeg.exe",
                    r"C:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe",
                    r"C:\ffmpeg\ffmpeg-7.0-essentials_build\bin\ffmpeg.exe",
                    r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
                    r"D:\ffmpeg\bin\ffmpeg.exe",
                    r"D:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe",
                ]
                
                # 自动检测 C:\ffmpeg 下的所有子目录
                if os.path.exists(r"C:\ffmpeg"):
                    try:
                        for item in os.listdir(r"C:\ffmpeg"):
                            potential_path = os.path.join(r"C:\ffmpeg", item, "bin", "ffmpeg.exe")
                            if os.path.exists(potential_path):
                                common_paths.insert(0, potential_path)
                    except:
                        pass
                
                for path in common_paths:
                    if os.path.exists(path):
                        ffmpeg_path = path
                        break
        
        if not ffmpeg_path:
            return False, "FFmpeg 不可用，未找到 FFmpeg 可执行文件"
        
        # 确保路径是绝对路径
        ffmpeg_exe = os.path.abspath(ffmpeg_path)
        
        # 如果是目录，添加 ffmpeg.exe
        if os.path.isdir(ffmpeg_exe):
            ffmpeg_exe = os.path.join(ffmpeg_exe, "ffmpeg.exe")
        elif not ffmpeg_exe.endswith(".exe"):
            if not ffmpeg_exe.endswith("ffmpeg"):
                ffmpeg_exe = os.path.join(ffmpeg_exe, "ffmpeg.exe") if os.path.isdir(ffmpeg_exe) else ffmpeg_exe
        
        # 确保 ffmpeg.exe 存在
        if not os.path.exists(ffmpeg_exe):
            return False, f"FFmpeg 可执行文件不存在: {ffmpeg_exe}"
        
        logger.info(f"使用 FFmpeg 路径: {ffmpeg_exe}")
        
        # 方法1：尝试直接使用 subprocess 调用 FFmpeg（更可靠）
        try:
            # 构建 FFmpeg 命令
            cmd = [
                ffmpeg_exe,
                '-i', input_file,  # 输入文件
                '-y',  # 覆盖输出文件
                '-acodec', 'pcm_s16le',  # 使用 PCM 16-bit little-endian 编码
                '-ar', '44100',  # 采样率 44.1kHz
                '-ac', '2',  # 立体声
                output_file
            ]
            
            logger.info(f"执行 FFmpeg 命令: {' '.join(cmd)}")
            
            # 执行转换
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5分钟超时
                check=False
            )
            
            if result.returncode == 0:
                if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                    logger.info(f"✓ 使用 subprocess 直接调用 FFmpeg 成功转换: {output_file}")
                    return True, f"使用 FFmpeg 成功转换 {format_hint} 格式"
                else:
                    logger.warning(f"FFmpeg 命令成功但输出文件不存在或为空")
            else:
                logger.warning(f"FFmpeg 命令失败 (返回码: {result.returncode}): {result.stderr}")
        except subprocess.TimeoutExpired:
            logger.error(f"FFmpeg 转换超时")
            return False, "FFmpeg 转换超时（超过5分钟）"
        except Exception as e:
            logger.warning(f"直接调用 FFmpeg 失败，尝试使用 pydub: {e}")
        
        # 方法2：fallback 到 pydub
        try:
            from pydub import AudioSegment
            
            # 配置 pydub 使用指定路径
            AudioSegment.converter = ffmpeg_exe
            
            # 同时配置 ffprobe（pydub 也需要它，通常在同一目录）
            ffprobe_exe = ffmpeg_exe.replace("ffmpeg.exe", "ffprobe.exe")
            if os.path.exists(ffprobe_exe):
                AudioSegment.ffprobe = ffprobe_exe
                logger.info(f"使用 FFprobe 路径: {AudioSegment.ffprobe}")
            
            # 尝试转换
            audio = AudioSegment.from_file(input_file)
            audio.export(output_file, format='wav')
            
            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                logger.info(f"✓ 使用 pydub 成功转换: {output_file}")
                return True, f"使用 FFmpeg 成功转换 {format_hint} 格式"
            else:
                return False, "转换完成但输出文件无效"
        except Exception as e:
            logger.error(f"pydub 转换也失败: {e}")
            return False, f"FFmpeg 转换失败: {str(e)}"
    
    def _convert_with_soundfile(
        self, 
        input_file: str, 
        output_file: str, 
        format_hint: str
    ) -> Tuple[bool, str]:
        """使用 soundfile 转换（仅支持 OGG、FLAC）"""
        try:
            import soundfile as sf
            
            if format_hint not in ['ogg', 'flac']:
                return False, f"soundfile 不支持 {format_hint} 格式"
            
            data, samplerate = sf.read(input_file)
            sf.write(output_file, data, samplerate, format='WAV')
            return True, f"使用 soundfile 成功转换 {format_hint} 格式"
        except ImportError:
            return False, "soundfile 未安装"
        except Exception as e:
            return False, f"soundfile 转换失败: {str(e)}"
    
    def _convert_with_scipy(
        self, 
        input_file: str, 
        output_file: str, 
        format_hint: str
    ) -> Tuple[bool, str]:
        """使用 scipy.io.wavfile 转换（仅支持 WAV）"""
        try:
            from scipy.io import wavfile
            
            if format_hint != 'wav':
                return False, f"scipy.io.wavfile 仅支持 WAV 格式"
            
            rate, data = wavfile.read(input_file)
            wavfile.write(output_file, rate, data)
            return True, "使用 scipy 成功处理 WAV 文件"
        except ImportError:
            return False, "scipy 未安装"
        except Exception as e:
            return False, f"scipy 转换失败: {str(e)}"
    
    def _generate_error_message(self, format_hint: str) -> str:
        """生成错误消息"""
        format_name = format_hint.upper() if format_hint else "未知格式"
        
        # 检查可用的转换器
        available = []
        if self.available_converters.get('ffmpeg'):
            available.append("FFmpeg")
        if self.available_converters.get('soundfile'):
            available.append("soundfile (仅 OGG/FLAC)")
        
        if not available:
            return (
                f"无法处理 {format_name} 格式的音频文件。\n\n"
                f"【解决方案】\n"
                f"1. 安装 FFmpeg（推荐）：按照 backend/FFMPEG_INSTALL_GUIDE.md 中的说明安装\n"
                f"2. 或安装 Python 库：pip install soundfile（仅支持 OGG/FLAC 格式）\n"
                f"3. 或转换为 WAV 格式后再上传（最简单）"
            )
        else:
            return (
                f"无法处理 {format_name} 格式的音频文件。\n\n"
                f"当前可用的转换器: {', '.join(available)}\n\n"
                f"【解决方案】\n"
                f"1. 安装 FFmpeg（推荐）：支持所有格式，包括 {format_name}\n"
                f"2. 或转换为 WAV 格式后再上传（最简单）"
            )


# 全局转换器实例
_converter_instance = None

def get_audio_converter() -> AudioConverter:
    """获取全局音频转换器实例（单例模式）"""
    global _converter_instance
    if _converter_instance is None:
        _converter_instance = AudioConverter()
    return _converter_instance
