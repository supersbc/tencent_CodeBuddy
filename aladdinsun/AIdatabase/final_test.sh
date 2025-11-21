#!/bin/bash
echo "=========================================="
echo "🧪 全面功能测试"
echo "=========================================="

# 1. 健康检查
echo ""
echo "1️⃣ 健康检查..."
HEALTH=$(curl -s http://localhost:18080/api/health)
if [[ $HEALTH == *"ok"* ]]; then
    echo "   ✅ 健康检查通过"
else
    echo "   ❌ 健康检查失败"
    exit 1
fi

# 2. 信创预测测试
echo ""
echo "2️⃣ 信创预测测试..."
RESULT=$(curl -s -X POST http://localhost:18080/api/predict \
  -H "Content-Type: application/json" \
  -d '{"data_volume": 5, "enable_xinchuan": true, "xinchuan_mode": "standard"}')

if [[ $RESULT == *"xinchuan_enabled"* ]] && [[ $RESULT == *"success"* ]]; then
    echo "   ✅ 信创预测功能正常"
else
    echo "   ❌ 信创预测功能异常"
    exit 1
fi

# 3. 检查日志错误
echo ""
echo "3️⃣ 检查日志错误..."
ERRORS=$(tail -100 app.log | grep -E "OpenBLAS.*failed|Error|Exception|Traceback" | grep -v "WARNING")
if [ -z "$ERRORS" ]; then
    echo "   ✅ 日志无错误"
else
    echo "   ⚠️  发现日志错误:"
    echo "$ERRORS"
fi

# 4. 进程状态
echo ""
echo "4️⃣ 进程状态..."
FLASK_PID=$(ps aux | grep "python3 app_simple.py" | grep -v grep | awk '{print $2}')
NGINX_PID=$(ps aux | grep "nginx: master" | grep -v grep | awk '{print $2}')

if [ ! -z "$FLASK_PID" ]; then
    echo "   ✅ Flask运行正常 (PID: $FLASK_PID)"
else
    echo "   ❌ Flask未运行"
    exit 1
fi

if [ ! -z "$NGINX_PID" ]; then
    echo "   ✅ Nginx运行正常 (PID: $NGINX_PID)"
else
    echo "   ⚠️  Nginx未运行"
fi

echo ""
echo "=========================================="
echo "✅ 所有测试通过！"
echo "=========================================="
echo "📍 访问地址: https://aladdinsun.devcloud.woa.com"
echo "=========================================="
