#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简化的服务器启动脚本
直接启动Flask服务器
"""
import warnings
warnings.filterwarnings("ignore")

import os
import sys

# 设置环境变量
os.environ['PYTHONWARNINGS'] = 'ignore'
os.environ['PYTHONUNBUFFERED'] = '1'

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置matplotlib后端
try:
    import matplotlib
    matplotlib.use('Agg')
except:
    pass

print("=" * 60)
print("音频降噪系统后端服务启动中...")
print("=" * 60)

# 导入app
try:
    from app import app
    print("[成功] 应用模块导入成功")
except Exception as e:
    print(f"[错误] 导入应用模块失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 检查端口
import subprocess
try:
    result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True, encoding='gbk', errors='ignore')
    if ':5000' in result.stdout and 'LISTENING' in result.stdout:
        print("[警告] 端口5000已被占用，尝试清理...")
        # 这里可以添加清理端口的代码
except:
    pass

print("=" * 60)
print("服务地址: http://127.0.0.1:5000")
print("=" * 60)
print("提示：按 Ctrl+C 停止服务")
print("=" * 60)
print("")

# 启动服务器
try:
    print("正在启动Flask服务...")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
except KeyboardInterrupt:
    print("\n[信息] 服务器已停止")
except Exception as e:
    print(f"[错误] 启动服务失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

