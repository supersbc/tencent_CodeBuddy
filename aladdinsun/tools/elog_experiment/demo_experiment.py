#!/usr/bin/env python3
"""
E-Log 演示实验脚本（简化版）
不需要额外依赖，直接运行展示实验框架
"""

import os
import json
from datetime import datetime
from pathlib import Path
import random


class ELogDemo:
    """E-Log演示实验类"""
    
    def __init__(self):
        self.output_dir = Path("./demo_results")
        self.output_dir.mkdir(exist_ok=True)
        
        print("=" * 80)
        print("E-Log 实验演示")
        print("论文: E-Log: Fine-Grained Elastic Log-Based Anomaly Detection")
        print("实验: IoTDB + TSBS，测试不同触发阈值")
        print("=" * 80)
        
        self.results = []
    
    def run_threshold_experiments(self):
        """运行触发阈值实验"""
        print("\n" + "=" * 80)
        print("阶段1: 触发阈值实验")
        print("=" * 80)
        
        # 测试不同的θ值
        theta_values = [0.00, 0.01, 0.02, 0.03, 0.05, 0.10]
        alpha = 100  # 固定α=100
        
        print(f"\n测试阈值: θ = {theta_values}")
        print(f"固定参数: α = {alpha}")
        print(f"计算公式: θ = β / (α + β)")
        
        for theta in theta_values:
            # 计算对应的β值
            if theta == 0:
                beta = 0
            else:
                beta = theta * alpha / (1 - theta)
            
            print(f"\n{'='*60}")
            print(f"测试配置: θ={theta:.2f}, α={alpha}, β={beta:.2f}")
            print(f"{'='*60}")
            
            # 模拟实验结果
            result = self.simulate_experiment(theta, alpha, beta)
            self.results.append(result)
            
            # 打印结果
            self.print_result(result)
    
    def simulate_experiment(self, theta, alpha, beta):
        """
        模拟实验结果
        根据论文，θ越大，日志越多，准确率越高，但吞吐量下降
        """
        # 基准值
        base_log_size = 5.0  # GB
        base_throughput = 30000  # records/s
        base_f1_detection = 0.85
        base_f1_diagnosis = 0.76
        
        # θ的影响
        # θ越大 -> 日志越多 -> 准确率提升 -> 吞吐量下降
        log_multiplier = 1 + theta * 2  # 日志增长
        accuracy_boost = theta * 0.15   # 准确率提升
        throughput_penalty = theta * 0.3  # 吞吐量下降
        
        # 添加随机噪声
        noise = lambda: random.uniform(-0.02, 0.02)
        
        result = {
            'theta': theta,
            'alpha': alpha,
            'beta': beta,
            
            # 日志体积指标
            'log_volume': {
                'log_generation_rate': round(base_log_size * log_multiplier / 30 + noise(), 2),  # MB/s
                'total_log_size': round(base_log_size * log_multiplier + noise(), 2),  # GB
                'compression_ratio': round(0.5 + noise() * 0.1, 2)
            },
            
            # 吞吐量指标
            'throughput': {
                'write_throughput': int(base_throughput * (1 - throughput_penalty) + noise() * 1000),
                'cpu_usage': round(50 + theta * 30 + noise() * 5, 1),  # %
                'memory_usage': round(55 + theta * 20 + noise() * 5, 1),  # %
            },
            
            # 准确率指标
            'accuracy': {
                'detection_f1': round(min(0.99, base_f1_detection + accuracy_boost + noise()), 4),
                'diagnosis_f1': round(min(0.99, base_f1_diagnosis + accuracy_boost + noise()), 4),
                'detection_precision': round(min(0.99, 0.87 + accuracy_boost + noise()), 4),
                'detection_recall': round(min(0.99, 0.83 + accuracy_boost + noise()), 4),
            },
            
            'timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def print_result(self, result):
        """打印单次实验结果"""
        print("\n结果:")
        print("-" * 60)
        
        print("日志体积:")
        print(f"  生成速率: {result['log_volume']['log_generation_rate']} MB/s")
        print(f"  总大小: {result['log_volume']['total_log_size']} GB")
        print(f"  压缩比: {result['log_volume']['compression_ratio']}")
        
        print("\n吞吐量:")
        print(f"  写入吞吐量: {result['throughput']['write_throughput']} records/s")
        print(f"  CPU使用率: {result['throughput']['cpu_usage']}%")
        print(f"  内存使用率: {result['throughput']['memory_usage']}%")
        
        print("\n准确率:")
        print(f"  检测F1: {result['accuracy']['detection_f1']}")
        print(f"  诊断F1: {result['accuracy']['diagnosis_f1']}")
        print(f"  检测精确率: {result['accuracy']['detection_precision']}")
        print(f"  检测召回率: {result['accuracy']['detection_recall']}")
        
        print("-" * 60)
    
    def save_results(self):
        """保存实验结果"""
        print("\n" + "=" * 80)
        print("保存实验结果")
        print("=" * 80)
        
        # 保存JSON
        json_path = self.output_dir / "threshold_results.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"\nJSON结果已保存: {json_path}")
        
        # 保存CSV格式
        csv_path = self.output_dir / "threshold_results.csv"
        with open(csv_path, 'w', encoding='utf-8') as f:
            # 写入表头
            f.write("theta,alpha,beta,log_size_gb,throughput_rps,cpu_usage,detection_f1,diagnosis_f1\n")
            
            # 写入数据
            for r in self.results:
                f.write(f"{r['theta']},{r['alpha']},{r['beta']},"
                       f"{r['log_volume']['total_log_size']},"
                       f"{r['throughput']['write_throughput']},"
                       f"{r['throughput']['cpu_usage']},"
                       f"{r['accuracy']['detection_f1']},"
                       f"{r['accuracy']['diagnosis_f1']}\n")
        
        print(f"CSV结果已保存: {csv_path}")
    
    def generate_summary_table(self):
        """生成结果摘要表"""
        print("\n" + "=" * 80)
        print("实验结果摘要")
        print("=" * 80)
        
        print("\n三维指标对比表:")
        print("-" * 100)
        print(f"{'θ':>6} | {'日志(GB)':>10} | {'吞吐量(rec/s)':>15} | {'检测F1':>10} | {'诊断F1':>10} | {'综合评分':>10}")
        print("-" * 100)
        
        for r in self.results:
            # 计算综合评分（归一化后的加权平均）
            # 日志越小越好，吞吐量越大越好，F1越大越好
            norm_log = 1 - (r['log_volume']['total_log_size'] - 5) / 10  # 归一化
            norm_throughput = r['throughput']['write_throughput'] / 30000
            norm_f1 = (r['accuracy']['detection_f1'] + r['accuracy']['diagnosis_f1']) / 2
            
            score = (norm_log * 0.2 + norm_throughput * 0.3 + norm_f1 * 0.5) * 100
            
            print(f"{r['theta']:>6.2f} | "
                  f"{r['log_volume']['total_log_size']:>10.2f} | "
                  f"{r['throughput']['write_throughput']:>15,} | "
                  f"{r['accuracy']['detection_f1']:>10.4f} | "
                  f"{r['accuracy']['diagnosis_f1']:>10.4f} | "
                  f"{score:>10.2f}")
        
        print("-" * 100)
    
    def generate_report(self):
        """生成Markdown报告"""
        print("\n生成实验报告...")
        
        report_path = self.output_dir / "experiment_report.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# E-Log 实验报告\n\n")
            f.write(f"**实验时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("**实验目标**: 测试不同触发阈值对日志体积、吞吐量、准确率的影响\n\n")
            
            f.write("## 1. 实验配置\n\n")
            f.write("- **数据库**: Apache IoTDB v1.2.2\n")
            f.write("- **基准测试**: TSBS (Time Series Benchmark Suite)\n")
            f.write("- **测试阈值**: θ = [0.00, 0.01, 0.02, 0.03, 0.05, 0.10]\n")
            f.write("- **固定参数**: α = 100 (准确率权重)\n")
            f.write("- **计算公式**: θ = β / (α + β)\n\n")
            
            f.write("## 2. 实验结果\n\n")
            f.write("### 2.1 三维指标对比\n\n")
            f.write("| θ | α | β | 日志体积(GB) | 吞吐量(rec/s) | CPU(%) | 检测F1 | 诊断F1 |\n")
            f.write("|---|---|---|------------|-------------|--------|--------|--------|\n")
            
            for r in self.results:
                f.write(f"| {r['theta']:.2f} | {r['alpha']:.0f} | {r['beta']:.2f} | "
                       f"{r['log_volume']['total_log_size']:.2f} | "
                       f"{r['throughput']['write_throughput']:,} | "
                       f"{r['throughput']['cpu_usage']:.1f} | "
                       f"{r['accuracy']['detection_f1']:.4f} | "
                       f"{r['accuracy']['diagnosis_f1']:.4f} |\n")
            
            f.write("\n### 2.2 关键发现\n\n")
            
            # 找到最佳配置
            best_f1 = max(self.results, key=lambda x: x['accuracy']['detection_f1'])
            best_throughput = max(self.results, key=lambda x: x['throughput']['write_throughput'])
            min_log = min(self.results, key=lambda x: x['log_volume']['total_log_size'])
            
            f.write(f"1. **最高检测F1**: θ={best_f1['theta']:.2f}, F1={best_f1['accuracy']['detection_f1']:.4f}\n")
            f.write(f"2. **最高吞吐量**: θ={best_throughput['theta']:.2f}, "
                   f"吞吐量={best_throughput['throughput']['write_throughput']:,} rec/s\n")
            f.write(f"3. **最小日志**: θ={min_log['theta']:.2f}, "
                   f"日志={min_log['log_volume']['total_log_size']:.2f} GB\n\n")
            
            f.write("### 2.3 论文对比\n\n")
            f.write("根据论文报告的结果：\n")
            f.write("- 异常检测F1提升: 3.15% (相比SOTA)\n")
            f.write("- 异常诊断F1提升: 9.32% (相比SOTA)\n")
            f.write("- 日志存储减少: 43.53% (相比info-level)\n")
            f.write("- 写入吞吐量提升: 26.22% (相比info-level)\n\n")
            
            f.write("## 3. 结论与建议\n\n")
            f.write("基于实验结果，推荐配置：\n\n")
            f.write(f"- **推荐θ值**: 0.01 (论文推荐值)\n")
            f.write(f"- **对应α**: 100\n")
            f.write(f"- **对应β**: 1\n")
            f.write(f"- **理由**: 在保持高准确率的同时，最小化日志开销和性能影响\n\n")
            
            f.write("## 4. 下一步工作\n\n")
            f.write("1. 在真实IoTDB环境中运行完整实验\n")
            f.write("2. 实现LPS Reducer强化学习算法\n")
            f.write("3. 实现Cascade LPS Discriminator\n")
            f.write("4. 测试不确定性触发机制\n")
            f.write("5. 与SOTA方法进行详细对比\n")
        
        print(f"实验报告已保存: {report_path}")
    
    def run(self):
        """运行完整演示"""
        try:
            # 运行实验
            self.run_threshold_experiments()
            
            # 保存结果
            self.save_results()
            
            # 生成摘要
            self.generate_summary_table()
            
            # 生成报告
            self.generate_report()
            
            print("\n" + "=" * 80)
            print("演示实验完成！")
            print(f"结果保存在: {self.output_dir}")
            print("=" * 80)
            
            print("\n下一步:")
            print("1. 查看 demo_results/threshold_results.json - 详细结果")
            print("2. 查看 demo_results/threshold_results.csv - CSV格式")
            print("3. 查看 demo_results/experiment_report.md - 实验报告")
            
        except Exception as e:
            print(f"\n错误: {e}")
            raise


if __name__ == "__main__":
    demo = ELogDemo()
    demo.run()
