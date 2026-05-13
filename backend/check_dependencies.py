#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
依赖检查脚本
功能：检查所有必需的Python依赖是否已安装
"""

import sys

# 必需的核心依赖
REQUIRED_PACKAGES = {
    'flask': 'Flask框架',
    'flask_cors': 'Flask-CORS（跨域支持）',
    'pymysql': 'MySQL数据库连接',
    'pandas': '数据处理',
    'scipy': '科学计算（音频降噪需要）',
    'pydub': '音频处理',
    'numpy': '数值计算',
    'mutagen': '音频元数据读取',
    'jieba': '中文分词',
    'snownlp': '中文情感分析',
    'matplotlib': '图表绘制',
    'requests': 'HTTP请求',
    'openai': 'OpenAI API（AI聊天）'
}

# 可选的依赖
OPTIONAL_PACKAGES = {
    'qianfan': '百度文心一言（可选）',
    'jpype': 'Java调用功能（可选）',
    'tkinter': 'GUI工具包（可选，服务器环境通常不可用）'
}

def check_package(package_name, display_name):
    """检查单个包是否已安装"""
    try:
        __import__(package_name)
        print(f"[成功] {display_name} ({package_name})")
        return True
    except ImportError:
        print(f"[缺失] {display_name} ({package_name})")
        return False

def main():
    """主检查函数"""
    print("=" * 60)
    print("检查Python依赖包...")
    print("=" * 60)
    print()
    
    # 检查Python版本
    print(f"Python版本: {sys.version}")
    print(f"Python路径: {sys.executable}")
    print()
    
    # 检查必需依赖
    print("=" * 60)
    print("必需依赖检查：")
    print("=" * 60)
    missing_required = []
    for package, display_name in REQUIRED_PACKAGES.items():
        if not check_package(package, display_name):
            missing_required.append(package)
    
    print()
    
    # 检查可选依赖
    print("=" * 60)
    print("可选依赖检查：")
    print("=" * 60)
    missing_optional = []
    for package, display_name in OPTIONAL_PACKAGES.items():
        if not check_package(package, display_name):
            missing_optional.append(package)
    
    print()
    print("=" * 60)
    print("检查结果：")
    print("=" * 60)
    
    if missing_required:
        print(f"[错误] 缺失 {len(missing_required)} 个必需依赖：")
        for pkg in missing_required:
            print(f"  - {pkg}")
        print()
        print("请运行以下命令安装缺失的依赖：")
        print(f"  pip install {' '.join(missing_required)}")
        print()
        print("或安装所有依赖：")
        print("  pip install -r requirements.txt")
        return False
    else:
        print("[成功] 所有必需依赖已安装！")
    
    if missing_optional:
        print(f"[提示] 缺失 {len(missing_optional)} 个可选依赖（不影响核心功能）")
        for pkg in missing_optional:
            print(f"  - {pkg}")
    
    print()
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)













