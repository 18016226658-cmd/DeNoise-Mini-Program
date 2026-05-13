#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速系统检查
"""
import sys
import os

print("=" * 60)
print("系统快速检查")
print("=" * 60)

# 检查后端
print("\n[后端检查]")
try:
    from app import create_app
    app = create_app()
    print("[OK] Flask应用创建成功")
    
    # 检查蓝图
    blueprints = list(app.blueprints.keys())
    print(f"[OK] 已注册蓝图: {', '.join(blueprints)}")
    
    # 检查关键路由
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(str(rule))
    
    key_routes = ['/api/DeNoiseAudio', '/api/separateAudio', '/api/uploadAudio', '/api/getAudioInfo']
    for route in key_routes:
        if any(route in r for r in routes):
            print(f"[OK] 路由已注册: {route}")
        else:
            print(f"[WARN] 路由未找到: {route}")
    
    # 检查模块
    try:
        from deNoise import DeNoise_all
        print("[OK] 降噪模块已导入")
    except Exception as e:
        print(f"[ERROR] 降噪模块导入失败: {e}")
    
    # 检查目录
    from config import AUDIO_INPUT_DIR, AUDIO_OUTPUT_DIR, AUDIO_UPLOAD_DIR
    for name, path in [("输入目录", AUDIO_INPUT_DIR), ("输出目录", AUDIO_OUTPUT_DIR), ("上传目录", AUDIO_UPLOAD_DIR)]:
        if os.path.exists(path):
            print(f"[OK] {name}存在: {path}")
        else:
            os.makedirs(path, exist_ok=True)
            print(f"[OK] {name}已创建: {path}")
            
except Exception as e:
    print(f"[ERROR] 后端检查失败: {e}")
    import traceback
    traceback.print_exc()

# 检查前端
print("\n[前端检查]")
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'wxminpro')
if os.path.exists(frontend_path):
    print(f"[OK] 前端目录存在: {frontend_path}")
    
    # 检查关键文件
    key_files = [
        'app.json',
        'config/api.js',
        'pages/DeNoise/DeNoise.js',
        'subpackages/audio/pages/AudioSep/AudioSep.js'
    ]
    
    for file_path in key_files:
        full_path = os.path.join(frontend_path, file_path)
        if os.path.exists(full_path):
            print(f"[OK] 文件存在: {file_path}")
        else:
            print(f"[WARN] 文件不存在: {file_path}")
else:
    print(f"[ERROR] 前端目录不存在: {frontend_path}")

print("\n" + "=" * 60)
print("检查完成")
print("=" * 60)
print("\n下一步:")
print("  1. 启动后端: cd backend && python app.py")
print("  2. 在微信开发者工具中打开wxminpro项目")
print("  3. 测试降噪和分离功能")


