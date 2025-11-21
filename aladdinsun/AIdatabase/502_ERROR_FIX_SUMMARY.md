# Nginx 502 错误修复总结

## 🐛 问题现象

用户反馈：
1. "预测失败，请重试"
2. Nginx返回 **502 Bad Gateway** 错误

## 🔍 问题诊断

### 1. 检查进程状态
```bash
ps aux | grep -E "app_simple|nginx"
```

**发现**：
- ✅ Nginx正常运行（PID 1027325）
- ❌ Flask应用进程消失（崩溃）

### 2. 查看错误日志
```bash
tail -300 app.log
```

**关键错误**：
```
OpenBLAS blas_thread_init: pthread_create failed for thread 63 of 64: Resource temporarily unavailable
OpenBLAS blas_thread_init: RLIMIT_NPROC -1 current -1 max
```

### 3. 根本原因

**OpenBLAS线程资源耗尽**：
- OpenBLAS默认会创建大量线程（64个）
- 系统资源限制导致线程创建失败
- Flask进程崩溃，Nginx无法连接到后端 → 502错误

## ✅ 修复方案

### 方案1: 环境变量限制（临时）

创建启动脚本 `start_fixed.sh`:
```bash
#!/bin/bash
export OPENBLAS_NUM_THREADS=4
export OMP_NUM_THREADS=4
export MKL_NUM_THREADS=4

nohup python3 app_simple.py > app.log 2>&1 &
```

### 方案2: 代码内设置（永久）

修改 `app_simple.py`，在导入任何科学计算库之前设置：
```python
# 修复OpenBLAS线程资源问题 - 必须在导入任何科学计算库之前设置
import os
os.environ['OPENBLAS_NUM_THREADS'] = '4'
os.environ['OMP_NUM_THREADS'] = '4'
os.environ['MKL_NUM_THREADS'] = '4'

from flask import Flask, render_template, request, jsonify
# ... 其他导入
```

**重要**：必须在 `from flask import ...` 之前设置，因为Flask可能会间接导入numpy等库。

## 📝 修复步骤

### 1. 修改代码
```bash
cd /data/workspace/tencent_CodeBuddy/aladdinsun/AIdatabase
# 编辑 app_simple.py，在文件开头添加环境变量设置
```

### 2. 重启服务
```bash
# 方法1: 使用修复脚本
./start_fixed.sh

# 方法2: 手动重启
pkill -f app_simple.py
sleep 2
nohup python3 app_simple.py > app.log 2>&1 &
```

### 3. 验证修复
```bash
# 检查进程
ps aux | grep app_simple

# 检查日志（不应有OpenBLAS错误）
tail -50 app.log | grep -E "OpenBLAS|pthread|Resource"

# 测试API
curl http://localhost:18080/api/health
python3 test_xinchuan_fix.py
```

## ✅ 修复结果

### 修复前
```
OpenBLAS blas_thread_init: pthread_create failed for thread 63 of 64
→ Flask崩溃
→ Nginx 502 Bad Gateway
```

### 修复后
```
✅ Flask正常运行 (PID: 1054512)
✅ Nginx正常运行 (PID: 1027325)
✅ 健康检查通过
✅ 预测功能正常
```

## 🧪 测试验证

### 1. 健康检查
```bash
curl http://localhost:18080/api/health
```
**响应**：
```json
{
  "status": "ok",
  "version": "4.0",
  "message": "TDSQL部署资源预测系统运行正常"
}
```

### 2. 信创预测测试
```bash
python3 test_xinchuan_fix.py
```
**结果**：
```
✅ 测试通过！循环引用问题已修复

🇨🇳 信创模式: standard
  - 服务器品牌: 浪潮, 华为, 联想
  - 网络设备: 华为, H3C
  - CPU芯片: 鲲鹏920, 海光EPYC, 飞腾
  - 成本优势: 相比国外品牌节约 8-15%

💰 信创方案成本: ¥316,000 (31.6万元)
```

### 3. 日志检查
```bash
tail -50 app.log | grep -E "OpenBLAS|Error|Exception"
```
**结果**: 无错误 ✅

## 📊 问题影响范围

### 受影响功能
- ❌ 部署预测功能（POST /api/predict）
- ❌ Excel解析功能（POST /api/parse_excel）
- ❌ 所有需要加载numpy/pandas的功能

### 未受影响
- ✅ 静态页面访问
- ✅ Nginx服务
- ✅ 文件下载功能

## 🔧 技术细节

### OpenBLAS是什么？
OpenBLAS（Open Basic Linear Algebra Subprograms）是一个优化的线性代数库，被numpy等科学计算库依赖。

### 为什么会创建64个线程？
默认情况下，OpenBLAS会尝试使用所有CPU核心，在64核服务器上会创建64个线程。

### 为什么设置为4？
- 平衡性能和资源消耗
- 4个线程足以处理预测计算
- 避免系统资源耗尽

### 其他可选值
```bash
# 保守（节省资源）
export OPENBLAS_NUM_THREADS=1

# 中等（推荐）
export OPENBLAS_NUM_THREADS=4

# 激进（高性能，但可能资源不足）
export OPENBLAS_NUM_THREADS=8
```

## 🚀 预防措施

### 1. 启动脚本
始终使用 `start_fixed.sh` 启动服务，确保环境变量生效。

### 2. 系统监控
```bash
# 监控Flask进程
watch -n 5 'ps aux | grep app_simple'

# 监控日志
tail -f app.log | grep -E "Error|Exception|OpenBLAS"
```

### 3. 自动重启（可选）
配置systemd或supervisor自动重启崩溃的Flask进程。

## 📁 相关文件

| 文件 | 说明 |
|------|------|
| `app_simple.py` | 主应用（已添加环境变量设置） |
| `start_fixed.sh` | 修复后的启动脚本 |
| `test_xinchuan_fix.py` | 测试脚本 |
| `app.log` | 应用日志 |

## 🎯 总结

### 问题
- Nginx 502错误
- Flask进程崩溃
- OpenBLAS线程资源耗尽

### 解决方案
- 在代码开头设置 `OPENBLAS_NUM_THREADS=4`
- 限制OpenBLAS线程数为4

### 效果
- ✅ 502错误消失
- ✅ Flask稳定运行
- ✅ 所有功能正常
- ✅ 日志无错误

---

**修复时间**: 2025-11-11  
**修复人员**: AI Assistant  
**状态**: ✅ 已完全修复
