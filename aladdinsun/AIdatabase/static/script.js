let uploadedImage = null;

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeUpload();
    initializeManualInput();
});

function initializeUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const previewImage = document.getElementById('previewImage');
    const analyzeBtn = document.getElementById('analyzeBtn');

    // 点击上传区域
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });

    // 文件选择
    fileInput.addEventListener('change', (e) => {
        handleFileSelect(e.target.files[0]);
    });

    // 拖拽上传
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        handleFileSelect(e.dataTransfer.files[0]);
    });

    // 分析按钮
    analyzeBtn.addEventListener('click', () => {
        analyzeImage();
    });
}

function handleFileSelect(file) {
    if (!file) return;

    if (!file.type.startsWith('image/')) {
        alert('请上传图片文件！');
        return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
        const previewImage = document.getElementById('previewImage');
        const uploadPlaceholder = document.querySelector('.upload-placeholder');
        
        previewImage.src = e.target.result;
        previewImage.style.display = 'block';
        uploadPlaceholder.style.display = 'none';
        document.getElementById('analyzeBtn').style.display = 'block';
        
        uploadedImage = file;
    };
    reader.readAsDataURL(file);
}

function analyzeImage() {
    if (!uploadedImage) {
        alert('请先上传图片！');
        return;
    }

    const formData = new FormData();
    formData.append('image', uploadedImage);

    showLoading();

    fetch('/api/analyze', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        if (data.error) {
            alert('分析失败: ' + data.error);
        } else {
            displayResults(data);
        }
    })
    .catch(error => {
        hideLoading();
        alert('请求失败: ' + error.message);
    });
}

function initializeManualInput() {
    const manualAnalyzeBtn = document.getElementById('manualAnalyzeBtn');
    
    manualAnalyzeBtn.addEventListener('click', () => {
        analyzeManualInput();
    });
}

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

    showLoading();

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
            displayResults(result);
        }
    })
    .catch(error => {
        hideLoading();
        alert('请求失败: ' + error.message);
    });
}

function showLoading() {
    document.getElementById('loadingSection').style.display = 'block';
    document.getElementById('resultSection').style.display = 'none';
}

function hideLoading() {
    document.getElementById('loadingSection').style.display = 'none';
}

function displayResults(data) {
    document.getElementById('resultSection').style.display = 'block';
    
    // 显示架构信息
    displayArchitecture(data.architecture);
    
    // 显示服务器清单
    displayServers(data.resources.servers);
    
    // 显示网络设备
    displayNetwork(data.resources.switches, data.resources.network);
    
    // 显示存储配置
    displayStorage(data.resources.storage);
    
    // 显示成本估算
    displayCost(data.resources.cost, data.resources.summary);
    
    // 显示建议
    displayRecommendations(data.recommendations);
    
    // 滚动到结果区域
    document.getElementById('resultSection').scrollIntoView({ behavior: 'smooth' });
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
    let html = '<table class="server-table"><thead><tr><th>服务器类型</th><th>数量</th><th>规格</th><th>CPU</th><th>内存</th><th>磁盘</th><th>用途</th></tr></thead><tbody>';
    
    for (const [key, server] of Object.entries(servers)) {
        html += `
            <tr>
                <td>${server.role}</td>
                <td>${server.count} 台</td>
                <td>${server.spec.toUpperCase()}</td>
                <td>${server.config.cpu} 核</td>
                <td>${server.config.memory_gb} GB</td>
                <td>${server.config.disk_gb} GB</td>
                <td>${server.details}</td>
            </tr>
        `;
    }
    
    html += '</tbody></table>';
    document.getElementById('serverResult').innerHTML = html;
}

function displayNetwork(switches, network) {
    let html = '<h4>交换机配置</h4>';
    html += '<table class="switch-table"><thead><tr><th>交换机类型</th><th>数量</th><th>端口数</th><th>速率</th><th>用途</th></tr></thead><tbody>';
    
    for (const [key, sw] of Object.entries(switches)) {
        html += `
            <tr>
                <td>${sw.role}</td>
                <td>${sw.count} 台</td>
                <td>${sw.config.ports} 个</td>
                <td>${sw.config.speed}</td>
                <td>${sw.details}</td>
            </tr>
        `;
    }
    
    html += '</tbody></table>';
    
    html += '<h4 style="margin-top: 20px;">网络带宽</h4>';
    html += `
        <div class="architecture-info">
            <div class="info-item">
                <div class="info-label">平均带宽</div>
                <div class="info-value">${network.average_bandwidth_mbps} Mbps</div>
            </div>
            <div class="info-item">
                <div class="info-label">峰值带宽</div>
                <div class="info-value">${network.peak_bandwidth_mbps} Mbps</div>
            </div>
            <div class="info-item">
                <div class="info-label">推荐配置</div>
                <div class="info-value">${network.recommended}</div>
            </div>
            <div class="info-item">
                <div class="info-label">网卡配置</div>
                <div class="info-value">${network.network_cards}</div>
            </div>
        </div>
    `;
    
    document.getElementById('networkResult').innerHTML = html;
}

function displayStorage(storage) {
    const html = `
        <div class="architecture-info">
            <div class="info-item">
                <div class="info-label">总容量</div>
                <div class="info-value">${storage.total_capacity_tb} TB</div>
            </div>
            <div class="info-item">
                <div class="info-label">原始数据</div>
                <div class="info-value">${storage.raw_data_gb} GB</div>
            </div>
            <div class="info-item">
                <div class="info-label">副本数</div>
                <div class="info-value">${storage.replica_count} 个</div>
            </div>
            <div class="info-item">
                <div class="info-label">存储类型</div>
                <div class="info-value">${storage.storage_type}</div>
            </div>
            <div class="info-item">
                <div class="info-label">RAID 级别</div>
                <div class="info-value">${storage.raid_level}</div>
            </div>
            <div class="info-item">
                <div class="info-label">增长预留</div>
                <div class="info-value">${storage.growth_reserve}</div>
            </div>
        </div>
    `;
    
    document.getElementById('storageResult').innerHTML = html;
}

function displayCost(cost, summary) {
    const html = `
        <div class="architecture-info">
            <div class="info-item">
                <div class="info-label">硬件成本</div>
                <div class="info-value">¥${cost.hardware_cost.toLocaleString()}</div>
            </div>
            <div class="info-item">
                <div class="info-label">存储成本</div>
                <div class="info-value">¥${cost.storage_cost.toLocaleString()}</div>
            </div>
            <div class="info-item">
                <div class="info-label">年维护费</div>
                <div class="info-value">¥${cost.annual_maintenance.toLocaleString()}</div>
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

function displayRecommendations(recommendations) {
    let html = '';
    
    recommendations.forEach(rec => {
        html += `
            <div class="recommendation-item ${rec.type}">
                <div class="recommendation-title">${rec.title}</div>
                <div class="recommendation-content">${rec.content}</div>
            </div>
        `;
    });
    
    document.getElementById('recommendationsResult').innerHTML = html;
}

function exportReport() {
    alert('导出功能开发中...');
    // TODO: 实现导出为 PDF 或 Excel
}

function printReport() {
    window.print();
}
