#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查服务器状态
"""

import requests
import sys

BASE_URL = "http://127.0.0.1:5000"

print("=" * 60)
print("检查服务器状态")
print("=" * 60)

# 测试服务器是否响应
try:
    # 尝试访问一个不存在的路由，如果返回404说明服务器在运行
    response = requests.get(f"{BASE_URL}/api/test", timeout=2)
    print(f"[成功] 服务器正在运行")
    print(f"  状态码: {response.status_code}")
    print(f"  服务器响应正常")
except requests.exceptions.ConnectionError:
    print("[失败] 无法连接到服务器")
    print("  请确保后端服务器正在运行")
    sys.exit(1)
except Exception as e:
    print(f"[信息] 服务器可能正在运行，但测试请求失败: {e}")

# 测试实际API
print("\n测试实际API接口...")
try:
    # 测试 getAudioInfo（会返回错误，但说明路由存在）
    response = requests.post(
        f"{BASE_URL}/api/getAudioInfo",
        data={"filePath": "test", "filename": "test", "extension": "wav"},
        timeout=2
    )
    print(f"  /api/getAudioInfo: 状态码 {response.status_code}")
    if response.status_code != 404:
        print("  [成功] 路由已注册")
    else:
        print("  [失败] 路由未找到")
except Exception as e:
    print(f"  [错误] {e}")

print("\n" + "=" * 60)
print("检查完成")
print("=" * 60)

