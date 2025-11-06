# 📸 图片上传与识别功能指南

## ✅ 已修复的问题

### 1. 文件类型支持扩展
**之前**: 只支持 `.xlsx`, `.xls`, `.json`  
**现在**: 支持 `.xlsx`, `.xls`, `.json`, `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.pdf`

### 2. 图片识别功能
新增了完整的图片处理能力，支持两种识别模式：

#### 模式 A: OCR 文字识别（推荐）
- **需要安装**: `pip install pytesseract pillow`
- **需要系统工具**: Tesseract OCR
  - macOS: `brew install tesseract tesseract-lang`
  - Ubuntu: `sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim`
  - Windows: 下载安装 [Tesseract-OCR](https://github.com/UB-Mannheim/tesseract/wiki)

**功能**:
- 从图片中提取文字内容
- 智能识别关键参数（QPS、并发数、行业等）
- 支持中英文混合识别
- 显示完整的 OCR 识别文本

#### 模式 B: 基础图像分析（无需额外安装）
- **需要安装**: `pip install pillow`（通常已安装）

**功能**:
- 读取图片基本信息（尺寸、格式）
- 基于图片属性进行智能推断
- 提供默认参数配置

### 3. PDF 文件支持
- **需要安装**: `pip install PyPDF2`

**功能**:
- 提取 PDF 文本内容（前5页）
- 从文本中识别关键参数
- 支持架构文档、需求文档等

## 🎯 使用方法

### 1. 上传图片
1. 点击"选择文件"按钮或拖拽文件到上传区域
2. 选择图片文件（支持 PNG、JPG、JPEG、GIF、BMP）
3. 系统自动识别并提取参数

### 2. 查看识别结果
识别结果包含以下信息：
- **文件信息**: 文件名、识别方式
- **图片信息**: 尺寸、格式（如 1920x1080 PNG）
- **OCR 文本**: 可展开查看完整识别文本
- **提取参数**: 自动提取的业务参数
- **架构推荐**: 基于参数的架构建议

### 3. 示例识别流程

```
上传图片: architecture_diagram.png (1920x1080)
    ↓
OCR 识别文本:
    "电商系统架构设计
     预计 QPS: 10000
     并发用户: 5000
     数据量: 500GB"
    ↓
提取参数:
    - industry: 电商
    - qps: 10000
    - concurrent_users: 5000
    - data_volume: 500
    ↓
架构推荐:
    - 类型: 分布式集群
    - 节点数: 6
    - 部署模式: 主从复制 + 读写分离
```

## 📦 安装依赖

### 基础功能（必需）
```bash
pip install flask pillow openpyxl
```

### OCR 功能（推荐）
```bash
# 安装 Python 库
pip install pytesseract

# 安装 Tesseract OCR 引擎
# macOS
brew install tesseract tesseract-lang

# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim

# Windows
# 下载并安装: https://github.com/UB-Mannheim/tesseract/wiki
```

### PDF 支持（可选）
```bash
pip install PyPDF2
```

## 🔍 识别能力说明

### 支持的参数识别
系统可以从图片/PDF中自动识别以下参数：

1. **行业类型**
   - 关键词: 金融、电商、游戏、物联网、社交等
   - 默认值: 金融

2. **QPS（每秒查询数）**
   - 从数字中提取
   - 默认值: 5000

3. **并发用户数**
   - 从数字中提取
   - 默认值: 1000

4. **数据量**
   - 从数字中提取
   - 默认值: 100GB

5. **可用性要求**
   - 默认值: 99.99%

### 智能推断逻辑
- 优先使用 OCR 识别的文本内容
- 通过关键词匹配识别行业类型
- 通过正则表达式提取数字参数
- 如果无法识别，使用合理的默认值

## 🎨 前端展示优化

### 新增显示内容
1. **文件信息卡片**
   - 蓝色边框高亮显示
   - 显示文件名和识别方式

2. **图片信息**
   - 显示图片尺寸和格式
   - 便于确认上传正确

3. **OCR 文本折叠面板**
   - 默认折叠，点击展开
   - 显示完整识别文本
   - 最大高度 200px，可滚动

4. **提取参数列表**
   - 清晰展示所有提取的参数
   - 显示智能推断说明

## 🐛 故障排除

### 问题 1: 图片上传后无响应
**解决方案**:
- 检查文件格式是否支持
- 查看浏览器控制台错误信息
- 确认服务器日志

### 问题 2: OCR 识别失败
**可能原因**:
- 未安装 pytesseract 或 Tesseract OCR
- Tesseract 未添加到系统 PATH

**解决方案**:
```bash
# 检查 Tesseract 是否安装
tesseract --version

# 如果未找到，重新安装
brew install tesseract  # macOS
```

### 问题 3: 识别结果不准确
**优化建议**:
- 使用清晰的图片（分辨率 > 800x600）
- 确保文字清晰可读
- 避免复杂背景
- 使用标准字体

### 问题 4: PDF 无法处理
**解决方案**:
```bash
# 安装 PyPDF2
pip install PyPDF2

# 如果仍然失败，尝试升级
pip install --upgrade PyPDF2
```

## 📊 测试示例

### 测试图片 1: 架构图
创建一个包含以下文字的图片：
```
TDSQL 架构设计
行业: 电商
QPS: 15000
并发用户: 8000
数据量: 1TB
```

**预期结果**:
- industry: 电商
- qps: 15000
- concurrent_users: 8000
- data_volume: 1000

### 测试图片 2: 需求文档截图
上传包含业务需求的文档截图

**预期结果**:
- 自动提取关键数字
- 识别行业关键词
- 生成架构推荐

## 🚀 性能优化

### 图片处理优化
- 自动压缩大图片（未来版本）
- 缓存识别结果（未来版本）
- 异步处理提升响应速度

### OCR 优化
- 预处理图片提高识别率
- 支持多语言识别
- 自定义识别区域

## 📝 更新日志

### v3.1 (2025-10-25)
- ✅ 新增图片上传支持（PNG、JPG、JPEG、GIF、BMP）
- ✅ 新增 OCR 文字识别功能
- ✅ 新增 PDF 文件支持
- ✅ 优化前端显示，展示识别详情
- ✅ 智能参数提取和推断
- ✅ 完善错误处理和降级方案

### v3.0 (之前)
- Excel 文件上传
- JSON 文件上传
- 手动参数输入
- 模型库管理
- 自我学习功能

## 🔗 相关文档
- [README_FINAL.md](./README_FINAL.md) - 完整系统文档
- [USAGE_GUIDE.md](./USAGE_GUIDE.md) - 快速上手指南
- [FIXED_SUMMARY.md](./FIXED_SUMMARY.md) - 问题修复总结

## 💡 提示
- 首次使用建议先测试 Excel/JSON 上传，确认基础功能正常
- OCR 功能需要额外安装，但可以大幅提升用户体验
- 如果 OCR 不可用，系统会自动降级到基础图像分析
- 建议使用高质量、文字清晰的图片以获得最佳识别效果
