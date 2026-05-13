/*
Navicat MySQL Data Transfer

Source Server         : sm
Source Server Version : 80026
Source Host           : localhost:3306
Source Database       : audio

Target Server Type    : MYSQL
Target Server Version : 80026
File Encoding         : 65001

Date: 2025-12-04 09:29:00
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `denoisetable`
-- ----------------------------
DROP TABLE IF EXISTS `denoisetable`;
CREATE TABLE `denoisetable` (
  `id` int NOT NULL AUTO_INCREMENT,
  `UserID` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'Phone',
  `UserName` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '用户昵称',
  `DeNoiseTime` datetime DEFAULT NULL COMMENT '降噪时间',
  `Gender` varchar(2) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '性别',
  `Birthday` date DEFAULT NULL COMMENT '出生年月',
  `AudioName` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '音频文件名称',
  `Extension` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '音频文件类型',
  `FileSize` double(10,2) DEFAULT NULL COMMENT '音频文件大小（Mb）',
  `Duration` double(10,2) DEFAULT NULL COMMENT '音频文件播放时长（秒数）',
  `N_channels` int DEFAULT NULL COMMENT '音频声道数',
  `BOrder` int DEFAULT NULL COMMENT '巴特沃斯滤波阶数',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=315 DEFAULT CHARSET=utf8mb3;

-- ----------------------------
-- Records of denoisetable
-- ----------------------------
INSERT INTO `denoisetable` VALUES ('1', '1001', '王小明', '2024-02-13 07:59:01', '男', '2001-10-11', '楼兰新娘\r\n楼兰新娘\r\n楼兰新娘', 'ogg', '11.82', '289.00', '2', '5');
INSERT INTO `denoisetable` VALUES ('2', '1001', '王小明', '2024-02-13 08:00:07', '男', '2001-10-11', null, null, null, null, null, null);
INSERT INTO `denoisetable` VALUES ('3', '1001', '王小明', '2024-02-13 08:01:34', '男', '2001-10-11', null, null, null, null, null, null);
INSERT INTO `denoisetable` VALUES ('4', '1001', '王小明', '2024-02-13 08:06:05', '男', '2001-10-11', null, null, null, null, null, null);
INSERT INTO `denoisetable` VALUES ('6', '1001', '王小明', '2024-02-13 08:07:26', '男', '2001-10-11', null, null, null, null, null, null);
INSERT INTO `denoisetable` VALUES ('7', '1001', '王小明', '2024-02-13 08:08:01', '男', '2001-10-11', null, null, null, null, null, null);
INSERT INTO `denoisetable` VALUES ('8', '1001', '王小明', '2024-02-13 08:08:49', '男', '2001-10-11', null, null, null, null, null, null);
INSERT INTO `denoisetable` VALUES ('9', '1001', '王小明', '2024-02-22 22:57:32', '男', '2001-10-11', null, null, null, null, null, null);
INSERT INTO `denoisetable` VALUES ('10', '1001', '王小明', '2024-02-22 23:02:05', '男', '2001-10-11', null, null, null, null, null, null);
INSERT INTO `denoisetable` VALUES ('11', '13685153598', 'SM', '2024-02-22 23:40:05', '男', '1964-09-04', null, null, null, null, null, null);
INSERT INTO `denoisetable` VALUES ('12', '18051094982', '苏梦', '2024-02-23 00:29:39', '女', '1999-09-09', null, null, null, null, null, null);
INSERT INTO `denoisetable` VALUES ('307', '13222222222', '李二', '2025-01-11 19:43:44', '女', '2002-10-10', '徐千雅 - 坐上火车去拉萨 (Live)', 'wav', '8.15', '48.42', '2', '5');
INSERT INTO `denoisetable` VALUES ('308', '13111111111', '许成浒', '2025-01-12 13:18:39', '女', '2002-09-08', '徐千雅 - 坐上火车去拉萨 (Live)', 'wav', '8.15', '48.42', '2', '5');
INSERT INTO `denoisetable` VALUES ('309', '13333333333', '张三', '2025-01-12 13:45:07', '男', '2000-10-10', '彩云之南', 'wav', '13.08', '77.78', '2', '5');
INSERT INTO `denoisetable` VALUES ('310', '13685153598', 'SM', '2025-10-16 20:18:29', '男', '1964-09-04', '不过人间 (Live)-海来阿木-short', 'wav', '3.32', '19.73', '2', '5');
INSERT INTO `denoisetable` VALUES ('311', '13685153598', 'SM', '2025-10-16 20:22:33', '男', '1964-09-04', '别知己-海来阿木-原歌曲', 'wav', '46.91', '278.82', '2', '5');
INSERT INTO `denoisetable` VALUES ('312', '13685153598', 'SM', '2025-10-16 20:23:27', '男', '1964-09-04', '别知己-海来阿木-原歌曲', 'wav', '46.91', '278.82', '2', '5');
INSERT INTO `denoisetable` VALUES ('313', '13685153598', 'SM', '2025-10-16 21:02:49', '男', '1964-09-04', '月亮代表我的心', 'wav', '35.43', '210.61', '2', '5');
INSERT INTO `denoisetable` VALUES ('314', '13685153598', 'SM', '2025-10-19 16:59:18', '男', '1964-09-04', '徐千雅 - 坐上火车去拉萨 ', 'wav', '3.12', '18.53', '2', '5');

-- ----------------------------
-- Table structure for `sepaudiotable`
-- ----------------------------
DROP TABLE IF EXISTS `sepaudiotable`;
CREATE TABLE `sepaudiotable` (
  `id` int NOT NULL AUTO_INCREMENT,
  `UserID` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'Phone',
  `UserName` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '用户昵称',
  `Gender` varchar(4) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '性别',
  `Birthday` date DEFAULT NULL COMMENT '出生年月',
  `SepTime` datetime DEFAULT NULL COMMENT '分离时间',
  `MxName` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '分离模型',
  `AudioName` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '音频文件名（歌曲名）',
  `Extension` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '音频文件类型（歌曲类型）',
  `FileSize` double(10,2) DEFAULT NULL COMMENT '音频文件大小（Mb）',
  `Duration` double(10,2) DEFAULT NULL COMMENT '音频播放时长（秒）',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8mb3;

-- ----------------------------
-- Records of sepaudiotable
-- ----------------------------
INSERT INTO `sepaudiotable` VALUES ('1', '1001', '王小明', '男', '2001-10-11', '2024-02-13 07:59:01', 'htdemucs', '楼兰新娘', 'ogg', '11.82', '289.00');
INSERT INTO `sepaudiotable` VALUES ('2', '1001', '王小明', '男', '2001-10-11', '2024-02-13 08:00:07', 'htdemucs', ' 我在苍山洱海等你-艾米尔', 'wav', '37.70', '302.00');
INSERT INTO `sepaudiotable` VALUES ('3', '1001', '王小明', '男', '2001-10-11', '2024-02-13 08:01:34', 'hdemucs_mmi', '杨卫英 - 云南洱海', 'mp3', '8.56', '288.00');
INSERT INTO `sepaudiotable` VALUES ('4', '1001', '王小明', '男', '2001-10-11', '2024-02-13 08:06:05', 'htdemucs_6s', '最美的情缘 (3D环绕版)-魏新雨', 'wav', '41.56', '298.00');
INSERT INTO `sepaudiotable` VALUES ('6', '1001', '王小明', '男', '2001-10-11', '2024-02-13 08:07:26', 'htdemucs_ft', '杨惟钧 - 洱海', 'mp3', '6.88', '302.00');
INSERT INTO `sepaudiotable` VALUES ('7', '1001', '王小明', '男', '2001-10-11', '2024-02-13 08:08:01', 'mdx', '最美的情缘-崔伟立', 'wav', '36.98', '279.00');
INSERT INTO `sepaudiotable` VALUES ('8', '1001', '王小明', '男', '2001-10-11', '2024-02-13 08:08:49', 'mdx_extra', '郭津彤 _ 汤晓菲 - 洱海故事', 'mp3', '7.87', '209.00');
INSERT INTO `sepaudiotable` VALUES ('9', '1001', '王小明', '男', '2001-10-11', '2024-02-22 22:57:32', 'mdx_extra_q', '李志华 - 洱海欢歌', 'mp3', '5.87', '306.00');
INSERT INTO `sepaudiotable` VALUES ('10', '1001', '王小明', '男', '2001-10-11', '2024-02-22 23:02:05', 'mdx_q', '洱海谣-家园计划', 'wav', '36.68', '288.00');
INSERT INTO `sepaudiotable` VALUES ('11', '13685153598', 'SM', '男', '1964-09-04', '2024-02-22 23:40:05', 'repro_mdx_a', '晓晴 - 望苍山观洱海', 'wav', '43.56', '304.00');
INSERT INTO `sepaudiotable` VALUES ('12', '18051094982', '苏梦', '女', '1999-09-09', '2024-02-23 00:29:39', 'repro_mdx_a_hybrid_only', '洱海有约-林琦', 'mp3', '6.78', '289.00');
INSERT INTO `sepaudiotable` VALUES ('307', '13222222222', '李二', '女', '2002-10-10', '2025-01-05 20:43:12', 'htdemucs', '蒋倩如 - 小河淌水', 'ogg', '5.85', '279.69');
INSERT INTO `sepaudiotable` VALUES ('308', '13222222222', '李二', '女', '2002-10-10', '2025-01-05 20:57:24', 'htdemucs', '蒋倩如 - 小河淌水', 'flac', '5.85', '279.69');
INSERT INTO `sepaudiotable` VALUES ('309', '13685153598', 'SM', '男', '1964-09-04', '2025-01-05 21:38:30', 'htdemucs', '李明翰 - 梦回云南', 'wav', '6.98', '296.01');
INSERT INTO `sepaudiotable` VALUES ('310', '13685153598', 'SM', '男', '1964-09-04', '2025-01-05 21:45:50', 'htdemucs', '群星 - 蝴蝶泉边', 'ogg', '8.85', '242.00');
INSERT INTO `sepaudiotable` VALUES ('311', '13685153598', 'SM', '男', '1964-09-04', '2025-01-05 23:03:55', 'htdemucs', '杜聪 - 茶歌', 'ogg', '3.09', '314.37');
INSERT INTO `sepaudiotable` VALUES ('312', '13685153598', 'SM', '男', '1964-09-04', '2025-01-05 23:10:19', 'htdemucs', '杜聪 - 茶歌', 'flac', '3.09', '314.37');
INSERT INTO `sepaudiotable` VALUES ('313', '13222222222', '李二', '女', '2002-10-10', '2025-01-05 23:25:51', 'htdemucs', '李明翰 - 梦回云南', 'ogg', '6.98', '296.01');
INSERT INTO `sepaudiotable` VALUES ('314', '13222222222', '李二', '女', '2002-10-10', '2025-01-06 15:03:58', 'htdemucs', '杜聪 - 茶歌', 'ogg', '3.09', '314.37');
INSERT INTO `sepaudiotable` VALUES ('315', '13222222222', '李二', '女', '2002-10-10', '2025-01-06 17:18:44', 'htdemucs', '蒋倩如 - 小河淌水', 'mp3', '5.85', '279.69');
INSERT INTO `sepaudiotable` VALUES ('316', '13222222222', '李二', '女', '2002-10-10', '2025-01-08 12:04:14', 'htdemucs', '华语群星 - 彩云之南', 'mp3', '11.82', '288.91');
INSERT INTO `sepaudiotable` VALUES ('317', '13222222222', '李二', '女', '2002-10-10', '2025-01-08 13:07:50', 'htdemucs', '华语群星 - 大理三月好风光', 'mp3', '2.70', '257.22');
INSERT INTO `sepaudiotable` VALUES ('318', '13222222222', '李二', '女', '2002-10-10', '2025-01-08 13:13:25', 'htdemucs', '华语群星 - 大理三月好风光', 'ogg', '2.70', '257.22');
INSERT INTO `sepaudiotable` VALUES ('319', '13222222222', '李二', '女', '2002-10-10', '2025-01-08 15:19:26', 'htdemucs', '李明翰 - 梦回云南', 'flac', '6.98', '296.01');
INSERT INTO `sepaudiotable` VALUES ('320', '13222222222', '李二', '女', '2002-10-10', '2025-01-08 16:01:35', 'htdemucs', '李明翰 - 梦回云南', 'ogg', '6.98', '296.01');
INSERT INTO `sepaudiotable` VALUES ('321', '13222222222', '李二', '女', '2002-10-10', '2025-01-08 18:24:13', 'htdemucs', '谭炎健 - 香格里拉', 'ogg', '10.66', '298.50');
INSERT INTO `sepaudiotable` VALUES ('322', '13222222222', '李二', '女', '2002-10-10', '2025-01-08 19:00:49', 'htdemucs', '华语群星 - 大理三月好风光', 'ogg', '2.70', '257.22');
INSERT INTO `sepaudiotable` VALUES ('323', '13222222222', '李二', '女', '2002-10-10', '2025-01-08 19:36:53', 'htdemucs', '丽江古城美-李红', 'wav', '51.74', '307.54');
INSERT INTO `sepaudiotable` VALUES ('324', '13222222222', '李二', '女', '2002-10-10', '2025-01-08 19:50:06', 'htdemucs', '群星 - 蝴蝶泉边', 'ogg', '8.85', '242.00');
INSERT INTO `sepaudiotable` VALUES ('325', '13222222222', '李二', '女', '2002-10-10', '2025-01-08 20:03:35', 'htdemucs', '谭炎健 - 香格里拉', 'ogg', '10.66', '298.50');
INSERT INTO `sepaudiotable` VALUES ('326', '13222222222', '李二', '女', '2002-10-10', '2025-01-08 20:19:21', 'htdemucs', '唐文娟 - 洱海情', 'flac', '11.35', '274.00');
INSERT INTO `sepaudiotable` VALUES ('327', '13222222222', '李二', '女', '2002-10-10', '2025-01-09 19:35:17', 'htdemucs', '谭炎健 - 香格里拉', 'ogg', '10.66', '298.50');
INSERT INTO `sepaudiotable` VALUES ('328', '13222222222', '李二', '女', '2002-10-10', '2025-01-09 20:32:50', 'htdemucs', '老黑 _ 司岗里阿妹 - 通撒美', 'ogg', '8.20', '228.87');
INSERT INTO `sepaudiotable` VALUES ('329', '13222222222', '李二', '女', '2002-10-10', '2025-01-09 20:51:06', 'htdemucs', '华语群星 - 彩云之南', 'flac', '11.82', '288.91');
INSERT INTO `sepaudiotable` VALUES ('330', '13222222222', '李二', '女', '2002-10-10', '2025-01-09 21:06:00', 'htdemucs', '谭炎健 - 香格里拉', 'ogg', '10.66', '298.50');
INSERT INTO `sepaudiotable` VALUES ('331', '13222222222', '李二', '女', '2002-10-10', '2025-01-09 21:35:03', 'htdemucs', '蒋倩如 - 小河淌水', 'ogg', '5.85', '279.69');
INSERT INTO `sepaudiotable` VALUES ('332', '13685153598', 'SM', '男', '1964-09-04', '2025-01-11 23:38:20', 'htdemucs', '徐千雅 - 坐上火车去拉萨 (Live)', 'ogg', '0.75', '48.43');
INSERT INTO `sepaudiotable` VALUES ('333', '13222222222', '李二', '女', '2002-10-10', '2025-01-11 23:46:08', 'htdemucs', '彩云之南', 'mp3', '1.19', '77.81');
INSERT INTO `sepaudiotable` VALUES ('334', '13111111111', '许成浒', '女', '2002-09-08', '2025-01-12 12:11:55', 'htdemucs', '彩云之南', 'mp3', '1.19', '77.81');
INSERT INTO `sepaudiotable` VALUES ('335', '13333333333', '张三', '男', '2000-10-10', '2025-01-12 13:36:09', 'htdemucs', '彩云之南', 'mp3', '1.19', '77.81');
INSERT INTO `sepaudiotable` VALUES ('336', '13333333333', '张三', '男', '2000-10-10', '2025-01-13 07:51:15', 'htdemucs', '阿鲁阿卓 - 情深谊长', 'flac', '27.24', '244.68');
INSERT INTO `sepaudiotable` VALUES ('337', '13333333333', '张三', '男', '2000-10-10', '2025-01-13 07:56:58', 'htdemucs', '白玛多吉 - 等你来云南', 'flac', '26.74', '235.59');
INSERT INTO `sepaudiotable` VALUES ('338', '13333333333', '张三', '男', '2000-10-10', '2025-01-17 11:24:12', 'htdemucs', '李明翰 - 梦回云南', 'ogg', '6.98', '296.01');
INSERT INTO `sepaudiotable` VALUES ('339', '13111111111', '许成浒', '女', '2002-09-08', '2025-01-18 19:56:59', 'htdemucs', '陈依梦 - 伤心的雪花 (温柔女声版)', 'ogg', '10.55', '267.68');
INSERT INTO `sepaudiotable` VALUES ('340', '13333333333', '张三', '男', '2000-10-10', '2025-01-19 14:06:30', 'htdemucs', '不过人间 (Live)-海来阿木', 'ac3', '0.46', '19.89');
INSERT INTO `sepaudiotable` VALUES ('341', '13333333333', '张三', '男', '2000-10-10', '2025-01-19 14:09:05', 'htdemucs', '点歌的人-海来阿木', 'mp3', '0.47', '31.01');
INSERT INTO `sepaudiotable` VALUES ('342', '13333333333', '张三', '男', '2000-10-10', '2025-01-19 14:15:26', 'htdemucs', '你的万水千山-海来阿木', 'ogg', '0.46', '29.69');
INSERT INTO `sepaudiotable` VALUES ('343', '13333333333', '张三', '男', '2000-10-10', '2025-01-19 14:17:34', 'htdemucs', '酒醉的蝴蝶-采薇薇', 'mp3', '0.63', '41.21');
INSERT INTO `sepaudiotable` VALUES ('344', '13111111111', '许成浒', '女', '2002-09-08', '2025-01-19 18:14:25', 'htdemucs', '彩云之南', 'ogg', '1.20', '77.81');
INSERT INTO `sepaudiotable` VALUES ('345', '13222222222', '李二', '女', '2002-10-10', '2025-01-19 19:21:19', 'htdemucs', '魏新雨 - 最美的情缘-魏新雨', 'ogg', '8.43', '245.22');
INSERT INTO `sepaudiotable` VALUES ('346', '13222222222', '李二', '女', '2002-10-10', '2025-01-19 19:24:44', 'htdemucs', 'Cruel Summer-Taylor Swift, 专辑名：Lover', 'ogg', '0.79', '51.07');
INSERT INTO `sepaudiotable` VALUES ('347', '13222222222', '李二', '女', '2002-10-10', '2025-01-23 21:13:06', 'htdemucs', '不过人间 (Live)-海来阿木', 'ogg', '0.31', '19.94');
INSERT INTO `sepaudiotable` VALUES ('348', '13111111111', '许成浒', '女', '2002-09-08', '2025-01-24 11:14:51', 'htdemucs', '不过人间 (Live)-海来阿木', 'ogg', '0.31', '19.94');
INSERT INTO `sepaudiotable` VALUES ('349', '13111111111', '许成浒', '女', '2002-09-08', '2025-01-24 12:12:04', 'htdemucs', '不过人间 (Live)-海来阿木', 'ogg', '0.31', '19.94');
INSERT INTO `sepaudiotable` VALUES ('350', '13333333333', '张三', '男', '2000-10-10', '2025-01-25 09:01:18', 'htdemucs', '梁祝', 'wav', '21.68', '128.86');

-- ----------------------------
-- Table structure for `users`
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `UserID` int NOT NULL AUTO_INCREMENT,
  `Phone` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `UserName` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Password` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `RegisterTime` datetime DEFAULT NULL,
  `Gender` varchar(2) DEFAULT NULL,
  `Birthday` date DEFAULT NULL,
  `FaceImg` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `UserType` int DEFAULT NULL,
  `MaxSepTimes` int DEFAULT NULL,
  `CurSepTimes` int DEFAULT NULL,
  `MaxNoiseTimes` int DEFAULT NULL,
  `CurNoiseTimes` int DEFAULT NULL,
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb3;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES ('1', '13685153598', 'SM', '123456', '2024-02-22 18:48:39', '男', '1964-09-04', '/static/image/header.png', '1', '999999', '0', '999999', '5');
INSERT INTO `users` VALUES ('32', '13555555555', '13555', '123456', '2024-03-05 20:11:19', '男', '2020-10-10', '/static/icon/FaceImg/ieP779eY2XF0505be85713f63d02bf38b8ceaf480c41.png', '2', '10', '0', '3', '2');
INSERT INTO `users` VALUES ('33', '13777777777', '137', '123456', '2024-03-07 07:50:43', '男', '1990-10-10', '/static/icon/FaceImg/96z5UApHjyr00ebcfcf3f7bfa03c17c4b9b03f60120b.png', '2', '10', '0', '3', '3');
INSERT INTO `users` VALUES ('34', '18888888888', '188', '123456', '2024-03-10 17:58:26', '男', '2000-10-10', '/static/icon/FaceImg/2T0Ud7xocAV76f6f1ff892d51a07102963a6cb5096ab.png', '2', '3', '0', '3', '0');
INSERT INTO `users` VALUES ('35', '13811111111', '张一', '123456', '2024-04-06 06:20:33', '女', '2005-09-08', '/static/icon/FaceImg/72KF7Z73ghU752a64f430b4aeb8a1071884dd0cd6531.png', '3', '3', '0', '3', null);
INSERT INTO `users` VALUES ('36', '13111111111', '许成浒', '123456', '2024-04-06 14:41:54', '女', '2002-09-08', '/static/icon/FaceImg/WEn2xlV696WFfbd59fe664f5f714307073bb3020dc02.png', '1', '999999', '0', '999999', '1');
INSERT INTO `users` VALUES ('40', '13333333333', '张三', '123456', '2024-04-12 09:13:15', '男', '2000-10-10', '/static/icon/FaceImg/FtPHe6hbjsVi0ebcfcf3f7bfa03c17c4b9b03f60120b.png', '3', '10', '0', '10', '10');
INSERT INTO `users` VALUES ('41', '13222222222', '李二', '123456', '2025-01-04 14:38:40', '女', '2002-10-10', '/static/image/ala.png', '2', '100', '0', '100', '4');
INSERT INTO `users` VALUES ('42', '13822222222', '张二', '123456', '2025-01-18 19:32:53', '男', '2003-10-01', '/static/icon/FaceImg/aoEN8c8CokFQ060051fdcee400ac2ee543160c6ddf4a.png', '2', '100', '0', '3', '0');
INSERT INTO `users` VALUES ('43', '13833333333', '张小三', '123456', '2025-01-18 19:35:43', '女', '2003-10-02', '/static/icon/FaceImg/MQJK0Jfh1JpCd846baa16dae4a4e2c4392e18df4297b.png', '3', '3', '0', '3', '0');
INSERT INTO `users` VALUES ('44', '13444444444', 'Lisi', '123456', '2024-02-22 19:12:36', '女', '1999-09-09', '/static/image/ala.png', '2', '10', '0', '10', '0');
INSERT INTO `users` VALUES ('45', '13999999998', '小明', '123456', '2024-02-26 12:11:37', '男', '2010-10-11', '/static/icon/FaceImg/TFGt6xy248mo104ac104b54b817a26d4ab55275f4e34.png', '3', '10', '0', '10', '0');

-- ----------------------------
-- Table structure for `users_copy1`
-- ----------------------------
DROP TABLE IF EXISTS `users_copy1`;
CREATE TABLE `users_copy1` (
  `UserID` int NOT NULL AUTO_INCREMENT,
  `Phone` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `UserName` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Password` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `RegisterTime` datetime DEFAULT NULL,
  `Gender` varchar(2) DEFAULT NULL,
  `Birthday` date DEFAULT NULL,
  `FaceImg` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `UserType` int DEFAULT NULL,
  `MaxSepTimes` int DEFAULT NULL,
  `CurSepTimes` int DEFAULT NULL,
  `MaxNoiseTimes` int DEFAULT NULL,
  `CurNoiseTimes` int DEFAULT NULL,
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb3;

-- ----------------------------
-- Records of users_copy1
-- ----------------------------
INSERT INTO `users_copy1` VALUES ('1', '13685153598', 'SM', '123456', '2024-02-22 18:48:39', '男', '1964-09-04', '/static/image/header.png', '1', '999999', '0', '999999', '0');
INSERT INTO `users_copy1` VALUES ('32', '13555555555', '13555', '123456', '2024-03-05 20:11:19', '男', '2020-10-10', '/static/icon/FaceImg/ieP779eY2XF0505be85713f63d02bf38b8ceaf480c41.png', '2', '10', '0', '3', '2');
INSERT INTO `users_copy1` VALUES ('33', '13777777777', '137', '123456', '2024-03-07 07:50:43', '男', '1990-10-10', '/static/icon/FaceImg/96z5UApHjyr00ebcfcf3f7bfa03c17c4b9b03f60120b.png', '2', '10', '0', '3', '3');
INSERT INTO `users_copy1` VALUES ('34', '18888888888', '188', '123456', '2024-03-10 17:58:26', '男', '2000-10-10', '/static/icon/FaceImg/2T0Ud7xocAV76f6f1ff892d51a07102963a6cb5096ab.png', '2', '3', '0', '3', '0');
INSERT INTO `users_copy1` VALUES ('35', '13811111111', '张一', '123456', '2024-04-06 06:20:33', '女', '2005-09-08', '/static/icon/FaceImg/72KF7Z73ghU752a64f430b4aeb8a1071884dd0cd6531.png', '3', '3', '0', '3', null);
INSERT INTO `users_copy1` VALUES ('36', '13111111111', '许成浒', '123456', '2024-04-06 14:41:54', '女', '2002-09-08', '/static/icon/FaceImg/WEn2xlV696WFfbd59fe664f5f714307073bb3020dc02.png', '1', '999999', '0', '999999', '1');
INSERT INTO `users_copy1` VALUES ('40', '13333333333', '张三', '123456', '2024-04-12 09:13:15', '男', '2000-10-10', '/static/icon/FaceImg/FtPHe6hbjsVi0ebcfcf3f7bfa03c17c4b9b03f60120b.png', '3', '10', '0', '10', '10');
INSERT INTO `users_copy1` VALUES ('41', '13222222222', '李二', '123456', '2025-01-04 14:38:40', '女', '2002-10-10', '/static/image/ala.png', '2', '100', '0', '100', '4');
INSERT INTO `users_copy1` VALUES ('42', '13822222222', '张二', '123456', '2025-01-18 19:32:53', '男', '2003-10-01', '/static/icon/FaceImg/aoEN8c8CokFQ060051fdcee400ac2ee543160c6ddf4a.png', '2', '100', '0', '3', '0');
INSERT INTO `users_copy1` VALUES ('43', '13833333333', '张小三', '123456', '2025-01-18 19:35:43', '女', '2003-10-02', '/static/icon/FaceImg/MQJK0Jfh1JpCd846baa16dae4a4e2c4392e18df4297b.png', '3', '3', '0', '3', '0');
INSERT INTO `users_copy1` VALUES ('44', '13444444444', 'Lisi', '123456', '2024-02-22 19:12:36', '女', '1999-09-09', '/static/image/ala.png', '2', '10', '0', '10', '0');
INSERT INTO `users_copy1` VALUES ('45', '13999999998', '小明', '123456', '2024-02-26 12:11:37', '男', '2010-10-11', '/static/icon/FaceImg/TFGt6xy248mo104ac104b54b817a26d4ab55275f4e34.png', '3', '10', '0', '10', '0');
