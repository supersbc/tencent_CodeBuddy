# E-Log 实验快速开始指南

## 🚀 5分钟快速体验

### 选项1: 演示实验（无需任何依赖）

最简单的方式，直接运行模拟实验：

```bash
cd elog_experiment
python3 demo_experiment.py
```

**输出示例**:
```
================================================================================
E-Log 实验演示
论文: E-Log: Fine-Grained Elastic Log-Based Anomaly Detection
实验: IoTDB + TSBS，测试不同触发阈值
================================================================================

阶段1: 触发阈值实验
================================================================================
测试阈值: θ = [0.00, 0.01, 0.02, 0.03, 0.05, 0.10]
...
```

查看结果：
```bash
# 查看可视化
python3 visualize_results.py

# 查看详细报告
cat demo_results/experiment_report.md

# 查看CSV数据
cat demo_results/threshold_results.csv
```

---

## 🐳 完整实验（需要Docker）

### 前置要求

- ✅ Docker (>= 20.10)
- ✅ Docker Compose (>= 1.29)
- ✅ 至少16GB内存
- ✅ 至少50GB磁盘空间

### 一键启动

```bash
cd elog_experiment

# 自动搭建环境（包含IoTDB集群 + 监控）
bash scripts/setup_environment.sh
```

这个脚本会自动完成：
1. ✓ 检查Docker环境
2. ✓ 创建必要目录
3. ✓ 拉取Docker镜像
4. ✓ 启动IoTDB集群（3数据节点 + 1配置节点）
5. ✓ 启动Prometheus和Grafana
6. ✓ 验证集群状态

### 验证安装

```bash
# 查看容器状态
docker-compose ps

# 连接IoTDB CLI
docker exec -it iotdb-datanode-1 /iotdb/sbin/start-cli.sh -h localhost -p 6667

# 在CLI中执行
IoTDB> show cluster
IoTDB> show databases
```

### 访问监控

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (用户名/密码: admin/admin)

---

## 📊 运行实验

### 方式1: 使用已有数据（推荐）

如果你已经下载了E-Log数据集：

```bash
# 下载数据集
wget https://github.com/AIOPS-LogDB/E-Log-Dataset/releases/download/v1.0/elog-dataset.tar.gz
tar -xzf elog-dataset.tar.gz -C data/

# 运行实验
python3 scripts/run_experiment.py --config config/experiment_config.yaml
```

### 方式2: 生成新数据

使用TSBS生成测试数据：

```bash
# 安装TSBS（需要Go环境）
git clone https://github.com/timescale/tsbs
cd tsbs
go build ./cmd/tsbs_generate_data
go build ./cmd/tsbs_load_iotdb

# 生成数据
./tsbs_generate_data --use-case=iot --scale=100 --timestamp-start="2024-01-01T00:00:00Z" --timestamp-end="2024-01-02T00:00:00Z" --seed=123 --format=iotdb > /tmp/iotdb-data.txt

# 加载到IoTDB
./tsbs_load_iotdb --file=/tmp/iotdb-data.txt --host=localhost --port=6667
```

---

## 🎯 实验场景

### 场景1: 测试不同触发阈值

```bash
# 编辑配置文件
vim config/experiment_config.yaml

# 修改theta_values
threshold_experiment:
  enabled: true
  theta_values: [0.00, 0.01, 0.02, 0.03, 0.05, 0.10]

# 运行实验
python3 scripts/run_experiment.py
```

### 场景2: 测试不确定性触发

```bash
# 启用不确定性触发
vim config/experiment_config.yaml

uncertainty_trigger:
  enabled: true
  methods:
    - name: "confidence_based"
      threshold: 0.8

# 运行实验
python3 scripts/run_experiment.py
```

### 场景3: 对比SOTA方法

```bash
# 启用基线对比
vim config/experiment_config.yaml

baseline_comparison:
  enabled: true
  methods:
    - name: "LogRobust"
    - name: "PLELog"
    - name: "E-Log"

# 运行实验
python3 scripts/run_experiment.py
```

---

## 📈 查看结果

### 实验结果位置

```
data/results/
├── metrics/
│   ├── threshold_results.json
│   ├── threshold_results.csv
│   └── uncertainty_results.json
├── plots/
│   ├── 3d_curves.png
│   └── threshold_comparison.png
└── experiment_report.md
```

### 可视化结果

```bash
# 使用内置可视化工具
python3 visualize_results.py

# 或使用Jupyter Notebook（如果已安装）
jupyter notebook notebooks/results_visualization.ipynb
```

---

## 🛠️ 常见问题

### Q1: Docker容器启动失败

```bash
# 查看日志
docker-compose logs

# 重启容器
docker-compose restart

# 完全重建
docker-compose down -v
docker-compose up -d
```

### Q2: IoTDB连接超时

```bash
# 检查容器状态
docker-compose ps

# 等待更长时间（集群启动需要30-60秒）
sleep 60

# 手动验证
docker exec iotdb-datanode-1 bash -c "echo 'show cluster' | /iotdb/sbin/start-cli.sh -h localhost -p 6667"
```

### Q3: 内存不足

编辑 `docker-compose.yml`，减少堆内存：

```yaml
environment:
  - IOTDB_HEAP_SIZE=4G  # 从8G改为4G
```

### Q4: 端口冲突

修改 `docker-compose.yml` 中的端口映射：

```yaml
ports:
  - "16667:6667"  # 使用16667代替6667
```

---

## 🔧 高级配置

### 自定义实验参数

编辑 `config/experiment_config.yaml`:

```yaml
# 修改时间窗口
feature_extraction:
  window_size: 10  # 从5秒改为10秒

# 修改模型参数
model:
  lstm:
    hidden_size: 128  # 从64改为128
    num_layers: 3     # 从2改为3

# 修改LPS Reducer参数
lps_reducer:
  alpha: 200  # 从100改为200
  beta: 2     # 从1改为2
```

### 自定义IoTDB配置

编辑 `config/iotdb_config.yaml`:

```yaml
# 修改日志级别
logging:
  log_level: "DEBUG"  # 从INFO改为DEBUG

# 修改性能参数
performance:
  write:
    batch_size: 2000  # 从1000改为2000
    write_threads: 16 # 从8改为16
```

---

## 📚 下一步

1. **阅读论文分析**: `../elog_paper_summary.md`
2. **查看实验总结**: `../ELOG_EXPERIMENT_SUMMARY.md`
3. **查看文件清单**: `FILES.md`
4. **查看完整README**: `README.md`

---

## 🆘 获取帮助

- 查看日志: `docker-compose logs -f`
- 查看容器状态: `docker-compose ps`
- 进入容器: `docker exec -it iotdb-datanode-1 bash`
- 停止集群: `docker-compose down`
- 清理数据: `docker-compose down -v && rm -rf data/ logs/`

---

## ✅ 检查清单

运行实验前，确保：

- [ ] Docker和Docker Compose已安装
- [ ] 至少16GB可用内存
- [ ] 至少50GB可用磁盘空间
- [ ] 端口6667-6669, 9090, 3000未被占用
- [ ] Python 3.7+已安装
- [ ] 已阅读README.md

---

*快速开始指南 - 最后更新: 2025-10-29*
