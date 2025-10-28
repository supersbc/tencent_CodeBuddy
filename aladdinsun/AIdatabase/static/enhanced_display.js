/**
 * 增强的结果显示函数
 * 显示详细的设备清单和成本明细
 */

// 显示详细的服务器清单
function displayServersDetailed(servers) {
    let html = `
        <div class="detailed-table-container">
            <table class="detailed-table">
                <thead>
                    <tr>
                        <th>服务器类型</th>
                        <th>型号</th>
                        <th>数量</th>
                        <th>CPU</th>
                        <th>内存</th>
                        <th>磁盘</th>
                        <th>单价</th>
                        <th>总价</th>
                        <th>用途说明</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    let totalPrice = 0;
    let totalServers = 0;
    let totalCPU = 0;
    let totalMemory = 0;
    
    for (const [key, server] of Object.entries(servers)) {
        if (!server) continue;
        
        totalPrice += server.total_price || 0;
        totalServers += server.count || 0;
        totalCPU += server.total_cpu || 0;
        totalMemory += server.total_memory_gb || 0;
        
        html += `
            <tr>
                <td><strong>${server.role}</strong></td>
                <td>${server.config.model || '-'}</td>
                <td>${server.count} 台</td>
                <td>${server.config.cpu} 核</td>
                <td>${server.config.memory_gb} GB</td>
                <td>${server.config.disk_gb} GB</td>
                <td>¥${(server.unit_price || 0).toLocaleString()}</td>
                <td><strong>¥${(server.total_price || 0).toLocaleString()}</strong></td>
                <td>${server.details}</td>
            </tr>
        `;
    }
    
    html += `
                </tbody>
                <tfoot>
                    <tr class="total-row">
                        <td colspan="2"><strong>合计</strong></td>
                        <td><strong>${totalServers} 台</strong></td>
                        <td><strong>${totalCPU} 核</strong></td>
                        <td><strong>${totalMemory} GB</strong></td>
                        <td colspan="2"></td>
                        <td><strong>¥${totalPrice.toLocaleString()}</strong></td>
                        <td></td>
                    </tr>
                </tfoot>
            </table>
        </div>
    `;
    
    return html;
}

// 显示详细的网络设备清单
function displayNetworkDetailed(network) {
    let html = `
        <div class="detailed-table-container">
            <table class="detailed-table">
                <thead>
                    <tr>
                        <th>设备类型</th>
                        <th>型号</th>
                        <th>数量</th>
                        <th>规格</th>
                        <th>单价</th>
                        <th>总价</th>
                        <th>用途说明</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    let totalPrice = 0;
    
    for (const [key, device] of Object.entries(network)) {
        if (!device || !device.count) continue;
        
        totalPrice += device.total_price || 0;
        
        const spec = device.config?.speed || device.config?.ports || '-';
        const model = device.config?.model || '-';
        
        html += `
            <tr>
                <td><strong>${device.role}</strong></td>
                <td>${model}</td>
                <td>${device.count} 台</td>
                <td>${spec}</td>
                <td>¥${(device.unit_price || 0).toLocaleString()}</td>
                <td><strong>¥${(device.total_price || 0).toLocaleString()}</strong></td>
                <td>${device.details}</td>
            </tr>
        `;
    }
    
    html += `
                </tbody>
                <tfoot>
                    <tr class="total-row">
                        <td colspan="5"><strong>合计</strong></td>
                        <td><strong>¥${totalPrice.toLocaleString()}</strong></td>
                        <td></td>
                    </tr>
                </tfoot>
            </table>
        </div>
    `;
    
    return html;
}

// 显示详细的存储配置
function displayStorageDetailed(storage) {
    let html = `
        <div class="detailed-table-container">
            <table class="detailed-table">
                <thead>
                    <tr>
                        <th>存储类型</th>
                        <th>容量(TB)</th>
                        <th>类型</th>
                        <th>IOPS</th>
                        <th>单价/TB</th>
                        <th>总价</th>
                        <th>用途说明</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    const storageTypes = ['primary_storage', 'backup_storage', 'log_storage'];
    let totalPrice = 0;
    let totalCapacity = 0;
    
    for (const type of storageTypes) {
        const item = storage[type];
        if (!item) continue;
        
        totalPrice += item.total_price || 0;
        totalCapacity += item.capacity_tb || 0;
        
        html += `
            <tr>
                <td><strong>${item.role}</strong></td>
                <td>${item.capacity_tb} TB</td>
                <td>${item.config.type}</td>
                <td>${(item.config.iops || 0).toLocaleString()}</td>
                <td>¥${(item.price_per_tb || 0).toLocaleString()}</td>
                <td><strong>¥${(item.total_price || 0).toLocaleString()}</strong></td>
                <td>${item.details}</td>
            </tr>
        `;
    }
    
    html += `
                </tbody>
                <tfoot>
                    <tr class="total-row">
                        <td><strong>合计</strong></td>
                        <td><strong>${totalCapacity} TB</strong></td>
                        <td colspan="3"></td>
                        <td><strong>¥${totalPrice.toLocaleString()}</strong></td>
                        <td></td>
                    </tr>
                </tfoot>
            </table>
        </div>
    `;
    
    return html;
}

// 显示基础设施
function displayInfrastructure(infrastructure) {
    let html = `
        <div class="detailed-table-container">
            <table class="detailed-table">
                <thead>
                    <tr>
                        <th>设施类型</th>
                        <th>数量/规格</th>
                        <th>单价</th>
                        <th>总价</th>
                        <th>说明</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    const items = ['racks', 'pdu', 'ups', 'cables'];
    let totalPrice = 0;
    
    for (const item of items) {
        const data = infrastructure[item];
        if (!data) continue;
        
        totalPrice += data.total_price || 0;
        
        const quantity = data.count || data.capacity_kw || '-';
        
        html += `
            <tr>
                <td><strong>${getInfraName(item)}</strong></td>
                <td>${quantity}</td>
                <td>¥${(data.unit_price || 0).toLocaleString()}</td>
                <td><strong>¥${(data.total_price || 0).toLocaleString()}</strong></td>
                <td>${data.details}</td>
            </tr>
        `;
    }
    
    html += `
                </tbody>
                <tfoot>
                    <tr class="total-row">
                        <td colspan="3"><strong>合计</strong></td>
                        <td><strong>¥${totalPrice.toLocaleString()}</strong></td>
                        <td></td>
                    </tr>
                </tfoot>
            </table>
        </div>
    `;
    
    return html;
}

function getInfraName(key) {
    const names = {
        'racks': '机柜',
        'pdu': 'PDU电源',
        'ups': 'UPS电源',
        'cables': '线缆'
    };
    return names[key] || key;
}

// 显示详细成本明细
function displayCostDetailed(cost) {
    const breakdown = cost.breakdown || {};
    
    let html = `
        <div class="cost-breakdown">
            <h3>💰 成本明细</h3>
            
            <!-- 硬件成本 -->
            <div class="cost-section">
                <h4>1. 硬件成本</h4>
                <table class="cost-table">
                    <tr>
                        <td>服务器</td>
                        <td class="cost-value">¥${(breakdown['硬件成本']?.servers || 0).toLocaleString()}</td>
                    </tr>
                    <tr>
                        <td>网络设备</td>
                        <td class="cost-value">¥${(breakdown['硬件成本']?.network || 0).toLocaleString()}</td>
                    </tr>
                    <tr>
                        <td>存储设备</td>
                        <td class="cost-value">¥${(breakdown['硬件成本']?.storage || 0).toLocaleString()}</td>
                    </tr>
                    <tr>
                        <td>基础设施</td>
                        <td class="cost-value">¥${(breakdown['硬件成本']?.infrastructure || 0).toLocaleString()}</td>
                    </tr>
                    <tr class="subtotal">
                        <td><strong>硬件小计</strong></td>
                        <td class="cost-value"><strong>¥${(breakdown['硬件成本']?.subtotal || 0).toLocaleString()}</strong></td>
                    </tr>
                </table>
            </div>
            
            <!-- 软件成本 -->
            <div class="cost-section">
                <h4>2. 软件成本</h4>
                <table class="cost-table">
                    <tr>
                        <td>软件许可证</td>
                        <td class="cost-value">¥${(breakdown['软件成本']?.licenses || 0).toLocaleString()}</td>
                    </tr>
                    <tr class="subtotal">
                        <td><strong>软件小计</strong></td>
                        <td class="cost-value"><strong>¥${(breakdown['软件成本']?.subtotal || 0).toLocaleString()}</strong></td>
                    </tr>
                </table>
            </div>
            
            <!-- 实施成本 -->
            <div class="cost-section">
                <h4>3. 实施成本</h4>
                <table class="cost-table">
                    <tr>
                        <td>部署实施</td>
                        <td class="cost-value">¥${(breakdown['实施成本']?.deployment || 0).toLocaleString()}</td>
                    </tr>
                    <tr>
                        <td>培训费用</td>
                        <td class="cost-value">¥${(breakdown['实施成本']?.training || 0).toLocaleString()}</td>
                    </tr>
                    <tr class="subtotal">
                        <td><strong>实施小计</strong></td>
                        <td class="cost-value"><strong>¥${(breakdown['实施成本']?.subtotal || 0).toLocaleString()}</strong></td>
                    </tr>
                </table>
            </div>
            
            <!-- 年度运维成本 -->
            <div class="cost-section">
                <h4>4. 年度运维成本</h4>
                <table class="cost-table">
                    <tr>
                        <td>软件维保</td>
                        <td class="cost-value">¥${(breakdown['年度运维成本']?.software_maintenance || 0).toLocaleString()}</td>
                    </tr>
                    <tr>
                        <td>电费</td>
                        <td class="cost-value">¥${(breakdown['年度运维成本']?.power || 0).toLocaleString()}</td>
                    </tr>
                    <tr>
                        <td>制冷费用</td>
                        <td class="cost-value">¥${(breakdown['年度运维成本']?.cooling || 0).toLocaleString()}</td>
                    </tr>
                    <tr>
                        <td>人员成本</td>
                        <td class="cost-value">¥${(breakdown['年度运维成本']?.personnel || 0).toLocaleString()}</td>
                    </tr>
                    <tr class="subtotal">
                        <td><strong>运维小计</strong></td>
                        <td class="cost-value"><strong>¥${(breakdown['年度运维成本']?.subtotal || 0).toLocaleString()}</strong></td>
                    </tr>
                </table>
            </div>
            
            <!-- 总成本 -->
            <div class="cost-section total-cost">
                <h4>💎 总成本汇总</h4>
                <table class="cost-table">
                    <tr>
                        <td>硬件成本</td>
                        <td class="cost-value">¥${(cost.total?.hardware || 0).toLocaleString()}</td>
                    </tr>
                    <tr>
                        <td>软件成本</td>
                        <td class="cost-value">¥${(cost.total?.software || 0).toLocaleString()}</td>
                    </tr>
                    <tr>
                        <td>实施成本</td>
                        <td class="cost-value">¥${(cost.total?.deployment || 0).toLocaleString()}</td>
                    </tr>
                    <tr>
                        <td>首年运维成本</td>
                        <td class="cost-value">¥${(cost.total?.first_year_operation || 0).toLocaleString()}</td>
                    </tr>
                    <tr class="grand-total">
                        <td><strong>首年总成本</strong></td>
                        <td class="cost-value"><strong>¥${(cost.total?.total_first_year || 0).toLocaleString()}</strong></td>
                    </tr>
                    <tr>
                        <td>后续年度运维成本</td>
                        <td class="cost-value">¥${(cost.total?.annual_operation || 0).toLocaleString()}/年</td>
                    </tr>
                </table>
            </div>
        </div>
    `;
    
    return html;
}

// 添加样式
const style = document.createElement('style');
style.textContent = `
    .detailed-table-container {
        overflow-x: auto;
        margin: 20px 0;
    }
    
    .detailed-table {
        width: 100%;
        border-collapse: collapse;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .detailed-table th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px;
        text-align: left;
        font-weight: 600;
    }
    
    .detailed-table td {
        padding: 10px 12px;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .detailed-table tbody tr:hover {
        background: #f5f5f5;
    }
    
    .detailed-table .total-row {
        background: #f0f0f0;
        font-weight: bold;
    }
    
    .cost-breakdown {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .cost-section {
        margin: 20px 0;
        padding: 15px;
        background: #f9f9f9;
        border-radius: 8px;
    }
    
    .cost-section h4 {
        margin: 0 0 15px 0;
        color: #667eea;
    }
    
    .cost-table {
        width: 100%;
        border-collapse: collapse;
    }
    
    .cost-table td {
        padding: 8px 12px;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .cost-table .cost-value {
        text-align: right;
        font-weight: 500;
    }
    
    .cost-table .subtotal td {
        background: #e8e8e8;
        font-weight: bold;
        padding: 10px 12px;
    }
    
    .total-cost {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border: 2px solid #667eea;
    }
    
    .grand-total td {
        background: #667eea;
        color: white;
        font-size: 1.1em;
        padding: 12px;
    }
`;
document.head.appendChild(style);
