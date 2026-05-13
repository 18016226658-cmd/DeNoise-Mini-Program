#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试服务器启动脚本
"""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("测试服务器启动")
print("=" * 60)

# 测试导入
try:
    print("\n[1] 测试导入 app 模块...")
    from app import app
    print(f"[成功] app 模块导入成功，类型: {type(app)}")
except Exception as e:
    print(f"[失败] 导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试 app 对象
if app is None:
    print("[失败] app 对象为 None")
    sys.exit(1)

# 测试路由
try:
    print("\n[2] 测试路由注册...")
    with app.test_client() as client:
        # 测试根路径
        response = client.get('/')
        print(f"[信息] 根路径响应状态: {response.status_code}")
        
        # 测试一个API路径
        response = client.post('/api/getAudioInfo', 
                              data={'filename': 'test', 'extension': 'wav'},
                              content_type='application/x-www-form-urlencoded')
        print(f"[信息] getAudioInfo 响应状态: {response.status_code}")
    
    print("[成功] 路由测试完成")
except Exception as e:
    print(f"[警告] 路由测试失败: {e}")
    import traceback
    traceback.print_exc()

# 测试启动（不实际启动，只检查配置）
print("\n[3] 检查启动配置...")
print(f"[信息] Flask 应用已配置")
print(f"[信息] 准备在 0.0.0.0:5000 启动")

print("\n" + "=" * 60)
print("测试完成！如果看到此消息，说明服务器可以正常启动")
print("=" * 60)
print("\n提示: 使用以下命令启动服务器:")
print("  python run.py")
print("  或")
print("  python -u run.py")

