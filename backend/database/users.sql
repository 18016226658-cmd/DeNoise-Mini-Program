/*
 Navicat Premium Data Transfer

 Source Server         : sm
 Source Server Type    : MySQL
 Source Server Version : 80026
 Source Host           : localhost:3306
 Source Schema         : chatgpt

 Target Server Type    : MySQL
 Target Server Version : 80026
 File Encoding         : 65001

 Date: 08/10/2024 20:48:19
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `UserID` int(0) NOT NULL AUTO_INCREMENT,
  `Phone` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `UserName` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Password` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `RegisterTime` datetime(0) NULL DEFAULT NULL,
  `Gender` varchar(2) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `Birthday` date NULL DEFAULT NULL,
  `FaceImg` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `UserType` int(0) NULL DEFAULT NULL,
  PRIMARY KEY (`UserID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 41 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, '13685153598', 'SM', '123456', '2024-02-22 18:48:39', '男', '1964-09-04', '/static/image/header.png', 1);
INSERT INTO `users` VALUES (2, '13444444444', 'Lisi', '123456', '2024-02-22 19:12:36', '女', '1999-09-09', '/static/image/ala.png', 2);
INSERT INTO `users` VALUES (30, '13999999998', '小明', '123456', '2024-02-26 12:11:37', '男', '2010-10-11', '/static/icon/FaceImg/TFGt6xy248mo104ac104b54b817a26d4ab55275f4e34.png', 3);
INSERT INTO `users` VALUES (32, '13555555555', '13555', '123456', '2024-03-05 20:11:19', '男', '2020-10-10', '/static/icon/FaceImg/ieP779eY2XF0505be85713f63d02bf38b8ceaf480c41.png', 3);
INSERT INTO `users` VALUES (33, '13777777777', '137', '123456', '2024-03-07 07:50:43', '男', '1990-10-10', '/static/icon/FaceImg/96z5UApHjyr00ebcfcf3f7bfa03c17c4b9b03f60120b.png', 3);
INSERT INTO `users` VALUES (34, '18888888888', '188', '123456', '2024-03-10 17:58:26', '男', '2000-10-10', '/static/icon/FaceImg/2T0Ud7xocAV76f6f1ff892d51a07102963a6cb5096ab.png', 3);
INSERT INTO `users` VALUES (35, '13811111111', '张一', '123456', '2024-04-06 06:20:33', '女', '2005-09-08', '/static/icon/FaceImg/72KF7Z73ghU752a64f430b4aeb8a1071884dd0cd6531.png', 3);
INSERT INTO `users` VALUES (36, '15111111111', '钟佳妮', '123456', '2024-04-06 14:41:54', '女', '2002-09-08', '/static/icon/FaceImg/WEn2xlV696WFfbd59fe664f5f714307073bb3020dc02.png', 1);
INSERT INTO `users` VALUES (40, '13333333333', '张三', '123456', '2024-04-12 09:13:15', '男', '2000-10-10', '/static/icon/FaceImg/FtPHe6hbjsVi0ebcfcf3f7bfa03c17c4b9b03f60120b.png', 2);

SET FOREIGN_KEY_CHECKS = 1;
