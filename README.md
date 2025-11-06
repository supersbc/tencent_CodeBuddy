# AIdatabase - AI部署资源预测系统

## 📋 项目简介

智能化的数据库/AI系统部署资源预测工具,通过机器学习算法预测系统部署所需的硬件资源配置。

## 🌟 主要功能

- **智能预测**: 基于历史数据预测部署资源需求(CPU/内存/存储/网络)
- **多系统支持**: 支持复杂的多系统环境部署
- **模型库管理**: 预置8个行业模型库(腾讯官方、阿里云、GitHub开源等)
- **图像识别**: 支持架构图OCR识别,自动提取参数
- **参数可视化**: 专业参数表单生成和Excel模板导入导出

## 📦 项目结构

```
AIdatabase/
├── app.py                      # Flask主程序
├── deployment_predictor.py     # 部署预测核心引擎
├── model_library_manager.py    # 模型库管理器
├── requirements.txt            # Python依赖包
│
├── model_libraries/            # 预置模型库(8个)
│   ├── tencent_official_v2.1.0.json       # 腾讯官方模型库
│   ├── alibaba_cloud_v1.6.2.json          # 阿里云模型库
│   ├── github_opensource_v2.0.5.json      # GitHub开源模型库
│   ├── community_finance_v1.8.3.json      # 金融行业模型库
│   ├── community_ecommerce_v1.5.2.json    # 电商行业模型库
│   ├── community_gaming_v1.3.1.json       # 游戏行业模型库
│   ├── huggingface_v1.2.0.json            # HuggingFace模型库
│   └── kaggle_winner_v1.0.8.json          # Kaggle获奖模型库
│
├── templates/                  # Web界面模板
│   ├── index.html              # 主页面
│   ├── predict_v2.html         # 预测界面(专业版)
│   ├── model_library.html      # 模型库管理
│   └── ...
│
├── static/                     # 静态资源
│   ├── script.js               # 前端逻辑
│   ├── style.css               # 样式表
│   └── ...
│
├── training_data/              # 训练数据
│   └── cases.json              # 历史案例数据
│
├── uploads/                    # 用户上传文件目录
│
└── 文档/                       # 项目文档
    ├── 快速使用指南-v3.0.md
    ├── 多系统复杂部署使用指南.md
    ├── 模型库使用指南.md
    ├── DEPLOYMENT_GUIDE.md
    └── ...
```

## 🚀 快速开始

### 1. 环境要求

- Python 3.7+
- pip

### 2. 安装依赖

```bash
cd AIdatabase
pip install -r requirements.txt
```

### 3. 启动服务

```bash
# 方式1: 使用启动脚本
bash start.sh

# 方式2: 直接运行
python app.py
```

### 4. 访问系统

浏览器访问: **https://aladdinsun.devcloud.woa.com/**

## 📊 核心功能详解

### 1. 智能资源预测

基于机器学习算法,输入系统参数后自动预测:
- **CPU**: 核心数、主频要求
- **内存**: 容量需求、类型建议
- **存储**: 磁盘空间、IOPS、吞吐量
- **网络**: 带宽需求、延迟要求

### 2. 预置模型库

系统预置8个行业模型库,覆盖不同场景:

| 模型库 | 版本 | 适用场景 | 案例数 |
|--------|------|----------|--------|
| 腾讯官方 | v2.1.0 | 企业级应用 | 500+ |
| 阿里云 | v1.6.2 | 云原生应用 | 400+ |
| GitHub开源 | v2.0.5 | 开源项目 | 600+ |
| 金融行业 | v1.8.3 | 金融系统 | 350+ |
| 电商行业 | v1.5.2 | 电商平台 | 300+ |
| 游戏行业 | v1.3.1 | 游戏服务器 | 250+ |
| HuggingFace | v1.2.0 | AI模型部署 | 200+ |
| Kaggle获奖 | v1.0.8 | 数据科学 | 150+ |

### 3. 多系统复杂环境

支持复杂的多系统环境部署预测:
- 跨数据中心部署
- 主备/灾备配置
- 微服务架构
- 分布式数据库集群

### 4. 智能识别功能

- **架构图OCR**: 上传架构图自动识别系统组件
- **Excel导入**: 批量导入部署参数
- **参数提取**: 自动提取关键配置信息

## 📖 使用指南

### 基础使用流程

1. **选择模型库**: 根据业务场景选择合适的模型库
2. **输入参数**: 填写系统基础参数(用户数、数据量等)
3. **获取预测**: 系统自动计算资源需求
4. **导出报告**: 生成详细的资源配置报告

### 进阶功能

- **自定义模型库**: 创建专属的预测模型
- **参数学习**: 系统从历史案例中学习优化
- **多方案对比**: 生成多个配置方案供选择

详细文档请查看:
- [快速使用指南](./AIdatabase/快速使用指南-v3.0.md)
- [多系统复杂部署使用指南](./AIdatabase/多系统复杂部署使用指南.md)
- [模型库使用指南](./AIdatabase/模型库使用指南.md)

## 📈 项目统计

- **文件总数**: 168个
- **代码行数**: 约15,000行
- **主要语言**: Python (85%), JavaScript (10%), HTML/CSS (5%)
- **模型库**: 8个预置 + 支持自定义
- **历史案例**: 2,750+ 真实部署案例

## 🔧 技术栈

### 后端
- **Web框架**: Flask 2.0+
- **机器学习**: scikit-learn, pandas, numpy
- **图像识别**: PaddleOCR (可选)
- **数据处理**: pandas, openpyxl

### 前端
- **UI框架**: Bootstrap 4
- **交互**: jQuery, Ajax
- **可视化**: Chart.js (可选)

### 部署
- **Web服务器**: Flask内置 / Nginx + uWSGI
- **Python版本**: 3.7+
- **操作系统**: Linux / macOS / Windows

## 🎯 应用场景

1. **数据库部署规划**
   - MySQL/PostgreSQL集群
   - MongoDB分片集群
   - Redis缓存集群

2. **AI系统部署**
   - TensorFlow Serving
   - PyTorch模型推理
   - ONNX Runtime部署

3. **大数据平台**
   - Hadoop/Spark集群
   - Kafka消息队列
   - Elasticsearch搜索引擎

4. **云原生应用**
   - Kubernetes集群
   - Docker容器化
   - 微服务架构

## 📝 版本历史

- **v4.3** (2025-11-06): 增强多系统复杂部署功能
- **v4.2** (2025-10): 新增8个预置模型库
- **v4.0** (2025-09): 重构预测引擎,提升准确率
- **v3.2** (2025-08): 新增架构图OCR识别
- **v3.0** (2025-07): 引入机器学习预测模型

详见: [更新日志](./AIdatabase/更新日志_v4.2.md)

## 🤝 贡献指南

欢迎提交Issue和Pull Request!

## 📞 技术支持

如有问题,请联系:
- **项目负责人**: aladdinsun
- **电话**: 15271909262
- **邮箱**: aladdinsun@tencent.com

## 📄 许可证

内部项目,仅供腾讯内部使用。

---

**最后更新**: 2025-11-06  
**项目状态**: 🟢 活跃维护中
