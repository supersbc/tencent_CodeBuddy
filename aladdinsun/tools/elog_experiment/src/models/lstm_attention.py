"""
LSTM + Self-Attention 模型实现
用于E-Log的异常检测和诊断
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class SelfAttention(nn.Module):
    """自注意力机制"""
    
    def __init__(self, hidden_size, num_heads=4, dropout=0.1):
        super(SelfAttention, self).__init__()
        self.hidden_size = hidden_size
        self.num_heads = num_heads
        self.head_dim = hidden_size // num_heads
        
        assert hidden_size % num_heads == 0, "hidden_size必须能被num_heads整除"
        
        self.query = nn.Linear(hidden_size, hidden_size)
        self.key = nn.Linear(hidden_size, hidden_size)
        self.value = nn.Linear(hidden_size, hidden_size)
        
        self.dropout = nn.Dropout(dropout)
        self.out = nn.Linear(hidden_size, hidden_size)
        
    def forward(self, x, mask=None):
        """
        Args:
            x: (batch_size, seq_len, hidden_size)
            mask: (batch_size, seq_len) 可选的mask
        Returns:
            output: (batch_size, seq_len, hidden_size)
            attention_weights: (batch_size, num_heads, seq_len, seq_len)
        """
        batch_size, seq_len, _ = x.size()
        
        # 计算Q, K, V
        Q = self.query(x)  # (batch_size, seq_len, hidden_size)
        K = self.key(x)
        V = self.value(x)
        
        # 重塑为多头
        Q = Q.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        K = K.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        V = V.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        # 现在形状: (batch_size, num_heads, seq_len, head_dim)
        
        # 计算注意力分数
        scores = torch.matmul(Q, K.transpose(-2, -1)) / (self.head_dim ** 0.5)
        # scores: (batch_size, num_heads, seq_len, seq_len)
        
        # 应用mask（如果有）
        if mask is not None:
            mask = mask.unsqueeze(1).unsqueeze(2)  # (batch_size, 1, 1, seq_len)
            scores = scores.masked_fill(mask == 0, -1e9)
        
        # 计算注意力权重
        attention_weights = F.softmax(scores, dim=-1)
        attention_weights = self.dropout(attention_weights)
        
        # 应用注意力权重
        context = torch.matmul(attention_weights, V)
        # context: (batch_size, num_heads, seq_len, head_dim)
        
        # 合并多头
        context = context.transpose(1, 2).contiguous().view(batch_size, seq_len, self.hidden_size)
        
        # 输出投影
        output = self.out(context)
        
        return output, attention_weights


class LSTMAttentionModel(nn.Module):
    """
    LSTM + Self-Attention 模型
    用于异常检测（二分类）或异常诊断（多分类）
    """
    
    def __init__(self, 
                 input_size,
                 hidden_size=64,
                 num_layers=2,
                 num_classes=2,
                 num_heads=4,
                 dropout=0.2,
                 bidirectional=False):
        """
        Args:
            input_size: 输入特征维度
            hidden_size: LSTM隐藏层大小
            num_layers: LSTM层数
            num_classes: 分类数量（2=检测，N=诊断）
            num_heads: 注意力头数
            dropout: Dropout比率
            bidirectional: 是否使用双向LSTM
        """
        super(LSTMAttentionModel, self).__init__()
        
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.bidirectional = bidirectional
        self.num_directions = 2 if bidirectional else 1
        
        # LSTM层
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=dropout if num_layers > 1 else 0,
            bidirectional=bidirectional,
            batch_first=True
        )
        
        # Self-Attention层
        lstm_output_size = hidden_size * self.num_directions
        self.attention = SelfAttention(
            hidden_size=lstm_output_size,
            num_heads=num_heads,
            dropout=dropout
        )
        
        # 全连接层
        self.fc = nn.Sequential(
            nn.Linear(lstm_output_size, lstm_output_size // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(lstm_output_size // 2, num_classes)
        )
        
    def forward(self, x, lengths=None):
        """
        Args:
            x: (batch_size, seq_len, input_size)
            lengths: (batch_size,) 每个序列的实际长度
        Returns:
            output: (batch_size, num_classes)
            attention_weights: (batch_size, num_heads, seq_len, seq_len)
        """
        batch_size, seq_len, _ = x.size()
        
        # LSTM前向传播
        if lengths is not None:
            # 打包序列以处理变长输入
            packed_x = nn.utils.rnn.pack_padded_sequence(
                x, lengths.cpu(), batch_first=True, enforce_sorted=False
            )
            lstm_out, (h_n, c_n) = self.lstm(packed_x)
            lstm_out, _ = nn.utils.rnn.pad_packed_sequence(
                lstm_out, batch_first=True, total_length=seq_len
            )
        else:
            lstm_out, (h_n, c_n) = self.lstm(x)
        
        # lstm_out: (batch_size, seq_len, hidden_size * num_directions)
        
        # Self-Attention
        attn_out, attention_weights = self.attention(lstm_out)
        # attn_out: (batch_size, seq_len, hidden_size * num_directions)
        
        # 使用最后一个时间步的输出
        # 如果是双向LSTM，需要合并前向和后向的最后隐藏状态
        if self.bidirectional:
            # h_n: (num_layers * 2, batch_size, hidden_size)
            h_forward = h_n[-2, :, :]
            h_backward = h_n[-1, :, :]
            final_hidden = torch.cat([h_forward, h_backward], dim=1)
        else:
            # h_n: (num_layers, batch_size, hidden_size)
            final_hidden = h_n[-1, :, :]
        
        # 或者使用注意力输出的平均
        # final_hidden = torch.mean(attn_out, dim=1)
        
        # 全连接层分类
        output = self.fc(final_hidden)
        
        return output, attention_weights


class MultiPatternLSTMAttention(nn.Module):
    """
    多模式LSTM+Attention模型
    同时处理顺序、数量和语义三种嵌入
    """
    
    def __init__(self,
                 sequential_size,
                 quantitative_size,
                 semantic_size,
                 hidden_size=64,
                 num_layers=2,
                 num_classes=2,
                 num_heads=4,
                 dropout=0.2):
        """
        Args:
            sequential_size: 顺序嵌入维度
            quantitative_size: 数量嵌入维度
            semantic_size: 语义嵌入维度
            其他参数同LSTMAttentionModel
        """
        super(MultiPatternLSTMAttention, self).__init__()
        
        # 三个独立的LSTM+Attention分支
        self.sequential_branch = LSTMAttentionModel(
            input_size=sequential_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            num_classes=hidden_size,  # 输出特征而非分类
            num_heads=num_heads,
            dropout=dropout
        )
        
        self.quantitative_branch = LSTMAttentionModel(
            input_size=quantitative_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            num_classes=hidden_size,
            num_heads=num_heads,
            dropout=dropout
        )
        
        self.semantic_branch = LSTMAttentionModel(
            input_size=semantic_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            num_classes=hidden_size,
            num_heads=num_heads,
            dropout=dropout
        )
        
        # 融合层
        self.fusion = nn.Sequential(
            nn.Linear(hidden_size * 3, hidden_size * 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size * 2, hidden_size),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size, num_classes)
        )
        
    def forward(self, sequential_x, quantitative_x, semantic_x):
        """
        Args:
            sequential_x: (batch_size, seq_len, sequential_size)
            quantitative_x: (batch_size, seq_len, quantitative_size)
            semantic_x: (batch_size, seq_len, semantic_size)
        Returns:
            output: (batch_size, num_classes)
            attention_weights: dict of attention weights from each branch
        """
        # 三个分支的前向传播
        seq_out, seq_attn = self.sequential_branch(sequential_x)
        quant_out, quant_attn = self.quantitative_branch(quantitative_x)
        sem_out, sem_attn = self.semantic_branch(semantic_x)
        
        # 拼接三个分支的输出
        combined = torch.cat([seq_out, quant_out, sem_out], dim=1)
        
        # 融合并分类
        output = self.fusion(combined)
        
        attention_weights = {
            'sequential': seq_attn,
            'quantitative': quant_attn,
            'semantic': sem_attn
        }
        
        return output, attention_weights


if __name__ == "__main__":
    # 测试代码
    print("测试LSTM+Attention模型...")
    
    # 单模式模型测试
    batch_size = 16
    seq_len = 10
    input_size = 50
    num_classes = 2
    
    model = LSTMAttentionModel(
        input_size=input_size,
        hidden_size=64,
        num_layers=2,
        num_classes=num_classes,
        num_heads=4,
        dropout=0.2
    )
    
    x = torch.randn(batch_size, seq_len, input_size)
    output, attn_weights = model(x)
    
    print(f"输入形状: {x.shape}")
    print(f"输出形状: {output.shape}")
    print(f"注意力权重形状: {attn_weights.shape}")
    
    # 多模式模型测试
    print("\n测试多模式LSTM+Attention模型...")
    
    multi_model = MultiPatternLSTMAttention(
        sequential_size=30,
        quantitative_size=20,
        semantic_size=100,
        hidden_size=64,
        num_layers=2,
        num_classes=11,  # 11种异常类型
        num_heads=4,
        dropout=0.2
    )
    
    seq_x = torch.randn(batch_size, seq_len, 30)
    quant_x = torch.randn(batch_size, seq_len, 20)
    sem_x = torch.randn(batch_size, seq_len, 100)
    
    output, attn_dict = multi_model(seq_x, quant_x, sem_x)
    
    print(f"输出形状: {output.shape}")
    print(f"注意力权重: {list(attn_dict.keys())}")
    
    print("\n模型测试完成！")
