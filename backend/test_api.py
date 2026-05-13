#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试API接口 - 验证后端路由是否正常工作
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

print("=" * 60)
print("测试后端API接口")
print("=" * 60)

# 测试1: 测试 getAudioInfo 接口
print("\n[1/2] 测试 /api/getAudioInfo 接口...")
try:
    response = requests.post(
        f"{BASE_URL}/api/getAudioInfo",
        data={
            "filePath": "http://tmp/test.wav",
            "filename": "test",
            "extension": "wav"
        },
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        timeout=5
    )
    print(f"  状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"  响应: {response.json()}")
        print("  [成功] getAudioInfo 接口正常")
    else:
        print(f"  [失败] 状态码: {response.status_code}")
        print(f"  响应: {response.text[:200]}")
except requests.exceptions.ConnectionError:
    print("  [失败] 无法连接到服务器，请确保后端服务器正在运行")
except Exception as e:
    print(f"  [失败] 错误: {e}")

# 测试2: 测试 DeNoiseAudio 接口
print("\n[2/2] 测试 /api/DeNoiseAudio 接口...")
try:
    test_data = {
        "audioPath": "http://tmp/test.wav",
        "filePath": "http://tmp/test.wav",
        "fileSize": 1.0,
        "duration": "00:00:10",
        "orgFileName": "test.wav",
        "filename": "test",
        "extension": "wav",
        "title": "Test",
        "artist": "Test",
        "album": "Test",
        "MaxSepTimes": 10,
        "CurSepTimes": 0,
        "MaxNoiseTimes": 10,
        "CurNoiseTimes": 0,
        "Phone": "13800138000",
        "UserName": "Test",
        "Gender": "男",
        "Birthday": "2000-01-01",
        "N_channels": 2,
        "Order": 5
    }
    response = requests.post(
        f"{BASE_URL}/api/DeNoiseAudio",
        json=test_data,
        headers={'Content-Type': 'application/json'},
        timeout=5
    )
    print(f"  状态码: {response.status_code}")
    if response.status_code in [200, 400, 500]:  # 400/500 也算正常响应（说明路由存在）
        print("  [成功] DeNoiseAudio 接口路由存在")
        if response.status_code == 200:
            print(f"  响应: {response.json()}")
        else:
            print(f"  响应: {response.text[:200]}")
    else:
        print(f"  [失败] 状态码: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("  [失败] 无法连接到服务器，请确保后端服务器正在运行")
except Exception as e:
    print(f"  [失败] 错误: {e}")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
print("\n如果所有接口都能正常响应（即使返回错误），说明路由已正确注册。")
print("如果返回 404，说明路由未注册。")
print("如果无法连接，请确保后端服务器正在运行。")

