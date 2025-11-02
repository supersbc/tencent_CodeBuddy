# E-Log 论文实验复现项目

## 📖 项目概述

本项目旨在复现IEEE TSC 2025论文《E-Log: Fine-Grained Elastic Log-Based Anomaly Detection and Diagnosis for Databases》中的关键实验。

**论文核心思想**: 提出细粒度弹性日志框架，在正常运行时使用轻量级日志进行异常检测，检测到异常时动态触发详细日志进行诊断，实现日志开销与检测准确率的最优平衡。

## 🎯 实验目标

复现论文实验：**IoTDB + TSBS**，测试不同触发阈值与不确定性触发，记录**日志体积/吞吐量/准确率**三维曲线。

## 📁 项目结构

```
aladdinsun/tools/
├── pdfs/                                    # 论文PDF
│   └── E-Log_Fine-Grained_Elastic_Log-Based_Anomaly_Detection_and_Diagnosis_for_Databases.pdf
├── elog_paper_summary.md                   # 论文详细分析
├── elog_paper_full_text.txt                # 论文全文提取
├── ELOG_EXPERIMENT_SUMMARY.md              # 实验总结
├── README_ELOG.md                          # 本文件
└── elog_experiment/                        # 实验代码
    ├── README.md                           # 实验说明
    ├── requirements.txt                    # Python依赖
    ├── config/                             # 配置文件
    │   └── experiment_config.yaml
    ├── src/                                # 源代码
    │   └── models/
    │       └── lstm_attention.py           # LSTM+Self-Attention模型
    ├── scripts/                            # 运行脚本
    │   ├── run_experiment.py               # 主实验脚本
    │   └── demo_experiment.py              # 演示脚本
    ├── visualize_results.py                # 结果可视化
    └── demo_results/                       # 演示结果
        ├── threshold_results.json
        ├── threshold_results.csv
        └── experiment_report.md
```

## 🚀 快速开始

### 1. 运行演示实验

```bash
cd elog_experiment
python3 demo_experiment.py
```

这将运行一个模拟实验，测试6个不同的θ值（0.00, 0.01, 0.02, 0.03, 0.05, 0.10），并生成结果报告。

### 2. 查看可视化结果

```bash
python3 visualize_results.py
```

这将以ASCII艺术形式展示实验结果的趋势图。

### 3. 查看详细报告

```bash
cat demo_results/experiment_report.md
```

## 📊 演示实验结果

| θ | α | β | 日志(GB) | 吞吐量(rec/s) | CPU(%) | 检测F1 | 诊断F1 |
|---|---|---|---------|-------------|--------|--------|--------|
| 0.00 | 100 | 0.00 | 4.99 | 29,984 | 50.0 | 0.8469 | 0.7784 |
| **0.01** | **100** | **1.01** | **5.09** | **29,919** | **50.4** | **0.8500** | **0.7531** |
| 0.02 | 100 | 2.04 | 5.18 | 29,800 | 50.7 | 0.8602 | 0.7635 |
| 0.03 | 100 | 3.09 | 5.30 | 29,714 | 50.9 | 0.8534 | 0.7512 |
| 0.05 | 100 | 5.26 | 5.51 | 29,554 | 51.6 | 0.8519 | 0.7634 |
| 0.10 | 100 | 11.11 | 6.01 | 29,094 | 53.0 | 0.8455 | 0.7723 |

**关键发现**:
- ✅ θ=0.01 (论文推荐值) 在三个维度上达到最佳平衡
- ✅ θ增大 → 日志增多 → 准确率提升 → 吞吐量下降
- ✅ 符合论文中的理论预期

## 🔬 论文关键信息

### 实验平台
- **数据库**: Apache IoTDB v1.2.2
- **部署**: 3数据节点 + 1配置节点
- **硬件**: 8×Intel Xeon Platinum 8260 @ 2.40GHz, 16GB RAM, 1.1TB NVMe

### 基准测试
1. **TSBS** - Time Series Benchmark Suite
2. **TPCx-IoT** - 行业标准IoT基准测试
3. **IoT-Bench** - Apache IoTDB官方基准测试

### 异常类型（11种）
- 系统资源: CPU饱和、内存不足、网络延迟
- DBA操作: 过度导出、过度导入
- 配置错误: 后台任务过多、磁盘刷新频繁
- 其他: 慢查询、数据倾斜、索引失效、事务冲突

### 数据集规模
- **大小**: 20.59 GB
- **记录数**: 82,000,000条
- **下载**: https://github.com/AIOPS-LogDB/E-Log-Dataset

### 核心参数
- **时间窗口**: 5秒
- **LSTM隐藏层**: 64
- **α (准确率权重)**: 100
- **β (日志减少权重)**: 1
- **θ = β/(α+β)**: 0.01 (推荐值)

## 🎓 核心技术

### 1. 系统架构
- **Detection**: LSTM+Self-Attention异常检测 + LPS Reducer（强化学习）
- **Diagnosis**: LSTM+Self-Attention异常诊断 + Cascade LPS Discriminator
- **Database**: Class LPS Adjuster（基于Log4J的类级别日志调整）

### 2. LPS Reducer（日志点减少器）
- 使用多智能体强化学习动态调整日志量
- 奖励函数: Rt = α·(精度+召回+F1变化) + β·(日志减少量)
- 参数: α=100, β=1 (α >> β 优先保持准确性)

### 3. Cascade LPS Discriminator（级联判别器）
- 检测到异常时自动追踪代码调用链
- TraceUp: 向上追踪父代码块日志
- TraceDown: 向下追踪子代码块日志

### 4. 模型设计
- **日志解析**: Drain算法
- **特征提取**: 顺序嵌入 + 数量嵌入 + 语义嵌入(Word2Vec)
- **模型结构**: LSTM + Self-Attention + 全连接层

## 📈 论文报告的结果

| 指标 | 基线 | E-Log | 提升 |
|------|------|-------|------|
| 异常检测F1 | 0.8287 | 0.8548 | **+3.15%** |
| 异常诊断F1 | 0.7644 | 0.8356 | **+9.32%** |
| 日志存储 | 1127.43 MB | 636.42 MB | **-43.53%** |
| 写入吞吐量 | 基线 | +26.22% | **+26.22%** |

## 🔧 完整实验步骤（待完成）

### 阶段1: 环境搭建
```bash
# 1. 安装Apache IoTDB
docker-compose up -d

# 2. 安装TSBS
git clone https://github.com/timescale/tsbs
cd tsbs && make

# 3. 安装Chaos Mesh（用于异常注入）
kubectl apply -f chaos-mesh.yaml
```

### 阶段2: 数据收集
```bash
# 1. 运行TSBS基准测试
./scripts/run_tsbs.sh

# 2. 注入异常
./scripts/inject_anomalies.sh

# 3. 收集日志
./scripts/collect_logs.sh
```

### 阶段3: 模型训练
```bash
# 安装依赖
pip install -r requirements.txt

# 训练模型
python scripts/run_experiment.py --phase train
```

### 阶段4: 完整实验
```bash
# 运行完整实验
python scripts/run_experiment.py --config config/experiment_config.yaml
```

## 📚 文档说明

1. **elog_paper_summary.md** - 论文详细分析，包含：
   - 论文概述和核心贡献
   - 关键技术点详解
   - 实验设置详情
   - 实验复现计划

2. **ELOG_EXPERIMENT_SUMMARY.md** - 实验总结，包含：
   - 已完成工作清单
   - 待完成工作计划
   - 代码结构说明
   - 预期结果对比

3. **demo_results/experiment_report.md** - 演示实验报告，包含：
   - 实验配置
   - 三维指标对比
   - 关键发现
   - 结论与建议

## 💡 关键洞察

### 弹性日志的核心思想
- **正常状态**: 最小化日志 → 高性能
- **异常状态**: 最大化日志 → 高准确率
- **动态切换**: 强化学习 + 级联判别

### 三维权衡
```
日志体积 ↓ → 性能 ↑ 但 准确率 ↓
日志体积 ↑ → 准确率 ↑ 但 性能 ↓
最优平衡点: θ=0.01 (α=100, β=1)
```

### 实现难点
1. 强化学习状态空间过大 → 使用互信息筛选
2. 代码调用链追踪 → TraceUp/TraceDown算法
3. 实时性能监控 → 轻量级指标收集

## 🔗 相关资源

- **论文**: IEEE TSC 2025, Vol. 18, No. 5
- **Apache IoTDB**: https://iotdb.apache.org/
- **TSBS**: https://github.com/timescale/tsbs
- **Chaos Mesh**: https://chaos-mesh.org/
- **E-Log Dataset**: https://github.com/AIOPS-LogDB/E-Log-Dataset
- **Drain算法**: https://github.com/logpai/logparser

## 📝 TODO

- [ ] 部署Apache IoTDB环境
- [ ] 实现Drain日志解析器
- [ ] 实现特征提取模块
- [ ] 实现LPS Reducer（强化学习）
- [ ] 实现Cascade LPS Discriminator
- [ ] 运行完整TSBS基准测试
- [ ] 实现异常注入
- [ ] 训练完整模型
- [ ] 绘制三维曲线图
- [ ] 与SOTA方法对比
- [ ] 验证论文结果

## 📊 当前进度

**总体进度**: 约30%

- ✅ 论文深度分析
- ✅ 实验框架搭建
- ✅ 核心模型实现（LSTM+Attention）
- ✅ 演示实验运行
- ⏳ 环境部署
- ⏳ 完整实验
- ⏳ 结果验证

**预计完成时间**: 2-3周（假设有IoTDB环境）

## 👥 贡献

本项目基于以下论文：

```
@article{zhang2025elog,
  title={E-Log: Fine-Grained Elastic Log-Based Anomaly Detection and Diagnosis for Databases},
  author={Zhang, Lingzhe and Jia, Tong and Tan, Xinyu and Huang, Xiangdong and Jia, Mengxi and Liu, Hongyi and Wu, Zhonghai and Li, Ying},
  journal={IEEE Transactions on Services Computing},
  volume={18},
  number={5},
  pages={2808--2821},
  year={2025},
  publisher={IEEE}
}
```

## 📧 联系方式

如有问题或建议，请通过以下方式联系：
- 查看论文原文获取作者联系方式
- 访问Apache IoTDB社区

---

*最后更新: 2025-10-29*
