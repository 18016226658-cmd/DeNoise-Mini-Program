-- ============================================
-- 数据库迁移脚本：添加新字段（保留现有数据）- 兼容版本
-- ============================================
-- 说明：此脚本用于在现有数据库中添加新字段
--       - factor_count: 分解次数（因子数量）
--       - calc_desc: 计算说明（介绍算）
-- 使用方法：在 MySQL 中执行此脚本
-- 注意：此脚本会保留所有现有数据
-- 兼容性：支持 MySQL 5.6+ 版本
-- ============================================

USE `xqq`;

-- 添加 factor_count 字段（如果不存在）
-- 方法：先检查字段是否存在，如果不存在则添加
SET @exist := (
    SELECT COUNT(*) 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = DATABASE() 
    AND TABLE_NAME = 'histories' 
    AND COLUMN_NAME = 'factor_count'
);

SET @sqlstmt := IF(@exist = 0,
    'ALTER TABLE `histories` ADD COLUMN `factor_count` INT(11) DEFAULT NULL COMMENT ''分解次数（因子数量）'' AFTER `digit_count`',
    'SELECT ''字段 factor_count 已存在，跳过添加'' AS message'
);

PREPARE stmt FROM @sqlstmt;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 添加 calc_desc 字段（如果不存在）
SET @exist := (
    SELECT COUNT(*) 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = DATABASE() 
    AND TABLE_NAME = 'histories' 
    AND COLUMN_NAME = 'calc_desc'
);

SET @sqlstmt := IF(@exist = 0,
    'ALTER TABLE `histories` ADD COLUMN `calc_desc` TEXT DEFAULT NULL COMMENT ''计算说明（介绍算）'' AFTER `factor_count`',
    'SELECT ''字段 calc_desc 已存在，跳过添加'' AS message'
);

PREPARE stmt FROM @sqlstmt;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 更新已有数据的 factor_count
-- 方法：通过计算 factors JSON 字符串中的逗号数量来估算因子数量
-- 格式：["factor1","factor2","factor3"] -> 3个因子
UPDATE `histories`
SET `factor_count` = (
    CASE 
        WHEN `factors` IS NULL OR `factors` = '' OR `factors` = '[]' THEN 0
        WHEN `factors` LIKE '[%]' THEN 
            -- 计算 JSON 数组中的元素数量（通过逗号数量+1）
            (LENGTH(`factors`) - LENGTH(REPLACE(`factors`, ',', '')) + 1)
        ELSE NULL
    END
)
WHERE `factor_count` IS NULL 
  AND `factors` IS NOT NULL;

-- 对于 calc_desc 字段，已有记录保持为 NULL
-- 新记录会通过应用程序自动填充

-- ============================================
-- 迁移完成
-- ============================================
-- 已添加字段：
--   1. factor_count: 分解次数（因子数量）
--   2. calc_desc: 计算说明（介绍算）
-- 
-- 注意：
--   - 新字段已添加到现有表中，所有现有数据已保留
--   - 已有记录的 factor_count 已从 factors JSON 字段自动计算
--   - 已有记录的 calc_desc 保持为 NULL（新记录会自动填充）
--   - 兼容 MySQL 5.6+ 版本
-- ============================================


