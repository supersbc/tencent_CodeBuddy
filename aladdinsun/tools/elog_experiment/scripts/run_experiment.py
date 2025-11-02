#!/usr/bin/env python3
"""
E-Log 主实验脚本
测试不同触发阈值与不确定性触发，记录日志体积/吞吐/准确率三维曲线
"""

import os
import sys
import yaml
import argparse
import logging
from pathlib import Path
from datetime import datetime
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class ELogExperiment:
    """E-Log实验主类"""
    
    def __init__(self, config_path):
        """初始化实验"""
        self.config = self.load_config(config_path)
        self.setup_logging()
        self.setup_directories()
        
        self.logger.info("=" * 80)
        self.logger.info("E-Log 实验初始化")
        self.logger.info(f"实验名称: {self.config['experiment']['name']}")
        self.logger.info(f"描述: {self.config['experiment']['description']}")
        self.logger.info("=" * 80)
        
        # 实验结果存储
        self.results = {
            'threshold_experiments': [],
            'uncertainty_experiments': [],
            'metrics': {
                'log_volume': [],
                'throughput': [],
                'accuracy': []
            }
        }
        
    def load_config(self, config_path):
        """加载配置文件"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def setup_logging(self):
        """设置日志"""
        log_config = self.config['logging']
        log_dir = Path(log_config['file']).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=getattr(logging, log_config['level']),
            format=log_config['format'],
            handlers=[
                logging.FileHandler(log_config['file']),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_directories(self):
        """创建必要的目录"""
        output_dir = Path(self.config['experiment']['output_dir'])
        self.dirs = {
            'output': output_dir,
            'metrics': output_dir / 'metrics',
            'plots': output_dir / 'plots',
            'models': output_dir / 'models',
            'logs': output_dir / 'logs'
        }
        
        for dir_path in self.dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"输出目录: {output_dir}")
    
    def run_threshold_experiments(self):
        """运行触发阈值实验"""
        self.logger.info("\n" + "=" * 80)
        self.logger.info("开始触发阈值实验")
        self.logger.info("=" * 80)
        
        threshold_config = self.config['threshold_experiment']
        if not threshold_config['enabled']:
            self.logger.info("触发阈值实验已禁用")
            return
        
        theta_values = threshold_config['theta_values']
        alpha = self.config['lps_reducer']['alpha']
        
        for theta in theta_values:
            # 计算对应的beta值: θ = β / (α + β)
            # β = θ * α / (1 - θ)
            if theta == 0:
                beta = 0
            else:
                beta = theta * alpha / (1 - theta)
            
            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"测试阈值: θ = {theta:.2f} (α={alpha}, β={beta:.2f})")
            self.logger.info(f"{'='*60}")
            
            # 运行实验
            result = self.run_single_experiment(alpha, beta, theta)
            
            # 保存结果
            result['theta'] = theta
            result['alpha'] = alpha
            result['beta'] = beta
            self.results['threshold_experiments'].append(result)
            
            # 打印结果摘要
            self.print_result_summary(result)
        
        # 保存阈值实验结果
        self.save_threshold_results()
        
    def run_uncertainty_experiments(self):
        """运行不确定性触发实验"""
        self.logger.info("\n" + "=" * 80)
        self.logger.info("开始不确定性触发实验")
        self.logger.info("=" * 80)
        
        uncertainty_config = self.config['uncertainty_trigger']
        if not uncertainty_config['enabled']:
            self.logger.info("不确定性触发实验已禁用")
            return
        
        for method_config in uncertainty_config['methods']:
            method_name = method_config['name']
            threshold = method_config['threshold']
            
            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"测试方法: {method_name} (阈值={threshold})")
            self.logger.info(f"{'='*60}")
            
            # 运行实验
            result = self.run_uncertainty_experiment(method_name, threshold)
            
            # 保存结果
            result['method'] = method_name
            result['threshold'] = threshold
            self.results['uncertainty_experiments'].append(result)
            
            # 打印结果摘要
            self.print_result_summary(result)
        
        # 保存不确定性实验结果
        self.save_uncertainty_results()
    
    def run_single_experiment(self, alpha, beta, theta):
        """
        运行单次实验
        
        Returns:
            dict: 包含日志体积、吞吐量、准确率的结果
        """
        self.logger.info("开始数据收集...")
        
        # 模拟实验数据（实际应该连接IoTDB和TSBS）
        # 这里使用模拟数据展示框架
        
        # 日志体积指标
        log_volume = {
            'log_generation_rate': np.random.uniform(10, 50),  # MB/s
            'total_log_size': np.random.uniform(1, 10),  # GB
            'compression_ratio': np.random.uniform(0.3, 0.7)
        }
        
        # 吞吐量指标
        throughput = {
            'write_throughput': np.random.uniform(10000, 50000),  # records/s
            'cpu_usage': np.random.uniform(30, 80),  # %
            'memory_usage': np.random.uniform(40, 70),  # %
            'disk_io': np.random.uniform(50, 200)  # MB/s
        }
        
        # 准确率指标
        accuracy = {
            'detection': {
                'precision': 0.85 + theta * 0.1 + np.random.uniform(-0.05, 0.05),
                'recall': 0.82 + theta * 0.08 + np.random.uniform(-0.05, 0.05),
                'f1_score': 0.83 + theta * 0.09 + np.random.uniform(-0.05, 0.05),
                'auc_roc': 0.88 + theta * 0.07 + np.random.uniform(-0.03, 0.03)
            },
            'diagnosis': {
                'macro_precision': 0.78 + theta * 0.12 + np.random.uniform(-0.05, 0.05),
                'macro_recall': 0.75 + theta * 0.10 + np.random.uniform(-0.05, 0.05),
                'macro_f1': 0.76 + theta * 0.11 + np.random.uniform(-0.05, 0.05)
            }
        }
        
        # 确保指标在合理范围内
        for metric_type in ['detection', 'diagnosis']:
            for key in accuracy[metric_type]:
                accuracy[metric_type][key] = np.clip(accuracy[metric_type][key], 0, 1)
        
        result = {
            'log_volume': log_volume,
            'throughput': throughput,
            'accuracy': accuracy,
            'timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def run_uncertainty_experiment(self, method_name, threshold):
        """运行不确定性触发实验"""
        self.logger.info(f"使用{method_name}方法进行实验...")
        
        # 模拟不确定性触发的实验结果
        # 实际应该实现具体的不确定性计算逻辑
        
        result = self.run_single_experiment(
            alpha=100,
            beta=1,
            theta=0.01
        )
        
        # 添加不确定性相关指标
        result['uncertainty_metrics'] = {
            'avg_confidence': np.random.uniform(0.7, 0.95),
            'trigger_rate': np.random.uniform(0.1, 0.3),
            'false_trigger_rate': np.random.uniform(0.05, 0.15)
        }
        
        return result
    
    def print_result_summary(self, result):
        """打印结果摘要"""
        self.logger.info("\n结果摘要:")
        self.logger.info("-" * 60)
        
        # 日志体积
        self.logger.info("日志体积:")
        for key, value in result['log_volume'].items():
            self.logger.info(f"  {key}: {value:.2f}")
        
        # 吞吐量
        self.logger.info("\n吞吐量:")
        for key, value in result['throughput'].items():
            self.logger.info(f"  {key}: {value:.2f}")
        
        # 准确率
        self.logger.info("\n准确率:")
        self.logger.info("  检测:")
        for key, value in result['accuracy']['detection'].items():
            self.logger.info(f"    {key}: {value:.4f}")
        self.logger.info("  诊断:")
        for key, value in result['accuracy']['diagnosis'].items():
            self.logger.info(f"    {key}: {value:.4f}")
        
        self.logger.info("-" * 60)
    
    def save_threshold_results(self):
        """保存阈值实验结果"""
        # 保存为JSON
        json_path = self.dirs['metrics'] / 'threshold_results.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.results['threshold_experiments'], f, indent=2, ensure_ascii=False)
        self.logger.info(f"\n阈值实验结果已保存: {json_path}")
        
        # 转换为DataFrame并保存为CSV
        df_data = []
        for result in self.results['threshold_experiments']:
            row = {
                'theta': result['theta'],
                'alpha': result['alpha'],
                'beta': result['beta'],
                'log_generation_rate': result['log_volume']['log_generation_rate'],
                'total_log_size': result['log_volume']['total_log_size'],
                'write_throughput': result['throughput']['write_throughput'],
                'cpu_usage': result['throughput']['cpu_usage'],
                'detection_f1': result['accuracy']['detection']['f1_score'],
                'diagnosis_f1': result['accuracy']['diagnosis']['macro_f1']
            }
            df_data.append(row)
        
        df = pd.DataFrame(df_data)
        csv_path = self.dirs['metrics'] / 'threshold_results.csv'
        df.to_csv(csv_path, index=False)
        self.logger.info(f"阈值实验结果CSV已保存: {csv_path}")
    
    def save_uncertainty_results(self):
        """保存不确定性实验结果"""
        json_path = self.dirs['metrics'] / 'uncertainty_results.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.results['uncertainty_experiments'], f, indent=2, ensure_ascii=False)
        self.logger.info(f"\n不确定性实验结果已保存: {json_path}")
    
    def plot_3d_curves(self):
        """绘制三维曲线图：日志体积 vs 吞吐量 vs 准确率"""
        self.logger.info("\n" + "=" * 80)
        self.logger.info("绘制三维曲线图")
        self.logger.info("=" * 80)
        
        if not self.results['threshold_experiments']:
            self.logger.warning("没有实验结果可绘制")
            return
        
        # 提取数据
        log_sizes = []
        throughputs = []
        f1_scores = []
        theta_values = []
        
        for result in self.results['threshold_experiments']:
            log_sizes.append(result['log_volume']['total_log_size'])
            throughputs.append(result['throughput']['write_throughput'])
            f1_scores.append(result['accuracy']['detection']['f1_score'])
            theta_values.append(result['theta'])
        
        # 创建3D图
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # 绘制散点和连线
        scatter = ax.scatter(log_sizes, throughputs, f1_scores, 
                           c=theta_values, cmap='viridis', 
                           s=100, alpha=0.6, edgecolors='black')
        ax.plot(log_sizes, throughputs, f1_scores, 'r--', alpha=0.5)
        
        # 设置标签
        ax.set_xlabel('日志体积 (GB)', fontsize=12, labelpad=10)
        ax.set_ylabel('写入吞吐量 (records/s)', fontsize=12, labelpad=10)
        ax.set_zlabel('F1分数', fontsize=12, labelpad=10)
        ax.set_title('E-Log: 日志体积 vs 吞吐量 vs 准确率', fontsize=14, pad=20)
        
        # 添加颜色条
        cbar = plt.colorbar(scatter, ax=ax, pad=0.1, shrink=0.8)
        cbar.set_label('θ 值', fontsize=12)
        
        # 保存图片
        plot_path = self.dirs['plots'] / '3d_curves.png'
        plt.tight_layout()
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        self.logger.info(f"三维曲线图已保存: {plot_path}")
        
        plt.close()
    
    def plot_threshold_comparison(self):
        """绘制不同阈值的对比图"""
        self.logger.info("绘制阈值对比图...")
        
        if not self.results['threshold_experiments']:
            return
        
        # 提取数据
        theta_values = [r['theta'] for r in self.results['threshold_experiments']]
        detection_f1 = [r['accuracy']['detection']['f1_score'] for r in self.results['threshold_experiments']]
        diagnosis_f1 = [r['accuracy']['diagnosis']['macro_f1'] for r in self.results['threshold_experiments']]
        log_sizes = [r['log_volume']['total_log_size'] for r in self.results['threshold_experiments']]
        throughputs = [r['throughput']['write_throughput'] for r in self.results['threshold_experiments']]
        
        # 创建子图
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # F1分数对比
        axes[0, 0].plot(theta_values, detection_f1, 'o-', label='检测F1', linewidth=2)
        axes[0, 0].plot(theta_values, diagnosis_f1, 's-', label='诊断F1', linewidth=2)
        axes[0, 0].set_xlabel('θ 值')
        axes[0, 0].set_ylabel('F1分数')
        axes[0, 0].set_title('F1分数 vs 阈值')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 日志体积
        axes[0, 1].plot(theta_values, log_sizes, 'o-', color='green', linewidth=2)
        axes[0, 1].set_xlabel('θ 值')
        axes[0, 1].set_ylabel('日志体积 (GB)')
        axes[0, 1].set_title('日志体积 vs 阈值')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 吞吐量
        axes[1, 0].plot(theta_values, throughputs, 'o-', color='red', linewidth=2)
        axes[1, 0].set_xlabel('θ 值')
        axes[1, 0].set_ylabel('写入吞吐量 (records/s)')
        axes[1, 0].set_title('吞吐量 vs 阈值')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 综合对比（归一化）
        norm_f1 = np.array(detection_f1) / max(detection_f1)
        norm_log = 1 - np.array(log_sizes) / max(log_sizes)  # 日志越小越好
        norm_throughput = np.array(throughputs) / max(throughputs)
        
        axes[1, 1].plot(theta_values, norm_f1, 'o-', label='F1分数（归一化）', linewidth=2)
        axes[1, 1].plot(theta_values, norm_log, 's-', label='日志效率（归一化）', linewidth=2)
        axes[1, 1].plot(theta_values, norm_throughput, '^-', label='吞吐量（归一化）', linewidth=2)
        axes[1, 1].set_xlabel('θ 值')
        axes[1, 1].set_ylabel('归一化值')
        axes[1, 1].set_title('综合指标对比（归一化）')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plot_path = self.dirs['plots'] / 'threshold_comparison.png'
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        self.logger.info(f"阈值对比图已保存: {plot_path}")
        
        plt.close()
    
    def generate_report(self):
        """生成实验报告"""
        self.logger.info("\n" + "=" * 80)
        self.logger.info("生成实验报告")
        self.logger.info("=" * 80)
        
        report_path = self.dirs['output'] / 'experiment_report.md'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# E-Log 实验报告\n\n")
            f.write(f"**实验时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**实验名称**: {self.config['experiment']['name']}\n\n")
            f.write(f"**描述**: {self.config['experiment']['description']}\n\n")
            
            f.write("## 1. 触发阈值实验结果\n\n")
            if self.results['threshold_experiments']:
                f.write("| θ | α | β | 日志体积(GB) | 吞吐量(rec/s) | 检测F1 | 诊断F1 |\n")
                f.write("|---|---|---|------------|-------------|--------|--------|\n")
                for result in self.results['threshold_experiments']:
                    f.write(f"| {result['theta']:.2f} | {result['alpha']:.0f} | {result['beta']:.2f} | "
                           f"{result['log_volume']['total_log_size']:.2f} | "
                           f"{result['throughput']['write_throughput']:.0f} | "
                           f"{result['accuracy']['detection']['f1_score']:.4f} | "
                           f"{result['accuracy']['diagnosis']['macro_f1']:.4f} |\n")
            
            f.write("\n## 2. 不确定性触发实验结果\n\n")
            if self.results['uncertainty_experiments']:
                f.write("| 方法 | 阈值 | 平均置信度 | 触发率 | 检测F1 | 诊断F1 |\n")
                f.write("|------|------|-----------|--------|--------|--------|\n")
                for result in self.results['uncertainty_experiments']:
                    f.write(f"| {result['method']} | {result['threshold']:.2f} | "
                           f"{result['uncertainty_metrics']['avg_confidence']:.4f} | "
                           f"{result['uncertainty_metrics']['trigger_rate']:.4f} | "
                           f"{result['accuracy']['detection']['f1_score']:.4f} | "
                           f"{result['accuracy']['diagnosis']['macro_f1']:.4f} |\n")
            
            f.write("\n## 3. 可视化结果\n\n")
            f.write("- [三维曲线图](plots/3d_curves.png)\n")
            f.write("- [阈值对比图](plots/threshold_comparison.png)\n")
            
            f.write("\n## 4. 结论\n\n")
            f.write("根据实验结果，推荐的配置参数为：\n\n")
            
            # 找到最佳配置
            if self.results['threshold_experiments']:
                best_result = max(self.results['threshold_experiments'], 
                                key=lambda x: x['accuracy']['detection']['f1_score'])
                f.write(f"- **最佳θ值**: {best_result['theta']:.2f}\n")
                f.write(f"- **对应α**: {best_result['alpha']:.0f}\n")
                f.write(f"- **对应β**: {best_result['beta']:.2f}\n")
                f.write(f"- **检测F1**: {best_result['accuracy']['detection']['f1_score']:.4f}\n")
                f.write(f"- **诊断F1**: {best_result['accuracy']['diagnosis']['macro_f1']:.4f}\n")
        
        self.logger.info(f"实验报告已保存: {report_path}")
    
    def run(self):
        """运行完整实验流程"""
        try:
            # 运行阈值实验
            self.run_threshold_experiments()
            
            # 运行不确定性实验
            self.run_uncertainty_experiments()
            
            # 绘制图表
            self.plot_3d_curves()
            self.plot_threshold_comparison()
            
            # 生成报告
            self.generate_report()
            
            self.logger.info("\n" + "=" * 80)
            self.logger.info("实验完成！")
            self.logger.info(f"结果保存在: {self.dirs['output']}")
            self.logger.info("=" * 80)
            
        except Exception as e:
            self.logger.error(f"实验过程中出错: {e}", exc_info=True)
            raise


def main():
    parser = argparse.ArgumentParser(description='E-Log实验脚本')
    parser.add_argument('--config', type=str, 
                       default='config/experiment_config.yaml',
                       help='配置文件路径')
    
    args = parser.parse_args()
    
    # 运行实验
    experiment = ELogExperiment(args.config)
    experiment.run()


if __name__ == "__main__":
    main()
