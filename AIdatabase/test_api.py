#!/usr/bin/env python3
"""
测试部署资源预测API
"""

import requests
import json

def test_predict():
    """测试预测接口"""
    url = "http://127.0.0.1:5173/api/predict"
    
    data = {
        "qps": 5000,
        "tps": 1500,
        "data_volume": 500,
        "concurrent_users": 1000,
        "data_growth_rate": 0.3,
        "ha_level": "high",
        "industry": "finance"
    }
    
    print("=" * 60)
    print("🧪 测试部署资源预测API")
    print("=" * 60)
    print(f"\n📤 请求参数:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
    try:
        response = requests.post(url, json=data)
        result = response.json()
        
        if result.get('success'):
            print("\n✅ 预测成功!")
            print("\n📊 预测结果概览:")
            print("-" * 60)
            
            # 输入摘要
            summary = result.get('input_summary', {})
            print(f"系统规模: {summary.get('scale', 'N/A').upper()}")
            print(f"QPS: {summary.get('qps', 0):,}")
            print(f"峰值QPS: {summary.get('peak_qps', 0):,}")
            print(f"当前数据量: {summary.get('current_data_gb', 0):,} GB")
            print(f"预测数据量(3年): {summary.get('projected_data_gb', 0):,.0f} GB")
            
            # 架构信息
            arch = result.get('architecture', {})
            topology = arch.get('topology', {})
            print(f"\n🏗️ 架构设计:")
            print(f"架构类型: {arch.get('description', 'N/A')}")
            print(f"分片数: {topology.get('shard_count', 0)}")
            print(f"副本数: {topology.get('replica_count', 0)}")
            print(f"数据库节点: {topology.get('db_nodes', 0)} 台")
            print(f"代理节点: {topology.get('proxy_nodes', 0)} 台")
            print(f"应用节点: {topology.get('app_nodes', 0)} 台")
            
            # 设备统计
            equipment = result.get('equipment_list', {})
            servers = equipment.get('servers', [])
            network_devices = equipment.get('network_devices', [])
            print(f"\n🖥️ 设备统计:")
            print(f"服务器总数: {len(servers)} 台")
            print(f"网络设备: {len(network_devices)} 台")
            
            # 成本分析
            cost = result.get('cost_breakdown', {}).get('summary', {})
            print(f"\n💰 成本分析:")
            print(f"硬件成本: ¥{cost.get('total_hardware', 0):,.0f}")
            print(f"软件成本: ¥{cost.get('total_software', 0):,.0f}")
            print(f"服务成本: ¥{cost.get('total_services', 0):,.0f}")
            print(f"初始投资: ¥{cost.get('initial_investment', 0):,.0f}")
            print(f"年度运营: ¥{cost.get('annual_operating', 0):,.0f}/年")
            print(f"3年TCO: ¥{cost.get('three_year_tco', 0):,.0f}")
            
            # 建议数量
            recommendations = result.get('recommendations', [])
            print(f"\n💡 部署建议: {len(recommendations)} 条")
            
            print("\n" + "=" * 60)
            print("✅ 测试通过！系统运行正常")
            print("=" * 60)
            
        else:
            print(f"\n❌ 预测失败: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"\n❌ 请求失败: {str(e)}")

if __name__ == '__main__':
    test_predict()
