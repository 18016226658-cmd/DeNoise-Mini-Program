"""
大整数分解系统 - Flask 后端主程序
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

from config import Config
from models import db, User, History
from api.auth import auth_bp
from api.factorize import factorize_bp
from api.history import history_bp
from api.analysis import analysis_bp
from api.admin import admin_bp

def create_app():
    """创建并配置 Flask 应用"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化数据库
    db.init_app(app)
    
    # 启用 CORS（跨域资源共享）
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # 注册蓝图
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(factorize_bp, url_prefix='/api/factorize')
    app.register_blueprint(history_bp, url_prefix='/api/history')
    app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
        # 初始化管理员账户
        init_admin_user()
    
    return app

def init_admin_user():
    """初始化管理员账户"""
    admin = User.query.filter_by(username='xqq').first()
    if not admin:
        admin = User(
            username='xqq',
            password='123456',  # 生产环境应该使用哈希
            level='admin',
            level_name='管理员',
            max_digits=200
        )
        db.session.add(admin)
        db.session.commit()
        print('管理员账户已创建: xqq / 123456')
    else:
        # 确保密码正确
        if admin.password != '123456':
            admin.password = '123456'
            db.session.commit()
            print('管理员账户密码已更新为 123456')

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

