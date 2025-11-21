#!/usr/bin/env python3
"""
测试信创设备详细参数功能
验证CPU、内存、硬盘等完整配置信息
"""

import requests
import json

# API地址
API_URL = 'http://127.0.0.1:18080/api/predict'

# 测试数据
test_data = {
    'data_volume': 10,  # 10TB
    'tps': 5000,
    'concurrent_users': 2000,
    'need_disaster_recovery': False,
    'enable_xinchuan': True,
    'xinchuan_mode': 'standard'  # 标准信创模式
}

print("=" * 80)
print("测试信创设备详细参数功能")
print("=" * 80)

try:
    response = requests.post(API_URL, json=test_data, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        
        if result.get('success'):
            data = result['data']
            
            print("\n✅ 预测成功!\n")
            
            # 检查信创方案
            if data.get('xinchuan_enabled') and data.get('xinchuan_solution'):
                xc_solution = data['xinchuan_solution']
                equipment_list = xc_solution.get('equipment_list', [])
                
                print(f"信创模式: {data.get('xinchuan_mode')}")
                print(f"设备总数: {len(equipment_list)}")
                print("\n" + "=" * 80)
                print("详细设备配置清单")
                print("=" * 80)
                
                # 服务器配置
                print("\n🖥️  服务器配置:")
                print("-" * 80)
                server_categories = ['数据库服务器', '代理服务器', '监控服务器']
                
                for item in equipment_list:
                    if item['category'] in server_categories:
                        print(f"\n【{item['category']}】 {item['name']}")
                        print(f"  厂商: {item.get('vendor', 'N/A')}")
                        print(f"  认证: {item.get('certification', 'N/A')}")
                        print(f"  CPU: {item.get('cpu_cores', 'N/A')}核 {item.get('cpu_model', 'N/A')}")
                        print(f"  内存: {item.get('memory_gb', 'N/A')}GB")
                        print(f"  硬盘: {item.get('disk_gb', 'N/A')}GB {item.get('disk_type', 'N/A')}")
                        print(f"  网络: {item.get('network', 'N/A')}")
                        print(f"  功耗: {item.get('power_w', 'N/A')}W")
                        print(f"  数量: {item['quantity']}")
                        print(f"  单价: ¥{item['unit_price']:,}")
                        print(f"  总价: ¥{item['total_price']:,}")
                
                # 网络设备配置
                print("\n" + "=" * 80)
                print("🌐 网络设备配置:")
                print("-" * 80)
                network_categories = ['核心交换机', '接入交换机', '安全防火墙']
                
                for item in equipment_list:
                    if item['category'] in network_categories:
                        print(f"\n【{item['category']}】 {item['name']}")
                        print(f"  厂商: {item.get('vendor', 'N/A')}")
                        print(f"  认证: {item.get('certification', 'N/A')}")
                        print(f"  类型: {item.get('device_type', item['category'])}")
                        
                        if 'ports' in item:
                            print(f"  端口: {item['ports']}口 {item.get('speed', '')}")
                        if 'uplink' in item:
                            print(f"  上联: {item['uplink']}")
                        if 'throughput' in item:
                            print(f"  吞吐量: {item['throughput']}")
                        
                        print(f"  功耗: {item.get('power_w', 'N/A')}W")
                        print(f"  数量: {item['quantity']}")
                        print(f"  单价: ¥{item['unit_price']:,}")
                        print(f"  总价: ¥{item['total_price']:,}")
                
                # 成本汇总
                print("\n" + "=" * 80)
                print("💰 成本汇总:")
                print("-" * 80)
                cost = xc_solution.get('cost_breakdown', {})
                print(f"硬件成本: ¥{cost.get('hardware_cost', 0):,.0f}")
                print(f"软件成本: ¥{cost.get('software_cost', 0):,.0f}")
                print(f"基础设施: ¥{cost.get('infrastructure_cost', 0):,.0f}")
                print(f"总成本: ¥{cost.get('total_initial_cost', 0):,.0f}")
                
                # 成本对比
                if cost.get('xinchuan_comparison'):
                    comp = cost['xinchuan_comparison']
                    print(f"\n对比国外品牌:")
                    print(f"  传统方案成本: ¥{comp.get('international_cost', 0):,.0f}")
                    print(f"  信创方案成本: ¥{comp.get('xinchuan_cost', 0):,.0f}")
                    print(f"  💰 节约: ¥{comp.get('cost_savings', 0):,.0f} ({comp.get('savings_percent', 0)}%)")
                
                print("\n" + "=" * 80)
                print("✅ 所有设备参数完整!")
                print("=" * 80)
                
                # 验证关键字段
                missing_fields = []
                for item in equipment_list:
                    if item['category'] in server_categories:
                        required_fields = ['cpu_cores', 'cpu_model', 'memory_gb', 'disk_gb', 'disk_type', 'network', 'power_w']
                        for field in required_fields:
                            if field not in item or not item[field]:
                                missing_fields.append(f"{item['name']}.{field}")
                    elif item['category'] in network_categories:
                        if 'power_w' not in item or not item['power_w']:
                            missing_fields.append(f"{item['name']}.power_w")
                
                if missing_fields:
                    print("\n⚠️  警告: 以下字段缺失:")
                    for field in missing_fields:
                        print(f"  - {field}")
                else:
                    print("\n✅ 所有必填字段都已包含!")
                
            else:
                print("\n❌ 信创方案未启用或数据缺失")
        else:
            print(f"\n❌ 预测失败: {result.get('error', '未知错误')}")
    else:
        print(f"\n❌ HTTP错误: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"\n❌ 请求异常: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)
