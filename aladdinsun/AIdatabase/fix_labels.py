#!/usr/bin/env python3
"""
修复HTML中的label标签，为每个input添加id并关联label的for属性
"""

import re
from pathlib import Path

def fix_labels_in_file(filepath):
    """修复文件中的label标签"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 计数器，用于生成唯一ID
    id_counter = {}
    
    def generate_id(name):
        """根据name属性生成唯一ID"""
        if name not in id_counter:
            id_counter[name] = 0
        id_counter[name] += 1
        return f"{name}_{id_counter[name]}" if id_counter[name] > 1 else name
    
    # 匹配模式：<label>文本</label> 后面跟着 <input>（可能有换行）
    pattern = r'(<label>([^<]+)</label>\s*\n\s*<input\s+type="[^"]+"\s+name="([^"]+)")'
    
    def replacer(match):
        full_match = match.group(0)
        label_text = match.group(2)
        input_name = match.group(3)
        
        # 如果input已经有id，跳过
        if 'id=' in full_match:
            # 提取已有的id
            id_match = re.search(r'id="([^"]+)"', full_match)
            if id_match:
                field_id = id_match.group(1)
                # 只更新label的for属性
                return full_match.replace(
                    f'<label>{label_text}</label>',
                    f'<label for="{field_id}">{label_text}</label>'
                )
        
        # 生成新的ID
        field_id = generate_id(input_name)
        
        # 替换label和input
        new_label = f'<label for="{field_id}">{label_text}</label>'
        new_input = full_match.replace(
            f'<label>{label_text}</label>',
            new_label
        ).replace(
            f'name="{input_name}"',
            f'name="{input_name}" id="{field_id}"'
        )
        
        return new_input
    
    # 执行替换
    original_content = content
    content = re.sub(pattern, replacer, content)
    
    # 统计修复数量
    fixes = len(re.findall(pattern, original_content))
    
    # 写回文件
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 修复了 {fixes} 个label标签")
        return fixes
    else:
        print("⚠️  没有需要修复的label标签")
        return 0

if __name__ == '__main__':
    template_file = Path('templates/predict_v2.html')
    
    if template_file.exists():
        print(f"正在修复文件: {template_file}")
        fixed_count = fix_labels_in_file(template_file)
        print(f"\n总共修复: {fixed_count} 个label标签")
    else:
        print(f"错误: 文件不存在 {template_file}")
