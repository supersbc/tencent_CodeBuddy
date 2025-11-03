# IoTDB 生产级集群部署方案

## 📋 部署概览

**集群架构**: 3 ConfigNode + 6 DataNode (高可用生产级配置)  
**预计部署时间**: 2-4 小时  
**目标环境**: TencentOS Server 3.2  
**IoTDB 版本**: 1.3.2 (最新稳定版)

---

## 🖥️ 服务器资源配置

### 当前可用资源
- **CPU**: 64 核 AMD EPYC 9754
- **内存**: 247 GB (可用 195 GB)
- **磁盘**: 1.5 TB 可用空间 (/codev)
- **网络**: 内网高速

### 集群资源分配

#### ConfigNode 配置 (3 个节点)
```
每个 ConfigNode:
- CPU: 2 核
- 内存: 4 GB
- 磁盘: 50 GB
- 端口: 10710, 10720 (依次递增)

总计: 6 核 + 12 GB + 150 GB
```

#### DataNode 配置 (6 个节点)
```
每个 DataNode:
- CPU: 8 核
- 内存: 24 GB
- 磁盘: 200 GB
- 端口: 6667, 10730, 10740, 10750, 10760 (依次递增)

总计: 48 核 + 144 GB + 1.2 TB
```

#### 资源利用率
```
总 CPU 使用: 54 核 / 64 核 (84%)
总内存使用: 156 GB / 195 GB (80%)
总磁盘使用: 1.35 TB / 1.5 TB (90%)
```

---

## 📂 目录结构规划

```
/data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb/
├── apache-iotdb-1.3.2/              # IoTDB 安装目录
├── cluster/                          # 集群配置目录
│   ├── confignode-1/                # ConfigNode 1
│   ├── confignode-2/                # ConfigNode 2
│   ├── confignode-3/                # ConfigNode 3
│   ├── datanode-1/                  # DataNode 1
│   ├── datanode-2/                  # DataNode 2
│   ├── datanode-3/                  # DataNode 3
│   ├── datanode-4/                  # DataNode 4
│   ├── datanode-5/                  # DataNode 5
│   └── datanode-6/                  # DataNode 6
├── scripts/                          # 管理脚本
│   ├── deploy.sh                    # 一键部署脚本
│   ├── start-cluster.sh             # 启动集群
│   ├── stop-cluster.sh              # 停止集群
│   ├── status-cluster.sh            # 查看状态
│   └── clean-cluster.sh             # 清理集群
└── logs/                            # 日志目录

/codev/iotdb_data/                   # 数据存储目录 (2TB 大盘)
├── confignode-1/
├── confignode-2/
├── confignode-3/
├── datanode-1/
├── datanode-2/
├── datanode-3/
├── datanode-4/
├── datanode-5/
└── datanode-6/
```

---

## 🔧 部署步骤详解

### 阶段 1: 环境准备 (15-30 分钟)

#### 1.1 安装 Java 环境
```bash
# 安装 OpenJDK 11
sudo yum install -y java-11-openjdk java-11-openjdk-devel

# 配置 JAVA_HOME
echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk' >> ~/.bashrc
echo 'export PATH=$JAVA_HOME/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# 验证安装
java -version
```

#### 1.2 系统参数优化
```bash
# 增加文件描述符限制
echo "* soft nofile 65535" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 65535" | sudo tee -a /etc/security/limits.conf

# 优化内核参数
sudo tee -a /etc/sysctl.conf << EOF
vm.swappiness=1
vm.max_map_count=655360
net.core.somaxconn=65535
net.ipv4.tcp_max_syn_backlog=65535
EOF

sudo sysctl -p

# 当前会话立即生效
ulimit -n 65535
```

#### 1.3 创建目录结构
```bash
# 创建工作目录
mkdir -p /data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb
cd /data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb

# 创建数据目录
mkdir -p /codev/iotdb_data/{confignode-{1..3},datanode-{1..6}}

# 创建日志目录
mkdir -p logs scripts cluster
```

---

### 阶段 2: 下载和安装 IoTDB (5-10 分钟)

#### 2.1 下载 IoTDB
```bash
cd /data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb

# 下载 IoTDB 1.3.2
wget https://dlcdn.apache.org/iotdb/1.3.2/apache-iotdb-1.3.2-all-bin.zip

# 如果 wget 失败，使用备用下载源
# wget https://mirrors.tuna.tsinghua.edu.cn/apache/iotdb/1.3.2/apache-iotdb-1.3.2-all-bin.zip

# 解压
unzip apache-iotdb-1.3.2-all-bin.zip

# 验证
ls -lh apache-iotdb-1.3.2-all-bin/
```

#### 2.2 配置环境变量
```bash
export IOTDB_HOME=/data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb/apache-iotdb-1.3.2-all-bin
export PATH=$IOTDB_HOME/sbin:$PATH
```

---

### 阶段 3: 集群配置 (20-30 分钟)

#### 3.1 ConfigNode 配置

**ConfigNode-1 配置** (`cluster/confignode-1/iotdb-system.properties`)
```properties
####################
# ConfigNode 配置
####################
cn_internal_address=127.0.0.1
cn_internal_port=10710
cn_consensus_port=10720
cn_seed_config_node=127.0.0.1:10710

# 数据目录
cn_system_dir=/codev/iotdb_data/confignode-1/system
cn_consensus_dir=/codev/iotdb_data/confignode-1/consensus

# JVM 配置
MAX_HEAP_SIZE=4G
HEAP_NEWSIZE=2G
```

**ConfigNode-2 配置** (端口递增)
```properties
cn_internal_address=127.0.0.1
cn_internal_port=10711
cn_consensus_port=10721
cn_seed_config_node=127.0.0.1:10710

cn_system_dir=/codev/iotdb_data/confignode-2/system
cn_consensus_dir=/codev/iotdb_data/confignode-2/consensus

MAX_HEAP_SIZE=4G
HEAP_NEWSIZE=2G
```

**ConfigNode-3 配置**
```properties
cn_internal_address=127.0.0.1
cn_internal_port=10712
cn_consensus_port=10722
cn_seed_config_node=127.0.0.1:10710

cn_system_dir=/codev/iotdb_data/confignode-3/system
cn_consensus_dir=/codev/iotdb_data/confignode-3/consensus

MAX_HEAP_SIZE=4G
HEAP_NEWSIZE=2G
```

#### 3.2 DataNode 配置

**DataNode-1 配置** (`cluster/datanode-1/iotdb-system.properties`)
```properties
####################
# DataNode 配置
####################
dn_rpc_address=127.0.0.1
dn_rpc_port=6667
dn_internal_address=127.0.0.1
dn_internal_port=10730
dn_mpp_data_exchange_port=10740
dn_schema_region_consensus_port=10750
dn_data_region_consensus_port=10760

# ConfigNode 地址
dn_seed_config_node=127.0.0.1:10710

# 数据目录
dn_system_dir=/codev/iotdb_data/datanode-1/system
dn_data_dirs=/codev/iotdb_data/datanode-1/data
dn_consensus_dir=/codev/iotdb_data/datanode-1/consensus
dn_wal_dirs=/codev/iotdb_data/datanode-1/wal

# 性能配置
schema_replication_factor=2
data_replication_factor=2

# JVM 配置
MAX_HEAP_SIZE=16G
HEAP_NEWSIZE=8G
```

**DataNode-2 到 DataNode-6** (端口依次递增)
```
DataNode-2: 6668, 10731, 10741, 10751, 10761
DataNode-3: 6669, 10732, 10742, 10752, 10762
DataNode-4: 6670, 10733, 10743, 10753, 10763
DataNode-5: 6671, 10734, 10744, 10754, 10764
DataNode-6: 6672, 10735, 10745, 10755, 10765
```

---

### 阶段 4: 启动集群 (10-15 分钟)

#### 4.1 启动顺序
```bash
# 1. 启动第一个 ConfigNode (种子节点)
cd $IOTDB_HOME
./sbin/start-confignode.sh -c cluster/confignode-1

# 等待 10 秒
sleep 10

# 2. 启动其他 ConfigNode
./sbin/start-confignode.sh -c cluster/confignode-2
./sbin/start-confignode.sh -c cluster/confignode-3

# 等待 10 秒
sleep 10

# 3. 启动所有 DataNode
./sbin/start-datanode.sh -c cluster/datanode-1
./sbin/start-datanode.sh -c cluster/datanode-2
./sbin/start-datanode.sh -c cluster/datanode-3
./sbin/start-datanode.sh -c cluster/datanode-4
./sbin/start-datanode.sh -c cluster/datanode-5
./sbin/start-datanode.sh -c cluster/datanode-6
```

#### 4.2 验证集群状态
```bash
# 连接 CLI
./sbin/start-cli.sh -h 127.0.0.1 -p 6667

# 在 CLI 中执行
IoTDB> show cluster;
IoTDB> show cluster details;
```

**预期输出**:
```
+------+----------+-------+---------------+------------+
|NodeID|  NodeType| Status|InternalAddress|InternalPort|
+------+----------+-------+---------------+------------+
|     0|ConfigNode|Running|      127.0.0.1|       10710|
|     1|ConfigNode|Running|      127.0.0.1|       10711|
|     2|ConfigNode|Running|      127.0.0.1|       10712|
|     3|  DataNode|Running|      127.0.0.1|       10730|
|     4|  DataNode|Running|      127.0.0.1|       10731|
|     5|  DataNode|Running|      127.0.0.1|       10732|
|     6|  DataNode|Running|      127.0.0.1|       10733|
|     7|  DataNode|Running|      127.0.0.1|       10734|
|     8|  DataNode|Running|      127.0.0.1|       10735|
+------+----------+-------+---------------+------------+
Total line number = 9
```

---

### 阶段 5: 功能验证 (30-60 分钟)

#### 5.1 基础功能测试
```sql
-- 创建数据库
CREATE DATABASE root.test;

-- 创建时间序列
CREATE TIMESERIES root.test.device1.temperature WITH DATATYPE=FLOAT, ENCODING=RLE;
CREATE TIMESERIES root.test.device1.humidity WITH DATATYPE=FLOAT, ENCODING=RLE;

-- 插入数据
INSERT INTO root.test.device1(timestamp,temperature,humidity) VALUES(1,25.5,60.0);
INSERT INTO root.test.device1(timestamp,temperature,humidity) VALUES(2,26.0,61.5);

-- 查询数据
SELECT * FROM root.test.device1;

-- 查看存储组
SHOW DATABASES;
```

#### 5.2 性能测试
```bash
# 使用 IoTDB Benchmark 进行压力测试
cd $IOTDB_HOME/tools/iotdb-benchmark

# 配置测试参数
cat > conf/config.properties << EOF
HOST=127.0.0.1
PORT=6667
DEVICE_NUMBER=100
SENSOR_NUMBER=10
CLIENT_NUMBER=10
OPERATION_PROPORTION=1:0:0:0:0:0:0:0:0:0:0
LOOP=10000
EOF

# 运行测试
./benchmark.sh
```

#### 5.3 高可用测试
```bash
# 1. 停止一个 ConfigNode
./sbin/stop-confignode.sh -c cluster/confignode-3

# 2. 验证集群仍可用
./sbin/start-cli.sh -h 127.0.0.1 -p 6667
IoTDB> show cluster;

# 3. 重启 ConfigNode
./sbin/start-confignode.sh -c cluster/confignode-3

# 4. 停止一个 DataNode
./sbin/stop-datanode.sh -c cluster/datanode-6

# 5. 验证数据仍可访问（副本因子=2）
IoTDB> SELECT * FROM root.test.device1;

# 6. 重启 DataNode
./sbin/start-datanode.sh -c cluster/datanode-6
```

---

## 🔍 监控部署 (可选，30-60 分钟)

### 6.1 Prometheus 监控

#### 安装 Prometheus
```bash
cd /data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb

# 下载 Prometheus
wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz
tar -xzf prometheus-2.45.0.linux-amd64.tar.gz
cd prometheus-2.45.0.linux-amd64

# 配置 Prometheus
cat > prometheus.yml << EOF
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'iotdb'
    static_configs:
      - targets: ['127.0.0.1:9091']  # IoTDB metrics 端口
EOF

# 启动 Prometheus
./prometheus --config.file=prometheus.yml &
```

#### 启用 IoTDB Metrics
```bash
# 编辑 iotdb-system.properties
echo "enable_metric=true" >> $IOTDB_HOME/conf/iotdb-system.properties
echo "metric_reporter_list=PROMETHEUS" >> $IOTDB_HOME/conf/iotdb-system.properties
echo "metric_prometheus_reporter_port=9091" >> $IOTDB_HOME/conf/iotdb-system.properties

# 重启集群
```

### 6.2 Grafana 可视化

```bash
# 下载 Grafana
wget https://dl.grafana.com/oss/release/grafana-10.0.0.linux-amd64.tar.gz
tar -xzf grafana-10.0.0.linux-amd64.tar.gz
cd grafana-10.0.0

# 启动 Grafana
./bin/grafana-server &

# 访问 http://your-ip:3000
# 默认账号: admin/admin
```

**配置步骤**:
1. 添加 Prometheus 数据源
2. 导入 IoTDB Dashboard (ID: 13039)
3. 查看集群监控指标

---

## ⚙️ 性能优化 (可选，30-60 分钟)

### 7.1 JVM 参数优化

**ConfigNode JVM 配置** (`conf/confignode-env.sh`)
```bash
MAX_HEAP_SIZE=4G
HEAP_NEWSIZE=2G
MAX_DIRECT_MEMORY_SIZE=2G

CONFIGNODE_JMX_OPTS="
  -XX:+UseG1GC
  -XX:MaxGCPauseMillis=200
  -XX:+PrintGCDetails
  -XX:+PrintGCDateStamps
  -Xloggc:logs/gc-confignode.log
"
```

**DataNode JVM 配置** (`conf/datanode-env.sh`)
```bash
MAX_HEAP_SIZE=16G
HEAP_NEWSIZE=8G
MAX_DIRECT_MEMORY_SIZE=8G

DATANODE_JMX_OPTS="
  -XX:+UseG1GC
  -XX:MaxGCPauseMillis=200
  -XX:ParallelGCThreads=8
  -XX:ConcGCThreads=4
  -XX:+PrintGCDetails
  -XX:+PrintGCDateStamps
  -Xloggc:logs/gc-datanode.log
"
```

### 7.2 存储引擎优化

```properties
# iotdb-system.properties

# 写入性能优化
wal_buffer_size=33554432
flush_proportion=0.4
reject_proportion=0.8

# 查询性能优化
chunk_buffer_pool_enable=true
max_deduplicated_path_num=1000

# 压缩优化
compaction_strategy=LEVEL
target_compaction_file_size=2147483648
```

### 7.3 网络优化

```properties
# RPC 配置
rpc_thrift_compression_enable=true
rpc_advanced_compression_enable=true
rpc_max_concurrent_client_num=65535

# 连接池配置
max_connection_for_internal_service=100
```

---

## 📊 性能基准测试

### 预期性能指标

| 指标 | 目标值 | 说明 |
|------|--------|------|
| **写入吞吐** | 150万+ 点/秒 | 6 DataNode 并发写入 |
| **查询 QPS** | 10万+ | 简单查询 |
| **写入延迟** | < 50ms | P99 |
| **查询延迟** | < 10ms | 简单查询 P99 |
| **并发连接** | 2000+ | 客户端连接数 |
| **数据压缩比** | 10:1 | 时序数据压缩 |
| **可用性** | 99.9%+ | 容忍 1 节点故障 |

### 压力测试命令

```bash
# 写入测试
./benchmark.sh -cf conf/write-test.properties

# 查询测试
./benchmark.sh -cf conf/query-test.properties

# 混合测试
./benchmark.sh -cf conf/mixed-test.properties
```

---

## 🛠️ 运维管理

### 日常运维脚本

#### 启动集群
```bash
#!/bin/bash
# start-cluster.sh

echo "启动 ConfigNode..."
for i in {1..3}; do
    $IOTDB_HOME/sbin/start-confignode.sh -c cluster/confignode-$i
    sleep 3
done

echo "启动 DataNode..."
for i in {1..6}; do
    $IOTDB_HOME/sbin/start-datanode.sh -c cluster/datanode-$i
    sleep 2
done

echo "集群启动完成"
```

#### 停止集群
```bash
#!/bin/bash
# stop-cluster.sh

echo "停止 DataNode..."
for i in {1..6}; do
    $IOTDB_HOME/sbin/stop-datanode.sh -c cluster/datanode-$i
done

echo "停止 ConfigNode..."
for i in {1..3}; do
    $IOTDB_HOME/sbin/stop-confignode.sh -c cluster/confignode-$i
done

echo "集群停止完成"
```

#### 查看状态
```bash
#!/bin/bash
# status-cluster.sh

echo "检查进程状态..."
ps aux | grep -E "ConfigNode|DataNode" | grep -v grep

echo -e "\n检查端口监听..."
netstat -tlnp | grep -E "6667|1071[0-2]|1073[0-5]"

echo -e "\n集群状态..."
$IOTDB_HOME/sbin/start-cli.sh -h 127.0.0.1 -p 6667 -e "show cluster"
```

### 备份策略

```bash
# 数据备份脚本
#!/bin/bash
BACKUP_DIR=/codev/iotdb_backup/$(date +%Y%m%d)
mkdir -p $BACKUP_DIR

# 备份数据目录
rsync -av /codev/iotdb_data/ $BACKUP_DIR/

# 备份配置文件
tar -czf $BACKUP_DIR/configs.tar.gz cluster/

echo "备份完成: $BACKUP_DIR"
```

---

## 🚨 故障排查

### 常见问题

#### 1. 节点启动失败
```bash
# 检查日志
tail -f logs/log_datanode_all.log

# 检查端口占用
netstat -tlnp | grep 6667

# 检查磁盘空间
df -h /codev
```

#### 2. 集群状态异常
```bash
# 查看详细状态
./sbin/start-cli.sh -h 127.0.0.1 -p 6667 -e "show cluster details"

# 检查网络连接
telnet 127.0.0.1 10710
```

#### 3. 性能下降
```bash
# 检查 GC 日志
tail -f logs/gc-datanode.log

# 检查系统资源
top
iostat -x 1
```

---

## 📈 扩容方案

### 添加 DataNode

```bash
# 1. 准备新节点配置
mkdir -p cluster/datanode-7
cp cluster/datanode-1/iotdb-system.properties cluster/datanode-7/

# 2. 修改端口配置
# dn_rpc_port=6673
# dn_internal_port=10736
# ...

# 3. 启动新节点
./sbin/start-datanode.sh -c cluster/datanode-7

# 4. 验证
./sbin/start-cli.sh -h 127.0.0.1 -p 6667 -e "show cluster"
```

---

## 📝 部署检查清单

### 部署前检查
- [ ] Java 11 已安装
- [ ] 系统参数已优化
- [ ] 目录结构已创建
- [ ] 磁盘空间充足 (> 1.5 TB)
- [ ] 内存充足 (> 160 GB)

### 部署中检查
- [ ] IoTDB 下载成功
- [ ] 配置文件正确
- [ ] 端口无冲突
- [ ] 节点启动成功

### 部署后检查
- [ ] 集群状态正常
- [ ] 基础功能测试通过
- [ ] 性能测试达标
- [ ] 高可用测试通过
- [ ] 监控系统运行

---

## 🎯 下一步行动

### 立即执行
1. 安装 Java 环境
2. 下载 IoTDB 安装包
3. 创建目录结构

### 后续优化
1. 部署监控系统
2. 配置自动备份
3. 性能调优
4. 压力测试

---

## 📞 技术支持

### 官方资源
- 官方文档: https://iotdb.apache.org/
- GitHub: https://github.com/apache/iotdb
- 社区论坛: https://iotdb.apache.org/community/

### 问题反馈
- 提交 Issue: https://github.com/apache/iotdb/issues
- 邮件列表: dev@iotdb.apache.org

---

**文档版本**: v1.0  
**创建时间**: 2025-10-28  
**适用版本**: IoTDB 1.3.2  
**部署环境**: TencentOS Server 3.2
