# RAG-based AI Assistant for Central Bank of Sri Lanka

A Retrieval-Augmented Generation (RAG) AI assistant that provides accurate, context-aware responses based on official Central Bank of Sri Lanka documents including Annual Reports, Monetary Policy Reports, Financial Stability Reviews, and regulatory circulars.

## 🎯 Features

- **Intelligent Document Processing**: Automated ingestion and processing of PDF documents from the Central Bank of Sri Lanka
- **Context-Aware Responses**: RAG-based retrieval system for accurate information extraction
- **Interactive Web Interface**: User-friendly chat interface for querying financial and regulatory information
- **Multi-Source Knowledge Base**: Supports Annual Reports, Monetary Policy Reports, Financial Stability Reviews, Laws, and Circulars
- **Smart Chunking**: Advanced document chunking for optimal retrieval performance

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python
- **AI/ML**: LangChain, OpenAI, Sentence Transformers
- **Vector Databases**: Pinecone
- **Document Processing**: PyPDF, Unstructured
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Docker-ready

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key
- Pinecone API key (optional, for cloud vector storage)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/RAG-based-AI-assistant-for-Central-Bank-of-Sri-Lanka.git
   cd RAG-based-AI-assistant-for-Central-Bank-of-Sri-Lanka
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_ENVIRONMENT=your_pinecone_environment
   ```

## 📖 Usage

1. **Process Documents** (First time setup)
   ```bash
   python ingestion/smart_ingest.py
   ```

2. **Start the Application**
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Access the Interface**
   
   Open your browser and navigate to: `http://localhost:8000`

## 📁 Project Structure

```
├── app/                    # FastAPI application
│   ├── main.py            # Application entry point
│   ├── routes.py          # API routes
│   └── schemas.py         # Pydantic schemas
├── data/                  # Document storage
│   ├── raw/              # Raw PDF documents
│   └── processed/        # Processed JSON data
├── ingestion/            # Document processing
│   ├── pdf_parser.py     # PDF parsing utilities
│   └── smart_ingest.py   # Smart chunking ingestion
├── retriever/            # RAG pipeline
│   ├── basic_retriever.py
│   └── rag_pipeline.py
├── static/               # Frontend assets
│   ├── css/
│   └── js/
├── templates/            # HTML templates
├── notebook/             # Jupyter notebooks for experimentation
└── requirements.txt      # Python dependencies
```


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

## ⚠️ Disclaimer

This is an independent project and is not officially affiliated with or endorsed by the Central Bank of Sri Lanka. All information is sourced from publicly available documents.
