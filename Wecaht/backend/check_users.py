"""
检查数据库中的用户数据
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, User, History

app = create_app()

with app.app_context():
    # 检查所有用户
    all_users = User.query.all()
    print(f'总用户数: {len(all_users)}')
    
    # 检查非管理员用户
    non_admin_users = User.query.filter(User.level != 'admin').all()
    print(f'非管理员用户数: {len(non_admin_users)}')
    
    # 按等级统计
    print('\n按等级统计:')
    for level in ['normal', 'vip', 'svip', 'admin']:
        count = User.query.filter_by(level=level).count()
        print(f'  {level}: {count} 个用户')
    
    # 检查历史记录
    history_count = History.query.count()
    print(f'\n历史记录总数: {history_count}')
    
    # 检查是否有用户有历史记录
    users_with_history = db.session.query(User).join(History).distinct().count()
    print(f'有历史记录的用户数: {users_with_history}')


