# AIdatabase 服务故障排查指南

## 🚨 问题现象

无法通过 https://aladdinsun.devcloud.woa.com/ 访问AIdatabase服务

---

## 🔍 排查步骤

### 1️⃣ 检查进程状态

```bash
cd /data/workspace/tencent_CodeBuddy/aladdinsun/AIdatabase

# 检查Flask应用进程
ps aux | grep app_simple.py

# 检查Nginx进程  
ps aux | grep nginx

# 检查端口监听
ss -tlnp | grep -E ':80|:5000|:18080'
# 或
netstat -tlnp | grep -E ':80|:5000|:18080'
```

**预期结果:**
- Flask应用监听端口: 18080 或 5000
- Nginx监听端口: 80 或 443

---

### 2️⃣ 检查Python环境

```bash
# 检查Python版本
python3 --version

# 检查Flask是否安装
python3 -c "import flask; print(flask.__version__)"

# 检查其他依赖
pip3 list | grep -iE 'flask|numpy|pandas|openpyxl'
```

**如果Flask未安装:**

```bash
# 使用腾讯镜像源安装
pip3 install Flask==3.0.0 -i https://mirrors.tencent.com/pypi/simple/

# 或安装所有依赖
pip3 install -r requirements.txt -i https://mirrors.tencent.com/pypi/simple/
```

---

### 3️⃣ 检查日志

```bash
cd /data/workspace/tencent_CodeBuddy/aladdinsun/AIdatabase

# 查看Flask日志
tail -f app.log

# 查看Nginx日志
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log
```

**常见错误:**
- `ModuleNotFoundError: No module named 'flask'` → 安装Flask
- `Address already in use` → 端口被占用
- `Permission denied` → 权限问题

---

### 4️⃣ 检查Nginx配置

```bash
# 测试Nginx配置
nginx -t

# 查看Nginx配置文件
cat /etc/nginx/nginx.conf | grep -A 20 "server {"

# 查找aladdinsun相关配置
grep -r "aladdinsun" /etc/nginx/
```

**需要的Nginx配置示例:**

```nginx
server {
    listen 80;
    server_name aladdinsun.devcloud.woa.com;
    
    location / {
        proxy_pass http://127.0.0.1:18080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

## 🔧 修复方案

### 方案1: 重启服务 (推荐)

```bash
cd /data/workspace/tencent_CodeBuddy/aladdinsun/AIdatabase

# 停止所有服务
pkill -f app_simple.py
pkill nginx
sleep 2

# 重新启动
bash start_with_nginx.sh

# 检查状态
ps aux | grep -E 'app_simple|nginx' | grep -v grep
ss -tlnp | grep -E ':80|:18080'
```

---

### 方案2: 独立启动(不用Nginx)

如果Nginx有问题,可以直接启动Flask服务:

```bash
cd /data/workspace/tencent_CodeBuddy/aladdinsun/AIdatabase

# 停止旧进程
pkill -f app_simple.py

# 启动Flask (前台,方便看日志)
python3 app_simple.py

# 或后台启动
nohup python3 app_simple.py > app.log 2>&1 &

# 访问测试
curl http://localhost:5000
# 或
curl http://localhost:18080
```

**修改app_simple.py启动端口:**

在文件末尾找到:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=18080, debug=False)
```

---

### 方案3: 安装缺失依赖

```bash
cd /data/workspace/tencent_CodeBuddy/aladdinsun/AIdatabase

# 完整安装(可能需要一些时间)
pip3 install -r requirements.txt -i https://mirrors.tencent.com/pypi/simple/

# 或只安装核心依赖
pip3 install Flask==3.0.0 pandas openpyxl numpy scikit-learn \
    -i https://mirrors.tencent.com/pypi/simple/
```

---

### 方案4: 配置Nginx反向代理

如果Nginx配置不存在,创建新配置:

```bash
# 创建配置文件
sudo tee /etc/nginx/conf.d/aidatabase.conf << 'EOF'
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
    }
    
    location /static {
        alias /data/workspace/tencent_CodeBuddy/aladdinsun/AIdatabase/static;
    }
}
EOF

# 测试配置
sudo nginx -t

# 重载Nginx
sudo nginx -s reload
```

---

## 🎯 快速修复脚本

创建一个一键修复脚本:

```bash
#!/bin/bash
# quick_fix.sh

cd /data/workspace/tencent_CodeBuddy/aladdinsun/AIdatabase

echo "🔧 快速修复AIdatabase服务..."

# 1. 停止旧进程
pkill -f app_simple.py
pkill nginx
sleep 2

# 2. 安装Flask(如果没有)
python3 -c "import flask" 2>/dev/null || pip3 install Flask==3.0.0 -i https://mirrors.tencent.com/pypi/simple/

# 3. 启动Flask
nohup python3 app_simple.py > app.log 2>&1 &
sleep 5

# 4. 检查状态
if ss -tlnp | grep -q ":18080\|:5000"; then
    echo "✅ Flask服务启动成功!"
    ss -tlnp | grep -E ":18080|:5000"
    
    # 5. 启动Nginx
    nginx 2>/dev/null
    
    if ss -tlnp | grep -q ":80"; then
        echo "✅ Nginx启动成功!"
        echo "📍 访问地址: http://aladdinsun.devcloud.woa.com"
    else
        echo "⚠️  Nginx启动失败,但Flask可直接访问"
        echo "📍 访问地址: http://服务器IP:18080 或 :5000"
    fi
else
    echo "❌ Flask启动失败,查看日志:"
    tail -30 app.log
fi
```

保存并执行:

```bash
chmod +x quick_fix.sh
bash quick_fix.sh
```

---

## 📊 常见问题FAQ

### Q1: 端口被占用怎么办?

```bash
# 查看占用端口的进程
lsof -i :18080
# 或
ss -tlnp | grep :18080

# 杀死占用进程
kill -9 <PID>
# 或强制释放端口
fuser -k 18080/tcp
```

### Q2: 没有权限启动Nginx?

```bash
# 使用sudo
sudo nginx

# 或检查Nginx是否已运行
ps aux | grep nginx
```

### Q3: Flask启动后立即退出?

```bash
# 前台运行查看错误
cd /data/workspace/tencent_CodeBuddy/aladdinsun/AIdatabase
python3 app_simple.py

# 查看完整日志
tail -100 app.log
```

### Q4: 访问域名返回502/504?

可能原因:
1. Flask服务未启动 → 检查进程
2. Nginx配置错误 → 检查 `nginx -t`
3. 端口不匹配 → 检查Flask端口和Nginx proxy_pass
4. 防火墙阻止 → 检查iptables/firewalld

### Q5: HTTPS访问问题?

```bash
# 检查SSL证书配置
nginx -T | grep ssl

# 如果需要HTTPS,配置:
server {
    listen 443 ssl;
    server_name aladdinsun.devcloud.woa.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://127.0.0.1:18080;
        ...
    }
}
```

---

## 🎓 验证清单

修复后,依次检查:

- [ ] Flask进程运行中: `ps aux | grep app_simple`
- [ ] 端口监听正常: `ss -tlnp | grep 18080`
- [ ] 本地访问成功: `curl http://localhost:18080`
- [ ] Nginx运行中: `ps aux | grep nginx`
- [ ] 80端口监听: `ss -tlnp | grep :80`
- [ ] 域名访问成功: 浏览器访问 http://aladdinsun.devcloud.woa.com

---

## 📞 还是不行?

提供以下信息协助排查:

```bash
# 收集诊断信息
cd /data/workspace/tencent_CodeBuddy/aladdinsun/AIdatabase

echo "=== Python版本 ===" > debug_info.txt
python3 --version >> debug_info.txt

echo -e "\n=== Flask版本 ===" >> debug_info.txt
python3 -c "import flask; print(flask.__version__)" 2>&1 >> debug_info.txt

echo -e "\n=== 进程状态 ===" >> debug_info.txt
ps aux | grep -E 'app_simple|nginx' >> debug_info.txt

echo -e "\n=== 端口监听 ===" >> debug_info.txt
ss -tlnp 2>&1 >> debug_info.txt

echo -e "\n=== 最新日志 ===" >> debug_info.txt
tail -50 app.log >> debug_info.txt 2>&1

echo -e "\n=== Nginx配置 ===" >> debug_info.txt
nginx -T 2>&1 | head -100 >> debug_info.txt

cat debug_info.txt
```

---

**创建时间:** 2025-11-11  
**最后更新:** 2025-11-11
