#!/bin/bash

echo "=========================================="
echo "🚀 启动 TDSQL 部署资源预测系统"
echo "=========================================="

# 停止旧进程
echo "📌 停止旧进程..."
pkill -f app_simple.py
pkill nginx
sleep 2

# 启动 Flask 应用
echo "📌 启动 Flask 应用（端口 18080）..."
cd /data/workspace/tencent_CodeBuddy/aladdinsun/AIdatabase
nohup python3 app_simple.py > app.log 2>&1 &
sleep 3

# 检查 Flask 是否启动成功
if ss -tlnp | grep -q 18080; then
    echo "✅ Flask 应用启动成功（端口 18080）"
else
    echo "❌ Flask 应用启动失败"
    exit 1
fi

# 启动 Nginx
echo "📌 启动 Nginx（端口 80）..."
nginx

# 检查 Nginx 是否启动成功
if ss -tlnp | grep -q ":80"; then
    echo "✅ Nginx 启动成功（端口 80）"
else
    echo "❌ Nginx 启动失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 所有服务启动成功！"
echo "=========================================="
echo ""
echo "📍 访问地址："
echo "  - http://aladdinsun.devcloud.woa.com"
echo "  - http://21.91.205.22"
echo ""
echo "📊 服务状态："
echo "  - Flask 应用：端口 18080"
echo "  - Nginx 反向代理：端口 80"
echo ""
echo "🔧 管理命令："
echo "  - 查看 Flask 日志：tail -f app.log"
echo "  - 查看 Nginx 日志：tail -f /var/log/nginx/tdsql_access.log"
echo "  - 重启服务：bash start_with_nginx.sh"
echo "=========================================="
