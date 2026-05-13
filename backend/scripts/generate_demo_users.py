#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量生成 users 表演示用户
=========================
用途：
  - 为前端“所有用户”列表提供足够的真实数据
  - 配合 denoisetable 的演示数据，用于可视化展示
说明：
  - 仅用于开发/演示环境，请勿在正式生产环境使用
"""

import os
import random
from datetime import datetime, timedelta

import pymysql

import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
  sys.path.append(BASE_DIR)

from db_config import DB_CONFIG


def _random_birthday():
  """生成随机生日（1980-01-01 ~ 2005-12-31）"""
  start = datetime(1980, 1, 1)
  end = datetime(2005, 12, 31)
  days = (end - start).days
  d = start + timedelta(days=random.randint(0, days))
  return d.strftime("%Y-%m-%d")


def generate_demo_users(user_count: int = 100):
  """
  生成演示用户：
  - 手机号：11 位，以 13 开头递增
  - 密码：统一 '123456'
  - 用户类型：2（普通用户）
  - 配额：降噪/分离各 100 次
  """
  conn = pymysql.connect(**DB_CONFIG)
  cursor = conn.cursor()

  # 先读取已存在的手机号，避免重复插入
  cursor.execute("SELECT Phone FROM users")
  existing_phones = {row[0] for row in cursor.fetchall()}

  inserted = 0
  for i in range(user_count):
    phone = "13{:08d}".format(i + 1)  # 1300000001, 1300000002, ...
    if phone in existing_phones:
      continue

    user_name = f"用户{(i + 1):03d}"
    password = "123456"
    register_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    gender = random.choice(["男", "女"])
    birthday = _random_birthday()
    face_img = "/static/image/header.png"
    user_type = 2  # 普通用户
    max_sep = 100
    cur_sep = 0
    max_noise = 100
    cur_noise = 0

    sql = """
      INSERT INTO users
      (Phone, UserName, Password, RegisterTime, Gender, Birthday,
       FaceImg, UserType, MaxSepTimes, CurSepTimes, MaxNoiseTimes, CurNoiseTimes)
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(
      sql,
      (
        phone,
        user_name,
        password,
        register_time,
        gender,
        birthday,
        face_img,
        user_type,
        max_sep,
        cur_sep,
        max_noise,
        cur_noise,
      ),
    )
    inserted += 1

  conn.commit()
  cursor.close()
  conn.close()
  print("已生成并插入 {} 个演示用户。".format(inserted))


if __name__ == "__main__":
  generate_demo_users(user_count=100)


