#!/usr/bin/env python3
"""
验证所有预置模型库文件的完整性和格式
"""

import json
import os
from pathlib import Path

def verify_model_libraries():
    """验证所有模型库文件"""
    
    libraries_dir = Path('model_libraries')
    
    # 预期的模型库文件
    expected_libraries = {
        'tencent_official_v2.1.0.json': {
            'name': '腾讯云官方模型库',
            'min_cases': 5,
            'source': 'tencent_cloud_official'
        },
        'community_finance_v1.8.3.json': {
            'name': '金融行业社区模型库',
            'min_cases': 5,
            'source': 'community_finance'
        },
        'community_ecommerce_v1.5.2.json': {
            'name': '电商行业社区模型库',
            'min_cases': 5,
            'source': 'community_ecommerce'
        },
        'community_gaming_v1.3.1.json': {
            'name': '游戏行业社区模型库',
            'min_cases': 5,
            'source': 'community_gaming'
        },
        'github_opensource_v2.0.5.json': {
            'name': 'GitHub开源模型库',
            'min_cases': 5,
            'source': 'github_opensource'
        },
        'huggingface_v1.2.0.json': {
            'name': 'HuggingFace模型库',
            'min_cases': 5,
            'source': 'huggingface_models'
        },
        'kaggle_winner_v1.0.8.json': {
            'name': 'Kaggle竞赛模型库',
            'min_cases': 5,
            'source': 'kaggle_competition'
        },
        'alibaba_cloud_v1.6.2.json': {
            'name': '阿里云模型库',
            'min_cases': 5,
            'source': 'alibaba_cloud'
        }
    }
    
    print("=" * 80)
    print("🔍 开始验证预置模型库...")
    print("=" * 80)
    print()
    
    total_cases = 0
    verified_count = 0
    error_count = 0
    
    for filename, info in expected_libraries.items():
        filepath = libraries_dir / filename
        
        print(f"📦 验证: {info['name']}")
        print(f"   文件: {filename}")
        
        # 检查文件是否存在
        if not filepath.exists():
            print(f"   ❌ 错误: 文件不存在")
            error_count += 1
            print()
            continue
        
        # 检查文件大小
        file_size = filepath.stat().st_size
        print(f"   📊 大小: {file_size / 1024:.2f} KB")
        
        # 读取并验证JSON格式
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                print(f"   ❌ 错误: 数据格式不是列表")
                error_count += 1
                print()
                continue
            
            case_count = len(data)
            print(f"   📈 案例数: {case_count}")
            
            if case_count < info['min_cases']:
                print(f"   ⚠️  警告: 案例数少于预期 ({info['min_cases']})")
            
            # 验证每个案例的结构
            valid_cases = 0
            for i, case in enumerate(data):
                if not isinstance(case, dict):
                    print(f"   ❌ 案例 {i+1}: 不是字典格式")
                    continue
                
                # 检查必需字段
                required_fields = ['id', 'source', 'timestamp', 'input', 'output', 'metadata']
                missing_fields = [f for f in required_fields if f not in case]
                
                if missing_fields:
                    print(f"   ❌ 案例 {i+1}: 缺少字段 {missing_fields}")
                    continue
                
                # 验证source字段
                if case.get('source') != info['source']:
                    print(f"   ⚠️  案例 {i+1}: source字段不匹配 (期望: {info['source']}, 实际: {case.get('source')})")
                
                valid_cases += 1
            
            print(f"   ✅ 有效案例: {valid_cases}/{case_count}")
            
            if valid_cases == case_count:
                print(f"   ✅ 验证通过")
                verified_count += 1
                total_cases += case_count
            else:
                print(f"   ⚠️  部分案例有问题")
                error_count += 1
            
        except json.JSONDecodeError as e:
            print(f"   ❌ JSON解析错误: {e}")
            error_count += 1
        except Exception as e:
            print(f"   ❌ 未知错误: {e}")
            error_count += 1
        
        print()
    
    # 总结
    print("=" * 80)
    print("📊 验证总结")
    print("=" * 80)
    print(f"✅ 验证通过: {verified_count}/{len(expected_libraries)} 个模型库")
    print(f"❌ 验证失败: {error_count} 个")
    print(f"📈 总案例数: {total_cases}")
    print()
    
    if error_count == 0:
        print("🎉 所有模型库验证通过！")
        return True
    else:
        print("⚠️  部分模型库存在问题，请检查")
        return False

if __name__ == '__main__':
    success = verify_model_libraries()
    exit(0 if success else 1)
