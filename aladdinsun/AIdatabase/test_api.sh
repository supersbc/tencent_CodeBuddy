#!/bin/bash
# 测试预测API

echo "========================================="
echo "测试TDSQL部署资源预测API"
echo "========================================="
echo ""

echo "1. 测试基本预测(不含信创)..."
curl -X POST http://localhost:18080/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "total_data_size_gb": 1000,
    "qps": 5000,
    "concurrent_users": 200,
    "enable_xinchuan": false
  }' | python3 -m json.tool | head -50

echo ""
echo ""
echo "2. 测试信创方案对比..."
curl -X POST http://localhost:18080/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "total_data_size_gb": 1000,
    "qps": 5000,
    "concurrent_users": 200,
    "enable_xinchuan": true,
    "xinchuan_mode": "standard"
  }' | python3 -c "import json,sys; r=json.load(sys.stdin); print('成功!' if r.get('success') else '失败:'+r.get('error','')); print('包含traditional_solution:', 'traditional_solution' in r.get('data',{})); print('包含xinchuan_solution:', 'xinchuan_solution' in r.get('data',{}))"

echo ""
echo "========================================="
echo "测试完成!"
echo "========================================="
