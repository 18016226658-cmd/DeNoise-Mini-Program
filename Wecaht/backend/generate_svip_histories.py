"""
仅生成SVIP用户的历史记录数据
为每个SVIP用户生成1-2条历史记录，使用真实的分解算法
"""
import sys
import os
import random
import json
from datetime import datetime, timedelta

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, User, History
from algorithms import factorize, get_number_type, get_factorization_level, miller_rabin

app = create_app()

def generate_random_number(digit_count):
    """生成指定位数的随机数字字符串"""
    # 第一位不能是0
    first_digit = random.randint(1, 9)
    # 其余位可以是0-9
    other_digits = ''.join([str(random.randint(0, 9)) for _ in range(digit_count - 1)])
    return str(first_digit) + other_digits

def generate_svip_histories():
    """仅为SVIP用户生成1-2条历史记录"""
    with app.app_context():
        # 获取所有SVIP用户
        users = User.query.filter(User.level == 'svip').all()
        
        if not users:
            print('❌ 没有找到SVIP用户，请先运行 generate_real_users.py 生成用户')
            return
        
        print('=' * 60)
        print(f'开始为 {len(users)} 个SVIP用户生成历史记录')
        print('=' * 60)
        
        total_histories = 0
        histories = []
        
        for idx, user in enumerate(users, 1):
            # 每个SVIP用户生成1-2条记录
            record_count = random.randint(1, 2)
            
            print(f'\n处理用户 {idx}/{len(users)}: {user.username} ({user.level_name}) - 生成 {record_count} 条记录...')
            
            for i in range(record_count):
                try:
                    # 根据用户等级确定最大位数
                    max_digits = user.max_digits
                    
                    # 随机生成数字位数（5位到最大位数之间）
                    digit_count = random.randint(5, max_digits)
                    
                    # 生成随机数字
                    number_str = generate_random_number(digit_count)
                    number = int(number_str)
                    
                    # 特殊处理：0和1
                    if number == 0:
                        factors = [0]
                        formula = '0'
                        number_type = {'type': 'zero', 'type_name': '非素非合', 'description': '0既不是素数也不是合数'}
                        factorization_level = {'level': 'complete', 'level_name': '完全分解', 'description': '0的分解已完成'}
                        elapsed_time = 0.001
                    elif number == 1:
                        factors = [1]
                        formula = '1'
                        number_type = {'type': 'unit', 'type_name': '非素非合', 'description': '1既不是素数也不是合数'}
                        factorization_level = {'level': 'complete', 'level_name': '完全分解', 'description': '1的分解已完成'}
                        elapsed_time = 0.001
                    else:
                        # 使用真实算法进行分解
                        start_time = datetime.now()
                        factors = factorize(number, mode='standard')
                        elapsed_time = (datetime.now() - start_time).total_seconds()
                        
                        # 判断数字类型
                        number_type = get_number_type(number, factors)
                        
                        # 判断分解程度
                        factorization_level = get_factorization_level(number, factors)
                        
                        # 生成分解式
                        factor_counts = {}
                        for f in factors:
                            key = str(f)
                            factor_counts[key] = factor_counts.get(key, 0) + 1
                        
                        formula_parts = []
                        for factor, count in factor_counts.items():
                            if count > 1:
                                formula_parts.append(f'{factor}^{count}')
                            else:
                                formula_parts.append(str(factor))
                        formula = ' × '.join(formula_parts)
                    
                    # 计算分解次数（因子数量）
                    factor_count = len(factors)
                    # 计算说明（介绍算）：结合数字类型和分解程度描述
                    calc_desc = f"{number_type['description']}；{factorization_level['description']}"

                    # 随机生成时间（过去90天内）
                    days_ago = random.randint(0, 90)
                    hours_ago = random.randint(0, 23)
                    minutes_ago = random.randint(0, 59)
                    seconds_ago = random.randint(0, 59)
                    
                    create_time = datetime.now() - timedelta(
                        days=days_ago,
                        hours=hours_ago,
                        minutes=minutes_ago,
                        seconds=seconds_ago
                    )
                    
                    # 创建历史记录对象
                    history = History(
                        user_id=user.id,
                        number=number_str,
                        factors=json.dumps([str(f) for f in factors]),
                        formula=formula,
                        number_type=number_type['type'],
                        number_type_name=number_type['type_name'],
                        factorization_level=factorization_level['level'],
                        factorization_level_name=factorization_level['level_name'],
                        elapsed_time=round(elapsed_time, 3),
                        digit_count=digit_count,
                        factor_count=factor_count,
                        calc_desc=calc_desc,
                        create_time=create_time
                    )
                    
                    histories.append(history)
                    total_histories += 1
                    
                    # 每100条记录批量提交一次，避免内存占用过大
                    if len(histories) >= 100:
                        db.session.add_all(histories)
                        db.session.commit()
                        print(f'  已生成 {total_histories} 条记录...')
                        histories = []
                
                except Exception as e:
                    print(f'  ⚠️ 生成记录失败: {e}')
                    continue
        
        # 提交剩余记录
        if histories:
            db.session.add_all(histories)
            db.session.commit()
        
        print(f'\n✅ 成功生成 {total_histories} 条SVIP用户历史记录！')
        
        # 显示统计信息
        print('\nSVIP用户历史记录统计：')
        svip_user_ids = [u.id for u in users]
        total = History.query.filter(History.user_id.in_(svip_user_ids)).count()
        complete = History.query.filter(
            History.user_id.in_(svip_user_ids),
            History.factorization_level == 'complete'
        ).count()
        partial = History.query.filter(
            History.user_id.in_(svip_user_ids),
            History.factorization_level == 'partial'
        ).count()
        failed = History.query.filter(
            History.user_id.in_(svip_user_ids),
            History.factorization_level == 'failed'
        ).count()
        
        print(f'  总记录数: {total}')
        print(f'  完全分解: {complete} ({complete*100/total:.1f}%)' if total > 0 else '  完全分解: 0')
        print(f'  部分分解: {partial} ({partial*100/total:.1f}%)' if total > 0 else '  部分分解: 0')
        print(f'  失败: {failed} ({failed*100/total:.1f}%)' if total > 0 else '  失败: 0')

if __name__ == '__main__':
    try:
        generate_svip_histories()
    except Exception as e:
        print(f'❌ 生成SVIP用户历史记录失败: {e}')
        import traceback
        traceback.print_exc()

