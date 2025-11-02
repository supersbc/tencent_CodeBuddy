# E-Log 论文分析与实验复现计划

## 论文概述

**标题**: E-Log: Fine-Grained Elastic Log-Based Anomaly Detection and Diagnosis for Databases

**发表**: IEEE Transactions on Services Computing, Vol. 18, No. 5, September/October 2025

**核心贡献**:
- 提出了一种细粒度弹性日志框架，在正常运行时使用轻量级日志进行异常检测，在检测到异常时触发详细日志进行诊断
- 在Apache IoTDB上实现并评估，使用TSBS、TPCx-IoT和IoT-Bench基准测试
- 相比SOTA方法，异常检测准确率提升3.15%，诊断性能提升9.32%
- 日志存储减少43.53%，平均写入吞吐量提升26.22%

## 关键技术点

### 1. 系统架构
E-Log包含三个主要组件：
- **Detection**: 基于LSTM和自注意力机制的异常检测模型 + LPS Reducer（强化学习）
- **Diagnosis**: 基于LSTM和自注意力机制的异常诊断模型 + Cascade LPS Discriminator
- **Database**: Class LPS Adjuster（基于Log4J的类级别日志调整接口）

### 2. 核心算法

#### LPS Reducer（日志点减少器）
- 使用多智能体强化学习动态调整日志量
- 状态表示: St = {(Lt,i, Rt,i, at,i, bt,i), ..., Pt-1}
- 动作空间: At ∈ {DISABLE at,i, ENABLE bt,i}
- 奖励函数: Rt = α·(精度变化 + 召回率变化 + F1变化) + β·(日志减少量)
- 参数设置: α=100, β=1 (α >> β 以优先保持检测准确性)

#### Cascade LPS Discriminator（级联日志点判别器）
- 当检测到异常时，自动追踪代码调用链
- TraceUp: 向上追踪父代码块的日志点
- TraceDown: 向下追踪子代码块的日志点
- 启用完整调用链的相关日志进行诊断

### 3. 模型设计
- **日志解析**: 使用Drain算法
- **日志分组**: 固定时间窗口（5秒）
- **特征提取**: 
  - 顺序嵌入 (Sequential Embedding): Et
  - 数量嵌入 (Quantitative Embedding): Ct
  - 语义嵌入 (Semantic Embedding): Vt (使用Word2Vec)
- **模型结构**: LSTM + Self-Attention + 全连接层
- **隐藏层大小**: 64

## 实验设置详情

### 1. 实验平台
- **数据库**: Apache IoTDB v1.2.2
- **部署**: 4个Docker容器（3个数据节点 + 1个配置节点）
- **硬件配置**:
  - CPU: 8 × Intel Xeon Platinum 8260 @ 2.40 GHz
  - 内存: 16 GB DIMM RAM
  - 磁盘: 1.1 TB NVMe
  - 系统: OpenJDK 11

### 2. 基准测试工具
1. **TSBS** (Time Series Benchmark Suite)
   - 广泛用于时序数据库测试
   - GitHub: https://github.com/timescale/tsbs

2. **TPCx-IoT**
   - 行业标准IoT网关系统基准测试
   - 提供可验证的性能、成本效益和可用性指标

3. **IoT-Bench**
   - Apache IoTDB官方基准测试工具
   - arXiv:1901.08304

### 3. 异常注入类型（11种）

#### 系统资源不足（3种）
1. **CPU饱和**: 使用Chaos Mesh注入CPU压力
2. **内存不足**: 使用Chaos Mesh注入内存压力
3. **网络延迟/丢包**: 使用Chaos Mesh注入网络故障

#### DBA操作异常（2种）
4. **过度导出操作**: 通过调整读写负载实现
5. **过度导入操作**: 通过调整读写负载实现

#### 系统配置错误（2种）
6. **后台任务过多**: 模拟LSM数据库中的compaction任务过多
7. **磁盘刷新过于频繁**: 修改数据库配置参数

#### 其他异常类型（4种）
8. **慢查询**
9. **数据倾斜**
10. **索引失效**
11. **事务冲突**

### 4. 数据集规模
- **总大小**: 20.59 GB
- **记录数**: 82,000,000条
- **异常类型**: 11种
- **数据集地址**: https://github.com/AIOPS-LogDB/E-Log-Dataset

### 5. 异常注入流程
```
正常运行 → 记录时间戳 → 注入异常 → 持续一段时间 → 记录时间戳 → 恢复正常 → 循环
```

## 实验复现计划

### 阶段1: 环境搭建
1. 安装Apache IoTDB v1.2.2
2. 配置Docker环境（3数据节点 + 1配置节点）
3. 安装TSBS基准测试工具
4. 安装Chaos Mesh用于异常注入

### 阶段2: 基准测试运行
1. 运行TSBS基准测试，收集正常日志
2. 使用Chaos Mesh注入不同类型异常
3. 记录日志数据、系统指标（CPU、内存、吞吐量）

### 阶段3: 模型实现
1. 实现日志解析（Drain算法）
2. 实现特征提取（顺序、数量、语义嵌入）
3. 实现LSTM + Self-Attention模型
4. 实现LPS Reducer（强化学习）
5. 实现Cascade LPS Discriminator

### 阶段4: 实验评估
**测试不同触发阈值（θ = β/(α+β)）**:
- θ = 0.00 (β=0, α=100)
- θ = 0.01 (β=1, α=100) ← 论文推荐
- θ = 0.02 (β=2, α=100)
- θ = 0.03 (β=3, α=100)
- θ = 0.05 (β=5, α=100)
- θ = 0.10 (β=10, α=100)

**测试不确定性触发**:
- 基于模型置信度的动态阈值
- 基于异常分数的自适应触发

**记录三维曲线数据**:
1. **日志体积**: 
   - 正常运行时的日志生成速率
   - 异常诊断时的日志生成速率
   - 总体日志存储大小

2. **吞吐量**:
   - 写入吞吐量（records/sec）
   - CPU使用率
   - 内存使用率

3. **准确率**:
   - 异常检测: Precision, Recall, F1-score
   - 异常诊断: Macro Precision, Macro Recall, Macro F1-score

### 阶段5: 结果分析与可视化
1. 绘制三维曲线图
2. 对比不同阈值下的性能
3. 分析不确定性触发的效果
4. 与SOTA方法对比

## 关键实验参数

| 参数 | 值 | 说明 |
|------|-----|------|
| 时间窗口 | 5秒 | 日志分组窗口大小 |
| LSTM隐藏层 | 64 | 模型隐藏层维度 |
| α (LPS Reducer) | 100 | 准确率权重 |
| β (LPS Reducer) | 1 | 日志减少权重 |
| 日志级别 | Info | 基线对比 |
| 批次大小 | 32 | 模型训练批次 |
| 学习率 | 0.001 | 优化器学习率 |

## 预期结果

根据论文报告的结果：
- **异常检测F1**: 提升3.15%（相比SOTA）
- **异常诊断F1**: 提升9.32%（相比SOTA）
- **日志存储**: 减少43.53%（相比info-level）
- **写入吞吐量**: 提升26.22%（相比info-level）

## 参考文献

1. TSBS: https://github.com/timescale/tsbs
2. Apache IoTDB: https://iotdb.apache.org/
3. Chaos Mesh: https://chaos-mesh.org/
4. E-Log Dataset: https://github.com/AIOPS-LogDB/E-Log-Dataset
5. Drain算法: He et al., "Drain: An online log parsing approach with fixed depth tree", ICWS 2017
