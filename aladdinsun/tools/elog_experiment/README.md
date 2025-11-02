# E-Log 实验复现

本目录包含E-Log论文实验的复现代码。

## 目录结构

```
elog_experiment/
├── README.md                 # 本文件
├── requirements.txt          # Python依赖
├── config/                   # 配置文件
│   ├── iotdb_config.yaml    # IoTDB配置
│   └── experiment_config.yaml # 实验参数配置
├── data/                     # 数据目录
│   ├── raw_logs/            # 原始日志
│   ├── parsed_logs/         # 解析后的日志
│   └── results/             # 实验结果
├── src/                      # 源代码
│   ├── __init__.py
│   ├── log_parser.py        # 日志解析（Drain算法）
│   ├── feature_extractor.py # 特征提取
│   ├── models/              # 模型实现
│   │   ├── __init__.py
│   │   ├── lstm_attention.py # LSTM+Self-Attention
│   │   ├── lps_reducer.py   # LPS Reducer（强化学习）
│   │   └── cascade_discriminator.py # Cascade LPS Discriminator
│   ├── anomaly_injector.py  # 异常注入
│   ├── metrics_collector.py # 指标收集
│   └── visualizer.py        # 结果可视化
├── scripts/                  # 运行脚本
│   ├── setup_environment.sh # 环境搭建
│   ├── run_tsbs.sh          # 运行TSBS基准测试
│   ├── inject_anomalies.sh  # 注入异常
│   └── run_experiment.py    # 主实验脚本
└── notebooks/                # Jupyter notebooks
    ├── data_analysis.ipynb  # 数据分析
    └── results_visualization.ipynb # 结果可视化

```

## 快速开始

### 方式1: 运行演示实验（推荐）

不需要IoTDB环境，直接运行模拟实验：

```bash
# 运行演示实验
python3 demo_experiment.py

# 查看可视化结果
python3 visualize_results.py

# 查看报告
cat demo_results/experiment_report.md
```

### 方式2: 完整实验（需要Docker）

#### 1. 一键搭建环境

```bash
# 自动安装并启动IoTDB集群
bash scripts/setup_environment.sh
```

这个脚本会：
- ✓ 检查Docker和Docker Compose
- ✓ 创建必要的目录
- ✓ 拉取Docker镜像
- ✓ 启动IoTDB集群（3数据节点 + 1配置节点）
- ✓ 启动Prometheus和Grafana监控
- ✓ 验证集群状态

#### 2. 手动配置（可选）

如果需要自定义配置：

```bash
# 编辑IoTDB配置
vim config/iotdb_config.yaml

# 编辑实验配置
vim config/experiment_config.yaml

# 启动集群
docker-compose up -d

# 查看集群状态
docker-compose ps
```

#### 3. 运行实验

```bash
# 完整实验流程
python scripts/run_experiment.py --config config/experiment_config.yaml

# 或分步骤运行
bash scripts/run_tsbs.sh
python scripts/run_experiment.py --phase train
python scripts/run_experiment.py --phase test
```

### 访问信息

启动后可以访问：

- **IoTDB数据节点1**: `localhost:6667`
- **IoTDB数据节点2**: `localhost:6668`
- **IoTDB数据节点3**: `localhost:6669`
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

连接IoTDB CLI:
```bash
docker exec -it iotdb-datanode-1 /iotdb/sbin/start-cli.sh -h localhost -p 6667
```

## 实验参数

### 触发阈值测试

测试不同的 θ = β/(α+β) 值：
- θ = 0.00, 0.01, 0.02, 0.03, 0.05, 0.10

### 评估指标

1. **日志体积**
   - 日志生成速率 (MB/s)
   - 总日志大小 (GB)
   - 日志压缩比

2. **吞吐量**
   - 写入吞吐量 (records/s)
   - CPU使用率 (%)
   - 内存使用率 (%)

3. **准确率**
   - 异常检测: Precision, Recall, F1-score
   - 异常诊断: Macro-P, Macro-R, Macro-F1

## 结果输出

实验结果将保存在 `data/results/` 目录：
- `metrics_*.csv`: 各项指标数据
- `curves_*.png`: 三维曲线图
- `comparison_*.json`: 与SOTA方法对比
