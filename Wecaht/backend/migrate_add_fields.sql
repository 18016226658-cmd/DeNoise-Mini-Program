-- ============================================
-- 数据库迁移脚本：添加新字段（保留现有数据）
-- ============================================
-- 说明：此脚本用于在现有数据库中添加新字段
--       - factor_count: 分解次数（因子数量）
--       - calc_desc: 计算说明（介绍算）
-- 使用方法：在 MySQL 中执行此脚本
-- 注意：此脚本会保留所有现有数据
-- ============================================

USE `xqq`;

-- 检查并添加 factor_count 字段（如果不存在）
SET @dbname = DATABASE();
SET @tablename = 'histories';
SET @columnname = 'factor_count';
SET @preparedStatement = (SELECT IF(
  (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE
      (TABLE_SCHEMA = @dbname)
      AND (TABLE_NAME = @tablename)
      AND (COLUMN_NAME = @columnname)
  ) > 0,
  'SELECT 1',  -- 字段已存在，不执行任何操作
  CONCAT('ALTER TABLE `', @tablename, '` ADD COLUMN `', @columnname, '` INT(11) DEFAULT NULL COMMENT ''分解次数（因子数量）'' AFTER `digit_count`')
));
PREPARE alterIfNotExists FROM @preparedStatement;
EXECUTE alterIfNotExists;
DEALLOCATE PREPARE alterIfNotExists;

-- 检查并添加 calc_desc 字段（如果不存在）
SET @columnname = 'calc_desc';
SET @preparedStatement = (SELECT IF(
  (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE
      (TABLE_SCHEMA = @dbname)
      AND (TABLE_NAME = @tablename)
      AND (COLUMN_NAME = @columnname)
  ) > 0,
  'SELECT 1',  -- 字段已存在，不执行任何操作
  CONCAT('ALTER TABLE `', @tablename, '` ADD COLUMN `', @columnname, '` TEXT DEFAULT NULL COMMENT ''计算说明（介绍算）'' AFTER `factor_count`')
));
PREPARE alterIfNotExists FROM @preparedStatement;
EXECUTE alterIfNotExists;
DEALLOCATE PREPARE alterIfNotExists;

-- 更新已有数据的 factor_count（从 factors JSON 字段计算）
-- 注意：MySQL 5.7+ 支持 JSON 函数，如果版本较低可能需要调整
UPDATE `histories`
SET `factor_count` = (
  SELECT COUNT(*) 
  FROM JSON_TABLE(
    `factors`,
    '$[*]' COLUMNS (value TEXT PATH '$')
  ) AS jt
)
WHERE `factor_count` IS NULL 
  AND `factors` IS NOT NULL 
  AND `factors` != ''
  AND JSON_VALID(`factors`);

-- 如果上面的 JSON_TABLE 不支持（MySQL 5.6 或更早版本），可以使用以下方法：
-- 通过计算 factors JSON 字符串中的元素数量来估算
-- UPDATE `histories`
-- SET `factor_count` = (
--   (LENGTH(`factors`) - LENGTH(REPLACE(`factors`, ',', '')) + 1)
-- )
-- WHERE `factor_count` IS NULL 
--   AND `factors` IS NOT NULL 
--   AND `factors` != ''
--   AND `factors` LIKE '[%]';

-- 对于无法自动计算 factor_count 的记录，设置为 NULL（已允许）
-- calc_desc 字段暂时保持为 NULL，后续新记录会自动填充

-- ============================================
-- 迁移完成
-- ============================================
-- 已添加字段：
--   1. factor_count: 分解次数（因子数量）
--   2. calc_desc: 计算说明（介绍算）
-- 
-- 注意：
--   - 新字段已添加到现有表中，所有现有数据已保留
--   - 已有记录的 factor_count 已尝试从 factors JSON 字段自动计算
--   - 已有记录的 calc_desc 保持为 NULL（新记录会自动填充）
--   - 如果 MySQL 版本 < 5.7，JSON_TABLE 可能不支持，需要手动调整更新语句
-- ============================================


