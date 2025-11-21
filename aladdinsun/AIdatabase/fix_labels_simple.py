#!/usr/bin/env python3
import re

# 读取文件
with open('templates/predict_v2.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 定义需要修复的字段映射（label文本 -> field_id）
fields_to_fix = [
    (r'数据规模 \(GB\) \*', 'total_data_size_gb'),
    (r'表数量 \*', 'table_count'),
    (r'数据增长率 \(%/年\) \*', 'data_growth_rate'),
    (r'QPS \(每秒查询数\) \*', 'qps'),
    (r'TPS \(每秒事务数\) \*', 'tps'),
    (r'并发连接数 \*', 'concurrent_connections'),
    (r'行业类型', 'industry'),
    (r'预计上线时间', 'launch_date'),
    (r'预算范围 \(万元\)', 'budget'),
    (r'当前数据规模 \(GB\) \*', 'current_data_size_gb'),
    (r'预计3年后数据规模 \(GB\)', 'future_data_size_gb'),
    (r'数据库数量', 'database_count'),
    (r'单表最大记录数', 'max_table_rows'),
    (r'平均行大小 \(字节\)', 'avg_row_size'),
    (r'数据保留期限 \(年\)', 'data_retention_years'),
    (r'日常QPS', 'normal_qps'),
    (r'峰值QPS', 'peak_qps'),
    (r'日常TPS', 'normal_tps'),
    (r'峰值TPS', 'peak_tps'),
    (r'平均并发连接数 \*', 'avg_concurrent_connections'),
    (r'峰值并发连接数', 'peak_concurrent_connections'),
    (r'平均响应时间要求 \(ms\)', 'avg_response_time'),
    (r'P99响应时间要求 \(ms\)', 'p99_response_time'),
]

fixed_count = 0

for label_pattern, field_id in fields_to_fix:
    # 修复label的for属性
    label_regex = f'<label>{label_pattern}</label>'
    label_text = label_pattern.replace(r'\(', '(').replace(r'\)', ')').replace(r'\*', '*').replace(r'\\', '')
    new_label = f'<label for="{field_id}">{label_text}</label>'
    
    # 先检查是否存在
    if re.search(label_regex, content):
        content = re.sub(label_regex, new_label, content)
        fixed_count += 1
    
    # 为input添加id（如果name匹配且没有id）
    input_pattern = f'(name="{field_id}"(?! id))'
    if re.search(input_pattern, content):
        content = re.sub(input_pattern, f'name="{field_id}" id="{field_id}"', content)

print(f"✅ 修复了 {fixed_count} 个label标签")

# 写回文件
with open('templates/predict_v2.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 文件已保存")
