#!/usr/bin/env python3
"""完整功能测试"""

import requests
import json
import time

print("=" * 60)
print("🧪 TDSQL部署资源预测系统 - 完整功能测试")
print("=" * 60)

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

# 测试2: 上传JSON文件
print("\n📍 测试2: 上传JSON文件并解析")
try:
    with open('test_upload.json', 'rb') as f:
        files = {'file': ('test_upload.json', f, 'application/json')}
        response = requests.post('http://127.0.0.1:5173/api/upload', files=files, timeout=10)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 上传成功")
        print(f"✅ 文件名: {result.get('filename')}")
        params = result.get('params', {})
        param_count = len([k for k in params.keys() if not k.startswith('error')])
        print(f"✅ 解析参数数量: {param_count}")
        print(f"✅ 参数详情: {json.dumps(params, indent=2, ensure_ascii=False)}")
    else:
        print(f"❌ 上传失败: {response.status_code}")
except Exception as e:
    print(f"❌ 错误: {e}")

# 测试3: 使用解析的参数进行预测
print("\n📍 测试3: 部署资源预测")
try:
    test_params = {
        'qps': 5000,
        'data_volume': 500,
        'ha_level': 'high',
        'industry': '金融'
    }
    
    print(f"📤 请求参数: {json.dumps(test_params, ensure_ascii=False)}")
    
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
            
            # 检查数据结构
            if 'input_summary' in data:
                summary = data['input_summary']
                print(f"✅ 系统规模: {summary.get('scale', 'N/A').upper()}")
                print(f"✅ QPS: {summary.get('qps', 0):,}")
                print(f"✅ 数据量: {summary.get('current_data_gb', 0):,} GB")
            
            if 'equipment_list' in data:
                servers = data['equipment_list'].get('servers', [])
                print(f"✅ 服务器数量: {len(servers)} 台")
            
            if 'cost_breakdown' in data:
                cost = data['cost_breakdown'].get('summary', {})
                print(f"✅ 初始投资: ¥{cost.get('initial_investment', 0):,.0f}")
                print(f"✅ 3年TCO: ¥{cost.get('three_year_tco', 0):,.0f}")
            
            if 'architecture' in data:
                arch = data['architecture']
                print(f"✅ 架构类型: {arch.get('type', 'N/A')}")
                print(f"✅ 架构描述: {arch.get('description', 'N/A')}")
        else:
            print(f"❌ 预测失败: {result.get('error')}")
    else:
        print(f"❌ 请求失败: {response.status_code}")
        print(f"   响应: {response.text[:200]}")
except Exception as e:
    print(f"❌ 错误: {e}")

# 测试4: 清除上传文件
print("\n📍 测试4: 清除上传文件")
try:
    response = requests.post('http://127.0.0.1:5173/api/clear_uploads', timeout=5)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ {result.get('message')}")
    else:
        print(f"❌ 清除失败: {response.status_code}")
except Exception as e:
    print(f"❌ 错误: {e}")

print("\n" + "=" * 60)
print("✅ 所有测试完成")
print("=" * 60)
print("\n🌐 访问系统: http://127.0.0.1:5173")
print("📚 查看文档: FILE_UPLOAD_GUIDE.md")
