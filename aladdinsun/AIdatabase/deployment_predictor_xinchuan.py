"""
TDSQL 部署资源预测系统 - 信创版核心引擎
支持国产化设备配置
"""

import math
import json
from datetime import datetime
from xinchuan_device_catalog import XinChuangDeviceCatalog

class DeploymentResourcePredictorXinChuan:
    """部署资源预测器 - 信创国产化版本"""
    
    def __init__(self, xinchuan_mode='standard'):
        """
        初始化预测器
        
        Args:
            xinchuan_mode: 信创模式
                - 'standard': 标准信创(服务器+网络国产化) 
                - 'strict': 严格信创(全国产CPU)
                - 'full': 完全信创(全栈国产)
                - 'off': 关闭信创模式(使用国外品牌)
        """
        self.xinchuan_mode = xinchuan_mode
        self.xc_catalog = XinChuangDeviceCatalog()
        
        # 根据信创模式选择设备库
        if xinchuan_mode in ['standard', 'strict', 'full']:
            self.server_catalog = self.xc_catalog.server_catalog
            self.network_catalog = self.xc_catalog.network_catalog
            self.storage_catalog = self.xc_catalog.storage_catalog
            self.software_licenses = self.xc_catalog.software_licenses
        else:
            # 非信创模式,使用原有国外品牌配置
            self._init_international_catalog()
        
        # 基础设施成本(通用)
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
    
    def _init_international_catalog(self):
        """初始化国外品牌设备配置库"""
        self.server_catalog = {
            'db_small': {
                'name': 'Dell PowerEdge R440',
                'cpu_cores': 8, 'cpu_model': 'Intel Xeon Silver 4208',
                'memory_gb': 32, 'disk_gb': 1000, 'disk_type': 'SSD SATA',
                'network': '双万兆网卡',
                'price': 28000, 'power_w': 350,
                'use_case': '小型数据库节点',
                'vendor': 'Dell', 'certification': 'Standard'
            },
            'db_medium': {
                'name': 'Dell PowerEdge R640',
                'cpu_cores': 16, 'cpu_model': 'Intel Xeon Gold 5218',
                'memory_gb': 64, 'disk_gb': 2000, 'disk_type': 'SSD SATA',
                'network': '双万兆网卡',
                'price': 45000, 'power_w': 500,
                'use_case': '中型数据库节点',
                'vendor': 'Dell', 'certification': 'Standard'
            },
            'db_large': {
                'name': 'Dell PowerEdge R740',
                'cpu_cores': 32, 'cpu_model': 'Intel Xeon Gold 6248',
                'memory_gb': 128, 'disk_gb': 4000, 'disk_type': 'NVMe SSD',
                'network': '双万兆网卡',
                'price': 85000, 'power_w': 750,
                'use_case': '大型数据库节点',
                'vendor': 'Dell', 'certification': 'Standard'
            },
            'db_xlarge': {
                'name': 'Dell PowerEdge R940',
                'cpu_cores': 64, 'cpu_model': 'Intel Xeon Platinum 8280',
                'memory_gb': 256, 'disk_gb': 8000, 'disk_type': 'NVMe SSD',
                'network': '双万兆网卡',
                'price': 180000, 'power_w': 1200,
                'use_case': '超大型数据库节点',
                'vendor': 'Dell', 'certification': 'Standard'
            },
            'proxy_server': {
                'name': 'Dell PowerEdge R340',
                'cpu_cores': 8, 'cpu_model': 'Intel Xeon E-2278G',
                'memory_gb': 32, 'disk_gb': 500, 'disk_type': 'SSD SATA',
                'network': '双万兆网卡',
                'price': 22000, 'power_w': 300,
                'use_case': 'TDSQL代理节点',
                'vendor': 'Dell', 'certification': 'Standard'
            },
            'monitor_server': {
                'name': 'Dell PowerEdge R340',
                'cpu_cores': 4, 'cpu_model': 'Intel Xeon E-2234',
                'memory_gb': 16, 'disk_gb': 1000, 'disk_type': 'SSD SATA',
                'network': '双千兆网卡',
                'price': 20000, 'power_w': 250,
                'use_case': '监控服务器',
                'vendor': 'Dell', 'certification': 'Standard'
            }
        }
        
        self.network_catalog = {
            'core_switch_10g': {
                'name': 'Cisco Nexus 93180YC-FX',
                'type': '核心交换机',
                'ports': 48, 'speed': '10Gbps',
                'uplink': '6x40Gbps',
                'price': 85000, 'power_w': 250,
                'vendor': 'Cisco', 'certification': 'Standard'
            },
            'access_switch_1g': {
                'name': 'Cisco Catalyst 2960-X',
                'type': '接入交换机',
                'ports': 48, 'speed': '1Gbps',
                'uplink': '4x10Gbps',
                'price': 12000, 'power_w': 100,
                'vendor': 'Cisco', 'certification': 'Standard'
            },
            'firewall': {
                'name': 'Fortinet FortiGate 600E',
                'type': '防火墙',
                'throughput': '10Gbps',
                'price': 120000, 'power_w': 150,
                'vendor': 'Fortinet', 'certification': 'Standard'
            }
        }
        
        self.storage_catalog = {
            'ssd_sata': {
                'type': 'SATA SSD',
                'model': 'Samsung 870 EVO',
                'price_per_tb': 1200,
                'iops': 50000,
                'throughput_mbps': 550,
                'vendor': 'Samsung'
            },
            'ssd_nvme': {
                'type': 'NVMe SSD',
                'model': 'Samsung 980 PRO',
                'price_per_tb': 2500,
                'iops': 500000,
                'throughput_mbps': 7000,
                'vendor': 'Samsung'
            }
        }
        
        self.software_licenses = {
            'os_redhat': {
                'name': 'Red Hat Enterprise Linux',
                'price_per_server': 5000,
                'annual_maintenance_rate': 0.15,
                'vendor': 'Red Hat'
            },
            'monitoring_prometheus': {
                'name': 'Prometheus监控套件',
                'price_per_node': 0,
                'annual_maintenance_rate': 0,
                'vendor': '开源社区'
            }
        }
    
    def predict(self, input_data):
        """主预测函数"""
        # 1. 分析输入参数
        analysis = self._analyze_requirements(input_data)
        
        # 2. 设计架构(考虑信创要求)
        architecture = self._design_architecture_xinchuan(analysis)
        
        # 3. 计算设备清单(使用信创设备)
        equipment_list = self._calculate_equipment_xinchuan(architecture, analysis)
        
        # 4. 计算成本(包含信创优势说明)
        cost_breakdown = self._calculate_cost_xinchuan(equipment_list, architecture)
        
        # 5. 生成架构图描述
        architecture_diagram = self._generate_architecture_diagram(architecture)
        
        # 6. 生成建议
        recommendations = self._generate_recommendations_xinchuan(analysis, architecture)
        
        return {
            'xinchuan_mode': self.xinchuan_mode,
            'xinchuan_info': self._get_xinchuan_info(),
            'input_summary': analysis,
            'architecture': architecture,
            'equipment_list': equipment_list,
            'cost_breakdown': cost_breakdown,
            'architecture_diagram': architecture_diagram,
            'recommendations': recommendations,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def _get_xinchuan_info(self):
        """获取信创模式信息"""
        if self.xinchuan_mode == 'off':
            return {
                'enabled': False,
                'mode': '标准模式(国际品牌)',
                'description': '使用Dell、Cisco等国际品牌设备'
            }
        
        rec = self.xc_catalog.get_xinchuan_recommendation(self.xinchuan_mode)
        return {
            'enabled': True,
            'mode': rec['description'],
            'servers': rec['servers'],
            'network': rec['network'],
            'cpu': rec['cpu'],
            'cost_advantage': rec['cost_advantage'],
            'compliance': '符合国家信创要求' if self.xinchuan_mode == 'full' else '部分符合信创要求'
        }
    
    def _analyze_requirements(self, input_data):
        """分析需求(与原版相同)"""
        # 这里保持原有逻辑
        return {
            'total_data_size_tb': input_data.get('data_size_gb', 1000) / 1024,
            'daily_transactions': input_data.get('transactions_per_day', 1000000),
            'concurrent_connections': input_data.get('max_connections', 1000),
            'business_type': input_data.get('business_type', 'OLTP'),
            'ha_requirement': input_data.get('high_availability', True),
            'dr_requirement': input_data.get('disaster_recovery', False)
        }
    
    def _design_architecture_xinchuan(self, analysis):
        """设计架构(考虑信创要求)"""
        # 根据数据量和事务量动态计算节点数量
        data_size_tb = analysis['total_data_size_tb']
        daily_txn = analysis['daily_transactions']
        
        # 动态计算数据库节点数量（每TB数据至少1个节点，最少3个，最多20个）
        db_nodes_by_data = max(3, min(20, int(data_size_tb / 10) + 3))
        
        # 根据事务量调整节点数（每百万事务/天至少1个节点）
        db_nodes_by_txn = max(3, min(20, int(daily_txn / 1000000) + 3))
        
        # 取较大值作为数据库节点数
        database_nodes = max(db_nodes_by_data, db_nodes_by_txn)
        
        # 代理节点数量随数据库节点增加而增加
        proxy_nodes = max(2, min(6, int(database_nodes / 3) + 1))
        
        # 监控节点（大规模部署需要多个监控节点）
        monitoring_nodes = 1 if database_nodes <= 10 else 2
        
        # 基础架构设计
        architecture = {
            'deployment_mode': 'cluster',
            'database_nodes': database_nodes,
            'proxy_nodes': proxy_nodes,
            'monitoring_nodes': monitoring_nodes,
            'xinchuan_compliance': self.xinchuan_mode != 'off'
        }
        
        # 根据数据量调整节点规格
        if data_size_tb > 50:
            architecture['node_spec'] = 'db_xlarge'
        elif data_size_tb > 10:
            architecture['node_spec'] = 'db_large'
        elif data_size_tb > 2:
            architecture['node_spec'] = 'db_medium'
        else:
            architecture['node_spec'] = 'db_small'
        
        print(f"\n🏗️  架构设计: {database_nodes}个数据库节点, {proxy_nodes}个代理节点, {monitoring_nodes}个监控节点")
        print(f"📊 数据量: {data_size_tb:.1f}TB, 日事务: {daily_txn:,}, 节点规格: {architecture['node_spec']}")
        
        return architecture
    
    def _calculate_equipment_xinchuan(self, architecture, analysis):
        """计算设备清单(使用信创设备)"""
        equipment = []
        
        # 数据库服务器
        db_spec = self.server_catalog[architecture['node_spec']]
        for i in range(architecture['database_nodes']):
            equipment.append({
                'category': '数据库服务器',
                'name': db_spec['name'],
                'spec': f"{db_spec['cpu_cores']}核 {db_spec['cpu_model']}, {db_spec['memory_gb']}GB内存, {db_spec['disk_gb']}GB {db_spec['disk_type']}",
                'cpu_cores': db_spec['cpu_cores'],
                'cpu_model': db_spec['cpu_model'],
                'memory_gb': db_spec['memory_gb'],
                'disk_gb': db_spec['disk_gb'],
                'disk_type': db_spec['disk_type'],
                'network': db_spec.get('network', '双万兆网卡'),
                'power_w': db_spec.get('power_w', 0),
                'quantity': 1,
                'unit_price': db_spec['price'],
                'total_price': db_spec['price'],
                'vendor': db_spec.get('vendor', 'N/A'),
                'certification': db_spec.get('certification', 'N/A'),
                'use_case': db_spec.get('use_case', '数据库节点'),
                'xinchuan_compliant': self.xinchuan_mode != 'off'
            })
        
        # 代理服务器
        proxy_spec = self.server_catalog['proxy_server']
        equipment.append({
            'category': '代理服务器',
            'name': proxy_spec['name'],
            'spec': f"{proxy_spec['cpu_cores']}核 {proxy_spec['cpu_model']}, {proxy_spec['memory_gb']}GB内存, {proxy_spec['disk_gb']}GB {proxy_spec['disk_type']}",
            'cpu_cores': proxy_spec['cpu_cores'],
            'cpu_model': proxy_spec['cpu_model'],
            'memory_gb': proxy_spec['memory_gb'],
            'disk_gb': proxy_spec['disk_gb'],
            'disk_type': proxy_spec['disk_type'],
            'network': proxy_spec.get('network', '双万兆网卡'),
            'power_w': proxy_spec.get('power_w', 0),
            'quantity': architecture['proxy_nodes'],
            'unit_price': proxy_spec['price'],
            'total_price': proxy_spec['price'] * architecture['proxy_nodes'],
            'vendor': proxy_spec.get('vendor', 'N/A'),
            'certification': proxy_spec.get('certification', 'N/A'),
            'use_case': proxy_spec.get('use_case', '代理节点'),
            'xinchuan_compliant': self.xinchuan_mode != 'off'
        })
        
        # 监控服务器
        monitor_spec = self.server_catalog['monitor_server']
        equipment.append({
            'category': '监控服务器',
            'name': monitor_spec['name'],
            'spec': f"{monitor_spec['cpu_cores']}核 {monitor_spec['cpu_model']}, {monitor_spec['memory_gb']}GB内存, {monitor_spec['disk_gb']}GB {monitor_spec['disk_type']}",
            'cpu_cores': monitor_spec['cpu_cores'],
            'cpu_model': monitor_spec['cpu_model'],
            'memory_gb': monitor_spec['memory_gb'],
            'disk_gb': monitor_spec['disk_gb'],
            'disk_type': monitor_spec['disk_type'],
            'network': monitor_spec.get('network', '双千兆网卡'),
            'power_w': monitor_spec.get('power_w', 0),
            'quantity': architecture.get('monitoring_nodes', 1),
            'unit_price': monitor_spec['price'],
            'total_price': monitor_spec['price'] * architecture.get('monitoring_nodes', 1),
            'vendor': monitor_spec.get('vendor', 'N/A'),
            'certification': monitor_spec.get('certification', 'N/A'),
            'use_case': monitor_spec.get('use_case', '监控节点'),
            'xinchuan_compliant': self.xinchuan_mode != 'off'
        })
        
        # 网络设备 - 核心交换机
        switch_spec = self.network_catalog['core_switch_10g']
        equipment.append({
            'category': '核心交换机',
            'name': switch_spec['name'],
            'spec': f"{switch_spec['ports']}口 {switch_spec['speed']}, 上联 {switch_spec.get('uplink', 'N/A')}",
            'ports': switch_spec['ports'],
            'speed': switch_spec['speed'],
            'uplink': switch_spec.get('uplink', 'N/A'),
            'power_w': switch_spec.get('power_w', 0),
            'quantity': 2,  # 双核心
            'unit_price': switch_spec['price'],
            'total_price': switch_spec['price'] * 2,
            'vendor': switch_spec.get('vendor', 'N/A'),
            'certification': switch_spec.get('certification', 'N/A'),
            'device_type': switch_spec.get('type', '核心交换机'),
            'xinchuan_compliant': self.xinchuan_mode != 'off'
        })
        
        # 网络设备 - 接入交换机
        access_switch_spec = self.network_catalog['access_switch_1g']
        equipment.append({
            'category': '接入交换机',
            'name': access_switch_spec['name'],
            'spec': f"{access_switch_spec['ports']}口 {access_switch_spec['speed']}, 上联 {access_switch_spec.get('uplink', 'N/A')}",
            'ports': access_switch_spec['ports'],
            'speed': access_switch_spec['speed'],
            'uplink': access_switch_spec.get('uplink', 'N/A'),
            'power_w': access_switch_spec.get('power_w', 0),
            'quantity': 2,
            'unit_price': access_switch_spec['price'],
            'total_price': access_switch_spec['price'] * 2,
            'vendor': access_switch_spec.get('vendor', 'N/A'),
            'certification': access_switch_spec.get('certification', 'N/A'),
            'device_type': access_switch_spec.get('type', '接入交换机'),
            'xinchuan_compliant': self.xinchuan_mode != 'off'
        })
        
        # 安全设备 - 防火墙
        if analysis.get('ha_requirement', True):
            firewall_spec = self.network_catalog['firewall']
            equipment.append({
                'category': '安全防火墙',
                'name': firewall_spec['name'],
                'spec': f"吞吐量 {firewall_spec.get('throughput', 'N/A')}",
                'throughput': firewall_spec.get('throughput', 'N/A'),
                'power_w': firewall_spec.get('power_w', 0),
                'quantity': 2,  # 双活
                'unit_price': firewall_spec['price'],
                'total_price': firewall_spec['price'] * 2,
                'vendor': firewall_spec.get('vendor', 'N/A'),
                'certification': firewall_spec.get('certification', 'N/A'),
                'device_type': firewall_spec.get('type', '防火墙'),
                'xinchuan_compliant': self.xinchuan_mode != 'off'
            })
        
        # 存储设备 - 根据数据量计算
        data_size_tb = analysis.get('total_data_size_tb', 1)
        replica_count = 3  # 3副本
        backup_ratio = 2   # 备份数据是原数据的2倍
        
        # 计算总存储需求（数据 + 副本 + 备份 + 30%余量）
        total_storage_tb = int((data_size_tb * replica_count + data_size_tb * backup_ratio) * 1.3)
        
        if total_storage_tb > 0:
            # 选择存储类型（根据性能需求）
            if analysis.get('daily_transactions', 0) > 10000000:  # 高性能需求
                storage_key = 'ssd_nvme'
            else:
                storage_key = 'ssd_sata'
            
            storage_spec = self.storage_catalog.get(storage_key, self.storage_catalog['ssd_sata'])
            storage_unit_price = storage_spec.get('price_per_tb', 1200)
            
            equipment.append({
                'category': '存储设备',
                'name': f"{storage_spec.get('model', 'SSD存储')} ({total_storage_tb}TB)",
                'spec': f"{storage_spec.get('type', 'SSD')} {total_storage_tb}TB, IOPS {storage_spec.get('iops', 50000)}",
                # 前端显示字段
                'type': storage_spec.get('type', 'SSD'),
                'model': storage_spec.get('model', 'SSD存储'),
                'capacity_tb': total_storage_tb,
                'iops': storage_spec.get('iops', 50000),
                'throughput': f"{storage_spec.get('throughput_mbps', 3000)}MB/s",
                'unit_price_per_tb': storage_unit_price,
                'total_price': storage_unit_price * total_storage_tb,
                # 其他字段
                'storage_type': storage_spec.get('type', 'SSD'),
                'quantity': 1,
                'unit_price': storage_unit_price,
                'vendor': storage_spec.get('vendor', 'N/A'),
                'use_case': f'数据存储({data_size_tb}TB) + 副本({data_size_tb * replica_count}TB) + 备份({data_size_tb * backup_ratio}TB)',
                'xinchuan_compliant': self.xinchuan_mode != 'off'
            })
        
        return equipment
    
    def _calculate_cost_xinchuan(self, equipment_list, architecture):
        """计算成本(包含信创对比)"""
        # 计算硬件总成本（设备）
        hardware_cost = sum(item['total_price'] for item in equipment_list)
        
        # 计算基础设施详细清单
        infrastructure = self._calculate_infrastructure_detailed(equipment_list, architecture)
        infrastructure_cost = infrastructure['total_price']
        
        # 软件成本
        software_cost = 0
        software_items = []
        
        # 操作系统
        if self.xinchuan_mode in ['standard', 'strict', 'full']:
            # 信创模式:使用国产OS
            os_license = self.software_licenses['os_openeuler']  # 免费
            software_items.append({
                'name': os_license['name'],
                'quantity': architecture['database_nodes'] + architecture['proxy_nodes'],
                'unit_price': os_license['price_per_server'],
                'total': 0,
                'note': '开源免费,可选商业支持'
            })
        else:
            # 标准模式:使用RedHat
            os_license = self.software_licenses.get('os_redhat', {'name': 'Red Hat Enterprise Linux', 'price_per_server': 5000})
            os_total = os_license['price_per_server'] * (architecture['database_nodes'] + architecture['proxy_nodes'])
            software_cost += os_total
            software_items.append({
                'name': os_license['name'],
                'quantity': architecture['database_nodes'] + architecture['proxy_nodes'],
                'unit_price': os_license['price_per_server'],
                'total': os_total
            })
        
        # 数据库许可证（非信创模式可能需要）
        if self.xinchuan_mode == 'off':
            db_license_cost = 50000 * architecture['database_nodes']  # 假设每节点5万
            software_cost += db_license_cost
            software_items.append({
                'name': 'TDSQL Enterprise License',
                'quantity': architecture['database_nodes'],
                'unit_price': 50000,
                'total': db_license_cost
            })
        
        total_cost = hardware_cost + infrastructure_cost + software_cost
        
        # 信创成本对比
        cost_comparison = self._calculate_cost_comparison(total_cost)
        
        return {
            'hardware_cost': hardware_cost,
            'infrastructure_cost': infrastructure_cost,
            'infrastructure_items': infrastructure['items'],  # 详细基础设施清单
            'software_cost': software_cost,
            'software_items': software_items,
            'total_initial_cost': total_cost,
            'xinchuan_comparison': cost_comparison
        }
    
    def _calculate_infrastructure_detailed(self, equipment_list, architecture):
        """计算详细的基础设施清单"""
        import math
        
        # 统计服务器和网络设备数量
        servers = [e for e in equipment_list if '服务器' in e.get('category', '')]
        network_devices = [e for e in equipment_list if e.get('category') in ['核心交换机', '接入交换机', '安全防火墙']]
        
        total_servers = sum(s.get('quantity', 1) for s in servers)
        total_network = sum(n.get('quantity', 1) for n in network_devices)
        
        # 计算功率（服务器按平均500W，网络设备按150W）
        total_power_w = sum(s.get('power_w', 500) * s.get('quantity', 1) for s in servers)
        total_power_w += sum(n.get('power_w', 150) * n.get('quantity', 1) for n in network_devices)
        total_power_kw = total_power_w / 1000
        
        # 计算机柜数量（服务器2U，网络设备1U）
        total_u = total_servers * 2 + total_network * 1
        rack_count = max(1, math.ceil(total_u / 42))
        
        items = []
        
        # 机柜
        rack_price = self.infrastructure_costs['rack_42u']['price']
        items.append({
            'category': '机柜',
            'name': self.infrastructure_costs['rack_42u']['name'],
            'type': self.infrastructure_costs['rack_42u']['name'],  # 前端显示字段
            'spec': f"42U标准机柜，共{total_u}U设备",
            'quantity': rack_count,
            'unit_price': rack_price,
            'total_price': rack_price * rack_count
        })
        
        # PDU（每机柜2个）
        pdu_count = rack_count * 2
        pdu_price = self.infrastructure_costs['pdu']['price']
        items.append({
            'category': 'PDU',
            'name': self.infrastructure_costs['pdu']['name'],
            'type': self.infrastructure_costs['pdu']['name'],  # 前端显示字段
            'spec': '双路供电，每机柜2个',
            'quantity': pdu_count,
            'unit_price': pdu_price,
            'total_price': pdu_price * pdu_count
        })
        
        # UPS
        ups_kw = math.ceil(total_power_kw * 1.5)  # 1.5倍冗余
        ups_price_per_kw = self.infrastructure_costs['ups_per_kw']['price_per_kw']
        items.append({
            'category': 'UPS',
            'name': self.infrastructure_costs['ups_per_kw']['name'],
            'type': self.infrastructure_costs['ups_per_kw']['name'],  # 前端显示字段
            'spec': f'{ups_kw}kW 在线式UPS',
            'quantity': 1,
            'capacity_kw': ups_kw,
            'unit_price': ups_price_per_kw * ups_kw,
            'total_price': ups_price_per_kw * ups_kw
        })
        
        # 网线及配件
        cable_price = self.infrastructure_costs['cable_per_server']['price']
        items.append({
            'category': '网线配件',
            'name': self.infrastructure_costs['cable_per_server']['name'],
            'type': self.infrastructure_costs['cable_per_server']['name'],  # 前端显示字段
            'spec': '网线、跳线、理线架等',
            'quantity': total_servers + total_network,
            'unit_price': cable_price,
            'total_price': cable_price * (total_servers + total_network)
        })
        
        # 部署实施
        deployment_price = self.infrastructure_costs['deployment_per_server']['price']
        items.append({
            'category': '实施费用',
            'name': self.infrastructure_costs['deployment_per_server']['name'],
            'type': self.infrastructure_costs['deployment_per_server']['name'],  # 前端显示字段
            'spec': '上架、布线、调试',
            'quantity': total_servers,
            'unit_price': deployment_price,
            'total_price': deployment_price * total_servers
        })
        
        # 技术培训
        training_price = self.infrastructure_costs['training']['price']
        items.append({
            'category': '技术培训',
            'name': self.infrastructure_costs['training']['name'],
            'type': self.infrastructure_costs['training']['name'],  # 前端显示字段
            'spec': '3天现场培训',
            'quantity': 1,
            'unit_price': training_price,
            'total_price': training_price
        })
        
        total_infrastructure_cost = sum(item['total_price'] for item in items)
        
        return {
            'items': items,
            'total_price': total_infrastructure_cost,
            'rack_count': rack_count,
            'total_power_kw': total_power_kw
        }
    
    def _calculate_cost_comparison(self, xinchuan_cost):
        """计算信创vs国外品牌成本对比
        
        注意: 这个函数已废弃,实际成本对比在app_simple.py中使用相同架构计算
        保留此函数仅为向后兼容
        """
        if self.xinchuan_mode == 'off':
            return None
        
        # 这里的估算已不再使用,实际对比基于相同架构的真实设备价格
        return {
            'xinchuan_cost': xinchuan_cost,
            'international_cost': 0,  # 由外部计算
            'cost_savings': 0,
            'savings_percent': 0,
            'note': '成本对比需要基于相同架构的真实设备价格计算'
        }
    
    def _generate_architecture_diagram(self, architecture):
        """生成架构图描述"""
        return {
            'layers': [
                '接入层: 核心交换机(双活)',
                f'代理层: {architecture["proxy_nodes"]}个代理节点',
                f'数据库层: {architecture["database_nodes"]}个数据库节点',
                '监控层: 监控服务器'
            ],
            'ha_design': '双活架构,故障自动切换'
        }
    
    def _generate_recommendations_xinchuan(self, analysis, architecture):
        """生成建议(包含信创建议)"""
        recommendations = []
        
        if self.xinchuan_mode in ['standard', 'strict', 'full']:
            recommendations.append({
                'category': '信创合规',
                'priority': 'high',
                'content': f'当前方案符合{self.xc_catalog.get_xinchuan_recommendation(self.xinchuan_mode)["description"]},满足国家信创要求'
            })
            
            if self.xinchuan_mode == 'standard':
                recommendations.append({
                    'category': '升级建议',
                    'priority': 'medium',
                    'content': '可考虑升级到严格信创模式(全国产CPU),进一步提升自主可控能力'
                })
        else:
            recommendations.append({
                'category': '信创建议',
                'priority': 'medium',
                'content': '建议启用信创模式,使用国产化设备,享受成本优势(节约8-15%)和政策支持'
            })
        
        # 性能优化建议
        recommendations.append({
            'category': '性能优化',
            'priority': 'high',
            'content': f'建议采用{architecture["node_spec"]}规格,配合NVMe SSD获得最佳性能'
        })
        
        return recommendations


# 使用示例
if __name__ == '__main__':
    print("=" * 70)
    print("TDSQL 部署资源预测系统 - 信创版本")
    print("=" * 70)
    
    # 测试输入
    test_input = {
        'data_size_gb': 5000,
        'transactions_per_day': 5000000,
        'max_connections': 2000,
        'business_type': 'OLTP',
        'high_availability': True,
        'disaster_recovery': False
    }
    
    # 测试不同信创模式
    modes = ['off', 'standard', 'strict', 'full']
    
    for mode in modes:
        print(f"\n{'=' * 70}")
        print(f"测试模式: {mode}")
        print(f"{'=' * 70}")
        
        predictor = DeploymentResourcePredictorXinChuan(xinchuan_mode=mode)
        result = predictor.predict(test_input)
        
        # 显示信创信息
        xc_info = result['xinchuan_info']
        print(f"\n信创模式: {xc_info['mode']}")
        if xc_info['enabled']:
            print(f"服务器品牌: {', '.join(xc_info['servers'])}")
            print(f"网络设备: {', '.join(xc_info['network'])}")
            print(f"CPU芯片: {', '.join(xc_info['cpu'])}")
            print(f"成本优势: {xc_info['cost_advantage']}")
        
        # 显示设备清单(前3项)
        print(f"\n设备清单示例:")
        for item in result['equipment_list'][:3]:
            print(f"  - {item['name']} x{item['quantity']}")
            print(f"    厂商: {item['vendor']}, 认证: {item['certification']}")
            print(f"    价格: ¥{item['total_price']:,}")
        
        # 显示成本对比
        cost = result['cost_breakdown']
        print(f"\n总成本: ¥{cost['total_initial_cost']:,.0f}")
        if cost['xinchuan_comparison']:
            comp = cost['xinchuan_comparison']
            print(f"  国外品牌参考价: ¥{comp['international_cost']:,.0f}")
            print(f"  💰 节约: ¥{comp['cost_savings']:,.0f} ({comp['savings_percent']}%)")
            print(f"  {comp['note']}")
