#!/usr/bin/env python3
"""
参数表单生成器 - 根据专业级参数定义生成Web表单
"""

from professional_parameters import (
    ProfessionalInputParameters,
    ParameterHelper,
    IndustryType,
    BusinessType,
    AvailabilityLevel,
    DisasterRecoveryType
)
from typing import Dict, List, Any


class ParameterFormGenerator:
    """参数表单生成器"""
    
    def __init__(self):
        self.helper = ParameterHelper()
        self.groups = self.helper.get_parameter_groups()
        self.descriptions = self.helper.get_parameter_descriptions()
        self.required = self.helper.get_required_parameters()
    
    def generate_form_config(self) -> Dict[str, Any]:
        """生成表单配置"""
        config = {
            'groups': [],
            'total_params': 0,
            'required_params': len(self.required)
        }
        
        # 为每个分组生成配置
        for group_name, param_names in self.groups.items():
            group_config = {
                'name': group_name,
                'fields': []
            }
            
            for param_name in param_names:
                field_config = self._generate_field_config(param_name)
                if field_config:
                    group_config['fields'].append(field_config)
                    config['total_params'] += 1
            
            config['groups'].append(group_config)
        
        return config
    
    def _generate_field_config(self, param_name: str) -> Dict[str, Any]:
        """生成单个字段配置"""
        # 获取参数类型和默认值
        params = ProfessionalInputParameters()
        if not hasattr(params, param_name):
            return None
        
        default_value = getattr(params, param_name)
        field_type = type(default_value).__name__
        
        config = {
            'name': param_name,
            'label': self._get_field_label(param_name),
            'type': self._map_field_type(field_type, param_name),
            'required': param_name in self.required,
            'description': self.descriptions.get(param_name, ''),
            'default': default_value
        }
        
        # 添加选项（如果是枚举类型）
        if 'industry' in param_name.lower():
            config['options'] = self._get_industry_options()
        elif 'business_type' in param_name.lower():
            config['options'] = self._get_business_type_options()
        elif 'availability_level' in param_name.lower():
            config['options'] = self._get_availability_options()
        elif 'dr_type' in param_name.lower():
            config['options'] = self._get_dr_type_options()
        
        # 添加验证规则
        config['validation'] = self._get_validation_rules(param_name, field_type)
        
        return config
    
    def _get_field_label(self, param_name: str) -> str:
        """获取字段标签"""
        # 将下划线转换为空格并首字母大写
        label_map = {
            'total_data_size_gb': '数据总量(GB)',
            'total_data_size_tb': '数据总量(TB)',
            'avg_qps': '平均QPS',
            'peak_qps': '峰值QPS',
            'avg_tps': '平均TPS',
            'peak_tps': '峰值TPS',
            'concurrent_connections': '并发连接数',
            'table_count': '表数量',
            'database_count': '数据库数量',
            'data_growth_rate_yearly': '年度数据增长率(%)',
            'data_growth_rate_monthly': '月度数据增长率(%)',
            'read_write_ratio': '读写比例',
            'need_high_availability': '需要高可用',
            'need_disaster_recovery': '需要灾备',
            'need_read_write_split': '需要读写分离',
            'need_sharding': '需要分库分表',
            'rto_minutes': 'RTO恢复时间(分钟)',
            'rpo_minutes': 'RPO恢复点(分钟)',
            'backup_frequency': '备份频率',
            'backup_retention_days': '备份保留天数',
            'need_encryption': '需要加密',
            'need_cache': '需要缓存',
            'cache_size_gb': '缓存大小(GB)',
            'monitoring_level': '监控级别',
            'team_expertise': '团队技术水平',
            'total_budget': '总预算',
            'cost_priority': '成本优先级',
            'industry': '行业类型',
            'business_type': '业务类型',
            'scenario_name': '场景名称',
            'availability_level': '可用性级别',
            'dr_type': '灾备类型',
        }
        
        return label_map.get(param_name, param_name.replace('_', ' ').title())
    
    def _map_field_type(self, python_type: str, param_name: str) -> str:
        """映射Python类型到HTML表单类型"""
        if python_type == 'bool':
            return 'checkbox'
        elif python_type in ['int', 'float']:
            return 'number'
        elif python_type == 'str':
            if 'email' in param_name:
                return 'email'
            elif 'phone' in param_name:
                return 'tel'
            elif 'date' in param_name or 'deadline' in param_name:
                return 'date'
            elif param_name in ['industry', 'business_type', 'availability_level', 'dr_type']:
                return 'select'
            elif 'description' in param_name or 'notes' in param_name:
                return 'textarea'
            else:
                return 'text'
        elif python_type == 'list':
            return 'multiselect'
        else:
            return 'text'
    
    def _get_industry_options(self) -> List[Dict[str, str]]:
        """获取行业选项"""
        return [
            {'value': item.value, 'label': item.value}
            for item in IndustryType
        ]
    
    def _get_business_type_options(self) -> List[Dict[str, str]]:
        """获取业务类型选项"""
        return [
            {'value': item.value, 'label': item.value}
            for item in BusinessType
        ]
    
    def _get_availability_options(self) -> List[Dict[str, str]]:
        """获取可用性级别选项"""
        return [
            {'value': item.value, 'label': item.value}
            for item in AvailabilityLevel
        ]
    
    def _get_dr_type_options(self) -> List[Dict[str, str]]:
        """获取灾备类型选项"""
        return [
            {'value': item.value, 'label': item.value}
            for item in DisasterRecoveryType
        ]
    
    def _get_validation_rules(self, param_name: str, field_type: str) -> Dict[str, Any]:
        """获取验证规则"""
        rules = {}
        
        if param_name in self.required:
            rules['required'] = True
        
        if field_type in ['int', 'float']:
            rules['min'] = 0
            
            # 特定字段的最大值
            if 'ratio' in param_name or 'percent' in param_name:
                rules['max'] = 100
            elif 'availability' in param_name:
                rules['max'] = 100
        
        return rules
    
    def generate_simplified_form(self) -> Dict[str, Any]:
        """生成简化表单（只包含核心参数）"""
        core_groups = {
            "业务基础信息": ["industry", "business_type", "scenario_name"],
            "数据规模": ["total_data_size_gb", "table_count", "data_growth_rate_yearly"],
            "性能指标": ["avg_qps", "avg_tps", "concurrent_connections", "avg_response_time_ms"],
            "可用性要求": ["availability_level", "need_high_availability", "need_disaster_recovery"],
            "读写特征": ["read_write_ratio", "need_read_write_split"],
            "安全合规": ["data_sensitivity", "need_encryption", "compliance_required"],
            "成本预算": ["total_budget", "cost_priority"]
        }
        
        config = {
            'groups': [],
            'total_params': 0,
            'mode': 'simplified'
        }
        
        for group_name, param_names in core_groups.items():
            group_config = {
                'name': group_name,
                'fields': []
            }
            
            for param_name in param_names:
                field_config = self._generate_field_config(param_name)
                if field_config:
                    group_config['fields'].append(field_config)
                    config['total_params'] += 1
            
            config['groups'].append(group_config)
        
        return config
    
    def generate_advanced_form(self) -> Dict[str, Any]:
        """生成高级表单（包含所有参数）"""
        return self.generate_form_config()


def main():
    """演示表单生成"""
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║              参数表单生成器                                        ║")
    print("╚══════════════════════════════════════════════════════════════════╝\n")
    
    generator = ParameterFormGenerator()
    
    # 生成简化表单
    print("📋 简化表单配置:\n")
    simplified = generator.generate_simplified_form()
    print(f"   参数分组: {len(simplified['groups'])}")
    print(f"   总参数数: {simplified['total_params']}\n")
    
    for group in simplified['groups']:
        print(f"   【{group['name']}】")
        for field in group['fields']:
            required = "* " if field['required'] else "  "
            print(f"      {required}{field['label']} ({field['type']})")
        print()
    
    # 生成完整表单
    print("\n" + "="*70 + "\n")
    print("📋 完整表单配置:\n")
    full = generator.generate_advanced_form()
    print(f"   参数分组: {len(full['groups'])}")
    print(f"   总参数数: {full['total_params']}")
    print(f"   必填参数: {full['required_params']}\n")
    
    # 显示每个分组的参数数量
    for group in full['groups']:
        print(f"   【{group['name']}】 - {len(group['fields'])} 个参数")
    
    print("\n" + "="*70)
    print("\n✅ 表单配置生成完成！")


if __name__ == '__main__':
    main()
