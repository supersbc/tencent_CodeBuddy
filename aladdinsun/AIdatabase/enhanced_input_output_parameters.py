#!/usr/bin/env python3
"""
增强的输入输出参数定义
支持多系统环境、复杂部署拓扑、详细的架构输出
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime
import json


@dataclass
class EnhancedInputParameters:
    """增强的输入参数"""
    
    # ========== 基础信息 ==========
    project_name: str = ""
    project_code: str = ""
    submitter: str = ""
    submit_date: str = ""
    
    # ========== 多系统环境 ==========
    environment_name: str = ""  # 环境名称
    total_systems: int = 1  # 系统总数
    systems: List[Dict[str, Any]] = field(default_factory=list)  # 系统列表
    
    # 每个系统包含:
    # - system_name: 系统名称
    # - system_type: 系统类型（核心/辅助/外围）
    # - business_module: 业务模块
    # - data_size_gb: 数据量(GB)
    # - table_count: 表数量
    # - qps: QPS
    # - tps: TPS
    # - peak_qps: 峰值QPS
    # - connections: 连接数
    # - availability_requirement: 可用性要求
    # - data_sensitivity: 数据敏感度
    # - backup_requirement: 备份要求
    
    # ========== 整体统计（自动计算） ==========
    total_data_size_tb: float = 0.0
    total_qps: int = 0
    total_tps: int = 0
    total_connections: int = 0
    max_single_system_qps: int = 0
    
    # ========== 部署拓扑 ==========
    deployment_mode: str = "单中心"  # 单中心、同城双中心、同城多中心、两地三中心、三地五中心
    
    # 同城部署
    same_city_centers: int = 1
    same_city_distance_km: float = 0.0
    same_city_network_latency_ms: float = 0.0
    same_city_bandwidth_mbps: int = 0
    
    # 异地部署
    remote_centers: int = 0
    remote_regions: List[str] = field(default_factory=list)  # 异地区域列表
    remote_distance_km: float = 0.0
    remote_network_latency_ms: float = 0.0
    remote_bandwidth_mbps: int = 0
    
    # 数据中心详情
    data_centers: List[Dict[str, Any]] = field(default_factory=list)
    
    # ========== 容灾配置 ==========
    disaster_recovery_type: str = "冷备"  # 冷备、温备、热备、主备、双活、多活
    sync_mode: str = "异步"  # 异步、半同步、同步、强同步
    rpo_seconds: int = 3600  # 恢复点目标（秒）
    rto_seconds: int = 7200  # 恢复时间目标（秒）
    
    # 故障切换
    auto_failover: bool = False
    failover_time_seconds: int = 0
    auto_failback: bool = False
    
    # ========== 网络架构 ==========
    network_architecture: str = "专线"  # 专线、VPN、公网、云专线、SD-WAN
    network_redundancy: bool = False  # 网络冗余
    
    # ========== 业务特征 ==========
    industry: str = "通用"
    business_type: str = "OLTP"  # OLTP、OLAP、HTAP
    business_peak_hours: str = ""  # 业务高峰时段
    seasonal_peak: str = ""  # 季节性高峰
    growth_rate_yearly: float = 0.0  # 年增长率%
    
    # 读写特征
    read_write_ratio: str = "7:3"  # 读写比例
    read_qps: int = 0
    write_qps: int = 0
    
    # ========== 性能要求 ==========
    avg_response_time_ms: int = 100
    p95_response_time_ms: int = 200
    p99_response_time_ms: int = 500
    max_response_time_ms: int = 1000
    
    # ========== 可用性与合规 ==========
    availability_requirement: str = "99.9%"
    data_residency: str = ""  # 数据驻留要求
    compliance_requirements: List[str] = field(default_factory=list)  # 等保、分保、GDPR等
    
    # ========== 安全要求 ==========
    data_encryption_at_rest: bool = False  # 静态加密
    data_encryption_in_transit: bool = False  # 传输加密
    access_control: str = "基础"  # 基础、增强、严格
    audit_logging: bool = False  # 审计日志
    
    # ========== 备份策略 ==========
    backup_frequency: str = "每日"  # 每小时、每日、每周
    backup_retention_days: int = 7
    backup_type: str = "全量+增量"  # 全量、增量、全量+增量
    backup_location: str = "本地"  # 本地、异地、云端
    
    # ========== 扩展性 ==========
    horizontal_scaling: bool = False  # 水平扩展
    vertical_scaling: bool = False  # 垂直扩展
    auto_scaling: bool = False  # 自动伸缩
    max_scale_out_nodes: int = 0  # 最大扩展节点数
    
    # ========== 成本预算 ==========
    budget_level: str = "中"  # 低、中、高
    monthly_budget: float = 0.0
    prefer_cloud: bool = False  # 是否优先云服务
    
    # ========== 其他 ==========
    special_requirements: str = ""
    notes: str = ""


@dataclass
class DatabaseInstance:
    """数据库实例"""
    instance_id: str = ""
    instance_name: str = ""
    instance_type: str = "主实例"  # 主实例、只读实例、灾备实例
    
    # 规格
    cpu_cores: int = 0
    memory_gb: int = 0
    storage_gb: int = 0
    storage_type: str = "SSD"  # SSD、NVMe、HDD
    iops: int = 0
    
    # 网络
    network_bandwidth_mbps: int = 0
    max_connections: int = 0
    
    # 位置
    region: str = ""
    availability_zone: str = ""
    data_center_id: str = ""
    
    # 角色
    role: str = "主库"  # 主库、从库、备库
    is_active: bool = True
    
    # 性能
    estimated_qps: int = 0
    estimated_tps: int = 0


@dataclass
class ShardingConfig:
    """分片配置"""
    enable_sharding: bool = False
    
    # 分库
    database_sharding: bool = False
    database_count: int = 1
    database_sharding_key: str = ""
    
    # 分表
    table_sharding: bool = False
    table_count_per_db: int = 1
    table_sharding_key: str = ""
    
    # 分片策略
    sharding_algorithm: str = "hash"  # hash、range、list、consistent_hash
    
    # 路由
    routing_rules: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ReadWriteSplitConfig:
    """读写分离配置"""
    enable_read_write_split: bool = False
    
    # 只读实例
    readonly_instance_count: int = 0
    readonly_instances: List[DatabaseInstance] = field(default_factory=list)
    
    # 负载均衡
    load_balance_algorithm: str = "轮询"  # 轮询、加权轮询、最少连接、一致性哈希
    
    # 延迟控制
    max_replication_delay_ms: int = 1000
    delay_threshold_ms: int = 500


@dataclass
class HighAvailabilityConfig:
    """高可用配置"""
    ha_mode: str = "主从"  # 主从、MGR、Galera
    
    # 主从配置
    master_count: int = 1
    slave_count: int = 0
    
    # 故障检测
    health_check_interval_seconds: int = 5
    failure_detection_time_seconds: int = 15
    
    # 故障切换
    auto_failover: bool = False
    failover_time_seconds: int = 60
    vip_enabled: bool = False  # 虚拟IP
    
    # 数据一致性
    consistency_check: bool = False
    data_checksum: bool = False


@dataclass
class PerformanceOptimization:
    """性能优化配置"""
    
    # 缓存
    enable_query_cache: bool = False
    query_cache_size_mb: int = 0
    enable_redis_cache: bool = False
    redis_cache_size_gb: int = 0
    
    # 连接池
    connection_pool_size: int = 100
    max_connections: int = 1000
    
    # 索引优化
    auto_index_recommendation: bool = False
    
    # 查询优化
    slow_query_threshold_ms: int = 1000
    enable_query_rewrite: bool = False


@dataclass
class MonitoringConfig:
    """监控配置"""
    
    # 监控级别
    monitoring_level: str = "标准"  # 基础、标准、高级
    
    # 指标采集
    metrics_collection_interval_seconds: int = 60
    
    # 告警
    alert_enabled: bool = True
    alert_channels: List[str] = field(default_factory=list)  # 短信、邮件、电话、企业微信
    
    # 日志
    slow_query_log: bool = True
    error_log: bool = True
    audit_log: bool = False
    
    # 可视化
    dashboard_enabled: bool = True


@dataclass
class CostEstimation:
    """成本估算"""
    
    # 硬件成本
    server_cost_monthly: float = 0.0
    storage_cost_monthly: float = 0.0
    network_cost_monthly: float = 0.0
    
    # 软件成本
    license_cost_monthly: float = 0.0
    
    # 运维成本
    operation_cost_monthly: float = 0.0
    
    # 总成本
    total_cost_monthly: float = 0.0
    total_cost_yearly: float = 0.0
    
    # 成本明细
    cost_breakdown: Dict[str, float] = field(default_factory=dict)


@dataclass
class EnhancedOutputParameters:
    """增强的输出参数"""
    
    # ========== 基础信息 ==========
    recommendation_id: str = ""
    generated_at: str = ""
    version: str = "2.0"
    
    # ========== 架构方案 ==========
    architecture_name: str = ""
    architecture_type: str = ""  # 单机、主从、分布式
    deployment_mode: str = ""
    
    # ========== 数据库实例 ==========
    total_instances: int = 0
    instances: List[DatabaseInstance] = field(default_factory=list)
    
    # 按类型分组
    master_instances: List[DatabaseInstance] = field(default_factory=list)
    slave_instances: List[DatabaseInstance] = field(default_factory=list)
    readonly_instances: List[DatabaseInstance] = field(default_factory=list)
    
    # ========== 分片配置 ==========
    sharding_config: Optional[ShardingConfig] = None
    
    # ========== 读写分离 ==========
    read_write_split_config: Optional[ReadWriteSplitConfig] = None
    
    # ========== 高可用配置 ==========
    ha_config: Optional[HighAvailabilityConfig] = None
    
    # ========== 性能优化 ==========
    performance_config: Optional[PerformanceOptimization] = None
    
    # ========== 监控配置 ==========
    monitoring_config: Optional[MonitoringConfig] = None
    
    # ========== 容量规划 ==========
    capacity_planning: Dict[str, Any] = field(default_factory=dict)
    # - current_capacity: 当前容量
    # - peak_capacity: 峰值容量
    # - reserved_capacity: 预留容量
    # - growth_projection: 增长预测
    
    # ========== 性能预估 ==========
    performance_estimation: Dict[str, Any] = field(default_factory=dict)
    # - estimated_qps: 预估QPS
    # - estimated_tps: 预估TPS
    # - estimated_response_time_ms: 预估响应时间
    # - estimated_throughput_mbps: 预估吞吐量
    
    # ========== 成本估算 ==========
    cost_estimation: Optional[CostEstimation] = None
    
    # ========== 部署拓扑 ==========
    deployment_topology: Dict[str, Any] = field(default_factory=dict)
    # - data_centers: 数据中心列表
    # - network_links: 网络链路
    # - replication_topology: 复制拓扑
    
    # ========== 实施建议 ==========
    implementation_suggestions: List[str] = field(default_factory=list)
    
    # ========== 风险评估 ==========
    risk_assessment: List[Dict[str, str]] = field(default_factory=list)
    # - risk_type: 风险类型
    # - risk_level: 风险等级（低、中、高）
    # - description: 描述
    # - mitigation: 缓解措施
    
    # ========== 优化建议 ==========
    optimization_recommendations: List[Dict[str, str]] = field(default_factory=list)
    # - category: 类别
    # - recommendation: 建议
    # - priority: 优先级
    # - expected_benefit: 预期收益
    
    # ========== 对比方案 ==========
    alternative_solutions: List[Dict[str, Any]] = field(default_factory=list)
    
    # ========== 详细说明 ==========
    detailed_description: str = ""
    architecture_diagram_url: str = ""  # 架构图URL
    
    # ========== 置信度 ==========
    confidence_score: float = 0.0  # 0-100
    prediction_accuracy: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)
    
    def to_json(self, indent: int = 2) -> str:
        """转换为JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


class ParameterValidator:
    """参数验证器"""
    
    @staticmethod
    def validate_input(params: EnhancedInputParameters) -> tuple[bool, List[str]]:
        """
        验证输入参数
        
        Returns:
            (是否有效, 错误列表)
        """
        errors = []
        
        # 必填字段检查
        if not params.project_name:
            errors.append("项目名称不能为空")
        
        if params.total_systems <= 0:
            errors.append("系统总数必须大于0")
        
        if not params.systems:
            errors.append("系统列表不能为空")
        
        # 数值范围检查
        if params.total_data_size_tb < 0:
            errors.append("数据量不能为负数")
        
        if params.total_qps < 0:
            errors.append("QPS不能为负数")
        
        # 部署模式检查
        valid_deployment_modes = [
            "单中心", "同城双中心", "同城多中心", 
            "两地三中心", "三地五中心", "多地多中心"
        ]
        if params.deployment_mode not in valid_deployment_modes:
            errors.append(f"部署模式必须是: {', '.join(valid_deployment_modes)}")
        
        # RPO/RTO检查
        if params.rpo_seconds < 0:
            errors.append("RPO不能为负数")
        
        if params.rto_seconds < 0:
            errors.append("RTO不能为负数")
        
        # 系统列表检查
        for idx, system in enumerate(params.systems):
            if not system.get('system_name'):
                errors.append(f"第{idx+1}个系统名称不能为空")
        
        return len(errors) == 0, errors


# 测试代码
if __name__ == '__main__':
    print("=" * 60)
    print("📋 增强输入输出参数测试")
    print("=" * 60)
    
    # 创建输入参数
    input_params = EnhancedInputParameters(
        project_name="电商平台数据库架构",
        total_systems=3,
        systems=[
            {
                'system_name': '订单系统',
                'system_type': '核心',
                'data_size_gb': 5000,
                'qps': 50000,
                'tps': 10000
            },
            {
                'system_name': '用户系统',
                'system_type': '核心',
                'data_size_gb': 2000,
                'qps': 30000,
                'tps': 5000
            },
            {
                'system_name': '商品系统',
                'system_type': '核心',
                'data_size_gb': 3000,
                'qps': 40000,
                'tps': 8000
            }
        ],
        deployment_mode="两地三中心",
        disaster_recovery_type="双活",
        industry="电商平台"
    )
    
    # 验证参数
    validator = ParameterValidator()
    is_valid, errors = validator.validate_input(input_params)
    
    print(f"\n✅ 参数验证: {'通过' if is_valid else '失败'}")
    if errors:
        print("❌ 错误列表:")
        for error in errors:
            print(f"   - {error}")
    
    # 创建输出参数
    output_params = EnhancedOutputParameters(
        recommendation_id="REC-20250125-001",
        generated_at=datetime.now().isoformat(),
        architecture_name="两地三中心双活架构",
        architecture_type="分布式",
        deployment_mode="两地三中心",
        total_instances=6
    )
    
    print(f"\n📤 输出参数:")
    print(f"   - 推荐ID: {output_params.recommendation_id}")
    print(f"   - 架构名称: {output_params.architecture_name}")
    print(f"   - 实例总数: {output_params.total_instances}")
    
    print("\n" + "=" * 60)
    print("✅ 测试完成")
    print("=" * 60)
