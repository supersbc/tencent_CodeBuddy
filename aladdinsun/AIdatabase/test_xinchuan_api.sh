#!/bin/bash
# 测试信创模式API

echo "=========================================="
echo "测试信创模式部署预测 API"
echo "=========================================="

curl -X POST http://localhost:18080/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "data_volume": 5,
    "qps": 5000,
    "tps": 1500,
    "concurrent_users": 2000,
    "industry": "finance",
    "need_high_availability": true,
    "enable_xinchuan": true,
    "xinchuan_mode": "standard"
  }' 2>&1 | python3 -m json.tool

echo ""
echo "=========================================="
echo "测试完成"
echo "=========================================="
