# test/test_audio.py
# 音频处理测试脚本

import os
import sys

# 添加backend目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

def test_denoise_algorithm():
    """测试降噪算法"""
    try:
        from deNoise import DeNoise_all
        
        # 测试音频文件路径（需要实际存在的文件）
        input_file = '../backend/Audio/input/test.wav'
        output_file = '../backend/Audio/output/test_denoised.wav'
        
        if os.path.exists(input_file):
            print(f"开始测试降噪算法...")
            print(f"输入文件: {input_file}")
            print(f"输出文件: {output_file}")
            
            # 执行降噪
            DeNoise_all(input_file, output_file)
            
            if os.path.exists(output_file):
                print("✓ 降噪测试成功")
                return True
            else:
                print("✗ 降噪测试失败：输出文件未生成")
                return False
        else:
            print(f"✗ 测试文件不存在: {input_file}")
            print("请确保测试音频文件存在")
            return False
            
    except ImportError as e:
        print(f"✗ 导入模块失败: {e}")
        return False
    except Exception as e:
        print(f"✗ 降噪测试失败: {e}")
        return False

def test_butterworth_filter():
    """测试巴特沃斯滤波器"""
    try:
        from scipy.signal import butter, filtfilt
        import numpy as np
        
        # 生成测试信号
        fs = 44100  # 采样率
        t = np.linspace(0, 1, fs)
        signal = np.sin(2 * np.pi * 440 * t)  # 440Hz正弦波
        
        # 设计滤波器
        nyquist = 0.5 * fs
        low = 300 / nyquist
        high = 3000 / nyquist
        b, a = butter(5, [low, high], btype='band')
        
        # 应用滤波器
        filtered = filtfilt(b, a, signal)
        
        print("✓ 巴特沃斯滤波器测试成功")
        print(f"  原始信号长度: {len(signal)}")
        print(f"  滤波后信号长度: {len(filtered)}")
        return True
        
    except Exception as e:
        print(f"✗ 滤波器测试失败: {e}")
        return False

def main():
    """运行所有测试"""
    print("=" * 50)
    print("音频处理测试开始")
    print("=" * 50)
    
    # 测试滤波器
    print("\n1. 测试巴特沃斯滤波器")
    test_butterworth_filter()
    
    # 测试降噪算法
    print("\n2. 测试降噪算法")
    test_denoise_algorithm()
    
    print("\n" + "=" * 50)
    print("音频处理测试完成")
    print("=" * 50)

if __name__ == '__main__':
    main()

