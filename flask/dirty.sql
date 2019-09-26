/*
Navicat MySQL Data Transfer

Source Server         : monster
Source Server Version : 50722
Source Host           : localhost:3306
Source Database       : flask_dirty

Target Server Type    : MYSQL
Target Server Version : 50722
File Encoding         : 65001

Date: 2019-09-26 17:49:00
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `alembic_version`
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
`version_num`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
PRIMARY KEY (`version_num`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci

;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
BEGIN;
INSERT INTO `alembic_version` VALUES ('7b06b0e7544d');
COMMIT;

-- ----------------------------
-- Table structure for `bods`
-- ----------------------------
DROP TABLE IF EXISTS `bods`;
CREATE TABLE `bods` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`time`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`data`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`remark`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=21

;

-- ----------------------------
-- Records of bods
-- ----------------------------
BEGIN;
INSERT INTO `bods` VALUES ('1', '190500', '18.44', 'ok'), ('2', '190501', '49.18', 'ok'), ('3', '190502', '12.05', 'ok'), ('4', '190503', '14.67', 'ok'), ('5', '190504', '44.29', 'ok'), ('6', '190505', '31.68', 'ok'), ('7', '190506', '16.98', 'ok'), ('8', '190507', '17.34', 'ok'), ('9', '190508', '38.08', 'ok'), ('10', '190509', '26.53', 'ok'), ('11', '190510', '21.22', 'ok'), ('12', '190511', '48.46', 'ok'), ('13', '190512', '12.38', 'ok'), ('14', '190513', '21.88', 'ok'), ('15', '190514', '21.9', 'ok'), ('16', '190515', '13.46', 'ok'), ('17', '190516', '18.83', 'ok'), ('18', '190517', '32.78', 'ok'), ('19', '190518', '39.18', 'ok'), ('20', '190519', '38.35', 'ok');
COMMIT;

-- ----------------------------
-- Table structure for `cctvs`
-- ----------------------------
DROP TABLE IF EXISTS `cctvs`;
CREATE TABLE `cctvs` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`name`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`avatar`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`port`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=25

;

-- ----------------------------
-- Records of cctvs
-- ----------------------------
BEGIN;
INSERT INTO `cctvs` VALUES ('1', 'cctv', '/static/img/0.jpg', '98'), ('2', 'cctv', '/static/img/3.jpg', '12'), ('3', 'cctv', '/static/img/1.jpg', '39'), ('4', 'cctv', '/static/img/1.jpg', '96'), ('5', 'cctv', '/static/img/4.jpg', '0'), ('6', 'cctv', '/static/img/1.jpg', '83'), ('7', 'cctv', '/static/img/4.jpg', '37'), ('8', 'cctv', '/static/img/1.jpg', '72'), ('9', 'cctv', '/static/img/0.jpg', '84'), ('10', 'cctv', '/static/img/0.jpg', '12'), ('11', 'cctv', '/static/img/4.jpg', '17'), ('12', 'cctv', '/static/img/4.jpg', '88'), ('13', 'cctv', '/static/img/1.jpg', '29'), ('14', 'cctv', '/static/img/2.jpg', '88'), ('15', 'cctv', '/static/img/0.jpg', '2'), ('16', 'cctv', '/static/img/2.jpg', '42'), ('17', 'cctv', '/static/img/1.jpg', '79'), ('18', 'cctv', '/static/img/3.jpg', '67'), ('19', 'cctv', '/static/img/4.jpg', '55'), ('20', 'cctv', '/static/img/2.jpg', '59'), ('21', 'cctv', '/static/img/0.jpg', '25'), ('22', 'cctv', '/static/img/2.jpg', '72'), ('23', 'cctv', '/static/img/4.jpg', '61'), ('24', 'cctv', '/static/img/3.jpg', '62');
COMMIT;

-- ----------------------------
-- Table structure for `cods`
-- ----------------------------
DROP TABLE IF EXISTS `cods`;
CREATE TABLE `cods` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`time`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`data`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`remark`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=21

;

-- ----------------------------
-- Records of cods
-- ----------------------------
BEGIN;
INSERT INTO `cods` VALUES ('1', '190500', '40.71', 'ok'), ('2', '190501', '47.38', 'ok'), ('3', '190502', '46.9', 'ok'), ('4', '190503', '42.92', 'ok'), ('5', '190504', '44.97', 'ok'), ('6', '190505', '47.67', 'ok'), ('7', '190506', '40.27', 'ok'), ('8', '190507', '48.98', 'ok'), ('9', '190508', '46.86', 'ok'), ('10', '190509', '49.06', 'ok'), ('11', '190510', '46.92', 'ok'), ('12', '190511', '44.09', 'ok'), ('13', '190512', '44.39', 'ok'), ('14', '190513', '47.32', 'ok'), ('15', '190514', '49.91', 'ok'), ('16', '190515', '40.18', 'ok'), ('17', '190516', '47.69', 'ok'), ('18', '190517', '49.52', 'ok'), ('19', '190518', '44.51', 'ok'), ('20', '190519', '45.97', 'ok');
COMMIT;

-- ----------------------------
-- Table structure for `phs`
-- ----------------------------
DROP TABLE IF EXISTS `phs`;
CREATE TABLE `phs` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`time`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`data`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`remark`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=21

;

-- ----------------------------
-- Records of phs
-- ----------------------------
BEGIN;
INSERT INTO `phs` VALUES ('1', '190500', '6.61', 'ok'), ('2', '190501', '6.11', 'ok'), ('3', '190502', '6.4', 'ok'), ('4', '190503', '6.74', 'ok'), ('5', '190504', '6.87', 'ok'), ('6', '190505', '6.06', 'ok'), ('7', '190506', '6.77', 'ok'), ('8', '190507', '6.03', 'ok'), ('9', '190508', '6.93', 'ok'), ('10', '190509', '6.76', 'ok'), ('11', '190510', '6.22', 'ok'), ('12', '190511', '6.79', 'ok'), ('13', '190512', '6.56', 'ok'), ('14', '190513', '6.68', 'ok'), ('15', '190514', '6.15', 'ok'), ('16', '190515', '7', 'ok'), ('17', '190516', '6.73', 'ok'), ('18', '190517', '6', 'ok'), ('19', '190518', '6.53', 'ok'), ('20', '190519', '6.25', 'ok');
COMMIT;

-- ----------------------------
-- Table structure for `rcpts`
-- ----------------------------
DROP TABLE IF EXISTS `rcpts`;
CREATE TABLE `rcpts` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`name`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`number`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`email`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=5

;

-- ----------------------------
-- Records of rcpts
-- ----------------------------
BEGIN;
INSERT INTO `rcpts` VALUES ('1', '张0', '54813633240', '139500857@qq.com'), ('2', '张1', '35787050519', '261330643@qq.com'), ('3', '张2', '56045532899', '829296766@qq.com'), ('4', '张3', '42849569049', '775083445@qq.com');
COMMIT;

-- ----------------------------
-- Table structure for `users`
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`name`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`password`  varchar(120) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`),
UNIQUE INDEX `name` (`name`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=2

;

-- ----------------------------
-- Records of users
-- ----------------------------
BEGIN;
INSERT INTO `users` VALUES ('1', 'test', '123');
COMMIT;

-- ----------------------------
-- Auto increment value for `bods`
-- ----------------------------
ALTER TABLE `bods` AUTO_INCREMENT=21;

-- ----------------------------
-- Auto increment value for `cctvs`
-- ----------------------------
ALTER TABLE `cctvs` AUTO_INCREMENT=25;

-- ----------------------------
-- Auto increment value for `cods`
-- ----------------------------
ALTER TABLE `cods` AUTO_INCREMENT=21;

-- ----------------------------
-- Auto increment value for `phs`
-- ----------------------------
ALTER TABLE `phs` AUTO_INCREMENT=21;

-- ----------------------------
-- Auto increment value for `rcpts`
-- ----------------------------
ALTER TABLE `rcpts` AUTO_INCREMENT=5;

-- ----------------------------
-- Auto increment value for `users`
-- ----------------------------
ALTER TABLE `users` AUTO_INCREMENT=2;
