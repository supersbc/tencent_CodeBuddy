import numpy as np

try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("PyTorch 未安装，使用基于规则的预测模式")

class TDSQLArchitecturePredictor:
    """TDSQL 架构预测模型"""
    
    def __init__(self, input_dim=50, hidden_dim=256):
        if not TORCH_AVAILABLE:
            print("初始化基于规则的预测器")
            return
        super(TDSQLArchitecturePredictor, self).__init__()
        
        if not TORCH_AVAILABLE:
            return
            
        # 特征提取网络
        self.feature_extractor = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, 128),
            nn.ReLU()
        )
        
        # 架构类型预测（单机/分布式/混合）
        self.architecture_classifier = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 3),
            nn.Softmax(dim=1)
        )
        
        # 节点数量预测
        self.node_count_predictor = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )
        
        # 分片数量预测
        self.shard_count_predictor = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )
        
        # 副本数量预测
        self.replica_count_predictor = nn.Sequential(
            nn.Linear(128, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )
    
    def forward(self, x):
        """前向传播"""
        if not TORCH_AVAILABLE:
            return None
            
        features = self.feature_extractor(x)
        
        arch_type = self.architecture_classifier(features)
        node_count = self.node_count_predictor(features)
        shard_count = self.shard_count_predictor(features)
        replica_count = self.replica_count_predictor(features)
        
        return {
            'architecture_type': arch_type,
            'node_count': node_count,
            'shard_count': shard_count,
            'replica_count': replica_count
        }
    
    def predict(self, data):
        """预测 TDSQL 架构配置"""
        if not TORCH_AVAILABLE:
            # 使用基于规则的预测
            return self._rule_based_predict(data)
        
        # 提取特征
        features = self._extract_features(data)
        
        # 转换为张量
        x = torch.FloatTensor(features).unsqueeze(0)
        
        # 预测
        with torch.no_grad():
            output = self.forward(x)
        
        # 解析结果
        arch_types = ['standalone', 'distributed', 'hybrid']
        arch_idx = torch.argmax(output['architecture_type'], dim=1).item()
        
        result = {
            'architecture_type': arch_types[arch_idx],
            'node_count': max(1, int(output['node_count'].item())),
            'shard_count': max(1, int(output['shard_count'].item())),
            'replica_count': max(1, int(output['replica_count'].item())),
            'confidence': output['architecture_type'][0][arch_idx].item()
        }
        
        # 基于规则的调整
        result = self._apply_business_rules(data, result)
        
        return result
    
    def _rule_based_predict(self, data):
        """基于规则的预测（不使用深度学习）"""
        total_data_gb = data.get('total_data_size_gb', 0)
        qps = data.get('qps', 0)
        
        # 初始预测
        result = {
            'architecture_type': 'standalone',
            'node_count': 1,
            'shard_count': 1,
            'replica_count': 1,
            'confidence': 0.85
        }
        
        # 根据数据量和性能决定架构
        if total_data_gb > 5000 or qps > 50000:
            result['architecture_type'] = 'distributed'
            result['node_count'] = max(3, int(total_data_gb / 1000))
            result['shard_count'] = max(3, int(total_data_gb / 1000))
            result['confidence'] = 0.90
        elif total_data_gb > 1000 or qps > 10000:
            result['architecture_type'] = 'distributed'
            result['node_count'] = max(2, int(total_data_gb / 500))
            result['shard_count'] = max(2, int(total_data_gb / 500))
            result['confidence'] = 0.85
        elif total_data_gb > 100 or qps > 1000:
            result['architecture_type'] = 'hybrid'
            result['node_count'] = 2
            result['shard_count'] = 1
            result['confidence'] = 0.80
        
        # 副本数量
        if data.get('need_disaster_recovery', False):
            result['replica_count'] = 3
        elif data.get('need_high_availability', False):
            result['replica_count'] = 2
        
        # 应用业务规则
        result = self._apply_business_rules(data, result)
        
        return result
    
    def _extract_features(self, data):
        """从数据中提取特征向量"""
        features = np.zeros(50)
        
        # 数据量特征
        features[0] = data.get('total_data_size_gb', 0) / 10000  # 归一化
        features[1] = data.get('table_count', 0) / 1000
        features[2] = data.get('database_count', 0) / 100
        
        # 性能特征
        features[3] = data.get('qps', 0) / 100000
        features[4] = data.get('tps', 0) / 50000
        features[5] = data.get('concurrent_connections', 0) / 10000
        
        # 业务特征
        features[6] = 1 if data.get('need_high_availability', False) else 0
        features[7] = 1 if data.get('need_disaster_recovery', False) else 0
        features[8] = 1 if data.get('need_read_write_split', False) else 0
        
        # 数据库类型特征
        db_types = data.get('source_db_types', [])
        features[9] = 1 if 'MySQL' in db_types else 0
        features[10] = 1 if 'Oracle' in db_types else 0
        features[11] = 1 if 'PostgreSQL' in db_types else 0
        
        # 表大小分布
        features[12] = data.get('max_table_size_gb', 0) / 1000
        features[13] = data.get('avg_table_size_gb', 0) / 100
        
        # 增长率
        features[14] = data.get('data_growth_rate', 0) / 100
        
        return features
    
    def _apply_business_rules(self, data, prediction):
        """应用业务规则调整预测结果"""
        total_data_gb = data.get('total_data_size_gb', 0)
        qps = data.get('qps', 0)
        
        # 规则1: 大数据量强制使用分布式
        if total_data_gb > 5000:
            prediction['architecture_type'] = 'distributed'
            prediction['shard_count'] = max(prediction['shard_count'], 
                                           int(total_data_gb / 1000))
        
        # 规则2: 高并发强制使用分布式
        if qps > 50000:
            prediction['architecture_type'] = 'distributed'
            prediction['node_count'] = max(prediction['node_count'], 
                                          int(qps / 10000))
        
        # 规则3: 高可用要求至少2个副本
        if data.get('need_high_availability', False):
            prediction['replica_count'] = max(prediction['replica_count'], 2)
        
        # 规则4: 容灾要求至少3个副本
        if data.get('need_disaster_recovery', False):
            prediction['replica_count'] = max(prediction['replica_count'], 3)
        
        # 规则5: 小数据量使用单机
        if total_data_gb < 100 and qps < 1000:
            prediction['architecture_type'] = 'standalone'
            prediction['node_count'] = 1
            prediction['shard_count'] = 1
        
        return prediction
