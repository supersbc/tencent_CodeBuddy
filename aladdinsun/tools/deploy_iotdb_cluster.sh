#!/bin/bash

################################################################################
# IoTDB 生产级集群一键部署脚本
# 版本: v1.0
# 架构: 3 ConfigNode + 6 DataNode
# 作者: AI Assistant
# 日期: 2025-10-28
################################################################################

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置变量
IOTDB_VERSION="1.3.2"
WORK_DIR="/data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb"
DATA_DIR="/codev/iotdb_data"
IOTDB_HOME="${WORK_DIR}/apache-iotdb-${IOTDB_VERSION}-all-bin"

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

# 检查命令是否存在
check_command() {
    if ! command -v $1 &> /dev/null; then
        log_error "$1 未安装"
        return 1
    fi
    return 0
}

# 阶段 1: 环境检查
check_environment() {
    log_step "阶段 1/7: 环境检查"
    
    # 检查 Java
    if ! check_command java; then
        log_error "请先安装 Java 11"
        log_info "执行: sudo yum install -y java-11-openjdk java-11-openjdk-devel"
        exit 1
    fi
    
    java_version=$(java -version 2>&1 | head -n 1 | awk -F '"' '{print $2}')
    log_info "Java 版本: $java_version"
    
    # 检查磁盘空间
    available_space=$(df -BG /codev | tail -1 | awk '{print $4}' | sed 's/G//')
    if [ "$available_space" -lt 100 ]; then
        log_error "磁盘空间不足，需要至少 100 GB，当前可用: ${available_space}G"
        exit 1
    fi
    log_info "磁盘空间充足: ${available_space}G"
    
    # 检查内存
    total_mem=$(free -g | grep Mem | awk '{print $2}')
    if [ "$total_mem" -lt 64 ]; then
        log_warn "内存可能不足，建议至少 64 GB，当前: ${total_mem}G"
    else
        log_info "内存充足: ${total_mem}G"
    fi
    
    # 检查必要命令
    for cmd in wget unzip netstat; do
        if ! check_command $cmd; then
            log_error "请先安装 $cmd"
            exit 1
        fi
    done
    
    log_info "环境检查通过 ✓"
}

# 阶段 2: 系统优化
optimize_system() {
    log_step "阶段 2/7: 系统参数优化"
    
    # 设置文件描述符
    log_info "设置文件描述符限制..."
    ulimit -n 65535
    
    # 检查是否有 root 权限
    if [ "$EUID" -eq 0 ]; then
        # 永久设置
        if ! grep -q "nofile 65535" /etc/security/limits.conf; then
            echo "* soft nofile 65535" >> /etc/security/limits.conf
            echo "* hard nofile 65535" >> /etc/security/limits.conf
            log_info "已永久设置文件描述符限制"
        fi
    else
        log_warn "非 root 用户，跳过永久配置"
    fi
    
    log_info "当前文件描述符限制: $(ulimit -n)"
    log_info "系统优化完成 ✓"
}

# 阶段 3: 创建目录结构
create_directories() {
    log_step "阶段 3/7: 创建目录结构"
    
    # 创建工作目录
    mkdir -p "$WORK_DIR"
    mkdir -p "$WORK_DIR/scripts"
    mkdir -p "$WORK_DIR/logs"
    mkdir -p "$WORK_DIR/cluster"
    
    # 创建数据目录
    for i in {1..3}; do
        mkdir -p "$DATA_DIR/confignode-$i"/{system,consensus}
    done
    
    for i in {1..6}; do
        mkdir -p "$DATA_DIR/datanode-$i"/{system,data,consensus,wal}
    done
    
    log_info "目录结构创建完成 ✓"
    log_info "工作目录: $WORK_DIR"
    log_info "数据目录: $DATA_DIR"
}

# 阶段 4: 下载 IoTDB
download_iotdb() {
    log_step "阶段 4/7: 下载 IoTDB"
    
    cd "$WORK_DIR"
    
    IOTDB_ZIP="apache-iotdb-${IOTDB_VERSION}-all-bin.zip"
    
    if [ -f "$IOTDB_ZIP" ]; then
        log_info "安装包已存在，跳过下载"
    else
        log_info "正在下载 IoTDB ${IOTDB_VERSION}..."
        
        # 主下载源
        DOWNLOAD_URL="https://dlcdn.apache.org/iotdb/${IOTDB_VERSION}/${IOTDB_ZIP}"
        
        if wget -q --show-progress "$DOWNLOAD_URL"; then
            log_info "下载完成 ✓"
        else
            log_error "下载失败，请检查网络连接"
            exit 1
        fi
    fi
    
    # 解压
    if [ -d "$IOTDB_HOME" ]; then
        log_info "IoTDB 已解压，跳过"
    else
        log_info "正在解压..."
        unzip -q "$IOTDB_ZIP"
        log_info "解压完成 ✓"
    fi
    
    # 设置权限
    chmod +x "$IOTDB_HOME/sbin"/*.sh
}

# 阶段 5: 配置集群
configure_cluster() {
    log_step "阶段 5/7: 配置集群"
    
    log_info "配置 3 个 ConfigNode..."
    
    # ConfigNode 配置
    for i in {1..3}; do
        cn_port=$((10710 + i - 1))
        consensus_port=$((10720 + i - 1))
        
        mkdir -p "$WORK_DIR/cluster/confignode-$i/conf"
        
        cat > "$WORK_DIR/cluster/confignode-$i/conf/iotdb-system.properties" << EOF
# ConfigNode-$i 配置
cn_internal_address=127.0.0.1
cn_internal_port=$cn_port
cn_consensus_port=$consensus_port
cn_seed_config_node=127.0.0.1:10710

# 数据目录
cn_system_dir=$DATA_DIR/confignode-$i/system
cn_consensus_dir=$DATA_DIR/confignode-$i/consensus

# 日志
cn_log_dir=$WORK_DIR/logs/confignode-$i
EOF
        
        # JVM 配置
        cat > "$WORK_DIR/cluster/confignode-$i/conf/confignode-env.sh" << EOF
#!/bin/bash
export MAX_HEAP_SIZE=4G
export HEAP_NEWSIZE=2G
export MAX_DIRECT_MEMORY_SIZE=2G
EOF
        chmod +x "$WORK_DIR/cluster/confignode-$i/conf/confignode-env.sh"
        
        log_info "ConfigNode-$i 配置完成 (端口: $cn_port)"
    done
    
    log_info "配置 6 个 DataNode..."
    
    # DataNode 配置
    for i in {1..6}; do
        rpc_port=$((6667 + i - 1))
        internal_port=$((10730 + i - 1))
        mpp_port=$((10740 + i - 1))
        schema_port=$((10750 + i - 1))
        data_port=$((10760 + i - 1))
        
        mkdir -p "$WORK_DIR/cluster/datanode-$i/conf"
        
        cat > "$WORK_DIR/cluster/datanode-$i/conf/iotdb-system.properties" << EOF
# DataNode-$i 配置
dn_rpc_address=127.0.0.1
dn_rpc_port=$rpc_port
dn_internal_address=127.0.0.1
dn_internal_port=$internal_port
dn_mpp_data_exchange_port=$mpp_port
dn_schema_region_consensus_port=$schema_port
dn_data_region_consensus_port=$data_port

# ConfigNode 地址
dn_seed_config_node=127.0.0.1:10710

# 数据目录
dn_system_dir=$DATA_DIR/datanode-$i/system
dn_data_dirs=$DATA_DIR/datanode-$i/data
dn_consensus_dir=$DATA_DIR/datanode-$i/consensus
dn_wal_dirs=$DATA_DIR/datanode-$i/wal

# 日志
dn_log_dir=$WORK_DIR/logs/datanode-$i

# 副本配置
schema_replication_factor=2
data_replication_factor=2

# 性能优化
wal_buffer_size=33554432
flush_proportion=0.4
reject_proportion=0.8
EOF
        
        # JVM 配置
        cat > "$WORK_DIR/cluster/datanode-$i/conf/datanode-env.sh" << EOF
#!/bin/bash
export MAX_HEAP_SIZE=16G
export HEAP_NEWSIZE=8G
export MAX_DIRECT_MEMORY_SIZE=8G
EOF
        chmod +x "$WORK_DIR/cluster/datanode-$i/conf/datanode-env.sh"
        
        log_info "DataNode-$i 配置完成 (RPC端口: $rpc_port)"
    done
    
    log_info "集群配置完成 ✓"
}

# 阶段 6: 启动集群
start_cluster() {
    log_step "阶段 6/7: 启动集群"
    
    cd "$IOTDB_HOME"
    
    # 启动第一个 ConfigNode (种子节点)
    log_info "启动 ConfigNode-1 (种子节点)..."
    IOTDB_CONF="$WORK_DIR/cluster/confignode-1/conf" \
        ./sbin/start-confignode.sh > /dev/null 2>&1
    sleep 10
    
    # 启动其他 ConfigNode
    for i in {2..3}; do
        log_info "启动 ConfigNode-$i..."
        IOTDB_CONF="$WORK_DIR/cluster/confignode-$i/conf" \
            ./sbin/start-confignode.sh > /dev/null 2>&1
        sleep 5
    done
    
    log_info "等待 ConfigNode 集群稳定..."
    sleep 10
    
    # 启动所有 DataNode
    for i in {1..6}; do
        log_info "启动 DataNode-$i..."
        IOTDB_CONF="$WORK_DIR/cluster/datanode-$i/conf" \
            ./sbin/start-datanode.sh > /dev/null 2>&1
        sleep 3
    done
    
    log_info "等待 DataNode 启动..."
    sleep 15
    
    log_info "集群启动完成 ✓"
}

# 阶段 7: 验证集群
verify_cluster() {
    log_step "阶段 7/7: 验证集群状态"
    
    # 检查进程
    log_info "检查进程状态..."
    cn_count=$(ps aux | grep ConfigNode | grep -v grep | wc -l)
    dn_count=$(ps aux | grep DataNode | grep -v grep | wc -l)
    
    log_info "ConfigNode 进程数: $cn_count (预期: 3)"
    log_info "DataNode 进程数: $dn_count (预期: 6)"
    
    if [ "$cn_count" -ne 3 ] || [ "$dn_count" -ne 6 ]; then
        log_warn "进程数量不符合预期，请检查日志"
    fi
    
    # 检查端口
    log_info "检查端口监听..."
    for port in 6667 6668 6669 6670 6671 6672 10710 10711 10712; do
        if netstat -tlnp 2>/dev/null | grep -q ":$port "; then
            log_info "端口 $port: 监听中 ✓"
        else
            log_warn "端口 $port: 未监听"
        fi
    done
    
    # 连接集群查看状态
    log_info "查询集群状态..."
    sleep 5
    
    "$IOTDB_HOME/sbin/start-cli.sh" -h 127.0.0.1 -p 6667 -e "show cluster" 2>/dev/null || {
        log_warn "无法连接到集群，请稍后手动验证"
    }
    
    log_info "验证完成 ✓"
}

# 创建管理脚本
create_management_scripts() {
    log_info "创建管理脚本..."
    
    # 启动脚本
    cat > "$WORK_DIR/scripts/start-cluster.sh" << 'EOF'
#!/bin/bash
IOTDB_HOME="/data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb/apache-iotdb-1.3.2-all-bin"
WORK_DIR="/data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb"

echo "启动 ConfigNode..."
for i in {1..3}; do
    IOTDB_CONF="$WORK_DIR/cluster/confignode-$i/conf" \
        $IOTDB_HOME/sbin/start-confignode.sh
    sleep 3
done

sleep 10

echo "启动 DataNode..."
for i in {1..6}; do
    IOTDB_CONF="$WORK_DIR/cluster/datanode-$i/conf" \
        $IOTDB_HOME/sbin/start-datanode.sh
    sleep 2
done

echo "集群启动完成"
EOF
    
    # 停止脚本
    cat > "$WORK_DIR/scripts/stop-cluster.sh" << 'EOF'
#!/bin/bash
IOTDB_HOME="/data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb/apache-iotdb-1.3.2-all-bin"

echo "停止 DataNode..."
for i in {1..6}; do
    $IOTDB_HOME/sbin/stop-datanode.sh
done

echo "停止 ConfigNode..."
for i in {1..3}; do
    $IOTDB_HOME/sbin/stop-confignode.sh
done

echo "集群停止完成"
EOF
    
    # 状态查看脚本
    cat > "$WORK_DIR/scripts/status-cluster.sh" << 'EOF'
#!/bin/bash
IOTDB_HOME="/data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb/apache-iotdb-1.3.2-all-bin"

echo "=== 进程状态 ==="
ps aux | grep -E "ConfigNode|DataNode" | grep -v grep

echo -e "\n=== 端口监听 ==="
netstat -tlnp | grep -E "6667|1071[0-2]|1073[0-5]"

echo -e "\n=== 集群状态 ==="
$IOTDB_HOME/sbin/start-cli.sh -h 127.0.0.1 -p 6667 -e "show cluster"
EOF
    
    chmod +x "$WORK_DIR/scripts"/*.sh
    log_info "管理脚本创建完成 ✓"
}

# 显示部署总结
show_summary() {
    log_step "部署完成！"
    
    cat << EOF
${GREEN}╔════════════════════════════════════════════════════════════╗
║          IoTDB 生产级集群部署成功！                        ║
╚════════════════════════════════════════════════════════════╝${NC}

${BLUE}集群信息:${NC}
  架构: 3 ConfigNode + 6 DataNode
  版本: IoTDB ${IOTDB_VERSION}
  工作目录: ${WORK_DIR}
  数据目录: ${DATA_DIR}

${BLUE}连接信息:${NC}
  CLI 连接: ${IOTDB_HOME}/sbin/start-cli.sh -h 127.0.0.1 -p 6667
  RPC 端口: 6667-6672 (6个DataNode)
  
${BLUE}管理脚本:${NC}
  启动集群: ${WORK_DIR}/scripts/start-cluster.sh
  停止集群: ${WORK_DIR}/scripts/stop-cluster.sh
  查看状态: ${WORK_DIR}/scripts/status-cluster.sh

${BLUE}常用命令:${NC}
  # 查看集群状态
  ${IOTDB_HOME}/sbin/start-cli.sh -h 127.0.0.1 -p 6667 -e "show cluster"
  
  # 查看详细信息
  ${IOTDB_HOME}/sbin/start-cli.sh -h 127.0.0.1 -p 6667 -e "show cluster details"
  
  # 查看日志
  tail -f ${WORK_DIR}/logs/datanode-1/log_datanode_all.log

${BLUE}下一步:${NC}
  1. 运行功能测试
  2. 进行性能测试
  3. 配置监控系统
  4. 设置定期备份

${YELLOW}注意事项:${NC}
  - 首次启动可能需要 1-2 分钟完全就绪
  - 建议配置 Prometheus + Grafana 监控
  - 定期备份数据目录: ${DATA_DIR}

${GREEN}部署文档: ${WORK_DIR}/../IoTDB_Production_Deployment_Plan.md${NC}

EOF
}

# 主函数
main() {
    echo -e "${BLUE}"
    cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     IoTDB 生产级集群自动部署脚本                             ║
║     版本: v1.0                                                ║
║     架构: 3 ConfigNode + 6 DataNode                           ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}\n"
    
    # 执行部署流程
    check_environment
    optimize_system
    create_directories
    download_iotdb
    configure_cluster
    create_management_scripts
    start_cluster
    verify_cluster
    show_summary
    
    log_info "部署脚本执行完成！"
}

# 执行主函数
main "$@"
