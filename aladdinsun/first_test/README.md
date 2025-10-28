# 🐍 Python 待办事项管理器

一个基于 Flask 框架构建的现代化待办事项管理 Web 应用。

## ✨ 功能特点

- ✅ 添加、完成、删除待办事项
- 🔍 三种筛选模式：全部、进行中、已完成
- 📊 实时统计数据展示
- 💾 数据持久化存储（JSON 文件）
- 🎨 现代化 UI 设计
- 📱 响应式布局，支持移动端

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
python app.py
```

### 3. 访问应用

打开浏览器访问：http://localhost:5000

## 📁 项目结构

```
.
├── app.py              # Flask 应用主文件
├── requirements.txt    # Python 依赖
├── todos.json         # 数据存储文件（自动生成）
├── templates/         # HTML 模板
│   └── index.html
└── static/           # 静态资源
    ├── style.css     # 样式文件
    └── script.js     # 前端 JavaScript
```

## 🔧 技术栈

- **后端**: Flask (Python)
- **前端**: HTML5, CSS3, JavaScript (ES6+)
- **数据存储**: JSON 文件
- **API**: RESTful API

## 📝 API 接口

- `GET /api/todos` - 获取所有待办事项
- `POST /api/todos` - 添加新待办事项
- `PUT /api/todos/<id>` - 更新待办事项
- `DELETE /api/todos/<id>` - 删除待办事项
- `GET /api/stats` - 获取统计信息

## 💡 使用说明

1. 在输入框中输入待办事项内容
2. 点击"添加"按钮或按回车键添加
3. 点击复选框标记任务完成状态
4. 使用筛选按钮查看不同状态的任务
5. 点击"删除"按钮移除任务

所有数据会自动保存到 `todos.json` 文件中。

## 🎯 特色

- 使用 Flask 构建的轻量级 Web 应用
- RESTful API 设计
- 前后端分离架构
- 优雅的动画效果
- 完整的错误处理

## 📄 许可

MIT License
