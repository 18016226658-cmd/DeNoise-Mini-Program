# 真实数据生成说明

## 概述

本目录提供了生成真实测试数据的Python脚本，用于为系统生成500个用户和相应的历史记录数据。

## 文件说明

### 1. `generate_real_users.py`
生成500个真实用户数据，包含：
- 300个普通用户（最大分解50位）
- 150个VIP用户（最大分解80位）
- 49个SVIP用户（最大分解120位）
- 1个管理员（xqq，最大分解200位）

每个用户包含：
- 随机性别、职业、出生日期
- 随机注册时间（过去1年内）
- 随机登录次数（1-100次）

### 2. `generate_real_histories.py`
为每个用户生成10-20条历史记录，使用真实的分解算法：
- 根据用户等级限制生成相应位数的数字
- 使用真实的Pollard's Rho算法进行分解
- 生成真实的分解结果、耗时、数字类型等信息
- 随机生成时间（过去90天内）

### 3. `generate_all_real_data.py`
一键生成所有数据的主脚本，按顺序执行：
1. 生成500个用户
2. 为每个用户生成10-20条历史记录

## 使用方法

### 方法1：一键生成（推荐）

```bash
cd backend
python generate_all_real_data.py
```

### 方法2：分步生成

```bash
cd backend

# 步骤1：生成用户
python generate_real_users.py

# 步骤2：生成历史记录（需要较长时间）
python generate_real_histories.py
```

## 数据库配置

脚本使用以下数据库配置（在 `config.py` 中设置）：
- 数据库名：`xqq`
- 用户名：`root`
- 密码：`123456`
- 主机：`localhost`
- 端口：`3306`

如需修改，请编辑 `backend/config.py` 文件。

## 生成的数据量

- **用户数量**：500个（不包括管理员xqq）
- **历史记录数量**：约5000-10000条（每个用户10-20条）
- **生成时间**：根据数字大小，可能需要10-30分钟

## 注意事项

1. **执行时间**：生成历史记录需要使用真实算法进行分解计算，可能需要较长时间，请耐心等待。

2. **数据覆盖**：
   - 如果数据库中已有用户（除管理员外），脚本会跳过生成
   - 如果数据库中已有历史记录，脚本会继续添加新记录

3. **内存使用**：脚本采用批量提交策略（每100条记录提交一次），避免内存占用过大。

4. **错误处理**：如果某条记录生成失败，脚本会继续处理下一条，不会中断整个流程。

## 验证数据

生成完成后，可以执行以下SQL查询验证数据：

```sql
-- 查看用户统计
SELECT 
    level_name AS '用户等级',
    COUNT(*) AS '用户数量'
FROM users
WHERE username != 'xqq'
GROUP BY level_name;

-- 查看历史记录统计
SELECT 
    COUNT(*) AS '总记录数',
    COUNT(DISTINCT user_id) AS '用户数',
    AVG(elapsed_time) AS '平均耗时(秒)',
    COUNT(CASE WHEN factorization_level = 'complete' THEN 1 END) AS '完全分解',
    COUNT(CASE WHEN factorization_level = 'partial' THEN 1 END) AS '部分分解'
FROM histories;

-- 查看各等级用户的记录数
SELECT 
    u.level_name AS '用户等级',
    COUNT(h.id) AS '记录数',
    AVG(h.elapsed_time) AS '平均耗时(秒)'
FROM users u
LEFT JOIN histories h ON u.id = h.user_id
WHERE u.username != 'xqq'
GROUP BY u.level_name;
```

## 清理数据

如果需要清理生成的数据：

```sql
-- 删除所有历史记录
DELETE FROM histories WHERE user_id IN (
    SELECT id FROM users WHERE username != 'xqq'
);

-- 删除所有测试用户
DELETE FROM users WHERE username != 'xqq';
```

## 故障排除

### 问题1：数据库连接失败
**解决方案**：
- 检查MySQL服务是否运行
- 检查 `config.py` 中的数据库配置是否正确
- 检查数据库 `xqq` 是否已创建

### 问题2：生成时间过长
**解决方案**：
- 这是正常现象，因为需要使用真实算法进行分解
- 可以分批生成，先生成用户，再生成部分用户的历史记录

### 问题3：内存不足
**解决方案**：
- 脚本已采用批量提交策略，如果仍有问题，可以减少每批的数量
- 修改 `generate_real_histories.py` 中的批量提交数量（默认100）

## 联系支持

如有问题，请检查：
1. Python版本是否3.8+
2. 依赖包是否已安装（`pip install -r requirements.txt`）
3. MySQL数据库是否正常运行
4. 数据库连接配置是否正确

