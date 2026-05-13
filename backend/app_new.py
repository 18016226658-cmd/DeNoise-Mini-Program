#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
音频降噪系统 - Flask 后端主程序
"""
import warnings
warnings.filterwarnings("ignore")
import os
os.environ['PYTHONWARNINGS'] = 'ignore'
os.environ['PYTHONUNBUFFERED'] = '1'

from flask import Flask
from flask_cors import CORS
from config import AUDIO_INPUT_DIR, AUDIO_OUTPUT_DIR, AUDIO_UPLOAD_DIR, AUDIO_DOWNLOAD_DIR

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
    from config import FLASK_CONFIG, DB_CONFIG
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
    
    # 确保目录存在
    os.makedirs(AUDIO_INPUT_DIR, exist_ok=True)
    os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)
    os.makedirs(AUDIO_UPLOAD_DIR, exist_ok=True)
    os.makedirs(AUDIO_DOWNLOAD_DIR, exist_ok=True)
    
    print("[信息] 音频目录已初始化")
    print(f"  - 输入目录: {AUDIO_INPUT_DIR}")
    print(f"  - 输出目录: {AUDIO_OUTPUT_DIR}")
    print(f"  - 上传目录: {AUDIO_UPLOAD_DIR}")
    print(f"  - 下载目录: {AUDIO_DOWNLOAD_DIR}")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

