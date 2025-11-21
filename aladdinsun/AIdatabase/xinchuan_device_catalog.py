"""
信创国产化设备配置库
支持国产服务器、芯片、网络设备、存储等
"""

class XinChuangDeviceCatalog:
    """信创国产化设备目录"""
    
    def __init__(self):
        # 国产服务器配置库
        self.server_catalog = {
            'db_small': {
                'name': '浪潮 NF5280M6',  # 国产品牌
                'cpu_cores': 8, 
                'cpu_model': '鲲鹏920 2.6GHz',  # 华为鲲鹏
                'memory_gb': 32, 
                'disk_gb': 1000, 
                'disk_type': 'SSD SATA',
                'network': '双万兆网卡',
                'price': 26000,  # 国产设备更有价格优势
                'power_w': 320,
                'use_case': '小型数据库节点',
                'vendor': '浪潮',
                'certification': '信创认证'
            },
            'db_small_alt': {
                'name': '华为 TaiShan 200 2280',
                'cpu_cores': 8,
                'cpu_model': '鲲鹏920 2.6GHz',
                'memory_gb': 32,
                'disk_gb': 1000,
                'disk_type': 'SSD SATA',
                'network': '双万兆网卡',
                'price': 27000,
                'power_w': 310,
                'use_case': '小型数据库节点',
                'vendor': '华为',
                'certification': '信创认证'
            },
            'db_medium': {
                'name': '浪潮 NF8260M6',
                'cpu_cores': 16,
                'cpu_model': '鲲鹏920 3.0GHz',
                'memory_gb': 64,
                'disk_gb': 2000,
                'disk_type': 'SSD SATA',
                'network': '双万兆网卡',
                'price': 42000,
                'power_w': 480,
                'use_case': '中型数据库节点',
                'vendor': '浪潮',
                'certification': '信创认证'
            },
            'db_medium_alt': {
                'name': '联想 ThinkSystem SR650',
                'cpu_cores': 16,
                'cpu_model': '海光 EPYC 7542',  # 海光国产CPU
                'memory_gb': 64,
                'disk_gb': 2000,
                'disk_type': 'SSD SATA',
                'network': '双万兆网卡',
                'price': 43000,
                'power_w': 470,
                'use_case': '中型数据库节点',
                'vendor': '联想',
                'certification': '信创认证'
            },
            'db_large': {
                'name': '浪潮 NF8480M6',
                'cpu_cores': 32,
                'cpu_model': '鲲鹏920 3.0GHz (双路)',
                'memory_gb': 128,
                'disk_gb': 4000,
                'disk_type': 'NVMe SSD',
                'network': '双万兆网卡',
                'price': 78000,
                'power_w': 700,
                'use_case': '大型数据库节点',
                'vendor': '浪潮',
                'certification': '信创认证'
            },
            'db_large_alt': {
                'name': '华为 TaiShan 200 2480',
                'cpu_cores': 32,
                'cpu_model': '鲲鹏920 3.0GHz (双路)',
                'memory_gb': 128,
                'disk_gb': 4000,
                'disk_type': 'NVMe SSD',
                'network': '双万兆网卡',
                'price': 80000,
                'power_w': 680,
                'use_case': '大型数据库节点',
                'vendor': '华为',
                'certification': '信创认证'
            },
            'db_xlarge': {
                'name': '浪潮 NF8680M6 (四路)',
                'cpu_cores': 64,
                'cpu_model': '鲲鹏920 3.0GHz (四路)',
                'memory_gb': 256,
                'disk_gb': 8000,
                'disk_type': 'NVMe SSD',
                'network': '双万兆网卡',
                'price': 165000,
                'power_w': 1150,
                'use_case': '超大型数据库节点',
                'vendor': '浪潮',
                'certification': '信创认证'
            },
            'db_xlarge_alt': {
                'name': '华为 TaiShan 200 5280 (四路)',
                'cpu_cores': 64,
                'cpu_model': '鲲鹏920 3.0GHz (四路)',
                'memory_gb': 256,
                'disk_gb': 8000,
                'disk_type': 'NVMe SSD',
                'network': '双万兆网卡',
                'price': 170000,
                'power_w': 1100,
                'use_case': '超大型数据库节点',
                'vendor': '华为',
                'certification': '信创认证'
            },
            'app_server': {
                'name': '浪潮 NF5180M6',
                'cpu_cores': 4,
                'cpu_model': '飞腾 FT-2000+/64',  # 飞腾国产CPU
                'memory_gb': 16,
                'disk_gb': 500,
                'disk_type': 'SSD SATA',
                'network': '双千兆网卡',
                'price': 16500,
                'power_w': 230,
                'use_case': '应用服务器',
                'vendor': '浪潮',
                'certification': '信创认证'
            },
            'app_server_alt': {
                'name': '联想 ThinkSystem SR258',
                'cpu_cores': 4,
                'cpu_model': '龙芯 3C5000',  # 龙芯国产CPU
                'memory_gb': 16,
                'disk_gb': 500,
                'disk_type': 'SSD SATA',
                'network': '双千兆网卡',
                'price': 17000,
                'power_w': 240,
                'use_case': '应用服务器',
                'vendor': '联想',
                'certification': '信创认证'
            },
            'proxy_server': {
                'name': '浪潮 NF5280M6',
                'cpu_cores': 8,
                'cpu_model': '鲲鹏920 2.6GHz',
                'memory_gb': 32,
                'disk_gb': 500,
                'disk_type': 'SSD SATA',
                'network': '双万兆网卡',
                'price': 20000,
                'power_w': 280,
                'use_case': 'TDSQL代理节点',
                'vendor': '浪潮',
                'certification': '信创认证'
            },
            'monitor_server': {
                'name': '浪潮 NF5180M6',
                'cpu_cores': 4,
                'cpu_model': '飞腾 FT-2000+/64',
                'memory_gb': 16,
                'disk_gb': 1000,
                'disk_type': 'SSD SATA',
                'network': '双千兆网卡',
                'price': 18500,
                'power_w': 230,
                'use_case': '监控服务器',
                'vendor': '浪潮',
                'certification': '信创认证'
            }
        }
        
        # 国产网络设备配置库
        self.network_catalog = {
            'core_switch_10g': {
                'name': '华为 CE6800-48S4Q-EI',  # 华为核心交换机
                'type': '核心交换机',
                'ports': 48,
                'speed': '10Gbps',
                'uplink': '4x40Gbps',
                'price': 75000,
                'power_w': 230,
                'vendor': '华为',
                'certification': '信创认证'
            },
            'core_switch_10g_alt': {
                'name': 'H3C S6800-54HF',  # 新华三
                'type': '核心交换机',
                'ports': 48,
                'speed': '10Gbps',
                'uplink': '6x40Gbps',
                'price': 78000,
                'power_w': 240,
                'vendor': 'H3C(新华三)',
                'certification': '信创认证'
            },
            'core_switch_40g': {
                'name': '华为 CE12800',
                'type': '核心交换机',
                'ports': 36,
                'speed': '40Gbps',
                'uplink': '100Gbps',
                'price': 250000,
                'power_w': 380,
                'vendor': '华为',
                'certification': '信创认证'
            },
            'access_switch_1g': {
                'name': '华为 S5735-L48P4XE-A',
                'type': '接入交换机',
                'ports': 48,
                'speed': '1Gbps',
                'uplink': '4x10Gbps',
                'price': 10500,
                'power_w': 90,
                'vendor': '华为',
                'certification': '信创认证'
            },
            'access_switch_1g_alt': {
                'name': 'H3C S5560-48C-PWR-EI',
                'type': '接入交换机',
                'ports': 48,
                'speed': '1Gbps',
                'uplink': '4x10Gbps',
                'price': 11000,
                'power_w': 95,
                'vendor': 'H3C(新华三)',
                'certification': '信创认证'
            },
            'access_switch_10g': {
                'name': '华为 S6730-H48X6C',
                'type': '接入交换机',
                'ports': 48,
                'speed': '10Gbps',
                'uplink': '6x40Gbps',
                'price': 40000,
                'power_w': 180,
                'vendor': '华为',
                'certification': '信创认证'
            },
            'firewall': {
                'name': '天融信 NGFW4000-UF',  # 天融信国产防火墙
                'type': '防火墙',
                'throughput': '10Gbps',
                'price': 100000,
                'power_w': 140,
                'vendor': '天融信',
                'certification': '信创认证'
            },
            'firewall_alt': {
                'name': '启明星辰 天清汉马USG6000',
                'type': '防火墙',
                'throughput': '10Gbps',
                'price': 105000,
                'power_w': 135,
                'vendor': '启明星辰',
                'certification': '信创认证'
            },
            'load_balancer': {
                'name': 'Array APV8600',  # Array国产负载均衡
                'type': '负载均衡器',
                'throughput': '20Gbps',
                'price': 130000,
                'power_w': 180,
                'vendor': 'Array(阿莱)',
                'certification': '信创认证'
            },
            'load_balancer_alt': {
                'name': '深信服 AD3000',
                'type': '负载均衡器',
                'throughput': '20Gbps',
                'price': 135000,
                'power_w': 185,
                'vendor': '深信服',
                'certification': '信创认证'
            },
            'router': {
                'name': '华为 NetEngine 8000 M8',
                'type': '路由器',
                'throughput': '20Gbps',
                'price': 70000,
                'power_w': 160,
                'vendor': '华为',
                'certification': '信创认证'
            }
        }
        
        # 国产存储设备
        self.storage_catalog = {
            'ssd_sata': {
                'type': 'SATA SSD',
                'model': '长江存储 致钛 TiPlus5000',  # 国产存储
                'price_per_tb': 1100,
                'iops': 48000,
                'throughput_mbps': 540,
                'vendor': '长江存储',
                'certification': '信创认证'
            },
            'ssd_sata_alt': {
                'type': 'SATA SSD',
                'model': '光威 骁将 SSD',
                'price_per_tb': 1000,
                'iops': 45000,
                'throughput_mbps': 520,
                'vendor': '光威',
                'certification': '信创认证'
            },
            'ssd_nvme': {
                'type': 'NVMe SSD',
                'model': '长江存储 致钛 PC005 Active',
                'price_per_tb': 2200,
                'iops': 480000,
                'throughput_mbps': 6800,
                'vendor': '长江存储',
                'certification': '信创认证'
            },
            'ssd_nvme_alt': {
                'type': 'NVMe SSD',
                'model': '宏杉 MS7000 NVMe',
                'price_per_tb': 2300,
                'iops': 470000,
                'throughput_mbps': 6500,
                'vendor': '宏杉',
                'certification': '信创认证'
            },
            'hdd': {
                'type': 'SATA HDD',
                'model': '希捷 银河 Exos X18',
                'price_per_tb': 300,
                'iops': 150,
                'throughput_mbps': 250,
                'vendor': '希捷',
                'certification': '标准认证'
            }
        }
        
        # 国产软件许可证
        self.software_licenses = {
            'tdsql_enterprise': {
                'name': 'TDSQL企业版',
                'price_per_core': 3000,
                'annual_maintenance_rate': 0.20,
                'vendor': '腾讯',
                'certification': '信创认证'
            },
            'os_openeuler': {
                'name': 'openEuler 操作系统',  # 华为开源OS
                'price_per_server': 0,  # 开源免费
                'annual_maintenance_rate': 0,
                'vendor': '华为/openEuler社区',
                'certification': '信创认证',
                'note': '开源免费,可选商业支持'
            },
            'os_kylin': {
                'name': '银河麒麟 V10 服务器版',  # 麒麟OS
                'price_per_server': 3800,
                'annual_maintenance_rate': 0.15,
                'vendor': '麒麟软件',
                'certification': '信创认证'
            },
            'os_uos': {
                'name': '统信UOS V20 服务器版',  # 统信OS
                'price_per_server': 3500,
                'annual_maintenance_rate': 0.15,
                'vendor': '统信软件',
                'certification': '信创认证'
            },
            'monitoring_prometheus': {
                'name': 'Prometheus监控套件',
                'price_per_node': 0,  # 开源免费
                'annual_maintenance_rate': 0,
                'vendor': '开源社区',
                'certification': '开源软件',
                'note': '开源免费'
            },
            'monitoring_zabbix': {
                'name': 'Zabbix监控系统',
                'price_per_node': 0,
                'annual_maintenance_rate': 0,
                'vendor': '开源社区',
                'certification': '开源软件',
                'note': '国产化常用监控'
            },
            'backup_software': {
                'name': '爱数备份容灾系统',  # 国产备份软件
                'price_per_tb': 450,
                'annual_maintenance_rate': 0.15,
                'vendor': '爱数',
                'certification': '信创认证'
            },
            'backup_software_alt': {
                'name': '英方云备份',
                'price_per_tb': 480,
                'annual_maintenance_rate': 0.15,
                'vendor': '英方',
                'certification': '信创认证'
            }
        }
        
        # 国产数据库(可选)
        self.database_options = {
            'gaussdb': {
                'name': 'GaussDB (华为)',
                'price_per_core': 2800,
                'annual_maintenance_rate': 0.18,
                'vendor': '华为',
                'certification': '信创认证',
                'compatibility': 'PostgreSQL兼容'
            },
            'oceanbase': {
                'name': 'OceanBase (蚂蚁)',
                'price_per_core': 2500,
                'annual_maintenance_rate': 0.18,
                'vendor': '蚂蚁集团',
                'certification': '信创认证',
                'compatibility': 'MySQL兼容'
            },
            'dameng': {
                'name': '达梦数据库 DM8',
                'price_per_core': 3200,
                'annual_maintenance_rate': 0.20,
                'vendor': '达梦',
                'certification': '信创认证',
                'compatibility': 'Oracle兼容'
            }
        }
        
    def get_xinchuan_recommendation(self, requirement_level='standard'):
        """
        获取信创推荐方案
        
        Args:
            requirement_level: 信创要求级别
                - 'standard': 标准信创(服务器+网络国产化)
                - 'strict': 严格信创(全栈国产化,包括CPU)
                - 'full': 完全信创(所有软硬件国产化)
        """
        recommendations = {
            'standard': {
                'description': '标准信创方案',
                'servers': ['浪潮', '华为', '联想'],
                'network': ['华为', 'H3C'],
                'storage': ['长江存储', '光威'],
                'os': ['openEuler(免费)', '银河麒麟', '统信UOS'],
                'cpu': ['鲲鹏920', '海光EPYC', '飞腾'],
                'cost_advantage': '相比国外品牌节约 8-15%'
            },
            'strict': {
                'description': '严格信创方案(全国产CPU)',
                'servers': ['浪潮', '华为'],
                'network': ['华为', 'H3C'],
                'storage': ['长江存储'],
                'os': ['openEuler', '银河麒麟'],
                'cpu': ['鲲鹏920', '飞腾', '龙芯'],
                'cost_advantage': '相比国外品牌节约 5-12%'
            },
            'full': {
                'description': '完全信创方案(全栈国产)',
                'servers': ['浪潮', '华为'],
                'network': ['华为'],
                'storage': ['长江存储'],
                'os': ['openEuler', '银河麒麟'],
                'cpu': ['鲲鹏920'],
                'database': ['GaussDB', 'OceanBase'],
                'security': ['天融信', '启明星辰'],
                'cost_advantage': '相比国外品牌节约 3-10%',
                'note': '完全符合国家信创要求'
            }
        }
        
        return recommendations.get(requirement_level, recommendations['standard'])
    
    def get_vendor_comparison(self):
        """获取国产vs国外品牌对比"""
        return {
            '服务器': {
                '国产品牌': ['浪潮(市占率第1)', '华为', '联想', '新华三'],
                '国外品牌': ['Dell', 'HP', 'IBM'],
                '优势': '价格低8-15%,政策支持,售后本土化',
                '技术成熟度': '已达国际主流水平'
            },
            'CPU芯片': {
                '国产品牌': ['鲲鹏920(ARM)', '海光(x86)', '飞腾(ARM)', '龙芯(MIPS)'],
                '国外品牌': ['Intel Xeon', 'AMD EPYC'],
                '优势': '自主可控,安全可靠,生态逐步完善',
                '技术成熟度': '鲲鹏/海光已可替代主流应用'
            },
            '网络设备': {
                '国产品牌': ['华为(全球第1)', 'H3C', '锐捷'],
                '国外品牌': ['Cisco', 'Juniper'],
                '优势': '技术领先,价格优势明显',
                '技术成熟度': '已超越国外品牌'
            },
            '存储': {
                '国产品牌': ['长江存储', '宏杉', '华为'],
                '国外品牌': ['Samsung', 'Intel', 'Western Digital'],
                '优势': '价格低10-20%,快速响应',
                '技术成熟度': '企业级应用已成熟'
            },
            '操作系统': {
                '国产品牌': ['openEuler(免费)', '银河麒麟', '统信UOS'],
                '国外品牌': ['Red Hat', 'SUSE'],
                '优势': 'openEuler免费,麒麟/UOS比RedHat便宜25%',
                '技术成熟度': '基于Linux,稳定可靠'
            }
        }


# 使用示例
if __name__ == '__main__':
    catalog = XinChuangDeviceCatalog()
    
    print("=" * 60)
    print("信创国产化设备推荐")
    print("=" * 60)
    
    # 获取推荐方案
    for level in ['standard', 'strict', 'full']:
        rec = catalog.get_xinchuan_recommendation(level)
        print(f"\n{rec['description']}:")
        print(f"  服务器: {', '.join(rec['servers'])}")
        print(f"  网络: {', '.join(rec['network'])}")
        print(f"  CPU: {', '.join(rec['cpu'])}")
        print(f"  成本优势: {rec['cost_advantage']}")
    
    print("\n" + "=" * 60)
    print("国产vs国外品牌对比")
    print("=" * 60)
    comparison = catalog.get_vendor_comparison()
    for category, info in comparison.items():
        print(f"\n{category}:")
        print(f"  国产: {', '.join(info['国产品牌'])}")
        print(f"  优势: {info['优势']}")
