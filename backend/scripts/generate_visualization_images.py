#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
离线生成可视化统计图片
=====================
用途：
  - 直接从数据库读取 denoisetable 数据
  - 生成 4 张统计图片并保存到 static/visualization 目录
说明：
  - 与 /api/getStatisticsImages 使用同一套统计逻辑
  - 可在未启动 Flask 服务时单独执行
"""

import os
import sys
import time

import pymysql
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from db_config import DB_CONFIG  # noqa: E402
from config import VISUALIZATION_IMAGE_DIR, BASE_DIR  # noqa: E402


def load_statistics_raw():
    """从数据库加载原始降噪记录并做聚合统计，返回字典。"""
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

    date_data = {}
    week_data = {}
    time_data = {}
    user_data = {}

    for user_id, user_name, de_noise_time in records:
        user_id = user_id or ""
        user_name = user_name or "未知用户"

        if not de_noise_time:
            continue

        if isinstance(de_noise_time, str):
            de_noise_time = datetime.strptime(de_noise_time, "%Y-%m-%d %H:%M:%S")

        date_str = de_noise_time.strftime("%Y-%m-%d")
        date_data[date_str] = date_data.get(date_str, 0) + 1

        weekday = de_noise_time.weekday()
        week_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        week_name = week_names[weekday]
        week_data[week_name] = week_data.get(week_name, 0) + 1

        hour = de_noise_time.hour
        time_data[hour] = time_data.get(hour, 0) + 1

        user_key = f"{user_name}({user_id})"
        user_data[user_key] = user_data.get(user_key, 0) + 1

    date_list = []
    today = datetime.now().date()
    for i in range(30):
        date = today - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        date_list.append({"date": date_str, "count": date_data.get(date_str, 0)})
    date_list.reverse()

    week_list = []
    week_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    for week_name in week_names:
        week_list.append({"week": week_name, "count": week_data.get(week_name, 0)})

    time_list = []
    for hour in range(24):
        time_list.append({"hour": hour, "count": time_data.get(hour, 0)})

    user_list = []
    sorted_users = sorted(user_data.items(), key=lambda x: x[1], reverse=True)[:10]
    for user_key, count in sorted_users:
        if "(" in user_key and ")" in user_key:
            user_name = user_key.split("(")[0]
            user_id = user_key.split("(")[1].rstrip(")")
        else:
            user_name = user_key
            user_id = ""
        user_list.append({"userName": user_name, "userId": user_id, "count": count})

    return {
        "dateData": date_list,
        "weekData": week_list,
        "timeData": time_list,
        "userData": user_list,
    }


def generate_images():
    """生成 4 张统计图片到 VISUALIZATION_IMAGE_DIR 目录。"""
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import font_manager
    import matplotlib.pyplot as plt

    # 配置中文字体为 SimHei，避免中文乱码
    font_path = os.path.join(BASE_DIR, "SimHei.ttf")
    if os.path.exists(font_path):
        try:
            font_manager.fontManager.addfont(font_path)
            font_prop = font_manager.FontProperties(fname=font_path)
            font_name = font_prop.get_name()
            # 同时设置 family 和 sans-serif，确保中文优先使用该字体
            matplotlib.rcParams["font.family"] = font_name
            matplotlib.rcParams["font.sans-serif"] = [font_name]
            print("使用字体：", font_name)
        except Exception as e:
            print("加载 SimHei.ttf 字体失败：", e)
    # 解决坐标轴负号显示为方块的问题
    matplotlib.rcParams["axes.unicode_minus"] = False

    if not os.path.exists(VISUALIZATION_IMAGE_DIR):
        os.makedirs(VISUALIZATION_IMAGE_DIR, exist_ok=True)

    data = load_statistics_raw()

    # 1. 日期折线图
    dates = [item["date"] for item in data["dateData"]]
    counts = [item["count"] for item in data["dateData"]]
    plt.figure(figsize=(8, 4))
    plt.plot(dates, counts, marker="o")
    plt.xticks(rotation=45, fontsize=6)
    plt.title("日期－降噪次数")
    plt.xlabel("日期")
    plt.ylabel("次数")
    plt.tight_layout()
    plt.savefig(os.path.join(VISUALIZATION_IMAGE_DIR, "date_line.png"))
    plt.close()

    # 2. 周次饼图
    week_labels = [item["week"] for item in data["weekData"]]
    week_counts = [item["count"] for item in data["weekData"]]
    plt.figure(figsize=(5, 5))
    plt.pie(week_counts, labels=week_labels, autopct="%1.1f%%")
    plt.title("周次－降噪次数")
    plt.tight_layout()
    plt.savefig(os.path.join(VISUALIZATION_IMAGE_DIR, "week_pie.png"))
    plt.close()

    # 3. 时间折线图
    hours = [item["hour"] for item in data["timeData"]]
    hour_counts = [item["count"] for item in data["timeData"]]
    plt.figure(figsize=(8, 4))
    plt.plot(hours, hour_counts, marker="o")
    plt.title("一天中时间－降噪次数")
    plt.xlabel("小时")
    plt.ylabel("次数")
    plt.xticks(range(0, 24, 2))
    plt.tight_layout()
    plt.savefig(os.path.join(VISUALIZATION_IMAGE_DIR, "time_line.png"))
    plt.close()

    # 4. 活跃用户柱状图
    user_names = [item["userName"] for item in data["userData"]]
    user_counts = [item["count"] for item in data["userData"]]
    plt.figure(figsize=(8, 4))
    plt.bar(user_names, user_counts)
    plt.title("活跃用户－降噪次数")
    plt.xlabel("用户")
    plt.ylabel("次数")
    plt.xticks(rotation=45, fontsize=6)
    plt.tight_layout()
    plt.savefig(os.path.join(VISUALIZATION_IMAGE_DIR, "user_bar.png"))
    plt.close()

    print("可视化图片已生成到目录：", VISUALIZATION_IMAGE_DIR)


if __name__ == "__main__":
    generate_images()


