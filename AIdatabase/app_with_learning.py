"""
支持自我学习的 TDSQL 架构预测系统
用户可以提交实际案例，系统会自动学习并优化预测准确性
"""

from flask import Flask, render_template, request, jsonify
import json
import os
from werkzeug.utils import secure_filename
from model import TDSQLArchitecturePredictor
from architecture_calculator import ArchitectureCalculator
from enhanced_calculator import EnhancedArchitectureCalculator
from training_system import TrainingSystem
from image_ocr import ImageTableRecognizer
from model_library_manager import ModelLibraryManager
from custom_model_builder import CustomModelBuilder
from parameter_form_generator import ParameterFormGenerator

app = Flask(__name__)

# 配置上传
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'xlsx', 'xls'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# 创建上传目录
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 初始化处理器
architecture_calculator = ArchitectureCalculator()
enhanced_calculator = EnhancedArchitectureCalculator()  # 增强版计算器
model = TDSQLArchitecturePredictor()
trainer = TrainingSystem(model)
recognizer = ImageTableRecognizer()
library_manager = ModelLibraryManager()  # 模型库管理器
custom_builder = CustomModelBuilder()  # 自定义模型库构建器
form_generator = ParameterFormGenerator()  # 参数表单生成器

print("✅ TDSQL 架构智能预测系统初始化成功")
print("🧠 支持自我学习和持续优化")

@app.route('/')
def index():
    """主页"""
    return render_template('index_learning.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    """分析上传的图片"""
    try:
        # 使用模拟数据
        extracted_data = {
            'total_data_size_gb': 8640.87,
            'table_count': 150,
            'database_count': 8,
            'qps': 50000,
            'tps': 20000,
            'concurrent_connections': 5000,
            'need_high_availability': True,
            'need_disaster_recovery': True,
            'need_read_write_split': True,
            'source_db_types': ['MySQL', 'Oracle'],
            'max_table_size_gb': 1000,
            'avg_table_size_gb': 57.6,
            'data_growth_rate': 30
        }
        
        prediction = model.predict(extracted_data)
        resources = architecture_calculator.calculate_resources(extracted_data, prediction)
        
        report = {
            'extracted_data': extracted_data,
            'architecture': prediction,
            'resources': resources,
            'recommendations': generate_recommendations(extracted_data, prediction, resources)
        }
        
        return jsonify(report)
    
    except Exception as e:
        print(f"错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'处理失败: {str(e)}'}), 500

@app.route('/api/manual_input', methods=['POST'])
def manual_input():
    """手动输入数据分析"""
    try:
        data = request.get_json()
        prediction = model.predict(data)
        
        # 使用增强版计算器获取详细清单
        resources = enhanced_calculator.calculate_resources(data, prediction)
        
        report = {
            'architecture': prediction,
            'resources': resources,
            'recommendations': generate_recommendations(data, prediction, resources)
        }
        
        return jsonify(report)
    
    except Exception as e:
        return jsonify({'error': f'处理失败: {str(e)}'}), 500

@app.route('/api/submit_case', methods=['POST'])
def submit_case():
    """提交实际案例用于训练"""
    try:
        data = request.get_json()
        
        input_data = data.get('input')
        output_data = data.get('output')
        feedback = data.get('feedback', '')
        
        # 添加案例
        case_id = trainer.add_case(input_data, output_data, feedback)
        
        # 获取统计信息
        stats = trainer.get_statistics()
        
        return jsonify({
            'success': True,
            'case_id': case_id,
            'message': '案例已成功添加到训练集',
            'statistics': stats
        })
    
    except Exception as e:
        return jsonify({'error': f'提交失败: {str(e)}'}), 500

@app.route('/api/train_model', methods=['POST'])
def train_model():
    """触发模型训练"""
    try:
        data = request.get_json()
        epochs = data.get('epochs', 50)
        
        # 开始训练
        success = trainer.train(epochs=epochs, batch_size=2, learning_rate=0.001)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'模型训练完成，共 {epochs} 轮'
            })
        else:
            return jsonify({
                'success': False,
                'message': '训练数据不足或 PyTorch 未安装'
            })
    
    except Exception as e:
        return jsonify({'error': f'训练失败: {str(e)}'}), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """获取训练统计信息"""
    try:
        stats = trainer.get_statistics()
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({'error': f'获取统计失败: {str(e)}'}), 500

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """提交预测反馈"""
    try:
        data = request.get_json()
        
        # 记录反馈
        feedback_data = {
            'timestamp': data.get('timestamp'),
            'input': data.get('input'),
            'predicted': data.get('predicted'),
            'actual': data.get('actual'),
            'rating': data.get('rating'),
            'comment': data.get('comment')
        }
        
        # 如果提供了实际结果，添加为训练案例
        if data.get('actual'):
            case_id = trainer.add_case(
                data.get('input'),
                data.get('actual'),
                feedback_data
            )
            
            return jsonify({
                'success': True,
                'message': '反馈已提交，并添加到训练集',
                'case_id': case_id
            })
        else:
            return jsonify({
                'success': True,
                'message': '反馈已记录'
            })
    
    except Exception as e:
        return jsonify({'error': f'提交反馈失败: {str(e)}'}), 500

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/recognize_file', methods=['POST'])
def recognize_file():
    """识别上传的图片或Excel文件"""
    try:
        # 检查文件
        if 'file' not in request.files:
            return jsonify({'error': '没有上传文件'}), 400
        
        file = request.files['file']
        mode = request.form.get('mode', 'predict')
        
        if file.filename == '':
            return jsonify({'error': '文件名为空'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': '不支持的文件类型'}), 400
        
        # 保存文件
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # 识别文件
        file_ext = filename.rsplit('.', 1)[1].lower()
        
        if file_ext in ['xlsx', 'xls']:
            # Excel文件识别
            extracted_data = recognizer.recognize_excel(filepath)
        else:
            # 图片识别
            extracted_data = recognizer.recognize_image(filepath)
        
        # 删除临时文件
        try:
            os.remove(filepath)
        except:
            pass
        
        # 返回识别结果
        return jsonify({
            'success': True,
            'data': extracted_data,
            'is_mock': extracted_data.get('_is_mock', False)
        })
    
    except Exception as e:
        print(f"文件识别错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'识别失败: {str(e)}'}), 500

def generate_recommendations(data, architecture, resources):
    """生成迁移建议"""
    recommendations = []
    
    total_data_gb = data.get('total_data_size_gb', 0)
    if total_data_gb > 10000:
        recommendations.append({
            'type': 'warning',
            'title': '大数据量迁移',
            'content': f'数据量达到 {total_data_gb} GB，建议分批迁移，预计迁移时间 {total_data_gb / 100:.1f} 小时'
        })
    
    if architecture['architecture_type'] == 'distributed':
        recommendations.append({
            'type': 'info',
            'title': '分布式架构',
            'content': '推荐使用 TDSQL 分布式架构，支持水平扩展和高可用'
        })
    
    if data.get('qps', 0) > 10000:
        recommendations.append({
            'type': 'success',
            'title': '高性能配置',
            'content': '建议启用读写分离和缓存优化，提升查询性能'
        })
    
    if data.get('need_high_availability', False):
        recommendations.append({
            'type': 'info',
            'title': '高可用部署',
            'content': f'已配置 {architecture["replica_count"]} 个副本，确保服务高可用性'
        })
    
    return recommendations

# ==================== 模型库管理 API ====================

@app.route('/model_library')
def model_library_page():
    """模型库管理页面"""
    return render_template('model_library.html')

@app.route('/api/model_libraries', methods=['GET'])
def get_model_libraries():
    """获取所有可用的模型库列表"""
    try:
        libraries = library_manager.list_available_libraries()
        return jsonify(libraries)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download_library', methods=['POST'])
def download_library():
    """下载模型库"""
    try:
        data = request.get_json()
        library_id = data.get('library_id')
        
        if not library_id:
            return jsonify({'error': '缺少library_id参数'}), 400
        
        result = library_manager.download_library(library_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/use_library', methods=['POST'])
def use_library():
    """使用指定的模型库"""
    try:
        data = request.get_json()
        library_id = data.get('library_id')
        
        if not library_id:
            return jsonify({'error': '缺少library_id参数'}), 400
        
        # 加载模型库数据
        cases = library_manager.load_library(library_id)
        
        if cases is None:
            return jsonify({'error': '模型库未安装或加载失败'}), 400
        
        # 将案例加载到训练系统
        loaded_count = 0
        for case in cases:
            try:
                trainer.add_case(
                    input_data=case['input'],
                    output_data=case['output'],
                    feedback=case.get('metadata', {})
                )
                loaded_count += 1
            except Exception as e:
                print(f"加载案例失败: {str(e)}")
        
        return jsonify({
            'success': True,
            'library_id': library_id,
            'loaded_cases': loaded_count
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete_library', methods=['POST'])
def delete_library():
    """删除模型库"""
    try:
        data = request.get_json()
        library_id = data.get('library_id')
        
        if not library_id:
            return jsonify({'error': '缺少library_id参数'}), 400
        
        # 检查是否是自定义库
        if library_id.startswith('custom_'):
            success = custom_builder.delete_library(library_id)
        else:
            success = library_manager.delete_library(library_id)
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': '删除失败或模型库不存在'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== 自定义模型库 API ====================

@app.route('/api/create_custom_library', methods=['POST'])
def create_custom_library():
    """创建自定义模型库"""
    try:
        data = request.get_json()
        
        name = data.get('name')
        description = data.get('description', '')
        industry = data.get('industry', '通用')
        author = data.get('author', 'User')
        version = data.get('version', 'v1.0.0')
        
        if not name:
            return jsonify({'error': '缺少模型库名称'}), 400
        
        result = custom_builder.create_custom_library(
            name=name,
            description=description,
            industry=industry,
            author=author,
            version=version
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/add_case_to_custom_library', methods=['POST'])
def add_case_to_custom_library():
    """向自定义模型库添加案例"""
    try:
        data = request.get_json()
        
        library_id = data.get('library_id')
        input_data = data.get('input_data')
        output_data = data.get('output_data')
        metadata = data.get('metadata', {})
        
        if not library_id or not input_data or not output_data:
            return jsonify({'error': '缺少必要参数'}), 400
        
        success = custom_builder.add_case_to_library(
            library_id,
            input_data,
            output_data,
            metadata
        )
        
        if success:
            # 获取更新后的库信息
            library_info = custom_builder.get_library_info(library_id)
            return jsonify({
                'success': True,
                'total_cases': library_info['metadata']['total_cases']
            })
        else:
            return jsonify({'error': '添加案例失败'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/import_library', methods=['POST'])
def import_library():
    """导入模型库文件"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': '没有上传文件'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': '文件名为空'}), 400
        
        # 保存临时文件
        filename = secure_filename(file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(temp_path)
        
        # 导入模型库
        result = custom_builder.import_library(temp_path)
        
        # 删除临时文件
        try:
            os.remove(temp_path)
        except:
            pass
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export_library/<library_id>', methods=['GET'])
def export_library(library_id):
    """导出模型库"""
    try:
        library_info = custom_builder.get_library_info(library_id)
        
        if not library_info:
            return jsonify({'error': '模型库不存在'}), 404
        
        # 返回JSON数据
        return jsonify(library_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/parameter_config', methods=['GET'])
def get_parameter_config():
    """获取参数配置"""
    try:
        mode = request.args.get('mode', 'simplified')  # simplified 或 advanced
        
        if mode == 'simplified':
            config = form_generator.generate_simplified_form()
        else:
            config = form_generator.generate_advanced_form()
        
        return jsonify(config)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/validate_parameters', methods=['POST'])
def validate_parameters():
    """验证参数"""
    try:
        from professional_parameters import ParameterHelper
        
        data = request.get_json()
        is_valid, errors = ParameterHelper.validate_parameters(data)
        
        return jsonify({
            'valid': is_valid,
            'errors': errors
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 TDSQL 架构智能预测系统 (支持自我学习)")
    print("="*60)
    print("📍 访问地址: http://localhost:5173")
    print("🧠 功能特性:")
    print("  ✅ 智能架构预测")
    print("  ✅ 提交实际案例")
    print("  ✅ 模型自我训练")
    print("  ✅ 持续优化准确性")
    print("="*60 + "\n")
    
    # 获取当前统计
    stats = trainer.get_statistics()
    print(f"📊 当前训练集: {stats['total_cases']} 个案例\n")
    
    app.run(debug=True, host='0.0.0.0', port=5173)
