# PDF 分析报告

目录: /Users/aladdin/Documents/理工大/论文学习/20251026

共计 5 篇

## 1150 IEEE TRANSACTIONS ON DEPENDABLE AND SECURE COMPUTING, VOL. 22, NO. 2, MARCH/APRIL 2025
- 文件: Log_Sequence_Anomaly_Detection_Based_on_Template_and_Parameter_Parsing_via_BERT.pdf
- 路径: /Users/aladdin/Documents/理工大/论文学习/20251026/Log_Sequence_Anomaly_Detection_Based_on_Template_and_Parameter_Parsing_via_BERT.pdf
- 作者: 1150 IEEE TRANSACTIONS ON DEPENDABLE AND SECURE COMPUTING, VOL. 22, NO. 2, MARCH/APRIL 2025
- 期刊/会议: IEEE Transactions on Dependable And Secure Computing
- 年份: 2025

### 摘要
Abstract —Logs record various operations and events during system running in text format, which is an essential basis for de- tecting and identifying potential security threats or system failures, and is widely used in system management to ensure security and reliability. Existing log sequence anomaly detection is limited by log parsing and does not consider all key features of logs, which may cause false or missed detection. In this article, we propose a fast and accurate log parsing

### 方法/框架（节选）
method and feed the entire log content into the deep learning network for analysis. To avoid semantic loss during parsing, we replace some variables with tokens containing seman- tic information and divide logs with appropriate granularity. To ensure the speed and accuracy of parsing, we propose a similarity- based fast merging method to deal with redundant templates. For anomaly detection, we use the complete log content features as input to the model. We use Bidirectional Encoder Representation from Transformers (BERT) to output anomaly detection

### 实验/结果（节选）
results directly after considering both the global and local information of log sequences. Experiments show that our log parsing method achieves the best average parsing quality on 16 datasets, and the anomaly detection method achieves optimal results on different datasets. Index Terms —Anomaly detection, BERT, log parsing, log sequence, system reliability. I. I NTRODUCTION LOGS are generally semi-structured text printed by log statements, which are widely used to record the running status of a system. By analyzing log information, we can help the developers and operation and maintenance engineers quickly locate system anomalies and errors to maintain system stability, which is a key step in building a secure and reliable system. As the scale and complexity of the system and software increase, the amount of logs increases rapidly (e.g., 50 GB/h) [1].I nv i e w of the rapid development of deep learning in the ﬁeld of natural language processing, the researchers use its powerful feature extraction capabilities for log anomaly detection [2],[3],[4]. Manuscript received 28 July 2023; revised 8 May 2024; accepted 8 July 2024. Date of publication 16 July 2024; date of current version 14 

---

## 1876 IEEE TRANSACTIONS ON DEPENDABLE AND SECURE COMPUTING, VOL. 21, NO. 4, JULY/AUGUST 2024
- 文件: LogGraph_Log_Event_Graph_Learning_Aided_Robust_Fine-Grained_Anomaly_Diagnosis.pdf
- 路径: /Users/aladdin/Documents/理工大/论文学习/20251026/LogGraph_Log_Event_Graph_Learning_Aided_Robust_Fine-Grained_Anomaly_Diagnosis.pdf
- 作者: 1876 IEEE TRANSACTIONS ON DEPENDABLE AND SECURE COMPUTING, VOL. 21, NO. 4, JULY/AUGUST 2024
- 期刊/会议: IEEE Transactions on Dependable And Secure Computing
- 年份: 2024

### 摘要
Abstract —Anomaly diagnosis relying on system logs to record runtime events is essential for improving the service quality of distributed systems and reducing economic losses. However, most existing log-based anomaly detection

### 引言（节选）
INTRODUCTION TODAY’S software-intensive systems, such as e-commerce, online payment services, and cloud computing systems, generally have large-scale and complicated logic functions, con- sisting of thousands of software components and serve millions of concurrent users [1]. This situation makes such systems more prone to errors. A trivial system anomaly may degrade the Manuscript received 13 April 2022; revised 26 February 2023; accepted 29 June 2023. Date of publication 7 July 2023; date of current version 11 July 2024. This work was supported by the Key Science and Technology Project of Anhui under Grant 202103a05020006, in part by the National Natural Science Foundations of China under Grants 62341113, 62101525, 62201543, and in part by the Fundamental Research Funds for the Central Universities Grant WK2100000015. (Corresponding author: Shuangwu Chen.) The authors are with the University of Science and Technology of China, Hefei, Anhui 230027, China, and also with the Institute of Artiﬁcial In- telligence, Hefei Comprehensive National Science Center, Hefei, Anhui 230026, China (e-mail: ljm0826@mail.ustc.edu.cn; hehuasen@ustc.edu.cn; chensw@ustc.edu.cn; kingdon@mail.ustc.edu.cn

### 方法/框架（节选）
approaches depend on the assumption of the ﬁxed quantitative or sequential patterns of a normal log event sequence. This assumption is challenged in the context of practical distributed and parallel systems due to the dynamic pattern of the log sequence, log data noise as well as concurrency of multiple anomalies. Against these challenges, this paper aims to perform the robust log-based anomaly diagnosis by capturing the event context information of the log event graph, called LogGraph, instead of straightforwardly employing the ﬁxed quantitative or sequential patterns of the log records, thus reducing its sensitivity to the log ﬂaws and the concurrency of multiple anomalies. Speciﬁcally, in order to handle multiple anomalies con- currency, LogGraph invokes the association rule to decouple log sequences. It further reinterprets a log record sequence into a log event graph modeled by event semantic embedding and event ad- jacency matrix. An attention-based Gated Graph Neural Network (GGNN) model is developed to capture the semantic information of the log graph, which enables the ﬁne-grained and robust anomaly identiﬁcation of the proposed scheme. We use real log data sets collected 

### 实验/结果（节选）
results show that the proposed LogGraph achieves high performance and strong robustness in anomaly diagnosis. Index Terms —Anomaly detection, graph neural network, log data analysis. I. INTRODUCTION TODAY’S software-intensive systems, such as e-commerce, online payment services, and cloud computing systems, generally have large-scale and complicated logic functions, con- sisting of thousands of software components and serve millions of concurrent users [1]. This situation makes such systems more prone to errors. A trivial system anomaly may degrade the Manuscript received 13 April 2022; revised 26 February 2023; accepted 29 June 2023. Date of publication 7 July 2023; date of current version 11 July 2024. This work was supported by the Key Science and Technology Project of Anhui under Grant 202103a05020006, in part by the National Natural Science Foundations of China under Grants 62341113, 62101525, 62201543, and in part by the Fundamental Research Funds for the Central Universities Grant WK2100000015. (Corresponding author: Shuangwu Chen.) The authors are with the University of Science and Technology of China, Hefei, Anhui 230027, China, and also with the Institute of Artiﬁcial In-

### 结论（节选）
conclusion is drawn in Section VI. II. R ELATED WORKS In recent years, many log-based anomaly detection methods have been proposed, which can be divided into three categories: log event based anomaly detection, log count vector based anomaly detection, and log sequence based anomaly detection. A. Log Event Based Anomaly Detection The anomaly detection methods based on log event focus on the anomaly of a single log through keyword matching, regular expression matching, or semantic sentiment analysis. Cinque et al. [5]proposed a rule-based log anomaly detec- tion method, which builds a rule base by manually extracting logs related to service errors or service complaints. Oprea et al.[6]detected early attack problems from DNS logs based on belief propagation, which is only applicable to speciﬁc attack scenarios. These two methods relying on keywords or regular expressions matching require a lot of professional knowledge, which make them too difﬁcult to implement. To overcome this obstacle, some literature used machine learning methods to detect log anomalies. Henriques et al. [19] used K-means to classify anomalous and normal events and then used XGBoost to generate interpretable rule

---

## 2808 IEEE TRANSACTIONS ON SERVICES COMPUTING, VOL. 18, NO. 5, SEPTEMBER/OCTOBER 2025
- 文件: E-Log_Fine-Grained_Elastic_Log-Based_Anomaly_Detection_and_Diagnosis_for_Databases.pdf
- 路径: /Users/aladdin/Documents/理工大/论文学习/20251026/E-Log_Fine-Grained_Elastic_Log-Based_Anomaly_Detection_and_Diagnosis_for_Databases.pdf
- 作者: 2808 IEEE TRANSACTIONS ON SERVICES COMPUTING, VOL. 18, NO. 5, SEPTEMBER/OCTOBER 2025
- 期刊/会议: IEEE Transactions on Services Computing
- 年份: 2025

### 摘要
Abstract —Database Management Systems (DBMS) form the backbone of modern large-scale software systems, where reliableanomaly detection and diagnosis are essential for ensuring systemavailability. However, existing log-based

### 引言（节选）
INTRODUCTION DATABASE management system (DBMS), such as Alibaba OceanBase [1], RocksDB [2], PingCAP TiDB [3], and Apache IoTDB [4], play a crucial role in modern software systems. They serve as foundational infrastructure to meet the demands of extremely high-volume data storage [5],[6]. Despite their widespread adoption, existing databases en- counter recurring anomalies including system failures and Received 24 May 2024; revised 6 July 2025; accepted 26 July 2025. Date of publication 1 August 2025; date of current version 9 October 2025. This workwas supported by the National Key Research and Development Plan under Grant 2021YFF0704202. (Corresponding authors: Tong Jia; Ying Li.) Lingzhe Zhang, Tong Jia, Mengxi Jia, Hongyi Liu, Zhonghai Wu, and Ying Li are with Peking University, Beijing 100871, China (e-mail: zhang.lingzhe@stu.pku.edu.cn; jia.tong@pku.edu.cn; mxjia@pku.edu.cn; hongyiliu@pku.edu.cn; wuzh@pku.edu.cn; li.ying@pku.edu.cn). Xinyu Tan is with Timecho Ltd., Beijing 100192, China (e-mail: xinyu.tan@ timecho.com). Xiangdong Huang is with Tsinghua University, Beijing 100084, China (e- mail: huangxdong@tsinghua.edu.cn). This article has supplementary downloadable material 

### 方法/框架（节选）
methods often impose sig-niﬁcant performance overhead by collecting large volumes of logs,which is impractical for DBMS requiring high read/write through-put. This paper addresses a critical yet underexplored challenge:how to balance logging granularity with runtime efﬁciency foreffective anomaly management in databases. We present E-Log,a novel ﬁne-grained elastic log-based framework for anomaly de-tection and diagnosis. E-Log intelligently adjusts the amount anddetail of logging based on system state—maintaining lightweightlogging during normal operation for efﬁcient anomaly detection,and triggering rich, informative logging only upon anomaly sus-picion for accurate diagnosis. This adaptive strategy signiﬁcantlyreduces runtime overhead while preserving diagnostic precision.We implement E-Log on Apache IoTDB and evaluate it usingbenchmarks including TSBS, TPCx-IoT, and IoT-Bench. Exper-imental

### 实验/结果（节选）
results show that E-Log improves anomaly detection accu-racy by 3.15% and diagnosis performance by 9.32% compared tostate-of-the-art methods. Moreover, it reduces log storage size by43.53% and increases average write throughput by 26.22%. Theseresults highlight E-Log’s potential to enable efﬁcient, accurate,and scalable anomaly management in high-performance database systems. Index Terms —Anomaly detection, anomaly diagnosis, database, elastic log. I. INTRODUCTION DATABASE management system (DBMS), such as Alibaba OceanBase [1], RocksDB [2], PingCAP TiDB [3], and Apache IoTDB [4], play a crucial role in modern software systems. They serve as foundational infrastructure to meet the demands of extremely high-volume data storage [5],[6]. Despite their widespread adoption, existing databases en- counter recurring anomalies including system failures and Received 24 May 2024; revised 6 July 2025; accepted 26 July 2025. Date of publication 1 August 2025; date of current version 9 October 2025. This workwas supported by the National Key Research and Development Plan under Grant 2021YFF0704202. (Corresponding authors: Tong Jia; Ying Li.) Lingzhe Zhang, Tong Jia, Mengxi Jia, Hongyi Liu, Zhon

---

## IEEE TRANSACTIONS ON SERVICES COMPUTING, VOL. 16, NO. 5, SEPTEMBER/OCTOBER 2023 3537
- 文件: MLog_Mogrifier_LSTM-Based_Log_Anomaly_Detection_Approach_Using_Semantic_Representation.pdf
- 路径: /Users/aladdin/Documents/理工大/论文学习/20251026/MLog_Mogrifier_LSTM-Based_Log_Anomaly_Detection_Approach_Using_Semantic_Representation.pdf
- 作者: IEEE TRANSACTIONS ON SERVICES COMPUTING, VOL. 16, NO. 5, SEPTEMBER/OCTOBER 2023 3537
- 期刊/会议: IEEE Transactions on Services Computing
- 年份: 2023

### 摘要
Abstract — Streaming logs provide valuable information for com- plex systems in diagnosing system faults or conducting security analysis. Although the log sequence anomaly detection has drawn more and more attention and achieved a satisfactory performance, it remains an extremely difﬁcult task because of several intrin- sic challenges including new event occurrences in a continuously evolving environment, making full use of rich dependency hidden in sequential events from the global and local view. To meet these challenges, in this article, we propose MLog, a hybrid deep neural network for detecting anomalies in log sequences. Speciﬁcally, MLog leverages the transformer encoder and a novel event In- verse Document Frequency (IDF) weighted mechanism to obtain a semantic vector for an individual log template. Log sequences represented by sequential template semantic vectors are then fed into a deep neural network combing the Mogriﬁer Long Short Term Memory (LSTM) with Convolutional Neural Network (CNN) to capture global and local sequential patterns simultaneously. We implement MLog and evaluate it by conducting extensive experi- ments on two well-known benchmark datasets, HDFS and BGL, from the aspects of detection accuracy and robustness. The

### 引言（节选）
INTRODUCTION AS AN important system runtime output, log records very useful information about system activities and states, hence plays an extremely critical role in complex system mainte- nance. However, as the scale and complexity of modern software systems increase, the possibility that they are subject to system incidents is also getting higher, which leads to rapidly generate more system logs than before. As a

### 方法/框架（节选）
Approach Using Semantic Representation Yuanyuan Fu , Kun Liang, and Jian Xu Abstract — Streaming logs provide valuable information for com- plex systems in diagnosing system faults or conducting security analysis. Although the log sequence anomaly detection has drawn more and more attention and achieved a satisfactory performance, it remains an extremely difﬁcult task because of several intrin- sic challenges including new event occurrences in a continuously evolving environment, making full use of rich dependency hidden in sequential events from the global and local view. To meet these challenges, in this article, we propose MLog, a hybrid deep neural network for detecting anomalies in log sequences. Speciﬁcally, MLog leverages the transformer encoder and a novel event In- verse Document Frequency (IDF) weighted mechanism to obtain a semantic vector for an individual log template. Log sequences represented by sequential template semantic vectors are then fed into a deep neural network combing the Mogriﬁer Long Short Term Memory (LSTM) with Convolutional Neural Network (CNN) to capture global and local sequential patterns simultaneously. We implement MLog and evaluate it by conduct

### 实验/结果（节选）
results show that MLog outperforms the state-of-the-art approaches and is robust to the evolving logs. To encourage reproducibility, we make the implementation of MLog available. Index Terms —Deep learning, log parsing, semantic vector, anomaly detection, mogriﬁer LSTM. I. INTRODUCTION AS AN important system runtime output, log records very useful information about system activities and states, hence plays an extremely critical role in complex system mainte- nance. However, as the scale and complexity of modern software systems increase, the possibility that they are subject to system incidents is also getting higher, which leads to rapidly generate more system logs than before. As a result, the huge scale of system logs and the rapid log generation have imposed a big challenge on system operational and maintenance experts to dis- cover system anomalies from log ﬁles and ﬁx them in time. Log analysis depending on manual efforts becomes an error-prone and cost-intensive task. Therefore, automatic log analysis for the purpose of detection anomalous system behaviors from the Manuscript received 21 April 2022; revised 21 June 2023; accepted 22 June 2023. Date of publication 26 June 202

---

## SwissLog: Robust Anomaly Detection and
- 文件: SwissLog_Robust_Anomaly_Detection_and_Localization_for_Interleaved_Unstructured_Logs.pdf
- 路径: /Users/aladdin/Documents/理工大/论文学习/20251026/SwissLog_Robust_Anomaly_Detection_and_Localization_for_Interleaved_Unstructured_Logs.pdf
- 作者: Xiaoyun Li , Pengfei Chen , Linxiao Jing, Zilong He , and Guangba Yu
- 期刊/会议: IEEE Transactions on Dependable And Secure Computing
- 年份: 2021

### 摘要
Abstract— Modern distributed systems generate interleaved logs when running in parallel. Identiﬁers (ID) are always attached to them to trace running instances or entities in logs. Therefore, log messages can be grouped by the same IDs to help anomaly detection and localization. The existing

### 方法/框架（节选）
approaches to achieve this still fall short meeting these challenges: 1) Log is solely processed in single components without mining log dependencies. 2) Log formats are continually changing in modern software systems. 3) It is challenging to detect latent performance issues non-intrusively by trivial monitoring tools. To remedy the above shortcomings, we propose SwissLog, a robust anomaly detection and localization tool for interleaved unstructured logs. SwissLog focuses on log sequential anomalies and tries to dig out possible performance issues. SwissLog constructs ID relation graphs across distributed components and groups log messages by IDs. Moreover, we propose an online data-driven log parser without parameter tuning. The grouped log messages are parsed via the novel log parser and transformed with semantic and temporal embedding. Finally, SwissLog utilizes an attention-based Bi-LSTM model and a heuristic searching algorithm to detect and localize anomalies in instance-granularity, respectively . The experiments on real-world and synthetic datasets conﬁrm the effectiveness, efﬁciency, and robustness of SwissLog. Index Terms— Deep learning, log parsing, anomaly detection, an

### 实验/结果（节选）
results prove the effectiveness and robustness of SwissLog. The source code of SwissLog1has also been released for repro- ducible research. Extended from its preliminary conference version [1], this paper makes several major enhancements including the application of inter-component log correlation, IDs relation construction for unstructured interleaved logs in the distrib- uted system, the heuristic-based anomaly localization in instance-level, the design and implementation of a novel online log parsing method, the advanced time embedding, new experimental comparison on latest log parser both in effectiveness and efﬁciency, a new real-world dataset to conﬁrm the effectiveness of SwissLog, and code release of SwissLog for reproducible research. 2M OTIVATION 2.1 Relation Between Identiﬁer Pairs Each ID identiﬁes an abstracted concept or a concrete resource instance, thus certain relationships (e.g., subordi- nate, dependent) between IDs during system execution. The log printer usually outputs these IDs in corresponding log messages. So with these IDs, we can reconstruct the inter- component interactions from logs. We can introduce a workﬂow construction method to proﬁle the distribut

---

