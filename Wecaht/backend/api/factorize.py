"""
大整数分解 API
"""
from flask import Blueprint, request, jsonify
from api.auth import login_required
from algorithms import factorize, validate_input, get_number_type, get_factorization_level
from models import db, History
from datetime import datetime

factorize_bp = Blueprint('factorize', __name__)

@factorize_bp.route('/factorize', methods=['POST'])
@login_required
def factorize_number():
    """分解大整数"""
    try:
        data = request.get_json()
        number_str = data.get('number', '').strip()
        mode = data.get('mode', 'standard')  # standard 或 fast
        
        if not number_str:
            return jsonify({
                'success': False,
                'message': '请输入数字'
            }), 400
        
        # 验证输入
        validation = validate_input(number_str)
        if not validation['valid']:
            return jsonify({
                'success': False,
                'message': validation['error']
            }), 400
        
        number = validation['number']
        digit_count = len(number_str)
        
        # 检查用户权限
        user = request.current_user
        if digit_count > user.max_digits:
            return jsonify({
                'success': False,
                'message': f'超过最大位数限制（{user.max_digits}位）'
            }), 403
        
        # 开始分解
        start_time = datetime.now()
        
        try:
            # 调用分解算法（带超时保护）
            factors = factorize(number, mode=mode)
        except Exception as algo_error:
            # 如果算法出错，返回错误信息
            return jsonify({
                'success': False,
                'message': f'分解算法执行失败: {str(algo_error)}'
            }), 500

        elapsed_time = (datetime.now() - start_time).total_seconds()

        # 检查是否超时（超过5分钟）
        if elapsed_time > 300:
            return jsonify({
                'success': False,
                'message': '分解时间过长，请尝试更小的数字或使用快速模式'
            }), 408  # 408 Request Timeout

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

        # 验证每个因子是否为素数
        factors_with_prime = []
        for f in factors:
            from algorithms import miller_rabin
            is_prime = False
            if f > 1:
                is_prime = miller_rabin(f, 3)
            factors_with_prime.append({
                'value': str(f),
                'is_prime': is_prime
            })

        factor_count = len(factors)
        calc_desc = f"{number_type['description']}；{factorization_level['description']}"

        result = {
            'number': number_str,
            'factors': factors_with_prime,
            'formula': formula,
            'elapsed_time': round(elapsed_time, 3),
            'number_type': number_type['type'],
            'number_type_name': number_type['type_name'],
            'number_type_desc': number_type['description'],
            'factorization_level': factorization_level['level'],
            'factorization_level_name': factorization_level['level_name'],
            'factorization_level_desc': factorization_level['description'],
            'factor_count': factor_count,
            'calc_desc': calc_desc
        }

        # 保存到历史记录（限制每个用户最多保留100条记录）
        # 注意：先返回结果，再异步保存历史记录，避免阻塞响应
        try:
            import json
            from sqlalchemy import desc

            # 先保存新记录
            history = History(
                user_id=user.id,
                number=number_str,
                factors=json.dumps([str(f) for f in factors]),  # 转换为 JSON 字符串
                formula=formula,
                number_type=number_type['type'],
                number_type_name=number_type['type_name'],
                factorization_level=factorization_level['level'],
                factorization_level_name=factorization_level['level_name'],
                elapsed_time=elapsed_time,
                digit_count=digit_count,
                factor_count=factor_count,
                calc_desc=calc_desc
            )
            db.session.add(history)
            db.session.commit()

            # 保存后再检查并清理旧记录（避免阻塞）
            try:
                user_history_count = History.query.filter_by(user_id=user.id).count()
                if user_history_count > 100:
                    # 获取需要保留的最新100条记录的ID
                    latest_histories = History.query.filter_by(user_id=user.id)\
                        .order_by(desc(History.create_time))\
                        .limit(100)\
                        .all()
                    latest_ids = [h.id for h in latest_histories]

                    # 删除不在最新100条中的记录（批量删除，更高效）
                    if latest_ids:
                        History.query.filter_by(user_id=user.id)\
                            .filter(~History.id.in_(latest_ids))\
                            .delete(synchronize_session=False)
                        db.session.commit()
            except Exception as cleanup_error:
                print(f'清理旧历史记录失败: {cleanup_error}')
                db.session.rollback()
                # 清理失败不影响主流程
        except Exception as e:
            print(f'保存历史记录失败: {e}')
            db.session.rollback()
            # 不影响返回结果
        
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'分解失败: {str(e)}'
        }), 500

@factorize_bp.route('/validate', methods=['POST'])
@login_required
def validate_number():
    """验证输入数字"""
    try:
        data = request.get_json()
        number_str = data.get('number', '').strip()
        
        if not number_str:
            return jsonify({
                'success': False,
                'message': '请输入数字'
            }), 400
        
        # 验证输入
        validation = validate_input(number_str)
        if not validation['valid']:
            return jsonify({
                'success': False,
                'message': validation['error']
            }), 400
        
        number = validation['number']
        digit_count = len(number_str)
        
        # 检查用户权限
        user = request.current_user
        if digit_count > user.max_digits:
            return jsonify({
                'success': False,
                'message': f'超过最大位数限制（{user.max_digits}位）'
            }), 403
        
        # 快速判断数字类型
        from algorithms import miller_rabin
        number_type = None
        
        if number == 0:
            number_type = {
                'type': 'zero',
                'type_name': '非素非合',
                'description': '0既不是素数也不是合数'
            }
        elif number == 1:
            number_type = {
                'type': 'unit',
                'type_name': '非素非合',
                'description': '1既不是素数也不是合数'
            }
        else:
            try:
                is_prime = miller_rabin(number, 3)
                if is_prime:
                    number_type = {
                        'type': 'prime',
                        'type_name': '素数',
                        'description': '只能被1和自身整除的正整数'
                    }
                else:
                    if number <= 1000000:
                        number_type = {
                            'type': 'composite',
                            'type_name': '合数',
                            'description': '有多个因子的正整数'
                        }
                    else:
                        number_type = {
                            'type': 'unknown',
                            'type_name': '未知',
                            'description': '需要分解后才能确定数字类型'
                        }
            except Exception as e:
                number_type = {
                    'type': 'unknown',
                    'type_name': '未知',
                    'description': '无法判断数字类型'
                }
        
        return jsonify({
            'success': True,
            'data': {
                'valid': True,
                'digit_count': digit_count,
                'number_type': number_type
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'验证失败: {str(e)}'
        }), 500

