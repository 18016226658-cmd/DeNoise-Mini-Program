#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量生成 denoisetable 演示数据
================================
用途：
  - 为降噪历史记录页面提供足够的测试数据
  - 为可视化图表（日期、周次、时间、活跃用户）提供统计基础

说明：
  - 仅用于开发/演示环境，请不要在正式生产库中执行
"""

import os
import random
from datetime import datetime, timedelta

import pymysql

# 确保可以导入到上一级目录的 db_config
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
  sys.path.append(BASE_DIR)

from db_config import DB_CONFIG


def _random_birthday():
  """生成随机生日（介于 1980-01-01 ~ 2005-12-31）"""
  start = datetime(1980, 1, 1)
  end = datetime(2005, 12, 31)
  delta_days = (end - start).days
  d = start + timedelta(days=random.randint(0, delta_days))
  return d.strftime("%Y-%m-%d")


def generate_demo_data(days: int = 90, user_count: int = 100):
  """
  生成演示降噪数据
  - days:  最近多少天
  - user_count: 生成多少个 11 位手机号用户
  """
  conn = pymysql.connect(**DB_CONFIG)
  cursor = conn.cursor()

  # 生成 user_count 个 11 位手机号用户
  users = []
  for i in range(user_count):
    # 130 开头 + 8 位递增数字，保证 11 位
    phone = "13{:08d}".format(i + 1)  # 1300000001, 1300000002, ...
    name = f"用户{(i + 1):03d}"
    gender = random.choice(["男", "女"])
    birthday = _random_birthday()
    users.append((phone, name, gender, birthday))

  audio_names = [
      "别知己-海来阿木.wav",
      "如果爱还在.wav",
      "徐千雅-坐上火车去拉萨.wav",
      "月亮代表我的心.wav",
      "彩云之南.wav",
  ]

  now = datetime.now()
  total_inserted = 0

  for d in range(days):
    day = (now - timedelta(days=d)).date()
    for user_id, user_name, gender, birthday in users:
      # 每个用户每天 0~5 条记录
      count = random.randint(0, 5)
      for _ in range(count):
        # 随机时间（小时、分钟、秒）
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        de_noise_time = datetime(
            day.year, day.month, day.day, hour, minute, second
        )

        audio_name = random.choice(audio_names)
        extension = "wav"
        file_size = round(random.uniform(3.0, 50.0), 2)  # MB
        duration_seconds = random.randint(30, 360)       # 30秒~6分钟
        n_channels = random.choice([1, 2])
        border = 5

        sql = """
          INSERT INTO denoisetable
          (UserID, UserName, DeNoiseTime, Gender, Birthday,
           AudioName, Extension, FileSize, Duration, N_channels, BOrder)
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            sql,
            (
                user_id,
                user_name,
                de_noise_time,
                gender,
                birthday,
                audio_name,
                extension,
                file_size,
                duration_seconds,
                n_channels,
                border,
            ),
        )
        total_inserted += 1

  conn.commit()
  cursor.close()
  conn.close()
  # 控制台可能是 GBK 编码，避免使用特殊符号
  print("已生成并插入 {} 条 denoisetable 演示数据（最近 {} 天，{} 个用户）。".format(total_inserted, days, len(users)))


if __name__ == "__main__":
  # 默认生成最近 90 天、100 个用户的数据
  generate_demo_data(days=90, user_count=100)


