#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
可靠的服务器启动脚本
"""

import sys
import os

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

print("正在导入应用模块...", flush=True)

try:
    from app import app
    
    if app is None:
        print("[错误] app 对象为 None", flush=True)
        sys.exit(1)
    
    print("[成功] 应用模块导入成功", flush=True)
    print("=" * 60, flush=True)
    print("音频降噪系统后端服务", flush=True)
    print("服务地址: http://127.0.0.1:5000", flush=True)
    print("=" * 60, flush=True)
    print("正在启动服务器...", flush=True)
    print("提示：按 Ctrl+C 停止服务", flush=True)
    print("=" * 60, flush=True)
    print("", flush=True)
    
    # 启动服务器
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    
except KeyboardInterrupt:
    print("\n[信息] 服务器已停止", flush=True)
    sys.exit(0)
except Exception as e:
    print(f"[错误] 启动失败: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)

