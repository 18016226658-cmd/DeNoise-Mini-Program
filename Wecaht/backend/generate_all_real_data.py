"""
一键生成所有真实测试数据
1. 生成500个用户
2. 为每个用户生成10-20条历史记录
"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print('=' * 60)
    print('大整数分解系统 - 真实数据生成工具')
    print('=' * 60)
    print()
    
    # 步骤1：生成用户
    print('【步骤 1/2】生成500个用户...')
    print('-' * 60)
    try:
        from generate_real_users import generate_users
        generate_users()
    except Exception as e:
        print(f'❌ 生成用户失败: {e}')
        return
    
    print()
    print('=' * 60)
    print()
    
    # 步骤2：生成历史记录
    print('【步骤 2/2】为每个用户生成10-20条历史记录...')
    print('-' * 60)
    print('注意：此过程可能需要较长时间，因为需要使用真实算法进行分解计算')
    print()
    
    try:
        from generate_real_histories import generate_histories
        generate_histories()
    except Exception as e:
        print(f'❌ 生成历史记录失败: {e}')
        import traceback
        traceback.print_exc()
        return
    
    print()
    print('=' * 60)
    print('✅ 所有数据生成完成！')
    print('=' * 60)
    print()
    print('现在可以：')
    print('1. 启动后端服务: python app.py')
    print('2. 打开小程序，使用管理员账户登录查看数据')
    print('3. 数据库名: xqq')
    print('4. 管理员账户: xqq / 123456')

if __name__ == '__main__':
    main()

