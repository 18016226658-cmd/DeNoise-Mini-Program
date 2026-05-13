"""
数据库初始化脚本
"""
from app import create_app, db
from models import User

def init_database():
    """初始化数据库"""
    app = create_app()
    
    with app.app_context():
        # 创建所有表
        db.create_all()
        print('数据库表已创建')
        
        # 初始化管理员账户
        admin = User.query.filter_by(username='xqq').first()
        if not admin:
            admin = User(
                username='xqq',
                password='123456',
                level='admin',
                level_name='管理员',
                max_digits=200
            )
            db.session.add(admin)
            db.session.commit()
            print('管理员账户已创建: xqq / 123456')
        else:
            print('管理员账户已存在')
        
        print('数据库初始化完成！')

if __name__ == '__main__':
    init_database()

