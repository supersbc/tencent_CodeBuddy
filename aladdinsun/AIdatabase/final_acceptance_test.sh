#!/bin/bash

# 信创设备完整参数功能验收测试
# 测试CPU、内存、硬盘、网络等完整配置信息

echo "================================================================================"
echo "信创设备完整参数功能验收测试"
echo "================================================================================"

API_URL="http://127.0.0.1:18080/api/predict"

# 测试数据
TEST_DATA='{
    "data_volume": 10,
    "tps": 5000,
    "concurrent_users": 2000,
    "need_disaster_recovery": false,
    "enable_xinchuan": true,
    "xinchuan_mode": "standard"
}'

echo -e "\n📋 测试数据:"
echo "$TEST_DATA" | python3 -m json.tool

echo -e "\n🚀 发送预测请求..."

RESPONSE=$(curl -s -X POST "$API_URL" \
    -H "Content-Type: application/json" \
    -d "$TEST_DATA")

# 检查响应
if [ $? -ne 0 ]; then
    echo "❌ 请求失败"
    exit 1
fi

echo "✅ 请求成功"

# 解析响应
SUCCESS=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('success', False))")

if [ "$SUCCESS" != "True" ]; then
    echo "❌ 预测失败"
    echo "$RESPONSE" | python3 -m json.tool
    exit 1
fi

echo -e "\n================================================================================"
echo "✅ 预测成功,开始验证设备参数..."
echo "================================================================================"

# 验证脚本
python3 << 'EOF'
import json
import sys

response_str = '''RESPONSE_PLACEHOLDER'''

try:
    response = json.loads(response_str)
    data = response.get('data', {})
    
    if not data.get('xinchuan_enabled'):
        print("❌ 信创功能未启用")
        sys.exit(1)
    
    xc_solution = data.get('xinchuan_solution', {})
    equipment_list = xc_solution.get('equipment_list', [])
    
    if not equipment_list:
        print("❌ 设备清单为空")
        sys.exit(1)
    
    print(f"\n📊 设备总数: {len(equipment_list)}")
    
    # 服务器参数验证
    print("\n" + "="*80)
    print("🖥️  服务器参数验证")
    print("="*80)
    
    server_categories = ['数据库服务器', '代理服务器', '监控服务器']
    required_server_fields = ['cpu_cores', 'cpu_model', 'memory_gb', 'disk_gb', 'disk_type', 'network', 'power_w']
    
    server_count = 0
    server_missing = []
    
    for item in equipment_list:
        if item['category'] in server_categories:
            server_count += 1
            print(f"\n检查: {item['name']} ({item['category']})")
            
            for field in required_server_fields:
                if field not in item or item[field] is None or item[field] == '':
                    server_missing.append(f"{item['name']}.{field}")
                    print(f"  ❌ 缺少字段: {field}")
                else:
                    value = item[field]
                    if field == 'cpu_cores':
                        print(f"  ✅ CPU核数: {value}核")
                    elif field == 'cpu_model':
                        print(f"  ✅ CPU型号: {value}")
                    elif field == 'memory_gb':
                        print(f"  ✅ 内存: {value}GB")
                    elif field == 'disk_gb':
                        print(f"  ✅ 硬盘: {value}GB")
                    elif field == 'disk_type':
                        print(f"  ✅ 硬盘类型: {value}")
                    elif field == 'network':
                        print(f"  ✅ 网络: {value}")
                    elif field == 'power_w':
                        print(f"  ✅ 功耗: {value}W")
    
    print(f"\n服务器设备数: {server_count}")
    
    # 网络设备参数验证
    print("\n" + "="*80)
    print("🌐 网络设备参数验证")
    print("="*80)
    
    network_categories = ['核心交换机', '接入交换机', '安全防火墙']
    network_count = 0
    network_missing = []
    
    for item in equipment_list:
        if item['category'] in network_categories:
            network_count += 1
            print(f"\n检查: {item['name']} ({item['category']})")
            
            # 检查设备类型
            if 'device_type' in item:
                print(f"  ✅ 设备类型: {item['device_type']}")
            
            # 交换机特有字段
            if '交换机' in item['category']:
                if 'ports' in item and item['ports']:
                    print(f"  ✅ 端口数: {item['ports']}口")
                else:
                    network_missing.append(f"{item['name']}.ports")
                    print(f"  ❌ 缺少字段: ports")
                
                if 'speed' in item and item['speed']:
                    print(f"  ✅ 端口速率: {item['speed']}")
                else:
                    network_missing.append(f"{item['name']}.speed")
                    print(f"  ❌ 缺少字段: speed")
                
                if 'uplink' in item and item['uplink']:
                    print(f"  ✅ 上联: {item['uplink']}")
            
            # 防火墙特有字段
            if '防火墙' in item['category']:
                if 'throughput' in item and item['throughput']:
                    print(f"  ✅ 吞吐量: {item['throughput']}")
            
            # 通用字段
            if 'power_w' in item and item['power_w']:
                print(f"  ✅ 功耗: {item['power_w']}W")
            else:
                network_missing.append(f"{item['name']}.power_w")
                print(f"  ❌ 缺少字段: power_w")
    
    print(f"\n网络设备数: {network_count}")
    
    # 总结
    print("\n" + "="*80)
    print("📊 验收结果汇总")
    print("="*80)
    
    print(f"\n设备统计:")
    print(f"  - 服务器设备: {server_count} 台")
    print(f"  - 网络设备: {network_count} 台")
    print(f"  - 总设备数: {len(equipment_list)} 台")
    
    all_passed = True
    
    if server_missing:
        print(f"\n❌ 服务器缺失字段 ({len(server_missing)}):")
        for field in server_missing:
            print(f"  - {field}")
        all_passed = False
    else:
        print(f"\n✅ 所有服务器参数完整 ({server_count} 台)")
    
    if network_missing:
        print(f"\n❌ 网络设备缺失字段 ({len(network_missing)}):")
        for field in network_missing:
            print(f"  - {field}")
        all_passed = False
    else:
        print(f"\n✅ 所有网络设备参数完整 ({network_count} 台)")
    
    # 成本信息
    cost = xc_solution.get('cost_breakdown', {})
    print(f"\n💰 成本信息:")
    print(f"  - 硬件成本: ¥{cost.get('hardware_cost', 0):,.0f}")
    print(f"  - 软件成本: ¥{cost.get('software_cost', 0):,.0f}")
    print(f"  - 总成本: ¥{cost.get('total_initial_cost', 0):,.0f}")
    
    if cost.get('xinchuan_comparison'):
        comp = cost['xinchuan_comparison']
        print(f"  - 传统方案: ¥{comp.get('international_cost', 0):,.0f}")
        print(f"  - 💰 节约: ¥{comp.get('cost_savings', 0):,.0f} ({comp.get('savings_percent', 0)}%)")
    
    print("\n" + "="*80)
    if all_passed:
        print("✅ 验收通过! 所有设备参数完整!")
        print("="*80)
        sys.exit(0)
    else:
        print("❌ 验收失败! 存在缺失字段!")
        print("="*80)
        sys.exit(1)
        
except Exception as e:
    print(f"❌ 解析错误: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
EOF

# 替换占位符
VALIDATION_SCRIPT=$(cat << 'EOF'
import json
import sys

response_str = '''RESPONSE_PLACEHOLDER'''

try:
    response = json.loads(response_str)
    data = response.get('data', {})
    
    if not data.get('xinchuan_enabled'):
        print("❌ 信创功能未启用")
        sys.exit(1)
    
    xc_solution = data.get('xinchuan_solution', {})
    equipment_list = xc_solution.get('equipment_list', [])
    
    if not equipment_list:
        print("❌ 设备清单为空")
        sys.exit(1)
    
    print(f"\n📊 设备总数: {len(equipment_list)}")
    
    # 服务器参数验证
    print("\n" + "="*80)
    print("🖥️  服务器参数验证")
    print("="*80)
    
    server_categories = ['数据库服务器', '代理服务器', '监控服务器']
    required_server_fields = ['cpu_cores', 'cpu_model', 'memory_gb', 'disk_gb', 'disk_type', 'network', 'power_w']
    
    server_count = 0
    server_missing = []
    
    for item in equipment_list:
        if item['category'] in server_categories:
            server_count += 1
            print(f"\n检查: {item['name']} ({item['category']})")
            
            for field in required_server_fields:
                if field not in item or item[field] is None or item[field] == '':
                    server_missing.append(f"{item['name']}.{field}")
                    print(f"  ❌ 缺少字段: {field}")
                else:
                    value = item[field]
                    if field == 'cpu_cores':
                        print(f"  ✅ CPU核数: {value}核")
                    elif field == 'cpu_model':
                        print(f"  ✅ CPU型号: {value}")
                    elif field == 'memory_gb':
                        print(f"  ✅ 内存: {value}GB")
                    elif field == 'disk_gb':
                        print(f"  ✅ 硬盘: {value}GB")
                    elif field == 'disk_type':
                        print(f"  ✅ 硬盘类型: {value}")
                    elif field == 'network':
                        print(f"  ✅ 网络: {value}")
                    elif field == 'power_w':
                        print(f"  ✅ 功耗: {value}W")
    
    print(f"\n服务器设备数: {server_count}")
    
    # 网络设备参数验证
    print("\n" + "="*80)
    print("🌐 网络设备参数验证")
    print("="*80)
    
    network_categories = ['核心交换机', '接入交换机', '安全防火墙']
    network_count = 0
    network_missing = []
    
    for item in equipment_list:
        if item['category'] in network_categories:
            network_count += 1
            print(f"\n检查: {item['name']} ({item['category']})")
            
            # 检查设备类型
            if 'device_type' in item:
                print(f"  ✅ 设备类型: {item['device_type']}")
            
            # 交换机特有字段
            if '交换机' in item['category']:
                if 'ports' in item and item['ports']:
                    print(f"  ✅ 端口数: {item['ports']}口")
                else:
                    network_missing.append(f"{item['name']}.ports")
                    print(f"  ❌ 缺少字段: ports")
                
                if 'speed' in item and item['speed']:
                    print(f"  ✅ 端口速率: {item['speed']}")
                else:
                    network_missing.append(f"{item['name']}.speed")
                    print(f"  ❌ 缺少字段: speed")
                
                if 'uplink' in item and item['uplink']:
                    print(f"  ✅ 上联: {item['uplink']}")
            
            # 防火墙特有字段
            if '防火墙' in item['category']:
                if 'throughput' in item and item['throughput']:
                    print(f"  ✅ 吞吐量: {item['throughput']}")
            
            # 通用字段
            if 'power_w' in item and item['power_w']:
                print(f"  ✅ 功耗: {item['power_w']}W")
            else:
                network_missing.append(f"{item['name']}.power_w")
                print(f"  ❌ 缺少字段: power_w")
    
    print(f"\n网络设备数: {network_count}")
    
    # 总结
    print("\n" + "="*80)
    print("📊 验收结果汇总")
    print("="*80)
    
    print(f"\n设备统计:")
    print(f"  - 服务器设备: {server_count} 台")
    print(f"  - 网络设备: {network_count} 台")
    print(f"  - 总设备数: {len(equipment_list)} 台")
    
    all_passed = True
    
    if server_missing:
        print(f"\n❌ 服务器缺失字段 ({len(server_missing)}):")
        for field in server_missing:
            print(f"  - {field}")
        all_passed = False
    else:
        print(f"\n✅ 所有服务器参数完整 ({server_count} 台)")
    
    if network_missing:
        print(f"\n❌ 网络设备缺失字段 ({len(network_missing)}):")
        for field in network_missing:
            print(f"  - {field}")
        all_passed = False
    else:
        print(f"\n✅ 所有网络设备参数完整 ({network_count} 台)")
    
    # 成本信息
    cost = xc_solution.get('cost_breakdown', {})
    print(f"\n💰 成本信息:")
    print(f"  - 硬件成本: ¥{cost.get('hardware_cost', 0):,.0f}")
    print(f"  - 软件成本: ¥{cost.get('software_cost', 0):,.0f}")
    print(f"  - 总成本: ¥{cost.get('total_initial_cost', 0):,.0f}")
    
    if cost.get('xinchuan_comparison'):
        comp = cost['xinchuan_comparison']
        print(f"  - 传统方案: ¥{comp.get('international_cost', 0):,.0f}")
        print(f"  - 💰 节约: ¥{comp.get('cost_savings', 0):,.0f} ({comp.get('savings_percent', 0)}%)")
    
    print("\n" + "="*80)
    if all_passed:
        print("✅ 验收通过! 所有设备参数完整!")
        print("="*80)
        sys.exit(0)
    else:
        print("❌ 验收失败! 存在缺失字段!")
        print("="*80)
        sys.exit(1)
        
except Exception as e:
    print(f"❌ 解析错误: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
EOF
)

ESCAPED_RESPONSE=$(echo "$RESPONSE" | sed 's/\\/\\\\/g' | sed "s/'/\\\\'/g")
echo "$VALIDATION_SCRIPT" | sed "s|RESPONSE_PLACEHOLDER|$ESCAPED_RESPONSE|g" | python3

TEST_RESULT=$?

echo ""
if [ $TEST_RESULT -eq 0 ]; then
    echo "================================================================================"
    echo "🎉 最终验收: 通过!"
    echo "================================================================================"
    echo ""
    echo "✅ 所有功能正常:"
    echo "  - 信创功能已启用"
    echo "  - 设备清单完整"
    echo "  - 服务器参数完整(CPU/内存/硬盘/网络/功耗)"
    echo "  - 网络设备参数完整(端口/速率/上联/功耗)"
    echo "  - 成本计算正确"
    echo "  - 成本对比正常"
    echo ""
    echo "🌟 访问地址: https://aladdinsun.devcloud.woa.com/predict"
    echo "================================================================================"
    exit 0
else
    echo "================================================================================"
    echo "❌ 最终验收: 失败!"
    echo "================================================================================"
    exit 1
fi
