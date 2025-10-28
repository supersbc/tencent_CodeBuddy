"""
创建测试数据模板（Excel格式）
用于演示智能识别功能
"""

import pandas as pd

# 创建测试数据
data = {
    '参数名称': [
        '数据总量',
        '表数量',
        '数据库数量',
        'QPS',
        'TPS',
        '并发连接数',
        '数据增长率',
        '高可用',
        '容灾',
        '读写分离'
    ],
    '参数值': [
        '8640.87 GB',
        '150',
        '8',
        '50000',
        '20000',
        '5000',
        '30%',
        '是',
        '是',
        '是'
    ],
    '说明': [
        '当前数据库总数据量',
        '所有表的总数',
        '数据库实例数量',
        '每秒查询次数',
        '每秒事务数',
        '最大并发连接数',
        '年数据增长率',
        '是否需要高可用部署',
        '是否需要容灾备份',
        '是否需要读写分离'
    ]
}

# 创建DataFrame
df = pd.DataFrame(data)

# 保存为Excel
excel_file = 'database_migration_template.xlsx'
df.to_excel(excel_file, index=False, sheet_name='数据库参数')

print(f"✅ 测试模板已创建: {excel_file}")
print("\n模板内容:")
print(df.to_string(index=False))

# 创建案例提交模板
case_data = {
    '输入参数': [
        '数据总量 (GB)',
        'QPS',
        '表数量',
        '并发连接数'
    ],
    '参数值': [
        '10000',
        '80000',
        '200',
        '8000'
    ],
    '实际架构': [
        '架构类型',
        '节点数量',
        '分片数量',
        '副本数量'
    ],
    '架构值': [
        'distributed',
        '8',
        '4',
        '2'
    ]
}

case_df = pd.DataFrame(case_data)
case_file = 'case_submission_template.xlsx'
case_df.to_excel(case_file, index=False, sheet_name='实际案例')

print(f"\n✅ 案例模板已创建: {case_file}")
print("\n案例模板内容:")
print(case_df.to_string(index=False))
