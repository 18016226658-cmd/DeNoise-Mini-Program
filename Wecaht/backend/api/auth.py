"""
认证相关 API
"""
from flask import Blueprint, request, jsonify
from models import db, User
from datetime import datetime
from functools import wraps

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    """登录验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'success': False, 'message': '未登录'}), 401
        
        # 简单的 token 验证（生产环境应该使用 JWT）
        # 这里使用 username 作为 token
        user = User.query.filter_by(username=token).first()
        if not user:
            return jsonify({'success': False, 'message': '无效的 token'}), 401
        
        request.current_user = user
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': '请输入用户名和密码'
            }), 400
        
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({
                'success': False,
                'message': '用户不存在'
            }), 404
        
        if user.password != password:
            return jsonify({
                'success': False,
                'message': '密码错误'
            }), 401
        
        # 更新登录信息
        user.last_login_time = datetime.now()
        user.login_count = (user.login_count or 0) + 1
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '登录成功',
            'data': {
                'user': user.to_dict(),
                'token': username  # 简单的 token（生产环境应该使用 JWT）
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'登录失败: {str(e)}'
        }), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        password_confirm = data.get('password_confirm', '').strip()
        gender = data.get('gender', '')
        gender_name = data.get('gender_name', '')
        birth_year = data.get('birth_year')
        birth_month = data.get('birth_month')
        birth_day = data.get('birth_day')
        job = data.get('job', '').strip()
        
        # 验证用户名
        if not username or len(username) < 3 or len(username) > 20:
            return jsonify({
                'success': False,
                'message': '用户名长度为3-20个字符'
            }), 400
        
        # 验证密码
        if not password or len(password) < 6:
            return jsonify({
                'success': False,
                'message': '密码至少6位'
            }), 400
        
        if password != password_confirm:
            return jsonify({
                'success': False,
                'message': '两次密码不一致'
            }), 400
        
        # 验证性别
        if not gender:
            return jsonify({
                'success': False,
                'message': '请选择性别'
            }), 400
        
        # 验证出生日期
        if not birth_year or not birth_month or not birth_day:
            return jsonify({
                'success': False,
                'message': '请选择出生日期'
            }), 400
        
        # 验证工作
        if not job:
            return jsonify({
                'success': False,
                'message': '请输入工作'
            }), 400
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            return jsonify({
                'success': False,
                'message': '用户名已存在'
            }), 400
        
        # 计算年龄
        current_date = datetime.now()
        age = current_date.year - birth_year
        if current_date.month < birth_month or \
           (current_date.month == birth_month and current_date.day < birth_day):
            age -= 1
        
        # 创建新用户（默认普通用户）
        user = User(
            username=username,
            password=password,
            level='normal',
            level_name='普通用户',
            max_digits=50,
            gender=gender,
            gender_name=gender_name,
            birth_year=birth_year,
            birth_month=birth_month,
            birth_day=birth_day,
            age=age,
            job=job,
            last_login_time=datetime.now(),
            login_count=1
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '注册成功',
            'data': {
                'user': user.to_dict(),
                'token': username
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'注册失败: {str(e)}'
        }), 500

@auth_bp.route('/user', methods=['GET'])
@login_required
def get_user():
    """获取当前用户信息"""
    try:
        user = request.current_user
        return jsonify({
            'success': True,
            'data': user.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取用户信息失败: {str(e)}'
        }), 500

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """用户登出"""
    return jsonify({
        'success': True,
        'message': '登出成功'
    })

