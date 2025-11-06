#!/usr/bin/env python3
"""
测试文件上传功能
"""

import requests
import json

def test_file_upload():
    """测试文件上传"""
    url = "http://127.0.0.1:5173/api/upload"
    
    print("=" * 60)
    print("🧪 测试文件上传功能")
    print("=" * 60)
    
    # 测试JSON文件上传
    print("\n📤 测试1: 上传JSON文件")
    with open('test_upload.json', 'rb') as f:
        files = {'file': ('test_upload.json', f, 'application/json')}
        response = requests.post(url, files=files)
        result = response.json()
        
        if result.get('success'):
            print("✅ JSON文件上传成功")
            print(f"提取方法: {result.get('method')}")
            print(f"提取参数: {json.dumps(result.get('data'), indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ 上传失败: {result.get('error')}")
    
    # 测试Excel文件上传（如果存在）
    import os
    if os.path.exists('test_data.xlsx'):
        print("\n📤 测试2: 上传Excel文件")
        with open('test_data.xlsx', 'rb') as f:
            files = {'file': ('test_data.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
            response = requests.post(url, files=files)
            result = response.json()
            
            if result.get('success'):
                print("✅ Excel文件上传成功")
                print(f"提取方法: {result.get('method')}")
                print(f"提取参数: {json.dumps(result.get('data'), indent=2, ensure_ascii=False)}")
            else:
                print(f"❌ 上传失败: {result.get('error')}")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    test_file_upload()
