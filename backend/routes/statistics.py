# routes/statistics.py
# ============================================
# 数据统计接口路由模块
# ============================================
# 功能：提供降噪数据统计接口（管理员功能）

from flask import Blueprint, request, jsonify, url_for, current_app
import pymysql
import json
from datetime import datetime, timedelta
import os
import time

from db_config import DB_CONFIG
from config import VISUALIZATION_IMAGE_DIR, BASE_DIR

# 创建蓝图对象
statistics_bp = Blueprint('statistics', __name__)


def _load_statistics_raw():
    """从数据库加载原始降噪记录并做聚合统计，返回字典。"""
    # 连接数据库
    connect = pymysql.Connect(**DB_CONFIG)
    cursor = connect.cursor()

    sql = """
        SELECT UserID, UserName, DeNoiseTime 
        FROM denoisetable 
        WHERE DeNoiseTime IS NOT NULL
        ORDER BY DeNoiseTime DESC
    """
    cursor.execute(sql)
    records = cursor.fetchall()
    connect.close()

    # 统计数据
    date_data = {}      # 日期 -> 次数
    week_data = {}      # 周次 -> 次数
    time_data = {}      # 小时 -> 次数
    user_data = {}      # 用户 -> 次数

    for record in records:
        user_id = record[0] or ''
        user_name = record[1] or '未知用户'
        de_noise_time = record[2]

        if not de_noise_time:
            continue

        # 解析时间
        if isinstance(de_noise_time, str):
            de_noise_time = datetime.strptime(de_noise_time, '%Y-%m-%d %H:%M:%S')

        # 1. 按日期统计
        date_str = de_noise_time.strftime('%Y-%m-%d')
        date_data[date_str] = date_data.get(date_str, 0) + 1

        # 2. 按周次统计（周一到周日）
        weekday = de_noise_time.weekday()  # 0=周一, 6=周日
        week_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        week_name = week_names[weekday]
        week_data[week_name] = week_data.get(week_name, 0) + 1

        # 3. 按小时统计
        hour = de_noise_time.hour
        time_data[hour] = time_data.get(hour, 0) + 1

        # 4. 按用户统计
        user_key = f"{user_name}({user_id})"
        user_data[user_key] = user_data.get(user_key, 0) + 1

    # 格式化日期数据（最近30天）
    date_list = []
    today = datetime.now().date()
    for i in range(30):
        date = today - timedelta(days=i)
        date_str = date.strftime('%Y-%m-%d')
        date_list.append({
            'date': date_str,
            'count': date_data.get(date_str, 0)
        })
    date_list.reverse()  # 按时间正序

    # 格式化周次数据
    week_list = []
    week_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    for week_name in week_names:
        week_list.append({
            'week': week_name,
            'count': week_data.get(week_name, 0)
        })

    # 格式化时间数据（0-23小时）
    time_list = []
    for hour in range(24):
        time_list.append({
            'hour': hour,
            'count': time_data.get(hour, 0)
        })

    # 格式化用户数据（按降噪次数排序，取前10名）
    user_list = []
    sorted_users = sorted(user_data.items(), key=lambda x: x[1], reverse=True)[:10]
    for user_key, count in sorted_users:
        # 解析用户名和手机号
        if '(' in user_key and ')' in user_key:
            user_name = user_key.split('(')[0]
            user_id = user_key.split('(')[1].rstrip(')')
        else:
            user_name = user_key
            user_id = ''
        user_list.append({
            'userName': user_name,
            'userId': user_id,
            'count': count
        })

    return {
        'dateData': date_list,
        'weekData': week_list,
        'timeData': time_list,
        'userData': user_list,
    }


@statistics_bp.route('/api/getStatistics', methods=['POST'])
def get_statistics():
    """
    获取降噪数据统计（原始 JSON 数据）
    """
    try:
        data = _load_statistics_raw()
        result = {
            'success': True,
            'data': data
        }
        return json.dumps(result, ensure_ascii=False), 200, {"Content-Type": "application/json"}
    except Exception as e:
        print(f"获取统计数据失败: {e}")
        import traceback
        traceback.print_exc()
        return json.dumps({
            'success': False,
            'message': f'获取统计数据失败: {str(e)}'
        }, ensure_ascii=False), 200, {"Content-Type": "application/json"}


def _generate_visualization_images():
    """
    生成可视化图表的内部函数（可被多个接口复用）
    返回生成结果字典
    """
    try:
        import matplotlib
        matplotlib.use('Agg')
        from matplotlib import font_manager
        import matplotlib.pyplot as plt

        # 使用 backend 目录下的 SimHei.ttf，避免中文乱码
        font_path = os.path.join(BASE_DIR, 'SimHei.ttf')
        if os.path.exists(font_path):
            try:
                font_manager.fontManager.addfont(font_path)
                font_prop = font_manager.FontProperties(fname=font_path)
                font_name = font_prop.get_name()
                matplotlib.rcParams['font.family'] = font_name
                matplotlib.rcParams['font.sans-serif'] = [font_name]
            except Exception as e:
                print(f'加载 SimHei.ttf 字体失败：{e}')
        # 解决坐标轴负号显示异常
        matplotlib.rcParams['axes.unicode_minus'] = False

        data = _load_statistics_raw()
        timestamp = int(time.time())

        # 1. 日期折线图
        dates = [item['date'] for item in data['dateData']]
        counts = [item['count'] for item in data['dateData']]
        plt.figure(figsize=(10, 5))
        plt.plot(dates, counts, marker='o', linewidth=2, markersize=4, color='#6A5ACD')
        plt.fill_between(dates, counts, alpha=0.3, color='#6A5ACD')
        plt.xticks(rotation=45, fontsize=8)
        plt.title('日期－降噪次数', fontsize=14, fontweight='bold')
        plt.xlabel('日期', fontsize=10)
        plt.ylabel('次数', fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        date_path = os.path.join(VISUALIZATION_IMAGE_DIR, 'date_line.png')
        plt.savefig(date_path, dpi=150, bbox_inches='tight')
        plt.close()

        # 2. 周次饼图
        week_labels = [item['week'] for item in data['weekData']]
        week_counts = [item['count'] for item in data['weekData']]
        plt.figure(figsize=(8, 8))
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE']
        plt.pie(week_counts, labels=week_labels, autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('周次－降噪次数', fontsize=14, fontweight='bold')
        plt.tight_layout()
        week_path = os.path.join(VISUALIZATION_IMAGE_DIR, 'week_pie.png')
        plt.savefig(week_path, dpi=150, bbox_inches='tight')
        plt.close()

        # 3. 时间折线图
        hours = [item['hour'] for item in data['timeData']]
        hour_counts = [item['count'] for item in data['timeData']]
        plt.figure(figsize=(10, 5))
        plt.plot(hours, hour_counts, marker='o', linewidth=2, markersize=4, color='#44ADFB')
        plt.fill_between(hours, hour_counts, alpha=0.3, color='#44ADFB')
        plt.title('一天中时间－降噪次数', fontsize=14, fontweight='bold')
        plt.xlabel('小时', fontsize=10)
        plt.ylabel('次数', fontsize=10)
        plt.xticks(range(0, 24, 2))
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        time_path = os.path.join(VISUALIZATION_IMAGE_DIR, 'time_line.png')
        plt.savefig(time_path, dpi=150, bbox_inches='tight')
        plt.close()

        # 4. 活跃用户柱状图
        user_names = [item['userName'] for item in data['userData']]
        user_counts = [item['count'] for item in data['userData']]
        plt.figure(figsize=(10, 5))
        colors_bar = plt.cm.viridis(range(len(user_names))) if len(user_names) > 0 else ['#6A5ACD']
        plt.bar(user_names, user_counts, color=colors_bar)
        plt.title('活跃用户－降噪次数', fontsize=14, fontweight='bold')
        plt.xlabel('用户', fontsize=10)
        plt.ylabel('次数', fontsize=10)
        plt.xticks(rotation=45, fontsize=8, ha='right')
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        user_path = os.path.join(VISUALIZATION_IMAGE_DIR, 'user_bar.png')
        plt.savefig(user_path, dpi=150, bbox_inches='tight')
        plt.close()

        # 生成静态访问路径
        base_url = '/static/visualization'
        return {
            'success': True,
            'timestamp': timestamp,
            'data': {
                'dateImage': f"{base_url}/date_line.png?t={timestamp}",
                'weekImage': f"{base_url}/week_pie.png?t={timestamp}",
                'timeImage': f"{base_url}/time_line.png?t={timestamp}",
                'userImage': f"{base_url}/user_bar.png?t={timestamp}",
            }
        }
    except Exception as e:
        print(f"生成统计图片失败: {e}")
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'message': f'生成统计图片失败: {str(e)}'
        }


@statistics_bp.route('/api/getStatisticsImages', methods=['POST'])
def get_statistics_images():
    """
    生成并返回可视化图片的访问路径
    - 日期－降噪次数（折线图）
    - 周次－降噪次数（饼图）
    - 一天中时间－降噪次数（折线图）
    - 活跃用户－降噪次数（柱状图）
    """
    result = _generate_visualization_images()
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 200


@statistics_bp.route('/api/regenerateVisualization', methods=['POST'])
def regenerate_visualization():
    """
    重新生成可视化图表（管理员功能）
    返回新生成的图片路径
    """
    result = _generate_visualization_images()
    if result['success']:
        return jsonify({
            'success': True,
            'message': '可视化图表已重新生成',
            'data': result['data']
        }), 200
    else:
        return jsonify({
            'success': False,
            'message': result.get('message', '生成失败')
        }), 200

