# IoTDB 生产级集群快速开始指南

## 🚀 一键部署（最快方式）

### 前提条件
```bash
# 1. 安装 Java 11（必需）
sudo yum install -y java-11-openjdk java-11-openjdk-devel

# 2. 验证 Java 安装
java -version
```

### 执行部署
```bash
# 进入 tools 目录
cd /data/workspace/tencent_CodeBuddy/aladdinsun/tools

# 执行一键部署脚本
./deploy_iotdb_cluster.sh
```

**预计时间**: 1-2 小时（取决于网络速度）

---

## 📖 部署内容

### 集群架构
- **3 个 ConfigNode**: 高可用配置管理
- **6 个 DataNode**: 数据存储和查询
- **副本因子**: 2（容忍 1 节点故障）

### 资源分配
- **总 CPU**: 54 核 / 64 核 (84%)
- **总内存**: 156 GB / 195 GB (80%)
- **总磁盘**: 1.35 TB / 1.5 TB (90%)

### 端口分配
```
ConfigNode:
- ConfigNode-1: 10710, 10720
- ConfigNode-2: 10711, 10721
- ConfigNode-3: 10712, 10722

DataNode (RPC端口):
- DataNode-1: 6667
- DataNode-2: 6668
- DataNode-3: 6669
- DataNode-4: 6670
- DataNode-5: 6671
- DataNode-6: 6672
```

---

## 🎮 集群管理

### 启动集群
```bash
cd /data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb
./scripts/start-cluster.sh
```

### 停止集群
```bash
./scripts/stop-cluster.sh
```

### 查看状态
```bash
./scripts/status-cluster.sh
```

### 连接 CLI
```bash
cd /data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb/apache-iotdb-1.3.2-all-bin
./sbin/start-cli.sh -h 127.0.0.1 -p 6667
```

---

## 🧪 快速测试

### 1. 查看集群状态
```sql
IoTDB> show cluster;
IoTDB> show cluster details;
```

### 2. 创建测试数据
```sql
-- 创建数据库
CREATE DATABASE root.test;

-- 创建时间序列
CREATE TIMESERIES root.test.device1.temperature WITH DATATYPE=FLOAT, ENCODING=RLE;
CREATE TIMESERIES root.test.device1.humidity WITH DATATYPE=FLOAT, ENCODING=RLE;

-- 插入数据
INSERT INTO root.test.device1(timestamp,temperature,humidity) VALUES(now(),25.5,60.0);
INSERT INTO root.test.device1(timestamp,temperature,humidity) VALUES(now(),26.0,61.5);

-- 查询数据
SELECT * FROM root.test.device1;
```

### 3. 性能测试
```sql
-- 查看存储组
SHOW DATABASES;

-- 查看时间序列
SHOW TIMESERIES root.test.**;

-- 统计数据点
COUNT TIMESERIES root.test.**;
```

---

## 📊 性能指标

### 预期性能
- **写入吞吐**: 150万+ 点/秒
- **查询 QPS**: 10万+
- **写入延迟**: < 50ms (P99)
- **查询延迟**: < 10ms (P99)
- **并发连接**: 2000+

### 监控指标
```bash
# 查看进程
ps aux | grep -E "ConfigNode|DataNode"

# 查看端口
netstat -tlnp | grep -E "6667|1071"

# 查看资源使用
top
free -h
df -h
```

---

## 📁 重要目录

### 安装目录
```
/data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb/
├── apache-iotdb-1.3.2-all-bin/    # IoTDB 程序
├── cluster/                        # 配置文件
├── scripts/                        # 管理脚本
└── logs/                          # 日志文件
```

### 数据目录
```
/codev/iotdb_data/
├── confignode-{1..3}/             # ConfigNode 数据
└── datanode-{1..6}/               # DataNode 数据
```

---

## 🔧 常用操作

### 查看日志
```bash
# DataNode 日志
tail -f /data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb/logs/datanode-1/log_datanode_all.log

# ConfigNode 日志
tail -f /data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb/logs/confignode-1/log_confignode_all.log
```

### 重启单个节点
```bash
# 停止 DataNode-1
kill $(ps aux | grep "datanode-1" | grep -v grep | awk '{print $2}')

# 启动 DataNode-1
cd /data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb/apache-iotdb-1.3.2-all-bin
IOTDB_CONF=/data/workspace/tencent_CodeBuddy/aladdinsun/tools/iotdb/cluster/datanode-1/conf \
    ./sbin/start-datanode.sh
```

### 清理数据（危险操作）
```bash
# 停止集群
./scripts/stop-cluster.sh

# 删除所有数据
rm -rf /codev/iotdb_data/*/

# 重新创建目录
for i in {1..3}; do
    mkdir -p /codev/iotdb_data/confignode-$i/{system,consensus}
done
for i in {1..6}; do
    mkdir -p /codev/iotdb_data/datanode-$i/{system,data,consensus,wal}
done

# 重新启动
./scripts/start-cluster.sh
```

---

## 🚨 故障排查

### 节点启动失败
```bash
# 1. 检查日志
tail -100 logs/datanode-1/log_datanode_all.log

# 2. 检查端口占用
netstat -tlnp | grep 6667

# 3. 检查进程
ps aux | grep DataNode

# 4. 检查磁盘空间
df -h /codev
```

### 集群状态异常
```bash
# 查看详细状态
./sbin/start-cli.sh -h 127.0.0.1 -p 6667 -e "show cluster details"

# 查看区域分布
./sbin/start-cli.sh -h 127.0.0.1 -p 6667 -e "show regions"
```

### 性能问题
```bash
# 检查 GC 日志
tail -f logs/datanode-1/gc.log

# 检查系统资源
iostat -x 1
vmstat 1
```

---

## 📚 文档索引

- **完整部署方案**: `IoTDB_Production_Deployment_Plan.md`
- **一键部署脚本**: `deploy_iotdb_cluster.sh`
- **快速开始**: `QUICK_START.md` (本文档)

---

## 🔗 相关资源

### 官方文档
- 官网: https://iotdb.apache.org/
- 文档: https://iotdb.apache.org/UserGuide/latest/
- GitHub: https://github.com/apache/iotdb

### 社区支持
- 邮件列表: dev@iotdb.apache.org
- Issues: https://github.com/apache/iotdb/issues
- 论坛: https://iotdb.apache.org/community/

---

## ⏱️ 时间估算

| 阶段 | 时间 |
|------|------|
| 安装 Java | 5 分钟 |
| 执行部署脚本 | 30-60 分钟 |
| 验证测试 | 15 分钟 |
| **总计** | **1-2 小时** |

---

**准备好了吗？执行以下命令开始部署：**

```bash
cd /data/workspace/tencent_CodeBuddy/aladdinsun/tools
./deploy_iotdb_cluster.sh
```

祝部署顺利！🎉
