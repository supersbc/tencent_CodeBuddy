# TDSQL 部署资源预测系统 v4.0 - 部署指南

## 🎯 系统概述

本系统已完全重构，实现了您的所有需求：

### ✅ 已完成的功能

1. **取消独立文件上传页面** - 所有功能集成在一个页面
2. **改名为"部署资源预测"** - 系统标题和功能已更新
3. **文件上传集成到手动输入页面** - 支持拖拽和点击上传
4. **详细的架构设计** - 包含分片、副本、高可用配置
5. **完整的设备清单**：
   - 服务器清单（型号、CPU、内存、存储、网络、价格、功耗）
   - 网络设备清单（交换机、防火墙、负载均衡器、路由器）
   - 存储设备清单（SSD/HDD、容量、IOPS、吞吐量）
   - 基础设施清单（机柜、PDU、UPS、网线）
6. **详细的成本清单**：
   - 硬件成本（服务器、网络、存储、基础设施）
   - 软件许可证（TDSQL、操作系统、监控、备份）
   - 服务费用（部署实施、技术培训）
   - 年度运营成本（电费、制冷、维护）
   - 3年TCO计算
7. **网络拓扑设计**：
   - 8层网络架构
   - VLAN划分（DMZ、APP、PROXY、DB、MGMT）
   - 设备连接关系
8. **架构图可视化** - 节点和连接关系数据
9. **专业部署建议** - 性能优化、高可用、监控、安全、备份等

## 📁 核心文件说明

### 1. 后端文件

- **`deployment_predictor.py`** (955行) - 核心预测引擎
  - 服务器配置库（7种规格）
  - 网络设备库（7种设备）
  - 存储设备库（3种类型）
  - 软件许可证库
  - 智能资源计算算法
  - 成本分析引擎
  - 架构设计引擎

- **`app.py`** (248行) - Flask应用主程序
  - `/` - 主页面
  - `/api/predict` - 预测接口
  - `/api/upload` - 文件上传接口
  - `/api/health` - 健康检查

### 2. 前端文件

- **`templates/index.html`** (1234行) - 主页面
  - 文件上传区域（支持拖拽）
  - 参数表单（8个参数）
  - 7个结果标签页
  - 完整的数据展示

### 3. 文档文件

- **`README_v4.md`** - 完整使用文档
- **`DEPLOYMENT_GUIDE_v4.md`** - 本文件
- **`start_predictor.sh`** - 启动脚本

## 🚀 快速启动

### 方法1：使用启动脚本

```bash
cd /Users/aladdin/Documents/gitdata/tencent_CodeBuddy/aladdinsun/AIdatabase
chmod +x start_predictor.sh
./start_predictor.sh
```

### 方法2：手动启动

```bash
cd /Users/aladdin/Documents/gitdata/tencent_CodeBuddy/aladdinsun/AIdatabase

# 安装依赖
pip3 install Flask openpyxl Pillow PyPDF2 pytesseract Werkzeug

# 启动服务
python3 app.py
```

### 方法3：后台运行

```bash
cd /Users/aladdin/Documents/gitdata/tencent_CodeBuddy/aladdinsun/AIdatabase

# 停止旧服务
lsof -ti:5173 | xargs kill -9 2>/dev/null

# 启动新服务
nohup python3 app.py > server.log 2>&1 &

# 查看日志
tail -f server.log
```

## 🌐 访问系统

启动成功后，在浏览器中访问：

```
http://127.0.0.1:5173
```

## 📊 使用示例

### 示例1：手动输入

1. 打开页面
2. 填写参数：
   - QPS: 5000
   - 数据量: 500 GB
   - 高可用级别: 高
   - 行业: 金融
3. 点击"开始预测"
4. 查看7个标签页的详细结果

### 示例2：文件上传

1. 准备JSON文件：
```json
{
  "qps": 5000,
  "data_volume": 500,
  "ha_level": "high",
  "industry": "finance"
}
```

2. 拖拽文件到上传区域
3. 系统自动提取参数并填充表单
4. 可手动修改参数
5. 点击"开始预测"

### 示例3：Excel文件上传

创建Excel文件，格式如下：

| 参数名称 | 参数值 |
|---------|--------|
| QPS | 5000 |
| 数据量(GB) | 500 |
| 高可用级别 | high |
| 行业 | 金融 |

上传后自动识别并填充。

## 📈 预测结果详解

### 1. 概览标签页

显示6个关键指标卡片：
- 系统规模（SMALL/MEDIUM/LARGE/XLARGE）
- QPS（每秒查询数）
- 数据量（GB）
- 服务器数量
- 初始投资（万元）
- 3年TCO（万元）

### 2. 架构设计标签页

- **架构类型**：单主从/分片集群/分布式集群
- **拓扑配置**：分片数、副本数、各类节点数量
- **高可用配置**：故障转移、备份策略、容灾方案

### 3. 设备清单标签页

#### 服务器清单表格
| 编号 | 角色 | 型号 | CPU | 内存 | 存储 | 网络 | 单价 | 功耗 |
|------|------|------|-----|------|------|------|------|------|
| db-01 | 数据库节点(Shard-1 MASTER) | Dell R640 | 16核 Gold 5218 | 64GB | 2TB SSD | 双万兆 | ¥45,000 | 500W |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

#### 网络设备清单表格
| 编号 | 类型 | 型号 | 规格 | 单价 | 功耗 |
|------|------|------|------|------|------|
| core-sw-01 | 核心交换机(主) | Cisco Nexus 93180YC-FX | 48x10Gbps | ¥85,000 | 250W |
| ... | ... | ... | ... | ... | ... |

#### 存储设备清单
| 类型 | 型号 | 容量 | IOPS | 吞吐量 | 总价 |
|------|------|------|------|--------|------|
| SSD SATA | Samsung 870 EVO | 2TB | 50,000 | 550MB/s | ¥2,400 |

#### 基础设施清单
| 类型 | 数量 | 单价 | 总价 |
|------|------|------|------|
| 42U标准机柜 | 1 | ¥8,000 | ¥8,000 |
| PDU电源分配单元 | 2 | ¥3,000 | ¥6,000 |
| UPS不间断电源 | 15kW | ¥5,000/kW | ¥75,000 |

### 4. 网络拓扑标签页

**8层网络架构**：
1. Internet接入层 → router-01
2. DMZ安全区 → firewall-01/02, lb-01/02
3. 核心交换层 → core-sw-01/02
4. 接入交换层 → access-sw-*
5. 应用服务层 → app-*
6. TDSQL代理层 → proxy-*
7. 数据库层 → db-*
8. 管理监控层 → monitor-01, backup-01

**VLAN划分**：
- VLAN 10: DMZ (10.0.10.0/24)
- VLAN 20: APP (10.0.20.0/24)
- VLAN 30: PROXY (10.0.30.0/24)
- VLAN 40: DB (10.0.40.0/24)
- VLAN 50: MGMT (10.0.50.0/24)

### 5. 成本分析标签页

**成本汇总**：
- 初始投资总额：¥XXX,XXX
- 3年总拥有成本(TCO)：¥XXX,XXX

**硬件成本**：
- 服务器：¥XXX,XXX
- 网络设备：¥XXX,XXX
- 存储设备：¥XXX,XXX
- 基础设施：¥XXX,XXX

**软件许可证**：
- TDSQL许可证：¥XXX,XXX
- 操作系统许可证：¥XXX,XXX
- 监控软件：¥XXX,XXX
- 备份软件：¥XXX,XXX

**服务费用**：
- 部署实施：¥XXX,XXX
- 技术培训：¥50,000

**年度运营成本**：
- 电费：¥XXX,XXX/年
- 制冷费用：¥XXX,XXX/年
- 软件维护：¥XXX,XXX/年

### 6. 架构图标签页

显示系统架构拓扑图，包含：
- 节点数量和类型
- 连接关系
- 分层结构

### 7. 部署建议标签页

根据系统规模和配置，提供：
- 🔴 高优先级建议（红色边框）
- 🟠 中优先级建议（橙色边框）
- 🔵 普通建议（蓝色边框）

建议类别：
- 性能优化
- 高可用
- 监控运维
- 安全加固
- 数据备份
- 容量规划

## 🔧 技术架构

### 后端技术栈
- **Flask** - Web框架
- **Python 3.7+** - 编程语言
- **openpyxl** - Excel文件处理
- **Pillow** - 图片处理
- **pytesseract** - OCR识别
- **PyPDF2** - PDF文件处理

### 前端技术栈
- **原生HTML5** - 页面结构
- **原生CSS3** - 样式设计
- **原生JavaScript** - 交互逻辑
- **无依赖** - 不需要任何前端框架

### 核心算法

#### 1. CPU核心数估算
```python
cores_for_qps = (qps / 1000) * 4
cores_for_tps = (tps / 1000) * 8
total_cores = max(cores_for_qps, cores_for_tps)
```

#### 2. 内存需求估算
```python
memory_for_data = data_size_gb * 0.2
memory_for_qps = (qps / 1000) * 4
total_memory = memory_for_data + memory_for_qps
```

#### 3. 规模等级判断
```python
if qps < 1000 and data_size_gb < 100:
    scale = 'small'
elif qps < 5000 and data_size_gb < 1000:
    scale = 'medium'
elif qps < 20000 and data_size_gb < 10000:
    scale = 'large'
else:
    scale = 'xlarge'
```

#### 4. 架构类型选择
```python
if scale == 'small':
    arch_type = 'single_master_slave'
    shard_count = 1
    replica_count = 2 if ha_level == 'high' else 1
elif scale in ['medium', 'large', 'xlarge']:
    arch_type = 'sharded'
    shard_count = 2/4/8  # 根据规模
    replica_count = 2/3  # 根据HA级别
```

## 🎨 界面特点

### 1. 现代化设计
- 渐变色背景
- 卡片式布局
- 圆角设计
- 阴影效果

### 2. 交互体验
- 拖拽上传
- 自动填充高亮
- 平滑滚动
- 标签页切换
- 响应式布局

### 3. 数据展示
- 表格展示
- 卡片展示
- 列表展示
- 图表展示（架构图）

## 📝 与之前版本的对比

| 特性 | v3.2 | v4.0 |
|------|------|------|
| 页面数量 | 2个（手动输入+文件上传） | 1个（融合） |
| 系统名称 | TDSQL架构预测 | 部署资源预测 |
| 设备清单 | 简单 | 详细（型号、规格、价格） |
| 成本清单 | 基础 | 详细（硬件、软件、服务、运营） |
| 网络拓扑 | 无 | 完整（8层架构+VLAN） |
| 架构图 | 无 | 有（可视化数据） |
| 部署建议 | 简单 | 详细（分类、优先级） |
| 文件上传 | 独立页面 | 集成到主页面 |

## 🔍 测试验证

### 1. 健康检查
```bash
curl http://127.0.0.1:5173/api/health
```

### 2. 预测测试
```bash
curl -X POST http://127.0.0.1:5173/api/predict \
  -H "Content-Type: application/json" \
  -d '{"qps":5000,"data_volume":500,"ha_level":"high"}'
```

### 3. 文件上传测试
```bash
curl -X POST http://127.0.0.1:5173/api/upload \
  -F "file=@test_data.json"
```

## 🐛 故障排查

### 问题1：端口被占用
```bash
# 查找占用端口的进程
lsof -ti:5173

# 杀死进程
lsof -ti:5173 | xargs kill -9
```

### 问题2：依赖缺失
```bash
# 安装所有依赖
pip3 install Flask openpyxl Pillow PyPDF2 pytesseract Werkzeug
```

### 问题3：OCR不可用
OCR功能是可选的，如果pytesseract不可用，系统会自动降级到基础文件解析。

## 📞 技术支持

如有问题，请查看：
1. `server.log` - 服务器日志
2. 浏览器控制台 - 前端错误
3. `README_v4.md` - 详细文档

## 🎉 总结

v4.0版本完全满足您的需求：
- ✅ 取消了独立的文件上传页面
- ✅ 改名为"部署资源预测"
- ✅ 文件上传集成到手动输入页面
- ✅ 提供详细的架构设计
- ✅ 提供完整的设备清单（服务器、交换机、存储等）
- ✅ 提供详细的成本清单（硬件、软件、服务、运营）
- ✅ 提供网络拓扑设计
- ✅ 提供架构图可视化
- ✅ 提供专业的部署建议

系统现在可以生成专业级的部署方案报告！
