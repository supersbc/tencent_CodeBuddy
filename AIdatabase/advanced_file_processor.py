#!/usr/bin/env python3
"""
高级文件处理器 - 支持Excel、PDF、图片等多种格式
智能识别大环境内的多个系统和复杂部署架构
"""

import os
import re
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

# Excel处理
try:
    import pandas as pd
    import openpyxl
    from openpyxl import load_workbook
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False
    print("⚠️  Excel处理库未安装")

# PDF处理
try:
    import PyPDF2
    import pdfplumber
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("⚠️  PDF处理库未安装")

# 图像处理
try:
    from PIL import Image
    import pytesseract
    import cv2
    import numpy as np
    IMAGE_AVAILABLE = True
except ImportError:
    IMAGE_AVAILABLE = False
    print("⚠️  图像处理库未安装")

# OCR增强
try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False


@dataclass
class SystemInfo:
    """单个系统信息"""
    system_name: str = ""
    system_type: str = ""  # 核心系统、辅助系统、外围系统
    business_module: str = ""  # 业务模块
    data_size_gb: float = 0.0
    table_count: int = 0
    qps: int = 0
    tps: int = 0
    peak_qps: int = 0
    connections: int = 0
    availability_requirement: str = "99.9%"
    data_sensitivity: str = "中"
    backup_requirement: str = "每日"
    notes: str = ""


@dataclass
class DeploymentTopology:
    """部署拓扑信息"""
    deployment_mode: str = "单中心"  # 单中心、同城双中心、同城多中心、两地三中心、三地五中心、多地多中心
    primary_region: str = ""  # 主中心区域
    disaster_regions: List[str] = field(default_factory=list)  # 灾备中心区域
    
    # 同城部署
    same_city_centers: int = 1  # 同城中心数量
    same_city_distance_km: float = 0.0  # 同城中心间距离
    same_city_network_latency_ms: float = 0.0  # 同城网络延迟
    
    # 异地部署
    remote_centers: int = 0  # 异地中心数量
    remote_distance_km: float = 0.0  # 异地距离
    remote_network_latency_ms: float = 0.0  # 异地网络延迟
    
    # 数据同步
    sync_mode: str = "异步"  # 同步、异步、半同步
    rpo_seconds: int = 0  # 恢复点目标（秒）
    rto_seconds: int = 0  # 恢复时间目标（秒）
    
    # 容灾策略
    disaster_recovery_type: str = "冷备"  # 冷备、温备、热备、双活、多活
    auto_failover: bool = False  # 自动故障切换
    failover_time_seconds: int = 0  # 故障切换时间
    
    # 网络架构
    network_architecture: str = "专线"  # 专线、VPN、公网
    bandwidth_mbps: int = 0  # 带宽


@dataclass
class MultiSystemEnvironment:
    """多系统大环境"""
    environment_name: str = ""
    total_systems: int = 0
    systems: List[SystemInfo] = field(default_factory=list)
    deployment: DeploymentTopology = field(default_factory=DeploymentTopology)
    
    # 整体统计
    total_data_size_tb: float = 0.0
    total_qps: int = 0
    total_tps: int = 0
    total_connections: int = 0
    
    # 业务特征
    business_peak_hours: str = ""  # 业务高峰时段
    seasonal_peak: str = ""  # 季节性高峰
    growth_rate_yearly: float = 0.0  # 年增长率
    
    # 合规要求
    compliance_requirements: List[str] = field(default_factory=list)
    data_residency: str = ""  # 数据驻留要求


class AdvancedFileProcessor:
    """高级文件处理器"""
    
    def __init__(self):
        self.supported_formats = {
            'excel': ['.xlsx', '.xls', '.xlsm', '.xlsb'],
            'pdf': ['.pdf'],
            'image': ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif'],
            'text': ['.txt', '.csv', '.json']
        }
        
        # 初始化OCR引擎
        self.easyocr_reader = None
        if EASYOCR_AVAILABLE:
            try:
                self.easyocr_reader = easyocr.Reader(['ch_sim', 'en'])
            except:
                pass
        
        # 关键词映射
        self.keywords = self._init_keywords()
    
    def _init_keywords(self) -> Dict[str, List[str]]:
        """初始化关键词映射"""
        return {
            # 系统识别
            'system_name': ['系统名称', '系统', 'system', '模块', 'module', '应用', 'application'],
            'system_type': ['系统类型', '类型', 'type', '核心', '辅助', '外围'],
            
            # 数据量
            'data_size': ['数据量', '数据大小', '容量', 'data size', 'capacity', 'storage', 'GB', 'TB', 'PB'],
            'table_count': ['表数量', '表数', '表个数', 'table count', 'tables'],
            'database_count': ['库数量', '数据库数', 'database count', 'databases'],
            
            # 性能指标
            'qps': ['QPS', 'qps', '每秒查询', 'queries per second', '查询数'],
            'tps': ['TPS', 'tps', '每秒事务', 'transactions per second', '事务数'],
            'peak_qps': ['峰值QPS', '高峰QPS', 'peak qps', '最大QPS'],
            'connections': ['连接数', '并发连接', 'connections', 'concurrent'],
            'response_time': ['响应时间', '延迟', 'response time', 'latency', 'RT'],
            
            # 可用性
            'availability': ['可用性', '高可用', 'availability', 'HA', 'SLA'],
            'rpo': ['RPO', 'rpo', '恢复点', 'recovery point'],
            'rto': ['RTO', 'rto', '恢复时间', 'recovery time'],
            
            # 部署方式
            'deployment_mode': ['部署方式', '部署模式', 'deployment', '架构模式'],
            'same_city': ['同城', '本地', 'same city', 'local'],
            'remote': ['异地', '远程', 'remote', 'disaster'],
            'multi_center': ['多中心', '双中心', '三中心', 'multi-center', 'dual-center'],
            'two_site_three_center': ['两地三中心', '2地3中心'],
            'active_active': ['双活', '多活', 'active-active', 'multi-active'],
            
            # 数据同步
            'sync_mode': ['同步方式', '同步模式', 'sync mode', '复制'],
            'async': ['异步', 'async', 'asynchronous'],
            'sync': ['同步', 'sync', 'synchronous'],
            'semi_sync': ['半同步', 'semi-sync', 'semi-synchronous'],
            
            # 备份
            'backup': ['备份', 'backup', '备份策略'],
            'backup_frequency': ['备份频率', 'backup frequency'],
            
            # 安全合规
            'security': ['安全', 'security', '加密', 'encryption'],
            'compliance': ['合规', 'compliance', '等保', '分保'],
            'data_sensitivity': ['敏感度', '数据敏感', 'sensitivity'],
        }
    
    def process_file(self, file_path: str) -> Dict[str, Any]:
        """
        处理文件并提取信息
        
        Args:
            file_path: 文件路径
            
        Returns:
            提取的信息字典
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        # 根据文件类型调用不同的处理方法
        if file_ext in self.supported_formats['excel']:
            return self.process_excel(file_path)
        elif file_ext in self.supported_formats['pdf']:
            return self.process_pdf(file_path)
        elif file_ext in self.supported_formats['image']:
            return self.process_image(file_path)
        elif file_ext in self.supported_formats['text']:
            return self.process_text(file_path)
        else:
            raise ValueError(f"不支持的文件格式: {file_ext}")
    
    def process_excel(self, file_path: str) -> Dict[str, Any]:
        """
        处理Excel文件
        支持多个工作表，智能识别系统信息和部署架构
        """
        if not EXCEL_AVAILABLE:
            raise ImportError("Excel处理库未安装，请安装: pip install pandas openpyxl")
        
        result = {
            'file_type': 'excel',
            'file_path': file_path,
            'systems': [],
            'deployment': {},
            'summary': {},
            'raw_data': {}
        }
        
        try:
            # 读取所有工作表
            excel_file = pd.ExcelFile(file_path)
            workbook = load_workbook(file_path)
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                result['raw_data'][sheet_name] = df.to_dict('records')
                
                # 智能识别工作表类型
                sheet_type = self._identify_sheet_type(sheet_name, df)
                
                if sheet_type == 'system_list':
                    # 系统清单表
                    systems = self._extract_systems_from_df(df)
                    result['systems'].extend(systems)
                
                elif sheet_type == 'deployment':
                    # 部署架构表
                    deployment = self._extract_deployment_from_df(df)
                    result['deployment'].update(deployment)
                
                elif sheet_type == 'summary':
                    # 汇总表
                    summary = self._extract_summary_from_df(df)
                    result['summary'].update(summary)
            
            # 计算整体统计
            result['statistics'] = self._calculate_statistics(result['systems'])
            
            # 智能推断部署方式
            if not result['deployment']:
                result['deployment'] = self._infer_deployment(result['systems'], result['summary'])
            
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
        else:
            result['success'] = True
        
        return result
    
    def process_pdf(self, file_path: str) -> Dict[str, Any]:
        """
        处理PDF文件
        提取文本和表格信息
        """
        if not PDF_AVAILABLE:
            raise ImportError("PDF处理库未安装，请安装: pip install PyPDF2 pdfplumber")
        
        result = {
            'file_type': 'pdf',
            'file_path': file_path,
            'systems': [],
            'deployment': {},
            'text_content': '',
            'tables': []
        }
        
        try:
            # 使用pdfplumber提取表格
            with pdfplumber.open(file_path) as pdf:
                all_text = []
                
                for page_num, page in enumerate(pdf.pages):
                    # 提取文本
                    text = page.extract_text()
                    if text:
                        all_text.append(text)
                    
                    # 提取表格
                    tables = page.extract_tables()
                    for table in tables:
                        if table:
                            # 转换为DataFrame
                            df = pd.DataFrame(table[1:], columns=table[0])
                            result['tables'].append({
                                'page': page_num + 1,
                                'data': df.to_dict('records')
                            })
                            
                            # 尝试从表格提取系统信息
                            systems = self._extract_systems_from_df(df)
                            result['systems'].extend(systems)
                
                result['text_content'] = '\n'.join(all_text)
            
            # 从文本中提取部署信息
            result['deployment'] = self._extract_deployment_from_text(result['text_content'])
            
            # 计算统计
            result['statistics'] = self._calculate_statistics(result['systems'])
            
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
        else:
            result['success'] = True
        
        return result
    
    def process_image(self, file_path: str) -> Dict[str, Any]:
        """
        处理图片文件
        使用OCR提取文本和表格
        """
        if not IMAGE_AVAILABLE:
            raise ImportError("图像处理库未安装")
        
        result = {
            'file_type': 'image',
            'file_path': file_path,
            'systems': [],
            'deployment': {},
            'ocr_text': ''
        }
        
        try:
            # 读取图像
            image = Image.open(file_path)
            
            # 图像预处理
            processed_image = self._preprocess_image(image)
            
            # OCR识别
            if self.easyocr_reader:
                # 使用EasyOCR（更准确）
                ocr_result = self.easyocr_reader.readtext(np.array(processed_image))
                result['ocr_text'] = '\n'.join([text[1] for text in ocr_result])
            else:
                # 使用Tesseract
                result['ocr_text'] = pytesseract.image_to_string(processed_image, lang='chi_sim+eng')
            
            # 尝试识别表格结构
            tables = self._extract_tables_from_image(processed_image)
            result['tables'] = tables
            
            # 从OCR文本提取信息
            result['systems'] = self._extract_systems_from_text(result['ocr_text'])
            result['deployment'] = self._extract_deployment_from_text(result['ocr_text'])
            
            # 计算统计
            result['statistics'] = self._calculate_statistics(result['systems'])
            
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
        else:
            result['success'] = True
        
        return result
    
    def process_text(self, file_path: str) -> Dict[str, Any]:
        """处理文本文件"""
        result = {
            'file_type': 'text',
            'file_path': file_path,
            'systems': [],
            'deployment': {}
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            result['text_content'] = content
            
            # 如果是JSON格式
            if file_path.endswith('.json'):
                try:
                    data = json.loads(content)
                    result['json_data'] = data
                    # 从JSON提取信息
                    if isinstance(data, dict):
                        if 'systems' in data:
                            result['systems'] = data['systems']
                        if 'deployment' in data:
                            result['deployment'] = data['deployment']
                except:
                    pass
            
            # 从文本提取信息
            if not result['systems']:
                result['systems'] = self._extract_systems_from_text(content)
            if not result['deployment']:
                result['deployment'] = self._extract_deployment_from_text(content)
            
            result['statistics'] = self._calculate_statistics(result['systems'])
            result['success'] = True
            
        except Exception as e:
            result['error'] = str(e)
            result['success'] = False
        
        return result
    
    def _identify_sheet_type(self, sheet_name: str, df: pd.DataFrame) -> str:
        """识别工作表类型"""
        sheet_name_lower = sheet_name.lower()
        
        # 检查工作表名称
        if any(keyword in sheet_name_lower for keyword in ['系统', 'system', '清单', 'list']):
            return 'system_list'
        elif any(keyword in sheet_name_lower for keyword in ['部署', 'deployment', '架构', 'architecture']):
            return 'deployment'
        elif any(keyword in sheet_name_lower for keyword in ['汇总', 'summary', '总计', 'total']):
            return 'summary'
        
        # 检查列名
        if not df.empty:
            columns_str = ' '.join(df.columns.astype(str)).lower()
            if any(keyword in columns_str for keyword in ['系统名称', 'system name', '模块']):
                return 'system_list'
            elif any(keyword in columns_str for keyword in ['部署', 'deployment', '中心', 'center']):
                return 'deployment'
        
        return 'unknown'
    
    def _extract_systems_from_df(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """从DataFrame提取系统信息"""
        systems = []
        
        if df.empty:
            return systems
        
        # 列名映射
        column_mapping = self._map_columns(df.columns)
        
        for idx, row in df.iterrows():
            system = {}
            
            for col_name, mapped_name in column_mapping.items():
                value = row.get(col_name)
                if pd.notna(value):
                    # 数据清洗和转换
                    system[mapped_name] = self._clean_value(value, mapped_name)
            
            if system:  # 只添加非空系统
                systems.append(system)
        
        return systems
    
    def _extract_deployment_from_df(self, df: pd.DataFrame) -> Dict[str, Any]:
        """从DataFrame提取部署信息"""
        deployment = {}
        
        # 查找部署相关的行
        for idx, row in df.iterrows():
            for col in df.columns:
                value = str(row[col]).lower()
                
                # 识别部署模式
                if '两地三中心' in value or '2地3中心' in value:
                    deployment['deployment_mode'] = '两地三中心'
                elif '同城双中心' in value or '同城2中心' in value:
                    deployment['deployment_mode'] = '同城双中心'
                elif '同城多中心' in value:
                    deployment['deployment_mode'] = '同城多中心'
                elif '三地五中心' in value or '3地5中心' in value:
                    deployment['deployment_mode'] = '三地五中心'
                elif '双活' in value or 'active-active' in value:
                    deployment['disaster_recovery_type'] = '双活'
                elif '多活' in value or 'multi-active' in value:
                    deployment['disaster_recovery_type'] = '多活'
                
                # 识别RPO/RTO
                rpo_match = re.search(r'RPO[：:=\s]*(\d+)\s*(秒|分|小时|s|m|h)', value, re.IGNORECASE)
                if rpo_match:
                    deployment['rpo'] = rpo_match.group(1) + rpo_match.group(2)
                
                rto_match = re.search(r'RTO[：:=\s]*(\d+)\s*(秒|分|小时|s|m|h)', value, re.IGNORECASE)
                if rto_match:
                    deployment['rto'] = rto_match.group(1) + rto_match.group(2)
        
        return deployment
    
    def _extract_summary_from_df(self, df: pd.DataFrame) -> Dict[str, Any]:
        """从DataFrame提取汇总信息"""
        summary = {}
        
        for idx, row in df.iterrows():
            for col in df.columns:
                col_lower = str(col).lower()
                value = row[col]
                
                if pd.notna(value):
                    if '总数据量' in col_lower or 'total data' in col_lower:
                        summary['total_data_size'] = self._parse_size(str(value))
                    elif '总qps' in col_lower or 'total qps' in col_lower:
                        summary['total_qps'] = self._parse_number(str(value))
                    elif '系统数' in col_lower or 'system count' in col_lower:
                        summary['total_systems'] = self._parse_number(str(value))
        
        return summary
    
    def _extract_systems_from_text(self, text: str) -> List[Dict[str, Any]]:
        """从文本提取系统信息"""
        systems = []
        
        # 使用正则表达式查找系统信息
        # 这里可以根据实际文本格式调整
        lines = text.split('\n')
        
        current_system = {}
        for line in lines:
            line = line.strip()
            if not line:
                if current_system:
                    systems.append(current_system)
                    current_system = {}
                continue
            
            # 尝试提取键值对
            if '：' in line or ':' in line:
                parts = re.split('[：:]', line, 1)
                if len(parts) == 2:
                    key, value = parts
                    key = key.strip()
                    value = value.strip()
                    
                    # 映射到标准字段
                    if '系统名称' in key or 'system name' in key.lower():
                        current_system['system_name'] = value
                    elif 'qps' in key.lower():
                        current_system['qps'] = self._parse_number(value)
                    elif '数据量' in key or 'data size' in key.lower():
                        current_system['data_size_gb'] = self._parse_size(value)
        
        if current_system:
            systems.append(current_system)
        
        return systems
    
    def _extract_deployment_from_text(self, text: str) -> Dict[str, Any]:
        """从文本提取部署信息"""
        deployment = {}
        
        text_lower = text.lower()
        
        # 识别部署模式
        if '两地三中心' in text or '2地3中心' in text:
            deployment['deployment_mode'] = '两地三中心'
            deployment['remote_centers'] = 2
            deployment['same_city_centers'] = 2
        elif '同城双中心' in text or '同城2中心' in text:
            deployment['deployment_mode'] = '同城双中心'
            deployment['same_city_centers'] = 2
        elif '同城多中心' in text:
            deployment['deployment_mode'] = '同城多中心'
        elif '三地五中心' in text or '3地5中心' in text:
            deployment['deployment_mode'] = '三地五中心'
        
        # 识别容灾类型
        if '双活' in text or 'active-active' in text_lower:
            deployment['disaster_recovery_type'] = '双活'
        elif '多活' in text or 'multi-active' in text_lower:
            deployment['disaster_recovery_type'] = '多活'
        
        # 提取RPO/RTO
        rpo_match = re.search(r'RPO[：:=\s]*(\d+)\s*(秒|分|小时|s|m|h)', text, re.IGNORECASE)
        if rpo_match:
            deployment['rpo'] = rpo_match.group(1) + rpo_match.group(2)
        
        rto_match = re.search(r'RTO[：:=\s]*(\d+)\s*(秒|分|小时|s|m|h)', text, re.IGNORECASE)
        if rto_match:
            deployment['rto'] = rto_match.group(1) + rto_match.group(2)
        
        return deployment
    
    def _calculate_statistics(self, systems: List[Dict[str, Any]]) -> Dict[str, Any]:
        """计算统计信息"""
        if not systems:
            return {}
        
        stats = {
            'total_systems': len(systems),
            'total_data_size_gb': 0,
            'total_qps': 0,
            'total_tps': 0,
            'total_connections': 0,
            'max_qps': 0,
            'avg_qps': 0
        }
        
        for system in systems:
            stats['total_data_size_gb'] += system.get('data_size_gb', 0)
            stats['total_qps'] += system.get('qps', 0)
            stats['total_tps'] += system.get('tps', 0)
            stats['total_connections'] += system.get('connections', 0)
            stats['max_qps'] = max(stats['max_qps'], system.get('qps', 0))
        
        if stats['total_systems'] > 0:
            stats['avg_qps'] = stats['total_qps'] / stats['total_systems']
        
        stats['total_data_size_tb'] = stats['total_data_size_gb'] / 1024
        
        return stats
    
    def _infer_deployment(self, systems: List[Dict[str, Any]], summary: Dict[str, Any]) -> Dict[str, Any]:
        """智能推断部署方式"""
        deployment = {
            'deployment_mode': '单中心',
            'disaster_recovery_type': '冷备'
        }
        
        # 根据系统数量和数据量推断
        total_systems = len(systems)
        total_data_gb = sum(s.get('data_size_gb', 0) for s in systems)
        max_qps = max((s.get('qps', 0) for s in systems), default=0)
        
        # 大规模系统建议多中心
        if total_systems > 10 or total_data_gb > 10000 or max_qps > 50000:
            deployment['deployment_mode'] = '两地三中心'
            deployment['disaster_recovery_type'] = '双活'
        elif total_systems > 5 or total_data_gb > 5000 or max_qps > 20000:
            deployment['deployment_mode'] = '同城双中心'
            deployment['disaster_recovery_type'] = '热备'
        
        return deployment
    
    def _map_columns(self, columns: List[str]) -> Dict[str, str]:
        """映射列名到标准字段"""
        mapping = {}
        
        for col in columns:
            col_lower = str(col).lower()
            
            if '系统名称' in col or 'system name' in col_lower or '系统' == col:
                mapping[col] = 'system_name'
            elif '系统类型' in col or 'system type' in col_lower:
                mapping[col] = 'system_type'
            elif '业务模块' in col or 'business' in col_lower or '模块' in col:
                mapping[col] = 'business_module'
            elif '数据量' in col or 'data size' in col_lower or '容量' in col:
                mapping[col] = 'data_size_gb'
            elif '表数' in col or 'table count' in col_lower:
                mapping[col] = 'table_count'
            elif 'qps' in col_lower:
                if '峰值' in col or 'peak' in col_lower:
                    mapping[col] = 'peak_qps'
                else:
                    mapping[col] = 'qps'
            elif 'tps' in col_lower:
                mapping[col] = 'tps'
            elif '连接' in col or 'connection' in col_lower:
                mapping[col] = 'connections'
            elif '可用性' in col or 'availability' in col_lower:
                mapping[col] = 'availability_requirement'
            elif '敏感' in col or 'sensitivity' in col_lower:
                mapping[col] = 'data_sensitivity'
            elif '备份' in col or 'backup' in col_lower:
                mapping[col] = 'backup_requirement'
            elif '备注' in col or 'note' in col_lower or '说明' in col:
                mapping[col] = 'notes'
        
        return mapping
    
    def _clean_value(self, value: Any, field_name: str) -> Any:
        """清洗和转换值"""
        if pd.isna(value):
            return None
        
        value_str = str(value).strip()
        
        # 数值类型字段
        if field_name in ['data_size_gb', 'qps', 'tps', 'peak_qps', 'connections', 'table_count']:
            return self._parse_number(value_str)
        
        # 大小字段
        if field_name == 'data_size_gb':
            return self._parse_size(value_str)
        
        return value_str
    
    def _parse_number(self, value: str) -> float:
        """解析数字"""
        # 移除逗号和空格
        value = re.sub(r'[,\s]', '', str(value))
        
        # 提取数字
        match = re.search(r'[\d.]+', value)
        if match:
            try:
                return float(match.group())
            except:
                return 0
        return 0
    
    def _parse_size(self, value: str) -> float:
        """解析大小（转换为GB）"""
        value = str(value).upper()
        
        # 提取数字
        match = re.search(r'([\d.]+)\s*([KMGTP]?B?)', value)
        if match:
            num = float(match.group(1))
            unit = match.group(2)
            
            # 转换为GB
            if 'TB' in unit or 'T' == unit:
                return num * 1024
            elif 'GB' in unit or 'G' == unit:
                return num
            elif 'MB' in unit or 'M' == unit:
                return num / 1024
            elif 'KB' in unit or 'K' == unit:
                return num / (1024 * 1024)
            elif 'PB' in unit or 'P' == unit:
                return num * 1024 * 1024
            else:
                return num
        
        return 0
    
    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """图像预处理"""
        # 转换为灰度图
        if image.mode != 'L':
            image = image.convert('L')
        
        # 转换为numpy数组
        img_array = np.array(image)
        
        # 二值化
        _, img_binary = cv2.threshold(img_array, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # 去噪
        img_denoised = cv2.fastNlMeansDenoising(img_binary)
        
        return Image.fromarray(img_denoised)
    
    def _extract_tables_from_image(self, image: Image.Image) -> List[Dict[str, Any]]:
        """从图像提取表格"""
        # 这里可以使用更高级的表格检测算法
        # 简化版本：返回空列表
        return []


# 测试代码
if __name__ == '__main__':
    processor = AdvancedFileProcessor()
    
    print("=" * 60)
    print("🚀 高级文件处理器测试")
    print("=" * 60)
    print(f"✅ 支持格式: {list(processor.supported_formats.keys())}")
    print(f"✅ Excel支持: {EXCEL_AVAILABLE}")
    print(f"✅ PDF支持: {PDF_AVAILABLE}")
    print(f"✅ 图像支持: {IMAGE_AVAILABLE}")
    print(f"✅ EasyOCR支持: {EASYOCR_AVAILABLE}")
    print("=" * 60)
