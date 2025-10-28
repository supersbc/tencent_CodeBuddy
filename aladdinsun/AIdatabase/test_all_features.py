#!/usr/bin/env python3
"""测试所有功能模块"""

import requests
import json
import time

print("=" * 70)
print("🧪 TDSQL部署资源预测系统 v4.2 - 完整功能测试")
print("=" * 70)

time.sleep(2)

# 测试1: 健康检查
print("\n📍 测试1: 健康检查")
try:
    response = requests.get('http://127.0.0.1:5173/api/health', timeout=5)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 服务状态: {result['status']}")
        print(f"✅ 版本: {result['version']}")
    else:
        print(f"❌ 健康检查失败: {response.status_code}")
except Exception as e:
    print(f"❌ 错误: {e}")

# 测试2: 部署资源预测
print("\n📍 测试2: 部署资源预测")
try:
    test_params = {
        'qps': 5000,
        'data_volume': 500,
        'ha_level': 'high',
        'industry': '金融'
    }
    
    response = requests.post(
        'http://127.0.0.1:5173/api/predict',
        json=test_params,
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            data = result.get('data', {})
            print(f"✅ 预测成功")
            
            if 'input_summary' in data:
                summary = data['input_summary']
                print(f"   系统规模: {summary.get('scale', 'N/A').upper()}")
            
            if 'equipment_list' in data:
                servers = data['equipment_list'].get('servers', [])
                print(f"   服务器数量: {len(servers)} 台")
            
            if 'cost_breakdown' in data:
                cost = data['cost_breakdown'].get('summary', {})
                print(f"   初始投资: ¥{cost.get('initial_investment', 0):,.0f}")
        else:
            print(f"❌ 预测失败: {result.get('error')}")
    else:
        print(f"❌ 请求失败: {response.status_code}")
except Exception as e:
    print(f"❌ 错误: {e}")

# 测试3: 模型库管理
print("\n📍 测试3: 模型库管理")
try:
    # 获取可用模型库列表
    response = requests.get('http://127.0.0.1:5173/api/model_libraries', timeout=10)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            libraries = result.get('libraries', [])
            print(f"✅ 获取模型库列表成功")
            print(f"   可用模型库数量: {len(libraries)}")
            
            # 显示前3个模型库
            for i, lib_info in enumerate(libraries[:3]):
                print(f"   {i+1}. {lib_info.get('name')} - {lib_info.get('cases')}个案例")
        else:
            print(f"❌ 获取失败: {result.get('error')}")
    else:
        print(f"❌ 请求失败: {response.status_code}")
except Exception as e:
    print(f"❌ 错误: {e}")

# 测试4: 获取已安装的模型库
print("\n📍 测试4: 已安装的模型库")
try:
    response = requests.get('http://127.0.0.1:5173/api/model_libraries/installed', timeout=10)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            libraries = result.get('libraries', [])
            print(f"✅ 获取已安装模型库成功")
            print(f"   已安装数量: {len(libraries)}")
            
            if libraries:
                for lib in libraries[:3]:
                    print(f"   - {lib.get('name')} (v{lib.get('version')})")
            else:
                print(f"   ℹ️  暂无已安装的模型库")
        else:
            print(f"❌ 获取失败: {result.get('error')}")
    else:
        print(f"❌ 请求失败: {response.status_code}")
except Exception as e:
    print(f"❌ 错误: {e}")

# 测试5: 训练系统 - 获取训练案例
print("\n📍 测试5: 训练系统 - 获取训练案例")
try:
    response = requests.get('http://127.0.0.1:5173/api/training/cases', timeout=10)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            cases = result.get('cases', [])
            print(f"✅ 获取训练案例成功")
            print(f"   训练案例数量: {len(cases)}")
        else:
            print(f"❌ 获取失败: {result.get('error')}")
    else:
        print(f"❌ 请求失败: {response.status_code}")
except Exception as e:
    print(f"❌ 错误: {e}")

# 测试6: 添加训练案例
print("\n📍 测试6: 添加训练案例")
try:
    case_data = {
        'input': {
            'qps': 3000,
            'data_volume': 300,
            'ha_level': 'medium',
            'industry': '电商'
        },
        'output': {
            'architecture_type': 'distributed',
            'node_count': 6,
            'shard_count': 4,
            'replica_count': 2
        },
        'feedback': {
            'accuracy': 0.95,
            'performance': 'good',
            'cost_effective': True
        }
    }
    
    response = requests.post(
        'http://127.0.0.1:5173/api/training/cases',
        json=case_data,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print(f"✅ 添加训练案例成功")
            print(f"   案例ID: {result.get('case_id')}")
        else:
            print(f"❌ 添加失败: {result.get('error')}")
    else:
        print(f"❌ 请求失败: {response.status_code}")
except Exception as e:
    print(f"❌ 错误: {e}")

# 测试7: 文件上传
print("\n📍 测试7: 文件上传")
try:
    with open('test_upload.json', 'rb') as f:
        files = {'file': ('test_upload.json', f, 'application/json')}
        response = requests.post('http://127.0.0.1:5173/api/upload', files=files, timeout=10)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            params = result.get('params', {})
            param_count = len([k for k in params.keys() if not k.startswith('error')])
            print(f"✅ 文件上传成功")
            print(f"   解析参数数量: {param_count}")
        else:
            print(f"❌ 上传失败: {result.get('error')}")
    else:
        print(f"❌ 请求失败: {response.status_code}")
except Exception as e:
    print(f"❌ 错误: {e}")

print("\n" + "=" * 70)
print("✅ 所有功能测试完成")
print("=" * 70)

print("\n🌐 访问地址:")
print("   主页面: http://127.0.0.1:5173")
print("   导航页面: http://127.0.0.1:5173/nav")
print("   模型库管理: http://127.0.0.1:5173/model_library")
print("   学习系统: http://127.0.0.1:5173/learning")

print("\n📚 功能模块:")
print("   ✅ 部署资源预测 - 智能分析生成部署方案")
print("   ✅ 模型库管理 - 下载和管理预训练模型")
print("   ✅ 自主训练 - 从实际案例中学习优化")
print("   ✅ 文件上传 - 支持多种格式自动解析")
