# 测试数据生成说明

## 概述

为了进行可视化分析，需要生成足够多的测试用户和历史记录数据。本目录提供了两个SQL脚本用于自动生成测试数据。

## 文件说明

### 1. `generate_test_users.sql`
生成测试用户数据，包含：
- 60个基础测试用户（20个普通用户 + 20个VIP用户 + 20个SVIP用户）
- 不同性别、职业、年龄段的用户
- 存储过程 `generate_more_test_users()` 用于生成更多用户

### 2. `generate_test_histories.sql`
生成测试历史记录数据，包含：
- 最近30天的历史记录（默认每天5条）
- 不同时间段、数字位数、分解类型的数据
- 存储过程 `generate_test_histories()` 用于生成更多历史记录

## 使用方法

### 方法1：直接执行SQL脚本（推荐）

```bash
# 1. 生成测试用户
mysql -u root -p xqq < backend/generate_test_users.sql

# 2. 生成测试历史记录
mysql -u root -p xqq < backend/generate_test_histories.sql
```

### 方法2：在MySQL客户端中执行

```sql
-- 1. 连接到数据库
USE xqq;

-- 2. 执行用户生成脚本
source backend/generate_test_users.sql;

-- 3. 执行历史记录生成脚本
source backend/generate_test_histories.sql;
```

### 方法3：使用存储过程生成更多数据

```sql
-- 生成额外的100个用户
CALL generate_more_test_users(100);

-- 生成更多历史记录（最近60天，每天10条）
CALL generate_test_histories(60, 10);
```

## 生成的数据统计
                         
### 用户数据
- **总用户数**: 60个（基础）+ 可扩展
- **用户等级分布**:
  - 普通用户: 20个
  - VIP用户: 20个
  - SVIP用户: 20个
- **性别分布**: 男、女、其他
- **职业分布**: 学生、教师、工程师、医生、程序员、设计师、销售、经理、研究员、其他
- **年龄段分布**: 18岁以下、18-24岁、25-34岁、35-44岁、45-54岁、55岁以上

### 历史记录数据
- **总记录数**: 150条（基础：30天 × 5条/天）+ 可扩展
- **时间分布**: 最近30天，24小时均匀分布
- **数字位数**: 10-100位随机分布
- **分解类型**: 完全分解、部分分解、失败
- **数字类型**: 素数、合数、未知

## 验证数据生成

### 查看用户统计
```sql
-- 查看用户等级分布
SELECT 
    `level_name` AS '用户等级',
    COUNT(*) AS '用户数量'
FROM `users`
WHERE `username` LIKE 'test_user_%'
GROUP BY `level_name`;

-- 查看职业分布
SELECT 
    `job` AS '职业',
    COUNT(*) AS '用户数量'
FROM `users`
WHERE `username` LIKE 'test_user_%'
GROUP BY `job`
ORDER BY `用户数量` DESC;
```

### 查看历史记录统计
```sql
-- 查看每日使用统计
SELECT 
    DATE(`create_time`) AS '日期',
    COUNT(*) AS '记录数量'
FROM `histories`
WHERE `user_id` IN (SELECT `id` FROM `users` WHERE `username` LIKE 'test_user_%')
GROUP BY DATE(`create_time`)
ORDER BY `日期` DESC;

-- 查看各职业使用统计
SELECT 
    u.`job` AS '职业',
    COUNT(h.`id`) AS '使用次数'
FROM `histories` h
JOIN `users` u ON h.`user_id` = u.`id`
WHERE u.`username` LIKE 'test_user_%'
GROUP BY u.`job`
ORDER BY `使用次数` DESC;
```

## 清理测试数据

如果需要清理测试数据，可以执行：

```sql
-- 删除测试历史记录
DELETE FROM `histories` 
WHERE `user_id` IN (
    SELECT `id` FROM `users` WHERE `username` LIKE 'test_user_%'
);

-- 删除测试用户
DELETE FROM `users` WHERE `username` LIKE 'test_user_%';

-- 删除存储过程
DROP PROCEDURE IF EXISTS `generate_more_test_users`;
DROP PROCEDURE IF EXISTS `generate_test_histories`;
```

## 注意事项

1. **执行顺序**: 必须先执行 `generate_test_users.sql`，再执行 `generate_test_histories.sql`（因为历史记录需要关联用户）

2. **数据量**: 
   - 基础数据：60个用户 + 150条历史记录（足够进行基本可视化分析）
   - 如需更丰富的数据，可以使用存储过程生成更多数据

3. **性能**: 
   - 生成大量数据时可能需要一些时间
   - 建议分批生成，避免一次性生成过多数据

4. **测试用户密码**: 所有测试用户的密码都是 `123456`（仅用于测试）

5. **数据真实性**: 生成的数据是模拟数据，仅用于测试和可视化分析

## 可视化分析

生成测试数据后，可以在管理员页面使用以下可视化功能：

1. **职业使用时间分布**: 分析不同职业在一天24小时内的使用时间分布
2. **用户偏好分析**: 分析用户年龄、性别、职业、数字位数、分解类型等偏好
3. **使用统计**: 查看系统整体使用情况，包括用户数、使用次数、成功率等

## 示例：生成大量测试数据

如果需要生成大量数据用于更详细的可视化分析：

```sql
-- 1. 生成200个用户
CALL generate_more_test_users(200);

-- 2. 生成最近90天的历史记录，每天20条
CALL generate_test_histories(90, 20);

-- 这将生成：
-- - 260个用户（60基础 + 200新增）
-- - 1800条历史记录（90天 × 20条/天）
```

## 故障排除

### 问题1：存储过程不存在
**解决方案**: 确保已执行完整的SQL脚本，存储过程会在脚本中自动创建

### 问题2：外键约束错误
**解决方案**: 确保先删除历史记录，再删除用户，或者使用 `ON DELETE CASCADE` 自动删除

### 问题3：数据生成太慢
**解决方案**: 
- 减少每次生成的数据量
- 分批生成数据
- 检查数据库索引是否正常

## 联系支持

如有问题，请检查：
1. MySQL版本是否支持存储过程（需要5.7+）
2. 数据库连接是否正常
3. 用户权限是否足够

