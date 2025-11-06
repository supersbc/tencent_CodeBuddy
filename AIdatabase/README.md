# 🚀 TDSQL 部署资源预测系统 v4.2

> 智能分析业务需求，自动生成详细的TDSQL部署方案  
> 整合模型库管理和自主训练功能

[![Version](https://img.shields.io/badge/version-4.2-blue.svg)](https://github.com)
[![Python](https://img.shields.io/badge/python-3.7+-green.svg)](https://www.python.org)
[![Flask](https://img.shields.io/badge/flask-2.0+-red.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

---

## 📋 目录

- [功能特性](#-功能特性)
- [快速开始](#-快速开始)
- [功能模块](#-功能模块)
- [API接口](#-api接口)
- [使用示例](#-使用示例)
- [测试验证](#-测试验证)
- [文档](#-文档)

---

## ✨ 功能特性

### 🔮 部署资源预测
- 智能参数分析和系统规模判断
- 详细的架构设计（分片、副本、高可用）
- 完整的设备清单（服务器、网络、存储）
- 精确的成本分析（初始投资、运营成本、TCO）
- 专业的网络拓扑设计
- 可视化架构图数据
- 专业部署建议

### 📁 文件上传
- 支持JSON/Excel/图片/PDF多种格式
- 自动参数提取和表单填充
- 拖拽上传，操作便捷
- 文件信息显示和清除功能

### 📚 模型库管理
- 9个预置行业模型库
- 模型库浏览、下载、激活
- 自定义模型库创建
- 覆盖金融、电商、游戏等多个行业

### 🎓 自主训练
- 实际案例提交
- 模型训练和优化
- 训练历史记录
- 模型评估和反馈

---

## 🚀 快速开始

### 1. 环境要求

- Python 3.7+
- Flask 2.0+

### 2. 安装依赖

```bash
# 基础依赖（必需）
pip install flask werkzeug

# 可选依赖
pip install openpyxl          # Excel支持
pip install pytesseract Pillow  # 图片OCR
pip install PyPDF2            # PDF支持
pip install torch numpy       # 机器学习
```

### 3. 启动服务

**方法1: 使用启动脚本（推荐）**
```bash
./start_complete.sh
```

**方法2: 手动启动**
```bash
python3 app_simple.py
```

### 4. 访问系统

打开浏览器访问: **http://127.0.0.1:5173/nav**

---

## 🎯 功能模块

### 1. 导航页面
**访问**: http://127.0.0.1:5173/nav

所有功能模块的入口，清晰的卡片式导航。

### 2. 部署资源预测
**访问**: http://127.0.0.1:5173

**输入方式**:
- 手动输入业务参数
- 上传JSON/Excel文件

**输出内容**:
- 📊 系统概览（规模、QPS、成本）
- 🏗️ 架构设计（分片、副本配置）
- 💻 设备清单（24台服务器详细配置）
- 🌐 网络拓扑（8层架构 + VLAN）
- 💰 成本分析（初始投资¥471万）
- 📈 架构图数据
- 💡 部署建议

### 3. 模型库管理
**访问**: http://127.0.0.1:5173/model_library

**可用模型库**:
- 腾讯云官方模型库（150案例，92-95%准确率）
- 金融行业社区模型库（80案例，93-96%准确率）
- 电商行业社区模型库（60案例，89-93%准确率）
- 游戏行业社区模型库（45案例，87-91%准确率）
- GitHub开源模型库（120案例）
- HuggingFace模型库（100案例）
- Kaggle竞赛模型库（85案例）
- 阿里云模型库（95案例）
- 自定义模型库

### 4. 学习系统
**访问**: http://127.0.0.1:5173/learning

**功能**:
- 提交实际部署案例
- 训练和优化模型
- 查看训练历史
- 评估模型性能

---

## 📡 API接口

### 基础接口

```bash
# 健康检查
GET /api/health

# 部署预测
POST /api/predict
Content-Type: application/json
{
  "qps": 5000,
  "data_volume": 500,
  "ha_level": "high",
  "industry": "金融"
}

# 文件上传
POST /api/upload
Content-Type: multipart/form-data

# 清除文件
POST /api/clear_uploads
```

### 模型库接口

```bash
# 获取模型库列表
GET /api/model_libraries

# 获取模型库详情
GET /api/model_libraries/{library_id}

# 下载模型库
POST /api/model_libraries/{library_id}/download

# 激活模型库
POST /api/model_libraries/{library_id}/activate

# 创建自定义模型库
POST /api/custom_library
```

### 训练系统接口

```bash
# 获取训练案例
GET /api/training/cases

# 添加训练案例
POST /api/training/cases

# 训练模型
POST /api/training/train

# 获取训练历史
GET /api/training/history

# 评估模型
POST /api/training/evaluate
```

---

## 💡 使用示例

### 示例1: 金融行业部署预测

```bash
curl -X POST http://127.0.0.1:5173/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "qps": 5000,
    "data_volume": 500,
    "ha_level": "high",
    "industry": "金融"
  }'
```

**响应**:
```json
{
  "success": true,
  "data": {
    "input_summary": {
      "scale": "large",
      "qps": 5000,
      "current_data_gb": 500
    },
    "equipment_list": {
      "servers": [24台服务器详细配置]
    },
    "cost_breakdown": {
      "summary": {
        "initial_investment": 4716500,
        "three_year_tco": 6044180
      }
    }
  }
}
```

### 示例2: 上传JSON文件

```bash
curl -X POST http://127.0.0.1:5173/api/upload \
  -F "file=@test_upload.json"
```

### 示例3: 获取模型库列表

```bash
curl http://127.0.0.1:5173/api/model_libraries
```

---

## 🧪 测试验证

### 运行完整测试

```bash
python3 test_all_features.py
```

**测试结果**:
```
✅ 健康检查 - 通过
✅ 部署资源预测 - 通过（24台服务器，¥471万）
✅ 模型库管理 - 通过（9个模型库）
✅ 训练系统 - 通过
✅ 文件上传 - 通过（6个参数）
```

### 其他测试脚本

```bash
# 文件解析测试
python3 test_file_parse.py

# 简单连接测试
python3 test_simple.py

# 完整功能测试
python3 test_complete.py
```

---

## 📚 文档

| 文档 | 说明 |
|-----|------|
| [COMPLETE_FEATURES_v4.2.md](COMPLETE_FEATURES_v4.2.md) | 完整功能说明 |
| [FINAL_SUMMARY_v4.2.md](FINAL_SUMMARY_v4.2.md) | 最终交付总结 |
| [UPDATE_NOTES.md](UPDATE_NOTES.md) | v4.1更新说明 |
| [FILE_UPLOAD_GUIDE.md](FILE_UPLOAD_GUIDE.md) | 文件上传指南 |
| [模型库使用指南.md](模型库使用指南.md) | 模型库详细说明 |
| [LEARNING_GUIDE.md](LEARNING_GUIDE.md) | 学习系统指南 |

---

## 🔧 故障排除

### 问题1: 服务无法启动

**解决**:
```bash
# 检查端口占用
lsof -i:5173

# 停止旧服务
lsof -ti:5173 | xargs kill -9

# 重新启动
python3 app_simple.py
```

### 问题2: 文件上传失败

**解决**:
```bash
# 检查uploads目录权限
ls -la uploads/

# 创建目录
mkdir -p uploads
chmod 755 uploads
```

### 问题3: Excel文件无法解析

**解决**:
```bash
pip install openpyxl
```

### 问题4: 图片OCR不工作

**解决**:
```bash
# macOS
brew install tesseract tesseract-lang
pip install pytesseract Pillow

# 验证安装
tesseract --version
```

---

## 📊 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    前端界面                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │ 部署预测 │ │ 模型库   │ │ 学习系统 │ │ 文件上传 │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    Flask API                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │ 预测接口 │ │ 模型接口 │ │ 训练接口 │ │ 上传接口 │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    核心引擎                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
│  │ 部署预测引擎 │ │ 模型库管理器 │ │ 训练系统     │   │
│  └──────────────┘ └──────────────┘ └──────────────┘   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    数据层                                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │ 上传文件 │ │ 模型库   │ │ 训练数据 │ │ 配置文件 │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 🎊 总结

TDSQL 部署资源预测系统 v4.2 提供了完整的部署规划解决方案：

- ✅ **智能预测** - 自动分析生成详细部署方案
- ✅ **模型库** - 9个行业模型库，随时下载使用
- ✅ **自主学习** - 从实际案例中持续优化
- ✅ **易于使用** - 多种输入方式，清晰的导航

**立即开始使用**: http://127.0.0.1:5173/nav

---

## 📞 支持

如有问题，请查看:
- 📚 [完整功能说明](COMPLETE_FEATURES_v4.2.md)
- 📝 [最终交付总结](FINAL_SUMMARY_v4.2.md)
- 🔍 [故障排除](#-故障排除)

---

**版本**: v4.2 (完整版)  
**更新时间**: 2025-10-26  
**状态**: ✅ 已完成并测试通过

**开始使用吧！** 🚀
