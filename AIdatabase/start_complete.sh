#!/bin/bash

echo "============================================================"
echo "🚀 TDSQL 部署资源预测系统 v4.2 启动脚本"
echo "============================================================"

# 检查Python版本
echo ""
echo "📍 检查Python环境..."
python3 --version

# 检查依赖
echo ""
echo "📍 检查依赖库..."
python3 -c "import flask; print('✅ Flask已安装')" 2>/dev/null || echo "❌ Flask未安装，请运行: pip install flask"
python3 -c "import werkzeug; print('✅ Werkzeug已安装')" 2>/dev/null || echo "❌ Werkzeug未安装，请运行: pip install werkzeug"

# 可选依赖检查
echo ""
echo "📍 检查可选依赖..."
python3 -c "import openpyxl; print('✅ openpyxl已安装 - Excel支持可用')" 2>/dev/null || echo "ℹ️  openpyxl未安装 - Excel支持不可用"
python3 -c "import pytesseract; print('✅ pytesseract已安装 - OCR支持可用')" 2>/dev/null || echo "ℹ️  pytesseract未安装 - OCR支持不可用"
python3 -c "import PyPDF2; print('✅ PyPDF2已安装 - PDF支持可用')" 2>/dev/null || echo "ℹ️  PyPDF2未安装 - PDF支持不可用"

# 停止旧服务
echo ""
echo "📍 停止旧服务..."
lsof -ti:5173 | xargs kill -9 2>/dev/null && echo "✅ 已停止旧服务" || echo "ℹ️  没有运行中的服务"

# 启动服务
echo ""
echo "📍 启动服务..."
python3 app_simple.py > server.log 2>&1 &
PID=$!

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 3

# 检查服务状态
if ps -p $PID > /dev/null; then
    echo ""
    echo "============================================================"
    echo "✅ 服务启动成功！"
    echo "============================================================"
    echo ""
    echo "🌐 访问地址:"
    echo "   导航页面: http://127.0.0.1:5173/nav"
    echo "   主页面: http://127.0.0.1:5173"
    echo "   模型库: http://127.0.0.1:5173/model_library"
    echo "   学习系统: http://127.0.0.1:5173/learning"
    echo ""
    echo "📊 服务信息:"
    echo "   进程ID: $PID"
    echo "   日志文件: server.log"
    echo ""
    echo "📝 功能模块:"
    echo "   ✅ 部署资源预测 - 智能分析生成部署方案"
    echo "   ✅ 模型库管理 - 下载和管理预训练模型"
    echo "   ✅ 自主训练 - 从实际案例中学习优化"
    echo "   ✅ 文件上传 - 支持多种格式自动解析"
    echo ""
    echo "🛑 停止服务:"
    echo "   lsof -ti:5173 | xargs kill -9"
    echo ""
    echo "📚 查看日志:"
    echo "   tail -f server.log"
    echo ""
    echo "🧪 运行测试:"
    echo "   python3 test_all_features.py"
    echo ""
    echo "============================================================"
else
    echo ""
    echo "❌ 服务启动失败！"
    echo "请查看日志: tail -50 server.log"
    exit 1
fi
