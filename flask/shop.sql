/*
Navicat MySQL Data Transfer

Source Server         : monster
Source Server Version : 50722
Source Host           : localhost:3306
Source Database       : flask_shop

Target Server Type    : MYSQL
Target Server Version : 50722
File Encoding         : 65001

Date: 2019-09-26 17:50:13
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
INSERT INTO `alembic_version` VALUES ('e8e3482ac777');
COMMIT;

-- ----------------------------
-- Table structure for `carts`
-- ----------------------------
DROP TABLE IF EXISTS `carts`;
CREATE TABLE `carts` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`user_id`  int(11) NULL DEFAULT NULL ,
`good_id`  int(11) NULL DEFAULT NULL ,
PRIMARY KEY (`id`),
FOREIGN KEY (`good_id`) REFERENCES `goods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
INDEX `good_id` (`good_id`) USING BTREE ,
INDEX `user_id` (`user_id`) USING BTREE 
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=17

;

-- ----------------------------
-- Records of carts
-- ----------------------------
BEGIN;
INSERT INTO `carts` VALUES ('1', null, '1'), ('2', null, '1'), ('3', null, '1'), ('4', null, '2'), ('5', null, '2'), ('6', null, '1'), ('7', null, '2'), ('8', null, '1'), ('9', null, '2'), ('10', null, '19'), ('11', null, '1'), ('12', null, '6'), ('13', null, '9'), ('14', null, '6'), ('15', null, '1'), ('16', null, '12');
COMMIT;

-- ----------------------------
-- Table structure for `goods`
-- ----------------------------
DROP TABLE IF EXISTS `goods`;
CREATE TABLE `goods` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`name`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`avatar`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`description`  varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`price`  int(11) NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
AUTO_INCREMENT=31

;

-- ----------------------------
-- Records of goods
-- ----------------------------
BEGIN;
INSERT INTO `goods` VALUES ('1', '商品_0', '/static/img/1.jpg', '这是商品_0_的描述', '21'), ('2', '商品_1', '/static/img/3.jpg', '这是商品_1_的描述', '20'), ('3', '商品_2', '/static/img/5.jpg', '这是商品_2_的描述', '31'), ('4', '商品_3', '/static/img/5.jpg', '这是商品_3_的描述', '41'), ('5', '商品_4', '/static/img/1.jpg', '这是商品_4_的描述', '43'), ('6', '商品_5', '/static/img/1.jpg', '这是商品_5_的描述', '48'), ('7', '商品_6', '/static/img/8.jpg', '这是商品_6_的描述', '18'), ('8', '商品_7', '/static/img/7.jpg', '这是商品_7_的描述', '54'), ('9', '商品_8', '/static/img/1.jpg', '这是商品_8_的描述', '74'), ('10', '商品_9', '/static/img/3.jpg', '这是商品_9_的描述', '45'), ('11', '商品_10', '/static/img/4.jpg', '这是商品_10_的描述', '12'), ('12', '商品_11', '/static/img/4.jpg', '这是商品_11_的描述', '82'), ('13', '商品_12', '/static/img/7.jpg', '这是商品_12_的描述', '13'), ('14', '商品_13', '/static/img/3.jpg', '这是商品_13_的描述', '69'), ('15', '商品_14', '/static/img/3.jpg', '这是商品_14_的描述', '89'), ('16', '商品_15', '/static/img/5.jpg', '这是商品_15_的描述', '78'), ('17', '商品_16', '/static/img/8.jpg', '这是商品_16_的描述', '69'), ('18', '商品_17', '/static/img/5.jpg', '这是商品_17_的描述', '81'), ('19', '商品_18', '/static/img/0.jpg', '这是商品_18_的描述', '20'), ('20', '商品_19', '/static/img/8.jpg', '这是商品_19_的描述', '72'), ('21', '商品_20', '/static/img/1.jpg', '这是商品_20_的描述', '66'), ('22', '商品_21', '/static/img/0.jpg', '这是商品_21_的描述', '99'), ('23', '商品_22', '/static/img/0.jpg', '这是商品_22_的描述', '84'), ('24', '商品_23', '/static/img/2.jpg', '这是商品_23_的描述', '89'), ('25', '商品_24', '/static/img/1.jpg', '这是商品_24_的描述', '18'), ('26', '商品_25', '/static/img/5.jpg', '这是商品_25_的描述', '31'), ('27', '商品_26', '/static/img/1.jpg', '这是商品_26_的描述', '97'), ('28', '商品_27', '/static/img/2.jpg', '这是商品_27_的描述', '94'), ('29', '商品_28', '/static/img/1.jpg', '这是商品_28_的描述', '89'), ('30', '商品_29', '/static/img/5.jpg', '这是商品_29_的描述', '19');
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
AUTO_INCREMENT=3

;

-- ----------------------------
-- Records of users
-- ----------------------------
BEGIN;
INSERT INTO `users` VALUES ('1', 'test', '123'), ('2', 'test1', '123');
COMMIT;

-- ----------------------------
-- Auto increment value for `carts`
-- ----------------------------
ALTER TABLE `carts` AUTO_INCREMENT=17;

-- ----------------------------
-- Auto increment value for `goods`
-- ----------------------------
ALTER TABLE `goods` AUTO_INCREMENT=31;

-- ----------------------------
-- Auto increment value for `users`
-- ----------------------------
ALTER TABLE `users` AUTO_INCREMENT=3;
