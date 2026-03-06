<p align="center">
  <img src="https://img.shields.io/badge/Smart%20Document-Insights-6366F1?style=for-the-badge&logo=googledrive&logoColor=white" alt="Smart Document Insights Logo" />
</p>

<h1 align="center">📄 Smart Document Insights // AI-Powered Q&A</h1>
<h3 align="center">Advanced PDF Analysis Console & Context-Aware Retrieval Platform</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.14+-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Groq-Inference-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/Model-Llama%203.3%2070B-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" />
</p>

<p align="center">
  <b>Uncover the Truth in Documents.</b><br/>
  Upload any PDF → Get real-time AI-driven answers, page-wise context retrieval, and full transparency with source page visualization.
</p>

---

## 📸 Screenshots

| Dashboard | AI Chat Interface | Source Transparency |
|:---:|:---:|:---:|
| Document Upload & Metrics | Streamed Intelligent Answers | Context-Aware Source Pages |

---

## ✨ Features

### 🎯 Core Intelligence
- **Context-Aware Retrieval** — Uses BM25Okapi to index and retrieve the most relevant pages per query without complex vector databases.
- **Accurate AI Generation** — Leverages Llama 3.3 70B (via Groq) to generate precise answers based strictly on provided context.
- **Source Transparency** — Every answer is backed by verified page numbers shown in an expandable UI section.

### 🔬 Deep Analysis
- **Page-wise Parsing** — Robust text extraction from PDFs using `pdfplumber`, treating every page as a distinct unit of context.
- **BM25Okapi Scoring** — Statistical keyword-based ranking ensures high precision for technical and factual queries.
- **Multi-Turn Conversation** — Intuitive chat interface that maintains session history for seamless interaction.

### 🚀 Workflow
- **Instant Indexing** — Fast document processing (under 3s for 100 pages) designed for a "zero-wait" experience.
- **Real-Time Streaming** — Answers are streamed token-by-token using Groq's high-speed LPU inference engine.
- **Secure Handling** — Local environment management via `python-dotenv` and secure deployment on Streamlit Cloud.

### 🖥️ Premium UI
- **Modern Streamlit Interface** — Sleek, responsive design with wide layout and persistent sidebar controls.
- **Dynamic Feedback** — Live metrics for page counts and document status updates.
- **Zero Configuration** — Pre-configured for immediate use with a valid Groq API key.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Streamlit Frontend                    │
│                 (app.py — Main UI)                      │
└─────────────────────┬───────────────────────────────────┘
                      │ st.session_state Interaction
┌─────────────────────▼───────────────────────────────────┐
│                    Parsing Engine                       │
│              (utils/parser.py — pdfplumber)             │
├─────────────────────────────────────────────────────────┤
│                    Retrieval Layer                      │
│            (utils/retriever.py — BM25Okapi)             │
├─────────────────────────────────────────────────────────┤
│                    Generation Pipe                      │
│           (utils/generator.py — Groq API)               │
├─────────────────────┬───────────────────────────────────┤
│         Model       │           Model Result            │
│  ┌──────────────┐   │    ┌───────────────────────────┐  │
│  │ Llama 3.3    │   │    │  Streamed Text Response   │  │
│  └──────────────┘   │    └───────────────────────────┘  │
└─────────────────────┴───────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend UI** | Streamlit |
| **PDF Parsing** | pdfplumber |
| **Retrieval Engine** | rank_bm25 (BM25Okapi) |
| **LLM Inference** | Groq Cloud (LPU Engine) |
| **Model** | Llama 3.3 70B (llama-3.3-70b-versatile) |
| **Env Management** | python-dotenv |

---

## 📁 Project Structure

```
smart-document-insights/
├── app.py                    # Main Application UI & Logic
├── .env                      # API Configuration (Excluded from Git)
├── .gitignore                # Version Control Specs
├── requirements.txt          # Project Dependencies
│
├── utils/
│   ├── parser.py             # PDF Processing & Text Extraction
│   ├── retriever.py          # BM25 Indexing & Search Logic
│   ├── generator.py          # Groq LLM API Wrapper
│   └── __init__.py           # Utility Package Init
│
└── venv/                      # Local Virtual Environment
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **Groq API Key** (Obtain at [console.groq.com](https://console.groq.com))

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Humble-Librarian/Smart-Document-Insights.git
cd Smart-Document-Insights

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Setup Environment
# Create a .env file and add your key:
# GROQ_API_KEY=your_key_here
```

### Running the Application

```bash
streamlit run app.py
```

---

## 📖 How It Works

```
PDF Upload (.pdf)
    │
    ▼
Text Extraction ──► Page-wise Structuring (PageIndex)
    │
    ▼
BM25Okapi Indexing (Page Corpus)
    │
    ▼
User Query Input
    │
    ├──► Tokenization & Retrieval (Find Top 3 Pages)
    └──► Context Fusion (Labelled Context Block)
            │
            ▼
    Llama 3.3 70B Inference (via Groq)
            │
            ├──► Token Stream to UI
            └──► Source Page Presentation
```

---

## ⚙️ Configuration

Key settings modified in `utils/generator.py`:

```python
MODEL_ID    = "llama-3.3-70b-versatile"
MAX_TOKENS  = 512
TEMPERATURE = 0.2      # Low for factual consistency
TOP_N_PAGES = 3        # Context window size
```

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/insight-engine`)
3. Commit your changes (`git commit -m 'Enhance Retrieval Logic'`)
4. Push to the branch (`git push origin feature/insight-engine`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built with ❤️ using Python, Streamlit & Groq<br/>
  <b>Smart Document Insights</b> — Uncover the Truth in Documents.
</p>
