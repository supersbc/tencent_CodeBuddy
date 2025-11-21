#!/usr/bin/env python3
"""
加载真实训练数据到系统
"""

import json
from training_system import TrainingSystem
from model import TDSQLArchitecturePredictor

def load_real_training_data():
    """加载真实训练数据"""
    print("🔄 正在加载真实训练数据...")
    
    # 初始化系统
    model = TDSQLArchitecturePredictor()
    trainer = TrainingSystem(model)
    
    # 读取真实训练数据
    try:
        with open('training_data.json', 'r', encoding='utf-8') as f:
            cases = json.load(f)
        
        print(f"📊 找到 {len(cases)} 个真实案例")
        
        # 加载每个案例
        loaded_count = 0
        for case in cases:
            try:
                case_id = trainer.add_case(
                    input_data=case['input'],
                    output_data=case['output'],
                    feedback=case.get('metadata', {})
                )
                loaded_count += 1
                print(f"  ✅ 案例 {loaded_count}: {case.get('metadata', {}).get('description', 'N/A')}")
            except Exception as e:
                print(f"  ❌ 加载失败: {str(e)}")
        
        print(f"\n✅ 成功加载 {loaded_count}/{len(cases)} 个案例")
        
        # 显示统计信息
        stats = trainer.get_statistics()
        print(f"\n📈 训练集统计:")
        print(f"  - 总案例数: {stats['total_cases']}")
        print(f"  - 架构类型分布: {stats['architecture_distribution']}")
        
        # 自动训练模型
        print(f"\n🚀 开始训练模型...")
        success = trainer.train(epochs=50, batch_size=4, learning_rate=0.001)
        
        if success:
            print(f"✅ 训练完成!")
            print(f"  - 训练案例数: {loaded_count}")
            print(f"  - 模型已保存")
        else:
            print(f"⚠️  训练未执行（可能是数据不足或PyTorch未安装）")
        
        return True
        
    except FileNotFoundError:
        print("❌ 未找到训练数据文件 training_data.json")
        print("💡 请先运行: python3 real_training_data.py")
        return False
    except Exception as e:
        print(f"❌ 加载失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    load_real_training_data()
