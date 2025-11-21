#!/bin/bash

echo "🚀 启动 TDSQL 架构智能预测系统..."
echo ""

# 检查Python版本
echo "📌 检查Python环境..."
python3 --version

# 检查依赖
echo ""
echo "📦 检查依赖包..."
pip3 list | grep -E "Flask|torch|Pillow|pandas|numpy|opencv-python|pytesseract|openpyxl|scikit-learn|transformers|easyocr|matplotlib" || {
    echo "⚠️  部分依赖未安装，正在安装..."
    pip3 install -r requirements.txt
}

# 创建必要的目录
echo ""
echo "📁 创建必要目录..."
mkdir -p uploads
mkdir -p model_libraries
mkdir -p static
mkdir -p templates

# 启动Flask应用
echo ""
echo "✅ 启动Web服务..."
echo "🌐 访问地址: http://127.0.0.1:5000"
echo "📊 系统功能:"
echo "   - 智能架构预测"
echo "   - 图像表格识别"
echo "   - 自我学习优化"
echo "   - 模型库管理"
echo "   - 150+专业参数"
echo ""
echo "按 Ctrl+C 停止服务"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 启动应用
python3 app_with_learning.py
