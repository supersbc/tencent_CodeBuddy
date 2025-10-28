#!/usr/bin/env python3
"""简单测试服务是否响应"""

import requests
import time

print("=" * 60)
print("🧪 测试服务连接")
print("=" * 60)

# 等待服务启动
time.sleep(2)

try:
    # 测试根路径
    print("\n📍 测试 GET /")
    response = requests.get('http://127.0.0.1:5173/', timeout=5)
    print(f"✅ 状态码: {response.status_code}")
    print(f"✅ 响应长度: {len(response.text)} 字节")
    print(f"✅ Content-Type: {response.headers.get('Content-Type')}")
    
    # 测试健康检查
    print("\n📍 测试 GET /api/health")
    response = requests.get('http://127.0.0.1:5173/api/health', timeout=5)
    print(f"✅ 状态码: {response.status_code}")
    print(f"✅ 响应: {response.json()}")
    
    print("\n✅ 服务正常运行！")
    
except requests.exceptions.Timeout:
    print("\n❌ 请求超时！服务可能卡住了")
except requests.exceptions.ConnectionError:
    print("\n❌ 无法连接到服务！")
except Exception as e:
    print(f"\n❌ 错误: {e}")
