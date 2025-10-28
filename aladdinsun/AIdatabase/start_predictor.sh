#!/bin/bash

echo "=========================================="
echo "🚀 TDSQL 部署资源预测系统 v4.0"
echo "=========================================="
echo ""

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3"
    echo "请先安装 Python 3.7+"
    exit 1
fi

echo "✅ Python 环境检查通过"

# 检查并安装依赖
echo ""
echo "📦 检查依赖包..."

if [ ! -f "requirements.txt" ]; then
    echo "⚠️  未找到 requirements.txt，创建基础依赖文件..."
    cat > requirements.txt << EOF
Flask==2.3.0
openpyxl==3.1.2
Pillow==10.0.0
PyPDF2==3.0.1
pytesseract==0.3.10
Werkzeug==2.3.0
EOF
fi

# 安装依赖
pip3 install -r requirements.txt

echo ""
echo "=========================================="
echo "🌟 启动服务..."
echo "=========================================="
echo ""

# 启动应用
python3 app.py
