"""
数据库迁移脚本：添加新字段（保留现有数据）
自动添加 factor_count 和 calc_desc 字段，并更新已有数据
"""
import sys
import os
import json

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, History
from sqlalchemy import text

app = create_app()

def migrate_database():
    """执行数据库迁移"""
    with app.app_context():
        print('=' * 60)
        print('开始数据库迁移：添加新字段')
        print('=' * 60)
        print()
        
        try:
            # 1. 检查并添加 factor_count 字段
            print('1. 检查 factor_count 字段...')
            try:
                # 检查字段是否存在
                result = db.session.execute(text("""
                    SELECT COUNT(*) as count
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_SCHEMA = DATABASE()
                    AND TABLE_NAME = 'histories'
                    AND COLUMN_NAME = 'factor_count'
                """))
                exists = result.fetchone()[0] > 0
                
                if not exists:
                    print('   添加 factor_count 字段...')
                    db.session.execute(text("""
                        ALTER TABLE `histories` 
                        ADD COLUMN `factor_count` INT(11) DEFAULT NULL 
                        COMMENT '分解次数（因子数量）' 
                        AFTER `digit_count`
                    """))
                    db.session.commit()
                    print('   ✅ factor_count 字段添加成功')
                else:
                    print('   ℹ️  factor_count 字段已存在，跳过')
            except Exception as e:
                print(f'   ❌ 添加 factor_count 字段失败: {e}')
                db.session.rollback()
                return False
            
            # 2. 检查并添加 calc_desc 字段
            print('2. 检查 calc_desc 字段...')
            try:
                result = db.session.execute(text("""
                    SELECT COUNT(*) as count
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_SCHEMA = DATABASE()
                    AND TABLE_NAME = 'histories'
                    AND COLUMN_NAME = 'calc_desc'
                """))
                exists = result.fetchone()[0] > 0
                
                if not exists:
                    print('   添加 calc_desc 字段...')
                    db.session.execute(text("""
                        ALTER TABLE `histories` 
                        ADD COLUMN `calc_desc` TEXT DEFAULT NULL 
                        COMMENT '计算说明（介绍算）' 
                        AFTER `factor_count`
                    """))
                    db.session.commit()
                    print('   ✅ calc_desc 字段添加成功')
                else:
                    print('   ℹ️  calc_desc 字段已存在，跳过')
            except Exception as e:
                print(f'   ❌ 添加 calc_desc 字段失败: {e}')
                db.session.rollback()
                return False
            
            # 3. 更新已有数据的 factor_count
            print('3. 更新已有数据的 factor_count...')
            try:
                # 获取所有需要更新的记录
                histories = History.query.filter(
                    (History.factor_count.is_(None)) | (History.factor_count == 0)
                ).filter(History.factors.isnot(None)).all()
                
                updated_count = 0
                for history in histories:
                    try:
                        # 解析 factors JSON 字符串
                        if history.factors:
                            factors_list = json.loads(history.factors)
                            if isinstance(factors_list, list):
                                history.factor_count = len(factors_list)
                                updated_count += 1
                    except (json.JSONDecodeError, TypeError) as e:
                        # 如果 JSON 解析失败，尝试从字符串估算
                        if history.factors and history.factors.startswith('['):
                            # 简单估算：计算逗号数量
                            comma_count = history.factors.count(',')
                            if comma_count >= 0:
                                history.factor_count = comma_count + 1
                                updated_count += 1
                
                if updated_count > 0:
                    db.session.commit()
                    print(f'   ✅ 已更新 {updated_count} 条记录的 factor_count')
                else:
                    print('   ℹ️  没有需要更新的记录')
            except Exception as e:
                print(f'   ⚠️  更新 factor_count 时出错: {e}')
                db.session.rollback()
                # 不阻止迁移继续
            
            # 4. 对于 calc_desc，已有记录保持为 NULL（新记录会自动填充）
            print('4. calc_desc 字段说明...')
            print('   ℹ️  已有记录的 calc_desc 保持为 NULL')
            print('   ℹ️  新记录会通过应用程序自动填充')
            
            print()
            print('=' * 60)
            print('✅ 数据库迁移完成！')
            print('=' * 60)
            print()
            print('已添加字段：')
            print('  1. factor_count: 分解次数（因子数量）')
            print('  2. calc_desc: 计算说明（介绍算）')
            print()
            print('注意：')
            print('  - 所有现有数据已保留')
            print('  - 已有记录的 factor_count 已自动更新')
            print('  - 已有记录的 calc_desc 保持为 NULL（新记录会自动填充）')
            
            return True
            
        except Exception as e:
            print(f'❌ 迁移失败: {e}')
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == '__main__':
    try:
        success = migrate_database()
        if success:
            print('\n✅ 迁移成功完成！')
        else:
            print('\n❌ 迁移失败，请检查错误信息')
            sys.exit(1)
    except Exception as e:
        print(f'❌ 执行迁移时出错: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)


