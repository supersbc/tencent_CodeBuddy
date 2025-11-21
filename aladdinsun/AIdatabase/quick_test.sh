#!/bin/bash
echo "========================================="
echo "快速测试预测API"
echo "========================================="
echo ""

echo "测试URL: http://localhost:18080/api/predict"
echo "测试数据: 1000GB, 5000 QPS, 200并发用户, 启用信创"
echo ""

curl -X POST http://localhost:18080/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "total_data_size_gb": 1000,
    "qps": 5000,
    "concurrent_users": 200,
    "enable_xinchuan": true,
    "xinchuan_mode": "standard"
  }' 2>/dev/null | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    if data.get('success'):
        print('✅ API调用成功!')
        result = data['data']
        print(f\"  - xinchuan_enabled: {result.get('xinchuan_enabled')}\")
        print(f\"  - traditional_solution: {'存在' if 'traditional_solution' in result else '不存在'}\")
        print(f\"  - xinchuan_solution: {'存在' if 'xinchuan_solution' in result else '不存在'}\")
        if 'traditional_solution' in result:
            print(f\"  - 传统方案设备数: {len(result['traditional_solution'].get('equipment_list', []))}\")
        if 'xinchuan_solution' in result:
            print(f\"  - 信创方案设备数: {len(result['xinchuan_solution'].get('equipment_list', []))}\")
    else:
        print('❌ API返回失败')
        print(f\"  错误: {data.get('error')}\")
except Exception as e:
    print(f'❌ 错误: {e}')
    import traceback
    traceback.print_exc()
"

echo ""
echo "========================================="
