<div align="center">

# LangChain ReAct Agent · 智能服装客服

**基于 LangChain + ReAct 范式 + RAG 检索增强的智能服装客服系统，参考优衣库风格**

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
&nbsp;
[![LangChain](https://img.shields.io/badge/LangChain-0.3-green)](https://www.langchain.com/)
&nbsp;
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2-orange)](https://github.com/langchain-ai/langgraph)
&nbsp;
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40-red)](https://streamlit.io/)
&nbsp;
[![License](https://img.shields.io/badge/License-MIT-yellow)](./LICENSE)

</div>

---

## 项目简介

基于 LangChain 框架实现的 **ReAct（Reasoning + Acting）Agent**，集成 RAG 检索增强、多工具调用和动态提示词切换。系统能根据用户意图自动判断任务类型（知识问答 / 购买报告生成），调用合适的工具和知识库完成推理，并通过 Streamlit 流式界面实时展示 Agent 的思考与执行过程。

## 效果展示

<div align="center">

<img src="assets/img.png" alt="对话界面" width="85%">

*智能服装客服对话界面*

&nbsp;

</div>

## 技术架构

```
用户输入 (Streamlit)
      │
      ▼
┌─────────────────────────────────────┐
│           ReAct Agent               │
│                                     │
│  ┌──────────┐    ┌─────────────┐   │
│  │ Thought  │───→│   Action    │   │
│  │ (推理)    │    │ (工具/RAG)  │   │
│  └──────────┘    └──────┬──────┘   │
│       ↑                 │          │
│       └─── Observation ←┘          │
│                                     │
│  Middleware: 工具监控 · 动态提示词切换│
└──────────────┬──────────────────────┘
               │
      ┌────────┼────────┐
      ▼        ▼        ▼
┌──────┐ ┌──────┐ ┌──────────┐
│ RAG  │ │ Tools│ │  Prompt  │
│Chroma│ │天气/ │ │ 动态切换  │
│向量库│ │用户/ │ │ 模板管理  │
│      │ │报告  │ │          │
└──────┘ └──────┘ └──────────┘
```

### 核心特性

| 特性 | 说明 |
|---|---|
| **ReAct 范式** | Thought → Action → Observation 循环，Agent 自主推理并决定调用哪个工具 |
| **RAG 检索增强** | Chroma 向量库 + DashScope Embedding，MD5 文件去重，支持 txt/pdf 混合加载 |
| **多工具调用** | 知识库检索 / 天气查询 / 用户定位 / 购买记录查询 / 报告上下文填充，Agent 按需自动选择 |
| **动态提示词切换** | Middleware 根据运行时上下文自动切换「普通问答」与「报告生成」两套 System Prompt |
| **流式对话界面** | Streamlit 构建，支持流式逐字输出、历史消息留存、Agent 推理过程可见 |

### 知识库内容

| 文档 | 内容 |
|---|---|
| `服装产品百科.txt` | 优衣库主要系列介绍（UT、AIRism、HEATTECH、羽绒服、牛仔裤等） |
| `尺码指南.txt` | 各品类尺码对照、测量方法、选码建议 |
| `面料与洗护.txt` | 常见面料特性、洗涤保养说明、洗涤符号解读 |
| `退换货政策.txt` | 退换货条件、流程、时限、特殊说明 |
| `穿搭推荐.txt` | 四季穿搭建议、场景搭配、色彩基础 |
| `常见问题100问.txt` | 高频问答汇总（尺码、面料、洗护、购买、搭配） |

### 技术栈

| 类别 | 技术 |
|---|---|
| LLM | 通义千问 qwen3-max（DashScope / ChatTongyi） |
| Agent 框架 | LangChain + LangGraph |
| 向量数据库 | Chroma |
| 文档处理 | PyPDF + RecursiveCharacterTextSplitter |
| 前端 | Streamlit |
| 配置 | YAML 驱动（Agent / RAG / Chroma / Prompts） |

## 快速开始

### 环境要求

- **Python** ≥ 3.10
- **DashScope API Key**（[阿里云百炼](https://bailian.console.aliyun.com/) 申请）

### 1. 克隆仓库

```bash
git clone https://github.com/lhh737/LangChain-ReAct-Agent.git
cd LangChain-ReAct-Agent
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API Key

参考 `.env.example`，设置阿里云百炼 API Key：

```bash
# Linux / macOS
export DASHSCOPE_API_KEY="your-api-key"

# Windows (CMD)
set DASHSCOPE_API_KEY=your-api-key
```

> 申请地址：[阿里云百炼控制台](https://bailian.console.aliyun.com/)

### 4. 初始化知识库（首次运行）

```bash
python -c "from rag.vector_store import VectorStoreService; VectorStoreService().load_document()"
```

### 5. 启动应用

```bash
streamlit run app.py
```

浏览器自动打开 http://localhost:8501

### 验证运行

启动后在聊天框输入以下测试问题：

- *UT 系列有哪些特点？怎么选尺码？*（RAG 知识库问答）
- *纯棉 T 恤洗后缩水怎么办？*（面料与洗护知识检索）
- *根据我的购买记录生成一份个性化报告*（报告生成 + 多工具调用）

## 项目结构

```
LangChain-ReAct-Agent/
├── agent/                          # Agent 核心
│   ├── react_agent.py              #   ReAct Agent 主逻辑（流式执行）
│   └── tools/
│       ├── agent_tools.py          #   工具函数（RAG检索/天气/用户/报告）
│       └── middleware.py           #   中间件（工具监控/动态提示词切换）
├── rag/                            # RAG 检索增强
│   ├── vector_store.py             #   Chroma 向量库 · 文档加载 · MD5 去重
│   └── rag_service.py              #   RAG 检索 → LLM 总结服务
├── model/
│   └── factory.py                  # 模型工厂（ChatTongyi + DashScopeEmbedding）
├── config/                         # YAML 配置文件
│   ├── agent.yml                   #   Agent 行为与工具配置
│   ├── chroma.yml                  #   向量库与检索参数
│   ├── prompts.yml                 #   提示词模板路径
│   └── rag.yml                     #   RAG 模型与参数
├── prompts/                        # 提示词模板
│   ├── main_prompt.txt             #   普通问答 System Prompt
│   ├── rag_summarize.txt           #   RAG 总结 Prompt
│   └── report_prompt.txt           #   报告生成 System Prompt
├── utils/                          # 工具函数
│   ├── config_handler.py           #   YAML 配置加载
│   ├── file_handler.py             #   文件解析（PDF/TXT）
│   ├── logger_handler.py           #   日志管理
│   ├── path_tool.py                #   路径工具
│   └── prompt_loader.py            #   提示词加载
├── data/                           # 知识库文档（服装领域）
│   └── external/
│       └── records.csv             # 用户购买记录数据
├── assets/                         # 效果展示截图
├── app.py                          # Streamlit 应用入口
├── requirements.txt
└── README.md
```

## 配置说明

项目通过 `config/` 目录下的 YAML 文件统一管理配置：

| 文件 | 说明 |
|---|---|
| `rag.yml` | 对话模型名称、Embedding 模型名称 |
| `chroma.yml` | Chroma 持久化路径、分块大小、检索 Top-K、支持的文件类型 |
| `prompts.yml` | 各场景提示词模板文件路径 |
| `agent.yml` | Agent 外部数据路径等 |

dashscope_api_key已在factory中设置 在此不方便展示

这个项目是我在别人的项目基础上利用codex进行改动和创新，不得不感叹现在ai对人类传统编程的降维打击。我很庆幸自己站在了时代的风口上，即使我对Java python只有基础的了解，但是我还是能够利用ai写出一个完整的项目

@huangmantou

