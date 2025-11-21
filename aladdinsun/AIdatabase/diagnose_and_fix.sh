#!/bin/bash

echo "=========================================="
echo "🔧 AIdatabase 服务诊断与修复工具"
echo "=========================================="
echo ""

cd /data/workspace/tencent_CodeBuddy/aladdinsun/AIdatabase

# 1. 检查Python环境
echo "📌 步骤1: 检查Python环境"
echo "----------------------------------------"
python3 --version
pip3 --version
echo ""

# 2. 检查并安装依赖
echo "📌 步骤2: 检查Flask依赖"
echo "----------------------------------------"
if python3 -c "import flask" 2>/dev/null; then
    echo "✅ Flask 已安装"
    python3 -c "import flask; print('   版本:', flask.__version__)"
else
    echo "❌ Flask 未安装，正在安装基础依赖..."
    pip3 install Flask==3.0.0 -i https://mirrors.tencent.com/pypi/simple/
fi
echo ""

# 3. 停止旧进程
echo "📌 步骤3: 停止旧进程"
echo "----------------------------------------"
pkill -f app_simple.py 2>/dev/null && echo "✅ 已停止旧的Flask进程" || echo "⚠️  没有运行中的Flask进程"
pkill -f nginx 2>/dev/null && echo "✅ 已停止Nginx进程" || echo "⚠️  没有运行中的Nginx进程"
sleep 2
echo ""

# 4. 检查端口占用
echo "📌 步骤4: 检查端口占用"
echo "----------------------------------------"
if ss -tlnp 2>/dev/null | grep -q ":18080"; then
    echo "⚠️  端口18080已被占用:"
    ss -tlnp | grep ":18080"
    echo "尝试释放..."
    fuser -k 18080/tcp 2>/dev/null
else
    echo "✅ 端口18080空闲"
fi

if ss -tlnp 2>/dev/null | grep -q ":80 "; then
    echo "⚠️  端口80已被占用:"
    ss -tlnp | grep ":80 "
else
    echo "✅ 端口80空闲"
fi
echo ""

# 5. 创建简化版启动脚本(不依赖nginx)
echo "📌 步骤5: 创建简化启动脚本"
echo "----------------------------------------"
cat > start_simple_standalone.sh << 'EOF'
#!/bin/bash
cd /data/workspace/tencent_CodeBuddy/aladdinsun/AIdatabase
echo "🚀 启动AIdatabase服务(独立模式,端口5000)..."
nohup python3 -u app_simple.py > app.log 2>&1 &
echo "PID: $!"
sleep 3
if ss -tlnp 2>/dev/null | grep -q ":5000"; then
    echo "✅ 服务启动成功!"
    echo "📍 访问地址: http://localhost:5000"
    ss -tlnp | grep ":5000"
else
    echo "❌ 服务启动失败,查看日志:"
    tail -20 app.log
fi
EOF
chmod +x start_simple_standalone.sh
echo "✅ 已创建 start_simple_standalone.sh"
echo ""

# 6. 检查app_simple.py配置
echo "📌 步骤6: 检查app_simple.py配置"
echo "----------------------------------------"
if grep -q "app.run" app_simple.py; then
    echo "✅ 发现启动配置:"
    grep -A 3 "if __name__" app_simple.py | tail -5
else
    echo "⚠️  未找到标准启动配置"
fi
echo ""

# 7. 测试Flask导入
echo "📌 步骤7: 测试Python导入"
echo "----------------------------------------"
python3 << 'PYEOF'
try:
    from flask import Flask
    print("✅ Flask导入成功")
    
    import os
    if os.path.exists('deployment_predictor.py'):
        print("✅ 找到 deployment_predictor.py")
    
    if os.path.exists('model_library_manager.py'):
        print("✅ 找到 model_library_manager.py")
        
    if os.path.exists('templates'):
        print("✅ 找到 templates 目录")
        
    print("✅ 基础依赖检查通过")
except Exception as e:
    print(f"❌ 导入失败: {e}")
PYEOF
echo ""

# 8. 尝试启动服务
echo "📌 步骤8: 尝试启动服务"
echo "----------------------------------------"
echo "正在后台启动Flask应用..."
nohup python3 -u app_simple.py > app.log 2>&1 &
FLASK_PID=$!
echo "Flask PID: $FLASK_PID"
sleep 5

# 检查启动状态
if ps -p $FLASK_PID > /dev/null 2>&1; then
    echo "✅ Flask进程运行中 (PID: $FLASK_PID)"
    
    if ss -tlnp 2>/dev/null | grep -q ":18080\|:5000"; then
        echo "✅ 端口监听成功:"
        ss -tlnp | grep -E ":18080|:5000"
        
        # 测试HTTP访问
        sleep 2
        if curl -s http://localhost:5000 > /dev/null 2>&1; then
            echo "✅ HTTP服务响应正常"
        elif curl -s http://localhost:18080 > /dev/null 2>&1; then
            echo "✅ HTTP服务响应正常 (端口18080)"
        else
            echo "⚠️  HTTP服务未响应,查看日志:"
            tail -30 app.log
        fi
    else
        echo "⚠️  端口未监听,查看日志:"
        tail -30 app.log
    fi
else
    echo "❌ Flask进程未运行,查看错误日志:"
    tail -50 app.log
fi
echo ""

# 9. 总结
echo "=========================================="
echo "📊 诊断总结"
echo "=========================================="
echo ""
echo "运行中的进程:"
ps aux | grep -E "app_simple|nginx" | grep -v grep
echo ""
echo "监听的端口:"
ss -tlnp 2>/dev/null | grep -E ":80 |:5000|:18080" || netstat -tlnp 2>/dev/null | grep -E ":80 |:5000|:18080"
echo ""
echo "最新日志 (app.log 最后10行):"
tail -10 app.log 2>/dev/null || echo "日志文件不存在"
echo ""
echo "=========================================="
echo "🎯 下一步操作建议:"
echo "=========================================="
echo "1. 查看完整日志: tail -f app.log"
echo "2. 重启服务: bash start_simple_standalone.sh"
echo "3. 检查nginx配置: nginx -t"
echo "4. 手动测试: python3 app_simple.py"
echo "=========================================="
