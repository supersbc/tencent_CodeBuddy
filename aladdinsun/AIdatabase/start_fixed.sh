#!/bin/bash
# 修复OpenBLAS线程资源问题并启动服务

echo "=========================================="
echo "🔧 修复并启动 AIdatabase 服务"
echo "=========================================="

# 1. 停止旧进程
echo "📌 停止旧进程..."
pkill -f app_simple.py
sleep 2

# 2. 设置环境变量限制OpenBLAS线程数
export OPENBLAS_NUM_THREADS=4
export OMP_NUM_THREADS=4
export MKL_NUM_THREADS=4

echo "✅ 已设置线程限制:"
echo "   OPENBLAS_NUM_THREADS=4"
echo "   OMP_NUM_THREADS=4"
echo "   MKL_NUM_THREADS=4"

# 3. 启动Flask应用
echo ""
echo "🚀 启动Flask应用..."
cd /data/workspace/tencent_CodeBuddy/aladdinsun/AIdatabase
nohup python3 app_simple.py > app.log 2>&1 &

sleep 4

# 4. 检查状态
echo ""
echo "📊 服务状态检查..."
PID=$(ps aux | grep "python3 app_simple.py" | grep -v grep | awk '{print $2}')

if [ ! -z "$PID" ]; then
    echo "✅ Flask服务启动成功! (PID: $PID)"
    echo "   监听端口: 18080"
    
    # 测试连接
    sleep 2
    RESPONSE=$(curl -s http://localhost:18080/api/health 2>&1)
    if [[ $RESPONSE == *"ok"* ]]; then
        echo "✅ 健康检查通过"
    else
        echo "⚠️  健康检查失败，但进程已启动"
    fi
else
    echo "❌ Flask服务启动失败!"
    echo "查看日志: tail -50 app.log"
    exit 1
fi

# 5. 检查Nginx
NGINX_PID=$(ps aux | grep "nginx: master" | grep -v grep | awk '{print $2}')
if [ ! -z "$NGINX_PID" ]; then
    echo "✅ Nginx运行正常 (PID: $NGINX_PID)"
else
    echo "⚠️  Nginx未运行"
fi

echo ""
echo "=========================================="
echo "✅ 服务启动完成!"
echo "=========================================="
echo "📍 访问地址:"
echo "   - 主页: https://aladdinsun.devcloud.woa.com"
echo "   - 预测: https://aladdinsun.devcloud.woa.com/predict"
echo ""
echo "📝 查看日志: tail -f app.log"
echo "=========================================="
