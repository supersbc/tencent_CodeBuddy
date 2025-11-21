# 📁 文件上传功能使用指南

## ✅ 功能状态

文件上传和解析功能已正常工作！

## 📊 测试结果

### ✅ JSON文件上传 - 完美支持
```json
上传成功
解析参数: {
  "qps": 8000,
  "tps": 2400,
  "data_volume": 1000,
  "concurrent_users": 2000,
  "ha_level": "high",
  "industry": "ecommerce"
}
```

### ✅ 预测功能 - 正常工作
```
预测成功
服务器数量: 24台
初始投资: ¥4,716,500
```

### ⚠️ 图片OCR - 需要安装依赖
图片文件可以上传，但OCR识别需要安装tesseract：
```bash
# macOS
brew install tesseract tesseract-lang

# 安装Python库
pip install pytesseract
```

## 📝 支持的文件格式

### 1. JSON文件 ✅ (推荐)

**示例文件**: `test_upload.json`

```json
{
  "qps": 8000,
  "tps": 2400,
  "data_volume": 1000,
  "concurrent_users": 2000,
  "ha_level": "high",
  "industry": "ecommerce",
  "growth_rate": 30,
  "backup_retention": 30
}
```

**支持的字段别名**:
- `qps` / `QPS` / `queries_per_second` / `每秒查询数`
- `tps` / `TPS` / `transactions_per_second` / `每秒事务数`
- `data_volume` / `data_size` / `storage` / `数据量`
- `concurrent_users` / `users` / `connections` / `并发用户数`
- `ha_level` / `high_availability` / `ha` / `高可用级别`
- `industry` / `business_type` / `行业`

### 2. Excel文件 ✅

**格式要求**:
| 参数名称 | 参数值 |
|---------|--------|
| QPS | 5000 |
| 数据量(GB) | 500 |
| 并发用户数 | 1000 |
| 高可用级别 | high |
| 行业 | 金融 |

**需要安装**: `pip install openpyxl`

### 3. 图片文件 ⚠️

**支持格式**: PNG, JPG, JPEG, GIF, BMP

**功能**:
- 基本信息识别 ✅
- OCR文字识别 ⚠️ (需要安装tesseract)

**安装OCR支持**:
```bash
# macOS
brew install tesseract tesseract-lang

# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim

# 安装Python库
pip install pytesseract Pillow
```

### 4. PDF文件 ⚠️

**功能**: 提取文本并解析参数

**需要安装**: `pip install PyPDF2`

## 🎯 使用方法

### 方法1: 网页拖拽上传

1. 访问 http://127.0.0.1:5173
2. 将文件拖拽到上传区域
3. 系统自动解析并填充参数
4. 点击"开始预测"生成报告

### 方法2: API调用

```python
import requests

# 上传文件
with open('test_upload.json', 'rb') as f:
    files = {'file': ('test_upload.json', f, 'application/json')}
    response = requests.post('http://127.0.0.1:5173/api/upload', files=files)

result = response.json()
print(f"解析参数: {result['params']}")

# 使用解析的参数进行预测
response = requests.post(
    'http://127.0.0.1:5173/api/predict',
    json=result['params']
)

prediction = response.json()
print(f"预测结果: {prediction['data']}")
```

## 📋 参数说明

| 参数 | 类型 | 说明 | 示例 |
|-----|------|------|------|
| qps | 整数 | 每秒查询数 | 5000 |
| tps | 整数 | 每秒事务数 | 1500 |
| data_volume | 整数 | 数据量(GB) | 500 |
| concurrent_users | 整数 | 并发用户数 | 1000 |
| ha_level | 字符串 | 高可用级别: low/medium/high | high |
| industry | 字符串 | 行业类型 | 金融/电商/游戏 |
| growth_rate | 整数 | 年增长率(%) | 30 |
| backup_retention | 整数 | 备份保留天数 | 30 |

## 🔍 故障排除

### 问题1: JSON文件上传失败
**解决**: 检查JSON格式是否正确，使用在线JSON验证工具

### 问题2: Excel文件无法解析
**解决**: 
```bash
pip install openpyxl
```

### 问题3: 图片OCR不工作
**解决**:
```bash
# macOS
brew install tesseract tesseract-lang
pip install pytesseract Pillow

# 验证安装
tesseract --version
```

### 问题4: PDF文件无法解析
**解决**:
```bash
pip install PyPDF2
```

## 🎉 快速测试

使用提供的测试文件:
```bash
cd /Users/aladdin/Documents/gitdata/tencent_CodeBuddy/aladdinsun/AIdatabase
python3 test_file_parse.py
```

## 📞 技术支持

如有问题，请查看:
- 服务器日志: `tail -f server.log`
- 上传目录: `ls -la uploads/`
- API健康检查: `curl http://127.0.0.1:5173/api/health`

---

**文件上传功能已就绪，开始使用吧！** 🚀
