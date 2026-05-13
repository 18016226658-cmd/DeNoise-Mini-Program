"""
生成真实用户数据
生成500个用户，包含不同等级、性别、职业、年龄段
"""
import sys
import os
import random
from datetime import datetime, timedelta

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, User

app = create_app()

# 职业列表
JOBS = ['学生', '教师', '工程师', '医生', '程序员', '设计师', '销售', '经理', '研究员', '其他']

# 性别列表
GENDERS = [
    {'value': 'male', 'name': '男'},
    {'value': 'female', 'name': '女'},
    {'value': 'other', 'name': '其他'}
]

# 用户等级配置
LEVEL_CONFIG = {
    'normal': {'name': '普通用户', 'max_digits': 50, 'count': 300},  # 300个普通用户
    'vip': {'name': 'VIP用户', 'max_digits': 80, 'count': 150},      # 150个VIP用户
    'svip': {'name': 'SVIP用户', 'max_digits': 120, 'count': 49},    # 49个SVIP用户
    'admin': {'name': '管理员', 'max_digits': 200, 'count': 1}       # 1个管理员（xqq）
}

def generate_users():
    """生成500个真实用户"""
    with app.app_context():
        # 检查是否已有用户（除了管理员）
        existing_count = User.query.filter(User.username != 'xqq').count()
        if existing_count >= 500:
            print(f'已有 {existing_count} 个用户，跳过生成')
            return
        
        print('=' * 60)
        print('开始生成500个真实用户数据')
        print('=' * 60)
        
        users = []
        user_id = 1
        
        # 生成各等级用户
        for level, config in LEVEL_CONFIG.items():
            if level == 'admin':
                continue  # 跳过管理员，已存在
            
            print(f'\n生成 {config["name"]} ({config["count"]}个)...')
            
            for i in range(config['count']):
                # 生成用户名
                username = f'user_{level}_{i+1:03d}'
                
                # 检查用户名是否已存在
                if User.query.filter_by(username=username).first():
                    continue
                
                # 随机选择性别
                gender_info = random.choice(GENDERS)
                
                # 随机生成出生日期（1980-2005年）
                birth_year = random.randint(1980, 2005)
                birth_month = random.randint(1, 12)
                birth_day = random.randint(1, 28)
                
                # 计算年龄
                current_date = datetime.now()
                age = current_date.year - birth_year
                if current_date.month < birth_month or \
                   (current_date.month == birth_month and current_date.day < birth_day):
                    age -= 1
                
                # 随机选择职业
                job = random.choice(JOBS)
                
                # 随机生成注册时间（过去1年内）
                days_ago = random.randint(1, 365)
                create_time = datetime.now() - timedelta(days=days_ago)
                
                # 随机生成最后登录时间（过去30天内）
                login_days_ago = random.randint(0, 30)
                last_login_time = datetime.now() - timedelta(days=login_days_ago) if login_days_ago > 0 else None
                
                # 随机生成登录次数（1-100次）
                login_count = random.randint(1, 100)
                
                # 创建用户对象
                user = User(
                    username=username,
                    password='123456',  # 所有测试用户密码统一为123456
                    level=level,
                    level_name=config['name'],
                    max_digits=config['max_digits'],
                    gender=gender_info['value'],
                    gender_name=gender_info['name'],
                    birth_year=birth_year,
                    birth_month=birth_month,
                    birth_day=birth_day,
                    age=age,
                    job=job,
                    create_time=create_time,
                    last_login_time=last_login_time,
                    login_count=login_count
                )
                
                users.append(user)
                user_id += 1
                
                # 每生成50个用户显示一次进度
                if len(users) % 50 == 0:
                    print(f'  已生成 {len(users)} 个用户...')
        
        # 批量插入用户
        print(f'\n正在插入 {len(users)} 个用户到数据库...')
        db.session.add_all(users)
        db.session.commit()
        
        print(f'\n✅ 成功生成 {len(users)} 个用户！')
        
        # 显示统计信息
        print('\n用户统计：')
        for level, config in LEVEL_CONFIG.items():
            if level == 'admin':
                continue
            count = User.query.filter_by(level=level).count()
            print(f'  {config["name"]}: {count} 个')
        
        print('\n职业分布：')
        for job in JOBS:
            count = User.query.filter_by(job=job).count()
            if count > 0:
                print(f'  {job}: {count} 个')
        
        print('\n性别分布：')
        for gender_info in GENDERS:
            count = User.query.filter_by(gender=gender_info['value']).count()
            if count > 0:
                print(f'  {gender_info["name"]}: {count} 个')

if __name__ == '__main__':
    try:
        generate_users()
    except Exception as e:
        print(f'❌ 生成用户失败: {e}')
        import traceback
        traceback.print_exc()

