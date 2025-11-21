#!/bin/bash

# TDSQL 部署资源预测系统 - DevCloud 部署脚本

set -e

echo "======================================"
echo "🚀 开始部署到 DevCloud"
echo "======================================"

# 1. 检查必要文件
echo "📋 检查文件..."
if [ ! -f "app_simple.py" ]; then
    echo "❌ 错误: app_simple.py 不存在"
    exit 1
fi

# 2. 验证Python语法
echo "🔍 验证Python语法..."
python -m py_compile app_simple.py
if [ $? -eq 0 ]; then
    echo "✅ Python语法检查通过"
else
    echo "❌ Python语法错误，请修复后再部署"
    exit 1
fi

# 3. 停止旧服务
echo "🛑 停止旧服务..."
pkill -f "python.*app_simple" || true
sleep 2

# 4. 备份日志
if [ -f "app.log" ]; then
    echo "💾 备份旧日志..."
    mv app.log "app.log.$(date +%Y%m%d_%H%M%S).bak"
fi

# 5. 启动新服务
echo "🚀 启动服务..."
nohup python app_simple.py > app.log 2>&1 &

# 6. 等待启动
echo "⏳ 等待服务启动..."
sleep 5

# 7. 检查服务状态
if pgrep -f "python.*app_simple" > /dev/null; then
    echo "✅ 服务启动成功！"
    echo ""
    echo "======================================"
    echo "📊 服务信息"
    echo "======================================"
    echo "进程ID: $(pgrep -f 'python.*app_simple')"
    echo "端口: 18080"
    echo "日志文件: app.log"
    echo ""
    echo "🌐 访问地址:"
    echo "  - 本地: http://127.0.0.1:18080"
    echo "  - DevCloud: https://aladdinsun.devcloud.woa.com/"
    echo ""
    echo "📝 查看日志:"
    echo "  tail -f app.log"
    echo "======================================"
    
    # 显示最近的日志
    echo ""
    echo "📋 最新日志:"
    tail -20 app.log
else
    echo "❌ 服务启动失败！"
    echo ""
    echo "错误日志:"
    cat app.log
    exit 1
fi
