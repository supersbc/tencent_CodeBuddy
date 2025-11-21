import math

class ArchitectureCalculator:
    """TDSQL 架构资源计算器"""
    
    def __init__(self):
        # 服务器配置模板
        self.server_specs = {
            'small': {'cpu': 8, 'memory_gb': 32, 'disk_gb': 1000, 'price': 5000},
            'medium': {'cpu': 16, 'memory_gb': 64, 'disk_gb': 2000, 'price': 10000},
            'large': {'cpu': 32, 'memory_gb': 128, 'disk_gb': 4000, 'price': 20000},
            'xlarge': {'cpu': 64, 'memory_gb': 256, 'disk_gb': 8000, 'price': 40000}
        }
        
        # 交换机配置
        self.switch_specs = {
            '48port_1g': {'ports': 48, 'speed': '1Gbps', 'price': 3000},
            '48port_10g': {'ports': 48, 'speed': '10Gbps', 'price': 15000},
            '32port_40g': {'ports': 32, 'speed': '40Gbps', 'price': 50000}
        }
    
    def calculate_resources(self, data, architecture):
        """计算所需资源"""
        total_data_gb = data.get('total_data_size_gb', 0)
        qps = data.get('qps', 0)
        replica_count = architecture.get('replica_count', 2)
        node_count = architecture.get('node_count', 1)
        shard_count = architecture.get('shard_count', 1)
        
        # 计算服务器配置
        servers = self._calculate_servers(
            total_data_gb, qps, node_count, shard_count, replica_count
        )
        
        # 计算交换机
        switches = self._calculate_switches(len(servers['database_servers']))
        
        # 计算存储
        storage = self._calculate_storage(total_data_gb, replica_count)
        
        # 计算网络带宽
        network = self._calculate_network(qps, total_data_gb)
        
        # 计算成本
        cost = self._calculate_cost(servers, switches, storage)
        
        return {
            'servers': servers,
            'switches': switches,
            'storage': storage,
            'network': network,
            'cost': cost,
            'summary': self._generate_summary(servers, switches, storage, cost)
        }
    
    def _calculate_servers(self, data_size_gb, qps, node_count, shard_count, replica_count):
        """计算服务器配置"""
        # 选择服务器规格
        if data_size_gb > 5000 or qps > 50000:
            db_spec = 'xlarge'
        elif data_size_gb > 2000 or qps > 20000:
            db_spec = 'large'
        elif data_size_gb > 500 or qps > 5000:
            db_spec = 'medium'
        else:
            db_spec = 'small'
        
        # 数据库服务器数量
        db_server_count = max(node_count, shard_count) * replica_count
        
        # 代理服务器（用于分布式架构）
        proxy_count = max(2, math.ceil(qps / 50000)) if node_count > 1 else 0
        
        # 管理服务器
        management_count = 2 if db_server_count > 3 else 1
        
        servers = {
            'database_servers': {
                'count': db_server_count,
                'spec': db_spec,
                'config': self.server_specs[db_spec],
                'role': 'TDSQL 数据节点',
                'details': f'{shard_count} 个分片 × {replica_count} 个副本'
            },
            'proxy_servers': {
                'count': proxy_count,
                'spec': 'medium',
                'config': self.server_specs['medium'],
                'role': 'TDSQL 代理节点',
                'details': '负载均衡和路由'
            } if proxy_count > 0 else None,
            'management_servers': {
                'count': management_count,
                'spec': 'small',
                'config': self.server_specs['small'],
                'role': '管理和监控节点',
                'details': 'ZooKeeper + 监控系统'
            }
        }
        
        # 移除 None 值
        servers = {k: v for k, v in servers.items() if v is not None}
        
        return servers
    
    def _calculate_switches(self, server_count):
        """计算交换机配置"""
        # 接入交换机（每48个端口一台）
        access_switch_count = math.ceil(server_count / 40)  # 留余量
        
        # 汇聚交换机（2台做冗余）
        aggregation_switch_count = 2 if server_count > 10 else 0
        
        # 核心交换机（2台做冗余）
        core_switch_count = 2 if server_count > 20 else 0
        
        switches = {
            'access_switches': {
                'count': access_switch_count,
                'spec': '48port_10g',
                'config': self.switch_specs['48port_10g'],
                'role': '接入交换机',
                'details': '连接服务器'
            },
            'aggregation_switches': {
                'count': aggregation_switch_count,
                'spec': '48port_10g',
                'config': self.switch_specs['48port_10g'],
                'role': '汇聚交换机',
                'details': '汇聚接入层流量'
            } if aggregation_switch_count > 0 else None,
            'core_switches': {
                'count': core_switch_count,
                'spec': '32port_40g',
                'config': self.switch_specs['32port_40g'],
                'role': '核心交换机',
                'details': '核心网络交换'
            } if core_switch_count > 0 else None
        }
        
        # 移除 None 值
        switches = {k: v for k, v in switches.items() if v is not None}
        
        return switches
    
    def _calculate_storage(self, data_size_gb, replica_count):
        """计算存储需求"""
        # 考虑副本和增长空间（预留50%）
        total_storage_gb = data_size_gb * replica_count * 1.5
        
        # 日志和备份空间（额外30%）
        total_storage_gb *= 1.3
        
        return {
            'total_capacity_gb': round(total_storage_gb, 2),
            'total_capacity_tb': round(total_storage_gb / 1024, 2),
            'raw_data_gb': data_size_gb,
            'replica_count': replica_count,
            'growth_reserve': '50%',
            'backup_space': '30%',
            'storage_type': 'SSD' if data_size_gb > 1000 else 'SSD/HDD混合',
            'raid_level': 'RAID 10（推荐）'
        }
    
    def _calculate_network(self, qps, data_size_gb):
        """计算网络带宽需求"""
        # 基于 QPS 估算带宽（假设每个请求平均 10KB）
        bandwidth_mbps = (qps * 10 * 8) / 1024  # 转换为 Mbps
        
        # 考虑峰值（3倍）
        peak_bandwidth_mbps = bandwidth_mbps * 3
        
        # 推荐带宽
        if peak_bandwidth_mbps > 8000:
            recommended = '10Gbps 或更高'
        elif peak_bandwidth_mbps > 800:
            recommended = '1Gbps - 10Gbps'
        else:
            recommended = '1Gbps'
        
        return {
            'average_bandwidth_mbps': round(bandwidth_mbps, 2),
            'peak_bandwidth_mbps': round(peak_bandwidth_mbps, 2),
            'recommended': recommended,
            'network_cards': '双万兆网卡（冗余）'
        }
    
    def _calculate_cost(self, servers, switches, storage):
        """计算成本估算"""
        total_cost = 0
        
        # 服务器成本
        for server_type, config in servers.items():
            count = config['count']
            price = config['config']['price']
            total_cost += count * price
        
        # 交换机成本
        for switch_type, config in switches.items():
            count = config['count']
            price = config['config']['price']
            total_cost += count * price
        
        # 存储成本（SSD: 2元/GB, HDD: 0.5元/GB）
        storage_gb = storage['total_capacity_gb']
        storage_cost = storage_gb * 2  # 假设使用 SSD
        total_cost += storage_cost
        
        return {
            'hardware_cost': round(total_cost, 2),
            'storage_cost': round(storage_cost, 2),
            'annual_maintenance': round(total_cost * 0.15, 2),  # 15% 维护费
            'total_first_year': round(total_cost * 1.15, 2),
            'currency': 'CNY'
        }
    
    def _generate_summary(self, servers, switches, storage, cost):
        """生成资源摘要"""
        total_servers = sum(s['count'] for s in servers.values())
        total_switches = sum(s['count'] for s in switches.values())
        
        return {
            'total_servers': total_servers,
            'total_switches': total_switches,
            'total_storage_tb': storage['total_capacity_tb'],
            'estimated_cost': cost['total_first_year'],
            'deployment_time': f'{total_servers * 2} 小时（估算）'
        }
