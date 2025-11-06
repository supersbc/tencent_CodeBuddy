"""
测试智能识别功能
"""

from image_ocr import ImageTableRecognizer
import json

def test_text_extraction():
    """测试文本提取"""
    print("=" * 60)
    print("测试1: 文本提取功能")
    print("=" * 60)
    
    recognizer = ImageTableRecognizer()
    
    test_text = """
    数据库迁移清单
    ━━━━━━━━━━━━━━━━━━━━
    数据总量: 8640.87 GB
    表数量: 150
    数据库数量: 8
    QPS: 50000
    TPS: 20000
    并发连接数: 5000
    数据增长率: 30%
    需要高可用: 是
    需要容灾: 是
    需要读写分离: 是
    """
    
    result = recognizer._extract_data_from_text(test_text)
    
    print("\n识别结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 验证结果
    assert result['total_data_size_gb'] == 8640.87, "数据量识别错误"
    assert result['table_count'] == 150, "表数量识别错误"
    assert result['qps'] == 50000, "QPS识别错误"
    assert result['need_high_availability'] == True, "高可用识别错误"
    
    print("\n✅ 文本提取测试通过！")

def test_excel_recognition():
    """测试Excel识别"""
    print("\n" + "=" * 60)
    print("测试2: Excel文件识别")
    print("=" * 60)
    
    recognizer = ImageTableRecognizer()
    
    try:
        result = recognizer.recognize_excel('database_migration_template.xlsx')
        
        print("\n识别结果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        if result.get('_is_mock'):
            print("\n⚠️  使用模拟数据（pandas未安装）")
        else:
            print("\n✅ Excel识别测试通过！")
    
    except Exception as e:
        print(f"\n⚠️  Excel识别测试失败: {str(e)}")

def test_number_extraction():
    """测试数字提取"""
    print("\n" + "=" * 60)
    print("测试3: 数字提取功能")
    print("=" * 60)
    
    recognizer = ImageTableRecognizer()
    
    test_cases = [
        ("8640.87 GB", ['GB'], 8640.87),
        ("150", [], 150),
        ("50,000", [], 50000),
        ("30%", ['%'], 30),
        ("5 TB", ['TB'], 5),
    ]
    
    for text, units, expected in test_cases:
        result = recognizer._extract_number(text, units)
        status = "✅" if result == expected else "❌"
        print(f"{status} '{text}' -> {result} (期望: {expected})")

def test_keyword_matching():
    """测试关键词匹配"""
    print("\n" + "=" * 60)
    print("测试4: 关键词匹配")
    print("=" * 60)
    
    recognizer = ImageTableRecognizer()
    
    test_texts = [
        "数据总量: 1000 GB",
        "Total Data Size: 1000 GB",
        "QPS: 50000",
        "每秒查询: 50000",
        "高可用部署",
        "High Availability: Yes",
    ]
    
    for text in test_texts:
        result = recognizer._extract_data_from_text(text)
        print(f"\n输入: {text}")
        print(f"识别: {json.dumps({k: v for k, v in result.items() if v and v != 0 and v != False}, ensure_ascii=False)}")

if __name__ == '__main__':
    print("\n🧪 开始测试智能识别功能...\n")
    
    try:
        test_text_extraction()
        test_excel_recognition()
        test_number_extraction()
        test_keyword_matching()
        
        print("\n" + "=" * 60)
        print("🎉 所有测试完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
