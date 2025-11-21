#!/usr/bin/env python3
"""测试设备清单对比功能"""

import requests
import json

print("=" * 80)
print("🧪 测试设备清单对比功能")
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
    "enable_xinchuan": True,  # 启用信创
    "xinchuan_mode": "standard"  # 标准信创模式
}

print("\n📤 发送预测请求...")
print(f"数据量: {test_data['data_volume']}TB")
print(f"信创模式: {test_data['xinchuan_mode']}")

try:
    response = requests.post(url, json=test_data, timeout=15)
    
    if response.status_code == 200:
        result = response.json()
        
        if result.get('success'):
            print("\n✅ 预测成功！")
            
            data = result.get('data', {})
            
            # 检查信创功能
            if data.get('xinchuan_enabled'):
                print("\n🇨🇳 信创模式已启用")
                print(f"   模式: {data.get('xinchuan_mode', 'N/A')}")
                
                xc_info = data.get('xinchuan_info', {})
                print(f"   服务器品牌: {', '.join(xc_info.get('servers', []))}")
                print(f"   网络设备: {', '.join(xc_info.get('network', []))}")
                print(f"   成本优势: {xc_info.get('cost_advantage', 'N/A')}")
                
                # 检查信创方案数据
                xc_solution = data.get('xinchuan_solution', {})
                if xc_solution:
                    print("\n📦 信创设备清单:")
                    equipment = xc_solution.get('equipment_list', [])
                    print(f"   共 {len(equipment)} 项设备")
                    
                    # 按类别统计
                    categories = {}
                    for item in equipment:
                        cat = item.get('category', '其他')
                        if cat not in categories:
                            categories[cat] = []
                        categories[cat].append(item)
                    
                    for category, items in categories.items():
                        print(f"\n   【{category}】")
                        for item in items:
                            print(f"      • {item.get('name', 'N/A')} x{item.get('quantity', 0)}")
                            print(f"        厂商: {item.get('vendor', 'N/A')}")
                            print(f"        单价: ¥{item.get('unit_price', 0):,}")
                            if item.get('certification'):
                                print(f"        认证: {item.get('certification')}")
                    
                    # 成本对比
                    print("\n💰 成本对比:")
                    traditional_cost = data.get('cost', {}).get('initial_investment', 0)
                    xinchuan_cost = xc_solution.get('cost_breakdown', {}).get('total_initial_cost', 0)
                    savings = traditional_cost - xinchuan_cost
                    savings_percent = (savings / traditional_cost * 100) if traditional_cost > 0 else 0
                    
                    print(f"   传统方案: ¥{traditional_cost:,.2f}")
                    print(f"   信创方案: ¥{xinchuan_cost:,.2f}")
                    print(f"   节约金额: ¥{savings:,.2f} ({savings_percent:.1f}%)")
                    
                else:
                    print("\n⚠️  未找到信创方案数据")
            else:
                print("\n⚠️  信创模式未启用")
            
            print("\n" + "=" * 80)
            print("✅ 测试完成！设备清单对比功能正常")
            print("=" * 80)
            print("\n📍 访问 https://aladdinsun.devcloud.woa.com/predict 查看完整对比")
            
        else:
            print(f"\n❌ 预测失败: {result.get('error', 'Unknown error')}")
    else:
        print(f"\n❌ HTTP错误: {response.status_code}")
        print(f"响应: {response.text[:500]}")
        
except requests.exceptions.ConnectionError:
    print("\n❌ 连接失败！请确保Flask服务正在运行")
except Exception as e:
    print(f"\n❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()

print()
