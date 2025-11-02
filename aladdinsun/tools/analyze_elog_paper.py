#!/usr/bin/env python3
"""
E-Log论文分析和提取脚本
提取论文中的关键信息，特别是实验设置部分
"""

import PyPDF2
import re
import json

def extract_pdf_text(pdf_path):
    """提取PDF文本内容"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            print(f"总页数: {len(pdf_reader.pages)}")
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += f"\n\n=== 第 {page_num + 1} 页 ===\n\n"
                text += page.extract_text()
    except Exception as e:
        print(f"提取PDF时出错: {e}")
        return None
    
    return text

def analyze_elog_paper(text):
    """分析E-Log论文内容"""
    
    analysis = {
        "title": "",
        "abstract": "",
        "key_concepts": [],
        "experiment_setup": {},
        "iotdb_tsbs_experiment": {},
        "threshold_settings": [],
        "metrics": []
    }
    
    # 提取标题
    title_match = re.search(r'E-Log[:\s]*([^\n]+)', text[:500])
    if title_match:
        analysis["title"] = title_match.group(0)
    
    # 查找实验相关部分
    experiment_keywords = [
        "IoTDB", "TSBS", "threshold", "uncertainty",
        "log volume", "throughput", "accuracy",
        "experiment", "evaluation", "dataset"
    ]
    
    # 分段分析
    sections = text.split('\n\n')
    
    for i, section in enumerate(sections):
        section_lower = section.lower()
        
        # 查找IoTDB和TSBS相关实验
        if 'iotdb' in section_lower and 'tsbs' in section_lower:
            analysis["iotdb_tsbs_experiment"]["section"] = section
            analysis["iotdb_tsbs_experiment"]["position"] = i
        
        # 查找阈值设置
        if 'threshold' in section_lower:
            analysis["threshold_settings"].append({
                "position": i,
                "content": section[:500]  # 只保存前500字符
            })
        
        # 查找评估指标
        if any(metric in section_lower for metric in ['accuracy', 'throughput', 'volume', 'f1-score']):
            if len(section) < 1000:  # 避免保存过长的段落
                analysis["metrics"].append({
                    "position": i,
                    "content": section
                })
    
    return analysis

def main():
    pdf_path = "/Users/aladdin/Documents/gitdata/tencent_CodeBuddy/aladdinsun/tools/pdfs/E-Log_Fine-Grained_Elastic_Log-Based_Anomaly_Detection_and_Diagnosis_for_Databases.pdf"
    
    print("正在提取PDF内容...")
    text = extract_pdf_text(pdf_path)
    
    if text:
        # 保存完整文本
        with open("elog_paper_full_text.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print("完整文本已保存到 elog_paper_full_text.txt")
        
        # 分析论文
        print("\n正在分析论文内容...")
        analysis = analyze_elog_paper(text)
        
        # 保存分析结果
        with open("elog_paper_analysis.json", "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        print("分析结果已保存到 elog_paper_analysis.json")
        
        # 打印关键信息
        print("\n=== 关键信息摘要 ===")
        print(f"标题: {analysis['title']}")
        print(f"\n找到 {len(analysis['threshold_settings'])} 处阈值相关内容")
        print(f"找到 {len(analysis['metrics'])} 处评估指标相关内容")
        
        if analysis['iotdb_tsbs_experiment']:
            print("\n=== IoTDB + TSBS 实验部分 ===")
            print(analysis['iotdb_tsbs_experiment'].get('section', '未找到')[:1000])

if __name__ == "__main__":
    main()
