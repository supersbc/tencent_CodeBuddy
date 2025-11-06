#!/usr/bin/env python3
"""
测试图片上传和识别功能
"""

import requests
import json
from PIL import Image, ImageDraw, ImageFont
import os

def create_test_image():
    """创建一个测试图片"""
    # 创建一个白色背景的图片
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # 添加文字
    text = """
    TDSQL 架构设计文档
    
    项目名称: 电商平台数据库架构
    
    业务需求:
    - 行业类型: 电商
    - 预计 QPS: 15000
    - 并发用户数: 8000
    - 数据量: 500 GB
    - 可用性要求: 99.99%
    
    技术要求:
    - 支持高并发读写
    - 数据强一致性
    - 自动故障切换
    """
    
    # 使用默认字体
    try:
        # 尝试使用系统字体
        font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 20)
    except:
        # 如果失败，使用默认字体
        font = ImageFont.load_default()
    
    # 绘制文字
    y_position = 50
    for line in text.strip().split('\n'):
        draw.text((50, y_position), line.strip(), fill='black', font=font)
        y_position += 30
    
    # 保存图片
    filepath = 'test_architecture.png'
    img.save(filepath)
    print(f"✅ 测试图片已创建: {filepath}")
    return filepath

def test_upload(filepath):
    """测试上传图片"""
    url = 'http://127.0.0.1:5173/api/analyze'
    
    print(f"\n🔄 正在上传文件: {filepath}")
    
    with open(filepath, 'rb') as f:
        files = {'file': (os.path.basename(filepath), f, 'image/png')}
        response = requests.post(url, files=files)
    
    print(f"📡 响应状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ 上传成功！")
        print("\n📊 返回数据:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        # 详细展示识别结果
        if data.get('extracted_data'):
            print("\n🔍 识别详情:")
            extracted = data['extracted_data']
            
            if extracted.get('method'):
                print(f"  识别方式: {extracted['method']}")
            
            if extracted.get('image_info'):
                info = extracted['image_info']
                print(f"  图片信息: {info['width']}x{info['height']} ({info['format']})")
            
            if extracted.get('data'):
                print("\n  提取的参数:")
                for key, value in extracted['data'].items():
                    print(f"    - {key}: {value}")
            
            if extracted.get('ocr_text'):
                print(f"\n  OCR 识别文本:")
                print("  " + "-" * 50)
                print("  " + extracted['ocr_text'][:200].replace('\n', '\n  '))
                if len(extracted['ocr_text']) > 200:
                    print("  ... (已截断)")
                print("  " + "-" * 50)
        
        if data.get('architecture'):
            print("\n🏗️ 架构推荐:")
            arch = data['architecture']
            print(f"  类型: {arch.get('type', 'N/A')}")
            print(f"  节点数: {arch.get('nodes', 'N/A')}")
            print(f"  部署模式: {arch.get('deployment', 'N/A')}")
    else:
        print(f"\n❌ 上传失败")
        print(f"错误信息: {response.text}")

def test_json_upload():
    """测试 JSON 文件上传"""
    json_data = {
        "industry": "游戏",
        "qps": 20000,
        "data_volume": 200,
        "concurrent_users": 5000,
        "availability": 99.95
    }
    
    filepath = 'test_config.json'
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 测试 JSON 已创建: {filepath}")
    
    url = 'http://127.0.0.1:5173/api/analyze'
    
    print(f"\n🔄 正在上传 JSON 文件...")
    
    with open(filepath, 'rb') as f:
        files = {'file': (filepath, f, 'application/json')}
        response = requests.post(url, files=files)
    
    print(f"📡 响应状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ JSON 上传成功！")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"\n❌ 上传失败: {response.text}")

def main():
    print("=" * 60)
    print("🧪 TDSQL 图片上传功能测试")
    print("=" * 60)
    
    # 检查服务是否运行
    try:
        response = requests.get('http://127.0.0.1:5173/api/health')
        if response.status_code == 200:
            print("✅ 服务运行正常")
            print(f"   {response.json()}")
        else:
            print("⚠️ 服务响应异常")
            return
    except Exception as e:
        print(f"❌ 无法连接到服务: {e}")
        print("   请确保服务已启动: python3 app_final.py")
        return
    
    # 测试 1: 图片上传
    print("\n" + "=" * 60)
    print("测试 1: 图片上传与识别")
    print("=" * 60)
    image_path = create_test_image()
    test_upload(image_path)
    
    # 测试 2: JSON 上传
    print("\n" + "=" * 60)
    print("测试 2: JSON 文件上传")
    print("=" * 60)
    test_json_upload()
    
    print("\n" + "=" * 60)
    print("✅ 测试完成")
    print("=" * 60)
    print("\n💡 提示:")
    print("  - 如果看到 'OCR识别' 说明 OCR 功能正常")
    print("  - 如果看到 '图像分析' 说明使用基础模式（未安装 OCR）")
    print("  - 可以安装 OCR: pip install pytesseract && brew install tesseract")
    print("\n🌐 访问 Web 界面: http://127.0.0.1:5173")

if __name__ == '__main__':
    main()
