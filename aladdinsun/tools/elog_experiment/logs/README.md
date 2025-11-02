# Logs 目录说明

本目录用于存储IoTDB集群的运行日志。

## 📁 目录结构

```
logs/
├── confignode/          # 配置节点日志
├── datanode1/           # 数据节点1日志
├── datanode2/           # 数据节点2日志
└── datanode3/           # 数据节点3日志
```

## 📝 日志文件类型

每个节点目录下会包含以下日志文件：

### 1. 主日志文件
- `log_all.log` - 所有级别的日志（包含DEBUG/INFO/WARN/ERROR）
- `log_info.log` - INFO级别及以上的日志
- `log_warn.log` - WARN级别及以上的日志
- `log_error.log` - ERROR级别的日志

### 2. E-Log特定日志
- `log_elog.log` - E-Log弹性日志（根据θ阈值动态记录）
- `log_elog_metrics.log` - E-Log性能指标

### 3. 审计日志
- `log_audit.log` - 操作审计日志

## 🔍 日志查看

### 实时查看日志

```bash
# 查看配置节点日志
tail -f logs/confignode/log_all.log

# 查看数据节点1的错误日志
tail -f logs/datanode1/log_error.log

# 查看E-Log日志
tail -f logs/datanode1/log_elog.log
```

### 搜索日志

```bash
# 搜索错误信息
grep -r "ERROR" logs/

# 搜索特定时间段的日志
grep "2025-11-02 19:" logs/datanode1/log_all.log

# 搜索异常堆栈
grep -A 10 "Exception" logs/datanode1/log_error.log
```

### 统计日志

```bash
# 统计各级别日志数量
grep -c "ERROR" logs/datanode1/log_all.log
grep -c "WARN" logs/datanode1/log_all.log
grep -c "INFO" logs/datanode1/log_all.log

# 查看日志文件大小
du -sh logs/*/
```

## 📊 E-Log日志分析

E-Log日志格式示例：

```
2025-11-02 19:00:01.234 [INFO] [LPS-Reducer] θ=0.01, uncertainty=0.85, action=LOG
2025-11-02 19:00:01.235 [INFO] [Cascade-Discriminator] template_id=42, confidence=0.92
2025-11-02 19:00:01.236 [WARN] [Anomaly-Detector] Potential anomaly detected, F1=0.87
```

### 提取E-Log指标

```bash
# 提取触发决策
grep "LPS-Reducer" logs/datanode1/log_elog.log

# 提取异常检测结果
grep "Anomaly-Detector" logs/datanode1/log_elog.log

# 统计日志触发率
grep -c "action=LOG" logs/datanode1/log_elog.log
grep -c "action=SKIP" logs/datanode1/log_elog.log
```

## 🧹 日志清理

### 手动清理

```bash
# 清理所有日志
rm -rf logs/*/log_*.log

# 清理7天前的日志
find logs/ -name "*.log" -mtime +7 -delete

# 清理特定节点日志
rm -rf logs/datanode1/*
```

### 自动清理（cron）

```bash
# 添加到crontab，每天凌晨2点清理7天前的日志
0 2 * * * find /path/to/logs/ -name "*.log" -mtime +7 -delete
```

## 📈 日志大小预估

根据不同日志级别的预期大小：

| 日志级别 | 每小时 | 每天 | 说明 |
|---------|--------|------|------|
| DEBUG | ~500MB | ~12GB | 包含所有调试信息 |
| INFO | ~100MB | ~2.4GB | 标准运行日志 |
| WARN | ~10MB | ~240MB | 警告信息 |
| ERROR | ~1MB | ~24MB | 错误信息 |
| E-Log (θ=0.01) | ~50MB | ~1.2GB | 弹性日志（论文推荐） |

## ⚙️ 日志配置

日志配置在 `config/iotdb_config.yaml` 中：

```yaml
log:
  level: INFO                    # 基础日志级别
  max_file_size: 100MB          # 单个日志文件最大大小
  max_backup_index: 10          # 保留的备份文件数量
  elog_enabled: true            # 启用E-Log
  elog_theta: 0.01              # E-Log阈值
```

## 🔧 故障排查

### 常见问题

1. **日志文件过大**
   - 调整 `max_file_size` 和 `max_backup_index`
   - 提高日志级别（DEBUG → INFO → WARN）
   - 启用E-Log减少日志量

2. **找不到日志文件**
   - 检查Docker容器是否运行: `docker-compose ps`
   - 检查卷挂载: `docker-compose config`
   - 查看容器日志: `docker-compose logs datanode1`

3. **权限问题**
   - 检查目录权限: `ls -la logs/`
   - 修改权限: `chmod -R 755 logs/`

## 📚 相关文档

- IoTDB日志配置: https://iotdb.apache.org/UserGuide/Master/Reference/Config-Manual.html
- E-Log论文: `../pdfs/E-Log_Fine-Grained_Elastic_Log-Based_Anomaly_Detection.pdf`
- 实验配置: `../config/iotdb_config.yaml`

---

*目录创建时间: 2025-11-02*
*状态: 已创建，等待IoTDB运行*
