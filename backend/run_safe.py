#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
安全启动脚本 - 使用最少的代码启动服务器
避免复杂的打印和检查，直接启动
"""

import sys
import os

# 基础设置
import warnings
warnings.filterwarnings("ignore")
os.environ['PYTHONWARNINGS'] = 'ignore'
os.environ['PYTHONUNBUFFERED'] = '1'

# 设置 matplotlib 后端（在导入任何其他库之前）
try:
    import matplotlib
    matplotlib.use('Agg')
except:
    pass

# 直接导入并启动
try:
    from app import app
    print("=" * 60)
    print("音频降噪系统后端服务")
    print("服务地址: http://127.0.0.1:5000")
    print("=" * 60)
    print("正在启动服务器...")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
except KeyboardInterrupt:
    print("\n服务器已停止")
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

