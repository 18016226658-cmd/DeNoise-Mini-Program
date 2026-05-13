#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
最简单的启动脚本 - 直接启动，不做任何检查
"""

import warnings
warnings.filterwarnings("ignore")
import os
os.environ['PYTHONWARNINGS'] = 'ignore'
os.environ['PYTHONUNBUFFERED'] = '1'

try:
    import matplotlib
    matplotlib.use('Agg')
except:
    pass

from app import app

# 验证 app 对象
if app is None:
    print("[错误] app 对象为 None，无法启动服务器")
    exit(1)

print("=" * 60, flush=True)
print("音频降噪系统后端服务", flush=True)
print("服务地址: http://127.0.0.1:5000", flush=True)
print("=" * 60, flush=True)
print("正在启动服务器...", flush=True)
print("提示：服务器启动后，此窗口将保持运行状态", flush=True)
print("按 Ctrl+C 可以停止服务器", flush=True)
print("=" * 60, flush=True)
print("", flush=True)

try:
    print("[信息] 开始启动Flask服务器...", flush=True)
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
except KeyboardInterrupt:
    print("\n[信息] 服务器已停止", flush=True)
except Exception as e:
    print(f"[错误] 启动服务器失败: {e}", flush=True)
    import traceback
    traceback.print_exc()
    exit(1)

