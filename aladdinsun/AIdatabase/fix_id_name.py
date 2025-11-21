#!/usr/bin/env python3
import re

with open('templates/predict_v2.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 需要修复的映射: id -> name
fixes = {
    'xinchuan': 'enable_xinchuan',
    'table_count_2': 'table_count',
    'data_growth_rate_2': 'data_growth_rate',
    # ha_pro 已经在前面修复了，保持不变
    'sharding': 'need_sharding',
    'cache': 'need_cache',
    'mq': 'need_mq',
    'encryption': 'need_encryption',
    'audit': 'need_audit',
    'masking': 'need_masking',
    'xinchuan_pro': 'enable_xinchuan_pro',  # 专业模式用不同的name
    # xinchuan_mode_pro 已修复
    'monitoring': 'need_monitoring',
    'auto_scaling': 'need_auto_scaling',
    'support': 'need_24x7_support',
}

for old_id, correct_name in fixes.items():
    # 查找pattern: id="old_id" ... name="..."
    # 替换为: id="correct_name" ... name="correct_name"
    
    # Pattern 1: id before name
    pattern1 = rf'(id="{old_id}")([^>]*)(name="[^"]*")'
    def repl1(m):
        return f'id="{correct_name}"{m.group(2)}name="{correct_name}"'
    content = re.sub(pattern1, repl1, content)
    
    # Pattern 2: name before id
    pattern2 = rf'(name="[^"]*")([^>]*)(id="{old_id}")'
    def repl2(m):
        return f'name="{correct_name}"{m.group(2)}id="{correct_name}"'
    content = re.sub(pattern2, repl2, content)
    
    # 同时更新对应的 label for
    content = re.sub(rf'(label for=")({old_id})(")', rf'\1{correct_name}\3', content)

with open('templates/predict_v2.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 批量修复完成")
print(f"修复了 {len(fixes)} 个字段的 id 和 name")
