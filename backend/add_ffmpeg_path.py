#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
将 FFmpeg 添加到系统 PATH 环境变量
"""

import os
import sys
import subprocess
import io

# 设置输出编码为 UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def add_ffmpeg_to_path():
    """添加 FFmpeg 路径到用户 PATH 环境变量"""
    ffmpeg_bin_path = r"C:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin"
    
    print("=" * 60)
    print("FFmpeg PATH 配置脚本")
    print("=" * 60)
    print()
    
    # 检查路径是否存在
    print("[1] 检查 FFmpeg 路径...")
    if not os.path.exists(ffmpeg_bin_path):
        print(f"[ERROR] 路径不存在: {ffmpeg_bin_path}")
        print()
        print("请确认 FFmpeg 已正确解压到该路径。")
        return False
    
    ffmpeg_exe = os.path.join(ffmpeg_bin_path, "ffmpeg.exe")
    if not os.path.exists(ffmpeg_exe):
        print(f"[ERROR] 找不到 ffmpeg.exe: {ffmpeg_exe}")
        return False
    
    print(f"[OK] FFmpeg 路径存在: {ffmpeg_bin_path}")
    print()
    
    # 检查是否已存在
    print("[2] 检查 PATH 环境变量...")
    current_user_path = os.environ.get('Path', '')
    
    # 获取用户环境变量（通过注册表或系统调用）
    try:
        # 使用 PowerShell 获取用户 PATH
        ps_cmd = "[Environment]::GetEnvironmentVariable('Path', 'User')"
        result = subprocess.run(
            ['powershell', '-Command', ps_cmd],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            current_user_path = result.stdout.strip()
    except Exception as e:
        print(f"⚠ 无法读取用户 PATH，使用当前会话 PATH: {e}")
    
    path_exists = False
    if ffmpeg_bin_path in current_user_path:
        print("[OK] 已在用户 PATH 中找到 FFmpeg 路径")
        path_exists = True
    
    if path_exists:
        print()
        print("FFmpeg 路径已在 PATH 中，无需重复添加。")
        print()
        print("如果仍然无法识别 ffmpeg 命令，请：")
        print("1. 关闭所有终端窗口")
        print("2. 重新打开新的终端窗口")
        print("3. 运行: ffmpeg -version")
        return True
    
    # 添加到用户 PATH
    print("[3] 添加到用户 PATH...")
    try:
        if current_user_path:
            new_user_path = current_user_path + ";" + ffmpeg_bin_path
        else:
            new_user_path = ffmpeg_bin_path
        
        # 使用 PowerShell 设置用户环境变量
        ps_cmd = f"[Environment]::SetEnvironmentVariable('Path', '{new_user_path}', 'User')"
        result = subprocess.run(
            ['powershell', '-Command', ps_cmd],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print("[OK] 已添加到用户 PATH")
            print(f"  路径: {ffmpeg_bin_path}")
        else:
            print(f"[ERROR] 添加到用户 PATH 失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"[ERROR] 添加到用户 PATH 失败: {e}")
        print()
        print("请尝试以管理员身份运行此脚本，或手动添加 PATH。")
        return False
    
    # 验证
    print()
    print("[4] 验证配置...")
    try:
        ps_cmd = "[Environment]::GetEnvironmentVariable('Path', 'User')"
        result = subprocess.run(
            ['powershell', '-Command', ps_cmd],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            updated_path = result.stdout.strip()
            if ffmpeg_bin_path in updated_path:
                print("[OK] PATH 配置成功")
            else:
                print("[ERROR] PATH 配置失败")
                return False
    except Exception as e:
        print(f"⚠ 验证配置时出错: {e}")
    
    # 测试 FFmpeg 命令
    print()
    print("[5] 测试 FFmpeg 命令...")
    try:
        result = subprocess.run(
            [ffmpeg_exe, '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("[OK] FFmpeg 可以正常运行")
            print()
            print("版本信息:")
            for line in result.stdout.split('\n')[:3]:
                print(f"  {line}")
        else:
            print("⚠ 无法直接运行 FFmpeg（可能需要重启终端）")
    except Exception as e:
        print(f"⚠ 无法直接运行 FFmpeg（可能需要重启终端）: {e}")
    
    print()
    print("=" * 60)
    print("[OK] FFmpeg PATH 配置完成！")
    print("=" * 60)
    print()
    print("重要提示：")
    print("1. 请关闭所有终端窗口")
    print("2. 重新打开新的终端窗口")
    print("3. 运行 'ffmpeg -version' 验证")
    print()
    print(f"配置的路径: {ffmpeg_bin_path}")
    
    return True

if __name__ == '__main__':
    success = add_ffmpeg_to_path()
    sys.exit(0 if success else 1)
