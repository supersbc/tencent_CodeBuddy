"""
图像表格智能识别模块
支持截图和Excel文件的智能识别和数据提取
"""

import re
from typing import Dict, Any, Optional
import json

try:
    from PIL import Image
    import pytesseract
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️  PIL/pytesseract 未安装，图像识别功能受限")

try:
    import pandas as pd
    import openpyxl
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False
    print("⚠️  pandas/openpyxl 未安装，Excel识别功能受限")

try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("⚠️  OpenCV 未安装，高级图像处理功能受限")


class ImageTableRecognizer:
    """图像表格识别器"""
    
    def __init__(self):
        self.keywords_mapping = {
            # 数据量相关
            'data_size': ['数据量', '数据总量', '总数据', 'data size', 'total data', '容量', 'capacity', 'GB', 'TB'],
            'table_count': ['表数量', '表个数', '表总数', 'table count', 'tables', '表'],
            'database_count': ['库数量', '数据库数', 'database count', 'databases', '库'],
            
            # 性能相关
            'qps': ['QPS', 'qps', '每秒查询', 'queries per second', '查询/秒'],
            'tps': ['TPS', 'tps', '每秒事务', 'transactions per second', '事务/秒'],
            'connections': ['连接数', '并发连接', 'connections', 'concurrent', '最大连接'],
            
            # 架构相关
            'architecture': ['架构', '架构类型', 'architecture', '部署方式'],
            'nodes': ['节点', '节点数', 'nodes', 'node count', '服务器数'],
            'replicas': ['副本', '副本数', 'replicas', 'replica count'],
            
            # 其他
            'growth_rate': ['增长率', '年增长', 'growth rate', '增长'],
            'ha': ['高可用', 'HA', 'high availability', '可用性'],
            'dr': ['容灾', 'DR', 'disaster recovery', '灾备'],
        }
    
    def recognize_image(self, image_path: str) -> Dict[str, Any]:
        """识别图像中的表格数据"""
        if not PIL_AVAILABLE:
            return self._mock_recognition()
        
        try:
            # 读取图像
            image = Image.open(image_path)
            
            # 预处理图像
            if CV2_AVAILABLE:
                image = self._preprocess_image(image)
            
            # OCR识别
            text = pytesseract.image_to_string(image, lang='chi_sim+eng')
            
            # 提取数据
            extracted_data = self._extract_data_from_text(text)
            
            return extracted_data
        
        except Exception as e:
            print(f"图像识别错误: {str(e)}")
            return self._mock_recognition()
    
    def recognize_excel(self, excel_path: str) -> Dict[str, Any]:
        """识别Excel文件中的数据"""
        if not EXCEL_AVAILABLE:
            return self._mock_recognition()
        
        try:
            # 读取Excel
            df = pd.read_excel(excel_path, sheet_name=0)
            
            # 提取数据
            extracted_data = self._extract_data_from_dataframe(df)
            
            return extracted_data
        
        except Exception as e:
            print(f"Excel识别错误: {str(e)}")
            return self._mock_recognition()
    
    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """预处理图像以提高OCR准确率"""
        # 转换为OpenCV格式
        img_array = np.array(image)
        
        # 转灰度
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        # 二值化
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # 去噪
        denoised = cv2.fastNlMeansDenoising(binary)
        
        # 转回PIL格式
        return Image.fromarray(denoised)
    
    def _extract_data_from_text(self, text: str) -> Dict[str, Any]:
        """从OCR文本中提取结构化数据"""
        data = {
            'total_data_size_gb': 0,
            'table_count': 0,
            'database_count': 0,
            'qps': 0,
            'tps': 0,
            'concurrent_connections': 0,
            'need_high_availability': False,
            'need_disaster_recovery': False,
            'need_read_write_split': False,
            'data_growth_rate': 30
        }
        
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 提取数据量
            if any(kw in line for kw in self.keywords_mapping['data_size']):
                data['total_data_size_gb'] = self._extract_number(line, ['GB', 'TB'])
                if 'TB' in line:
                    data['total_data_size_gb'] *= 1024
            
            # 提取表数量
            elif any(kw in line for kw in self.keywords_mapping['table_count']):
                data['table_count'] = int(self._extract_number(line))
            
            # 提取库数量
            elif any(kw in line for kw in self.keywords_mapping['database_count']):
                data['database_count'] = int(self._extract_number(line))
            
            # 提取QPS
            elif any(kw in line for kw in self.keywords_mapping['qps']):
                data['qps'] = int(self._extract_number(line))
            
            # 提取TPS
            elif any(kw in line for kw in self.keywords_mapping['tps']):
                data['tps'] = int(self._extract_number(line))
            
            # 提取连接数
            elif any(kw in line for kw in self.keywords_mapping['connections']):
                data['concurrent_connections'] = int(self._extract_number(line))
            
            # 提取增长率
            elif any(kw in line for kw in self.keywords_mapping['growth_rate']):
                data['data_growth_rate'] = self._extract_number(line, ['%'])
            
            # 检测高可用
            if any(kw in line for kw in self.keywords_mapping['ha']):
                data['need_high_availability'] = True
            
            # 检测容灾
            if any(kw in line for kw in self.keywords_mapping['dr']):
                data['need_disaster_recovery'] = True
        
        return data
    
    def _extract_data_from_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """从DataFrame中提取结构化数据"""
        data = {
            'total_data_size_gb': 0,
            'table_count': 0,
            'database_count': 0,
            'qps': 0,
            'tps': 0,
            'concurrent_connections': 0,
            'need_high_availability': False,
            'need_disaster_recovery': False,
            'need_read_write_split': False,
            'data_growth_rate': 30
        }
        
        # 遍历所有单元格
        for col in df.columns:
            for idx, value in df[col].items():
                if pd.isna(value):
                    continue
                
                cell_text = str(value).strip()
                
                # 检查列名和单元格内容
                combined_text = f"{col} {cell_text}"
                
                # 提取数据量
                if any(kw in combined_text for kw in self.keywords_mapping['data_size']):
                    num = self._extract_number(cell_text, ['GB', 'TB'])
                    if num > 0:
                        data['total_data_size_gb'] = num
                        if 'TB' in cell_text:
                            data['total_data_size_gb'] *= 1024
                
                # 提取表数量
                elif any(kw in combined_text for kw in self.keywords_mapping['table_count']):
                    num = self._extract_number(cell_text)
                    if num > 0:
                        data['table_count'] = int(num)
                
                # 提取QPS
                elif any(kw in combined_text for kw in self.keywords_mapping['qps']):
                    num = self._extract_number(cell_text)
                    if num > 0:
                        data['qps'] = int(num)
                
                # 提取TPS
                elif any(kw in combined_text for kw in self.keywords_mapping['tps']):
                    num = self._extract_number(cell_text)
                    if num > 0:
                        data['tps'] = int(num)
                
                # 提取连接数
                elif any(kw in combined_text for kw in self.keywords_mapping['connections']):
                    num = self._extract_number(cell_text)
                    if num > 0:
                        data['concurrent_connections'] = int(num)
                
                # 检测高可用
                if any(kw in combined_text for kw in self.keywords_mapping['ha']):
                    data['need_high_availability'] = True
                
                # 检测容灾
                if any(kw in combined_text for kw in self.keywords_mapping['dr']):
                    data['need_disaster_recovery'] = True
        
        return data
    
    def _extract_number(self, text: str, units: list = None) -> float:
        """从文本中提取数字"""
        # 移除单位
        if units:
            for unit in units:
                text = text.replace(unit, '')
        
        # 移除逗号和空格
        text = text.replace(',', '').replace(' ', '')
        
        # 提取数字（支持小数）
        numbers = re.findall(r'\d+\.?\d*', text)
        
        if numbers:
            return float(numbers[0])
        
        return 0
    
    def _mock_recognition(self) -> Dict[str, Any]:
        """模拟识别结果（用于演示）"""
        return {
            'total_data_size_gb': 8640.87,
            'table_count': 150,
            'database_count': 8,
            'qps': 50000,
            'tps': 20000,
            'concurrent_connections': 5000,
            'need_high_availability': True,
            'need_disaster_recovery': True,
            'need_read_write_split': True,
            'data_growth_rate': 30,
            '_is_mock': True
        }


# 测试代码
if __name__ == '__main__':
    recognizer = ImageTableRecognizer()
    
    # 测试文本提取
    test_text = """
    数据库迁移清单
    数据总量: 8640.87 GB
    表数量: 150
    QPS: 50000
    TPS: 20000
    并发连接数: 5000
    需要高可用: 是
    """
    
    result = recognizer._extract_data_from_text(test_text)
    print("识别结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
