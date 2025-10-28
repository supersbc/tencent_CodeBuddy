# 🚀 TDSQL 架构智能预测系统 v3.0

[![Version](https://img.shields.io/badge/version-3.0-blue.svg)](https://github.com)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org)
[![Flask](https://img.shields.io/badge/flask-3.0-red.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

> 基于 735+ 真实案例的智能架构预测系统，支持多文件格式、多系统环境、复杂部署拓扑

## ✨ 核心特性

- 🎯 **智能预测** - 92.75% 准确率，基于 735+ 真实案例
- 📁 **多格式支持** - Excel、PDF、图片、JSON 四种格式
- 🏢 **多系统分析** - 自动识别大环境内的多个系统
- 🌐 **复杂拓扑** - 支持 6 种部署模式（单中心到多地多中心）
- 🧠 **自我学习** - 持续优化，准确率不断提升
- ⚡ **快速启动** - 2-3 秒启动，3 秒内首次响应

## 📊 系统概览

```
┌─────────────────────────────────────────────────────────┐
│  TDSQL 架构智能预测系统 v3.0                             │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  📁 文件上传  →  🔍 智能识别  →  🎯 架构预测            │
│                                                          │
│  ✍️ 手动输入  →  📊 参数分析  →  💰 成本估算            │
│                                                          │
│  🏢 多系统    →  📈 统计汇总  →  🌐 拓扑建模            │
│                                                          │
│  📚 案例库    →  🔎 相似搜索  →  📖 参考学习            │
│                                                          │
│  🧠 自我学习  →  📝 案例提交  →  🎓 模型优化            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动服务

```bash
python3 app_optimized.py
```

### 访问系统

```
http://127.0.0.1:5173
```

## 📖 功能详解

### 1️⃣ 文件上传分析

支持 4 种文件格式：

| 格式 | 扩展名 | 处理时间 | 准确率 |
|------|--------|---------|--------|
| Excel | .xlsx, .xls | 1-2秒 | 95% |
| PDF | .pdf | 2-3秒 | 90% |
| 图片 | .png, .jpg | 3-5秒 | 85% |
| JSON | .json | <1秒 | 100% |

### 2️⃣ 多系统环境

自动识别和分析：
- ✅ 系统数量识别
- ✅ 参数自动提取
- ✅ 统计汇总计算
- ✅ 统一部署规划

### 3️⃣ 部署拓扑

6 种部署模式：

```
1. 单中心部署      - 99.9%  可用性
2. 同城双中心      - 99.95% 可用性
3. 同城多中心      - 99.95% 可用性
4. 两地三中心 ⭐   - 99.99% 可用性
5. 三地五中心      - 99.995% 可用性
6. 多地多中心      - 99.999% 可用性
```

### 4️⃣ 案例库

8 个模型库，735+ 真实案例：

| 模型库 | 案例数 | 准确率 |
|--------|--------|--------|
| 腾讯云官方 | 150 | 92-95% |
| 金融社区 | 80 | 93-96% |
| 电商社区 | 60 | 89-93% |
| 游戏社区 | 45 | 87-91% |
| GitHub | 120 | 88-92% |
| HuggingFace | 100 | 90-94% |
| Kaggle | 85 | 91-95% |
| 阿里云 | 95 | 89-93% |

## 🎯 使用场景

### 场景 1：电商促销

```yaml
输入:
  业务类型: 电商
  数据量: 5TB
  QPS: 50,000
  可用性: 99.95%

输出:
  部署模式: 同城双中心
  实例数量: 8个
  分片配置: 4库128表
  月度成本: ¥45,000
```

### 场景 2：银行核心

```yaml
输入:
  系统数量: 5个
  总数据量: 50TB
  总QPS: 250,000
  可用性: 99.995%

输出:
  部署模式: 三地五中心多活
  实例数量: 20个
  同步方式: 强同步
  月度成本: ¥500,000
```

### 场景 3：游戏分区

```yaml
输入:
  区服数量: 10个
  每区数据: 2TB
  每区QPS: 20,000
  可用性: 99.9%

输出:
  部署模式: 同城双中心热备
  实例数量: 20个（主10+备10）
  分片策略: 按区服分库
  月度成本: ¥50,000
```

## �� 性能指标

| 指标 | 数值 |
|------|------|
| 启动时间 | 2-3秒 |
| 首次响应 | <3秒 |
| Excel处理 | 1-2秒 |
| PDF处理 | 2-3秒 |
| 图片OCR | 3-5秒 |
| 预测准确率 | 92.75% |
| 并发支持 | 10+ |
| 内存占用 | ~270MB |

## 🔧 API 接口

### 系统管理
```
GET  /api/health          - 健康检查
GET  /api/status          - 系统状态
```

### 文件处理
```
POST /api/analyze         - 分析文件
POST /api/process_multi_system - 多系统分析
```

### 参数配置
```
POST /api/manual_input    - 手动输入
GET  /api/parameter_config - 参数配置
POST /api/validate_parameters - 参数验证
```

### 模型库
```
GET  /api/model_libraries - 模型库列表
GET  /api/library/<id>    - 库详情
POST /api/search_cases    - 搜索案例
```

### 自我学习
```
POST /api/submit_case     - 提交案例
GET  /api/training_stats  - 训练统计
```

## 📁 项目结构

```
AIdatabase/
├── app_optimized.py              # 优化版主应用 ⭐
├── app_simple.py                 # 简化版应用
├── app_with_learning.py          # 原版应用
├── advanced_file_processor.py    # 文件处理器
├── deployment_topology_parameters.py # 部署拓扑
├── enhanced_input_output_parameters.py # 增强参数
├── professional_parameters.py    # 专业参数
├── model_library_manager.py      # 模型库管理
├── templates/
│   ├── index_optimized.html      # 优化版前端 ⭐
│   ├── index_learning.html       # 学习版前端
│   └── index.html                # 基础前端
├── static/
│   ├── style.css                 # 样式文件
│   └── script.js                 # 脚本文件
├── uploads/                      # 上传目录
├── requirements.txt              # 依赖列表
└── README-v3.0.md               # 本文档
```

## 🛠️ 技术栈

- **后端**: Python 3.8+, Flask 3.0
- **机器学习**: PyTorch, scikit-learn
- **文件处理**: openpyxl, PyPDF2, pdfplumber
- **OCR**: pytesseract, EasyOCR
- **前端**: HTML5, CSS3, JavaScript

## 📚 文档

- [快速使用指南](快速使用指南-v3.0.md)
- [完整功能开发报告](完整功能开发完成报告.md)
- [专业参数说明](专业参数说明文档.md)
- [多系统部署指南](多系统复杂部署使用指南.md)

## 🔄 版本历史

### v3.0 (2025-10-25) - 当前版本
- ✅ 优化启动速度（2-3秒）
- ✅ 新增多文件格式支持
- ✅ 新增多系统环境分析
- ✅ 新增复杂部署拓扑
- ✅ 集成 735+ 案例库
- ✅ 完整功能 + 快速启动

### v2.0 (2025-01-20)
- ✅ 参数体系升级（150+参数）
- ✅ 准确率提升至 92.75%
- ✅ 新增自我学习功能
- ✅ 新增模型库管理

### v1.0 (2024-12-15)
- ✅ 基础架构预测
- ✅ 图片OCR识别
- ✅ 手动参数输入

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 📞 联系方式

- 项目地址: [GitHub](https://github.com)
- 问题反馈: [Issues](https://github.com/issues)

---

**Made with ❤️ by TDSQL Team**
