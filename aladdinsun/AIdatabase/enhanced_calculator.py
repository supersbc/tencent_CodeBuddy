"""
增强的架构资源计算器
提供详细的设备清单和成本明细
"""

import math

class EnhancedArchitectureCalculator:
    """增强的TDSQL架构资源计算器"""
    
    def __init__(self):
        # 服务器配置和价格（单位：元）
        self.server_specs = {
            'small': {
                'cpu': 8, 'memory_gb': 32, 'disk_gb': 1000,
                'model': 'Dell PowerEdge R440',
                'price': 28000,
                'power_w': 350
            },
            'medium': {
                'cpu': 16, 'memory_gb': 64, 'disk_gb': 2000,
                'model': 'Dell PowerEdge R640',
                'price': 45000,
                'power_w': 500
            },
            'large': {
                'cpu': 32, 'memory_gb': 128, 'disk_gb': 4000,
                'model': 'Dell PowerEdge R740',
                'price': 85000,
                'power_w': 750
            },
            'xlarge': {
                'cpu': 64, 'memory_gb': 256, 'disk_gb': 8000,
                'model': 'Dell PowerEdge R940',
                'price': 180000,
                'power_w': 1200
            }
        }
        
        # 交换机配置和价格
        self.switch_specs = {
            '48port_1g': {
                'ports': 48, 'speed': '1Gbps',
                'model': 'Cisco Catalyst 2960-X',
                'price': 12000,
                'power_w': 100
            },
            '48port_10g': {
                'ports': 48, 'speed': '10Gbps',
                'model': 'Cisco Nexus 93180YC-FX',
                'price': 85000,
                'power_w': 250
            },
            '32port_40g': {
                'ports': 32, 'speed': '40Gbps',
                'model': 'Cisco Nexus 9336C-FX2',
                'price': 280000,
                'power_w': 400
            }
        }
        
        # 存储设备
        self.storage_specs = {
            'ssd_sata': {'price_per_tb': 1200, 'iops': 50000, 'type': 'SATA SSD'},
            'ssd_nvme': {'price_per_tb': 2500, 'iops': 500000, 'type': 'NVMe SSD'},
            'hdd': {'price_per_tb': 300, 'iops': 150, 'type': 'SATA HDD'}
        }
        
        # 网络设备
        self.network_devices = {
            'firewall': {'model': 'Fortinet FortiGate 600E', 'price': 120000},
            'load_balancer': {'model': 'F5 BIG-IP 4200v', 'price': 150000},
            'router': {'model': 'Cisco ASR 1001-X', 'price': 80000}
        }
        
        # 软件许可证
        self.software_licenses = {
            'tdsql_enterprise': {'price_per_core': 3000, 'annual_maintenance': 0.2},
            'os_redhat': {'price_per_server': 5000, 'annual_maintenance': 0.15},
            'monitoring': {'price_per_node': 2000, 'annual_maintenance': 0.1}
        }
        
        # 其他成本
        self.other_costs = {
            'rack': {'price': 8000, 'capacity': 42},  # 42U机柜
            'pdu': {'price': 3000},  # 电源分配单元
            'ups': {'price_per_kw': 5000},  # UPS不间断电源
            'cable': {'price_per_server': 500},  # 网线等
            'deployment_per_server': 2000,  # 部署实施费用
            'training': 50000,  # 培训费用
            'annual_power_per_kw': 5000,  # 年电费
            'annual_cooling_ratio': 0.4  # 制冷成本占电费比例
        }
    
    def calculate_resources(self, data, architecture):
        """计算所需资源（增强版）"""
        total_data_gb = data.get('total_data_size_gb', 0)
        qps = data.get('qps', 0)
        tps = data.get('tps', 0)
        peak_qps = data.get('peak_qps', qps * 1.5)
        concurrent_connections = data.get('concurrent_connections', 1000)
        replica_count = architecture.get('replica_count', 2)
        node_count = architecture.get('node_count', 1)
        shard_count = architecture.get('shard_count', 1)
        
        # 计算服务器配置
        servers = self._calculate_servers_detailed(
            total_data_gb, qps, tps, peak_qps, concurrent_connections,
            node_count, shard_count, replica_count
        )
        
        # 计算网络设备
        network = self._calculate_network_detailed(servers, qps)
        
        # 计算存储
        storage = self._calculate_storage_detailed(total_data_gb, replica_count, qps)
        
        # 计算机柜和配套
        infrastructure = self._calculate_infrastructure(servers, network)
        
        # 计算软件许可
        software = self._calculate_software_licenses(servers)
        
        # 计算详细成本
        cost = self._calculate_cost_detailed(servers, network, storage, infrastructure, software)
        
        return {
            'servers': servers,
            'network': network,
            'storage': storage,
            'infrastructure': infrastructure,
            'software': software,
            'cost': cost,
            'summary': self._generate_summary(servers, network, storage, cost)
        }
    
    def _calculate_servers_detailed(self, data_size_gb, qps, tps, peak_qps, connections, 
                                    node_count, shard_count, replica_count):
        """计算详细的服务器配置"""
        
        # 选择数据库服务器规格
        if data_size_gb > 10000 or peak_qps > 100000:
            db_spec = 'xlarge'
        elif data_size_gb > 3000 or peak_qps > 30000:
            db_spec = 'large'
        elif data_size_gb > 500 or peak_qps > 5000:
            db_spec = 'medium'
        else:
            db_spec = 'small'
        
        # 数据库服务器数量
        db_server_count = max(node_count, shard_count) * replica_count
        
        # 代理服务器（用于分布式架构）
        if node_count > 1:
            proxy_count = max(2, math.ceil(peak_qps / 50000))
            proxy_spec = 'large' if peak_qps > 100000 else 'medium'
        else:
            proxy_count = 0
            proxy_spec = None
        
        # 管理服务器（ZooKeeper + 监控）
        if db_server_count > 10:
            mgmt_count = 5
            mgmt_spec = 'large'
        elif db_server_count > 3:
            mgmt_count = 3
            mgmt_spec = 'medium'
        else:
            mgmt_count = 1
            mgmt_spec = 'small'
        
        # 备份服务器
        backup_count = max(1, math.ceil(db_server_count / 10))
        backup_spec = db_spec
        
        servers = {
            'database_servers': {
                'count': db_server_count,
                'spec': db_spec,
                'config': self.server_specs[db_spec],
                'role': 'TDSQL数据节点',
                'details': f'{shard_count}分片 × {replica_count}副本',
                'unit_price': self.server_specs[db_spec]['price'],
                'total_price': self.server_specs[db_spec]['price'] * db_server_count,
                'total_cpu': self.server_specs[db_spec]['cpu'] * db_server_count,
                'total_memory_gb': self.server_specs[db_spec]['memory_gb'] * db_server_count,
                'total_disk_gb': self.server_specs[db_spec]['disk_gb'] * db_server_count,
                'total_power_w': self.server_specs[db_spec]['power_w'] * db_server_count
            }
        }
        
        if proxy_count > 0:
            servers['proxy_servers'] = {
                'count': proxy_count,
                'spec': proxy_spec,
                'config': self.server_specs[proxy_spec],
                'role': 'TDSQL代理节点',
                'details': '负载均衡和SQL路由',
                'unit_price': self.server_specs[proxy_spec]['price'],
                'total_price': self.server_specs[proxy_spec]['price'] * proxy_count,
                'total_cpu': self.server_specs[proxy_spec]['cpu'] * proxy_count,
                'total_memory_gb': self.server_specs[proxy_spec]['memory_gb'] * proxy_count,
                'total_disk_gb': self.server_specs[proxy_spec]['disk_gb'] * proxy_count,
                'total_power_w': self.server_specs[proxy_spec]['power_w'] * proxy_count
            }
        
        servers['management_servers'] = {
            'count': mgmt_count,
            'spec': mgmt_spec,
            'config': self.server_specs[mgmt_spec],
            'role': '管理监控节点',
            'details': 'ZooKeeper集群 + Prometheus监控',
            'unit_price': self.server_specs[mgmt_spec]['price'],
            'total_price': self.server_specs[mgmt_spec]['price'] * mgmt_count,
            'total_cpu': self.server_specs[mgmt_spec]['cpu'] * mgmt_count,
            'total_memory_gb': self.server_specs[mgmt_spec]['memory_gb'] * mgmt_count,
            'total_disk_gb': self.server_specs[mgmt_spec]['disk_gb'] * mgmt_count,
            'total_power_w': self.server_specs[mgmt_spec]['power_w'] * mgmt_count
        }
        
        servers['backup_servers'] = {
            'count': backup_count,
            'spec': backup_spec,
            'config': self.server_specs[backup_spec],
            'role': '备份服务器',
            'details': '全量备份 + 增量备份',
            'unit_price': self.server_specs[backup_spec]['price'],
            'total_price': self.server_specs[backup_spec]['price'] * backup_count,
            'total_cpu': self.server_specs[backup_spec]['cpu'] * backup_count,
            'total_memory_gb': self.server_specs[backup_spec]['memory_gb'] * backup_count,
            'total_disk_gb': self.server_specs[backup_spec]['disk_gb'] * backup_count,
            'total_power_w': self.server_specs[backup_spec]['power_w'] * backup_count
        }
        
        return servers
    
    def _calculate_network_detailed(self, servers, qps):
        """计算详细的网络设备"""
        
        # 计算总服务器数量
        total_servers = sum(s['count'] for s in servers.values() if s)
        
        # 选择交换机类型
        if qps > 100000:
            switch_type = '32port_40g'
            switches_needed = math.ceil(total_servers / 24)  # 40G交换机留余量
        elif qps > 20000:
            switch_type = '48port_10g'
            switches_needed = math.ceil(total_servers / 40)
        else:
            switch_type = '48port_1g'
            switches_needed = math.ceil(total_servers / 44)
        
        # 核心交换机（冗余）
        core_switches = 2 if switches_needed > 1 else 1
        
        network = {
            'access_switches': {
                'count': switches_needed,
                'type': switch_type,
                'config': self.switch_specs[switch_type],
                'role': '接入交换机',
                'details': f'连接{total_servers}台服务器',
                'unit_price': self.switch_specs[switch_type]['price'],
                'total_price': self.switch_specs[switch_type]['price'] * switches_needed,
                'total_power_w': self.switch_specs[switch_type]['power_w'] * switches_needed
            },
            'core_switches': {
                'count': core_switches,
                'type': switch_type,
                'config': self.switch_specs[switch_type],
                'role': '核心交换机',
                'details': '核心网络冗余',
                'unit_price': self.switch_specs[switch_type]['price'],
                'total_price': self.switch_specs[switch_type]['price'] * core_switches,
                'total_power_w': self.switch_specs[switch_type]['power_w'] * core_switches
            },
            'firewall': {
                'count': 2,
                'config': self.network_devices['firewall'],
                'role': '防火墙',
                'details': '主备防火墙',
                'unit_price': self.network_devices['firewall']['price'],
                'total_price': self.network_devices['firewall']['price'] * 2
            },
            'load_balancer': {
                'count': 2 if qps > 10000 else 1,
                'config': self.network_devices['load_balancer'],
                'role': '负载均衡器',
                'details': '应用层负载均衡',
                'unit_price': self.network_devices['load_balancer']['price'],
                'total_price': self.network_devices['load_balancer']['price'] * (2 if qps > 10000 else 1)
            }
        }
        
        return network
    
    def _calculate_storage_detailed(self, data_size_gb, replica_count, qps):
        """计算详细的存储配置"""
        
        # 计算总存储需求（数据 + 副本 + 备份 + 日志 + 余量）
        data_storage_gb = data_size_gb * replica_count
        backup_storage_gb = data_size_gb * 2  # 全量 + 增量备份
        log_storage_gb = data_size_gb * 0.2  # 日志空间
        buffer_ratio = 1.3  # 30%余量
        
        total_storage_gb = (data_storage_gb + backup_storage_gb + log_storage_gb) * buffer_ratio
        
        # 选择存储类型
        if qps > 50000:
            storage_type = 'ssd_nvme'
        elif qps > 5000:
            storage_type = 'ssd_sata'
        else:
            storage_type = 'hdd'
        
        storage_tb = math.ceil(total_storage_gb / 1024)
        
        storage = {
            'primary_storage': {
                'capacity_tb': math.ceil(data_storage_gb / 1024),
                'type': storage_type,
                'config': self.storage_specs[storage_type],
                'role': '主存储',
                'details': f'{replica_count}副本数据存储',
                'price_per_tb': self.storage_specs[storage_type]['price_per_tb'],
                'total_price': self.storage_specs[storage_type]['price_per_tb'] * math.ceil(data_storage_gb / 1024)
            },
            'backup_storage': {
                'capacity_tb': math.ceil(backup_storage_gb / 1024),
                'type': 'hdd',
                'config': self.storage_specs['hdd'],
                'role': '备份存储',
                'details': '全量备份 + 增量备份',
                'price_per_tb': self.storage_specs['hdd']['price_per_tb'],
                'total_price': self.storage_specs['hdd']['price_per_tb'] * math.ceil(backup_storage_gb / 1024)
            },
            'log_storage': {
                'capacity_tb': math.ceil(log_storage_gb / 1024),
                'type': 'ssd_sata',
                'config': self.storage_specs['ssd_sata'],
                'role': '日志存储',
                'details': 'binlog + redo log',
                'price_per_tb': self.storage_specs['ssd_sata']['price_per_tb'],
                'total_price': self.storage_specs['ssd_sata']['price_per_tb'] * math.ceil(log_storage_gb / 1024)
            },
            'total_capacity_tb': storage_tb,
            'total_price': (
                self.storage_specs[storage_type]['price_per_tb'] * math.ceil(data_storage_gb / 1024) +
                self.storage_specs['hdd']['price_per_tb'] * math.ceil(backup_storage_gb / 1024) +
                self.storage_specs['ssd_sata']['price_per_tb'] * math.ceil(log_storage_gb / 1024)
            )
        }
        
        return storage
    
    def _calculate_infrastructure(self, servers, network):
        """计算基础设施（机柜、PDU、UPS等）"""
        
        total_servers = sum(s['count'] for s in servers.values() if s)
        total_switches = sum(n['count'] for n in network.values() if n and 'count' in n)
        
        # 计算机柜数量（每个机柜42U，服务器2U，交换机1U）
        total_u = total_servers * 2 + total_switches * 1
        rack_count = math.ceil(total_u / 42)
        
        # 计算总功率
        total_power_w = sum(s.get('total_power_w', 0) for s in servers.values() if s)
        total_power_w += sum(n.get('total_power_w', 0) for n in network.values() if n)
        total_power_kw = math.ceil(total_power_w / 1000)
        
        infrastructure = {
            'racks': {
                'count': rack_count,
                'capacity_u': 42,
                'unit_price': self.other_costs['rack']['price'],
                'total_price': self.other_costs['rack']['price'] * rack_count,
                'details': f'标准42U机柜，共{total_u}U设备'
            },
            'pdu': {
                'count': rack_count * 2,  # 每个机柜2个PDU
                'unit_price': self.other_costs['pdu']['price'],
                'total_price': self.other_costs['pdu']['price'] * rack_count * 2,
                'details': '电源分配单元，双路供电'
            },
            'ups': {
                'capacity_kw': total_power_kw * 1.5,  # 1.5倍余量
                'unit_price': self.other_costs['ups']['price_per_kw'],
                'total_price': self.other_costs['ups']['price_per_kw'] * total_power_kw * 1.5,
                'details': f'{total_power_kw * 1.5}KW UPS不间断电源'
            },
            'cables': {
                'count': total_servers + total_switches,
                'unit_price': self.other_costs['cable']['price_per_server'],
                'total_price': self.other_costs['cable']['price_per_server'] * (total_servers + total_switches),
                'details': '网线、电源线等'
            },
            'total_power_kw': total_power_kw,
            'total_price': (
                self.other_costs['rack']['price'] * rack_count +
                self.other_costs['pdu']['price'] * rack_count * 2 +
                self.other_costs['ups']['price_per_kw'] * total_power_kw * 1.5 +
                self.other_costs['cable']['price_per_server'] * (total_servers + total_switches)
            )
        }
        
        return infrastructure
    
    def _calculate_software_licenses(self, servers):
        """计算软件许可证费用"""
        
        total_servers = sum(s['count'] for s in servers.values() if s)
        total_cpu = sum(s.get('total_cpu', 0) for s in servers.values() if s)
        db_nodes = servers['database_servers']['count']
        
        software = {
            'tdsql_license': {
                'cores': total_cpu,
                'price_per_core': self.software_licenses['tdsql_enterprise']['price_per_core'],
                'total_price': self.software_licenses['tdsql_enterprise']['price_per_core'] * total_cpu,
                'annual_maintenance': self.software_licenses['tdsql_enterprise']['price_per_core'] * total_cpu * 0.2,
                'details': 'TDSQL企业版许可证'
            },
            'os_license': {
                'servers': total_servers,
                'price_per_server': self.software_licenses['os_redhat']['price_per_server'],
                'total_price': self.software_licenses['os_redhat']['price_per_server'] * total_servers,
                'annual_maintenance': self.software_licenses['os_redhat']['price_per_server'] * total_servers * 0.15,
                'details': 'Red Hat Enterprise Linux'
            },
            'monitoring_license': {
                'nodes': db_nodes,
                'price_per_node': self.software_licenses['monitoring']['price_per_node'],
                'total_price': self.software_licenses['monitoring']['price_per_node'] * db_nodes,
                'annual_maintenance': self.software_licenses['monitoring']['price_per_node'] * db_nodes * 0.1,
                'details': 'Prometheus + Grafana企业版'
            },
            'total_price': (
                self.software_licenses['tdsql_enterprise']['price_per_core'] * total_cpu +
                self.software_licenses['os_redhat']['price_per_server'] * total_servers +
                self.software_licenses['monitoring']['price_per_node'] * db_nodes
            ),
            'total_annual_maintenance': (
                self.software_licenses['tdsql_enterprise']['price_per_core'] * total_cpu * 0.2 +
                self.software_licenses['os_redhat']['price_per_server'] * total_servers * 0.15 +
                self.software_licenses['monitoring']['price_per_node'] * db_nodes * 0.1
            )
        }
        
        return software
    
    def _calculate_cost_detailed(self, servers, network, storage, infrastructure, software):
        """计算详细成本"""
        
        # 硬件成本
        hardware_cost = {
            'servers': sum(s.get('total_price', 0) for s in servers.values() if s),
            'network': sum(n.get('total_price', 0) for n in network.values() if n),
            'storage': storage['total_price'],
            'infrastructure': infrastructure['total_price'],
            'subtotal': 0
        }
        hardware_cost['subtotal'] = sum(hardware_cost.values())
        
        # 软件成本
        software_cost = {
            'licenses': software['total_price'],
            'subtotal': software['total_price']
        }
        
        # 实施成本
        total_servers = sum(s['count'] for s in servers.values() if s)
        deployment_cost = {
            'deployment': self.other_costs['deployment_per_server'] * total_servers,
            'training': self.other_costs['training'],
            'subtotal': self.other_costs['deployment_per_server'] * total_servers + self.other_costs['training']
        }
        
        # 年度运维成本
        total_power_kw = infrastructure['total_power_kw']
        annual_operation_cost = {
            'software_maintenance': software['total_annual_maintenance'],
            'power': self.other_costs['annual_power_per_kw'] * total_power_kw,
            'cooling': self.other_costs['annual_power_per_kw'] * total_power_kw * self.other_costs['annual_cooling_ratio'],
            'personnel': 200000,  # 2名DBA年薪
            'subtotal': 0
        }
        annual_operation_cost['subtotal'] = sum(annual_operation_cost.values())
        
        # 总成本
        total_cost = {
            'hardware': hardware_cost['subtotal'],
            'software': software_cost['subtotal'],
            'deployment': deployment_cost['subtotal'],
            'first_year_operation': annual_operation_cost['subtotal'],
            'total_first_year': (
                hardware_cost['subtotal'] +
                software_cost['subtotal'] +
                deployment_cost['subtotal'] +
                annual_operation_cost['subtotal']
            ),
            'annual_operation': annual_operation_cost['subtotal']
        }
        
        return {
            'hardware': hardware_cost,
            'software': software_cost,
            'deployment': deployment_cost,
            'annual_operation': annual_operation_cost,
            'total': total_cost,
            'breakdown': {
                '硬件成本': hardware_cost,
                '软件成本': software_cost,
                '实施成本': deployment_cost,
                '年度运维成本': annual_operation_cost
            }
        }
    
    def _generate_summary(self, servers, network, storage, cost):
        """生成摘要"""
        total_servers = sum(s['count'] for s in servers.values() if s)
        total_cpu = sum(s.get('total_cpu', 0) for s in servers.values() if s)
        total_memory_gb = sum(s.get('total_memory_gb', 0) for s in servers.values() if s)
        
        return {
            'total_servers': total_servers,
            'total_cpu_cores': total_cpu,
            'total_memory_gb': total_memory_gb,
            'total_storage_tb': storage['total_capacity_tb'],
            'total_cost': cost['total']['total_first_year'],
            'deployment_time': f"{math.ceil(total_servers / 5)}-{math.ceil(total_servers / 3)}周"
        }

if __name__ == '__main__':
    # 测试
    calculator = EnhancedArchitectureCalculator()
    
    test_data = {
        'total_data_size_gb': 5000,
        'qps': 40000,
        'tps': 15000,
        'peak_qps': 60000,
        'concurrent_connections': 8000
    }
    
    test_arch = {
        'architecture_type': 'distributed',
        'node_count': 8,
        'shard_count': 8,
        'replica_count': 2
    }
    
    result = calculator.calculate_resources(test_data, test_arch)
    
    print("服务器清单:")
    for name, server in result['servers'].items():
        if server:
            print(f"  {name}: {server['count']}台 {server['config']['model']}")
    
    print(f"\n总成本: ¥{result['cost']['total']['total_first_year']:,}")
