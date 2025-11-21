#!/usr/bin/env python3
"""测试信创模式API - 修复循环引用问题"""

import requests
import json

print("=" * 80)
print("测试信创模式部署预测 API")
print("=" * 80)

url = "http://localhost:18080/api/predict"

# 测试数据
test_data = {
    "data_volume": 5,  # 5TB
    "qps": 5000,
    "tps": 1500,
    "concurrent_users": 2000,
    "industry": "finance",
    "need_high_availability": True,
    "enable_xinchuan": True,
    "xinchuan_mode": "standard"  # 标准信创模式
}

print("\n📤 发送请求...")
print(f"URL: {url}")
print(f"数据: {json.dumps(test_data, indent=2, ensure_ascii=False)}")

try:
    response = requests.post(url, json=test_data, timeout=10)
    
    print(f"\n📥 响应状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        
        if result.get('success'):
            print("\n✅ 预测成功！")
            
            data = result.get('data', {})
            
            # 显示基本信息
            print("\n" + "=" * 80)
            print("📊 预测结果摘要")
            print("=" * 80)
            
            # 信创模式信息
            if data.get('xinchuan_enabled'):
                print(f"\n🇨🇳 信创模式: {data.get('xinchuan_mode', 'N/A')}")
                xc_info = data.get('xinchuan_info', {})
                if xc_info:
                    print(f"  - 模式: {xc_info.get('mode', 'N/A')}")
                    print(f"  - 服务器品牌: {', '.join(xc_info.get('servers', []))}")
                    print(f"  - 网络设备: {', '.join(xc_info.get('network', []))}")
                    print(f"  - CPU芯片: {', '.join(xc_info.get('cpu', []))}")
                    print(f"  - 成本优势: {xc_info.get('cost_advantage', 'N/A')}")
                    print(f"  - 合规性: {xc_info.get('compliance', 'N/A')}")
            
            # 信创方案详情
            xc_solution = data.get('xinchuan_solution', {})
            if xc_solution:
                print("\n💰 信创方案成本:")
                cost = xc_solution.get('cost_breakdown', {})
                if cost:
                    total = cost.get('total_initial_cost', 0)
                    print(f"  - 总成本: ¥{total:,.2f} ({total/10000:.1f}万元)")
                
                print("\n📦 主要设备清单:")
                equipment = xc_solution.get('equipment_list', [])
                for idx, item in enumerate(equipment[:5], 1):
                    print(f"  {idx}. {item.get('name', 'N/A')} x{item.get('quantity', 0)}")
                    print(f"     - 厂商: {item.get('vendor', 'N/A')}")
                    print(f"     - 单价: ¥{item.get('unit_price', 0):,}")
                    print(f"     - 总价: ¥{item.get('total_price', 0):,}")
                
                if len(equipment) > 5:
                    print(f"  ... 还有 {len(equipment)-5} 项设备")
            
            print("\n" + "=" * 80)
            print("✅ 测试通过！循环引用问题已修复")
            print("=" * 80)
            
        else:
            print(f"\n❌ 预测失败: {result.get('error', 'Unknown error')}")
    else:
        print(f"\n❌ HTTP错误: {response.status_code}")
        print(f"响应: {response.text[:500]}")
        
except requests.exceptions.ConnectionError:
    print("\n❌ 连接失败！请确保Flask服务正在运行")
    print("启动命令: python3 app_simple.py")
except Exception as e:
    print(f"\n❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()

print()
