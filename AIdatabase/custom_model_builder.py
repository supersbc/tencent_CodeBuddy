#!/usr/bin/env python3
"""
自定义模型库构建器
允许用户创建、编辑和管理自己的模型库
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class CustomModelBuilder:
    """自定义模型库构建器"""
    
    def __init__(self):
        self.custom_libraries_dir = 'model_libraries/custom'
        self.custom_config_file = 'custom_libraries.json'
        self.ensure_directories()
    
    def ensure_directories(self):
        """确保目录存在"""
        os.makedirs(self.custom_libraries_dir, exist_ok=True)
    
    def create_custom_library(self, 
                            name: str,
                            description: str,
                            industry: str = '通用',
                            author: str = 'User',
                            version: str = 'v1.0.0') -> Dict:
        """
        创建新的自定义模型库
        
        Args:
            name: 模型库名称
            description: 描述
            industry: 行业类型
            author: 作者
            version: 版本号
        
        Returns:
            创建结果
        """
        # 生成库ID
        library_id = f"custom_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 创建库信息
        library_info = {
            'id': library_id,
            'name': name,
            'description': description,
            'version': version,
            'author': author,
            'industry': industry,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'cases': [],
            'metadata': {
                'total_cases': 0,
                'accuracy': 'N/A',
                'industries': [industry],
                'features': []
            }
        }
        
        # 保存到文件
        filename = f"{library_id}.json"
        filepath = os.path.join(self.custom_libraries_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(library_info, f, ensure_ascii=False, indent=2)
        
        # 更新配置
        self._update_custom_config(library_id, library_info)
        
        print(f"✅ 自定义模型库创建成功!")
        print(f"   ID: {library_id}")
        print(f"   名称: {name}")
        print(f"   文件: {filepath}")
        
        return {
            'success': True,
            'library_id': library_id,
            'filepath': filepath,
            'info': library_info
        }
    
    def add_case_to_library(self, 
                           library_id: str,
                           input_data: Dict,
                           output_data: Dict,
                           metadata: Optional[Dict] = None) -> bool:
        """
        向自定义模型库添加案例
        
        Args:
            library_id: 模型库ID
            input_data: 输入数据
            output_data: 输出数据
            metadata: 元数据
        
        Returns:
            是否成功
        """
        filepath = self._get_library_filepath(library_id)
        
        if not os.path.exists(filepath):
            print(f"❌ 模型库不存在: {library_id}")
            return False
        
        # 加载现有库
        with open(filepath, 'r', encoding='utf-8') as f:
            library = json.load(f)
        
        # 创建案例
        case = {
            'id': f"case_{len(library['cases']) + 1}",
            'timestamp': datetime.now().isoformat(),
            'input': input_data,
            'output': output_data,
            'metadata': metadata or {}
        }
        
        # 添加案例
        library['cases'].append(case)
        library['metadata']['total_cases'] = len(library['cases'])
        library['updated_at'] = datetime.now().isoformat()
        
        # 保存
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(library, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 案例已添加到模型库: {library['name']}")
        print(f"   当前案例数: {library['metadata']['total_cases']}")
        
        return True
    
    def import_cases_from_file(self, 
                              library_id: str,
                              cases_file: str) -> Dict:
        """
        从文件批量导入案例
        
        Args:
            library_id: 模型库ID
            cases_file: 案例文件路径
        
        Returns:
            导入结果
        """
        if not os.path.exists(cases_file):
            return {'success': False, 'error': '案例文件不存在'}
        
        try:
            with open(cases_file, 'r', encoding='utf-8') as f:
                cases = json.load(f)
            
            if not isinstance(cases, list):
                return {'success': False, 'error': '案例文件格式错误，应为数组'}
            
            imported_count = 0
            for case in cases:
                if 'input' in case and 'output' in case:
                    success = self.add_case_to_library(
                        library_id,
                        case['input'],
                        case['output'],
                        case.get('metadata', {})
                    )
                    if success:
                        imported_count += 1
            
            return {
                'success': True,
                'imported_count': imported_count,
                'total_cases': len(cases)
            }
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def list_custom_libraries(self) -> List[Dict]:
        """列出所有自定义模型库"""
        libraries = []
        
        if not os.path.exists(self.custom_libraries_dir):
            return libraries
        
        for filename in os.listdir(self.custom_libraries_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.custom_libraries_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        library = json.load(f)
                        libraries.append({
                            'id': library['id'],
                            'name': library['name'],
                            'description': library['description'],
                            'version': library['version'],
                            'author': library.get('author', 'Unknown'),
                            'cases': library['metadata']['total_cases'],
                            'industry': library.get('industry', '通用'),
                            'created_at': library.get('created_at', 'N/A'),
                            'updated_at': library.get('updated_at', 'N/A'),
                            'filepath': filepath
                        })
                except Exception as e:
                    print(f"加载库失败 {filename}: {str(e)}")
        
        return libraries
    
    def get_library_info(self, library_id: str) -> Optional[Dict]:
        """获取模型库详细信息"""
        filepath = self._get_library_filepath(library_id)
        
        if not os.path.exists(filepath):
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def update_library_metadata(self, 
                               library_id: str,
                               metadata: Dict) -> bool:
        """更新模型库元数据"""
        filepath = self._get_library_filepath(library_id)
        
        if not os.path.exists(filepath):
            return False
        
        with open(filepath, 'r', encoding='utf-8') as f:
            library = json.load(f)
        
        # 更新元数据
        for key, value in metadata.items():
            if key in library:
                library[key] = value
        
        library['updated_at'] = datetime.now().isoformat()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(library, f, ensure_ascii=False, indent=2)
        
        return True
    
    def delete_library(self, library_id: str) -> bool:
        """删除自定义模型库"""
        filepath = self._get_library_filepath(library_id)
        
        if not os.path.exists(filepath):
            return False
        
        try:
            os.remove(filepath)
            print(f"✅ 模型库已删除: {library_id}")
            return True
        except Exception as e:
            print(f"❌ 删除失败: {str(e)}")
            return False
    
    def export_library(self, library_id: str, output_file: str) -> bool:
        """导出模型库"""
        filepath = self._get_library_filepath(library_id)
        
        if not os.path.exists(filepath):
            return False
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                library = json.load(f)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(library, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 模型库已导出到: {output_file}")
            return True
        except Exception as e:
            print(f"❌ 导出失败: {str(e)}")
            return False
    
    def import_library(self, import_file: str) -> Dict:
        """导入模型库"""
        if not os.path.exists(import_file):
            return {'success': False, 'error': '文件不存在'}
        
        try:
            with open(import_file, 'r', encoding='utf-8') as f:
                library = json.load(f)
            
            # 生成新的ID
            library_id = f"custom_imported_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            library['id'] = library_id
            library['imported_at'] = datetime.now().isoformat()
            
            # 保存
            filename = f"{library_id}.json"
            filepath = os.path.join(self.custom_libraries_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(library, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 模型库已导入: {library['name']}")
            print(f"   案例数: {library['metadata']['total_cases']}")
            
            return {
                'success': True,
                'library_id': library_id,
                'name': library['name'],
                'cases': library['metadata']['total_cases']
            }
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _get_library_filepath(self, library_id: str) -> str:
        """获取模型库文件路径"""
        return os.path.join(self.custom_libraries_dir, f"{library_id}.json")
    
    def _update_custom_config(self, library_id: str, library_info: Dict):
        """更新自定义库配置"""
        config = {}
        
        if os.path.exists(self.custom_config_file):
            with open(self.custom_config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        
        config[library_id] = {
            'name': library_info['name'],
            'created_at': library_info['created_at'],
            'filepath': self._get_library_filepath(library_id)
        }
        
        with open(self.custom_config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)


def create_example_custom_library():
    """创建示例自定义模型库"""
    builder = CustomModelBuilder()
    
    # 创建自定义库
    result = builder.create_custom_library(
        name="我的TDSQL模型库",
        description="基于我的实际项目经验构建的模型库",
        industry="互联网",
        author="用户自定义",
        version="v1.0.0"
    )
    
    library_id = result['library_id']
    
    # 添加示例案例
    example_cases = [
        {
            'input': {
                'total_data_size_gb': 500,
                'table_count': 800,
                'qps': 5000,
                'tps': 2000,
                'concurrent_connections': 500,
                'need_high_availability': True,
                'need_disaster_recovery': False,
                'need_read_write_split': True,
                'data_growth_rate': 20,
                'industry': '互联网'
            },
            'output': {
                'architecture_type': 'distributed',
                'node_count': 4,
                'shard_count': 2,
                'replica_count': 2,
                'proxy_count': 2,
                'estimated_cost': 800000
            },
            'metadata': {
                'scenario': '社交平台',
                'verified': True,
                'notes': '实际生产环境案例'
            }
        },
        {
            'input': {
                'total_data_size_gb': 200,
                'table_count': 300,
                'qps': 2000,
                'tps': 800,
                'concurrent_connections': 200,
                'need_high_availability': True,
                'need_disaster_recovery': False,
                'need_read_write_split': False,
                'data_growth_rate': 15,
                'industry': '互联网'
            },
            'output': {
                'architecture_type': 'standalone',
                'node_count': 2,
                'shard_count': 1,
                'replica_count': 1,
                'proxy_count': 1,
                'estimated_cost': 300000
            },
            'metadata': {
                'scenario': '内容管理系统',
                'verified': True,
                'notes': '中小型应用'
            }
        }
    ]
    
    for case in example_cases:
        builder.add_case_to_library(
            library_id,
            case['input'],
            case['output'],
            case['metadata']
        )
    
    print(f"\n✅ 示例自定义模型库创建完成!")
    print(f"   库ID: {library_id}")
    print(f"   案例数: {len(example_cases)}")
    
    return library_id


def main():
    """主函数 - 演示自定义模型库功能"""
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║              自定义模型库构建器                                    ║")
    print("╚══════════════════════════════════════════════════════════════════╝\n")
    
    builder = CustomModelBuilder()
    
    # 创建示例库
    print("📝 创建示例自定义模型库...\n")
    library_id = create_example_custom_library()
    
    print("\n" + "="*70 + "\n")
    
    # 列出所有自定义库
    print("📚 当前的自定义模型库:\n")
    libraries = builder.list_custom_libraries()
    
    for i, lib in enumerate(libraries, 1):
        print(f"{i}. {lib['name']} ({lib['version']})")
        print(f"   作者: {lib['author']}")
        print(f"   行业: {lib['industry']}")
        print(f"   案例数: {lib['cases']}")
        print(f"   创建时间: {lib['created_at']}")
        print(f"   文件: {lib['filepath']}")
        print()
    
    print("="*70)
    print("\n✅ 自定义模型库演示完成！")
    print(f"\n💡 自定义库保存在: {builder.custom_libraries_dir}/")


if __name__ == '__main__':
    main()
