"""
管理员 API
"""
from flask import Blueprint, request, jsonify
from api.auth import login_required
from models import db, User, History
from datetime import datetime
from functools import wraps

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    """管理员权限装饰器：先验证登录，再检查是否为管理员。

    使用 @wraps 保留原函数名字，避免 Flask 端点名冲突。
    """

    @wraps(f)
    @login_required
    def wrapper(*args, **kwargs):
        user = request.current_user
        if user.level != 'admin':
            return jsonify(
                {
                    "success": False,
                    "message": "需要管理员权限",
                }
            ), 403
        return f(*args, **kwargs)

    return wrapper

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    """获取用户列表"""
    try:
        level = request.args.get('level', 'all')
        
        query = User.query
        if level != 'all':
            query = query.filter_by(level=level)
        
        users = query.all()
        
        # 统计各等级用户数
        total_users = User.query.count()
        normal_count = User.query.filter_by(level='normal').count()
        vip_count = User.query.filter_by(level='vip').count()
        svip_count = User.query.filter_by(level='svip').count()
        admin_count = User.query.filter_by(level='admin').count()
        
        return jsonify({
            'success': True,
            'data': {
                'users': [u.to_dict() for u in users],
                'stats': {
                    'total': total_users,
                    'normal': normal_count,
                    'vip': vip_count,
                    'svip': svip_count,
                    'admin': admin_count
                }
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取用户列表失败: {str(e)}'
        }), 500

@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@admin_required
def get_user_detail(user_id):
    """获取用户详情"""
    try:
        user = User.query.get_or_404(user_id)
        return jsonify({
            'success': True,
            'data': user.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取用户详情失败: {str(e)}'
        }), 500

@admin_bp.route('/users/<int:user_id>/level', methods=['PUT'])
@admin_required
def update_user_level(user_id):
    """修改用户等级"""
    try:
        data = request.get_json()
        level = data.get('level')
        level_map = {
            'normal': {'name': '普通用户', 'max_digits': 50},
            'vip': {'name': 'VIP用户', 'max_digits': 80},
            'svip': {'name': 'SVIP用户', 'max_digits': 120},
            'admin': {'name': '管理员', 'max_digits': 200}
        }
        
        if level not in level_map:
            return jsonify({
                'success': False,
                'message': '无效的用户等级'
            }), 400
        
        user = User.query.get_or_404(user_id)
        user.level = level
        user.level_name = level_map[level]['name']
        user.max_digits = level_map[level]['max_digits']
        user.update_time = datetime.now()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '用户等级修改成功',
            'data': user.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'修改用户等级失败: {str(e)}'
        }), 500

