"""
一键生成所有可视化图表
"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    print('=' * 60)
    print('开始生成所有可视化图表')
    print('=' * 60)
    print()
    
    scripts = [
        ('01_分解时间偏好分析.py', '分解时间偏好分析'),
        ('02_职业词云图.py', '职业词云图'),
        ('03_用户等级分布分析.py', '用户等级分布分析'),
        ('04_数字位数分布分析.py', '数字位数分布分析'),
        ('05_时间趋势与分解次数分析.py', '时间趋势与分解次数分析'),
    ]
    
    for script_name, description in scripts:
        print(f'正在生成: {description}...')
        print('-' * 60)
        try:
            script_path = os.path.join(os.path.dirname(__file__), script_name)
            with open(script_path, 'r', encoding='utf-8') as f:
                code = f.read()
            exec(compile(code, script_path, 'exec'))
            print()
        except Exception as e:
            print(f'❌ 生成失败: {e}')
            print()
    
    print('=' * 60)
    print('✅ 所有交互式图表生成完成！')
    print('=' * 60)
    print()
    print('生成的交互式HTML图表保存在: backend/pc/ 目录下')
    print('提示: 在浏览器中打开HTML文件即可查看交互式图表')
    print('     支持缩放、悬停查看详情、下载图片等功能')

if __name__ == '__main__':
    main()

