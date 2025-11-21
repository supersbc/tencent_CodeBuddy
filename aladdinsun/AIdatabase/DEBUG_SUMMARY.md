# AIdatabase 无法访问问题诊断总结

## 🚨 问题描述

**访问地址:** https://aladdinsun.devcloud.woa.com  
**症状:** 无法访问  
**可能原因:** Nginx配置问题 或 Flask应用未运行

---

## 🔍 问题分析

根据项目结构分析:

### 1. 服务架构

```
用户浏览器
    ↓
https://aladdinsun.devcloud.woa.com (域名)
    ↓
Nginx (端口80/443) ← 反向代理
    ↓
Flask App (端口18080 或 5000) ← Python应用
    ↓
app_simple.py
```

### 2. 启动脚本分析

项目中有 `start_with_nginx.sh`:
- Flask监听端口: **18080**
- Nginx监听端口: **80**
- 反向代理: Nginx → Flask(18080)

### 3. 可能的问题

#### ❌ 问题1: Flask应用未运行
```bash
# 检查命令
ps aux | grep app_simple.py
```

如果无进程 → Flask未启动

#### ❌ 问题2: Nginx未运行
```bash
# 检查命令
ps aux | grep nginx
```

如果无进程 → Nginx未启动

#### ❌ 问题3: 端口未监听
```bash
# 检查命令
ss -tlnp | grep -E ':80|:18080|:5000'
```

如果无输出 → 端口未监听

#### ❌ 问题4: Nginx配置错误
```bash
# 检查命令
nginx -t
```

如果报错 → 配置文件有问题

#### ❌ 问题5: Python依赖缺失
```bash
# 检查命令
python3 -c "import flask"
```

如果报错 → Flask未安装

---

## 🔧 完整修复步骤

### 步骤1: 安装Python依赖

```bash
cd /data/workspace/tencent_CodeBuddy/aladdinsun/AIdatabase

# 方式A: 安装全部依赖(推荐)
pip3 install -r requirements.txt -i https://mirrors.tencent.com/pypi/simple/

# 方式B: 只安装核心依赖(快速)
pip3 install Flask==3.0.0 pandas openpyxl numpy scikit-learn \
    -i https://mirrors.tencent.com/pypi/simple/
```

### 步骤2: 停止旧进程

```bash
# 停止Flask
pkill -f app_simple.py

# 停止Nginx
pkill nginx
# 或
sudo systemctl stop nginx

# 释放端口(如果被占用)
fuser -k 18080/tcp
fuser -k 80/tcp
```

### 步骤3: 启动Flask应用

#### 方式A: 后台启动

```bash
cd /data/workspace/tencent_CodeBuddy/aladdinsun/AIdatabase
nohup python3 app_simple.py > app.log 2>&1 &

# 等待5秒
sleep 5

# 检查是否启动成功
ps aux | grep app_simple
ss -tlnp | grep -E ':18080|:5000'

# 查看日志
tail -f app.log
```

#### 方式B: 前台启动(推荐用于调试)

```bash
cd /data/workspace/tencent_CodeBuddy/aladdinsun/AIdatabase
python3 app_simple.py

# 会实时显示日志,Ctrl+C停止
```

#### 方式C: 使用启动脚本

```bash
cd /data/workspace/tencent_CodeBuddy/aladdinsun/AIdatabase
bash start_with_nginx.sh
```

### 步骤4: 验证Flask服务

```bash
# 本地测试
curl http://localhost:18080
# 或
curl http://localhost:5000

# 如果返回HTML内容 → Flask正常
# 如果连接失败 → 查看app.log
```

### 步骤5: 配置Nginx

#### 检查Nginx配置

```bash
# 查找配置文件
ls -la /etc/nginx/conf.d/
ls -la /etc/nginx/sites-enabled/

# 查看主配置
cat /etc/nginx/nginx.conf

# 搜索aladdinsun相关配置
grep -r "aladdinsun" /etc/nginx/
```

#### 创建/更新配置文件

创建 `/etc/nginx/conf.d/aidatabase.conf`:

```nginx
server {
    listen 80;
    server_name aladdinsun.devcloud.woa.com;
    
    access_log /var/log/nginx/aidatabase_access.log;
    error_log /var/log/nginx/aidatabase_error.log;
    
    location / {
        proxy_pass http://127.0.0.1:18080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    location /static {
        alias /data/workspace/tencent_CodeBuddy/aladdinsun/AIdatabase/static;
        expires 30d;
    }
}

# HTTPS配置(如果需要)
server {
    listen 443 ssl;
    server_name aladdinsun.devcloud.woa.com;
    
    # SSL证书配置
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    access_log /var/log/nginx/aidatabase_ssl_access.log;
    error_log /var/log/nginx/aidatabase_ssl_error.log;
    
    location / {
        proxy_pass http://127.0.0.1:18080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}
```

### 步骤6: 启动Nginx

```bash
# 测试配置
sudo nginx -t

# 如果配置正确,启动Nginx
sudo nginx

# 或重启Nginx
sudo nginx -s reload

# 检查Nginx状态
ps aux | grep nginx
ss -tlnp | grep :80
```

### 步骤7: 验证访问

```bash
# 本地测试Nginx代理
curl http://localhost

# 测试域名(需要在服务器上)
curl http://aladdinsun.devcloud.woa.com

# 从浏览器访问
# http://aladdinsun.devcloud.woa.com
# https://aladdinsun.devcloud.woa.com
```

---

## 🎯 快速修复命令

```bash
# 一键修复脚本
cd /data/workspace/tencent_CodeBuddy/aladdinsun/AIdatabase
bash quick_fix.sh

# 如果脚本不存在或失败,手动执行:
# 1. 停止服务
pkill -f app_simple.py; pkill nginx; sleep 2

# 2. 启动Flask
cd /data/workspace/tencent_CodeBuddy/aladdinsun/AIdatabase
nohup python3 app_simple.py > app.log 2>&1 &

# 3. 等待并检查
sleep 5
ps aux | grep app_simple

# 4. 启动Nginx
sudo nginx

# 5. 检查端口
ss -tlnp | grep -E ':80|:18080'

# 6. 测试访问
curl http://localhost:18080
curl http://localhost
```

---

## 📋 故障排查清单

### ✅ 检查项1: Python环境

- [ ] Python3已安装: `python3 --version`
- [ ] Flask已安装: `python3 -c "import flask"`
- [ ] 依赖库已安装: `pip3 list | grep -iE 'flask|pandas|numpy'`

### ✅ 检查项2: Flask应用

- [ ] 进程运行中: `ps aux | grep app_simple`
- [ ] 端口监听: `ss -tlnp | grep -E ':18080|:5000'`
- [ ] HTTP响应正常: `curl http://localhost:18080`
- [ ] 日志无报错: `tail app.log`

### ✅ 检查项3: Nginx服务

- [ ] Nginx已安装: `which nginx`
- [ ] 配置文件正确: `nginx -t`
- [ ] Nginx运行中: `ps aux | grep nginx`
- [ ] 80端口监听: `ss -tlnp | grep :80`
- [ ] 反向代理正常: `curl http://localhost`

### ✅ 检查项4: 网络访问

- [ ] 防火墙允许80/443: `iptables -L | grep -E '80|443'`
- [ ] DNS解析正常: `nslookup aladdinsun.devcloud.woa.com`
- [ ] 域名可访问: 浏览器访问

---

## 🐛 常见错误及解决

### 错误1: ModuleNotFoundError: No module named 'flask'

**原因:** Flask未安装  
**解决:**
```bash
pip3 install Flask==3.0.0 -i https://mirrors.tencent.com/pypi/simple/
```

### 错误2: Address already in use

**原因:** 端口被占用  
**解决:**
```bash
# 查找占用进程
lsof -i :18080
# 或
ss -tlnp | grep :18080

# 杀死进程
kill -9 <PID>
# 或强制释放
fuser -k 18080/tcp
```

### 错误3: nginx: [emerg] bind() to 0.0.0.0:80 failed

**原因:** 80端口被占用或权限不足  
**解决:**
```bash
# 检查80端口
ss -tlnp | grep :80

# 使用sudo启动
sudo nginx

# 或改用其他端口(如8080)
```

### 错误4: 502 Bad Gateway

**原因:** Nginx无法连接到Flask后端  
**解决:**
```bash
# 检查Flask是否运行
ps aux | grep app_simple

# 检查Flask端口
ss -tlnp | grep 18080

# 检查Nginx配置中的proxy_pass
cat /etc/nginx/conf.d/aidatabase.conf | grep proxy_pass

# 应该是: proxy_pass http://127.0.0.1:18080;
```

### 错误5: 404 Not Found

**原因:** Nginx配置的路径不对  
**解决:**
检查 `location /` 配置,确保 `proxy_pass` 正确

---

## 📞 仍然无法解决?

### 收集诊断信息

```bash
cd /data/workspace/tencent_CodeBuddy/aladdinsun/AIdatabase

# 创建诊断报告
cat > diagnosis.txt << 'EOF'
========== Python环境 ==========
$(python3 --version 2>&1)
$(python3 -c "import flask; print('Flask:', flask.__version__)" 2>&1)

========== 进程状态 ==========
$(ps aux | grep -E 'app_simple|nginx' | grep -v grep)

========== 端口监听 ==========
$(ss -tlnp 2>&1 | grep -E ':80|:18080|:5000')

========== Flask日志 ==========
$(tail -50 app.log 2>&1)

========== Nginx配置测试 ==========
$(nginx -t 2>&1)

========== Nginx错误日志 ==========
$(tail -30 /var/log/nginx/error.log 2>&1)

========== 网络连接测试 ==========
$(curl -I http://localhost:18080 2>&1)
$(curl -I http://localhost 2>&1)
EOF

cat diagnosis.txt
```

---

## 🎓 最佳实践建议

1. **使用systemd管理服务** (推荐)

创建 `/etc/systemd/system/aidatabase.service`:

```ini
[Unit]
Description=AIdatabase Flask Application
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/data/workspace/tencent_CodeBuddy/aladdinsun/AIdatabase
ExecStart=/usr/bin/python3 app_simple.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

使用systemd管理:
```bash
sudo systemctl daemon-reload
sudo systemctl start aidatabase
sudo systemctl enable aidatabase
sudo systemctl status aidatabase
```

2. **使用虚拟环境**

```bash
cd /data/workspace/tencent_CodeBuddy/aladdinsun/AIdatabase
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **监控和日志**

```bash
# 实时监控日志
tail -f app.log

# 查看Nginx访问日志
tail -f /var/log/nginx/aidatabase_access.log

# 查看Nginx错误日志
tail -f /var/log/nginx/aidatabase_error.log
```

---

**创建日期:** 2025-11-11  
**适用版本:** AIdatabase v4.2+  
**维护者:** aladdinsun
