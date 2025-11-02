#!/usr/bin/env python3
"""
E-Log 实验结果可视化脚本
读取CSV结果并生成图表（使用纯文本ASCII艺术）
"""

import csv
from pathlib import Path


def read_results(csv_path):
    """读取CSV结果"""
    results = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append({
                'theta': float(row['theta']),
                'log_size': float(row['log_size_gb']),
                'throughput': int(row['throughput_rps']),
                'cpu': float(row['cpu_usage']),
                'detection_f1': float(row['detection_f1']),
                'diagnosis_f1': float(row['diagnosis_f1'])
            })
    return results


def normalize(values):
    """归一化到0-1"""
    min_val = min(values)
    max_val = max(values)
    if max_val == min_val:
        return [0.5] * len(values)
    return [(v - min_val) / (max_val - min_val) for v in values]


def plot_ascii_bar(label, value, max_width=50):
    """绘制ASCII条形图"""
    bar_length = int(value * max_width)
    bar = '█' * bar_length
    return f"{label:20s} |{bar:<{max_width}s}| {value:.4f}"


def visualize_results(results):
    """可视化实验结果"""
    
    print("\n" + "=" * 80)
    print("E-Log 实验结果可视化")
    print("=" * 80)
    
    # 提取数据
    theta_values = [r['theta'] for r in results]
    log_sizes = [r['log_size'] for r in results]
    throughputs = [r['throughput'] for r in results]
    detection_f1s = [r['detection_f1'] for r in results]
    diagnosis_f1s = [r['diagnosis_f1'] for r in results]
    
    # 1. 日志体积趋势
    print("\n1. 日志体积趋势 (GB)")
    print("-" * 80)
    for i, (theta, log_size) in enumerate(zip(theta_values, log_sizes)):
        norm_value = (log_size - min(log_sizes)) / (max(log_sizes) - min(log_sizes))
        print(plot_ascii_bar(f"θ={theta:.2f}", norm_value) + f" ({log_size:.2f} GB)")
    
    # 2. 吞吐量趋势
    print("\n2. 写入吞吐量趋势 (records/s)")
    print("-" * 80)
    norm_throughputs = normalize(throughputs)
    for i, (theta, throughput, norm) in enumerate(zip(theta_values, throughputs, norm_throughputs)):
        print(plot_ascii_bar(f"θ={theta:.2f}", norm) + f" ({throughput:,} rec/s)")
    
    # 3. 检测F1趋势
    print("\n3. 异常检测F1分数")
    print("-" * 80)
    norm_detection = normalize(detection_f1s)
    for i, (theta, f1, norm) in enumerate(zip(theta_values, detection_f1s, norm_detection)):
        print(plot_ascii_bar(f"θ={theta:.2f}", norm) + f" (F1={f1:.4f})")
    
    # 4. 诊断F1趋势
    print("\n4. 异常诊断F1分数")
    print("-" * 80)
    norm_diagnosis = normalize(diagnosis_f1s)
    for i, (theta, f1, norm) in enumerate(zip(theta_values, diagnosis_f1s, norm_diagnosis)):
        print(plot_ascii_bar(f"θ={theta:.2f}", norm) + f" (F1={f1:.4f})")
    
    # 5. 综合对比
    print("\n5. 综合指标对比（归一化）")
    print("-" * 80)
    print(f"{'θ':>6} | {'日志↓':>8} | {'吞吐↑':>8} | {'检测F1↑':>10} | {'诊断F1↑':>10} | {'综合分':>8}")
    print("-" * 80)
    
    for i in range(len(results)):
        # 日志越小越好，所以取反
        norm_log = 1 - (log_sizes[i] - min(log_sizes)) / (max(log_sizes) - min(log_sizes))
        norm_throughput = norm_throughputs[i]
        norm_det = norm_detection[i]
        norm_diag = norm_diagnosis[i]
        
        # 综合评分（加权平均）
        score = (norm_log * 0.2 + norm_throughput * 0.3 + 
                norm_det * 0.25 + norm_diag * 0.25)
        
        print(f"{theta_values[i]:>6.2f} | "
              f"{norm_log:>8.4f} | "
              f"{norm_throughput:>8.4f} | "
              f"{norm_det:>10.4f} | "
              f"{norm_diag:>10.4f} | "
              f"{score:>8.4f}")
    
    # 6. 最佳配置推荐
    print("\n6. 最佳配置推荐")
    print("-" * 80)
    
    # 找到最佳检测F1
    best_detection_idx = detection_f1s.index(max(detection_f1s))
    print(f"最高检测F1: θ={theta_values[best_detection_idx]:.2f}, "
          f"F1={detection_f1s[best_detection_idx]:.4f}")
    
    # 找到最佳吞吐量
    best_throughput_idx = throughputs.index(max(throughputs))
    print(f"最高吞吐量: θ={theta_values[best_throughput_idx]:.2f}, "
          f"吞吐量={throughputs[best_throughput_idx]:,} rec/s")
    
    # 找到最小日志
    min_log_idx = log_sizes.index(min(log_sizes))
    print(f"最小日志量: θ={theta_values[min_log_idx]:.2f}, "
          f"日志={log_sizes[min_log_idx]:.2f} GB")
    
    # 论文推荐值
    print(f"\n论文推荐值: θ=0.01 (α=100, β=1)")
    print("理由: 在保持高准确率的同时，最小化日志开销和性能影响")
    
    # 7. 三维关系图（简化版）
    print("\n7. 三维关系示意图")
    print("-" * 80)
    print("日志体积 ↑")
    print("    │")
    print("    │     ╱ 准确率 ↑")
    print("    │   ╱")
    print("    │ ╱")
    print("    │╱__________ 吞吐量 →")
    print("    │╲")
    print("    │  ╲")
    print("    │    ╲ 吞吐量 ↓")
    print("    │")
    print("\n关键洞察:")
    print("- θ ↑ → 日志 ↑ → 准确率 ↑ 但 吞吐量 ↓")
    print("- θ ↓ → 日志 ↓ → 吞吐量 ↑ 但 准确率 ↓")
    print("- 最优平衡点: θ=0.01")
    
    print("\n" + "=" * 80)


def main():
    csv_path = Path("demo_results/threshold_results.csv")
    
    if not csv_path.exists():
        print(f"错误: 找不到结果文件 {csv_path}")
        print("请先运行: python3 demo_experiment.py")
        return
    
    results = read_results(csv_path)
    visualize_results(results)
    
    print("\n提示: 查看 demo_results/experiment_report.md 获取完整报告")


if __name__ == "__main__":
    main()
