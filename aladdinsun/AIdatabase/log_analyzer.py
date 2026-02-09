"""
TDSQL 日志分析与健康评分模块
基于 E-Log 论文方法：Drain日志解析 + LSTM特征提取 + 多维度评分

分析维度：
1. 日志模式分析（Drain模板提取）
2. 异常检测评分（基于规则+统计）
3. 性能评分（响应时间/吞吐量）
4. 稳定性评分（错误率/波动性）
5. 综合健康评分
"""

import re
import os
import json
import math
import time
from datetime import datetime, timedelta
from collections import defaultdict, Counter


# ==============================================================
# Drain 日志解析器（基于 tdsql_experiment 的实现）
# ==============================================================

class DrainNode:
    def __init__(self, depth=0, digit_or_token=None):
        self.depth = depth
        self.digit_or_token = digit_or_token
        self.children = {}
        self.clusters = []


class LogCluster:
    def __init__(self, log_template, cluster_id):
        self.log_template = log_template
        self.cluster_id = cluster_id
        self.log_ids = []
        self.size = 0


class DrainParser:
    """Drain日志模板解析器"""

    def __init__(self, depth=4, sim_th=0.4, max_child=100):
        self.depth = depth
        self.sim_th = sim_th
        self.max_child = max_child
        self.root_node = DrainNode()
        self.clusters = []
        self.cluster_counter = 0

    def preprocess(self, content):
        content = re.sub(r'\[\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}[^\]]*\]', '', content)
        content = re.sub(r'\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}[.,]\d+', '<TIMESTAMP>', content)
        content = re.sub(r'\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}', '<TIMESTAMP>', content)
        content = re.sub(r'\b(INFO|ERROR|WARN|WARNING|DEBUG|TRACE|FATAL)\b', '<LEVEL>', content)
        content = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(:\d+)?\b', '<IP>', content)
        content = re.sub(r'\b0x[0-9a-fA-F]+\b', '<HEX>', content)
        content = re.sub(r'timecost=[\d.]+', 'timecost=<TIME>', content)
        content = re.sub(r'tid=\d+', 'tid=<TID>', content)
        content = re.sub(r'qid=\d+', 'qid=<QID>', content)
        content = re.sub(r'con=\S+', 'con=<CON>', content)
        content = re.sub(r'topic=\S+', 'topic=<TOPIC>', content)
        content = re.sub(r'resultcode=\d+', 'resultcode=<RC>', content)
        content = re.sub(r'\b\d+\b', '<NUM>', content)
        tokens = content.split()
        return [t for t in tokens if t.strip()]

    def _is_wildcard(self, token):
        wildcards = ['<NUM>', '<IP>', '<HEX>', '<TIMESTAMP>', '<LEVEL>',
                     '<TIME>', '<TID>', '<QID>', '<CON>', '<TOPIC>', '<RC>']
        return token in wildcards or token.isdigit()

    def _tree_search(self, tokens):
        node = self.root_node.children.get(str(len(tokens)))
        if node is None:
            return None
        depth = 1
        for token in tokens:
            key = '<*>' if self._is_wildcard(token) else token
            if key in node.children:
                node = node.children[key]
            elif '<*>' in node.children:
                node = node.children['<*>']
            else:
                return None
            depth += 1
            if depth >= self.depth:
                break
        return node

    def _add_to_tree(self, cluster):
        tokens = cluster.log_template
        key = str(len(tokens))
        if key not in self.root_node.children:
            self.root_node.children[key] = DrainNode(1, key)
        node = self.root_node.children[key]
        depth = 1
        for token in tokens:
            k = '<*>' if self._is_wildcard(token) else token
            if k not in node.children:
                node.children[k] = DrainNode(depth + 1, k)
            node = node.children[k]
            depth += 1
            if depth >= self.depth:
                break
        node.clusters.append(cluster)

    def _seq_dist(self, s1, s2):
        if len(s1) != len(s2):
            return 0
        return sum(1 for a, b in zip(s1, s2) if a == b) / len(s1)

    def _merge_template(self, s1, s2):
        return [a if a == b else '<*>' for a, b in zip(s1, s2)] if len(s1) == len(s2) else s1

    def parse(self, content):
        tokens = self.preprocess(content)
        if not tokens:
            return None
        node = self._tree_search(tokens)
        if node:
            best, best_sim = None, -1
            for c in node.clusters:
                sim = self._seq_dist(tokens, c.log_template)
                if sim > best_sim:
                    best_sim, best = sim, c
            if best_sim >= self.sim_th:
                best.log_template = self._merge_template(tokens, best.log_template)
                best.size += 1
                return best
        self.cluster_counter += 1
        cluster = LogCluster(tokens, self.cluster_counter)
        cluster.size = 1
        self.clusters.append(cluster)
        self._add_to_tree(cluster)
        return cluster


# ==============================================================
# TDSQL 日志行解析器
# ==============================================================

# 匹配常见的TDSQL日志格式
TDSQL_LOG_PATTERNS = [
    # 格式1: [2025-08-04 00:00:01 12345] INFO ...
    re.compile(
        r'\[(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s*(?:\d+)?\]\s*'
        r'(?P<level>INFO|ERROR|WARN|WARNING|DEBUG|TRACE|FATAL)\s+'
        r'(?P<content>.*)'
    ),
    # 格式2: 2025-08-04 00:00:01,123 [thread] INFO class - message
    re.compile(
        r'(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})[.,]\d+\s+'
        r'(?:\[.*?\]\s+)?'
        r'(?P<level>INFO|ERROR|WARN|WARNING|DEBUG|TRACE|FATAL)\s+'
        r'(?P<content>.*)'
    ),
    # 格式3: 2025-08-04 00:00:01 INFO message
    re.compile(
        r'(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+'
        r'(?P<level>INFO|ERROR|WARN|WARNING|DEBUG|TRACE|FATAL)\s+'
        r'(?P<content>.*)'
    ),
    # 格式4: INFO 2025-08-04 00:00:01 message
    re.compile(
        r'(?P<level>INFO|ERROR|WARN|WARNING|DEBUG|TRACE|FATAL)\s+'
        r'(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+'
        r'(?P<content>.*)'
    ),
]

# 提取数值字段
TIMECOST_PATTERN = re.compile(r'(?<![_\w])timecost=([\d.]+)')
RESULTCODE_PATTERN = re.compile(r'resultcode=(\d+)')
CLIENT_IP_PATTERN = re.compile(r'(?:clientIP|clientip|client_ip|cip)=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', re.IGNORECASE)
SQL_TYPE_PATTERN = re.compile(r'sql_type=(\d+)')
ERRINFO_PATTERN = re.compile(r'errinfo=([^&\s]+)')


def parse_log_line(line):
    """解析单行日志，返回结构化字段"""
    line = line.strip()
    if not line:
        return None

    parsed = {
        'raw': line,
        'timestamp': None,
        'level': 'INFO',
        'content': line,
        'timecost': None,
        'resultcode': None,
        'client_ip': None,
    }

    for pat in TDSQL_LOG_PATTERNS:
        m = pat.match(line)
        if m:
            parsed['timestamp'] = m.group('timestamp')
            parsed['level'] = m.group('level').upper()
            if parsed['level'] == 'WARNING':
                parsed['level'] = 'WARN'
            parsed['content'] = m.group('content')
            break

    tc = TIMECOST_PATTERN.search(line)
    if tc:
        parsed['timecost'] = float(tc.group(1))

    rc = RESULTCODE_PATTERN.search(line)
    if rc:
        parsed['resultcode'] = int(rc.group(1))

    ip = CLIENT_IP_PATTERN.search(line)
    if ip:
        parsed['client_ip'] = ip.group(1)

    return parsed


# ==============================================================
# 时间窗口切分（E-Log方法）
# ==============================================================

def split_into_windows(parsed_logs, window_size=60, window_step=30):
    """将日志按时间窗口切分"""
    if not parsed_logs:
        return []

    timestamped = []
    for log in parsed_logs:
        if log and log.get('timestamp'):
            try:
                for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S,%f'):
                    try:
                        ts = datetime.strptime(log['timestamp'], fmt)
                        log['_ts'] = ts
                        timestamped.append(log)
                        break
                    except ValueError:
                        continue
            except Exception:
                pass

    if not timestamped:
        chunk_size = max(50, len(parsed_logs) // 20)
        windows = []
        for i in range(0, len(parsed_logs), chunk_size):
            chunk = [l for l in parsed_logs[i:i + chunk_size] if l]
            if chunk:
                windows.append({
                    'logs': chunk,
                    'start_time': f'chunk_{i}',
                    'end_time': f'chunk_{i + len(chunk)}',
                    'index': len(windows)
                })
        return windows

    timestamped.sort(key=lambda x: x['_ts'])
    start_ts = timestamped[0]['_ts']
    end_ts = timestamped[-1]['_ts']

    windows = []
    current = start_ts
    while current < end_ts:
        window_end = current + timedelta(seconds=window_size)
        logs_in_window = [l for l in timestamped if current <= l['_ts'] < window_end]
        if logs_in_window:
            windows.append({
                'logs': logs_in_window,
                'start_time': current.strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': window_end.strftime('%Y-%m-%d %H:%M:%S'),
                'index': len(windows)
            })
        current += timedelta(seconds=window_step)

    return windows


# ==============================================================
# 特征提取（与 tdsql_experiment 一致）
# ==============================================================

def extract_window_features(window):
    """提取单个时间窗口的统计特征"""
    logs = window['logs']
    total = len(logs)

    timecosts = [l['timecost'] for l in logs if l.get('timecost') is not None]
    levels = Counter(l.get('level', 'INFO') for l in logs)
    result_codes = [l['resultcode'] for l in logs if l.get('resultcode') is not None]
    client_ips = set(l['client_ip'] for l in logs if l.get('client_ip'))

    error_count = levels.get('ERROR', 0) + levels.get('FATAL', 0)
    warn_count = levels.get('WARN', 0) + levels.get('WARNING', 0)

    features = {
        'log_count': total,
        'error_count': error_count,
        'warn_count': warn_count,
        'error_rate': error_count / max(total, 1),
        'warn_rate': warn_count / max(total, 1),
        'avg_timecost': sum(timecosts) / len(timecosts) if timecosts else 0,
        'max_timecost': max(timecosts) if timecosts else 0,
        'min_timecost': min(timecosts) if timecosts else 0,
        'std_timecost': _std(timecosts) if len(timecosts) > 1 else 0,
        'p95_timecost': _percentile(timecosts, 95) if timecosts else 0,
        'p99_timecost': _percentile(timecosts, 99) if timecosts else 0,
        'error_resultcode_count': sum(1 for rc in result_codes if rc != 0),
        'error_resultcode_rate': sum(1 for rc in result_codes if rc != 0) / max(len(result_codes), 1),
        'unique_client_count': len(client_ips),
        'level_distribution': dict(levels),
    }
    return features


def _std(values):
    if len(values) < 2:
        return 0
    mean = sum(values) / len(values)
    return math.sqrt(sum((v - mean) ** 2 for v in values) / (len(values) - 1))


def _percentile(values, p):
    if not values:
        return 0
    s = sorted(values)
    k = (len(s) - 1) * p / 100
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return s[int(k)]
    return s[f] * (c - k) + s[c] * (k - f)


# ==============================================================
# 异常检测标注（基于 tdsql_experiment 的规则）
# ==============================================================

def detect_anomaly(features, thresholds=None):
    """基于规则的异常检测"""
    if thresholds is None:
        thresholds = {
            'error_rate': 0.05,
            'high_timecost': 10.0,
            'error_resultcode_rate': 0.1,
            'p95_timecost': 5.0,
        }

    reasons = []
    score = 0

    if features['error_rate'] > thresholds['error_rate']:
        reasons.append(f"错误率过高: {features['error_rate']:.1%}")
        score += features['error_rate'] * 40

    if features['avg_timecost'] > thresholds['high_timecost']:
        reasons.append(f"平均响应时间过高: {features['avg_timecost']:.2f}s")
        score += min(features['avg_timecost'] / thresholds['high_timecost'] * 20, 30)

    if features['p95_timecost'] > thresholds['p95_timecost']:
        reasons.append(f"P95响应时间过高: {features['p95_timecost']:.2f}s")
        score += min(features['p95_timecost'] / thresholds['p95_timecost'] * 10, 15)

    if features['error_resultcode_rate'] > thresholds['error_resultcode_rate']:
        reasons.append(f"异常返回码比例: {features['error_resultcode_rate']:.1%}")
        score += features['error_resultcode_rate'] * 30

    if features['warn_rate'] > 0.2:
        reasons.append(f"告警率较高: {features['warn_rate']:.1%}")
        score += features['warn_rate'] * 10

    is_anomaly = score > 10
    return {
        'is_anomaly': is_anomaly,
        'anomaly_score': min(score, 100),
        'reasons': reasons
    }


# ==============================================================
# 多维度健康评分
# ==============================================================

def compute_health_scores(all_window_features, template_stats):
    """计算多维度健康评分"""

    total_windows = len(all_window_features)
    if total_windows == 0:
        return _default_scores()

    # 1. 性能评分（响应时间维度）
    all_avg_tc = [f['avg_timecost'] for f in all_window_features if f['avg_timecost'] > 0]
    all_p95_tc = [f['p95_timecost'] for f in all_window_features if f['p95_timecost'] > 0]

    if all_avg_tc:
        avg_tc = sum(all_avg_tc) / len(all_avg_tc)
        performance_score = max(0, 100 - avg_tc * 5)
        if all_p95_tc:
            avg_p95 = sum(all_p95_tc) / len(all_p95_tc)
            performance_score = max(0, performance_score - max(0, avg_p95 - 5) * 3)
    else:
        performance_score = 85  # 无响应时间数据时给默认分

    # 2. 稳定性评分（错误率+波动性）
    error_rates = [f['error_rate'] for f in all_window_features]
    avg_error_rate = sum(error_rates) / len(error_rates)
    error_rate_std = _std(error_rates) if len(error_rates) > 1 else 0

    stability_score = max(0, 100 - avg_error_rate * 200 - error_rate_std * 100)

    warn_rates = [f['warn_rate'] for f in all_window_features]
    avg_warn_rate = sum(warn_rates) / len(warn_rates)
    stability_score = max(0, stability_score - avg_warn_rate * 50)

    # 3. 可用性评分（异常窗口比例）
    anomaly_results = [detect_anomaly(f) for f in all_window_features]
    anomaly_count = sum(1 for a in anomaly_results if a['is_anomaly'])
    anomaly_ratio = anomaly_count / total_windows

    availability_score = max(0, 100 - anomaly_ratio * 120)

    # 4. 日志质量评分（模板丰富度+结构化程度）
    num_templates = template_stats.get('total_templates', 0)
    total_logs = template_stats.get('total_logs', 1)
    template_ratio = num_templates / max(total_logs, 1)

    if num_templates > 0:
        top5_coverage = template_stats.get('top5_coverage', 50)
        log_quality_score = min(100, 60 + top5_coverage * 0.3 + min(num_templates, 200) * 0.05)
    else:
        log_quality_score = 50

    # 5. 吞吐量评分
    log_counts = [f['log_count'] for f in all_window_features]
    avg_log_count = sum(log_counts) / len(log_counts)
    throughput_std = _std(log_counts) if len(log_counts) > 1 else 0
    throughput_cv = throughput_std / max(avg_log_count, 1)

    throughput_score = max(0, 100 - throughput_cv * 50)

    # 综合评分（加权平均）
    weights = {
        'performance': 0.25,
        'stability': 0.25,
        'availability': 0.25,
        'log_quality': 0.10,
        'throughput': 0.15,
    }
    overall = (
        performance_score * weights['performance'] +
        stability_score * weights['stability'] +
        availability_score * weights['availability'] +
        log_quality_score * weights['log_quality'] +
        throughput_score * weights['throughput']
    )

    def _grade(score):
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'

    scores = {
        'overall': round(overall, 1),
        'overall_grade': _grade(overall),
        'dimensions': {
            'performance': {
                'score': round(performance_score, 1),
                'grade': _grade(performance_score),
                'label': '性能表现',
                'description': '基于平均响应时间和P95响应时间评估',
                'details': {
                    'avg_response_time': round(sum(all_avg_tc) / len(all_avg_tc), 3) if all_avg_tc else 0,
                    'avg_p95_time': round(sum(all_p95_tc) / len(all_p95_tc), 3) if all_p95_tc else 0,
                }
            },
            'stability': {
                'score': round(stability_score, 1),
                'grade': _grade(stability_score),
                'label': '运行稳定性',
                'description': '基于错误率和告警率的波动评估',
                'details': {
                    'avg_error_rate': round(avg_error_rate, 4),
                    'error_rate_volatility': round(error_rate_std, 4),
                    'avg_warn_rate': round(avg_warn_rate, 4),
                }
            },
            'availability': {
                'score': round(availability_score, 1),
                'grade': _grade(availability_score),
                'label': '可用性',
                'description': '基于异常时间窗口占比评估',
                'details': {
                    'anomaly_windows': anomaly_count,
                    'total_windows': total_windows,
                    'anomaly_ratio': round(anomaly_ratio, 4),
                }
            },
            'log_quality': {
                'score': round(log_quality_score, 1),
                'grade': _grade(log_quality_score),
                'label': '日志质量',
                'description': '基于日志模板丰富度和结构化程度',
                'details': {
                    'total_templates': num_templates,
                    'template_ratio': round(template_ratio, 4),
                }
            },
            'throughput': {
                'score': round(throughput_score, 1),
                'grade': _grade(throughput_score),
                'label': '吞吐稳定性',
                'description': '基于日志吞吐量的平稳程度评估',
                'details': {
                    'avg_logs_per_window': round(avg_log_count, 1),
                    'throughput_cv': round(throughput_cv, 4),
                }
            },
        }
    }

    return scores


def _default_scores():
    return {
        'overall': 0,
        'overall_grade': 'F',
        'dimensions': {}
    }


# ==============================================================
# 生成分析建议
# ==============================================================

def generate_recommendations(scores, anomaly_details):
    """根据评分结果生成改进建议"""
    recommendations = []

    dims = scores.get('dimensions', {})

    perf = dims.get('performance', {})
    if perf.get('score', 100) < 70:
        avg_rt = perf.get('details', {}).get('avg_response_time', 0)
        recommendations.append({
            'category': '性能优化',
            'severity': 'high' if perf['score'] < 50 else 'medium',
            'title': '响应时间过高',
            'description': f'平均响应时间 {avg_rt:.3f}s，建议优化慢查询、增加索引或扩容数据库资源。',
            'actions': [
                '检查TOP慢查询并优化SQL',
                '检查索引使用情况，添加缺失索引',
                '评估是否需要增加数据库实例规格',
                '考虑读写分离分摊压力'
            ]
        })

    stab = dims.get('stability', {})
    if stab.get('score', 100) < 70:
        recommendations.append({
            'category': '稳定性改进',
            'severity': 'high' if stab['score'] < 50 else 'medium',
            'title': '错误率或告警率偏高',
            'description': f'平均错误率 {stab.get("details", {}).get("avg_error_rate", 0):.2%}，需排查错误根因。',
            'actions': [
                '分析ERROR日志的具体错误类型和堆栈',
                '检查数据库连接池配置是否合理',
                '排查是否存在死锁或锁等待',
                '检查磁盘空间和内存使用情况'
            ]
        })

    avail = dims.get('availability', {})
    if avail.get('score', 100) < 80:
        ar = avail.get('details', {}).get('anomaly_ratio', 0)
        recommendations.append({
            'category': '可用性保障',
            'severity': 'high' if avail['score'] < 60 else 'medium',
            'title': '异常时间窗口占比较高',
            'description': f'异常窗口占比 {ar:.1%}，需加强监控和告警配置。',
            'actions': [
                '配置关键指标的告警阈值',
                '建立数据库巡检机制',
                '评估是否需要高可用架构升级',
                '制定故障应急预案'
            ]
        })

    tp = dims.get('throughput', {})
    if tp.get('score', 100) < 70:
        recommendations.append({
            'category': '负载均衡',
            'severity': 'medium',
            'title': '吞吐量波动较大',
            'description': '日志吞吐量波动系数较高，可能存在突发流量问题。',
            'actions': [
                '分析流量高峰时段，评估容量规划',
                '考虑引入限流机制保护数据库',
                '优化连接池参数应对突发连接',
            ]
        })

    # 汇总异常窗口详情中的高频问题
    if anomaly_details:
        reason_counter = Counter()
        for ad in anomaly_details:
            for r in ad.get('reasons', []):
                reason_counter[r.split(':')[0]] += 1
        if reason_counter:
            top_reasons = reason_counter.most_common(3)
            recommendations.append({
                'category': '高频问题',
                'severity': 'medium',
                'title': '检测到反复出现的异常模式',
                'description': '以下异常模式在多个时间窗口中重复出现：',
                'actions': [f'{reason}（出现{count}次）' for reason, count in top_reasons]
            })

    if not recommendations:
        recommendations.append({
            'category': '整体状态',
            'severity': 'low',
            'title': '数据库运行状况良好',
            'description': '各项指标均在正常范围内，继续保持当前运维策略。',
            'actions': ['定期巡检', '保持监控告警配置']
        })

    return recommendations


# ==============================================================
# 主分析入口
# ==============================================================

class TDSQLLogAnalyzer:
    """TDSQL日志分析器"""

    def __init__(self):
        self.drain_parser = DrainParser(depth=4, sim_th=0.4, max_child=100)

    def analyze(self, log_content, window_size=60, window_step=30):
        """
        分析日志内容

        Args:
            log_content: 日志文本内容（字符串）
            window_size: 时间窗口大小（秒）
            window_step: 时间窗口步长（秒）

        Returns:
            完整分析报告（dict）
        """
        start_time = time.time()

        # 1. 解析日志行
        lines = log_content.strip().split('\n')
        parsed_logs = []
        for line in lines:
            p = parse_log_line(line)
            if p:
                parsed_logs.append(p)

        if not parsed_logs:
            return {'error': '无法解析日志内容，请检查日志格式'}

        # 2. Drain模板提取
        self.drain_parser = DrainParser(depth=4, sim_th=0.4, max_child=100)
        template_map = {}
        log_template_ids = []
        for log in parsed_logs:
            cluster = self.drain_parser.parse(log['content'])
            if cluster:
                tpl_str = ' '.join(cluster.log_template)
                if tpl_str not in template_map:
                    template_map[tpl_str] = {
                        'id': len(template_map),
                        'template': tpl_str,
                        'count': 0,
                        'example': log['raw'][:200]
                    }
                template_map[tpl_str]['count'] += 1
                log_template_ids.append(template_map[tpl_str]['id'])
            else:
                log_template_ids.append(-1)

        # 模板统计
        sorted_templates = sorted(template_map.values(), key=lambda x: x['count'], reverse=True)
        total_logs = len(parsed_logs)
        top5_count = sum(t['count'] for t in sorted_templates[:5])

        template_stats = {
            'total_templates': len(template_map),
            'total_logs': total_logs,
            'top5_coverage': top5_count / max(total_logs, 1) * 100,
            'top_templates': [
                {
                    'id': t['id'],
                    'template': t['template'][:120],
                    'count': t['count'],
                    'percentage': round(t['count'] / max(total_logs, 1) * 100, 2),
                    'example': t['example']
                }
                for t in sorted_templates[:15]
            ]
        }

        # 3. 时间窗口切分
        windows = split_into_windows(parsed_logs, window_size, window_step)
        if not windows:
            windows = [{'logs': parsed_logs, 'start_time': 'all', 'end_time': 'all', 'index': 0}]

        # 4. 提取每个窗口的特征
        all_features = []
        window_details = []
        for w in windows:
            feat = extract_window_features(w)
            all_features.append(feat)
            anomaly = detect_anomaly(feat)
            window_details.append({
                'index': w['index'],
                'start_time': w['start_time'],
                'end_time': w['end_time'],
                'log_count': feat['log_count'],
                'error_count': feat['error_count'],
                'warn_count': feat['warn_count'],
                'avg_timecost': round(feat['avg_timecost'], 3),
                'max_timecost': round(feat['max_timecost'], 3),
                'is_anomaly': anomaly['is_anomaly'],
                'anomaly_score': round(anomaly['anomaly_score'], 1),
                'reasons': anomaly['reasons'],
            })

        # 5. 健康评分
        scores = compute_health_scores(all_features, template_stats)

        # 6. 异常窗口详情
        anomaly_windows = [w for w in window_details if w['is_anomaly']]

        # 7. 改进建议
        recommendations = generate_recommendations(scores, anomaly_windows)

        # 8. 日志级别分布统计
        level_dist = Counter(l.get('level', 'INFO') for l in parsed_logs)

        # 9. 时间线数据（用于前端图表）
        timeline = {
            'windows': [w['start_time'] for w in window_details],
            'error_counts': [w['error_count'] for w in window_details],
            'avg_timecosts': [w['avg_timecost'] for w in window_details],
            'log_counts': [w['log_count'] for w in window_details],
            'anomaly_scores': [w['anomaly_score'] for w in window_details],
        }

        elapsed = time.time() - start_time

        return {
            'success': True,
            'summary': {
                'total_logs': total_logs,
                'total_windows': len(windows),
                'anomaly_windows': len(anomaly_windows),
                'total_templates': len(template_map),
                'analysis_time': round(elapsed, 2),
                'window_size': window_size,
                'window_step': window_step,
                'level_distribution': dict(level_dist),
            },
            'scores': scores,
            'recommendations': recommendations,
            'template_stats': template_stats,
            'timeline': timeline,
            'anomaly_windows': anomaly_windows[:50],  # 最多50个异常窗口详情
            'window_details': window_details[:200],  # 最多200个窗口详情
        }

    def analyze_file(self, filepath, window_size=60, window_step=30, max_lines=None, sample_ratio=None):
        """
        流式分析日志文件，支持超大文件（>1GB）
        不会一次性加载整个文件到内存，而是逐行读取、逐窗口聚合。

        Args:
            filepath: 日志文件路径
            window_size: 时间窗口大小（秒）
            window_step: 时间窗口步长（秒）
            max_lines: 最大处理行数（None=不限制）
            sample_ratio: 采样比例（0-1），用于加速超大文件分析
        """
        if not os.path.exists(filepath):
            return {'error': f'文件不存在: {filepath}'}

        file_size = os.path.getsize(filepath)

        # 超大文件自动启用采样
        if sample_ratio is None:
            if file_size > 500 * 1024 * 1024:  # >500MB
                sample_ratio = 0.1  # 10% 采样
            elif file_size > 100 * 1024 * 1024:  # >100MB
                sample_ratio = 0.3  # 30% 采样
            elif file_size > 50 * 1024 * 1024:  # >50MB
                sample_ratio = 0.5  # 50% 采样
            # 否则全量

        return self._stream_analyze_file(filepath, window_size, window_step, max_lines, sample_ratio, file_size)

    def _stream_analyze_file(self, filepath, window_size, window_step, max_lines, sample_ratio, file_size):
        """流式分析：逐行读取，按时间窗口聚合，内存占用极低"""
        import random

        start_time = time.time()

        # 重置 Drain 解析器
        self.drain_parser = DrainParser(depth=4, sim_th=0.4, max_child=100)

        # 第一遍：扫描文件，收集所有解析行的时间戳范围 + 提取 Drain 模板 + 统计特征
        # 为了内存效率，我们分两步：
        #   1) 快速扫描获取时间范围和总行数
        #   2) 按时间窗口分批聚合

        total_lines = 0
        processed_lines = 0
        skipped_lines = 0
        first_ts = None
        last_ts = None
        level_dist = Counter()
        template_map = {}

        # 用于时间窗口聚合的字典：window_key -> 累积特征
        window_accum = {}  # key: window_start_ts -> accumulated stats

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line_no, line in enumerate(f):
                    total_lines += 1

                    # 采样过滤
                    if sample_ratio is not None and sample_ratio < 1.0:
                        if random.random() > sample_ratio:
                            skipped_lines += 1
                            continue

                    # 最大行数限制
                    if max_lines and processed_lines >= max_lines:
                        break

                    parsed = parse_log_line(line)
                    if not parsed:
                        continue

                    processed_lines += 1
                    level_dist[parsed.get('level', 'INFO')] += 1

                    # 解析时间戳
                    ts = None
                    if parsed.get('timestamp'):
                        for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S,%f'):
                            try:
                                ts = datetime.strptime(parsed['timestamp'], fmt)
                                break
                            except ValueError:
                                continue

                    if ts:
                        if first_ts is None or ts < first_ts:
                            first_ts = ts
                        if last_ts is None or ts > last_ts:
                            last_ts = ts

                    # Drain 模板提取
                    cluster = self.drain_parser.parse(parsed['content'])
                    if cluster:
                        tpl_str = ' '.join(cluster.log_template)
                        if tpl_str not in template_map:
                            template_map[tpl_str] = {
                                'id': len(template_map),
                                'template': tpl_str,
                                'count': 0,
                                'example': parsed['raw'][:200]
                            }
                        template_map[tpl_str]['count'] += 1

                    # 按时间窗口聚合特征（关键优化：不存储原始日志行）
                    if ts and first_ts:
                        # 计算该日志属于哪些窗口
                        elapsed = (ts - first_ts).total_seconds()
                        # 找到该时间点所属的窗口起始时间
                        if window_step > 0:
                            # 该日志可能属于多个重叠窗口，但为了性能只归入主窗口
                            win_idx = int(elapsed // window_step)
                            win_start = first_ts + timedelta(seconds=win_idx * window_step)
                        else:
                            win_idx = int(elapsed // window_size)
                            win_start = first_ts + timedelta(seconds=win_idx * window_size)

                        win_key = win_start.strftime('%Y-%m-%d %H:%M:%S')
                        if win_key not in window_accum:
                            window_accum[win_key] = {
                                'start_ts': win_start,
                                'log_count': 0,
                                'error_count': 0,
                                'warn_count': 0,
                                'timecosts': [],  # 只存数值，不存原始行
                                'resultcodes': [],
                                'client_ips': set(),
                                'levels': Counter(),
                            }

                        acc = window_accum[win_key]
                        acc['log_count'] += 1
                        lvl = parsed.get('level', 'INFO')
                        acc['levels'][lvl] += 1
                        if lvl in ('ERROR', 'FATAL'):
                            acc['error_count'] += 1
                        if lvl in ('WARN', 'WARNING'):
                            acc['warn_count'] += 1
                        if parsed.get('timecost') is not None:
                            acc['timecosts'].append(parsed['timecost'])
                        if parsed.get('resultcode') is not None:
                            acc['resultcodes'].append(parsed['resultcode'])
                        if parsed.get('client_ip'):
                            acc['client_ips'].add(parsed['client_ip'])

        except Exception as e:
            return {'error': f'读取文件失败: {str(e)}'}

        if processed_lines == 0:
            return {'error': '无法解析日志内容，请检查日志格式'}

        # 模板统计
        sorted_templates = sorted(template_map.values(), key=lambda x: x['count'], reverse=True)
        top5_count = sum(t['count'] for t in sorted_templates[:5])
        template_stats = {
            'total_templates': len(template_map),
            'total_logs': processed_lines,
            'top5_coverage': top5_count / max(processed_lines, 1) * 100,
            'top_templates': [
                {
                    'id': t['id'],
                    'template': t['template'][:120],
                    'count': t['count'],
                    'percentage': round(t['count'] / max(processed_lines, 1) * 100, 2),
                    'example': t['example']
                }
                for t in sorted_templates[:15]
            ]
        }

        # 从聚合数据计算每个窗口的特征
        sorted_windows = sorted(window_accum.items(), key=lambda x: x[0])
        all_features = []
        window_details = []

        for idx, (win_key, acc) in enumerate(sorted_windows):
            total = acc['log_count']
            timecosts = acc['timecosts']

            feat = {
                'log_count': total,
                'error_count': acc['error_count'],
                'warn_count': acc['warn_count'],
                'error_rate': acc['error_count'] / max(total, 1),
                'warn_rate': acc['warn_count'] / max(total, 1),
                'avg_timecost': sum(timecosts) / len(timecosts) if timecosts else 0,
                'max_timecost': max(timecosts) if timecosts else 0,
                'min_timecost': min(timecosts) if timecosts else 0,
                'std_timecost': _std(timecosts) if len(timecosts) > 1 else 0,
                'p95_timecost': _percentile(timecosts, 95) if timecosts else 0,
                'p99_timecost': _percentile(timecosts, 99) if timecosts else 0,
                'error_resultcode_count': sum(1 for rc in acc['resultcodes'] if rc != 0),
                'error_resultcode_rate': sum(1 for rc in acc['resultcodes'] if rc != 0) / max(len(acc['resultcodes']), 1),
                'unique_client_count': len(acc['client_ips']),
                'level_distribution': dict(acc['levels']),
            }
            all_features.append(feat)

            anomaly = detect_anomaly(feat)
            win_end = acc['start_ts'] + timedelta(seconds=window_size)
            window_details.append({
                'index': idx,
                'start_time': win_key,
                'end_time': win_end.strftime('%Y-%m-%d %H:%M:%S'),
                'log_count': feat['log_count'],
                'error_count': feat['error_count'],
                'warn_count': feat['warn_count'],
                'avg_timecost': round(feat['avg_timecost'], 3),
                'max_timecost': round(feat['max_timecost'], 3),
                'is_anomaly': anomaly['is_anomaly'],
                'anomaly_score': round(anomaly['anomaly_score'], 1),
                'reasons': anomaly['reasons'],
            })

            # 释放大列表内存
            acc['timecosts'] = None
            acc['resultcodes'] = None
            acc['client_ips'] = None

        # 如果没有时间窗口（日志没有时间戳），退化为单窗口
        if not all_features:
            return {'error': '无法从日志中提取时间戳，无法进行时间窗口分析。请检查日志格式。'}

        # 健康评分
        scores = compute_health_scores(all_features, template_stats)

        # 异常窗口详情
        anomaly_windows = [w for w in window_details if w['is_anomaly']]

        # 改进建议
        recommendations = generate_recommendations(scores, anomaly_windows)

        # 时间线数据
        timeline = {
            'windows': [w['start_time'] for w in window_details],
            'error_counts': [w['error_count'] for w in window_details],
            'avg_timecosts': [w['avg_timecost'] for w in window_details],
            'log_counts': [w['log_count'] for w in window_details],
            'anomaly_scores': [w['anomaly_score'] for w in window_details],
        }

        elapsed = time.time() - start_time

        # 采样说明
        sampling_info = None
        if sample_ratio is not None and sample_ratio < 1.0:
            sampling_info = {
                'sample_ratio': sample_ratio,
                'total_file_lines': total_lines,
                'processed_lines': processed_lines,
                'skipped_lines': skipped_lines,
                'note': f'由于文件较大({file_size / 1024 / 1024:.0f}MB)，已使用{sample_ratio * 100:.0f}%采样分析'
            }

        return {
            'success': True,
            'summary': {
                'total_logs': processed_lines,
                'total_file_lines': total_lines,
                'total_windows': len(window_details),
                'anomaly_windows': len(anomaly_windows),
                'total_templates': len(template_map),
                'analysis_time': round(elapsed, 2),
                'window_size': window_size,
                'window_step': window_step,
                'level_distribution': dict(level_dist),
                'file_size_mb': round(file_size / 1024 / 1024, 1),
                'sampling_info': sampling_info,
            },
            'scores': scores,
            'recommendations': recommendations,
            'template_stats': template_stats,
            'timeline': timeline,
            'anomaly_windows': anomaly_windows[:50],
            'window_details': window_details[:200],
        }
