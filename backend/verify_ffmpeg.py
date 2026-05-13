#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FFmpeg 验证脚本
用于验证 FFmpeg 是否正确安装和配置
"""

import os
import subprocess
import sys

def check_ffmpeg():
    """检查 FFmpeg 是否可用"""
    print("=" * 60)
    print("FFmpeg 验证脚本")
    print("=" * 60)
    print()
    
    # 方法1：检查系统 PATH
    print("[1] 检查系统 PATH 中的 FFmpeg...")
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                               capture_output=True, 
                               text=True, 
                               timeout=5)
        if result.returncode == 0:
            print("✓ FFmpeg 在系统 PATH 中可用")
            print(f"  版本信息（前3行）:")
            for line in result.stdout.split('\n')[:3]:
                print(f"    {line}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        print("✗ FFmpeg 不在系统 PATH 中")
    
    print()
    
    # 方法2：检查常见路径
    print("[2] 检查常见安装路径...")
    common_paths = [
        r"C:\ffmpeg\bin\ffmpeg.exe",
        r"C:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe",
        r"C:\ffmpeg\ffmpeg-7.0-essentials_build\bin\ffmpeg.exe",
        r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
        r"D:\ffmpeg\bin\ffmpeg.exe",
    ]
    
    # 也检查 C:\ffmpeg 下的所有子目录
    if os.path.exists(r"C:\ffmpeg"):
        try:
            for item in os.listdir(r"C:\ffmpeg"):
                potential_path = os.path.join(r"C:\ffmpeg", item, "bin", "ffmpeg.exe")
                if os.path.exists(potential_path):
                    common_paths.insert(0, potential_path)
        except:
            pass
    
    found_path = None
    for path in common_paths:
        if os.path.exists(path):
            print(f"✓ 找到 FFmpeg: {path}")
            found_path = path
            # 验证是否可以运行
            try:
                result = subprocess.run([path, '-version'], 
                                       capture_output=True, 
                                       text=True, 
                                       timeout=5)
                if result.returncode == 0:
                    print(f"✓ FFmpeg 可以正常运行")
                    print(f"  版本信息（前3行）:")
                    for line in result.stdout.split('\n')[:3]:
                        print(f"    {line}")
                    print()
                    print("=" * 60)
                    print("✓ FFmpeg 验证成功！")
                    print("=" * 60)
                    print()
                    print(f"建议：在 backend/config.py 中设置：")
                    print(f"  FFMPEG_PATH = r\"{path}\"")
                    return True
            except Exception as e:
                print(f"✗ 无法运行 FFmpeg: {e}")
    
    if not found_path:
        print("✗ 未找到 FFmpeg")
    
    print()
    print("=" * 60)
    print("✗ FFmpeg 验证失败")
    print("=" * 60)
    print()
    print("解决方案：")
    print("1. 确保已将 FFmpeg 的 bin 目录添加到系统 PATH")
    print("2. 或在 backend/config.py 中设置 FFMPEG_PATH")
    print("3. 关闭并重新打开终端，然后重新运行此脚本")
    
    return False

if __name__ == '__main__':
    success = check_ffmpeg()
    sys.exit(0 if success else 1)
