-- ============================================
-- 大整数分解系统 - MySQL 数据库初始化脚本
-- ============================================
-- 说明：此脚本用于创建数据库和表结构
-- 使用方法：在 MySQL 中执行此脚本
-- ============================================

-- 1. 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS `xqq` 
  DEFAULT CHARACTER SET utf8mb4 
  DEFAULT COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE `xqq`;

-- 2. 删除已存在的表（先删除有外键依赖的表）
DROP TABLE IF EXISTS `histories`;
DROP TABLE IF EXISTS `users`;

-- 3. 创建用户表
CREATE TABLE `users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` VARCHAR(50) NOT NULL COMMENT '用户名',
  `password` VARCHAR(255) NOT NULL COMMENT '密码',
  `level` VARCHAR(20) NOT NULL DEFAULT 'normal' COMMENT '用户等级：normal, vip, svip, admin',
  `level_name` VARCHAR(50) NOT NULL DEFAULT '普通用户' COMMENT '用户等级名称',
  `max_digits` INT(11) NOT NULL DEFAULT 50 COMMENT '最大分解位数',
  `gender` VARCHAR(10) DEFAULT NULL COMMENT '性别：male, female, other',
  `gender_name` VARCHAR(10) DEFAULT NULL COMMENT '性别名称：男, 女, 其他',
  `birth_year` INT(11) DEFAULT NULL COMMENT '出生年份',
  `birth_month` INT(11) DEFAULT NULL COMMENT '出生月份',
  `birth_day` INT(11) DEFAULT NULL COMMENT '出生日期',
  `age` INT(11) DEFAULT NULL COMMENT '年龄',
  `job` VARCHAR(100) DEFAULT NULL COMMENT '职业',
  `avatar` VARCHAR(255) DEFAULT NULL COMMENT '头像URL',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_login_time` DATETIME DEFAULT NULL COMMENT '最后登录时间',
  `login_count` INT(11) DEFAULT 0 COMMENT '登录次数',
  `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `idx_level` (`level`),
  KEY `idx_create_time` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 4. 创建历史记录表
CREATE TABLE `histories` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '历史记录ID',
  `user_id` INT(11) NOT NULL COMMENT '用户ID',
  `number` TEXT NOT NULL COMMENT '原数（大整数，使用TEXT类型）',
  `factors` TEXT NOT NULL COMMENT '因子列表（JSON字符串）',
  `formula` TEXT DEFAULT NULL COMMENT '分解式',
  `number_type` VARCHAR(20) DEFAULT NULL COMMENT '数字类型：prime, composite, zero, unit, unknown',
  `number_type_name` VARCHAR(50) DEFAULT NULL COMMENT '数字类型名称：素数, 合数, 非素非合, 未知',
  `factorization_level` VARCHAR(20) DEFAULT NULL COMMENT '分解程度：complete, partial, failed',
  `factorization_level_name` VARCHAR(50) DEFAULT NULL COMMENT '分解程度名称：完全分解, 部分分解, 不能分解',
  `elapsed_time` FLOAT DEFAULT NULL COMMENT '耗时（秒）',
  `digit_count` INT(11) DEFAULT NULL COMMENT '数字位数',
  `factor_count` INT(11) DEFAULT NULL COMMENT '分解次数（因子数量）',
  `calc_desc` TEXT DEFAULT NULL COMMENT '计算说明（介绍算）',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_create_time` (`create_time`),
  CONSTRAINT `fk_histories_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='历史记录表';

-- 5. 插入默认管理员账户
-- 注意：密码为 '123456'（明文，实际生产环境应使用加密密码）
INSERT INTO `users` (`username`, `password`, `level`, `level_name`, `max_digits`, `create_time`, `login_count`) 
VALUES ('xqq', '123456', 'admin', '管理员', 200, NOW(), 0)
ON DUPLICATE KEY UPDATE `level`='admin', `level_name`='管理员', `max_digits`=200;

-- 6. 创建索引优化查询性能
-- 用户表索引（已在表定义中创建）
-- 历史记录表索引（已在表定义中创建）

-- ============================================
-- 初始化完成
-- ============================================
-- 默认管理员账户：
--   用户名：xqq
--   密码：123456
--   等级：管理员
--   最大分解位数：200位
-- ============================================

