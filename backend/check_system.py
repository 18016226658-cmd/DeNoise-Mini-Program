#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
系统检查脚本
功能：检查前后端配置，确保核心功能（降噪和分离）能正常工作
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_backend():
    """检查后端配置"""
    print("=" * 60)
    print("后端检查")
    print("=" * 60)
    
    issues = []
    
    # 1. 检查必要的模块
    print("\n[1] 检查Python模块...")
    try:
        import flask
        print("  [OK] Flask已安装")
    except ImportError:
        issues.append("Flask未安装")
        print("  [ERROR] Flask未安装")
    
    try:
        import pymysql
        print("  ✅ PyMySQL已安装")
    except ImportError:
        issues.append("PyMySQL未安装")
        print("  ❌ PyMySQL未安装")
    
    try:
        from pydub import AudioSegment
        print("  ✅ pydub已安装")
    except ImportError:
        issues.append("pydub未安装")
        print("  ❌ pydub未安装")
    
    try:
        from mutagen import File as MutagenFile
        print("  ✅ mutagen已安装")
    except ImportError:
        issues.append("mutagen未安装")
        print("  ❌ mutagen未安装")
    
    # 2. 检查数据库配置
    print("\n[2] 检查数据库配置...")
    try:
        from db_config import DB_CONFIG
        print(f"  ✅ 数据库配置已加载")
        print(f"     - 主机: {DB_CONFIG.get('host', 'N/A')}")
        print(f"     - 数据库: {DB_CONFIG.get('database', 'N/A')}")
    except Exception as e:
        issues.append(f"数据库配置错误: {e}")
        print(f"  ❌ 数据库配置错误: {e}")
    
    # 3. 检查音频目录
    print("\n[3] 检查音频目录...")
    try:
        from config import AUDIO_INPUT_DIR, AUDIO_OUTPUT_DIR, AUDIO_UPLOAD_DIR, AUDIO_DOWNLOAD_DIR
        
        dirs = {
            "输入目录": AUDIO_INPUT_DIR,
            "输出目录": AUDIO_OUTPUT_DIR,
            "上传目录": AUDIO_UPLOAD_DIR,
            "下载目录": AUDIO_DOWNLOAD_DIR
        }
        
        for name, path in dirs.items():
            if os.path.exists(path):
                print(f"  ✅ {name}: {path}")
            else:
                print(f"  ⚠️  {name}不存在，将自动创建: {path}")
                os.makedirs(path, exist_ok=True)
                print(f"     ✅ 已创建")
    except Exception as e:
        issues.append(f"音频目录配置错误: {e}")
        print(f"  ❌ 音频目录配置错误: {e}")
    
    # 4. 检查API路由
    print("\n[4] 检查API路由模块...")
    try:
        from api.audio import audio_bp
        print("  ✅ 音频路由模块 (api.audio) 已导入")
        
        # 检查关键路由
        routes = []
        for rule in audio_bp.url_map.iter_rules():
            routes.append(str(rule))
        
        key_routes = ['/api/DeNoiseAudio', '/api/separateAudio', '/api/uploadAudio', '/api/getAudioInfo']
        for route in key_routes:
            if any(route in r for r in routes):
                print(f"  ✅ 路由已注册: {route}")
            else:
                print(f"  ⚠️  路由未找到: {route}")
    except Exception as e:
        issues.append(f"音频路由模块导入失败: {e}")
        print(f"  ❌ 音频路由模块导入失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 5. 检查降噪模块
    print("\n[5] 检查降噪模块...")
    try:
        from deNoise import DeNoise_all
        print("  ✅ 降噪模块 (deNoise) 已导入")
    except Exception as e:
        issues.append(f"降噪模块导入失败: {e}")
        print(f"  ❌ 降噪模块导入失败: {e}")
    
    # 6. 检查Flask应用创建
    print("\n[6] 检查Flask应用...")
    try:
        from app import create_app
        app = create_app()
        print("  ✅ Flask应用创建成功")
        
        # 检查注册的蓝图
        blueprints = [bp.name for bp in app.blueprints.values()]
        print(f"  ✅ 已注册蓝图: {', '.join(blueprints)}")
        
        if 'audio' not in blueprints:
            issues.append("音频蓝图未注册")
            print("  ❌ 音频蓝图未注册")
        else:
            print("  ✅ 音频蓝图已注册")
            
    except Exception as e:
        issues.append(f"Flask应用创建失败: {e}")
        print(f"  ❌ Flask应用创建失败: {e}")
        import traceback
        traceback.print_exc()
    
    return issues

def check_frontend():
    """检查前端配置"""
    print("\n" + "=" * 60)
    print("前端检查")
    print("=" * 60)
    
    issues = []
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'wxminpro')
    
    # 1. 检查app.json
    print("\n[1] 检查app.json...")
    app_json_path = os.path.join(frontend_path, 'app.json')
    if os.path.exists(app_json_path):
        print("  ✅ app.json存在")
        try:
            import json
            with open(app_json_path, 'r', encoding='utf-8') as f:
                app_config = json.load(f)
            
            # 检查关键页面
            pages = app_config.get('pages', [])
            required_pages = ['pages/DeNoise/DeNoise', 'pages/home/home']
            for page in required_pages:
                if page in pages:
                    print(f"  ✅ 页面已配置: {page}")
                else:
                    issues.append(f"页面未配置: {page}")
                    print(f"  ❌ 页面未配置: {page}")
            
            # 检查tabBar
            tabbar = app_config.get('tabBar', {})
            if tabbar:
                print("  ✅ tabBar已配置")
            else:
                print("  ⚠️  tabBar未配置")
        except Exception as e:
            issues.append(f"app.json解析失败: {e}")
            print(f"  ❌ app.json解析失败: {e}")
    else:
        issues.append("app.json不存在")
        print("  ❌ app.json不存在")
    
    # 2. 检查API配置
    print("\n[2] 检查API配置...")
    api_config_path = os.path.join(frontend_path, 'config', 'api.js')
    if os.path.exists(api_config_path):
        print("  ✅ api.js存在")
        with open(api_config_path, 'r', encoding='utf-8') as f:
            content = f.read()
            key_endpoints = ['deNoiseAudio', 'separateAudio', 'uploadAudio', 'getAudioInfo']
            for endpoint in key_endpoints:
                if endpoint in content:
                    print(f"  ✅ API端点已配置: {endpoint}")
                else:
                    issues.append(f"API端点未配置: {endpoint}")
                    print(f"  ❌ API端点未配置: {endpoint}")
    else:
        issues.append("api.js不存在")
        print("  ❌ api.js不存在")
    
    # 3. 检查关键页面文件
    print("\n[3] 检查关键页面文件...")
    key_pages = {
        'pages/DeNoise/DeNoise.js': '降噪页面',
        'subpackages/audio/pages/AudioSep/AudioSep.js': '分离页面'
    }
    
    for page_path, name in key_pages.items():
        full_path = os.path.join(frontend_path, page_path)
        if os.path.exists(full_path):
            print(f"  ✅ {name}存在: {page_path}")
        else:
            issues.append(f"{name}不存在: {page_path}")
            print(f"  ❌ {name}不存在: {page_path}")
    
    return issues

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("系统检查 - 音频降噪系统")
    print("=" * 60)
    
    backend_issues = check_backend()
    frontend_issues = check_frontend()
    
    # 总结
    print("\n" + "=" * 60)
    print("检查总结")
    print("=" * 60)
    
    all_issues = backend_issues + frontend_issues
    
    if not all_issues:
        print("\n✅ 所有检查通过！系统配置正常。")
        print("\n下一步：")
        print("  1. 启动后端服务: cd backend && python app.py")
        print("  2. 在微信开发者工具中打开wxminpro项目")
        print("  3. 测试降噪和分离功能")
        return 0
    else:
        print(f"\n⚠️  发现 {len(all_issues)} 个问题：")
        for i, issue in enumerate(all_issues, 1):
            print(f"  {i}. {issue}")
        print("\n请修复这些问题后重新检查。")
        return 1

if __name__ == '__main__':
    sys.exit(main())

