#!/bin/bash

echo "======================================"
echo "🧪 TDSQL v3.2 融合版功能测试"
echo "======================================"
echo ""

# 测试 1: 健康检查
echo "测试 1: 健康检查"
echo "--------------------------------------"
curl -s http://127.0.0.1:5173/api/health | python3 -m json.tool
echo ""

# 测试 2: 获取参数配置（简化模式）
echo "测试 2: 获取参数配置（简化模式）"
echo "--------------------------------------"
curl -s "http://127.0.0.1:5173/api/parameter_config?mode=simplified" | python3 -m json.tool | head -30
echo "... (已截断)"
echo ""

# 测试 3: 文件上传识别
echo "测试 3: 文件上传识别（JSON）"
echo "--------------------------------------"
if [ -f "test_config.json" ]; then
    curl -s -X POST -F "file=@test_config.json" http://127.0.0.1:5173/api/analyze | python3 -m json.tool | head -40
    echo "... (已截断)"
else
    echo "⚠️ 测试文件不存在"
fi
echo ""

# 测试 4: 手动输入分析
echo "测试 4: 手动输入分析"
echo "--------------------------------------"
curl -s -X POST http://127.0.0.1:5173/api/predict \
  -H "Content-Type: application/json" \
  -d '{"industry":"电商","qps":10000,"data_volume":200,"concurrent_users":5000,"availability":99.95}' \
  | python3 -m json.tool | head -30
echo "... (已截断)"
echo ""

echo "======================================"
echo "✅ 测试完成"
echo "======================================"
echo ""
echo "🌐 访问地址:"
echo "  - 新版界面: http://127.0.0.1:5173"
echo "  - 旧版界面: http://127.0.0.1:5173/old"
echo "  - 测试页面: http://127.0.0.1:5173/test_upload.html"
echo ""
