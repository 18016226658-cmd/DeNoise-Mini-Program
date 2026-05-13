#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
音频降噪系统 - 后端启动脚本
"""
import warnings
warnings.filterwarnings("ignore")
import os
import sys
import subprocess
import time

os.environ['PYTHONWARNINGS'] = 'ignore'
os.environ['PYTHONUNBUFFERED'] = '1'

# 设置matplotlib后端
try:
    import matplotlib
    matplotlib.use('Agg')
except:
    pass

def check_and_kill_port(port=5000):
    """
    检查指定端口是否被占用，如果被占用则结束占用该端口的进程
    
    Args:
        port: 要检查的端口号，默认5000
    
    Returns:
        bool: 如果端口已释放或未被占用返回True，否则返回False
    """
    try:
        print(f"[检查] 正在检查端口 {port} 是否被占用...", flush=True)
        
        # 使用 netstat 查找占用端口的进程
        # netstat -ano | findstr :5000
        result = subprocess.run(
            ['netstat', '-ano'],
            capture_output=True,
            text=True,
            encoding='gbk',  # Windows中文环境使用gbk编码
            errors='ignore'
        )
        
        if result.returncode != 0:
            print(f"[警告] 无法执行 netstat 命令", flush=True)
            return False
        
        # 查找包含指定端口的行
        lines = result.stdout.split('\n')
        pids = []
        
        for line in lines:
            if f':{port}' in line and 'LISTENING' in line:
                # 解析PID（最后一列）
                # 格式: TCP    0.0.0.0:5000   0.0.0.0:0   LISTENING   12345
                parts = line.split()
                if len(parts) >= 5:
                    try:
                        pid = int(parts[-1])
                        if pid not in pids:
                            pids.append(pid)
                    except ValueError:
                        continue
        
        if not pids:
            print(f"[成功] 端口 {port} 未被占用", flush=True)
            return True
        
        print(f"[发现] 端口 {port} 被 {len(pids)} 个进程占用: {pids}", flush=True)
        
        # 结束占用端口的进程
        killed_count = 0
        for pid in pids:
            try:
                # 检查进程是否存在
                check_result = subprocess.run(
                    ['tasklist', '/FI', f'PID eq {pid}'],
                    capture_output=True,
                    text=True,
                    encoding='gbk',
                    errors='ignore'
                )
                
                if f'{pid}' in check_result.stdout:
                    # 结束进程
                    kill_result = subprocess.run(
                        ['taskkill', '/F', '/PID', str(pid)],
                        capture_output=True,
                        text=True,
                        encoding='gbk',
                        errors='ignore'
                    )
                    
                    if kill_result.returncode == 0:
                        print(f"[成功] 已结束进程 PID: {pid}", flush=True)
                        killed_count += 1
                    else:
                        print(f"[警告] 无法结束进程 PID: {pid}: {kill_result.stderr}", flush=True)
                else:
                    print(f"[信息] 进程 PID: {pid} 已不存在", flush=True)
            except Exception as e:
                print(f"[错误] 处理进程 PID: {pid} 时出错: {e}", flush=True)
        
        if killed_count > 0:
            print(f"[等待] 等待进程完全结束...", flush=True)
            time.sleep(2)  # 等待进程完全结束
        
        # 再次检查端口是否已释放
        result = subprocess.run(
            ['netstat', '-ano'],
            capture_output=True,
            text=True,
            encoding='gbk',
            errors='ignore'
        )
        
        lines = result.stdout.split('\n')
        still_occupied = False
        for line in lines:
            if f':{port}' in line and 'LISTENING' in line:
                still_occupied = True
                break
        
        if still_occupied:
            print(f"[警告] 端口 {port} 仍被占用，请手动检查", flush=True)
            return False
        else:
            print(f"[成功] 端口 {port} 已释放", flush=True)
            return True
            
    except Exception as e:
        print(f"[错误] 检查端口时出错: {e}", flush=True)
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("正在导入应用模块...", flush=True)
    try:
        from app import create_app
        app = create_app()
    except Exception as e:
        print(f"[错误] 导入应用模块失败: {e}", flush=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    if app is None:
        print("[错误] app 对象为 None", flush=True)
        sys.exit(1)
    
    print("=" * 60, flush=True)
    print("音频降噪系统后端服务启动中...", flush=True)
    print("=" * 60, flush=True)
    
    print("检查端口状态...", flush=True)
    check_and_kill_port(5000)
    
    print("=" * 60, flush=True)
    print("服务地址: http://127.0.0.1:5000", flush=True)
    print("提示：按 Ctrl+C 停止服务", flush=True)
    print("=" * 60, flush=True)
    print("", flush=True)
    
    try:
        print("正在启动Flask服务...", flush=True)
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    except KeyboardInterrupt:
        print("\n[信息] 服务已停止", flush=True)
    except Exception as e:
        print(f"[错误] 启动服务失败: {e}", flush=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)

