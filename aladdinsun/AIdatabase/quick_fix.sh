#!/bin/bash

echo "=========================================="
echo "🔧 AIdatabase 快速修复工具"
echo "=========================================="
echo ""

cd /data/workspace/tencent_CodeBuddy/aladdinsun/AIdatabase

# 1. 停止旧进程
echo "📌 步骤1: 停止旧进程"
pkill -f app_simple.py 2>/dev/null && echo "   ✅ 已停止Flask进程" || echo "   ⚠️  无运行中的Flask进程"
pkill nginx 2>/dev/null && echo "   ✅ 已停止Nginx进程" || echo "   ⚠️  无运行中的Nginx进程"
sleep 2
echo ""

# 2. 检查Flask是否安装
echo "📌 步骤2: 检查Flask环境"
if python3 -c "import flask" 2>/dev/null; then
    VERSION=$(python3 -c "import flask; print(flask.__version__)" 2>/dev/null)
    echo "   ✅ Flask已安装 (版本: $VERSION)"
else
    echo "   ❌ Flask未安装,正在安装..."
    pip3 install Flask==3.0.0 Werkzeug pandas openpyxl numpy scikit-learn -i https://mirrors.tencent.com/pypi/simple/ --quiet
    if [ $? -eq 0 ]; then
        echo "   ✅ Flask安装成功"
    else
        echo "   ❌ Flask安装失败,请手动安装: pip3 install Flask"
        exit 1
    fi
fi
echo ""

# 3. 启动Flask应用
echo "📌 步骤3: 启动Flask应用"
nohup python3 -u app_simple.py > app.log 2>&1 &
FLASK_PID=$!
echo "   Flask PID: $FLASK_PID"
sleep 5

# 检查Flask是否成功启动
if ps -p $FLASK_PID > /dev/null 2>&1; then
    echo "   ✅ Flask进程运行中"
    
    # 检查端口
    if ss -tlnp 2>/dev/null | grep -qE ":18080|:5000"; then
        PORT=$(ss -tlnp 2>/dev/null | grep -oE ":(18080|5000)" | head -1 | tr -d ':')
        echo "   ✅ Flask监听端口: $PORT"
        
        # 测试HTTP响应
        sleep 2
        if curl -s http://localhost:$PORT >/dev/null 2>&1; then
            echo "   ✅ HTTP服务响应正常"
        else
            echo "   ⚠️  HTTP服务可能需要更多时间初始化"
        fi
    else
        echo "   ⚠️  Flask未监听端口,查看日志:"
        tail -20 app.log
        exit 1
    fi
else
    echo "   ❌ Flask启动失败,错误日志:"
    tail -30 app.log
    exit 1
fi
echo ""

# 4. 启动Nginx
echo "📌 步骤4: 启动Nginx反向代理"
if command -v nginx >/dev/null 2>&1; then
    nginx 2>/dev/null
    sleep 2
    
    if ss -tlnp 2>/dev/null | grep -q ":80 "; then
        echo "   ✅ Nginx启动成功(端口80)"
    else
        echo "   ⚠️  Nginx启动失败或未监听80端口"
        echo "   提示: 可能需要sudo权限或配置有问题"
        echo "   运行: sudo nginx -t 检查配置"
    fi
else
    echo "   ⚠️  未找到Nginx,跳过"
fi
echo ""

# 5. 显示状态总结
echo "=========================================="
echo "📊 服务状态"
echo "=========================================="
echo ""

echo "运行中的进程:"
ps aux | grep -E "app_simple|nginx" | grep -v grep | awk '{printf "   PID: %-7s %s\n", $2, $11}' || echo "   无"
echo ""

echo "监听的端口:"
ss -tlnp 2>/dev/null | grep -E ":80 |:5000|:18080" | awk '{print "   "$1" "$4}' || echo "   无"
echo ""

echo "最新日志(最后5行):"
tail -5 app.log 2>/dev/null | sed 's/^/   /' || echo "   日志文件不存在"
echo ""

# 6. 访问指南
echo "=========================================="
echo "🎯 访问指南"
echo "=========================================="
if ss -tlnp 2>/dev/null | grep -q ":80 "; then
    echo "✅ 完整访问(通过Nginx):"
    echo "   📍 http://aladdinsun.devcloud.woa.com"
    echo "   📍 https://aladdinsun.devcloud.woa.com (如果配置了SSL)"
elif ss -tlnp 2>/dev/null | grep -qE ":18080|:5000"; then
    PORT=$(ss -tlnp 2>/dev/null | grep -oE ":(18080|5000)" | head -1 | tr -d ':')
    echo "⚠️  仅Flask直接访问(Nginx未启动):"
    echo "   📍 http://服务器IP:$PORT"
    echo "   📍 http://localhost:$PORT (本地)"
else
    echo "❌ 服务未正常启动,请查看日志:"
    echo "   tail -f app.log"
fi
echo ""

echo "=========================================="
echo "🛠️  其他命令"
echo "=========================================="
echo "查看日志:  tail -f app.log"
echo "停止服务:  pkill -f app_simple.py && pkill nginx"
echo "重启服务:  bash quick_fix.sh"
echo "手动启动:  python3 app_simple.py"
echo "=========================================="
