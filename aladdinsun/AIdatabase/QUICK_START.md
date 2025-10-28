# 🚀 快速开始 - TDSQL 智能规划系统

## 📍 当前状态
✅ 服务正在运行: http://127.0.0.1:5173  
✅ 所有功能已修复并可用

## 🎯 新增功能（v3.1）

### 📸 图片上传与识别
- ✅ 支持 PNG、JPG、JPEG、GIF、BMP 格式
- ✅ OCR 文字识别（可选）
- ✅ 智能降级到基础图像分析
- ✅ 显示图片元信息（尺寸、格式）

### 📄 PDF 文件支持
- ✅ 提取 PDF 文本内容
- ✅ 智能参数识别
- ✅ 支持多页文档

### 🔍 智能识别
- ✅ 自动提取行业类型
- ✅ 识别 QPS、并发数等参数
- ✅ 从文本中提取关键数字

## 🌐 访问方式

### 1. 主界面
```
http://127.0.0.1:5173
```
完整功能界面，包含所有模块

### 2. 测试页面
```
http://127.0.0.1:5173/test_upload.html
```
简化的文件上传测试页面

## 📝 使用示例

### 方式 1: Web 界面
1. 打开浏览器访问 http://127.0.0.1:5173
2. 选择"文件上传"标签
3. 点击或拖拽文件到上传区域
4. 查看分析结果

### 方式 2: API 调用
```bash
# 上传图片
curl -X POST -F "file=@image.png" http://127.0.0.1:5173/api/analyze

# 上传 JSON
curl -X POST -F "file=@config.json" http://127.0.0.1:5173/api/analyze

# 上传 Excel
curl -X POST -F "file=@data.xlsx" http://127.0.0.1:5173/api/analyze
```

### 方式 3: 测试脚本
```bash
cd /Users/aladdin/Documents/gitdata/tencent_CodeBuddy/aladdinsun/AIdatabase
python3 test_image_upload.py
```

## 📦 支持的文件格式

| 格式 | 扩展名 | 识别方式 |
|------|--------|----------|
| 图片 | .png, .jpg, .jpeg, .gif, .bmp | OCR/图像分析 |
| PDF | .pdf | 文本提取 |
| Excel | .xlsx, .xls | 表格解析 |
| JSON | .json | 直接解析 |

## 🧪 测试文件

系统已自动生成测试文件：
- `test_architecture.png` - 测试图片（800x600）
- `test_config.json` - 测试 JSON 配置

## 🔧 服务管理

### 查看服务状态
```bash
curl http://127.0.0.1:5173/api/health
```

### 查看日志
```bash
tail -f /Users/aladdin/Documents/gitdata/tencent_CodeBuddy/aladdinsun/AIdatabase/server.log
```

### 重启服务
```bash
# 停止服务
kill $(lsof -ti:5173)

# 启动服务
cd /Users/aladdin/Documents/gitdata/tencent_CodeBuddy/aladdinsun/AIdatabase
nohup python3 app_final.py > server.log 2>&1 &
```

## 💡 功能说明

### 1. 文件上传分析
- 自动识别文件类型
- 提取关键参数
- 生成架构推荐

### 2. 手动参数输入
- 简化模式：6个核心参数
- 完整模式：20+ 详细参数
- 实时表单验证

### 3. 模型库
- 8个预置模型库
- 735+ 真实案例
- 一键下载使用

### 4. 自我学习
- 提交训练案例
- 查看训练统计
- 持续优化模型

## 📚 详细文档

- [IMAGE_UPLOAD_GUIDE.md](./IMAGE_UPLOAD_GUIDE.md) - 图片上传详细指南
- [IMAGE_RECOGNITION_FIX_SUMMARY.md](./IMAGE_RECOGNITION_FIX_SUMMARY.md) - 修复总结
- [README_FINAL.md](./README_FINAL.md) - 完整系统文档
- [USAGE_GUIDE.md](./USAGE_GUIDE.md) - 使用指南

## 🎉 快速测试

### 测试 1: 图片上传
```bash
cd /Users/aladdin/Documents/gitdata/tencent_CodeBuddy/aladdinsun/AIdatabase
curl -X POST -F "file=@test_architecture.png" http://127.0.0.1:5173/api/analyze | python3 -m json.tool
```

### 测试 2: JSON 上传
```bash
curl -X POST -F "file=@test_config.json" http://127.0.0.1:5173/api/analyze | python3 -m json.tool
```

### 测试 3: 健康检查
```bash
curl http://127.0.0.1:5173/api/health | python3 -m json.tool
```

## 🐛 常见问题

### Q: 图片上传后显示"OCR未安装"
A: 这是正常的，系统会自动降级到基础图像分析模式。如需 OCR 功能：
```bash
pip install pytesseract
brew install tesseract tesseract-lang  # macOS
```

### Q: PDF 无法处理
A: 需要安装 PyPDF2：
```bash
pip install PyPDF2
```

### Q: 服务无法访问
A: 检查服务是否运行：
```bash
lsof -ti:5173
# 如果没有输出，说明服务未运行，需要启动
```

## 📞 获取帮助

如有问题，请查看：
1. 服务器日志: `server.log`
2. 浏览器控制台
3. API 返回的错误信息

---

**版本**: v3.1  
**更新时间**: 2025-10-25  
**状态**: ✅ 所有功能正常运行
