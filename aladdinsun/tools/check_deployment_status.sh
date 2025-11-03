#!/bin/bash

################################################################################
# 部署状态检查脚本
# 用于检查后台部署进度
################################################################################

WORK_DIR="/data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb"
DEPLOY_OUTPUT="/data/workspace/tencent_CodeBuddy/aladdinsun/tools/deploy_output.log"

echo "=========================================="
echo "IoTDB 集群部署状态检查"
echo "=========================================="
echo ""

# 检查部署进程
echo "📌 部署进程状态:"
if ps aux | grep deploy_iotdb_background | grep -v grep > /dev/null; then
    echo "✅ 部署脚本正在运行中..."
    ps aux | grep deploy_iotdb_background | grep -v grep
else
    echo "⚠️  部署脚本已完成或未运行"
fi

echo ""
echo "=========================================="
echo ""

# 检查 IoTDB 进程
echo "📌 IoTDB 进程状态:"
cn_count=$(ps aux | grep ConfigNode | grep -v grep | wc -l)
dn_count=$(ps aux | grep DataNode | grep -v grep | wc -l)

echo "ConfigNode 进程数: $cn_count / 3"
echo "DataNode 进程数: $dn_count / 6"

if [ "$cn_count" -eq 3 ] && [ "$dn_count" -eq 6 ]; then
    echo "✅ 所有节点已启动"
else
    echo "⚠️  部分节点未启动，部署可能仍在进行中"
fi

echo ""
echo "=========================================="
echo ""

# 检查端口监听
echo "📌 端口监听状态:"
listening_ports=0
for port in 6667 6668 6669 6670 6671 6672 10710 10711 10712; do
    if netstat -tlnp 2>/dev/null | grep -q ":$port "; then
        echo "✅ 端口 $port: 监听中"
        ((listening_ports++))
    else
        echo "⏳ 端口 $port: 未监听"
    fi
done

echo ""
echo "监听端口数: $listening_ports / 9"

echo ""
echo "=========================================="
echo ""

# 显示最新日志
echo "📌 最新部署日志 (最后 20 行):"
if [ -f "$DEPLOY_OUTPUT" ]; then
    tail -20 "$DEPLOY_OUTPUT"
else
    echo "日志文件不存在"
fi

echo ""
echo "=========================================="
echo ""

# 检查生成的文档
echo "📌 生成的文档:"
if [ -d "$WORK_DIR" ]; then
    ls -lh "$WORK_DIR"/*.md 2>/dev/null | tail -10 || echo "暂无文档生成"
else
    echo "工作目录不存在"
fi

echo ""
echo "=========================================="
echo ""

# 部署进度估算
if ps aux | grep deploy_iotdb_background | grep -v grep > /dev/null; then
    echo "📊 部署状态: 🔄 进行中"
    echo "预计剩余时间: 请查看日志了解详情"
elif [ "$cn_count" -eq 3 ] && [ "$dn_count" -eq 6 ]; then
    echo "📊 部署状态: ✅ 已完成"
    echo ""
    echo "🎉 集群部署成功！"
    echo ""
    echo "📄 查看部署报告:"
    echo "   ls -lh $WORK_DIR/DEPLOYMENT_REPORT_*.md"
    echo ""
    echo "📖 查看维护手册:"
    echo "   ls -lh $WORK_DIR/MAINTENANCE_MANUAL_*.md"
    echo ""
    echo "📋 查看设备清单:"
    echo "   ls -lh $WORK_DIR/EQUIPMENT_INVENTORY_*.md"
    echo ""
    echo "🔗 连接集群:"
    echo "   $WORK_DIR/apache-iotdb-1.3.2-all-bin/sbin/start-cli.sh -h 127.0.0.1 -p 6667"
else
    echo "📊 部署状态: ⚠️  异常"
    echo "请检查日志: tail -100 $DEPLOY_OUTPUT"
fi

echo ""
echo "=========================================="
echo ""
echo "💡 提示:"
echo "   - 实时查看日志: tail -f $DEPLOY_OUTPUT"
echo "   - 再次检查状态: bash $0"
echo "   - 查看完整日志: cat $WORK_DIR/deployment_*.log"
echo ""
