#!/usr/bin/env python3
"""
部署拓扑参数定义
支持各种复杂的部署架构：单中心、同城多中心、两地三中心、三地五中心、多地多中心等
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class DeploymentMode(Enum):
    """部署模式"""
    SINGLE_CENTER = "单中心"
    SAME_CITY_DUAL = "同城双中心"
    SAME_CITY_MULTI = "同城多中心"
    TWO_SITE_THREE_CENTER = "两地三中心"
    THREE_SITE_FIVE_CENTER = "三地五中心"
    MULTI_SITE_MULTI_CENTER = "多地多中心"
    GLOBAL_DISTRIBUTED = "全球分布式"


class DisasterRecoveryType(Enum):
    """容灾类型"""
    COLD_STANDBY = "冷备"  # 数据备份，需要手动恢复
    WARM_STANDBY = "温备"  # 数据同步，需要手动切换
    HOT_STANDBY = "热备"   # 数据实时同步，可快速切换
    ACTIVE_STANDBY = "主备"  # 主节点工作，备节点待命
    ACTIVE_ACTIVE = "双活"  # 两个中心同时工作
    MULTI_ACTIVE = "多活"   # 多个中心同时工作


class SyncMode(Enum):
    """数据同步模式"""
    ASYNC = "异步复制"  # 主库不等待从库确认
    SEMI_SYNC = "半同步复制"  # 主库等待至少一个从库确认
    SYNC = "同步复制"  # 主库等待所有从库确认
    GROUP_REPLICATION = "组复制"  # MySQL Group Replication
    STRONG_SYNC = "强同步"  # 金融级强同步


class NetworkType(Enum):
    """网络类型"""
    DEDICATED_LINE = "专线"  # 企业专线
    VPN = "VPN"  # 虚拟专用网络
    PUBLIC_INTERNET = "公网"  # 公共互联网
    CLOUD_CONNECT = "云专线"  # 云服务商专线
    SD_WAN = "SD-WAN"  # 软件定义广域网


class FailoverMode(Enum):
    """故障切换模式"""
    MANUAL = "手动切换"
    SEMI_AUTO = "半自动切换"  # 需要人工确认
    AUTO = "自动切换"  # 完全自动
    INTELLIGENT = "智能切换"  # AI辅助决策


@dataclass
class DataCenter:
    """数据中心定义"""
    center_id: str = ""
    center_name: str = ""
    center_type: str = "生产中心"  # 生产中心、灾备中心、开发中心、测试中心
    
    # 地理位置
    region: str = ""  # 区域：华北、华东、华南等
    city: str = ""  # 城市
    availability_zone: str = ""  # 可用区
    
    # 角色
    role: str = "主中心"  # 主中心、备中心、只读中心
    is_active: bool = True  # 是否激活
    priority: int = 1  # 优先级（1最高）
    
    # 容量
    max_qps: int = 0
    max_connections: int = 0
    storage_capacity_tb: float = 0.0
    
    # 网络
    public_ip: str = ""
    private_ip: str = ""
    bandwidth_mbps: int = 0


@dataclass
class NetworkLink:
    """网络链路"""
    link_id: str = ""
    source_center: str = ""
    target_center: str = ""
    
    # 网络特性
    network_type: str = "专线"
    bandwidth_mbps: int = 0
    latency_ms: float = 0.0
    packet_loss_rate: float = 0.0  # 丢包率
    
    # 距离
    distance_km: float = 0.0
    
    # 成本
    monthly_cost: float = 0.0


@dataclass
class ReplicationConfig:
    """复制配置"""
    replication_id: str = ""
    source_center: str = ""
    target_centers: List[str] = field(default_factory=list)
    
    # 复制模式
    sync_mode: str = "异步复制"
    replication_delay_ms: int = 0  # 复制延迟
    
    # 数据一致性
    consistency_level: str = "最终一致性"  # 强一致性、最终一致性、因果一致性
    
    # 过滤规则
    replicate_databases: List[str] = field(default_factory=list)
    replicate_tables: List[str] = field(default_factory=list)
    ignore_databases: List[str] = field(default_factory=list)
    ignore_tables: List[str] = field(default_factory=list)


@dataclass
class FailoverConfig:
    """故障切换配置"""
    failover_mode: str = "自动切换"
    
    # 检测配置
    health_check_interval_seconds: int = 5
    failure_threshold: int = 3  # 连续失败次数
    
    # 切换配置
    auto_failover: bool = True
    failover_timeout_seconds: int = 60
    require_manual_approval: bool = False
    
    # 回切配置
    auto_failback: bool = False
    failback_delay_seconds: int = 300
    
    # 通知
    alert_contacts: List[str] = field(default_factory=list)
    alert_methods: List[str] = field(default_factory=list)  # 短信、邮件、电话


@dataclass
class DeploymentTopology:
    """完整的部署拓扑"""
    topology_id: str = ""
    topology_name: str = ""
    deployment_mode: str = "单中心"
    
    # 数据中心
    data_centers: List[DataCenter] = field(default_factory=list)
    
    # 网络链路
    network_links: List[NetworkLink] = field(default_factory=list)
    
    # 复制配置
    replication_configs: List[ReplicationConfig] = field(default_factory=list)
    
    # 故障切换
    failover_config: FailoverConfig = field(default_factory=FailoverConfig)
    
    # 容灾指标
    disaster_recovery_type: str = "热备"
    rpo_seconds: int = 0  # 恢复点目标
    rto_seconds: int = 0  # 恢复时间目标
    
    # 可用性目标
    availability_target: str = "99.99%"
    max_downtime_minutes_per_year: float = 0.0
    
    # 成本
    total_monthly_cost: float = 0.0
    
    # 备注
    description: str = ""
    created_at: str = ""
    updated_at: str = ""


class DeploymentTopologyBuilder:
    """部署拓扑构建器"""
    
    @staticmethod
    def build_single_center() -> DeploymentTopology:
        """构建单中心部署"""
        topology = DeploymentTopology(
            topology_name="单中心部署",
            deployment_mode="单中心",
            disaster_recovery_type="本地备份",
            rpo_seconds=3600,  # 1小时
            rto_seconds=7200,  # 2小时
            availability_target="99.9%"
        )
        
        # 主中心
        main_center = DataCenter(
            center_id="dc-main-001",
            center_name="主数据中心",
            center_type="生产中心",
            role="主中心",
            is_active=True,
            priority=1
        )
        topology.data_centers.append(main_center)
        
        return topology
    
    @staticmethod
    def build_same_city_dual() -> DeploymentTopology:
        """构建同城双中心部署"""
        topology = DeploymentTopology(
            topology_name="同城双中心部署",
            deployment_mode="同城双中心",
            disaster_recovery_type="热备",
            rpo_seconds=0,  # 实时同步
            rto_seconds=300,  # 5分钟
            availability_target="99.95%"
        )
        
        # 主中心
        main_center = DataCenter(
            center_id="dc-main-001",
            center_name="主数据中心",
            center_type="生产中心",
            region="华东",
            city="上海",
            availability_zone="上海一区",
            role="主中心",
            is_active=True,
            priority=1
        )
        
        # 备中心（同城）
        standby_center = DataCenter(
            center_id="dc-standby-001",
            center_name="同城备份中心",
            center_type="灾备中心",
            region="华东",
            city="上海",
            availability_zone="上海二区",
            role="备中心",
            is_active=True,
            priority=2
        )
        
        topology.data_centers.extend([main_center, standby_center])
        
        # 网络链路
        link = NetworkLink(
            link_id="link-001",
            source_center="dc-main-001",
            target_center="dc-standby-001",
            network_type="专线",
            bandwidth_mbps=10000,  # 10Gbps
            latency_ms=2.0,  # 同城延迟很低
            distance_km=30
        )
        topology.network_links.append(link)
        
        # 复制配置
        replication = ReplicationConfig(
            replication_id="repl-001",
            source_center="dc-main-001",
            target_centers=["dc-standby-001"],
            sync_mode="半同步复制",
            replication_delay_ms=10,
            consistency_level="强一致性"
        )
        topology.replication_configs.append(replication)
        
        # 故障切换
        topology.failover_config = FailoverConfig(
            failover_mode="自动切换",
            auto_failover=True,
            failover_timeout_seconds=60,
            auto_failback=True
        )
        
        return topology
    
    @staticmethod
    def build_two_site_three_center() -> DeploymentTopology:
        """构建两地三中心部署"""
        topology = DeploymentTopology(
            topology_name="两地三中心部署",
            deployment_mode="两地三中心",
            disaster_recovery_type="双活",
            rpo_seconds=0,
            rto_seconds=60,  # 1分钟
            availability_target="99.99%"
        )
        
        # 主中心（上海）
        main_center = DataCenter(
            center_id="dc-main-001",
            center_name="上海主中心",
            center_type="生产中心",
            region="华东",
            city="上海",
            availability_zone="上海一区",
            role="主中心",
            is_active=True,
            priority=1
        )
        
        # 同城备中心（上海）
        same_city_standby = DataCenter(
            center_id="dc-standby-001",
            center_name="上海备中心",
            center_type="灾备中心",
            region="华东",
            city="上海",
            availability_zone="上海二区",
            role="备中心",
            is_active=True,
            priority=2
        )
        
        # 异地备中心（北京）
        remote_standby = DataCenter(
            center_id="dc-remote-001",
            center_name="北京备中心",
            center_type="灾备中心",
            region="华北",
            city="北京",
            availability_zone="北京一区",
            role="备中心",
            is_active=True,
            priority=3
        )
        
        topology.data_centers.extend([main_center, same_city_standby, remote_standby])
        
        # 网络链路 - 同城
        same_city_link = NetworkLink(
            link_id="link-001",
            source_center="dc-main-001",
            target_center="dc-standby-001",
            network_type="专线",
            bandwidth_mbps=10000,
            latency_ms=2.0,
            distance_km=30
        )
        
        # 网络链路 - 异地
        remote_link = NetworkLink(
            link_id="link-002",
            source_center="dc-main-001",
            target_center="dc-remote-001",
            network_type="专线",
            bandwidth_mbps=1000,
            latency_ms=30.0,  # 上海到北京约30ms
            distance_km=1200
        )
        
        topology.network_links.extend([same_city_link, remote_link])
        
        # 复制配置 - 同城半同步
        same_city_repl = ReplicationConfig(
            replication_id="repl-001",
            source_center="dc-main-001",
            target_centers=["dc-standby-001"],
            sync_mode="半同步复制",
            replication_delay_ms=10,
            consistency_level="强一致性"
        )
        
        # 复制配置 - 异地异步
        remote_repl = ReplicationConfig(
            replication_id="repl-002",
            source_center="dc-main-001",
            target_centers=["dc-remote-001"],
            sync_mode="异步复制",
            replication_delay_ms=100,
            consistency_level="最终一致性"
        )
        
        topology.replication_configs.extend([same_city_repl, remote_repl])
        
        # 故障切换
        topology.failover_config = FailoverConfig(
            failover_mode="自动切换",
            auto_failover=True,
            failover_timeout_seconds=60,
            auto_failback=False,  # 两地三中心通常不自动回切
            require_manual_approval=True
        )
        
        return topology
    
    @staticmethod
    def build_three_site_five_center() -> DeploymentTopology:
        """构建三地五中心部署"""
        topology = DeploymentTopology(
            topology_name="三地五中心部署",
            deployment_mode="三地五中心",
            disaster_recovery_type="多活",
            rpo_seconds=0,
            rto_seconds=30,
            availability_target="99.995%"
        )
        
        # 上海主中心
        sh_main = DataCenter(
            center_id="dc-sh-main",
            center_name="上海主中心",
            region="华东",
            city="上海",
            role="主中心",
            priority=1
        )
        
        # 上海备中心
        sh_standby = DataCenter(
            center_id="dc-sh-standby",
            center_name="上海备中心",
            region="华东",
            city="上海",
            role="备中心",
            priority=2
        )
        
        # 北京主中心
        bj_main = DataCenter(
            center_id="dc-bj-main",
            center_name="北京主中心",
            region="华北",
            city="北京",
            role="主中心",
            priority=1
        )
        
        # 北京备中心
        bj_standby = DataCenter(
            center_id="dc-bj-standby",
            center_name="北京备中心",
            region="华北",
            city="北京",
            role="备中心",
            priority=2
        )
        
        # 深圳备中心
        sz_standby = DataCenter(
            center_id="dc-sz-standby",
            center_name="深圳备中心",
            region="华南",
            city="深圳",
            role="备中心",
            priority=3
        )
        
        topology.data_centers.extend([sh_main, sh_standby, bj_main, bj_standby, sz_standby])
        
        return topology
    
    @staticmethod
    def build_active_active() -> DeploymentTopology:
        """构建双活部署"""
        topology = DeploymentTopology(
            topology_name="双活部署",
            deployment_mode="同城双中心",
            disaster_recovery_type="双活",
            rpo_seconds=0,
            rto_seconds=0,  # 双活无需切换
            availability_target="99.99%"
        )
        
        # 两个中心都是主中心
        center1 = DataCenter(
            center_id="dc-active-001",
            center_name="活动中心1",
            role="主中心",
            is_active=True,
            priority=1
        )
        
        center2 = DataCenter(
            center_id="dc-active-002",
            center_name="活动中心2",
            role="主中心",
            is_active=True,
            priority=1
        )
        
        topology.data_centers.extend([center1, center2])
        
        # 双向复制
        repl1 = ReplicationConfig(
            replication_id="repl-001",
            source_center="dc-active-001",
            target_centers=["dc-active-002"],
            sync_mode="强同步",
            consistency_level="强一致性"
        )
        
        repl2 = ReplicationConfig(
            replication_id="repl-002",
            source_center="dc-active-002",
            target_centers=["dc-active-001"],
            sync_mode="强同步",
            consistency_level="强一致性"
        )
        
        topology.replication_configs.extend([repl1, repl2])
        
        return topology


class DeploymentRecommender:
    """部署方式推荐器"""
    
    @staticmethod
    def recommend(
        total_data_tb: float,
        total_qps: int,
        availability_requirement: str,
        budget_level: str,
        industry: str
    ) -> Dict[str, Any]:
        """
        根据需求推荐部署方式
        
        Args:
            total_data_tb: 总数据量(TB)
            total_qps: 总QPS
            availability_requirement: 可用性要求
            budget_level: 预算水平（低、中、高）
            industry: 行业
            
        Returns:
            推荐结果
        """
        recommendations = []
        
        # 解析可用性要求
        availability_num = float(availability_requirement.replace('%', ''))
        
        # 金融行业特殊处理
        if industry in ['银行', '证券', '保险', '支付']:
            if availability_num >= 99.99:
                recommendations.append({
                    'mode': '两地三中心',
                    'disaster_type': '双活',
                    'reason': '金融行业高可用性要求，建议两地三中心双活部署',
                    'priority': 1
                })
            else:
                recommendations.append({
                    'mode': '同城双中心',
                    'disaster_type': '热备',
                    'reason': '金融行业需要同城容灾',
                    'priority': 2
                })
        
        # 根据数据量和QPS
        if total_data_tb > 100 or total_qps > 100000:
            recommendations.append({
                'mode': '两地三中心',
                'disaster_type': '双活',
                'reason': '大规模数据和高并发，建议两地三中心',
                'priority': 1
            })
        elif total_data_tb > 50 or total_qps > 50000:
            recommendations.append({
                'mode': '同城双中心',
                'disaster_type': '热备',
                'reason': '中等规模，建议同城双中心',
                'priority': 2
            })
        
        # 根据可用性要求
        if availability_num >= 99.99:
            recommendations.append({
                'mode': '两地三中心',
                'disaster_type': '双活',
                'reason': '99.99%可用性要求，建议两地三中心',
                'priority': 1
            })
        elif availability_num >= 99.95:
            recommendations.append({
                'mode': '同城双中心',
                'disaster_type': '热备',
                'reason': '99.95%可用性要求，建议同城双中心',
                'priority': 2
            })
        elif availability_num >= 99.9:
            recommendations.append({
                'mode': '同城双中心',
                'disaster_type': '温备',
                'reason': '99.9%可用性要求，同城双中心温备即可',
                'priority': 3
            })
        else:
            recommendations.append({
                'mode': '单中心',
                'disaster_type': '本地备份',
                'reason': '可用性要求不高，单中心即可',
                'priority': 4
            })
        
        # 根据预算
        if budget_level == '低':
            recommendations.append({
                'mode': '单中心',
                'disaster_type': '本地备份',
                'reason': '预算有限，建议单中心',
                'priority': 5
            })
        elif budget_level == '中':
            recommendations.append({
                'mode': '同城双中心',
                'disaster_type': '热备',
                'reason': '预算适中，建议同城双中心',
                'priority': 3
            })
        
        # 去重并排序
        unique_recommendations = {}
        for rec in recommendations:
            key = f"{rec['mode']}-{rec['disaster_type']}"
            if key not in unique_recommendations or rec['priority'] < unique_recommendations[key]['priority']:
                unique_recommendations[key] = rec
        
        sorted_recommendations = sorted(unique_recommendations.values(), key=lambda x: x['priority'])
        
        return {
            'recommended': sorted_recommendations[0] if sorted_recommendations else None,
            'alternatives': sorted_recommendations[1:3] if len(sorted_recommendations) > 1 else [],
            'all_options': sorted_recommendations
        }


# 测试代码
if __name__ == '__main__':
    print("=" * 60)
    print("🏗️  部署拓扑参数测试")
    print("=" * 60)
    
    # 测试构建器
    builder = DeploymentTopologyBuilder()
    
    print("\n1️⃣  单中心部署:")
    single = builder.build_single_center()
    print(f"   - 模式: {single.deployment_mode}")
    print(f"   - 容灾: {single.disaster_recovery_type}")
    print(f"   - RPO: {single.rpo_seconds}秒")
    print(f"   - RTO: {single.rto_seconds}秒")
    
    print("\n2️⃣  同城双中心部署:")
    dual = builder.build_same_city_dual()
    print(f"   - 模式: {dual.deployment_mode}")
    print(f"   - 容灾: {dual.disaster_recovery_type}")
    print(f"   - 数据中心数: {len(dual.data_centers)}")
    print(f"   - 网络链路数: {len(dual.network_links)}")
    
    print("\n3️⃣  两地三中心部署:")
    two_three = builder.build_two_site_three_center()
    print(f"   - 模式: {two_three.deployment_mode}")
    print(f"   - 容灾: {two_three.disaster_recovery_type}")
    print(f"   - 数据中心数: {len(two_three.data_centers)}")
    print(f"   - 复制配置数: {len(two_three.replication_configs)}")
    
    print("\n4️⃣  部署推荐:")
    recommender = DeploymentRecommender()
    result = recommender.recommend(
        total_data_tb=100,
        total_qps=50000,
        availability_requirement="99.99%",
        budget_level="高",
        industry="银行"
    )
    print(f"   - 推荐方案: {result['recommended']['mode']}")
    print(f"   - 容灾类型: {result['recommended']['disaster_type']}")
    print(f"   - 推荐理由: {result['recommended']['reason']}")
    
    print("\n" + "=" * 60)
    print("✅ 测试完成")
    print("=" * 60)
