#!/usr/bin/env python3
"""测试文件上传和解析功能"""

import requests
import json
import time

print("=" * 60)
print("🧪 测试文件上传和解析功能")
print("=" * 60)

# 等待服务启动
time.sleep(3)

# 测试1: 上传JSON文件
print("\n📤 测试1: 上传JSON文件")
try:
    with open('test_upload.json', 'rb') as f:
        files = {'file': ('test_upload.json', f, 'application/json')}
        response = requests.post('http://127.0.0.1:5173/api/upload', files=files, timeout=10)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 上传成功")
        print(f"✅ 文件名: {result.get('filename')}")
        print(f"✅ 解析参数: {json.dumps(result.get('params'), indent=2, ensure_ascii=False)}")
    else:
        print(f"❌ 上传失败: {response.status_code}")
        print(f"   响应: {response.text}")
except Exception as e:
    print(f"❌ 错误: {e}")

# 测试2: 上传图片文件
print("\n📤 测试2: 上传图片文件")
try:
    import os
    image_files = [f for f in os.listdir('uploads') if f.endswith(('.png', '.jpg', '.jpeg'))]
    if image_files:
        image_path = os.path.join('uploads', image_files[0])
        with open(image_path, 'rb') as f:
            files = {'file': (image_files[0], f, 'image/png')}
            response = requests.post('http://127.0.0.1:5173/api/upload', files=files, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 上传成功")
            print(f"✅ 文件名: {result.get('filename')}")
            print(f"✅ 解析结果: {json.dumps(result.get('params'), indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ 上传失败: {response.status_code}")
    else:
        print("⚠️  没有找到图片文件")
except Exception as e:
    print(f"❌ 错误: {e}")

# 测试3: 使用解析的参数进行预测
print("\n📤 测试3: 使用参数进行预测")
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
            print(f"✅ 服务器数量: {len(data.get('equipment_list', {}).get('servers', []))}")
            print(f"✅ 初始投资: ¥{data.get('cost_breakdown', {}).get('summary', {}).get('initial_investment', 0):,.0f}")
        else:
            print(f"❌ 预测失败: {result.get('error')}")
    else:
        print(f"❌ 请求失败: {response.status_code}")
except Exception as e:
    print(f"❌ 错误: {e}")

print("\n" + "=" * 60)
print("✅ 测试完成")
print("=" * 60)
