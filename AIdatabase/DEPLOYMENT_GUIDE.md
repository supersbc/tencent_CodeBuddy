# TDSQL 部署资源预测系统 - DevCloud 部署指南

## 使用 AnyDev 云研发环境部署

### 1. 创建云研发环境
1. 打开 iOA，进入「云研发」
2. 点击「创建环境」
3. 选择合适的配置（建议：2核4G）

### 2. 配置自定义域名
1. 在 AnyDev 中，进入「设置」-「资源管理」-「专属域名」
2. 如果已有 `aladdinsun.devcloud.woa.com` 域名，直接使用
3. 在创建环境时，选择「自定义域名」，选择你的域名

### 3. 部署应用
在云研发环境中执行：

```bash
# 进入项目目录
cd /workspace/AIdatabase

# 安装依赖
pip3 install flask==2.0.3 werkzeug==2.0.3 --user
pip3 install openpyxl pandas numpy --user

# 创建必要目录
mkdir -p uploads model_libraries training_data

# 启动应用（监听 0.0.0.0）
python3 app_simple.py
```

### 4. 配置端口转发
确保应用监听在 `0.0.0.0:5173`，这样才能通过域名访问

### 5. 访问应用
通过 `http://aladdinsun.devcloud.woa.com` 访问你的应用

## 方案二：使用 DevCloud CVM + Nginx

### 1. 申请 DevCloud CVM
访问 http://devcloud.woa.com 申请个人云服务器

### 2. 配置域名解析
1. 访问 UDNS 系统：http://udns.woa.com
2. 申请或修改域名 `aladdinsun.devcloud.woa.com`
3. 将解析内容填写为你的 CVM IP

### 3. 安装 Nginx
```bash
yum install nginx -y
```

### 4. 配置 Nginx
创建配置文件 `/etc/nginx/conf.d/tdsql.conf`：

```nginx
server {
    listen 80;
    server_name aladdinsun.devcloud.woa.com;
    
    location / {
        proxy_pass http://127.0.0.1:5173;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 5. 启动服务
```bash
# 启动 Nginx
systemctl start nginx
systemctl enable nginx

# 启动 Flask 应用
cd /path/to/AIdatabase
nohup python3 app_simple.py > server.log 2>&1 &
```

### 6. 开放端口
确保防火墙开放 80 端口

## 注意事项
- DevCloud 机器默认可访问外网
- 如需 HTTPS，需要申请证书并配置
- 建议使用 supervisor 或 systemd 管理 Flask 进程
