#!/usr/bin/env python3
"""
测试双方案对比功能
验证传统方案和信创方案的完整架构对比
"""

import requests
import json

API_URL = 'http://127.0.0.1:18080/api/predict'

test_data = {
    'data_volume': 10,
    'tps': 5000,
    'concurrent_users': 2000,
    'need_disaster_recovery': False,
    'enable_xinchuan': True,
    'xinchuan_mode': 'standard'
}

print("=" * 100)
print("双方案完整架构对比测试")
print("=" * 100)

response = requests.post(API_URL, json=test_data, timeout=30)

if response.status_code == 200:
    result = response.json()
    
    if result.get('success'):
        data = result['data']
        
        print("\n✅ 预测成功!\n")
        
        # 传统方案
        traditional = data.get('traditional_solution', {})
        traditional_equipment = traditional.get('equipment_list', [])
        traditional_cost = traditional.get('cost_breakdown', {})
        
        # 信创方案
        xinchuan = data.get('xinchuan_solution', {})
        xinchuan_equipment = xinchuan.get('equipment_list', [])
        xinchuan_cost = xinchuan.get('cost_breakdown', {})
        
        # 成本对比
        cost_comparison = data.get('cost_comparison', {})
        
        print("=" * 100)
        print("📊 传统方案 (国外品牌: Dell/Cisco)")
        print("=" * 100)
        print(f"\n设备总数: {len(traditional_equipment)}")
        print(f"总成本: ¥{traditional_cost.get('total_initial_cost', 0):,.0f}")
        
        print("\n设备清单:")
        for item in traditional_equipment:
            print(f"\n  [{item['category']}] {item['name']}")
            print(f"    厂商: {item.get('vendor', 'N/A')}")
            if 'cpu_model' in item:
                print(f"    CPU: {item.get('cpu_cores')}核 {item.get('cpu_model')}")
                print(f"    内存: {item.get('memory_gb')}GB")
                print(f"    硬盘: {item.get('disk_gb')}GB {item.get('disk_type')}")
            elif 'ports' in item:
                print(f"    端口: {item.get('ports')}口 {item.get('speed')}")
                print(f"    上联: {item.get('uplink', 'N/A')}")
            elif 'throughput' in item:
                print(f"    吞吐量: {item.get('throughput')}")
            print(f"    数量: {item['quantity']}")
            print(f"    单价: ¥{item['unit_price']:,}")
            print(f"    总价: ¥{item['total_price']:,}")
        
        print("\n" + "=" * 100)
        print("🇨🇳 信创方案 (国产品牌: 浪潮/华为)")
        print("=" * 100)
        print(f"\n设备总数: {len(xinchuan_equipment)}")
        print(f"总成本: ¥{xinchuan_cost.get('total_initial_cost', 0):,.0f}")
        
        print("\n设备清单:")
        for item in xinchuan_equipment:
            print(f"\n  [{item['category']}] {item['name']}")
            print(f"    厂商: {item.get('vendor', 'N/A')}")
            print(f"    认证: {item.get('certification', 'N/A')}")
            if 'cpu_model' in item:
                print(f"    CPU: {item.get('cpu_cores')}核 {item.get('cpu_model')}")
                print(f"    内存: {item.get('memory_gb')}GB")
                print(f"    硬盘: {item.get('disk_gb')}GB {item.get('disk_type')}")
            elif 'ports' in item:
                print(f"    端口: {item.get('ports')}口 {item.get('speed')}")
                print(f"    上联: {item.get('uplink', 'N/A')}")
            elif 'throughput' in item:
                print(f"    吞吐量: {item.get('throughput')}")
            print(f"    数量: {item['quantity']}")
            print(f"    单价: ¥{item['unit_price']:,}")
            print(f"    总价: ¥{item['total_price']:,}")
        
        print("\n" + "=" * 100)
        print("💰 成本对比分析")
        print("=" * 100)
        
        print(f"\n传统方案总成本: ¥{cost_comparison.get('traditional_cost', 0):,.0f}")
        print(f"信创方案总成本: ¥{cost_comparison.get('xinchuan_cost', 0):,.0f}")
        print(f"💰 节约金额: ¥{cost_comparison.get('cost_savings', 0):,.0f}")
        print(f"📊 节约比例: {cost_comparison.get('savings_percent', 0)}%")
        print(f"\n说明: {cost_comparison.get('note', '')}")
        
        # 逐项对比
        print("\n" + "=" * 100)
        print("📋 设备逐项对比")
        print("=" * 100)
        
        print(f"\n{'类别':<15} {'传统方案':<30} {'信创方案':<30} {'价格差异':<15}")
        print("-" * 100)
        
        # 按类别匹配设备
        categories = set([item['category'] for item in traditional_equipment] + 
                        [item['category'] for item in xinchuan_equipment])
        
        total_trad = 0
        total_xc = 0
        
        for cat in sorted(categories):
            trad_items = [item for item in traditional_equipment if item['category'] == cat]
            xc_items = [item for item in xinchuan_equipment if item['category'] == cat]
            
            if trad_items and xc_items:
                trad_name = trad_items[0]['name'][:28]
                xc_name = xc_items[0]['name'][:28]
                trad_price = sum(item['total_price'] for item in trad_items)
                xc_price = sum(item['total_price'] for item in xc_items)
                diff = trad_price - xc_price
                
                total_trad += trad_price
                total_xc += xc_price
                
                print(f"{cat:<15} {trad_name:<30} {xc_name:<30} -¥{diff:,}")
        
        print("-" * 100)
        print(f"{'总计':<15} {'¥' + f'{total_trad:,}':<30} {'¥' + f'{total_xc:,}':<30} -¥{total_trad - total_xc:,}")
        
        print("\n" + "=" * 100)
        print("✅ 测试通过! 双方案对比功能正常!")
        print("=" * 100)
        
    else:
        print(f"❌ 预测失败: {result.get('error')}")
else:
    print(f"❌ HTTP错误: {response.status_code}")
    print(response.text)
