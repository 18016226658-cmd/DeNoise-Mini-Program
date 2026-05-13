# test/test_api.py
# API接口测试脚本

import requests
import json

# 后端API地址
BASE_URL = 'http://127.0.0.1:5000'

def test_login():
    """测试登录接口"""
    url = f'{BASE_URL}/api/Login'
    data = {
        'Phone': '13811111111',
        'Password': '123456'
    }
    
    try:
        response = requests.post(url, data=data)
        print(f"登录测试: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"登录测试失败: {e}")
        return False

def test_register():
    """测试注册接口"""
    url = f'{BASE_URL}/api/Register'
    data = {
        'Phone': '13999999999',
        'UserName': '测试用户',
        'Password': '123456',
        'Gender': '男',
        'Birthday': '2000-01-01',
        'FaceImg': '/static/image/header.png'
    }
    
    try:
        response = requests.post(url, data=data)
        print(f"注册测试: {response.status_code}")
        print(f"响应: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"注册测试失败: {e}")
        return False

def test_get_audio_info():
    """测试获取音频信息接口"""
    url = f'{BASE_URL}/api/getAudioInfo'
    data = {
        'filePath': 'test.wav',
        'filename': 'test',
        'extension': 'wav'
    }
    
    try:
        response = requests.post(url, data=data)
        print(f"获取音频信息测试: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"获取音频信息测试失败: {e}")
        return False

def main():
    """运行所有测试"""
    print("=" * 50)
    print("API接口测试开始")
    print("=" * 50)
    
    # 测试登录
    print("\n1. 测试登录接口")
    test_login()
    
    # 测试注册
    print("\n2. 测试注册接口")
    test_register()
    
    # 测试获取音频信息
    print("\n3. 测试获取音频信息接口")
    test_get_audio_info()
    
    print("\n" + "=" * 50)
    print("API接口测试完成")
    print("=" * 50)

if __name__ == '__main__':
    main()

