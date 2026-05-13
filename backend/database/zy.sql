/*
 * 音频降噪系统 - 统一数据库建库脚本
 * Database: audio (或 chatgpt，根据实际需要选择)
 * Version: 1.0
 * Date: 2025-01-07
 * 
 * 说明：
 * 本脚本整合了用户管理、音频降噪、音频分离、聊天记录等功能所需的表结构
 * 包含：users, denoisetable, sepaudiotable, chattable
 * 
 * 使用前请先创建数据库：
 * CREATE DATABASE IF NOT EXISTS `audio` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
 */

-- 选择数据库（如果不存在会报错，请先创建数据库）
USE `audio`;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================
-- 1. 用户表（带配额管理）
-- ============================================
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `UserID` int NOT NULL AUTO_INCREMENT COMMENT '用户ID（自增主键）',
  `Phone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '手机号（唯一标识）',
  `UserName` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户名',
  `Password` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '密码',
  `RegisterTime` datetime DEFAULT NULL COMMENT '注册时间',
  `Gender` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '性别（男/女）',
  `Birthday` date DEFAULT NULL COMMENT '出生日期',
  `FaceImg` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '头像路径',
  `UserType` int DEFAULT NULL COMMENT '用户类型（1-管理员，2-普通用户，3-游客）',
  `MaxSepTimes` int DEFAULT NULL COMMENT '音频分离最大次数',
  `CurSepTimes` int DEFAULT 0 COMMENT '音频分离当前已用次数',
  `MaxNoiseTimes` int DEFAULT NULL COMMENT '音频降噪最大次数',
  `CurNoiseTimes` int DEFAULT 0 COMMENT '音频降噪当前已用次数',
  PRIMARY KEY (`UserID`) USING BTREE,
  UNIQUE KEY `uk_phone` (`Phone`) COMMENT '手机号唯一索引'
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='用户表';

-- ============================================
-- 2. 音频降噪历史记录表
-- ============================================
DROP TABLE IF EXISTS `denoisetable`;
CREATE TABLE `denoisetable` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `UserID` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '用户手机号',
  `UserName` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '用户昵称',
  `DeNoiseTime` datetime DEFAULT NULL COMMENT '降噪处理时间',
  `Gender` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '性别',
  `Birthday` date DEFAULT NULL COMMENT '出生年月',
  `AudioName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '音频文件名称',
  `Extension` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '音频文件类型（wav/mp3/ogg等）',
  `FileSize` double(10,2) DEFAULT NULL COMMENT '音频文件大小（MB）',
  `Duration` double(10,2) DEFAULT NULL COMMENT '音频文件播放时长（秒）',
  `N_channels` int DEFAULT NULL COMMENT '音频声道数（1-单声道，2-立体声）',
  `BOrder` int DEFAULT NULL COMMENT '巴特沃斯滤波阶数',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_userid` (`UserID`) COMMENT '用户ID索引',
  KEY `idx_denoisetime` (`DeNoiseTime`) COMMENT '降噪时间索引'
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='音频降噪历史记录表';

-- ============================================
-- 3. 音频分离历史记录表
-- ============================================
DROP TABLE IF EXISTS `sepaudiotable`;
CREATE TABLE `sepaudiotable` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `UserID` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户手机号',
  `UserName` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '用户昵称',
  `Gender` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '性别',
  `Birthday` date DEFAULT NULL COMMENT '出生年月',
  `SepTime` datetime DEFAULT NULL COMMENT '分离处理时间',
  `MxName` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '分离模型名称（如：htdemucs）',
  `AudioName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '音频文件名（歌曲名）',
  `Extension` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '音频文件类型（wav/mp3/ogg/flac等）',
  `FileSize` double(10,2) DEFAULT NULL COMMENT '音频文件大小（MB）',
  `Duration` double(10,2) DEFAULT NULL COMMENT '音频播放时长（秒）',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_userid` (`UserID`) COMMENT '用户ID索引',
  KEY `idx_septime` (`SepTime`) COMMENT '分离时间索引'
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='音频分离历史记录表';

-- ============================================
-- 4. 聊天记录表（ChatGPT/文心一言）
-- ============================================
DROP TABLE IF EXISTS `chattable`;
CREATE TABLE `chattable` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `Question` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '用户问题',
  `Answer` varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'AI回答',
  `UserID` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '用户手机号',
  `UserName` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '用户昵称',
  `ChatTime` datetime DEFAULT NULL COMMENT '聊天时间',
  `Gender` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '性别',
  `Birthday` date DEFAULT NULL COMMENT '出生日期',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_userid` (`UserID`) COMMENT '用户ID索引',
  KEY `idx_chattime` (`ChatTime`) COMMENT '聊天时间索引'
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='聊天记录表';

-- ============================================
-- 5. 外键约束（可选，建议在数据导入后再添加）
-- ============================================
-- 注意：如果UserID字段类型不一致，需要先统一类型
-- ALTER TABLE `denoisetable` 
--   ADD CONSTRAINT `fk_denoise_user` 
--   FOREIGN KEY (`UserID`) REFERENCES `users`(`Phone`) 
--   ON DELETE SET NULL ON UPDATE CASCADE;

-- ALTER TABLE `sepaudiotable` 
--   ADD CONSTRAINT `fk_sep_user` 
--   FOREIGN KEY (`UserID`) REFERENCES `users`(`Phone`) 
--   ON DELETE CASCADE ON UPDATE CASCADE;

-- ALTER TABLE `chattable` 
--   ADD CONSTRAINT `fk_chat_user` 
--   FOREIGN KEY (`UserID`) REFERENCES `users`(`Phone`) 
--   ON DELETE SET NULL ON UPDATE CASCADE;

-- ============================================
-- 6. 初始化数据（可选）
-- ============================================
-- 插入默认管理员账户（密码：123456）
INSERT INTO `users` (`Phone`, `UserName`, `Password`, `RegisterTime`, `Gender`, `Birthday`, `FaceImg`, `UserType`, `MaxSepTimes`, `CurSepTimes`, `MaxNoiseTimes`, `CurNoiseTimes`) 
VALUES 
('13685153598', 'SM', '123456', NOW(), '男', '1964-09-04', '/static/image/header.png', 1, 999999, 0, 999999, 0);

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================
-- 使用说明：
-- ============================================
-- 1. 创建数据库：
--    CREATE DATABASE IF NOT EXISTS `audio` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
--    USE `audio`;
--
-- 2. 执行本脚本：
--    source zy.sql;
--    或
--    mysql -u root -p audio < zy.sql;
--
-- 3. 验证表结构：
--    SHOW TABLES;
--    DESCRIBE users;
--    DESCRIBE denoisetable;
--    DESCRIBE sepaudiotable;
--    DESCRIBE chattable;
--
-- 4. 如果需要导入历史数据，请先执行本脚本创建表结构，
--    然后再导入 audio2.sql 和 chatgpt.sql 中的 INSERT 语句
-- ============================================

