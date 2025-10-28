"""
TDSQL 部署资源预测系统 - 核心计算引擎
生成详细的架构设计、设备清单、成本清单和架构图
"""

import math
import json
from datetime import datetime

class DeploymentResourcePredictor:
    """部署资源预测器"""
    
    def __init__(self):
        # 服务器配置库
        self.server_catalog = {
            'db_small': {
                'name': 'Dell PowerEdge R440',
                'cpu_cores': 8, 'cpu_model': 'Intel Xeon Silver 4208',
                'memory_gb': 32, 'disk_gb': 1000, 'disk_type': 'SSD SATA',
                'network': '双万兆网卡',
                'price': 28000, 'power_w': 350,
                'use_case': '小型数据库节点'
            },
            'db_medium': {
                'name': 'Dell PowerEdge R640',
                'cpu_cores': 16, 'cpu_model': 'Intel Xeon Gold 5218',
                'memory_gb': 64, 'disk_gb': 2000, 'disk_type': 'SSD SATA',
                'network': '双万兆网卡',
                'price': 45000, 'power_w': 500,
                'use_case': '中型数据库节点'
            },
            'db_large': {
                'name': 'Dell PowerEdge R740',
                'cpu_cores': 32, 'cpu_model': 'Intel Xeon Gold 6248',
                'memory_gb': 128, 'disk_gb': 4000, 'disk_type': 'NVMe SSD',
                'network': '双万兆网卡',
                'price': 85000, 'power_w': 750,
                'use_case': '大型数据库节点'
            },
            'db_xlarge': {
                'name': 'Dell PowerEdge R940',
                'cpu_cores': 64, 'cpu_model': 'Intel Xeon Platinum 8280',
                'memory_gb': 256, 'disk_gb': 8000, 'disk_type': 'NVMe SSD',
                'network': '双万兆网卡',
                'price': 180000, 'power_w': 1200,
                'use_case': '超大型数据库节点'
            },
            'app_server': {
                'name': 'Dell PowerEdge R340',
                'cpu_cores': 4, 'cpu_model': 'Intel Xeon E-2234',
                'memory_gb': 16, 'disk_gb': 500, 'disk_type': 'SSD SATA',
                'network': '双千兆网卡',
                'price': 18000, 'power_w': 250,
                'use_case': '应用服务器'
            },
            'proxy_server': {
                'name': 'Dell PowerEdge R340',
                'cpu_cores': 8, 'cpu_model': 'Intel Xeon E-2278G',
                'memory_gb': 32, 'disk_gb': 500, 'disk_type': 'SSD SATA',
                'network': '双万兆网卡',
                'price': 22000, 'power_w': 300,
                'use_case': 'TDSQL代理节点'
            },
            'monitor_server': {
                'name': 'Dell PowerEdge R340',
                'cpu_cores': 4, 'cpu_model': 'Intel Xeon E-2234',
                'memory_gb': 16, 'disk_gb': 1000, 'disk_type': 'SSD SATA',
                'network': '双千兆网卡',
                'price': 20000, 'power_w': 250,
                'use_case': '监控服务器'
            }
        }
        
        # 网络设备配置库
        self.network_catalog = {
            'core_switch_10g': {
                'name': 'Cisco Nexus 93180YC-FX',
                'type': '核心交换机',
                'ports': 48, 'speed': '10Gbps',
                'uplink': '6x40Gbps',
                'price': 85000, 'power_w': 250
            },
            'core_switch_40g': {
                'name': 'Cisco Nexus 9336C-FX2',
                'type': '核心交换机',
                'ports': 36, 'speed': '40Gbps',
                'uplink': '100Gbps',
                'price': 280000, 'power_w': 400
            },
            'access_switch_1g': {
                'name': 'Cisco Catalyst 2960-X',
                'type': '接入交换机',
                'ports': 48, 'speed': '1Gbps',
                'uplink': '4x10Gbps',
                'price': 12000, 'power_w': 100
            },
            'access_switch_10g': {
                'name': 'Cisco Catalyst 9300',
                'type': '接入交换机',
                'ports': 48, 'speed': '10Gbps',
                'uplink': '8x40Gbps',
                'price': 45000, 'power_w': 200
            },
            'firewall': {
                'name': 'Fortinet FortiGate 600E',
                'type': '防火墙',
                'throughput': '10Gbps',
                'price': 120000, 'power_w': 150
            },
            'load_balancer': {
                'name': 'F5 BIG-IP 4200v',
                'type': '负载均衡器',
                'throughput': '20Gbps',
                'price': 150000, 'power_w': 200
            },
            'router': {
                'name': 'Cisco ASR 1001-X',
                'type': '路由器',
                'throughput': '20Gbps',
                'price': 80000, 'power_w': 180
            }
        }
        
        # 存储设备
        self.storage_catalog = {
            'ssd_sata': {
                'type': 'SATA SSD',
                'model': 'Samsung 870 EVO',
                'price_per_tb': 1200,
                'iops': 50000,
                'throughput_mbps': 550
            },
            'ssd_nvme': {
                'type': 'NVMe SSD',
                'model': 'Samsung 980 PRO',
                'price_per_tb': 2500,
                'iops': 500000,
                'throughput_mbps': 7000
            },
            'hdd': {
                'type': 'SATA HDD',
                'model': 'Seagate Exos X16',
                'price_per_tb': 300,
                'iops': 150,
                'throughput_mbps': 250
            }
        }
        
        # 软件许可证
        self.software_licenses = {
            'tdsql_enterprise': {
                'name': 'TDSQL企业版',
                'price_per_core': 3000,
                'annual_maintenance_rate': 0.20
            },
            'os_redhat': {
                'name': 'Red Hat Enterprise Linux',
                'price_per_server': 5000,
                'annual_maintenance_rate': 0.15
            },
            'monitoring_prometheus': {
                'name': 'Prometheus监控套件',
                'price_per_node': 2000,
                'annual_maintenance_rate': 0.10
            },
            'backup_software': {
                'name': '备份软件',
                'price_per_tb': 500,
                'annual_maintenance_rate': 0.15
            }
        }
        
        # 其他成本
        self.infrastructure_costs = {
            'rack_42u': {'name': '42U标准机柜', 'price': 8000, 'capacity': 42},
            'pdu': {'name': '电源分配单元(PDU)', 'price': 3000},
            'ups_per_kw': {'name': 'UPS不间断电源', 'price_per_kw': 5000},
            'cable_per_server': {'name': '网线及配件', 'price': 500},
            'deployment_per_server': {'name': '部署实施费用', 'price': 2000},
            'training': {'name': '技术培训', 'price': 50000},
            'annual_power_per_kw': {'name': '年电费', 'price': 5000},
            'annual_cooling_ratio': {'name': '制冷成本比例', 'ratio': 0.4}
        }
    
    def predict(self, input_data):
        """
        主预测函数
        返回完整的部署资源预测结果
        """
        # 1. 分析输入参数
        analysis = self._analyze_requirements(input_data)
        
        # 2. 设计架构
        architecture = self._design_architecture(analysis)
        
        # 3. 计算设备清单
        equipment_list = self._calculate_equipment(architecture, analysis)
        
        # 4. 计算成本
        cost_breakdown = self._calculate_costs(equipment_list, architecture)
        
        # 5. 生成网络拓扑
        network_topology = self._design_network_topology(architecture, equipment_list)
        
        # 6. 生成架构图数据
        architecture_diagram = self._generate_architecture_diagram(architecture, equipment_list)
        
        # 7. 生成部署建议
        recommendations = self._generate_recommendations(analysis, architecture)
        
        return {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'input_summary': analysis['summary'],
            'architecture': architecture,
            'equipment_list': equipment_list,
            'network_topology': network_topology,
            'cost_breakdown': cost_breakdown,
            'architecture_diagram': architecture_diagram,
            'recommendations': recommendations,
            'metadata': {
                'version': '4.0',
                'calculation_time': datetime.now().isoformat()
            }
        }
    
    def _analyze_requirements(self, data):
        """分析业务需求"""
        # 提取关键参数
        qps = data.get('qps', 1000)
        tps = data.get('tps', qps * 0.3)
        data_size_gb = data.get('data_volume', 100)
        concurrent_users = data.get('concurrent_users', 100)
        ha_level = data.get('ha_level', 'high')
        industry = data.get('industry', 'general')
        
        # 计算峰值
        peak_qps = qps * 1.5
        peak_tps = tps * 1.5
        
        # 数据增长预测（3年）
        growth_rate = data.get('data_growth_rate', 0.3)
        projected_data_gb = data_size_gb * ((1 + growth_rate) ** 3)
        
        # 确定规模等级
        if qps < 1000 and data_size_gb < 100:
            scale = 'small'
        elif qps < 5000 and data_size_gb < 1000:
            scale = 'medium'
        elif qps < 20000 and data_size_gb < 10000:
            scale = 'large'
        else:
            scale = 'xlarge'
        
        return {
            'summary': {
                'scale': scale,
                'qps': qps,
                'peak_qps': peak_qps,
                'tps': tps,
                'peak_tps': peak_tps,
                'current_data_gb': data_size_gb,
                'projected_data_gb': projected_data_gb,
                'concurrent_users': concurrent_users,
                'ha_level': ha_level,
                'industry': industry
            },
            'requirements': {
                'cpu_cores_needed': self._estimate_cpu_cores(qps, tps),
                'memory_gb_needed': self._estimate_memory(data_size_gb, qps),
                'storage_gb_needed': projected_data_gb * 3,  # 数据+备份+日志
                'network_bandwidth_gbps': self._estimate_bandwidth(qps),
                'iops_needed': self._estimate_iops(tps)
            }
        }
    
    def _estimate_cpu_cores(self, qps, tps):
        """估算CPU核心数"""
        # 经验公式：每1000 QPS需要4核，每1000 TPS需要8核
        cores_for_qps = (qps / 1000) * 4
        cores_for_tps = (tps / 1000) * 8
        return math.ceil(max(cores_for_qps, cores_for_tps))
    
    def _estimate_memory(self, data_size_gb, qps):
        """估算内存需求"""
        # 经验公式：数据大小的20% + 每1000 QPS需要4GB
        memory_for_data = data_size_gb * 0.2
        memory_for_qps = (qps / 1000) * 4
        return math.ceil(memory_for_data + memory_for_qps)
    
    def _estimate_bandwidth(self, qps):
        """估算网络带宽（Gbps）"""
        # 假设每个请求平均10KB
        bandwidth_mbps = (qps * 10 * 8) / 1000  # Mbps
        bandwidth_gbps = bandwidth_mbps / 1000
        return max(1, math.ceil(bandwidth_gbps))
    
    def _estimate_iops(self, tps):
        """估算IOPS需求"""
        # 每个事务平均需要10次IO操作
        return tps * 10
    
    def _design_architecture(self, analysis):
        """设计系统架构"""
        scale = analysis['summary']['scale']
        ha_level = analysis['summary']['ha_level']
        
        # 根据规模确定架构类型
        if scale == 'small':
            arch_type = 'single_master_slave'
            shard_count = 1
            replica_count = 2 if ha_level == 'high' else 1
        elif scale == 'medium':
            arch_type = 'sharded'
            shard_count = 2
            replica_count = 2
        elif scale == 'large':
            arch_type = 'sharded'
            shard_count = 4
            replica_count = 3
        else:  # xlarge
            arch_type = 'sharded'
            shard_count = 8
            replica_count = 3
        
        # 计算节点数量
        db_nodes = shard_count * (1 + replica_count)  # 主节点 + 从节点
        proxy_nodes = max(2, shard_count)  # 代理节点
        app_nodes = max(2, math.ceil(analysis['summary']['qps'] / 5000))  # 应用节点
        
        return {
            'type': arch_type,
            'description': self._get_arch_description(arch_type),
            'topology': {
                'shard_count': shard_count,
                'replica_count': replica_count,
                'db_nodes': db_nodes,
                'proxy_nodes': proxy_nodes,
                'app_nodes': app_nodes,
                'monitor_nodes': 1,
                'backup_nodes': 1
            },
            'ha_config': {
                'level': ha_level,
                'auto_failover': True,
                'backup_strategy': 'full_daily_incremental_hourly',
                'disaster_recovery': ha_level == 'high'
            },
            'network_zones': {
                'dmz': ['load_balancer', 'firewall'],
                'app_zone': ['app_servers', 'proxy_servers'],
                'db_zone': ['db_servers'],
                'management_zone': ['monitor_server', 'backup_server']
            }
        }
    
    def _get_arch_description(self, arch_type):
        """获取架构描述"""
        descriptions = {
            'single_master_slave': '单主从架构 - 适用于小型应用，一主一从或一主多从',
            'sharded': '分片集群架构 - 适用于大规模应用，支持水平扩展',
            'distributed': '分布式集群架构 - 适用于超大规模应用，多地多活'
        }
        return descriptions.get(arch_type, '标准架构')
    
    def _calculate_equipment(self, architecture, analysis):
        """计算设备清单"""
        scale = analysis['summary']['scale']
        topology = architecture['topology']
        
        # 选择合适的服务器规格
        if scale == 'small':
            db_spec = 'db_small'
        elif scale == 'medium':
            db_spec = 'db_medium'
        elif scale == 'large':
            db_spec = 'db_large'
        else:
            db_spec = 'db_xlarge'
        
        equipment = {
            'servers': [],
            'network_devices': [],
            'storage': [],
            'infrastructure': []
        }
        
        # 数据库服务器
        db_server = self.server_catalog[db_spec]
        for i in range(topology['db_nodes']):
            shard_id = i // (topology['replica_count'] + 1)
            role = 'master' if i % (topology['replica_count'] + 1) == 0 else 'slave'
            equipment['servers'].append({
                'id': f'db-{i+1:02d}',
                'role': f'数据库节点 (Shard-{shard_id+1} {role.upper()})',
                'model': db_server['name'],
                'cpu': f"{db_server['cpu_cores']}核 {db_server['cpu_model']}",
                'memory': f"{db_server['memory_gb']}GB",
                'disk': f"{db_server['disk_gb']}GB {db_server['disk_type']}",
                'network': db_server['network'],
                'quantity': 1,
                'unit_price': db_server['price'],
                'total_price': db_server['price'],
                'power_w': db_server['power_w']
            })
        
        # 代理服务器
        proxy_server = self.server_catalog['proxy_server']
        for i in range(topology['proxy_nodes']):
            equipment['servers'].append({
                'id': f'proxy-{i+1:02d}',
                'role': 'TDSQL代理节点',
                'model': proxy_server['name'],
                'cpu': f"{proxy_server['cpu_cores']}核 {proxy_server['cpu_model']}",
                'memory': f"{proxy_server['memory_gb']}GB",
                'disk': f"{proxy_server['disk_gb']}GB {proxy_server['disk_type']}",
                'network': proxy_server['network'],
                'quantity': 1,
                'unit_price': proxy_server['price'],
                'total_price': proxy_server['price'],
                'power_w': proxy_server['power_w']
            })
        
        # 应用服务器
        app_server = self.server_catalog['app_server']
        for i in range(topology['app_nodes']):
            equipment['servers'].append({
                'id': f'app-{i+1:02d}',
                'role': '应用服务器',
                'model': app_server['name'],
                'cpu': f"{app_server['cpu_cores']}核 {app_server['cpu_model']}",
                'memory': f"{app_server['memory_gb']}GB",
                'disk': f"{app_server['disk_gb']}GB {app_server['disk_type']}",
                'network': app_server['network'],
                'quantity': 1,
                'unit_price': app_server['price'],
                'total_price': app_server['price'],
                'power_w': app_server['power_w']
            })
        
        # 监控服务器
        monitor_server = self.server_catalog['monitor_server']
        equipment['servers'].append({
            'id': 'monitor-01',
            'role': '监控服务器',
            'model': monitor_server['name'],
            'cpu': f"{monitor_server['cpu_cores']}核 {monitor_server['cpu_model']}",
            'memory': f"{monitor_server['memory_gb']}GB",
            'disk': f"{monitor_server['disk_gb']}GB {monitor_server['disk_type']}",
            'network': monitor_server['network'],
            'quantity': 1,
            'unit_price': monitor_server['price'],
            'total_price': monitor_server['price'],
            'power_w': monitor_server['power_w']
        })
        
        # 备份服务器
        equipment['servers'].append({
            'id': 'backup-01',
            'role': '备份服务器',
            'model': monitor_server['name'],
            'cpu': f"{monitor_server['cpu_cores']}核 {monitor_server['cpu_model']}",
            'memory': f"{monitor_server['memory_gb']}GB",
            'disk': f"{monitor_server['disk_gb']*2}GB {monitor_server['disk_type']}",
            'network': monitor_server['network'],
            'quantity': 1,
            'unit_price': monitor_server['price'],
            'total_price': monitor_server['price'],
            'power_w': monitor_server['power_w']
        })
        
        # 网络设备
        total_servers = len(equipment['servers'])
        
        # 核心交换机（双机热备）
        core_switch = self.network_catalog['core_switch_10g'] if scale in ['small', 'medium'] else self.network_catalog['core_switch_40g']
        equipment['network_devices'].append({
            'id': 'core-sw-01',
            'type': '核心交换机（主）',
            'model': core_switch['name'],
            'ports': f"{core_switch['ports']}x{core_switch['speed']}",
            'uplink': core_switch['uplink'],
            'quantity': 1,
            'unit_price': core_switch['price'],
            'total_price': core_switch['price'],
            'power_w': core_switch['power_w']
        })
        equipment['network_devices'].append({
            'id': 'core-sw-02',
            'type': '核心交换机（备）',
            'model': core_switch['name'],
            'ports': f"{core_switch['ports']}x{core_switch['speed']}",
            'uplink': core_switch['uplink'],
            'quantity': 1,
            'unit_price': core_switch['price'],
            'total_price': core_switch['price'],
            'power_w': core_switch['power_w']
        })
        
        # 接入交换机
        access_switch_count = math.ceil(total_servers / 40)  # 每台交换机接40台服务器
        access_switch = self.network_catalog['access_switch_1g'] if scale == 'small' else self.network_catalog['access_switch_10g']
        for i in range(access_switch_count):
            equipment['network_devices'].append({
                'id': f'access-sw-{i+1:02d}',
                'type': '接入交换机',
                'model': access_switch['name'],
                'ports': f"{access_switch['ports']}x{access_switch['speed']}",
                'uplink': access_switch['uplink'],
                'quantity': 1,
                'unit_price': access_switch['price'],
                'total_price': access_switch['price'],
                'power_w': access_switch['power_w']
            })
        
        # 防火墙（双机热备）
        firewall = self.network_catalog['firewall']
        equipment['network_devices'].append({
            'id': 'firewall-01',
            'type': '防火墙（主）',
            'model': firewall['name'],
            'throughput': firewall['throughput'],
            'quantity': 1,
            'unit_price': firewall['price'],
            'total_price': firewall['price'],
            'power_w': firewall['power_w']
        })
        equipment['network_devices'].append({
            'id': 'firewall-02',
            'type': '防火墙（备）',
            'model': firewall['name'],
            'throughput': firewall['throughput'],
            'quantity': 1,
            'unit_price': firewall['price'],
            'total_price': firewall['price'],
            'power_w': firewall['power_w']
        })
        
        # 负载均衡器（双机热备）
        lb = self.network_catalog['load_balancer']
        equipment['network_devices'].append({
            'id': 'lb-01',
            'type': '负载均衡器（主）',
            'model': lb['name'],
            'throughput': lb['throughput'],
            'quantity': 1,
            'unit_price': lb['price'],
            'total_price': lb['price'],
            'power_w': lb['power_w']
        })
        equipment['network_devices'].append({
            'id': 'lb-02',
            'type': '负载均衡器（备）',
            'model': lb['name'],
            'throughput': lb['throughput'],
            'quantity': 1,
            'unit_price': lb['price'],
            'total_price': lb['price'],
            'power_w': lb['power_w']
        })
        
        # 路由器
        router = self.network_catalog['router']
        equipment['network_devices'].append({
            'id': 'router-01',
            'type': '边界路由器',
            'model': router['name'],
            'throughput': router['throughput'],
            'quantity': 1,
            'unit_price': router['price'],
            'total_price': router['price'],
            'power_w': router['power_w']
        })
        
        # 存储设备（额外存储）
        total_storage_tb = math.ceil(analysis['requirements']['storage_gb_needed'] / 1000)
        storage_type = 'ssd_nvme' if scale in ['large', 'xlarge'] else 'ssd_sata'
        storage_spec = self.storage_catalog[storage_type]
        equipment['storage'].append({
            'type': storage_spec['type'],
            'model': storage_spec['model'],
            'capacity_tb': total_storage_tb,
            'iops': storage_spec['iops'],
            'throughput': f"{storage_spec['throughput_mbps']}MB/s",
            'unit_price_per_tb': storage_spec['price_per_tb'],
            'total_price': total_storage_tb * storage_spec['price_per_tb']
        })
        
        # 基础设施
        rack_count = math.ceil(total_servers / 30)  # 每个机柜30台服务器
        equipment['infrastructure'].append({
            'type': '42U标准机柜',
            'quantity': rack_count,
            'unit_price': self.infrastructure_costs['rack_42u']['price'],
            'total_price': rack_count * self.infrastructure_costs['rack_42u']['price']
        })
        
        equipment['infrastructure'].append({
            'type': 'PDU电源分配单元',
            'quantity': rack_count * 2,  # 每个机柜2个PDU
            'unit_price': self.infrastructure_costs['pdu']['price'],
            'total_price': rack_count * 2 * self.infrastructure_costs['pdu']['price']
        })
        
        # 计算总功率
        total_power_w = sum(s['power_w'] for s in equipment['servers'])
        total_power_w += sum(n['power_w'] for n in equipment['network_devices'])
        total_power_kw = math.ceil(total_power_w / 1000)
        
        equipment['infrastructure'].append({
            'type': 'UPS不间断电源',
            'capacity_kw': total_power_kw * 1.5,  # 1.5倍冗余
            'unit_price': self.infrastructure_costs['ups_per_kw']['price_per_kw'],
            'total_price': total_power_kw * 1.5 * self.infrastructure_costs['ups_per_kw']['price_per_kw']
        })
        
        equipment['infrastructure'].append({
            'type': '网线及配件',
            'quantity': total_servers,
            'unit_price': self.infrastructure_costs['cable_per_server']['price'],
            'total_price': total_servers * self.infrastructure_costs['cable_per_server']['price']
        })
        
        return equipment
    
    def _calculate_costs(self, equipment, architecture):
        """计算成本清单"""
        costs = {
            'hardware': {
                'servers': 0,
                'network_devices': 0,
                'storage': 0,
                'infrastructure': 0
            },
            'software': {
                'tdsql_license': 0,
                'os_license': 0,
                'monitoring': 0,
                'backup': 0
            },
            'services': {
                'deployment': 0,
                'training': 0
            },
            'annual_operating': {
                'power': 0,
                'cooling': 0,
                'maintenance': 0
            }
        }
        
        # 硬件成本
        costs['hardware']['servers'] = sum(s['total_price'] for s in equipment['servers'])
        costs['hardware']['network_devices'] = sum(n['total_price'] for n in equipment['network_devices'])
        costs['hardware']['storage'] = sum(s['total_price'] for s in equipment['storage'])
        costs['hardware']['infrastructure'] = sum(i['total_price'] for i in equipment['infrastructure'])
        
        # 软件许可证
        total_db_cores = sum(
            int(s['cpu'].split('核')[0]) 
            for s in equipment['servers'] 
            if 'db-' in s['id']
        )
        costs['software']['tdsql_license'] = total_db_cores * self.software_licenses['tdsql_enterprise']['price_per_core']
        
        total_servers = len(equipment['servers'])
        costs['software']['os_license'] = total_servers * self.software_licenses['os_redhat']['price_per_server']
        
        costs['software']['monitoring'] = total_servers * self.software_licenses['monitoring_prometheus']['price_per_node']
        
        total_storage_tb = sum(s['capacity_tb'] for s in equipment['storage'])
        costs['software']['backup'] = total_storage_tb * self.software_licenses['backup_software']['price_per_tb']
        
        # 服务成本
        costs['services']['deployment'] = total_servers * self.infrastructure_costs['deployment_per_server']['price']
        costs['services']['training'] = self.infrastructure_costs['training']['price']
        
        # 年度运营成本
        total_power_w = sum(s['power_w'] for s in equipment['servers'])
        total_power_w += sum(n['power_w'] for n in equipment['network_devices'])
        total_power_kw = total_power_w / 1000
        
        costs['annual_operating']['power'] = total_power_kw * self.infrastructure_costs['annual_power_per_kw']['price']
        costs['annual_operating']['cooling'] = costs['annual_operating']['power'] * self.infrastructure_costs['annual_cooling_ratio']['ratio']
        
        # 维护成本（软件许可证的年度维护费）
        costs['annual_operating']['maintenance'] = (
            costs['software']['tdsql_license'] * self.software_licenses['tdsql_enterprise']['annual_maintenance_rate'] +
            costs['software']['os_license'] * self.software_licenses['os_redhat']['annual_maintenance_rate'] +
            costs['software']['monitoring'] * self.software_licenses['monitoring_prometheus']['annual_maintenance_rate']
        )
        
        # 计算总成本
        total_hardware = sum(costs['hardware'].values())
        total_software = sum(costs['software'].values())
        total_services = sum(costs['services'].values())
        total_annual = sum(costs['annual_operating'].values())
        
        initial_investment = total_hardware + total_software + total_services
        three_year_tco = initial_investment + (total_annual * 3)
        
        return {
            'breakdown': costs,
            'summary': {
                'total_hardware': total_hardware,
                'total_software': total_software,
                'total_services': total_services,
                'initial_investment': initial_investment,
                'annual_operating': total_annual,
                'three_year_tco': three_year_tco,
                'monthly_operating': total_annual / 12
            }
        }
    
    def _design_network_topology(self, architecture, equipment):
        """设计网络拓扑"""
        return {
            'layers': [
                {
                    'name': 'Internet接入层',
                    'devices': ['router-01'],
                    'description': '连接外部网络'
                },
                {
                    'name': 'DMZ安全区',
                    'devices': ['firewall-01', 'firewall-02', 'lb-01', 'lb-02'],
                    'description': '安全隔离和负载均衡'
                },
                {
                    'name': '核心交换层',
                    'devices': ['core-sw-01', 'core-sw-02'],
                    'description': '核心网络交换，双机热备'
                },
                {
                    'name': '接入交换层',
                    'devices': [d['id'] for d in equipment['network_devices'] if 'access-sw' in d['id']],
                    'description': '服务器接入'
                },
                {
                    'name': '应用服务层',
                    'devices': [s['id'] for s in equipment['servers'] if 'app-' in s['id']],
                    'description': '应用服务器集群'
                },
                {
                    'name': 'TDSQL代理层',
                    'devices': [s['id'] for s in equipment['servers'] if 'proxy-' in s['id']],
                    'description': 'TDSQL代理节点'
                },
                {
                    'name': '数据库层',
                    'devices': [s['id'] for s in equipment['servers'] if 'db-' in s['id']],
                    'description': 'TDSQL数据库集群'
                },
                {
                    'name': '管理监控层',
                    'devices': ['monitor-01', 'backup-01'],
                    'description': '监控和备份服务'
                }
            ],
            'connections': [
                {'from': 'Internet', 'to': 'router-01', 'type': '外网连接'},
                {'from': 'router-01', 'to': 'firewall-01/02', 'type': '边界防护'},
                {'from': 'firewall-01/02', 'to': 'lb-01/02', 'type': '负载均衡'},
                {'from': 'lb-01/02', 'to': 'core-sw-01/02', 'type': '核心交换'},
                {'from': 'core-sw-01/02', 'to': 'access-sw-*', 'type': '接入交换'},
                {'from': 'access-sw-*', 'to': 'app-*', 'type': '应用服务器'},
                {'from': 'app-*', 'to': 'proxy-*', 'type': 'TDSQL代理'},
                {'from': 'proxy-*', 'to': 'db-*', 'type': '数据库访问'}
            ],
            'vlans': [
                {'id': 10, 'name': 'DMZ', 'subnet': '10.0.10.0/24'},
                {'id': 20, 'name': 'APP', 'subnet': '10.0.20.0/24'},
                {'id': 30, 'name': 'PROXY', 'subnet': '10.0.30.0/24'},
                {'id': 40, 'name': 'DB', 'subnet': '10.0.40.0/24'},
                {'id': 50, 'name': 'MGMT', 'subnet': '10.0.50.0/24'}
            ]
        }
    
    def _generate_architecture_diagram(self, architecture, equipment):
        """生成架构图数据（用于前端可视化）"""
        nodes = []
        links = []
        
        # 添加节点
        node_id = 0
        
        # Internet节点
        nodes.append({
            'id': node_id,
            'name': 'Internet',
            'type': 'internet',
            'layer': 0
        })
        internet_id = node_id
        node_id += 1
        
        # 路由器
        nodes.append({
            'id': node_id,
            'name': 'Router',
            'type': 'router',
            'layer': 1
        })
        router_id = node_id
        links.append({'source': internet_id, 'target': router_id})
        node_id += 1
        
        # 防火墙
        firewall_ids = []
        for i in range(2):
            nodes.append({
                'id': node_id,
                'name': f'Firewall-{i+1}',
                'type': 'firewall',
                'layer': 2
            })
            firewall_ids.append(node_id)
            links.append({'source': router_id, 'target': node_id})
            node_id += 1
        
        # 负载均衡器
        lb_ids = []
        for i in range(2):
            nodes.append({
                'id': node_id,
                'name': f'LB-{i+1}',
                'type': 'load_balancer',
                'layer': 3
            })
            lb_ids.append(node_id)
            for fw_id in firewall_ids:
                links.append({'source': fw_id, 'target': node_id})
            node_id += 1
        
        # 核心交换机
        core_sw_ids = []
        for i in range(2):
            nodes.append({
                'id': node_id,
                'name': f'Core-SW-{i+1}',
                'type': 'core_switch',
                'layer': 4
            })
            core_sw_ids.append(node_id)
            for lb_id in lb_ids:
                links.append({'source': lb_id, 'target': node_id})
            node_id += 1
        
        # 应用服务器
        app_ids = []
        for server in equipment['servers']:
            if 'app-' in server['id']:
                nodes.append({
                    'id': node_id,
                    'name': server['id'],
                    'type': 'app_server',
                    'layer': 5
                })
                app_ids.append(node_id)
                for sw_id in core_sw_ids:
                    links.append({'source': sw_id, 'target': node_id})
                node_id += 1
        
        # 代理服务器
        proxy_ids = []
        for server in equipment['servers']:
            if 'proxy-' in server['id']:
                nodes.append({
                    'id': node_id,
                    'name': server['id'],
                    'type': 'proxy_server',
                    'layer': 6
                })
                proxy_ids.append(node_id)
                for app_id in app_ids:
                    links.append({'source': app_id, 'target': node_id})
                node_id += 1
        
        # 数据库服务器
        for server in equipment['servers']:
            if 'db-' in server['id']:
                nodes.append({
                    'id': node_id,
                    'name': server['id'],
                    'type': 'db_server',
                    'layer': 7
                })
                for proxy_id in proxy_ids:
                    links.append({'source': proxy_id, 'target': node_id})
                node_id += 1
        
        return {
            'nodes': nodes,
            'links': links,
            'layout': 'hierarchical'
        }
    
    def _generate_recommendations(self, analysis, architecture):
        """生成部署建议"""
        recommendations = []
        
        scale = analysis['summary']['scale']
        
        # 性能优化建议
        if scale in ['large', 'xlarge']:
            recommendations.append({
                'category': '性能优化',
                'priority': 'high',
                'title': '启用SSD缓存加速',
                'description': '建议为数据库节点配置NVMe SSD作为缓存层，可提升30-50%的读写性能'
            })
        
        # 高可用建议
        if architecture['ha_config']['level'] == 'high':
            recommendations.append({
                'category': '高可用',
                'priority': 'high',
                'title': '配置异地容灾',
                'description': '建议在异地机房部署备份集群，实现RPO<1小时，RTO<30分钟'
            })
        
        # 监控建议
        recommendations.append({
            'category': '监控运维',
            'priority': 'medium',
            'title': '部署全链路监控',
            'description': '建议部署Prometheus+Grafana监控体系，实时监控数据库性能指标'
        })
        
        # 安全建议
        recommendations.append({
            'category': '安全加固',
            'priority': 'high',
            'title': '启用数据加密',
            'description': '建议启用TDE透明数据加密和SSL传输加密，保护数据安全'
        })
        
        # 备份建议
        recommendations.append({
            'category': '数据备份',
            'priority': 'high',
            'title': '制定备份策略',
            'description': '建议采用全量+增量备份策略：每日全量备份，每小时增量备份，保留30天'
        })
        
        # 容量规划建议
        if analysis['summary']['projected_data_gb'] > analysis['summary']['current_data_gb'] * 2:
            recommendations.append({
                'category': '容量规划',
                'priority': 'medium',
                'title': '预留扩展空间',
                'description': f"预测3年数据增长至{analysis['summary']['projected_data_gb']:.0f}GB，建议预留50%扩展空间"
            })
        
        return recommendations
    
    def parse_file(self, filepath):
        """
        解析上传的文件，提取业务参数
        支持: JSON, Excel, 图片(OCR), PDF
        """
        import os
        
        file_ext = os.path.splitext(filepath)[1].lower()
        params = {}
        
        try:
            if file_ext == '.json':
                # 解析JSON文件
                params = self._parse_json(filepath)
            elif file_ext in ['.xlsx', '.xls']:
                # 解析Excel文件
                params = self._parse_excel(filepath)
            elif file_ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
                # 解析图片文件（OCR）
                params = self._parse_image(filepath)
            elif file_ext == '.pdf':
                # 解析PDF文件
                params = self._parse_pdf(filepath)
            else:
                params = {'error': f'不支持的文件类型: {file_ext}'}
        except Exception as e:
            params = {'error': f'文件解析失败: {str(e)}'}
        
        return params
    
    def _parse_json(self, filepath):
        """解析JSON文件"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 提取参数
        params = {}
        
        # 映射字段
        field_mapping = {
            'qps': ['qps', 'QPS', 'queries_per_second', '每秒查询数'],
            'tps': ['tps', 'TPS', 'transactions_per_second', '每秒事务数'],
            'data_volume': ['data_volume', 'data_size', 'storage', '数据量', '存储容量'],
            'concurrent_users': ['concurrent_users', 'users', 'connections', '并发用户数', '连接数'],
            'ha_level': ['ha_level', 'high_availability', 'ha', '高可用级别'],
            'industry': ['industry', 'business_type', '行业', '业务类型'],
            'growth_rate': ['growth_rate', 'growth', '增长率'],
            'backup_retention': ['backup_retention', 'retention', '备份保留天数']
        }
        
        for key, aliases in field_mapping.items():
            for alias in aliases:
                if alias in data:
                    params[key] = data[alias]
                    break
        
        return params
    
    def _parse_excel(self, filepath):
        """解析Excel文件"""
        try:
            import openpyxl
            wb = openpyxl.load_workbook(filepath)
            ws = wb.active
            
            params = {}
            
            # 尝试从表格中提取参数
            for row in ws.iter_rows(min_row=1, max_row=50, values_only=True):
                if not row or len(row) < 2:
                    continue
                
                key = str(row[0]).strip() if row[0] else ''
                value = row[1]
                
                # 匹配参数
                if 'QPS' in key.upper() or '查询' in key:
                    params['qps'] = self._extract_number(value)
                elif 'TPS' in key.upper() or '事务' in key:
                    params['tps'] = self._extract_number(value)
                elif '数据量' in key or '存储' in key or 'DATA' in key.upper():
                    params['data_volume'] = self._extract_number(value)
                elif '并发' in key or '用户' in key or 'USER' in key.upper():
                    params['concurrent_users'] = self._extract_number(value)
                elif '高可用' in key or 'HA' in key.upper():
                    params['ha_level'] = str(value).lower()
                elif '行业' in key or 'INDUSTRY' in key.upper():
                    params['industry'] = str(value)
            
            return params
            
        except ImportError:
            return {'error': '需要安装openpyxl库: pip install openpyxl'}
        except Exception as e:
            return {'error': f'Excel解析失败: {str(e)}'}
    
    def _parse_image(self, filepath):
        """解析图片文件（OCR识别）"""
        try:
            # 尝试使用pytesseract进行OCR
            from PIL import Image
            import pytesseract
            
            image = Image.open(filepath)
            text = pytesseract.image_to_string(image, lang='chi_sim+eng')
            
            # 从文本中提取参数
            params = self._extract_params_from_text(text)
            return params
            
        except ImportError:
            # 如果没有OCR库，返回基本信息
            from PIL import Image
            image = Image.open(filepath)
            return {
                'info': f'图片文件 ({image.size[0]}x{image.size[1]})',
                'message': '需要安装pytesseract进行文字识别: pip install pytesseract',
                'suggestion': '请手动输入参数或上传JSON/Excel文件'
            }
        except Exception as e:
            return {'error': f'图片解析失败: {str(e)}'}
    
    def _parse_pdf(self, filepath):
        """解析PDF文件"""
        try:
            import PyPDF2
            
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ''
                for page in reader.pages[:10]:  # 只读前10页
                    text += page.extract_text()
            
            # 从文本中提取参数
            params = self._extract_params_from_text(text)
            return params
            
        except ImportError:
            return {'error': '需要安装PyPDF2库: pip install PyPDF2'}
        except Exception as e:
            return {'error': f'PDF解析失败: {str(e)}'}
    
    def _extract_params_from_text(self, text):
        """从文本中提取参数"""
        import re
        
        params = {}
        
        # QPS
        qps_match = re.search(r'QPS[:\s]*(\d+)', text, re.IGNORECASE)
        if qps_match:
            params['qps'] = int(qps_match.group(1))
        
        # TPS
        tps_match = re.search(r'TPS[:\s]*(\d+)', text, re.IGNORECASE)
        if tps_match:
            params['tps'] = int(tps_match.group(1))
        
        # 数据量
        data_match = re.search(r'数据量[:\s]*(\d+)\s*(GB|TB|G|T)?', text)
        if data_match:
            value = int(data_match.group(1))
            unit = data_match.group(2)
            if unit and unit.upper().startswith('T'):
                value *= 1000
            params['data_volume'] = value
        
        # 并发用户
        user_match = re.search(r'并发[用户数]*[:\s]*(\d+)', text)
        if user_match:
            params['concurrent_users'] = int(user_match.group(1))
        
        return params
    
    def _extract_number(self, value):
        """从值中提取数字"""
        if isinstance(value, (int, float)):
            return value
        
        if isinstance(value, str):
            import re
            match = re.search(r'(\d+(?:\.\d+)?)', value)
            if match:
                num = float(match.group(1))
                return int(num) if num.is_integer() else num
        
        return None
