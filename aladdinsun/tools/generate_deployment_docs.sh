#!/bin/bash

################################################################################
# 部署文档生成脚本
# 自动生成：部署报告、维护手册、设备清单
################################################################################

WORK_DIR="/data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DEPLOY_LOG="$1"

# 生成部署报告
generate_deployment_report() {
    REPORT_FILE="${WORK_DIR}/DEPLOYMENT_REPORT_${TIMESTAMP}.md"
    
    cat > "$REPORT_FILE" << 'EOF'
# IoTDB 生产级集群部署报告

## 📋 部署概要

**部署时间**: $(date '+%Y-%m-%d %H:%M:%S')
**部署人员**: 自动化部署脚本
**集群架构**: 3 ConfigNode + 6 DataNode
**IoTDB 版本**: 1.3.2

---

## ✅ 部署状态

### 节点状态
EOF

    # 获取进程信息
    echo "" >> "$REPORT_FILE"
    echo "#### ConfigNode 进程" >> "$REPORT_FILE"
    echo '```' >> "$REPORT_FILE"
    ps aux | grep ConfigNode | grep -v grep >> "$REPORT_FILE" 2>/dev/null || echo "未找到进程" >> "$REPORT_FILE"
    echo '```' >> "$REPORT_FILE"
    
    echo "" >> "$REPORT_FILE"
    echo "#### DataNode 进程" >> "$REPORT_FILE"
    echo '```' >> "$REPORT_FILE"
    ps aux | grep DataNode | grep -v grep >> "$REPORT_FILE" 2>/dev/null || echo "未找到进程" >> "$REPORT_FILE"
    echo '```' >> "$REPORT_FILE"
    
    # 端口监听
    cat >> "$REPORT_FILE" << 'EOF'

### 端口监听状态

| 端口 | 服务 | 状态 |
|------|------|------|
EOF
    
    for port in 6667 6668 6669 6670 6671 6672; do
        node=$((port - 6666))
        if netstat -tlnp 2>/dev/null | grep -q ":$port "; then
            echo "| $port | DataNode-$node RPC | ✅ 监听中 |" >> "$REPORT_FILE"
        else
            echo "| $port | DataNode-$node RPC | ❌ 未监听 |" >> "$REPORT_FILE"
        fi
    done
    
    for i in {1..3}; do
        port=$((10709 + i))
        if netstat -tlnp 2>/dev/null | grep -q ":$port "; then
            echo "| $port | ConfigNode-$i | ✅ 监听中 |" >> "$REPORT_FILE"
        else
            echo "| $port | ConfigNode-$i | ❌ 未监听 |" >> "$REPORT_FILE"
        fi
    done
    
    # 资源使用
    cat >> "$REPORT_FILE" << EOF

---

## 💻 资源使用情况

### 系统资源

\`\`\`
$(free -h)
\`\`\`

### 磁盘使用

\`\`\`
$(df -h | grep -E "Filesystem|/codev|overlay")
\`\`\`

### CPU 信息

\`\`\`
CPU 核心数: $(nproc)
CPU 型号: $(cat /proc/cpuinfo | grep "model name" | head -1 | cut -d: -f2)
\`\`\`

---

## 📂 目录结构

### 安装目录
\`\`\`
${WORK_DIR}/
├── apache-iotdb-1.3.2-all-bin/    # IoTDB 程序
├── cluster/                        # 配置文件
│   ├── confignode-{1..3}/
│   └── datanode-{1..6}/
├── scripts/                        # 管理脚本
└── logs/                          # 日志文件
\`\`\`

### 数据目录
\`\`\`
/data/workspace/iotdb_data/
├── confignode-{1..3}/
└── datanode-{1..6}/
\`\`\`

---

## 📊 集群状态

\`\`\`
$(${WORK_DIR}/apache-iotdb-1.3.2-all-bin/sbin/start-cli.sh -h 127.0.0.1 -p 6667 -e "show cluster" 2>/dev/null || echo "集群状态查询失败，请稍后手动查询")
\`\`\`

---

## 📝 部署日志

完整部署日志: \`${DEPLOY_LOG}\`

关键日志摘要:
\`\`\`
$(tail -50 "$DEPLOY_LOG" 2>/dev/null || echo "日志文件不存在")
\`\`\`

---

## 🔗 相关文档

- 维护操作手册: \`MAINTENANCE_MANUAL_${TIMESTAMP}.md\`
- 设备清单: \`EQUIPMENT_INVENTORY_${TIMESTAMP}.md\`
- 快速开始指南: \`QUICK_START.md\`
- 完整部署方案: \`IoTDB_Production_Deployment_Plan.md\`

---

**报告生成时间**: $(date '+%Y-%m-%d %H:%M:%S')
EOF

    echo "✅ 部署报告已生成: $REPORT_FILE"
}

# 生成维护手册
generate_maintenance_manual() {
    MANUAL_FILE="${WORK_DIR}/MAINTENANCE_MANUAL_${TIMESTAMP}.md"
    
    cat > "$MANUAL_FILE" << 'EOF'
# IoTDB 集群维护操作手册

## 📚 目录

1. [日常运维](#日常运维)
2. [启停管理](#启停管理)
3. [监控检查](#监控检查)
4. [备份恢复](#备份恢复)
5. [故障处理](#故障处理)
6. [性能优化](#性能优化)
7. [扩容缩容](#扩容缩容)

---

## 1. 日常运维

### 1.1 每日检查清单

```bash
# 检查集群状态
cd /data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb
./scripts/status-cluster.sh

# 检查磁盘空间
df -h /codev

# 检查内存使用
free -h

# 检查进程状态
ps aux | grep -E "ConfigNode|DataNode" | grep -v grep

# 查看最新日志
tail -100 logs/datanode-1/log_datanode_all.log
```

### 1.2 每周检查清单

```bash
# 检查数据目录大小
du -sh /data/workspace/iotdb_data/*

# 检查日志文件大小
du -sh /data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb/logs/*

# 查看 GC 日志
tail -100 logs/datanode-1/gc.log

# 检查系统负载
uptime
iostat -x 1 5
```

### 1.3 每月检查清单

```bash
# 清理旧日志（保留最近30天）
find /data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb/logs -name "*.log.*" -mtime +30 -delete

# 数据备份
bash /data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb/scripts/backup-data.sh

# 性能测试
bash /data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb/scripts/performance-test.sh
```

---

## 2. 启停管理

### 2.1 启动集群

```bash
# 完整启动
cd /data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb
./scripts/start-cluster.sh

# 分步启动
# 1. 启动 ConfigNode
for i in {1..3}; do
    IOTDB_CONF=/data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb/cluster/confignode-$i/conf \
        /data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb/apache-iotdb-1.3.2-all-bin/sbin/start-confignode.sh
    sleep 3
done

# 2. 启动 DataNode
for i in {1..6}; do
    IOTDB_CONF=/data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb/cluster/datanode-$i/conf \
        /data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb/apache-iotdb-1.3.2-all-bin/sbin/start-datanode.sh
    sleep 2
done
```

### 2.2 停止集群

```bash
# 完整停止
./scripts/stop-cluster.sh

# 优雅停止（推荐）
# 1. 先停止 DataNode
for i in {1..6}; do
    kill -15 $(ps aux | grep "datanode-$i" | grep -v grep | awk '{print $2}')
    sleep 2
done

# 2. 再停止 ConfigNode
for i in {1..3}; do
    kill -15 $(ps aux | grep "confignode-$i" | grep -v grep | awk '{print $2}')
    sleep 2
done
```

### 2.3 重启单个节点

```bash
# 重启 DataNode-1
# 1. 停止
kill -15 $(ps aux | grep "datanode-1" | grep -v grep | awk '{print $2}')
sleep 5

# 2. 启动
IOTDB_CONF=/data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb/cluster/datanode-1/conf \
    /data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb/apache-iotdb-1.3.2-all-bin/sbin/start-datanode.sh

# 3. 验证
sleep 10
/data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb/apache-iotdb-1.3.2-all-bin/sbin/start-cli.sh \
    -h 127.0.0.1 -p 6667 -e "show cluster"
```

---

## 3. 监控检查

### 3.1 集群健康检查

```bash
# 连接 CLI
cd /data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb/apache-iotdb-1.3.2-all-bin
./sbin/start-cli.sh -h 127.0.0.1 -p 6667

# 在 CLI 中执行
IoTDB> show cluster;
IoTDB> show cluster details;
IoTDB> show regions;
IoTDB> show databases;
```

### 3.2 性能监控

```bash
# 查看 JVM 内存使用
jstat -gc $(ps aux | grep DataNode | grep -v grep | head -1 | awk '{print $2}') 1000 10

# 查看系统资源
top -p $(ps aux | grep -E "ConfigNode|DataNode" | grep -v grep | awk '{print $2}' | tr '\n' ',' | sed 's/,$//')

# 查看网络连接
netstat -an | grep -E "6667|10710" | wc -l
```

### 3.3 日志监控

```bash
# 实时查看日志
tail -f logs/datanode-1/log_datanode_all.log

# 查找错误
grep -i error logs/datanode-*/log_datanode_all.log

# 查找警告
grep -i warn logs/datanode-*/log_datanode_all.log
```

---

## 4. 备份恢复

### 4.1 数据备份

```bash
#!/bin/bash
# backup-data.sh

BACKUP_DIR="/codev/iotdb_backup/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# 停止集群（可选，热备份可跳过）
# ./scripts/stop-cluster.sh

# 备份数据
rsync -av /data/workspace/iotdb_data/ "$BACKUP_DIR/data/"

# 备份配置
tar -czf "$BACKUP_DIR/configs.tar.gz" \
    /data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb/cluster/

echo "备份完成: $BACKUP_DIR"
```

### 4.2 数据恢复

```bash
#!/bin/bash
# restore-data.sh

BACKUP_DIR="$1"  # 备份目录路径

if [ -z "$BACKUP_DIR" ]; then
    echo "用法: $0 <备份目录>"
    exit 1
fi

# 停止集群
./scripts/stop-cluster.sh

# 恢复数据
rsync -av "$BACKUP_DIR/data/" /data/workspace/iotdb_data/

# 恢复配置
tar -xzf "$BACKUP_DIR/configs.tar.gz" -C /

# 启动集群
./scripts/start-cluster.sh

echo "恢复完成"
```

---

## 5. 故障处理

### 5.1 节点无法启动

**症状**: 节点启动后立即退出

**排查步骤**:
```bash
# 1. 查看日志
tail -100 logs/datanode-1/log_datanode_all.log

# 2. 检查端口占用
netstat -tlnp | grep 6667

# 3. 检查磁盘空间
df -h /codev

# 4. 检查配置文件
cat cluster/datanode-1/conf/iotdb-system.properties
```

**常见原因**:
- 端口被占用
- 磁盘空间不足
- 配置文件错误
- JVM 内存不足

### 5.2 集群状态异常

**症状**: show cluster 显示节点状态为 Unknown

**处理方法**:
```bash
# 1. 重启异常节点
kill -15 $(ps aux | grep "datanode-X" | grep -v grep | awk '{print $2}')
sleep 5
IOTDB_CONF=cluster/datanode-X/conf ./sbin/start-datanode.sh

# 2. 检查网络连接
telnet 127.0.0.1 10710

# 3. 查看 ConfigNode 日志
tail -100 logs/confignode-1/log_confignode_all.log
```

### 5.3 查询性能下降

**排查步骤**:
```bash
# 1. 检查 GC 频率
grep "Full GC" logs/datanode-*/gc.log | tail -20

# 2. 检查磁盘 I/O
iostat -x 1 10

# 3. 检查内存使用
free -h

# 4. 检查慢查询
grep "slow query" logs/datanode-*/log_datanode_all.log
```

---

## 6. 性能优化

### 6.1 JVM 参数调优

```bash
# 编辑 datanode-env.sh
vi cluster/datanode-1/conf/datanode-env.sh

# 推荐配置
export MAX_HEAP_SIZE=24G        # 增加堆内存
export HEAP_NEWSIZE=12G         # 增加新生代
export MAX_DIRECT_MEMORY_SIZE=12G

# 重启节点生效
```

### 6.2 系统参数优化

```bash
# 增加文件描述符
ulimit -n 65535

# 优化内核参数
sudo sysctl -w vm.swappiness=1
sudo sysctl -w vm.max_map_count=655360
```

### 6.3 存储优化

```bash
# 编辑 iotdb-system.properties
vi cluster/datanode-1/conf/iotdb-system.properties

# 优化配置
wal_buffer_size=67108864        # 增加 WAL 缓冲
flush_proportion=0.3            # 调整刷盘比例
compaction_strategy=LEVEL       # 使用 LEVEL 压缩策略
```

---

## 7. 扩容缩容

### 7.1 添加 DataNode

```bash
# 1. 创建配置目录
mkdir -p cluster/datanode-7/conf
mkdir -p /data/workspace/iotdb_data/datanode-7/{system,data,consensus,wal}

# 2. 复制配置文件
cp cluster/datanode-1/conf/* cluster/datanode-7/conf/

# 3. 修改端口配置
vi cluster/datanode-7/conf/iotdb-system.properties
# dn_rpc_port=6673
# dn_internal_port=10736
# ...

# 4. 启动新节点
IOTDB_CONF=cluster/datanode-7/conf ./sbin/start-datanode.sh

# 5. 验证
./sbin/start-cli.sh -h 127.0.0.1 -p 6667 -e "show cluster"
```

### 7.2 移除 DataNode

```bash
# 1. 在 CLI 中执行
IoTDB> remove datanode <datanode_id>;

# 2. 等待数据迁移完成
IoTDB> show cluster;

# 3. 停止节点
kill -15 $(ps aux | grep "datanode-X" | grep -v grep | awk '{print $2}')
```

---

## 📞 联系方式

**技术支持**: 
- 官方文档: https://iotdb.apache.org/
- GitHub Issues: https://github.com/apache/iotdb/issues

**紧急联系**: 
- 系统管理员: [填写联系方式]

---

**手册版本**: v1.0  
**更新时间**: $(date '+%Y-%m-%d')
EOF

    echo "✅ 维护手册已生成: $MANUAL_FILE"
}

# 生成设备清单
generate_equipment_inventory() {
    INVENTORY_FILE="${WORK_DIR}/EQUIPMENT_INVENTORY_${TIMESTAMP}.md"
    
    cat > "$INVENTORY_FILE" << EOF
# IoTDB 集群设备清单

## 📋 基本信息

**集群名称**: IoTDB 生产集群  
**部署时间**: $(date '+%Y-%m-%d %H:%M:%S')  
**IoTDB 版本**: 1.3.2  
**集群架构**: 3 ConfigNode + 6 DataNode

---

## 🖥️ 硬件资源

### 服务器信息

| 项目 | 配置 |
|------|------|
| **主机名** | $(hostname) |
| **操作系统** | $(cat /etc/os-release | grep "PRETTY_NAME" | cut -d'"' -f2) |
| **内核版本** | $(uname -r) |
| **CPU 型号** | $(cat /proc/cpuinfo | grep "model name" | head -1 | cut -d: -f2 | xargs) |
| **CPU 核心数** | $(nproc) 核 |
| **总内存** | $(free -h | grep Mem | awk '{print $2}') |
| **可用内存** | $(free -h | grep Mem | awk '{print $7}') |

### 磁盘信息

\`\`\`
$(df -h | grep -E "Filesystem|/codev|overlay")
\`\`\`

### 网络信息

| 项目 | 值 |
|------|-----|
| **IP 地址** | $(hostname -I | awk '{print $1}') |
| **网络接口** | $(ip link | grep "state UP" | awk -F: '{print $2}' | xargs) |

---

## 📦 软件清单

### 核心组件

| 组件 | 版本 | 安装路径 |
|------|------|---------|
| **IoTDB** | 1.3.2 | /data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb/apache-iotdb-1.3.2-all-bin |
| **Java** | $(java -version 2>&1 | head -1 | cut -d'"' -f2) | $(which java) |
| **Python** | $(python3 --version 2>&1 | awk '{print $2}') | $(which python3) |

### 依赖包

\`\`\`bash
$(rpm -qa | grep -E "java|python" | sort)
\`\`\`

---

## 🔧 节点清单

### ConfigNode 节点

| 节点ID | 内部地址 | 内部端口 | 共识端口 | 内存分配 | 数据目录 |
|--------|---------|---------|---------|---------|---------|
| ConfigNode-1 | 127.0.0.1 | 10710 | 10720 | 4 GB | /data/workspace/iotdb_data/confignode-1 |
| ConfigNode-2 | 127.0.0.1 | 10711 | 10721 | 4 GB | /data/workspace/iotdb_data/confignode-2 |
| ConfigNode-3 | 127.0.0.1 | 10712 | 10722 | 4 GB | /data/workspace/iotdb_data/confignode-3 |

**总计**: 3 节点，12 GB 内存

### DataNode 节点

| 节点ID | RPC地址 | RPC端口 | 内部端口 | MPP端口 | Schema端口 | Data端口 | 内存分配 | 数据目录 |
|--------|---------|---------|---------|---------|-----------|---------|---------|---------|
| DataNode-1 | 127.0.0.1 | 6667 | 10730 | 10740 | 10750 | 10760 | 16 GB | /data/workspace/iotdb_data/datanode-1 |
| DataNode-2 | 127.0.0.1 | 6668 | 10731 | 10741 | 10751 | 10761 | 16 GB | /data/workspace/iotdb_data/datanode-2 |
| DataNode-3 | 127.0.0.1 | 6669 | 10732 | 10742 | 10752 | 10762 | 16 GB | /data/workspace/iotdb_data/datanode-3 |
| DataNode-4 | 127.0.0.1 | 6670 | 10733 | 10743 | 10753 | 10763 | 16 GB | /data/workspace/iotdb_data/datanode-4 |
| DataNode-5 | 127.0.0.1 | 6671 | 10734 | 10744 | 10754 | 10764 | 16 GB | /data/workspace/iotdb_data/datanode-5 |
| DataNode-6 | 127.0.0.1 | 6672 | 10735 | 10745 | 10755 | 10765 | 16 GB | /data/workspace/iotdb_data/datanode-6 |

**总计**: 6 节点，96 GB 内存

---

## 📂 目录结构

### 安装目录

\`\`\`
/data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb/
├── apache-iotdb-1.3.2-all-bin/          # IoTDB 程序目录
│   ├── sbin/                             # 启动脚本
│   ├── conf/                             # 默认配置
│   └── lib/                              # 依赖库
├── cluster/                              # 集群配置目录
│   ├── confignode-1/conf/               # ConfigNode-1 配置
│   ├── confignode-2/conf/               # ConfigNode-2 配置
│   ├── confignode-3/conf/               # ConfigNode-3 配置
│   ├── datanode-1/conf/                 # DataNode-1 配置
│   ├── datanode-2/conf/                 # DataNode-2 配置
│   ├── datanode-3/conf/                 # DataNode-3 配置
│   ├── datanode-4/conf/                 # DataNode-4 配置
│   ├── datanode-5/conf/                 # DataNode-5 配置
│   └── datanode-6/conf/                 # DataNode-6 配置
├── scripts/                              # 管理脚本
│   ├── start-cluster.sh                 # 启动脚本
│   ├── stop-cluster.sh                  # 停止脚本
│   └── status-cluster.sh                # 状态查询脚本
└── logs/                                 # 日志目录
    ├── confignode-1/                    # ConfigNode-1 日志
    ├── confignode-2/                    # ConfigNode-2 日志
    ├── confignode-3/                    # ConfigNode-3 日志
    ├── datanode-1/                      # DataNode-1 日志
    ├── datanode-2/                      # DataNode-2 日志
    ├── datanode-3/                      # DataNode-3 日志
    ├── datanode-4/                      # DataNode-4 日志
    ├── datanode-5/                      # DataNode-5 日志
    └── datanode-6/                      # DataNode-6 日志
\`\`\`

### 数据目录

\`\`\`
/data/workspace/iotdb_data/
├── confignode-1/
│   ├── system/                          # 系统数据
│   └── consensus/                       # 共识数据
├── confignode-2/
│   ├── system/
│   └── consensus/
├── confignode-3/
│   ├── system/
│   └── consensus/
├── datanode-1/
│   ├── system/                          # 系统数据
│   ├── data/                            # 时序数据
│   ├── consensus/                       # 共识数据
│   └── wal/                             # 预写日志
├── datanode-2/
│   ├── system/
│   ├── data/
│   ├── consensus/
│   └── wal/
├── datanode-3/
│   ├── system/
│   ├── data/
│   ├── consensus/
│   └── wal/
├── datanode-4/
│   ├── system/
│   ├── data/
│   ├── consensus/
│   └── wal/
├── datanode-5/
│   ├── system/
│   ├── data/
│   ├── consensus/
│   └── wal/
└── datanode-6/
    ├── system/
    ├── data/
    ├── consensus/
    └── wal/
\`\`\`

---

## 🔌 端口分配

### ConfigNode 端口

| 节点 | 内部端口 | 共识端口 | 用途 |
|------|---------|---------|------|
| ConfigNode-1 | 10710 | 10720 | 配置管理、元数据管理 |
| ConfigNode-2 | 10711 | 10721 | 配置管理、元数据管理 |
| ConfigNode-3 | 10712 | 10722 | 配置管理、元数据管理 |

### DataNode 端口

| 节点 | RPC端口 | 内部端口 | MPP端口 | Schema端口 | Data端口 |
|------|---------|---------|---------|-----------|---------|
| DataNode-1 | 6667 | 10730 | 10740 | 10750 | 10760 |
| DataNode-2 | 6668 | 10731 | 10741 | 10751 | 10761 |
| DataNode-3 | 6669 | 10732 | 10742 | 10752 | 10762 |
| DataNode-4 | 6670 | 10733 | 10743 | 10753 | 10763 |
| DataNode-5 | 6671 | 10734 | 10744 | 10754 | 10764 |
| DataNode-6 | 6672 | 10735 | 10745 | 10755 | 10765 |

**端口说明**:
- **RPC端口**: 客户端连接端口
- **内部端口**: 节点间通信端口
- **MPP端口**: 分布式查询引擎端口
- **Schema端口**: 元数据共识端口
- **Data端口**: 数据共识端口

---

## ⚙️ 配置参数

### JVM 配置

#### ConfigNode JVM
\`\`\`bash
MAX_HEAP_SIZE=4G
HEAP_NEWSIZE=2G
MAX_DIRECT_MEMORY_SIZE=2G
\`\`\`

#### DataNode JVM
\`\`\`bash
MAX_HEAP_SIZE=16G
HEAP_NEWSIZE=8G
MAX_DIRECT_MEMORY_SIZE=8G
\`\`\`

### 核心配置参数

\`\`\`properties
# 副本配置
schema_replication_factor=2
data_replication_factor=2

# 性能配置
wal_buffer_size=33554432
flush_proportion=0.4
reject_proportion=0.8
\`\`\`

---

## 📊 资源使用统计

### 当前资源使用

\`\`\`
$(free -h)
\`\`\`

### 磁盘使用

\`\`\`
$(du -sh /data/workspace/iotdb_data/* 2>/dev/null || echo "数据目录统计中...")
\`\`\`

### 进程资源

\`\`\`
$(ps aux | grep -E "ConfigNode|DataNode" | grep -v grep | awk '{print $2, $3, $4, $11}' | column -t)
\`\`\`

---

## 📝 变更记录

| 日期 | 变更内容 | 操作人 |
|------|---------|--------|
| $(date '+%Y-%m-%d') | 初始部署 | 自动化脚本 |

---

## 📞 联系信息

**系统管理员**: [填写]  
**技术支持**: [填写]  
**紧急联系**: [填写]

---

**清单版本**: v1.0  
**生成时间**: $(date '+%Y-%m-%d %H:%M:%S')  
**下次更新**: $(date -d '+1 month' '+%Y-%m-%d')
EOF

    echo "✅ 设备清单已生成: $INVENTORY_FILE"
}

# 主函数
main() {
    echo "开始生成部署文档..."
    
    generate_deployment_report
    generate_maintenance_manual
    generate_equipment_inventory
    
    echo ""
    echo "=========================================="
    echo "所有文档生成完成！"
    echo "=========================================="
    echo ""
    echo "📄 部署报告: ${WORK_DIR}/DEPLOYMENT_REPORT_${TIMESTAMP}.md"
    echo "📖 维护手册: ${WORK_DIR}/MAINTENANCE_MANUAL_${TIMESTAMP}.md"
    echo "📋 设备清单: ${WORK_DIR}/EQUIPMENT_INVENTORY_${TIMESTAMP}.md"
    echo ""
}

main
