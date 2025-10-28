"""
TDSQL 架构预测模型训练系统
支持从实际案例中学习，持续优化预测准确性
"""

import json
import os
from datetime import datetime
import numpy as np

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import Dataset, DataLoader
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("⚠️  PyTorch 未安装，训练功能不可用")
    # 创建占位类
    class Dataset:
        pass

class TDSQLDataset(Dataset):
    """TDSQL 训练数据集"""
    
    def __init__(self, data_file='training_data.json'):
        self.data_file = data_file
        self.samples = self.load_data()
    
    def load_data(self):
        """加载训练数据"""
        if not os.path.exists(self.data_file):
            return []
        
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        sample = self.samples[idx]
        
        # 提取特征
        features = self._extract_features(sample['input'])
        
        # 提取标签
        labels = {
            'architecture_type': self._encode_architecture(sample['output']['architecture_type']),
            'node_count': sample['output']['node_count'],
            'shard_count': sample['output']['shard_count'],
            'replica_count': sample['output']['replica_count']
        }
        
        return torch.FloatTensor(features), labels
    
    def _extract_features(self, data):
        """提取特征向量"""
        features = np.zeros(50)
        
        features[0] = data.get('total_data_size_gb', 0) / 10000
        features[1] = data.get('table_count', 0) / 1000
        features[2] = data.get('database_count', 0) / 100
        features[3] = data.get('qps', 0) / 100000
        features[4] = data.get('tps', 0) / 50000
        features[5] = data.get('concurrent_connections', 0) / 10000
        features[6] = 1 if data.get('need_high_availability', False) else 0
        features[7] = 1 if data.get('need_disaster_recovery', False) else 0
        features[8] = 1 if data.get('need_read_write_split', False) else 0
        features[12] = data.get('max_table_size_gb', 0) / 1000
        features[13] = data.get('avg_table_size_gb', 0) / 100
        features[14] = data.get('data_growth_rate', 0) / 100
        
        return features
    
    def _encode_architecture(self, arch_type):
        """编码架构类型"""
        mapping = {'standalone': 0, 'distributed': 1, 'hybrid': 2}
        return mapping.get(arch_type, 1)


class TrainingSystem:
    """训练系统"""
    
    def __init__(self, model, data_file='training_data.json'):
        self.model = model
        self.data_file = data_file
        self.history_file = 'training_history.json'
        self.best_model_file = 'best_model.pth'
        self.training_history = []
    
    def add_case(self, input_data, output_data, feedback=None):
        """添加训练案例"""
        case = {
            'id': self._generate_id(),
            'timestamp': datetime.now().isoformat(),
            'input': input_data,
            'output': output_data,
            'feedback': feedback,
            'used_for_training': False
        }
        
        # 加载现有数据
        cases = self._load_cases()
        cases.append(case)
        
        # 保存
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(cases, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 案例已添加: ID={case['id']}")
        return case['id']
    
    def train(self, epochs=100, batch_size=32, learning_rate=0.001):
        """训练模型"""
        if not TORCH_AVAILABLE:
            print("❌ PyTorch 未安装，无法训练")
            return False
        
        # 加载数据集
        dataset = TDSQLDataset(self.data_file)
        
        if len(dataset) < 10:
            print(f"⚠️  训练数据不足（当前: {len(dataset)}，建议: ≥10）")
            return False
        
        print(f"📊 开始训练，数据集大小: {len(dataset)}")
        
        # 创建数据加载器
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        # 优化器
        optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        
        # 损失函数
        criterion_class = nn.CrossEntropyLoss()
        criterion_reg = nn.MSELoss()
        
        best_loss = float('inf')
        
        # 训练循环
        for epoch in range(epochs):
            total_loss = 0
            
            for features, labels in dataloader:
                optimizer.zero_grad()
                
                # 前向传播
                outputs = self.model(features)
                
                # 计算损失
                loss_arch = criterion_class(outputs['architecture_type'], 
                                           torch.LongTensor([labels['architecture_type']]))
                loss_node = criterion_reg(outputs['node_count'], 
                                         torch.FloatTensor([[labels['node_count']]]))
                loss_shard = criterion_reg(outputs['shard_count'], 
                                          torch.FloatTensor([[labels['shard_count']]]))
                loss_replica = criterion_reg(outputs['replica_count'], 
                                            torch.FloatTensor([[labels['replica_count']]]))
                
                loss = loss_arch + loss_node + loss_shard + loss_replica
                
                # 反向传播
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
            
            avg_loss = total_loss / len(dataloader)
            
            if (epoch + 1) % 10 == 0:
                print(f"Epoch [{epoch+1}/{epochs}], Loss: {avg_loss:.4f}")
            
            # 保存最佳模型
            if avg_loss < best_loss:
                best_loss = avg_loss
                torch.save(self.model.state_dict(), self.best_model_file)
                print(f"💾 保存最佳模型 (Loss: {best_loss:.4f})")
        
        # 记录训练历史
        self._save_training_history(epochs, len(dataset), best_loss)
        
        print(f"✅ 训练完成！最佳损失: {best_loss:.4f}")
        return True
    
    def evaluate(self, test_data):
        """评估模型"""
        if not TORCH_AVAILABLE:
            return None
        
        self.model.eval()
        correct = 0
        total = len(test_data)
        
        with torch.no_grad():
            for case in test_data:
                prediction = self.model.predict(case['input'])
                actual = case['output']
                
                if prediction['architecture_type'] == actual['architecture_type']:
                    correct += 1
        
        accuracy = correct / total if total > 0 else 0
        print(f"📊 模型准确率: {accuracy*100:.2f}%")
        return accuracy
    
    def get_statistics(self):
        """获取训练统计信息"""
        cases = self._load_cases()
        
        stats = {
            'total_cases': len(cases),
            'trained_cases': sum(1 for c in cases if c.get('used_for_training', False)),
            'architecture_distribution': {},
            'data_size_range': {'min': 0, 'max': 0, 'avg': 0},
            'qps_range': {'min': 0, 'max': 0, 'avg': 0}
        }
        
        if cases:
            # 架构分布
            for case in cases:
                arch = case['output']['architecture_type']
                stats['architecture_distribution'][arch] = \
                    stats['architecture_distribution'].get(arch, 0) + 1
            
            # 数据量范围
            data_sizes = [c['input']['total_data_size_gb'] for c in cases]
            stats['data_size_range'] = {
                'min': min(data_sizes),
                'max': max(data_sizes),
                'avg': sum(data_sizes) / len(data_sizes)
            }
            
            # QPS 范围
            qps_values = [c['input'].get('qps', 0) for c in cases]
            stats['qps_range'] = {
                'min': min(qps_values),
                'max': max(qps_values),
                'avg': sum(qps_values) / len(qps_values)
            }
        
        return stats
    
    def _load_cases(self):
        """加载案例"""
        if not os.path.exists(self.data_file):
            return []
        
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _generate_id(self):
        """生成唯一ID"""
        return f"case_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    
    def _save_training_history(self, epochs, dataset_size, final_loss):
        """保存训练历史"""
        history = {
            'timestamp': datetime.now().isoformat(),
            'epochs': epochs,
            'dataset_size': dataset_size,
            'final_loss': final_loss
        }
        
        # 加载历史记录
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                all_history = json.load(f)
        else:
            all_history = []
        
        all_history.append(history)
        
        # 保存
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(all_history, f, ensure_ascii=False, indent=2)


def create_sample_cases():
    """创建示例训练案例"""
    cases = [
        {
            'input': {
                'total_data_size_gb': 100,
                'table_count': 20,
                'database_count': 2,
                'qps': 500,
                'tps': 200,
                'concurrent_connections': 100,
                'need_high_availability': False,
                'need_disaster_recovery': False,
                'need_read_write_split': False,
                'max_table_size_gb': 10,
                'avg_table_size_gb': 5,
                'data_growth_rate': 10
            },
            'output': {
                'architecture_type': 'standalone',
                'node_count': 1,
                'shard_count': 1,
                'replica_count': 1
            }
        },
        {
            'input': {
                'total_data_size_gb': 8640,
                'table_count': 150,
                'database_count': 8,
                'qps': 50000,
                'tps': 20000,
                'concurrent_connections': 5000,
                'need_high_availability': True,
                'need_disaster_recovery': True,
                'need_read_write_split': True,
                'max_table_size_gb': 1000,
                'avg_table_size_gb': 57.6,
                'data_growth_rate': 30
            },
            'output': {
                'architecture_type': 'distributed',
                'node_count': 9,
                'shard_count': 9,
                'replica_count': 3
            }
        },
        {
            'input': {
                'total_data_size_gb': 2000,
                'table_count': 80,
                'database_count': 5,
                'qps': 15000,
                'tps': 8000,
                'concurrent_connections': 2000,
                'need_high_availability': True,
                'need_disaster_recovery': False,
                'need_read_write_split': True,
                'max_table_size_gb': 200,
                'avg_table_size_gb': 25,
                'data_growth_rate': 20
            },
            'output': {
                'architecture_type': 'distributed',
                'node_count': 4,
                'shard_count': 4,
                'replica_count': 2
            }
        }
    ]
    
    # 保存示例案例
    with open('training_data.json', 'w', encoding='utf-8') as f:
        json.dump(cases, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已创建 {len(cases)} 个示例训练案例")
    return cases


if __name__ == '__main__':
    print("="*60)
    print("🧠 TDSQL 架构预测模型训练系统")
    print("="*60)
    
    # 创建示例案例
    create_sample_cases()
    
    if TORCH_AVAILABLE:
        from model import TDSQLArchitecturePredictor
        
        # 初始化模型和训练系统
        model = TDSQLArchitecturePredictor()
        trainer = TrainingSystem(model)
        
        # 获取统计信息
        stats = trainer.get_statistics()
        print(f"\n📊 数据集统计:")
        print(f"  总案例数: {stats['total_cases']}")
        print(f"  架构分布: {stats['architecture_distribution']}")
        
        # 开始训练
        print("\n🚀 开始训练...")
        trainer.train(epochs=50, batch_size=2, learning_rate=0.001)
    else:
        print("\n⚠️  请先安装 PyTorch 以使用训练功能:")
        print("  pip install torch")
