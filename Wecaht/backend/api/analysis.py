"""
可视化分析 API
"""
from flask import Blueprint, request, jsonify, send_file
from api.auth import login_required
from models import db, User, History
from datetime import datetime, timedelta
import os
import json
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import defaultdict
import io
import base64
from functools import wraps

analysis_bp = Blueprint('analysis', __name__)

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def admin_required(f):
    """管理员权限装饰器：先验证登录，再检查是否为管理员。

    使用 @wraps 保留原函数名字，避免 Flask 端点名都变成 decorated_function
    导致 View function mapping is overwriting... 的报错。
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

@analysis_bp.route('/job-usage-time', methods=['GET'])
@admin_required
def job_usage_time():
    """分析不同职业的使用时间分布"""
    try:
        # 获取所有历史记录
        histories = History.query.join(User).all()
        
        # 按职业分组统计使用时间（按小时）
        job_hour_stats = defaultdict(lambda: defaultdict(int))
        
        for history in histories:
            if history.user and history.user.job and history.create_time:
                hour = history.create_time.hour
                job = history.user.job
                job_hour_stats[job][hour] += 1
        
        # 如果没有数据，返回空结果
        if not job_hour_stats:
            return jsonify({
                'success': True,
                'data': {
                    'jobs': [],
                    'hours': list(range(24)),
                    'data': []
                }
            })
        
        # 创建图表
        fig, ax = plt.subplots(figsize=(14, 8))
        
        jobs = list(job_hour_stats.keys())
        hours = list(range(24))
        
        # 为每个职业绘制折线图
        for job in jobs:
            values = [job_hour_stats[job][h] for h in hours]
            ax.plot(hours, values, marker='o', label=job, linewidth=2, markersize=6)
        
        ax.set_xlabel('时间（小时）', fontsize=12)
        ax.set_ylabel('使用次数', fontsize=12)
        ax.set_title('不同职业的使用时间分布', fontsize=14, fontweight='bold')
        ax.set_xticks(hours)
        ax.set_xticklabels([f'{h:02d}:00' for h in hours], rotation=45)
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # 保存图片到内存
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        # 转换为 base64
        img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
        
        # 准备数据
        data = []
        for job in jobs:
            values = [job_hour_stats[job][h] for h in hours]
            data.append({
                'job': job,
                'values': values
            })
        
        return jsonify({
            'success': True,
            'data': {
                'image': f'data:image/png;base64,{img_base64}',
                'jobs': jobs,
                'hours': hours,
                'data': data
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'生成图表失败: {str(e)}'
        }), 500

@analysis_bp.route('/user-preferences', methods=['GET'])
@admin_required
def user_preferences():
    """分析用户偏好"""
    try:
        # 获取所有历史记录
        histories = History.query.join(User).all()
        
        # 1. 按职业统计使用频率
        job_usage = defaultdict(int)
        # 2. 按性别统计使用频率
        gender_usage = defaultdict(int)
        # 3. 按年龄段统计使用频率
        age_group_usage = defaultdict(int)
        # 4. 按数字位数统计
        digit_usage = defaultdict(int)
        # 5. 按分解类型统计
        number_type_usage = defaultdict(int)
        
        for history in histories:
            user = history.user
            if not user:
                continue
            
            # 职业统计
            if user.job:
                job_usage[user.job] += 1
            
            # 性别统计
            if user.gender_name:
                gender_usage[user.gender_name] += 1
            
            # 年龄段统计
            if user.age:
                if user.age < 18:
                    age_group = '18岁以下'
                elif user.age < 25:
                    age_group = '18-24岁'
                elif user.age < 35:
                    age_group = '25-34岁'
                elif user.age < 45:
                    age_group = '35-44岁'
                elif user.age < 55:
                    age_group = '45-54岁'
                else:
                    age_group = '55岁以上'
                age_group_usage[age_group] += 1
            
            # 数字位数统计
            if history.digit_count:
                if history.digit_count <= 10:
                    digit_group = '1-10位'
                elif history.digit_count <= 20:
                    digit_group = '11-20位'
                elif history.digit_count <= 50:
                    digit_group = '21-50位'
                elif history.digit_count <= 100:
                    digit_group = '51-100位'
                else:
                    digit_group = '100位以上'
                digit_usage[digit_group] += 1
            
            # 分解类型统计
            if history.number_type_name:
                number_type_usage[history.number_type_name] += 1
        
        # 创建多个子图
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('用户偏好分析', fontsize=16, fontweight='bold')
        
        # 1. 职业使用频率（饼图）
        if job_usage:
            ax1 = axes[0, 0]
            jobs = list(job_usage.keys())
            values = list(job_usage.values())
            ax1.pie(values, labels=jobs, autopct='%1.1f%%', startangle=90)
            ax1.set_title('各职业使用频率', fontsize=12, fontweight='bold')
        
        # 2. 性别使用频率（柱状图）
        if gender_usage:
            ax2 = axes[0, 1]
            genders = list(gender_usage.keys())
            values = list(gender_usage.values())
            ax2.bar(genders, values, color=['#FF69B4', '#87CEEB', '#98FB98'])
            ax2.set_title('性别使用频率', fontsize=12, fontweight='bold')
            ax2.set_ylabel('使用次数')
            ax2.tick_params(axis='x', rotation=45)
        
        # 3. 年龄段使用频率（柱状图）
        if age_group_usage:
            ax3 = axes[0, 2]
            age_groups = ['18岁以下', '18-24岁', '25-34岁', '35-44岁', '45-54岁', '55岁以上']
            values = [age_group_usage.get(ag, 0) for ag in age_groups]
            ax3.bar(age_groups, values, color='#FFB6C1')
            ax3.set_title('年龄段使用频率', fontsize=12, fontweight='bold')
            ax3.set_ylabel('使用次数')
            ax3.tick_params(axis='x', rotation=45)
        
        # 4. 数字位数分布（柱状图）
        if digit_usage:
            ax4 = axes[1, 0]
            digit_groups = ['1-10位', '11-20位', '21-50位', '51-100位', '100位以上']
            values = [digit_usage.get(dg, 0) for dg in digit_groups]
            ax4.bar(digit_groups, values, color='#DDA0DD')
            ax4.set_title('数字位数分布', fontsize=12, fontweight='bold')
            ax4.set_ylabel('使用次数')
            ax4.tick_params(axis='x', rotation=45)
        
        # 5. 分解类型分布（饼图）
        if number_type_usage:
            ax5 = axes[1, 1]
            types = list(number_type_usage.keys())
            values = list(number_type_usage.values())
            ax5.pie(values, labels=types, autopct='%1.1f%%', startangle=90)
            ax5.set_title('数字类型分布', fontsize=12, fontweight='bold')
        
        # 6. 每日使用趋势（折线图）
        ax6 = axes[1, 2]
        daily_usage = defaultdict(int)
        for history in histories:
            if history.create_time:
                date = history.create_time.date()
                daily_usage[date] += 1
        
        if daily_usage:
            dates = sorted(daily_usage.keys())
            values = [daily_usage[d] for d in dates]
            ax6.plot(dates, values, marker='o', linewidth=2, markersize=4)
            ax6.set_title('每日使用趋势', fontsize=12, fontweight='bold')
            ax6.set_ylabel('使用次数')
            ax6.set_xlabel('日期')
            ax6.tick_params(axis='x', rotation=45)
            ax6.grid(True, alpha=0.3)
        
        # 隐藏空的子图
        for ax in axes.flat:
            if len(ax.patches) == 0 and len(ax.lines) == 0 and len(ax.collections) == 0:
                ax.axis('off')
        
        plt.tight_layout()
        
        # 保存图片到内存
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        # 转换为 base64
        img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
        
        return jsonify({
            'success': True,
            'data': {
                'image': f'data:image/png;base64,{img_base64}',
                'job_usage': dict(job_usage),
                'gender_usage': dict(gender_usage),
                'age_group_usage': dict(age_group_usage),
                'digit_usage': dict(digit_usage),
                'number_type_usage': dict(number_type_usage)
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'生成图表失败: {str(e)}'
        }), 500

@analysis_bp.route('/usage-statistics', methods=['GET'])
@admin_required
def usage_statistics():
    """使用统计信息（包含可视化图表）"""
    try:
        # 总用户数
        total_users = User.query.count()
        
        # 总使用次数
        total_usage = History.query.count()
        
        # 今日使用次数
        today = datetime.now().date()
        today_usage = History.query.filter(
            db.func.date(History.create_time) == today
        ).count()
        
        # 本周使用次数
        week_ago = today - timedelta(days=7)
        week_usage = History.query.filter(
            History.create_time >= week_ago
        ).count()
        
        # 本月使用次数
        month_ago = today - timedelta(days=30)
        month_usage = History.query.filter(
            History.create_time >= month_ago
        ).count()
        
        # 平均每次分解耗时
        avg_time = db.session.query(db.func.avg(History.elapsed_time)).scalar()
        avg_time = round(avg_time, 3) if avg_time else 0
        
        # 完全分解成功率
        total_complete = History.query.filter_by(factorization_level='complete').count()
        success_rate = (total_complete / total_usage * 100) if total_usage > 0 else 0
        
        # 生成可视化图表
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('系统使用统计', fontsize=16, fontweight='bold')
        
        # 1. 时间维度使用统计（柱状图）
        ax1 = axes[0, 0]
        time_labels = ['今日', '本周', '本月', '总计']
        time_values = [today_usage, week_usage, month_usage, total_usage]
        colors = ['#FF69B4', '#FFB6C1', '#FFC0CB', '#DDA0DD']
        ax1.bar(time_labels, time_values, color=colors)
        ax1.set_title('时间维度使用统计', fontsize=12, fontweight='bold')
        ax1.set_ylabel('使用次数')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # 2. 用户等级分布（饼图）
        ax2 = axes[0, 1]
        normal_count = User.query.filter_by(level='normal').count()
        vip_count = User.query.filter_by(level='vip').count()
        svip_count = User.query.filter_by(level='svip').count()
        admin_count = User.query.filter_by(level='admin').count()
        
        if total_users > 0:
            level_labels = ['普通用户', 'VIP用户', 'SVIP用户', '管理员']
            level_values = [normal_count, vip_count, svip_count, admin_count]
            level_colors = ['#87CEEB', '#FFD700', '#FF69B4', '#DC143C']
            # 过滤掉0值
            filtered_data = [(l, v, c) for l, v, c in zip(level_labels, level_values, level_colors) if v > 0]
            if filtered_data:
                labels, values, colors_list = zip(*filtered_data)
                ax2.pie(values, labels=labels, autopct='%1.1f%%', colors=colors_list, startangle=90)
                ax2.set_title('用户等级分布', fontsize=12, fontweight='bold')
        
        # 3. 分解类型分布（柱状图）
        ax3 = axes[1, 0]
        complete_count = History.query.filter_by(factorization_level='complete').count()
        partial_count = History.query.filter_by(factorization_level='partial').count()
        failed_count = History.query.filter_by(factorization_level='failed').count()
        
        type_labels = ['完全分解', '部分分解', '失败']
        type_values = [complete_count, partial_count, failed_count]
        ax3.bar(type_labels, type_values, color=['#90EE90', '#FFD700', '#FF6B6B'])
        ax3.set_title('分解类型分布', fontsize=12, fontweight='bold')
        ax3.set_ylabel('次数')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # 4. 数字位数分布（折线图）
        ax4 = axes[1, 1]
        digit_ranges = ['1-10位', '11-20位', '21-50位', '51-100位', '100位以上']
        digit_counts = [
            History.query.filter(History.digit_count.between(1, 10)).count(),
            History.query.filter(History.digit_count.between(11, 20)).count(),
            History.query.filter(History.digit_count.between(21, 50)).count(),
            History.query.filter(History.digit_count.between(51, 100)).count(),
            History.query.filter(History.digit_count > 100).count()
        ]
        ax4.plot(digit_ranges, digit_counts, marker='o', linewidth=2, markersize=8, color='#FF69B4')
        ax4.set_title('数字位数分布', fontsize=12, fontweight='bold')
        ax4.set_ylabel('使用次数')
        ax4.grid(True, alpha=0.3)
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        # 保存图片到内存
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        # 转换为 base64
        img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
        
        return jsonify({
            'success': True,
            'data': {
                'image': f'data:image/png;base64,{img_base64}',
                'total_users': total_users,
                'total_usage': total_usage,
                'today_usage': today_usage,
                'week_usage': week_usage,
                'month_usage': month_usage,
                'avg_time': avg_time,
                'success_rate': round(success_rate, 2),
                'normal_count': normal_count,
                'vip_count': vip_count,
                'svip_count': svip_count,
                'admin_count': admin_count,
                'complete_count': complete_count,
                'partial_count': partial_count,
                'failed_count': failed_count
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取统计信息失败: {str(e)}'
        }), 500

