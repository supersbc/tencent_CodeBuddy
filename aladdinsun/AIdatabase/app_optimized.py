"""
TDSQL 架构智能预测系统 - 优化版
支持完整功能 + 快速启动 + 延迟加载
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import os
from werkzeug.utils import secure_filename
import threading

app = Flask(__name__)

# 配置上传
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'xlsx', 'xls', 'pdf', 'json'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB max

# 创建上传目录
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 全局变量 - 延迟加载
_modules_loaded = False
_model = None
_architecture_calculator = None
_enhanced_calculator = None
_trainer = None
_recognizer = None
_library_manager = None
_custom_builder = None
_form_generator = None
_file_processor = None

def load_modules():
    """延迟加载所有模块"""
    global _modules_loaded, _model, _architecture_calculator, _enhanced_calculator
    global _trainer, _recognizer, _library_manager, _custom_builder, _form_generator
    global _file_processor
    
    if _modules_loaded:
        return
    
    print("🔄 开始加载模块...")
    
    try:
        from model import TDSQLArchitecturePredictor
        from architecture_calculator import ArchitectureCalculator
        from enhanced_calculator import EnhancedArchitectureCalculator
        from training_system import TrainingSystem
        from image_ocr import ImageTableRecognizer
        from model_library_manager import ModelLibraryManager
        from custom_model_builder import CustomModelBuilder
        from parameter_form_generator import ParameterFormGenerator
        from advanced_file_processor import AdvancedFileProcessor
        
        _model = TDSQLArchitecturePredictor()
        _architecture_calculator = ArchitectureCalculator()
        _enhanced_calculator = EnhancedArchitectureCalculator()
        _trainer = TrainingSystem(_model)
        _recognizer = ImageTableRecognizer()
        _library_manager = ModelLibraryManager()
        _custom_builder = CustomModelBuilder()
        _form_generator = ParameterFormGenerator()
        _file_processor = AdvancedFileProcessor()
        
        _modules_loaded = True
        print("✅ 所有模块加载完成")
    except Exception as e:
        print(f"⚠️ 模块加载警告: {str(e)}")
        print("💡 系统将以简化模式运行")

# 后台加载模块
def background_load():
    """后台加载模块"""
    load_modules()

# 启动后台加载
loading_thread = threading.Thread(target=background_load, daemon=True)
loading_thread.start()

print("✅ TDSQL 架构智能预测系统初始化成功")
print("🔄 正在后台加载完整功能...")

def get_model():
    """获取模型（确保已加载）"""
    if not _modules_loaded:
        load_modules()
    return _model

def get_file_processor():
    """获取文件处理器"""
    if not _modules_loaded:
        load_modules()
    return _file_processor

def allowed_file(filename):
    """检查文件类型"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """主页"""
    return render_template('index_optimized.html')

@app.route('/api/status', methods=['GET'])
def get_status():
    """获取系统状态"""
    return jsonify({
        'modules_loaded': _modules_loaded,
        'features': {
            'ml_prediction': _modules_loaded,
            'file_processing': _modules_loaded,
            'model_library': _modules_loaded,
            'self_learning': _modules_loaded
        }
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    """分析上传的图片"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': '没有上传文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '文件名为空'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': '不支持的文件格式'}), 400
        
        # 保存文件
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # 确保模块已加载
        if not _modules_loaded:
            load_modules()
        
        # 根据文件类型处理
        file_ext = filename.rsplit('.', 1)[1].lower()
        
        if file_ext in ['xlsx', 'xls']:
            # Excel文件处理
            extracted_data = _file_processor.process_excel(filepath)
        elif file_ext == 'pdf':
            # PDF文件处理
            extracted_data = _file_processor.process_pdf(filepath)
        elif file_ext == 'json':
            # JSON文件处理
            extracted_data = _file_processor.process_json(filepath)
        else:
            # 图片OCR处理
            extracted_data = _recognizer.recognize(filepath)
        
        # 使用模型预测
        prediction = _model.predict(extracted_data)
        
        # 计算资源
        resources = _enhanced_calculator.calculate_resources(extracted_data, prediction)
        
        # 生成报告
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
        
        # 确保模块已加载
        if not _modules_loaded:
            load_modules()
        
        # 使用模型预测架构
        prediction = _model.predict(data)
        
        # 计算所需资源
        resources = _enhanced_calculator.calculate_resources(data, prediction)
        
        # 生成详细报告
        report = {
            'architecture': prediction,
            'resources': resources,
            'recommendations': generate_recommendations(data, prediction, resources)
        }
        
        return jsonify(report)
    
    except Exception as e:
        print(f"错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'处理失败: {str(e)}'}), 500

@app.route('/api/submit_case', methods=['POST'])
def submit_case():
    """提交实际案例用于学习"""
    try:
        data = request.get_json()
        
        # 确保模块已加载
        if not _modules_loaded:
            load_modules()
        
        # 添加到训练集
        _trainer.add_case(
            data['input_data'],
            data['actual_architecture']
        )
        
        # 重新训练模型
        accuracy = _trainer.train()
        
        return jsonify({
            'success': True,
            'message': '案例已提交，模型已更新',
            'new_accuracy': accuracy,
            'total_cases': _trainer.get_case_count()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/training_stats', methods=['GET'])
def training_stats():
    """获取训练统计"""
    try:
        if not _modules_loaded:
            load_modules()
        
        stats = _trainer.get_stats()
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/model_libraries', methods=['GET'])
def get_model_libraries():
    """获取模型库列表"""
    try:
        if not _modules_loaded:
            load_modules()
        
        libraries = _library_manager.list_available_libraries()
        return jsonify({
            'success': True,
            'libraries': libraries,
            'total': len(libraries)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/library/<library_id>', methods=['GET'])
def get_library_detail(library_id):
    """获取模型库详情"""
    try:
        if not _modules_loaded:
            load_modules()
        
        library = _library_manager.get_library(library_id)
        if not library:
            return jsonify({'error': '模型库不存在'}), 404
        
        return jsonify(library)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search_cases', methods=['POST'])
def search_cases():
    """搜索相似案例"""
    try:
        data = request.get_json()
        
        if not _modules_loaded:
            load_modules()
        
        similar_cases = _library_manager.search_similar_cases(data)
        return jsonify(similar_cases)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/create_custom_library', methods=['POST'])
def create_custom_library():
    """创建自定义模型库"""
    try:
        data = request.get_json()
        
        if not _modules_loaded:
            load_modules()
        
        library_id = _custom_builder.create_library(
            name=data['name'],
            description=data.get('description', ''),
            cases=data.get('cases', [])
        )
        
        return jsonify({
            'success': True,
            'library_id': library_id,
            'message': '自定义模型库创建成功'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download_library/<library_id>', methods=['POST'])
def download_library(library_id):
    """下载模型库"""
    try:
        if not _modules_loaded:
            load_modules()
        
        result = _library_manager.download_library(library_id)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/export_library/<library_id>', methods=['GET'])
def export_library(library_id):
    """导出模型库"""
    try:
        if not _modules_loaded:
            load_modules()
        
        library_info = _custom_builder.get_library_info(library_id)
        
        if not library_info:
            return jsonify({'error': '模型库不存在'}), 404
        
        return jsonify(library_info)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/parameter_config', methods=['GET'])
def get_parameter_config():
    """获取参数配置"""
    try:
        if not _modules_loaded:
            load_modules()
        
        mode = request.args.get('mode', 'simplified')
        
        if mode == 'simplified':
            config = _form_generator.generate_simplified_form()
        else:
            config = _form_generator.generate_advanced_form()
        
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

@app.route('/api/process_multi_system', methods=['POST'])
def process_multi_system():
    """处理多系统环境"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': '没有上传文件'}), 400
        
        file = request.files['file']
        if not allowed_file(file.filename):
            return jsonify({'error': '不支持的文件格式'}), 400
        
        # 保存文件
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # 确保模块已加载
        if not _modules_loaded:
            load_modules()
        
        # 处理多系统环境
        result = _file_processor.extract_multi_system_environment(filepath)
        
        return jsonify(result)
    
    except Exception as e:
        print(f"错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'处理失败: {str(e)}'}), 500

@app.route('/api/deployment_topology', methods=['POST'])
def get_deployment_topology():
    """获取部署拓扑建议"""
    try:
        data = request.get_json()
        
        if not _modules_loaded:
            load_modules()
        
        from deployment_topology_parameters import DeploymentTopologyRecommender
        
        recommender = DeploymentTopologyRecommender()
        topology = recommender.recommend_topology(data)
        
        return jsonify(topology)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'version': '3.0',
        'modules_loaded': _modules_loaded,
        'message': 'TDSQL架构预测系统运行正常'
    })

def generate_recommendations(data, architecture, resources):
    """生成迁移建议"""
    recommendations = []
    
    # 基于数据量的建议
    total_data_gb = data.get('total_data_size_gb', 0)
    if total_data_gb > 10000:
        recommendations.append({
            'type': 'warning',
            'title': '大数据量迁移',
            'content': f'数据量达到 {total_data_gb} GB，建议分批迁移，预计迁移时间 {total_data_gb / 100:.1f} 小时'
        })
    
    # 基于架构的建议
    if architecture.get('architecture_type') == 'distributed':
        recommendations.append({
            'type': 'info',
            'title': '分布式架构',
            'content': '推荐使用 TDSQL 分布式架构，支持水平扩展和高可用'
        })
    
    # 基于性能的建议
    if data.get('qps', 0) > 10000:
        recommendations.append({
            'type': 'success',
            'title': '高性能配置',
            'content': '建议启用读写分离和缓存优化，提升查询性能'
        })
    
    # 多系统环境建议
    if data.get('system_count', 0) > 1:
        recommendations.append({
            'type': 'info',
            'title': '多系统环境',
            'content': f'检测到 {data.get("system_count")} 个系统，建议统一规划部署架构'
        })
    
    # 部署拓扑建议
    if data.get('availability_requirement'):
        avail = data['availability_requirement']
        if avail >= 99.99:
            recommendations.append({
                'type': 'warning',
                'title': '高可用要求',
                'content': '建议采用两地三中心或三地五中心部署，确保高可用性'
            })
    
    return recommendations

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 TDSQL 架构智能预测系统 (完整功能版)")
    print("="*60)
    print("📍 访问地址: http://localhost:5173")
    print("🧠 功能特性:")
    print("  ✅ 智能架构预测")
    print("  ✅ 多文件格式支持 (Excel/PDF/图片/JSON)")
    print("  ✅ 多系统环境分析")
    print("  ✅ 复杂部署拓扑建模")
    print("  ✅ 模型自我学习")
    print("  ✅ 735+ 真实案例库")
    print("="*60)
    print()
    
    # 禁用debug模式的reloader，避免多进程问题
    app.run(debug=False, host='0.0.0.0', port=5173, threaded=True, use_reloader=False)
