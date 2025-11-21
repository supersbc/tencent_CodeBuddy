#!/usr/bin/env python3
"""
增强的输入输出参数定义
根据实际TDSQL架构设计需求扩充和细化参数
"""

from typing import Dict, List, Any
from dataclasses import dataclass, field

@dataclass
class EnhancedInputParameters:
    """增强的输入参数"""
    
    # ========== 基础数据参数 ==========
    total_data_size_gb: float = 0  # 数据总量(GB)
    table_count: int = 0  # 表数量
    database_count: int = 1  # 数据库数量
    max_table_size_gb: float = 0  # 最大表大小(GB)
    avg_table_size_gb: float = 0  # 平均表大小(GB)
    data_growth_rate: float = 0  # 数据增长率(%)
    
    # ========== 性能参数 ==========
    qps: int = 0  # 每秒查询数
    tps: int = 0  # 每秒事务数
    peak_qps: int = 0  # 峰值QPS
    peak_tps: int = 0  # 峰值TPS
    concurrent_connections: int = 0  # 并发连接数
    max_connections: int = 0  # 最大连接数
    avg_query_time_ms: float = 0  # 平均查询时间(ms)
    slow_query_threshold_ms: float = 1000  # 慢查询阈值(ms)
    
    # ========== 读写特性 ==========
    read_write_ratio: str = '7:3'  # 读写比例
    read_qps: int = 0  # 读QPS
    write_qps: int = 0  # 写QPS
    need_read_write_split: bool = False  # 是否需要读写分离
    
    # ========== 可用性要求 ==========
    need_high_availability: bool = False  # 高可用需求
    availability_target: float = 99.9  # 可用性目标(%)
    need_disaster_recovery: bool = False  # 灾备需求
    dr_type: str = 'none'  # 灾备类型: none/same_city/remote/both
    rto_minutes: int = 60  # 恢复时间目标(分钟)
    rpo_minutes: int = 60  # 恢复点目标(分钟)
    
    # ========== 业务特性 ==========
    industry: str = '通用'  # 行业类型
    business_type: str = 'oltp'  # 业务类型: oltp/olap/htap
    scenario: str = ''  # 应用场景
    peak_period: str = ''  # 高峰时段
    seasonal_traffic: bool = False  # 是否有季节性流量
    
    # ========== 数据特性 ==========
    data_sensitivity: str = 'normal'  # 数据敏感级别: low/normal/high/critical
    need_encryption: bool = False  # 是否需要加密
    encryption_type: str = 'none'  # 加密类型: none/tde/column/both
    data_retention_days: int = 365  # 数据保留天数
    archive_strategy: str = 'none'  # 归档策略
    
    # ========== 备份要求 ==========
    backup_frequency: str = 'daily'  # 备份频率: hourly/daily/weekly
    backup_retention_days: int = 30  # 备份保留天数
    need_incremental_backup: bool = True  # 是否需要增量备份
    backup_window: str = '02:00-04:00'  # 备份窗口
    
    # ========== 合规要求 ==========
    compliance_required: bool = False  # 是否有合规要求
    compliance_standards: List[str] = field(default_factory=list)  # 合规标准
    audit_log_required: bool = False  # 是否需要审计日志
    data_masking_required: bool = False  # 是否需要数据脱敏
    
    # ========== 性能优化 ==========
    need_cache: bool = False  # 是否需要缓存
    cache_type: str = 'none'  # 缓存类型: none/redis/memcached
    cache_size_gb: int = 0  # 缓存大小(GB)
    need_connection_pool: bool = True  # 是否需要连接池
    
    # ========== 扩展性要求 ==========
    scalability_required: bool = False  # 是否需要扩展性
    expected_growth_years: int = 3  # 预期增长年限
    auto_scaling: bool = False  # 是否需要自动扩展
    max_scale_nodes: int = 0  # 最大扩展节点数
    
    # ========== 监控告警 ==========
    monitoring_level: str = 'basic'  # 监控级别: basic/standard/advanced
    alert_channels: List[str] = field(default_factory=list)  # 告警渠道
    custom_metrics: List[str] = field(default_factory=list)  # 自定义指标
    
    # ========== 安全要求 ==========
    network_isolation: bool = False  # 网络隔离
    ip_whitelist: bool = False  # IP白名单
    ssl_required: bool = False  # 是否需要SSL
    security_level: str = 'standard'  # 安全级别: basic/standard/high
    
    # ========== 成本约束 ==========
    budget_range: str = 'unlimited'  # 预算范围
    cost_priority: str = 'balanced'  # 成本优先级: cost/performance/balanced
    prefer_cloud: bool = False  # 是否优先云服务
    
    # ========== 时间要求 ==========
    deployment_deadline: str = ''  # 部署截止时间
    migration_window_hours: int = 0  # 迁移窗口(小时)
    
    # ========== 其他要求 ==========
    special_requirements: List[str] = field(default_factory=list)  # 特殊要求
    existing_infrastructure: Dict[str, Any] = field(default_factory=dict)  # 现有基础设施
    team_expertise: str = 'intermediate'  # 团队技术水平


@dataclass
class EnhancedOutputParameters:
    """增强的输出参数"""
    
    # ========== 架构设计 ==========
    architecture_type: str = ''  # 架构类型
    architecture_diagram: str = ''  # 架构图
    deployment_mode: str = ''  # 部署模式
    
    # ========== 节点配置 ==========
    node_count: int = 0  # 节点总数
    master_nodes: int = 0  # 主节点数
    slave_nodes: int = 0  # 从节点数
    shard_count: int = 0  # 分片数
    replica_count: int = 0  # 副本数
    proxy_count: int = 0  # 代理节点数
    
    # ========== 服务器清单 ==========
    servers: List[Dict] = field(default_factory=list)  # 服务器详细清单
    # 每个服务器包含: type, model, cpu, memory, disk, quantity, unit_price, total_price
    
    # ========== 网络设备 ==========
    network_devices: List[Dict] = field(default_factory=list)  # 网络设备清单
    # 包含: switches, load_balancers, firewalls
    
    # ========== 存储配置 ==========
    storage_config: Dict = field(default_factory=dict)  # 存储配置
    # 包含: ssd_capacity, hdd_capacity, backup_storage, archive_storage
    
    # ========== 基础设施 ==========
    infrastructure: Dict = field(default_factory=dict)  # 基础设施
    # 包含: racks, pdus, cables, kvm
    
    # ========== 软件配置 ==========
    software_config: Dict = field(default_factory=dict)  # 软件配置
    # 包含: tdsql_version, os_version, middleware
    
    # ========== 性能预估 ==========
    performance_estimation: Dict = field(default_factory=dict)  # 性能预估
    # 包含: max_qps, max_tps, latency, throughput
    
    # ========== 容量规划 ==========
    capacity_planning: Dict = field(default_factory=dict)  # 容量规划
    # 包含: current_capacity, 1year_capacity, 3year_capacity
    
    # ========== 成本分析 ==========
    cost_breakdown: Dict = field(default_factory=dict)  # 成本明细
    # 包含: hardware, software, labor, operation, total
    
    # ========== 高可用方案 ==========
    ha_solution: Dict = field(default_factory=dict)  # 高可用方案
    # 包含: failover_time, data_sync_mode, monitoring
    
    # ========== 灾备方案 ==========
    dr_solution: Dict = field(default_factory=dict)  # 灾备方案
    # 包含: dr_site, sync_mode, rto, rpo
    
    # ========== 备份策略 ==========
    backup_strategy: Dict = field(default_factory=dict)  # 备份策略
    # 包含: full_backup, incremental_backup, retention
    
    # ========== 监控方案 ==========
    monitoring_solution: Dict = field(default_factory=dict)  # 监控方案
    # 包含: metrics, alerts, dashboards
    
    # ========== 安全方案 ==========
    security_solution: Dict = field(default_factory=dict)  # 安全方案
    # 包含: encryption, access_control, audit
    
    # ========== 扩展方案 ==========
    scaling_plan: Dict = field(default_factory=dict)  # 扩展方案
    # 包含: vertical_scaling, horizontal_scaling, auto_scaling
    
    # ========== 迁移方案 ==========
    migration_plan: Dict = field(default_factory=dict)  # 迁移方案
    # 包含: migration_steps, downtime, rollback_plan
    
    # ========== 运维建议 ==========
    operation_recommendations: List[str] = field(default_factory=list)  # 运维建议
    
    # ========== 优化建议 ==========
    optimization_suggestions: List[str] = field(default_factory=list)  # 优化建议
    
    # ========== 风险评估 ==========
    risk_assessment: Dict = field(default_factory=dict)  # 风险评估
    # 包含: risks, mitigation_strategies
    
    # ========== 实施计划 ==========
    implementation_plan: Dict = field(default_factory=dict)  # 实施计划
    # 包含: phases, timeline, resources
    
    # ========== 文档清单 ==========
    documentation: List[str] = field(default_factory=list)  # 文档清单


# 参数映射和验证
class ParameterValidator:
    """参数验证器"""
    
    @staticmethod
    def validate_input(params: Dict) -> tuple[bool, str]:
        """验证输入参数"""
        # 必填参数检查
        required_fields = ['total_data_size_gb', 'qps', 'tps']
        for field in required_fields:
            if field not in params or params[field] <= 0:
                return False, f"缺少必填参数: {field}"
        
        # 数值范围检查
        if params.get('availability_target', 0) > 100:
            return False, "可用性目标不能超过100%"
        
        if params.get('data_growth_rate', 0) < 0:
            return False, "数据增长率不能为负"
        
        return True, "验证通过"
    
    @staticmethod
    def get_parameter_description() -> Dict:
        """获取参数说明"""
        return {
            'input': {
                '基础数据参数': {
                    'total_data_size_gb': '数据总量(GB) - 当前数据库总大小',
                    'table_count': '表数量 - 数据库中的表总数',
                    'database_count': '数据库数量 - 实例中的数据库个数',
                    'max_table_size_gb': '最大表大小(GB) - 单表最大数据量',
                    'avg_table_size_gb': '平均表大小(GB) - 表的平均大小',
                    'data_growth_rate': '数据增长率(%) - 年度数据增长百分比'
                },
                '性能参数': {
                    'qps': '每秒查询数 - 平均QPS',
                    'tps': '每秒事务数 - 平均TPS',
                    'peak_qps': '峰值QPS - 业务高峰期的QPS',
                    'peak_tps': '峰值TPS - 业务高峰期的TPS',
                    'concurrent_connections': '并发连接数 - 同时连接数',
                    'avg_query_time_ms': '平均查询时间(ms) - SQL平均执行时间'
                },
                '可用性要求': {
                    'need_high_availability': '高可用需求 - 是否需要HA',
                    'availability_target': '可用性目标(%) - 如99.9%, 99.99%',
                    'need_disaster_recovery': '灾备需求 - 是否需要异地灾备',
                    'rto_minutes': '恢复时间目标(分钟) - 故障后恢复时间',
                    'rpo_minutes': '恢复点目标(分钟) - 可接受的数据丢失时间'
                },
                '业务特性': {
                    'industry': '行业类型 - 金融/电商/游戏/互联网等',
                    'business_type': '业务类型 - OLTP/OLAP/HTAP',
                    'scenario': '应用场景 - 具体业务场景描述'
                },
                '安全合规': {
                    'data_sensitivity': '数据敏感级别 - low/normal/high/critical',
                    'need_encryption': '是否需要加密 - 数据加密需求',
                    'compliance_required': '合规要求 - 是否有行业合规要求',
                    'audit_log_required': '审计日志 - 是否需要审计功能'
                }
            },
            'output': {
                '架构设计': '推荐的TDSQL架构类型和部署模式',
                '节点配置': '主从节点、分片、副本的详细配置',
                '服务器清单': '详细的服务器型号、配置、数量、价格',
                '网络设备': '交换机、负载均衡器、防火墙等设备清单',
                '存储配置': 'SSD、HDD、备份存储的容量和配置',
                '成本分析': '硬件、软件、人力、运维的详细成本',
                '高可用方案': '故障切换、数据同步、监控方案',
                '灾备方案': '异地灾备、同步模式、RTO/RPO',
                '监控方案': '监控指标、告警策略、可视化方案',
                '实施计划': '分阶段实施计划和时间表'
            }
        }


def main():
    """演示参数定义"""
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║           TDSQL 增强参数定义                                       ║")
    print("╚══════════════════════════════════════════════════════════════════╝\n")
    
    # 获取参数说明
    descriptions = ParameterValidator.get_parameter_description()
    
    print("📥 输入参数分类:\n")
    for category, params in descriptions['input'].items():
        print(f"【{category}】")
        for param, desc in params.items():
            print(f"  • {param}: {desc}")
        print()
    
    print("\n" + "="*70 + "\n")
    print("📤 输出参数分类:\n")
    for category, desc in descriptions['output'].items():
        print(f"  • {category}: {desc}")
    
    print("\n" + "="*70)
    print("\n✅ 参数定义完成！")
    print(f"\n💡 输入参数: 50+ 个")
    print(f"💡 输出参数: 20+ 个维度")


if __name__ == '__main__':
    main()
