#!/usr/bin/env python3
"""
信创模式快速测试和对比工具
"""

from deployment_predictor_xinchuan import DeploymentResourcePredictorXinChuan
from xinchuan_device_catalog import XinChuangDeviceCatalog
import json

def test_all_modes():
    """测试所有信创模式并对比"""
    
    print("=" * 80)
    print("🇨🇳 AIdatabase 信创模式对比测试")
    print("=" * 80)
    
    # 测试场景
    scenarios = [
        {
            'name': '小型OLTP系统',
            'data': {
                'data_size_gb': 1000,
                'transactions_per_day': 1000000,
                'max_connections': 500,
                'business_type': 'OLTP',
                'high_availability': True
            }
        },
        {
            'name': '中型电商平台',
            'data': {
                'data_size_gb': 5000,
                'transactions_per_day': 5000000,
                'max_connections': 2000,
                'business_type': 'OLTP',
                'high_availability': True
            }
        },
        {
            'name': '大型金融系统',
            'data': {
                'data_size_gb': 20000,
                'transactions_per_day': 20000000,
                'max_connections': 5000,
                'business_type': 'OLTP',
                'high_availability': True,
                'disaster_recovery': True
            }
        }
    ]
    
    modes = [
        ('off', '国外品牌'),
        ('standard', '标准信创'),
        ('strict', '严格信创'),
        ('full', '完全信创')
    ]
    
    for scenario in scenarios:
        print(f"\n{'=' * 80}")
        print(f"📊 场景: {scenario['name']}")
        print(f"{'=' * 80}")
        print(f"数据量: {scenario['data']['data_size_gb']/1024:.1f}TB")
        print(f"日交易量: {scenario['data']['transactions_per_day']:,}")
        print(f"最大连接: {scenario['data']['max_connections']:,}")
        print()
        
        results = {}
        
        for mode_key, mode_name in modes:
            predictor = DeploymentResourcePredictorXinChuan(xinchuan_mode=mode_key)
            result = predictor.predict(scenario['data'])
            results[mode_key] = result
        
        # 打印对比表格
        print(f"{'模式':<12} {'总成本(万元)':<15} {'vs国外品牌':<15} {'主要设备'}")
        print("-" * 80)
        
        international_cost = results['off']['cost_breakdown']['total_initial_cost']
        
        for mode_key, mode_name in modes:
            result = results[mode_key]
            cost = result['cost_breakdown']['total_initial_cost']
            cost_wan = cost / 10000
            
            # 计算vs国外品牌
            if mode_key == 'off':
                vs_text = '-'
            else:
                savings = international_cost - cost
                savings_pct = (savings / international_cost) * 100
                vs_text = f"节约 {savings_pct:.1f}%"
            
            # 主要设备
            main_device = result['equipment_list'][0]['name'] if result['equipment_list'] else 'N/A'
            
            print(f"{mode_name:<12} ¥{cost_wan:>12.1f} {vs_text:<15} {main_device}")
        
        print()
        
        # 显示标准信创详细信息
        std_result = results['standard']
        print("💡 标准信创方案详情:")
        print("-" * 80)
        
        xc_info = std_result['xinchuan_info']
        print(f"  服务器品牌: {', '.join(xc_info['servers'])}")
        print(f"  网络设备: {', '.join(xc_info['network'])}")
        print(f"  CPU芯片: {', '.join(xc_info['cpu'])}")
        print(f"  成本优势: {xc_info['cost_advantage']}")
        print(f"  合规性: {xc_info['compliance']}")
        
        print("\n  主要设备清单:")
        for item in std_result['equipment_list'][:5]:
            print(f"    • {item['name']} x{item['quantity']}")
            print(f"      厂商: {item['vendor']}, 单价: ¥{item['unit_price']:,}")
        
        if len(std_result['equipment_list']) > 5:
            print(f"    ... 还有 {len(std_result['equipment_list'])-5} 项设备")


def compare_vendors():
    """对比国产vs国外品牌"""
    print("\n" + "=" * 80)
    print("🔍 国产 vs 国外品牌详细对比")
    print("=" * 80)
    
    catalog = XinChuangDeviceCatalog()
    comparison = catalog.get_vendor_comparison()
    
    for category, info in comparison.items():
        print(f"\n【{category}】")
        print(f"  国产品牌: {', '.join(info['国产品牌'])}")
        print(f"  国外品牌: {', '.join(info['国外品牌'])}")
        print(f"  优势: {info['优势']}")
        print(f"  技术成熟度: {info['技术成熟度']}")


def show_recommendations():
    """显示信创选择建议"""
    print("\n" + "=" * 80)
    print("💡 信创模式选择建议")
    print("=" * 80)
    
    recommendations = {
        '普通企业应用': {
            '推荐模式': '标准信创',
            '理由': '成本优势明显(节约8-15%),技术成熟',
            '案例': '电商平台、企业ERP、CRM系统'
        },
        '金融/能源行业': {
            '推荐模式': '严格信创',
            '理由': '满足行业监管要求,全国产CPU',
            '案例': '银行核心系统、交易所、电力调度'
        },
        '党政军系统': {
            '推荐模式': '完全信创',
            '理由': '国家强制要求,全栈国产化',
            '案例': '政务云、军工系统、涉密平台'
        },
        '外资企业': {
            '推荐模式': '关闭信创',
            '理由': '无信创要求,可自由选择',
            '案例': '外企分支机构、国际业务'
        }
    }
    
    for scenario, info in recommendations.items():
        print(f"\n场景: {scenario}")
        print(f"  ✅ 推荐: {info['推荐模式']}")
        print(f"  📝 理由: {info['理由']}")
        print(f"  📊 案例: {info['案例']}")


def cost_savings_analysis():
    """成本节约分析"""
    print("\n" + "=" * 80)
    print("💰 成本节约详细分析")
    print("=" * 80)
    
    # 模拟100台服务器的采购
    print("\n假设场景: 采购100台数据库服务器")
    print("-" * 80)
    
    catalog = XinChuangDeviceCatalog()
    
    # 中型服务器对比
    xc_server = catalog.server_catalog['db_medium']
    international_price = 45000  # Dell R640
    
    quantity = 100
    xc_total = xc_server['price'] * quantity
    intl_total = international_price * quantity
    savings = intl_total - xc_total
    savings_pct = (savings / intl_total) * 100
    
    print(f"\n服务器对比:")
    print(f"  国产方案: {xc_server['name']}")
    print(f"    - CPU: {xc_server['cpu_model']}")
    print(f"    - 单价: ¥{xc_server['price']:,}")
    print(f"    - 总价: ¥{xc_total:,} ({xc_total/10000:.1f}万元)")
    print(f"\n  国外方案: Dell PowerEdge R640")
    print(f"    - CPU: Intel Xeon Gold 5218")
    print(f"    - 单价: ¥{international_price:,}")
    print(f"    - 总价: ¥{intl_total:,} ({intl_total/10000:.1f}万元)")
    print(f"\n  💰 节约: ¥{savings:,} ({savings/10000:.1f}万元, {savings_pct:.1f}%)")
    
    # 操作系统成本对比
    print(f"\n操作系统对比:")
    print(f"  国产方案: openEuler (免费)")
    print(f"    - 单价: ¥0")
    print(f"    - 总价: ¥0")
    print(f"\n  国外方案: Red Hat Enterprise Linux")
    print(f"    - 单价: ¥5,000/台")
    print(f"    - 总价: ¥{5000*quantity:,} ({5000*quantity/10000:.1f}万元)")
    print(f"\n  💰 节约: ¥{5000*quantity:,} ({5000*quantity/10000:.1f}万元, 100%)")
    
    # 总计
    total_savings = savings + 5000*quantity
    print(f"\n{'=' * 80}")
    print(f"总节约: ¥{total_savings:,} ({total_savings/10000:.1f}万元)")
    print(f"{'=' * 80}")


if __name__ == '__main__':
    # 1. 测试所有模式
    test_all_modes()
    
    # 2. 品牌对比
    compare_vendors()
    
    # 3. 选择建议
    show_recommendations()
    
    # 4. 成本分析
    cost_savings_analysis()
    
    print("\n" + "=" * 80)
    print("✅ 测试完成!")
    print("=" * 80)
    print("\n📚 查看完整文档: cat 信创模式使用指南.md")
    print("🚀 启动Web服务: python3 app_simple.py")
    print("=" * 80)
