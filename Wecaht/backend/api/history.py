"""
历史记录 API
"""
from flask import Blueprint, request, jsonify
from api.auth import login_required
from models import db, History
from sqlalchemy import desc

history_bp = Blueprint('history', __name__)

@history_bp.route('/list', methods=['GET'])
@login_required
def get_history_list():
    """获取历史记录列表"""
    try:
        user = request.current_user
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # 管理员可以查看所有记录，普通用户只能查看自己的
        if user.level == 'admin':
            query = History.query
        else:
            query = History.query.filter_by(user_id=user.id)
        
        # 按时间倒序排列
        query = query.order_by(desc(History.create_time))
        
        # 分页
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        histories = [h.to_dict() for h in pagination.items]
        
        return jsonify({
            'success': True,
            'data': {
                'histories': histories,
                'total': pagination.total,
                'page': page,
                'per_page': per_page,
                'pages': pagination.pages
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取历史记录失败: {str(e)}'
        }), 500

@history_bp.route('/<int:history_id>', methods=['GET'])
@login_required
def get_history_detail(history_id):
    """获取历史记录详情"""
    try:
        user = request.current_user
        history = History.query.get_or_404(history_id)
        
        # 权限检查：管理员可以查看所有，普通用户只能查看自己的
        if user.level != 'admin' and history.user_id != user.id:
            return jsonify({
                'success': False,
                'message': '无权访问此记录'
            }), 403
        
        return jsonify({
            'success': True,
            'data': history.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取历史记录详情失败: {str(e)}'
        }), 500

@history_bp.route('/clear', methods=['POST'])
@login_required
def clear_history():
    """清空历史记录"""
    try:
        user = request.current_user
        
        # 管理员可以清空所有记录，普通用户只能清空自己的
        if user.level == 'admin':
            History.query.delete()
        else:
            History.query.filter_by(user_id=user.id).delete()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '历史记录已清空'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'清空历史记录失败: {str(e)}'
        }), 500

@history_bp.route('/stats', methods=['GET'])
@login_required
def get_history_stats():
    """获取历史记录统计"""
    try:
        user = request.current_user
        
        # 管理员可以查看所有统计，普通用户只能查看自己的
        if user.level == 'admin':
            query = History.query
        else:
            query = History.query.filter_by(user_id=user.id)
        
        total_count = query.count()
        success_count = query.filter(History.factorization_level == 'complete').count()
        
        return jsonify({
            'success': True,
            'data': {
                'total_count': total_count,
                'success_count': success_count
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取统计信息失败: {str(e)}'
        }), 500

