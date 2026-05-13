#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
音频降噪系统 - Flask 后端主程序
"""
import warnings
warnings.filterwarnings("ignore")
import os
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

os.environ['PYTHONWARNINGS'] = 'ignore'
os.environ['PYTHONUNBUFFERED'] = '1'

from flask import Flask, send_from_directory
from flask_cors import CORS
from config import AUDIO_INPUT_DIR, AUDIO_OUTPUT_DIR, AUDIO_UPLOAD_DIR, AUDIO_DOWNLOAD_DIR, AUDIO_TRY_DIR, VISUALIZATION_IMAGE_DIR, BASE_DIR

# 设置matplotlib后端
try:
    import matplotlib
    matplotlib.use('Agg')
except:
    pass

def create_app():
    """创建并配置 Flask 应用"""
    app = Flask(__name__)
    
    # 从config导入配置
    from config import Config, FLASK_CONFIG
    app.config.from_object(Config)
    # 同时更新 FLASK_CONFIG 以保持兼容性
    app.config.update(FLASK_CONFIG)
    
    # 启用 CORS（跨域资源共享）
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
    
    # 注册蓝图
    try:
        from api.audio import audio_bp
        app.register_blueprint(audio_bp, url_prefix='/api')
        print("[成功] 音频路由模块已注册")
    except Exception as e:
        print(f"[警告] 音频路由模块注册失败: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        from api.auth import auth_bp
        app.register_blueprint(auth_bp, url_prefix='/api')
        print("[成功] 用户路由模块已注册")
    except Exception as e:
        print(f"[警告] 用户路由模块注册失败: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        from routes.user import user_bp
        app.register_blueprint(user_bp)
        print("[成功] 用户路由模块（routes.user）已注册")
    except Exception as e:
        print(f"[警告] 用户路由模块（routes.user）注册失败: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        from api.ai import ai_bp
        app.register_blueprint(ai_bp, url_prefix='/api')
        print("[成功] AI路由模块已注册")
    except Exception as e:
        print(f"[警告] AI路由模块注册失败: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        from api.data import data_bp
        app.register_blueprint(data_bp, url_prefix='/api')
        print("[成功] 数据路由模块已注册")
    except Exception as e:
        print(f"[警告] 数据路由模块注册失败: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        from api.admin import admin_bp
        app.register_blueprint(admin_bp, url_prefix='/api')
        print("[成功] 管理路由模块已注册")
    except Exception as e:
        print(f"[警告] 管理路由模块注册失败: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        from routes.statistics import statistics_bp
        app.register_blueprint(statistics_bp)
        print("[成功] 统计路由模块已注册")
    except Exception as e:
        print(f"[警告] 统计路由模块注册失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 确保目录存在
    os.makedirs(AUDIO_INPUT_DIR, exist_ok=True)
    os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)
    os.makedirs(AUDIO_UPLOAD_DIR, exist_ok=True)
    os.makedirs(AUDIO_DOWNLOAD_DIR, exist_ok=True)
    os.makedirs(AUDIO_TRY_DIR, exist_ok=True)
    
    print("[信息] 音频目录已初始化")
    print(f"  - 输入目录: {AUDIO_INPUT_DIR}")
    print(f"  - 输出目录: {AUDIO_OUTPUT_DIR}")
    print(f"  - 上传目录: {AUDIO_UPLOAD_DIR}")
    print(f"  - 下载目录: {AUDIO_DOWNLOAD_DIR}")
    print(f"  - 临时目录: {AUDIO_TRY_DIR}")
    
    # 检查 FFmpeg 是否可用（用于处理非 WAV 格式音频）
    try:
        from api.audio import check_ffmpeg_available, get_ffmpeg_path, configure_pydub_ffmpeg
        # 尝试配置 FFmpeg
        if configure_pydub_ffmpeg():
            ffmpeg_path = get_ffmpeg_path()
            print(f"[成功] FFmpeg 已配置: {ffmpeg_path}")
        else:
            print("[警告] FFmpeg 未安装或不在 PATH 中")
            print("       非 WAV 格式音频文件（MP3、OGG 等）需要 FFmpeg 才能处理")
            print("       解决方案：")
            print("       1. 下载 FFmpeg: https://www.gyan.dev/ffmpeg/builds/")
            print("       2. 解压到 C:\\ffmpeg，将 C:\\ffmpeg\\bin 添加到系统 PATH")
            print("       3. 或在 backend/config.py 中设置 FFMPEG_PATH")
            print("       4. 或直接上传 WAV 格式文件（无需 FFmpeg）")
    except Exception as e:
        print(f"[警告] 检查 FFmpeg 时出错: {e}")
        import traceback
        traceback.print_exc()
    
    # 启动时自动生成可视化图表
    try:
        from routes.statistics import _load_statistics_raw
        import matplotlib
        matplotlib.use('Agg')
        from matplotlib import font_manager
        import matplotlib.pyplot as plt
        from config import VISUALIZATION_IMAGE_DIR, BASE_DIR
        
        print("[信息] 开始生成可视化图表...")
        
        # 配置中文字体
        font_path = os.path.join(BASE_DIR, 'SimHei.ttf')
        if os.path.exists(font_path):
            try:
                font_manager.fontManager.addfont(font_path)
                font_prop = font_manager.FontProperties(fname=font_path)
                font_name = font_prop.get_name()
                matplotlib.rcParams['font.family'] = font_name
                matplotlib.rcParams['font.sans-serif'] = [font_name]
            except Exception as e:
                print(f"[警告] 加载字体失败: {e}")
        matplotlib.rcParams['axes.unicode_minus'] = False
        
        # 加载统计数据
        data = _load_statistics_raw()
        
        # 1. 生成日期折线图
        dates = [item['date'] for item in data['dateData']]
        counts = [item['count'] for item in data['dateData']]
        plt.figure(figsize=(10, 5))
        plt.plot(dates, counts, marker='o', linewidth=2, markersize=4, color='#6A5ACD')
        plt.fill_between(dates, counts, alpha=0.3, color='#6A5ACD')
        plt.xticks(rotation=45, fontsize=8)
        plt.title('日期－降噪次数', fontsize=14, fontweight='bold')
        plt.xlabel('日期', fontsize=10)
        plt.ylabel('次数', fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        date_path = os.path.join(VISUALIZATION_IMAGE_DIR, 'date_line.png')
        plt.savefig(date_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"[成功] 日期折线图已生成: {date_path}")
        
        # 2. 生成周次饼图
        week_labels = [item['week'] for item in data['weekData']]
        week_counts = [item['count'] for item in data['weekData']]
        plt.figure(figsize=(8, 8))
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE']
        plt.pie(week_counts, labels=week_labels, autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('周次－降噪次数', fontsize=14, fontweight='bold')
        plt.tight_layout()
        week_path = os.path.join(VISUALIZATION_IMAGE_DIR, 'week_pie.png')
        plt.savefig(week_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"[成功] 周次饼图已生成: {week_path}")
        
        # 3. 生成时间折线图
        hours = [item['hour'] for item in data['timeData']]
        hour_counts = [item['count'] for item in data['timeData']]
        plt.figure(figsize=(10, 5))
        plt.plot(hours, hour_counts, marker='o', linewidth=2, markersize=4, color='#44ADFB')
        plt.fill_between(hours, hour_counts, alpha=0.3, color='#44ADFB')
        plt.title('一天中时间－降噪次数', fontsize=14, fontweight='bold')
        plt.xlabel('小时', fontsize=10)
        plt.ylabel('次数', fontsize=10)
        plt.xticks(range(0, 24, 2))
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        time_path = os.path.join(VISUALIZATION_IMAGE_DIR, 'time_line.png')
        plt.savefig(time_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"[成功] 时间折线图已生成: {time_path}")
        
        # 4. 生成活跃用户柱状图
        user_names = [item['userName'] for item in data['userData']]
        user_counts = [item['count'] for item in data['userData']]
        plt.figure(figsize=(10, 5))
        colors_bar = plt.cm.viridis(range(len(user_names)))
        plt.bar(user_names, user_counts, color=colors_bar)
        plt.title('活跃用户－降噪次数', fontsize=14, fontweight='bold')
        plt.xlabel('用户', fontsize=10)
        plt.ylabel('次数', fontsize=10)
        plt.xticks(rotation=45, fontsize=8, ha='right')
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        user_path = os.path.join(VISUALIZATION_IMAGE_DIR, 'user_bar.png')
        plt.savefig(user_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"[成功] 用户柱状图已生成: {user_path}")
        
        print("[成功] 所有可视化图表已生成完成")
    except Exception as e:
        print(f"[警告] 生成可视化图表失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 启动定时清理任务（清理超过24小时未下载的临时文件）
    try:
        import threading
        import time
        
        def cleanup_old_files():
            """清理超过24小时未下载的临时文件"""
            while True:
                try:
                    time.sleep(3600)  # 每小时检查一次
                    if os.path.exists(AUDIO_TRY_DIR):
                        current_time = time.time()
                        for filename in os.listdir(AUDIO_TRY_DIR):
                            file_path = os.path.join(AUDIO_TRY_DIR, filename)
                            if os.path.isfile(file_path):
                                # 获取文件修改时间
                                file_mtime = os.path.getmtime(file_path)
                                # 如果文件超过24小时未修改，删除
                                if current_time - file_mtime > 86400:  # 24小时 = 86400秒
                                    try:
                                        os.remove(file_path)
                                        print(f"已清理过期临时文件: {filename}")
                                    except Exception as e:
                                        print(f"清理文件失败 {filename}: {e}")
                except Exception as e:
                    print(f"清理任务错误: {e}")
        
        cleanup_thread = threading.Thread(target=cleanup_old_files, daemon=True)
        cleanup_thread.start()
        print("[信息] 临时文件自动清理任务已启动（24小时过期）")
    except Exception as e:
        print(f"[警告] 启动清理任务失败: {e}")

    # 添加静态文件路由，用于访问可视化图片
    @app.route('/static/visualization/<path:filename>')
    def serve_visualization_image(filename):
        """提供可视化图片的静态文件访问"""
        try:
            return send_from_directory(VISUALIZATION_IMAGE_DIR, filename)
        except Exception as e:
            print(f"提供静态文件失败: {e}")
            return f"文件未找到: {filename}", 404
    
    # 调试路由：打印当前应用注册的所有URL规则
    @app.route('/debug_routes')
    def debug_routes():
        """
        调试用：返回当前应用的 URL 映射列表，
        方便确认 /api/separateAudio 等路由是否成功注册。
        """
        return str(app.url_map)

    return app

if __name__ == '__main__':
    # 允许通过环境变量覆盖端口，默认5000（保持原先端口）
    port = int(os.environ.get('PORT', '5000'))
    app = create_app()
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)
