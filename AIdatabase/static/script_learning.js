// 全局变量
let currentPrediction = null;
let currentInput = null;

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', function() {
    loadStatistics();
});

// 切换标签页
function switchTab(tabName) {
    // 隐藏所有标签页
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // 显示选中的标签页
    if (tabName === 'predict') {
        document.getElementById('predictTab').classList.add('active');
        document.querySelectorAll('.tab')[0].classList.add('active');
    } else if (tabName === 'submit') {
        document.getElementById('submitTab').classList.add('active');
        document.querySelectorAll('.tab')[1].classList.add('active');
    } else if (tabName === 'feedback') {
        document.getElementById('feedbackTab').classList.add('active');
        document.querySelectorAll('.tab')[2].classList.add('active');
    }
}

// 加载统计信息
function loadStatistics() {
    fetch('/api/statistics')
        .then(response => response.json())
        .then(data => {
            document.getElementById('totalCases').textContent = data.total_cases || 0;
            document.getElementById('trainedCases').textContent = data.trained_cases || 0;
            
            // 显示架构分布
            if (data.architecture_distribution) {
                console.log('架构分布:', data.architecture_distribution);
            }
        })
        .catch(error => {
            console.error('加载统计失败:', error);
        });
}

// 手动输入分析
function analyzeManualInput() {
    const data = {
        total_data_size_gb: parseFloat(document.getElementById('dataSizeInput').value) || 0,
        table_count: parseInt(document.getElementById('tableCountInput').value) || 0,
        database_count: Math.max(1, Math.ceil((parseInt(document.getElementById('tableCountInput').value) || 0) / 10)),
        qps: parseInt(document.getElementById('qpsInput').value) || 0,
        tps: parseInt(document.getElementById('tpsInput').value) || 0,
        concurrent_connections: parseInt(document.getElementById('connectionsInput').value) || 1000,
        need_high_availability: document.getElementById('haCheckbox').checked,
        need_disaster_recovery: document.getElementById('drCheckbox').checked,
        need_read_write_split: document.getElementById('rwSplitCheckbox').checked,
        source_db_types: ['MySQL'],
        max_table_size_gb: (parseFloat(document.getElementById('dataSizeInput').value) || 0) / 10,
        avg_table_size_gb: (parseFloat(document.getElementById('dataSizeInput').value) || 0) / (parseInt(document.getElementById('tableCountInput').value) || 1),
        data_growth_rate: parseFloat(document.getElementById('growthRateInput').value) || 20
    };

    if (data.total_data_size_gb === 0) {
        alert('请至少输入数据总量！');
        return;
    }

    currentInput = data;
    showLoading('正在预测架构...');

    fetch('/api/manual_input', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        hideLoading();
        if (result.error) {
            alert('分析失败: ' + result.error);
        } else {
            currentPrediction = result;
            displayResults(result);
        }
    })
    .catch(error => {
        hideLoading();
        alert('请求失败: ' + error.message);
    });
}

// 显示结果
function displayResults(data) {
    document.getElementById('resultSection').style.display = 'block';
    
    // 显示架构信息
    displayArchitecture(data.architecture);
    
    // 显示详细清单
    if (typeof displayServersDetailed !== 'undefined') {
        // 使用增强版显示
        displayDetailedResults(data.resources);
    } else {
        // 使用基础版显示
        displayServers(data.resources.servers);
        displayCost(data.resources.cost, data.resources.summary);
    }
    
    // 滚动到结果区域
    document.getElementById('resultSection').scrollIntoView({ behavior: 'smooth' });
}

// 显示详细结果（增强版）
function displayDetailedResults(resources) {
    // 服务器清单
    if (resources.servers) {
        document.getElementById('serverResult').innerHTML = displayServersDetailed(resources.servers);
    }
    
    // 网络设备
    if (resources.network) {
        const networkHtml = `
            <h3>🌐 网络设备清单</h3>
            ${displayNetworkDetailed(resources.network)}
        `;
        document.getElementById('networkResult').innerHTML = networkHtml;
        document.getElementById('networkResultCard').style.display = 'block';
    }
    
    // 存储配置
    if (resources.storage) {
        const storageHtml = `
            <h3>💾 存储配置清单</h3>
            ${displayStorageDetailed(resources.storage)}
        `;
        document.getElementById('storageResult').innerHTML = storageHtml;
        document.getElementById('storageResultCard').style.display = 'block';
    }
    
    // 基础设施
    if (resources.infrastructure) {
        const infraHtml = `
            <h3>🏗️ 基础设施清单</h3>
            ${displayInfrastructure(resources.infrastructure)}
        `;
        document.getElementById('infrastructureResult').innerHTML = infraHtml;
        document.getElementById('infrastructureResultCard').style.display = 'block';
    }
    
    // 详细成本
    if (resources.cost) {
        document.getElementById('costResult').innerHTML = displayCostDetailed(resources.cost);
    }
}

function displayArchitecture(arch) {
    const archTypes = {
        'standalone': '单机架构',
        'distributed': '分布式架构',
        'hybrid': '混合架构'
    };
    
    const html = `
        <div class="architecture-info">
            <div class="info-item">
                <div class="info-label">架构类型</div>
                <div class="info-value">${archTypes[arch.architecture_type] || arch.architecture_type}</div>
            </div>
            <div class="info-item">
                <div class="info-label">节点数量</div>
                <div class="info-value">${arch.node_count} 个</div>
            </div>
            <div class="info-item">
                <div class="info-label">分片数量</div>
                <div class="info-value">${arch.shard_count} 个</div>
            </div>
            <div class="info-item">
                <div class="info-label">副本数量</div>
                <div class="info-value">${arch.replica_count} 个</div>
            </div>
            <div class="info-item">
                <div class="info-label">预测置信度</div>
                <div class="info-value">${(arch.confidence * 100).toFixed(1)}%</div>
            </div>
        </div>
    `;
    
    document.getElementById('architectureResult').innerHTML = html;
}

function displayServers(servers) {
    let html = '<table class="server-table"><thead><tr><th>服务器类型</th><th>数量</th><th>规格</th><th>CPU</th><th>内存</th><th>用途</th></tr></thead><tbody>';
    
    for (const [key, server] of Object.entries(servers)) {
        html += `
            <tr>
                <td>${server.role}</td>
                <td>${server.count} 台</td>
                <td>${server.spec.toUpperCase()}</td>
                <td>${server.config.cpu} 核</td>
                <td>${server.config.memory_gb} GB</td>
                <td>${server.details}</td>
            </tr>
        `;
    }
    
    html += '</tbody></table>';
    document.getElementById('serverResult').innerHTML = html;
}

function displayCost(cost, summary) {
    const html = `
        <div class="architecture-info">
            <div class="info-item">
                <div class="info-label">硬件成本</div>
                <div class="info-value">¥${cost.hardware_cost.toLocaleString()}</div>
            </div>
            <div class="info-item">
                <div class="info-label">首年总成本</div>
                <div class="info-value">¥${cost.total_first_year.toLocaleString()}</div>
            </div>
            <div class="info-item">
                <div class="info-label">部署时间</div>
                <div class="info-value">${summary.deployment_time}</div>
            </div>
        </div>
    `;
    
    document.getElementById('costResult').innerHTML = html;
}

// 提交案例
function submitCase() {
    const inputData = {
        total_data_size_gb: parseFloat(document.getElementById('caseDataSize').value) || 0,
        qps: parseInt(document.getElementById('caseQPS').value) || 0,
        table_count: 100,
        database_count: 5,
        tps: 0,
        concurrent_connections: 1000,
        need_high_availability: true,
        need_disaster_recovery: false,
        need_read_write_split: true,
        max_table_size_gb: 100,
        avg_table_size_gb: 50,
        data_growth_rate: 20
    };
    
    const outputData = {
        architecture_type: document.getElementById('caseArchType').value,
        node_count: parseInt(document.getElementById('caseNodeCount').value) || 1,
        shard_count: parseInt(document.getElementById('caseNodeCount').value) || 1,
        replica_count: 2
    };
    
    const feedback = document.getElementById('caseFeedback').value;
    
    if (inputData.total_data_size_gb === 0) {
        alert('请输入数据总量！');
        return;
    }
    
    showLoading('正在提交案例...');
    
    fetch('/api/submit_case', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            input: inputData,
            output: outputData,
            feedback: feedback
        })
    })
    .then(response => response.json())
    .then(result => {
        hideLoading();
        if (result.success) {
            alert('✅ 案例提交成功！\n案例ID: ' + result.case_id + '\n当前训练集: ' + result.statistics.total_cases + ' 个案例');
            
            // 清空表单
            document.getElementById('caseDataSize').value = '';
            document.getElementById('caseQPS').value = '';
            document.getElementById('caseNodeCount').value = '';
            document.getElementById('caseFeedback').value = '';
            
            // 刷新统计
            loadStatistics();
        } else {
            alert('提交失败: ' + result.error);
        }
    })
    .catch(error => {
        hideLoading();
        alert('提交失败: ' + error.message);
    });
}

// 训练模型
function trainModel() {
    if (!confirm('确定要开始训练模型吗？\n这可能需要几分钟时间。')) {
        return;
    }
    
    showLoading('正在训练模型，请稍候...');
    
    fetch('/api/train_model', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            epochs: 50
        })
    })
    .then(response => response.json())
    .then(result => {
        hideLoading();
        if (result.success) {
            alert('✅ ' + result.message);
            document.getElementById('lastTraining').textContent = '刚刚';
            loadStatistics();
        } else {
            alert('⚠️  ' + result.message);
        }
    })
    .catch(error => {
        hideLoading();
        alert('训练失败: ' + error.message);
    });
}

// 设置评分
function setRating(rating) {
    document.getElementById('feedbackRating').value = rating;
    alert('已选择 ' + rating + ' 星评价');
}

// 提交反馈
function submitFeedback() {
    const rating = parseInt(document.getElementById('feedbackRating').value);
    const comment = document.getElementById('feedbackComment').value;
    
    if (!comment) {
        alert('请输入反馈意见！');
        return;
    }
    
    showLoading('正在提交反馈...');
    
    fetch('/api/feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            timestamp: new Date().toISOString(),
            input: currentInput,
            predicted: currentPrediction,
            rating: rating,
            comment: comment
        })
    })
    .then(response => response.json())
    .then(result => {
        hideLoading();
        if (result.success) {
            alert('✅ ' + result.message);
            document.getElementById('feedbackComment').value = '';
        } else {
            alert('提交失败: ' + result.error);
        }
    })
    .catch(error => {
        hideLoading();
        alert('提交失败: ' + error.message);
    });
}

// 显示加载动画
function showLoading(text) {
    document.getElementById('loadingText').textContent = text || '正在处理中...';
    document.getElementById('loadingSection').style.display = 'block';
}

// 隐藏加载动画
function hideLoading() {
    document.getElementById('loadingSection').style.display = 'none';
}

// 处理文件上传（预测分析）
function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const fileName = file.name;
    const fileType = file.type;
    
    // 更新状态
    document.getElementById('uploadStatus').textContent = `已选择: ${fileName}`;
    
    // 如果是图片，显示预览
    if (fileType.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('imagePreview').src = e.target.result;
            document.getElementById('previewSection').style.display = 'block';
        };
        reader.readAsDataURL(file);
    } else {
        document.getElementById('previewSection').style.display = 'none';
    }
    
    // 上传并识别
    uploadAndRecognize(file, 'predict');
}

// 处理案例文件上传
function handleCaseFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const fileName = file.name;
    document.getElementById('caseUploadStatus').textContent = `已选择: ${fileName}`;
    
    // 上传并识别
    uploadAndRecognize(file, 'case');
}

// 上传并识别文件
function uploadAndRecognize(file, mode) {
    showLoading('正在智能识别文件内容...');
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('mode', mode);
    
    fetch('/api/recognize_file', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(result => {
        hideLoading();
        
        if (result.error) {
            alert('识别失败: ' + result.error);
            return;
        }
        
        // 填充表单
        if (mode === 'predict') {
            fillPredictForm(result.data);
            alert('✅ 文件识别成功！已自动填充表单，请检查并补充信息。');
        } else if (mode === 'case') {
            fillCaseForm(result.data);
            alert('✅ 案例文件识别成功！已自动填充表单，请检查并补充信息。');
        }
    })
    .catch(error => {
        hideLoading();
        alert('识别失败: ' + error.message);
    });
}

// 填充预测表单
function fillPredictForm(data) {
    if (data.total_data_size_gb) {
        document.getElementById('dataSizeInput').value = data.total_data_size_gb;
    }
    if (data.table_count) {
        document.getElementById('tableCountInput').value = data.table_count;
    }
    if (data.qps) {
        document.getElementById('qpsInput').value = data.qps;
    }
    if (data.tps) {
        document.getElementById('tpsInput').value = data.tps;
    }
    if (data.concurrent_connections) {
        document.getElementById('connectionsInput').value = data.concurrent_connections;
    }
    if (data.data_growth_rate) {
        document.getElementById('growthRateInput').value = data.data_growth_rate;
    }
    
    // 设置复选框
    if (data.need_high_availability !== undefined) {
        document.getElementById('haCheckbox').checked = data.need_high_availability;
    }
    if (data.need_disaster_recovery !== undefined) {
        document.getElementById('drCheckbox').checked = data.need_disaster_recovery;
    }
    if (data.need_read_write_split !== undefined) {
        document.getElementById('rwSplitCheckbox').checked = data.need_read_write_split;
    }
}

// 填充案例表单
function fillCaseForm(data) {
    if (data.total_data_size_gb) {
        document.getElementById('caseDataSize').value = data.total_data_size_gb;
    }
    if (data.qps) {
        document.getElementById('caseQPS').value = data.qps;
    }
    if (data.node_count) {
        document.getElementById('caseNodeCount').value = data.node_count;
    }
    if (data.architecture_type) {
        document.getElementById('caseArchType').value = data.architecture_type;
    }
}
