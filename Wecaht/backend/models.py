"""
数据库模型
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    level = db.Column(db.String(20), nullable=False, default='normal')  # normal, vip, svip, admin
    level_name = db.Column(db.String(50), nullable=False, default='普通用户')
    max_digits = db.Column(db.Integer, nullable=False, default=50)
    
    # 用户信息
    gender = db.Column(db.String(10))  # male, female, other
    gender_name = db.Column(db.String(10))  # 男, 女, 其他
    birth_year = db.Column(db.Integer)
    birth_month = db.Column(db.Integer)
    birth_day = db.Column(db.Integer)
    age = db.Column(db.Integer)
    job = db.Column(db.String(100))  # 职业
    
    # 头像
    avatar = db.Column(db.String(255))
    
    # 时间戳
    create_time = db.Column(db.DateTime, default=datetime.now)
    last_login_time = db.Column(db.DateTime)
    login_count = db.Column(db.Integer, default=0)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    histories = db.relationship('History', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'username': self.username,
            'level': self.level,
            'level_name': self.level_name,
            'max_digits': self.max_digits,
            'gender': self.gender,
            'gender_name': self.gender_name,
            'birth_year': self.birth_year,
            'birth_month': self.birth_month,
            'birth_day': self.birth_day,
            'age': self.age,
            'job': self.job,
            'avatar': self.avatar,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'last_login_time': self.last_login_time.isoformat() if self.last_login_time else None,
            'login_count': self.login_count,
            'update_time': self.update_time.isoformat() if self.update_time else None
        }

class History(db.Model):
    """历史记录模型"""
    __tablename__ = 'histories'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # 分解信息
    number = db.Column(db.Text, nullable=False)  # 原数（可能很大，使用 Text）
    factors = db.Column(db.Text, nullable=False)  # 因子列表（JSON 字符串）
    formula = db.Column(db.Text)  # 分解式
    number_type = db.Column(db.String(20))  # prime, composite, zero, unit, unknown
    number_type_name = db.Column(db.String(50))  # 素数, 合数, 非素非合, 未知
    factorization_level = db.Column(db.String(20))  # complete, partial, failed
    factorization_level_name = db.Column(db.String(50))  # 完全分解, 部分分解, 不能分解
    
    # 计算信息
    elapsed_time = db.Column(db.Float)  # 耗时（秒）
    digit_count = db.Column(db.Integer)  # 数字位数
    factor_count = db.Column(db.Integer)  # 分解次数（因子数量）
    calc_desc = db.Column(db.Text)  # 计算说明（介绍算）

    # 时间戳
    create_time = db.Column(db.DateTime, default=datetime.now, index=True)
    
    def to_dict(self):
        """转换为字典"""
        import json
        return {
            'id': self.id,
            'user_id': self.user_id,
            'number': self.number,
            'factors': json.loads(self.factors) if self.factors else [],
            'formula': self.formula,
            'number_type': self.number_type,
            'number_type_name': self.number_type_name,
            'factorization_level': self.factorization_level,
            'factorization_level_name': self.factorization_level_name,
            'elapsed_time': self.elapsed_time,
            'digit_count': self.digit_count,
            'factor_count': self.factor_count,
            'calc_desc': self.calc_desc,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'user': self.user.to_dict() if self.user else None
        }

