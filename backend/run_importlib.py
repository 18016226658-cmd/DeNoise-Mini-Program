#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
使用 importlib 安全导入 - 尝试更安全的模块导入方式
"""

import sys
import os
import importlib.util

# 基础设置
import warnings
warnings.filterwarnings("ignore")
os.environ['PYTHONWARNINGS'] = 'ignore'
os.environ['PYTHONUNBUFFERED'] = '1'

# 设置 matplotlib 后端
try:
    import matplotlib
    matplotlib.use('Agg')
except:
    pass

print("使用 importlib 导入 app 模块...", flush=True)

try:
    # 使用 importlib 导入模块
    spec = importlib.util.spec_from_file_location("app", "app.py")
    if spec is None or spec.loader is None:
        raise ImportError("无法创建模块规范")
    
    app_module = importlib.util.module_from_spec(spec)
    sys.modules["app"] = app_module
    
    # 执行模块
    spec.loader.exec_module(app_module)
    
    # 获取 app 对象
    app = app_module.app
    
    print("[成功] 应用模块导入成功", flush=True)
    print("=" * 60, flush=True)
    print("音频降噪系统后端服务", flush=True)
    print("服务地址: http://127.0.0.1:5000", flush=True)
    print("=" * 60, flush=True)
    print("正在启动服务器...", flush=True)
    
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    
except Exception as e:
    print(f"[错误] 导入或启动失败: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)
except KeyboardInterrupt:
    print("\n服务器已停止", flush=True)

