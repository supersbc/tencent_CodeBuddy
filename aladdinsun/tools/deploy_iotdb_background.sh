#!/bin/bash

################################################################################
# IoTDB 生产级集群后台部署脚本
# 版本: v1.0
# 架构: 3 ConfigNode + 6 DataNode
# 特性: 后台运行、详细日志、自动生成文档
################################################################################

set -e

# 配置变量
IOTDB_VERSION="1.3.2"
WORK_DIR="/data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb"
DATA_DIR="/data/workspace/iotdb_data"
IOTDB_HOME="${WORK_DIR}/apache-iotdb-${IOTDB_VERSION}-all-bin"
DEPLOY_LOG="${WORK_DIR}/deployment_$(date +%Y%m%d_%H%M%S).log"
DEPLOY_REPORT="${WORK_DIR}/deployment_report_$(date +%Y%m%d_%H%M%S).md"

# 创建日志目录
mkdir -p "$WORK_DIR"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$DEPLOY_LOG"
}

log_section() {
    echo "" | tee -a "$DEPLOY_LOG"
    echo "========================================" | tee -a "$DEPLOY_LOG"
    echo "$1" | tee -a "$DEPLOY_LOG"
    echo "========================================" | tee -a "$DEPLOY_LOG"
    echo "" | tee -a "$DEPLOY_LOG"
}

# 开始部署
log_section "IoTDB 生产级集群后台部署开始"
log "部署日志: $DEPLOY_LOG"
log "部署报告: $DEPLOY_REPORT"

# 阶段 1: 环境检查
log_section "阶段 1/7: 环境检查"

# 检查 Java
if ! command -v java &> /dev/null; then
    log "ERROR: Java 未安装，开始安装..."
    sudo yum install -y java-11-openjdk java-11-openjdk-devel >> "$DEPLOY_LOG" 2>&1
    log "Java 安装完成"
fi

java_version=$(java -version 2>&1 | head -n 1)
log "Java 版本: $java_version"

# 检查资源
available_space=$(df -BG /codev | tail -1 | awk '{print $4}' | sed 's/G//')
total_mem=$(free -g | grep Mem | awk '{print $2}')
cpu_cores=$(nproc)

log "CPU 核心数: $cpu_cores"
log "总内存: ${total_mem}G"
log "可用磁盘空间: ${available_space}G"

# 阶段 2: 系统优化
log_section "阶段 2/7: 系统参数优化"
ulimit -n 65535
log "文件描述符限制: $(ulimit -n)"

# 阶段 3: 创建目录
log_section "阶段 3/7: 创建目录结构"
mkdir -p "$WORK_DIR"/{scripts,logs,cluster}

for i in {1..3}; do
    mkdir -p "$DATA_DIR/confignode-$i"/{system,consensus}
done

for i in {1..6}; do
    mkdir -p "$DATA_DIR/datanode-$i"/{system,data,consensus,wal}
done

log "目录结构创建完成"

# 阶段 4: 下载 IoTDB
log_section "阶段 4/7: 下载 IoTDB"
cd "$WORK_DIR"

IOTDB_ZIP="apache-iotdb-${IOTDB_VERSION}-all-bin.zip"

if [ ! -f "$IOTDB_ZIP" ]; then
    log "正在下载 IoTDB ${IOTDB_VERSION}..."
    wget -q --show-progress "https://dlcdn.apache.org/iotdb/${IOTDB_VERSION}/${IOTDB_ZIP}" >> "$DEPLOY_LOG" 2>&1
    log "下载完成"
fi

if [ ! -d "$IOTDB_HOME" ]; then
    log "正在解压..."
    unzip -q "$IOTDB_ZIP"
    chmod +x "$IOTDB_HOME/sbin"/*.sh
    log "解压完成"
fi

# 阶段 5: 配置集群
log_section "阶段 5/7: 配置集群"

# ConfigNode 配置
for i in {1..3}; do
    cn_port=$((10710 + i - 1))
    consensus_port=$((10720 + i - 1))
    
    mkdir -p "$WORK_DIR/cluster/confignode-$i/conf"
    
    cat > "$WORK_DIR/cluster/confignode-$i/conf/iotdb-system.properties" << EOF
cn_internal_address=127.0.0.1
cn_internal_port=$cn_port
cn_consensus_port=$consensus_port
cn_seed_config_node=127.0.0.1:10710
cn_system_dir=$DATA_DIR/confignode-$i/system
cn_consensus_dir=$DATA_DIR/confignode-$i/consensus
cn_log_dir=$WORK_DIR/logs/confignode-$i
EOF
    
    cat > "$WORK_DIR/cluster/confignode-$i/conf/confignode-env.sh" << EOF
#!/bin/bash
export MAX_HEAP_SIZE=4G
export HEAP_NEWSIZE=2G
export MAX_DIRECT_MEMORY_SIZE=2G
EOF
    chmod +x "$WORK_DIR/cluster/confignode-$i/conf/confignode-env.sh"
    
    log "ConfigNode-$i 配置完成 (端口: $cn_port)"
done

# DataNode 配置
for i in {1..6}; do
    rpc_port=$((6667 + i - 1))
    internal_port=$((10730 + i - 1))
    mpp_port=$((10740 + i - 1))
    schema_port=$((10750 + i - 1))
    data_port=$((10760 + i - 1))
    
    mkdir -p "$WORK_DIR/cluster/datanode-$i/conf"
    
    cat > "$WORK_DIR/cluster/datanode-$i/conf/iotdb-system.properties" << EOF
dn_rpc_address=127.0.0.1
dn_rpc_port=$rpc_port
dn_internal_address=127.0.0.1
dn_internal_port=$internal_port
dn_mpp_data_exchange_port=$mpp_port
dn_schema_region_consensus_port=$schema_port
dn_data_region_consensus_port=$data_port
dn_seed_config_node=127.0.0.1:10710
dn_system_dir=$DATA_DIR/datanode-$i/system
dn_data_dirs=$DATA_DIR/datanode-$i/data
dn_consensus_dir=$DATA_DIR/datanode-$i/consensus
dn_wal_dirs=$DATA_DIR/datanode-$i/wal
dn_log_dir=$WORK_DIR/logs/datanode-$i
schema_replication_factor=2
data_replication_factor=2
wal_buffer_size=33554432
flush_proportion=0.4
reject_proportion=0.8
EOF
    
    cat > "$WORK_DIR/cluster/datanode-$i/conf/datanode-env.sh" << EOF
#!/bin/bash
export MAX_HEAP_SIZE=16G
export HEAP_NEWSIZE=8G
export MAX_DIRECT_MEMORY_SIZE=8G
EOF
    chmod +x "$WORK_DIR/cluster/datanode-$i/conf/datanode-env.sh"
    
    log "DataNode-$i 配置完成 (RPC端口: $rpc_port)"
done

# 阶段 6: 启动集群
log_section "阶段 6/7: 启动集群"

cd "$IOTDB_HOME"

# 启动 ConfigNode
log "启动 ConfigNode-1 (种子节点)..."
IOTDB_CONF="$WORK_DIR/cluster/confignode-1/conf" ./sbin/start-confignode.sh >> "$DEPLOY_LOG" 2>&1
sleep 10

for i in {2..3}; do
    log "启动 ConfigNode-$i..."
    IOTDB_CONF="$WORK_DIR/cluster/confignode-$i/conf" ./sbin/start-confignode.sh >> "$DEPLOY_LOG" 2>&1
    sleep 5
done

sleep 10

# 启动 DataNode
for i in {1..6}; do
    log "启动 DataNode-$i..."
    IOTDB_CONF="$WORK_DIR/cluster/datanode-$i/conf" ./sbin/start-datanode.sh >> "$DEPLOY_LOG" 2>&1
    sleep 3
done

sleep 15

# 阶段 7: 验证
log_section "阶段 7/7: 验证集群"

cn_count=$(ps aux | grep ConfigNode | grep -v grep | wc -l)
dn_count=$(ps aux | grep DataNode | grep -v grep | wc -l)

log "ConfigNode 进程数: $cn_count (预期: 3)"
log "DataNode 进程数: $dn_count (预期: 6)"

# 检查端口
for port in 6667 6668 6669 6670 6671 6672 10710 10711 10712; do
    if netstat -tlnp 2>/dev/null | grep -q ":$port "; then
        log "端口 $port: 监听中 ✓"
    else
        log "端口 $port: 未监听 ✗"
    fi
done

# 查询集群状态
sleep 5
log "查询集群状态..."
"$IOTDB_HOME/sbin/start-cli.sh" -h 127.0.0.1 -p 6667 -e "show cluster" >> "$DEPLOY_LOG" 2>&1 || log "集群状态查询失败"

log_section "部署完成"
log "部署日志已保存到: $DEPLOY_LOG"

# 生成部署报告
bash /data/workspace/tencent_CodeBuddy/aladdinsun/tools/generate_deployment_docs.sh "$DEPLOY_LOG"

log "所有文档已生成完成"
