# AI Backend Projects



Project backend AI dengan web interface:
- **3 Backend Services** (RAG, Ollama LLM, Semantic Search)
- **1 Unified Streamlit Dashboard** untuk showcase semua
- **Production-ready code** dengan error handling & monitoring

---

## 📋 Daftar Isi

1. [Project Overview](#-project-overview)
2. [Tech Stack](#-tech-stack)
3. [Installation & Setup](#-installation--setup)
4. [Running All Services](#-running-all-services)
5. [API Endpoints](#-api-endpoints)
6. [Project Details](#-project-details)
7. [Web Interface](#-web-interface)
8. [Architecture](#-architecture)
9. [Learning Resources](#-learning-resources)
10. [Troubleshooting](#-troubleshooting)

---

## 📦 Project Overview

### **3 Backend Microservices**

#### 1️⃣ **RAG Backend** (Port 8000)
- **Technology**: FastAPI, LangChain, Chroma
- **Purpose**: Retrieval-Augmented Generation untuk contextual AI responses
- **Features**:
  - Upload & indexing documents
  - Semantic search over documents
  - LLM response generation dengan context
  - Source citations

#### 2️⃣ **Ollama LLM Backend** (Port 8001)
- **Technology**: FastAPI, Ollama, Local LLMs
- **Purpose**: Direct integration dengan local language models
- **Features**:
  - Multi-model support (Mistral, Neural Chat, Llama 2)
  - Conversation history management
  - Configurable parameters (temperature, top_p)
  - Streaming responses

#### 3️⃣ **Semantic Search Backend** (Port 8002)
- **Technology**: FastAPI, FAISS, Sentence-Transformers
- **Purpose**: Document search using semantic similarity
- **Features**:
  - Fast similarity search dengan FAISS
  - Embeddings dengan Sentence-Transformers
  - Scalable indexing
  - Real-time search

### **Unified Web Interface**

#### 🎨 **Streamlit Dashboard** (Port 8501)
- **Technology**: Streamlit, Python
- **Purpose**: Single interface untuk interact dengan semua 3 backends
- **Features**:
  - 4 main tabs (RAG Chat, Direct LLM, Semantic Search, Dashboard)
  - Real-time health monitoring
  - Chat history management
  - Document upload & indexing
  - System status dashboard

---

## 🛠 Tech Stack

### **Backend Stack**
```
┌─────────────────────────────────────────┐
│           Backend Services              │
├─────────────────────────────────────────┤
│ Framework:  FastAPI (async Python)      │
│ Server:     Uvicorn                     │
│ APIs:       REST with JSON              │
│ Validation: Pydantic                    │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│         AI/ML & LLM Stack               │
├─────────────────────────────────────────┤
│ Orchestration: LangChain                │
│ Local LLMs:    Ollama                   │
│ Embeddings:    Sentence-Transformers    │
│ Models:        Hugging Face             │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│         Vector Database Stack           │
├─────────────────────────────────────────┤
│ Chroma (RAG):      Local vector DB      │
│ FAISS (Search):    Fast similarity search│
│ Embeddings:        all-MiniLM-L6-v2    │
└─────────────────────────────────────────┘
```

### **Frontend Stack**
```
┌─────────────────────────────────────────┐
│         Web Interface Stack             │
├─────────────────────────────────────────┤
│ Framework:   Streamlit                  │
│ Language:    Python                     │
│ HTTP:        requests library           │
│ Port:        8501                       │
└─────────────────────────────────────────┘
```

### **Complete Tech Coverage**

✅ **Languages**: Python  
✅ **Frameworks**: FastAPI, Streamlit  
✅ **Databases**: Chroma, FAISS, PostgreSQL-ready  
✅ **AI Tools**: LangChain, LangGraph-ready, Hugging Face, Ollama  
✅ **APIs**: REST, JSON, streaming  
✅ **DevTools**: Git, virtual environments, Docker-ready  

---

## 🚀 Installation & Setup

### **Prerequisites**

- Python 3.8+
- Ollama (untuk local LLMs)
- Git
- 8GB+ RAM recommended

### **Step 1: Clone Repository**

```bash
git clone https://github.com/wardaini/ai-backend-projects.git
cd ai-backend-projects
```

### **Step 2: Create Virtual Environment**

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### **Step 3: Install Global Dependencies**

```bash
pip install -r requirements.txt
```

### **Step 4: Setup Ollama**

**Download & Install:**
- Go to https://ollama.ai
- Download installer untuk OS Anda
- Install & run

**Pull Models:**
```bash
# Model yang direkomendasikan
ollama pull mistral

# Optional - model lain
ollama pull neural-chat
ollama pull llama2
```

**Verify Installation:**
```bash
# Test Ollama API
curl http://localhost:11434/api/tags
```

### **Step 5: Setup Environment Variables**

```bash
# Copy .env.example ke .env di setiap project folder
cp .env.example .env

# Atau setup global
cp .env.example .env
```

Default configuration tidak perlu diubah untuk local development.

---

## 🎯 Running All Services

### **Option A: Manual Setup (5 Terminals)**

**Terminal 1 - Ollama Server:**
```bash
ollama serve
# Output: Listening on 127.0.0.1:11434
```

**Terminal 2 - RAG Backend:**
```bash
cd projects/01-rag-langchain-chroma
python main.py
# Output: Application startup complete
# Access: http://localhost:8000/docs
```

**Terminal 3 - Ollama LLM Backend:**
```bash
cd projects/02-ollama-integration
python main.py
# Output: Application startup complete
# Access: http://localhost:8001/docs
```

**Terminal 4 - Semantic Search Backend:**
```bash
cd projects/03-semantic-search
python main.py
# Output: Application startup complete
# Access: http://localhost:8002/docs
```

**Terminal 5 - Streamlit Web:**
```bash
cd streamlit_app
pip install -r requirements.txt
streamlit run app.py
# Output: You can now view your Streamlit app in your browser
# Access: http://localhost:8501
```

### **Option B: Using Shell Script**

```bash
bash run_all.sh
```

### **Verify All Services Running**

```bash
# Health check semua services
curl http://localhost:8000/health
curl http://localhost:8001/health
curl http://localhost:8002/health

# Akses Streamlit dashboard
open http://localhost:8501
```

---

## 📡 API Endpoints

### **RAG Backend (Port 8000)**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/rag/upload-documents` | Upload & index documents |
| POST | `/rag/query` | Query dengan RAG |
| GET | `/rag/documents` | List indexed documents |
| DELETE | `/rag/reset` | Reset knowledge base |
| GET | `/health` | Health check |
| GET | `/docs` | Interactive API docs |

**Example Request:**
```bash
curl -X POST http://localhost:8000/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Apa itu machine learning?",
    "model": "mistral",
    "k": 3
  }'
```

### **Ollama LLM Backend (Port 8001)**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/models` | List available models |
| POST | `/chat` | Chat completion |
| POST | `/stream` | Streaming response |
| GET | `/history/{session_id}` | Get conversation history |
| DELETE | `/history/{session_id}` | Clear history |
| GET | `/health` | Health check |
| GET | `/docs` | Interactive API docs |

**Example Request:**
```bash
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Jelaskan Python",
    "model": "mistral",
    "session_id": "user123",
    "temperature": 0.7
  }'
```

### **Semantic Search Backend (Port 8002)**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/search` | Search documents |
| POST | `/index/build` | Build index from file |
| POST | `/index/add-documents` | Add documents to index |
| GET | `/index/info` | Get index information |
| DELETE | `/index/reset` | Reset index |
| GET | `/health` | Health check |
| GET | `/docs` | Interactive API docs |

**Example Request:**
```bash
curl -X POST http://localhost:8002/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "machine learning",
    "top_k": 5
  }'
```

### **API Documentation**

Setiap service punya interactive Swagger docs:
- RAG: http://localhost:8000/docs
- LLM: http://localhost:8001/docs
- Search: http://localhost:8002/docs

---

## 📚 Project Details

### **Project 1: RAG Backend dengan LangChain + Chroma**

**Location:** `projects/01-rag-langchain-chroma/`

**Architecture:**
```
┌──────────────────────────────────────┐
│   User Upload Documents              │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│   Document Chunking & Processing     │
│   (RecursiveCharacterTextSplitter)   │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│   Create Embeddings                  │
│   (HuggingFaceEmbeddings)            │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│   Store in Vector DB (Chroma)        │
│   with Persistence                   │
└──────────────────┬───────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
   User Query         Retrieved Context
        │                     │
        └──────────┬──────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│   LLM (Ollama) Generate Response     │
│   with Retrieved Context             │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│   Response + Source Citations        │
│   Return to User                     │
└──────────────────────────────────────┘
```

**Key Components:**
- **Document Loader**: Load text files
- **Text Splitter**: Chunk documents dengan overlap
- **Embeddings**: Convert text to vectors
- **Vector Store**: Chroma for persistence
- **Retriever**: Semantic similarity search
- **LLM Chain**: LangChain RetrievalQA chain

**Use Cases:**
- Customer support Q&A
- Knowledge base search
- Document analysis
- FAQ automation

**Setup:**
```bash
cd projects/01-rag-langchain-chroma
pip install -r requirements.txt
python main.py
```

---

### **Project 2: Ollama LLM Integration**

**Location:** `projects/02-ollama-integration/`

**Architecture:**
```
┌──────────────────────────────────────┐
│   Streamlit Web Interface            │
└──────────────────┬───────────────────┘
                   │ HTTP Request
                   ▼
┌──────────────────────────────────────┐
│   FastAPI LLM Backend                │
│   (Session Management)               │
└──────────────────┬───────────────────┘
                   │ Ollama API Call
                   ▼
┌──────────────────────────────────────┐
│   Ollama Server (Port 11434)         │
│   Running Local LLM                  │
│   (Mistral, Neural Chat, etc)        │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│   LLM Response Generation            │
│   with Conversation History          │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│   Stream/Return Response to User     │
└──────────────────────────────────────┘
```

**Key Features:**
- **Multi-Model Support**: Switch between Mistral, Neural Chat, Llama 2
- **Conversation History**: Keep context across messages
- **Parameter Control**: Temperature, top_p tuning
- **Session Management**: Track multiple conversations
- **Streaming**: Real-time response streaming (optional)

**Available Models:**

| Model | Size | Speed | Use Case |
|-------|------|-------|----------|
| mistral | 7B | ⚡ Fast | General purpose |
| neural-chat | 7B | ⚡ Fast | Conversation |
| llama2 | 7B-70B | ⏱ Medium | High quality |
| orca-mini | 3B | ⚡⚡ Very Fast | Quick responses |

**Setup:**
```bash
cd projects/02-ollama-integration
pip install -r requirements.txt
python main.py
```

**Available Models Reference:**
Lihat `projects/02-ollama-integration/models.md` untuk dokumentasi lengkap.

---

### **Project 3: Semantic Search Engine**

**Location:** `projects/03-semantic-search/`

**Architecture:**
```
┌──────────────────────────────────────┐
│   Upload Documents                   │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│   Create Embeddings                  │
│   (Sentence-Transformers)            │
│   all-MiniLM-L6-v2 (384 dims)       │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│   Build FAISS Index                  │
│   L2 (Euclidean) Distance            │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│   Persist to Disk                    │
│   (semantic_search.index)            │
└──────────────────┬───────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
   User Search Query    Retrieve Embeddings
        │                     │
        └──────────┬──────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│   FAISS Similarity Search            │
│   (Fast Vector Search)               │
└���─────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│   Ranked Results by Score (0-1)      │
│   Return to User                     │
└──────────────────────────────────────┘
```

**Key Features:**
- **Fast Similarity Search**: FAISS indexing
- **Semantic Understanding**: Sentence-Transformers embeddings
- **Persistence**: Save/load indices
- **Scalability**: Handle large document sets
- **Similarity Scoring**: 0-1 relevance scores

**Embedding Model:**
- **Model**: all-MiniLM-L6-v2
- **Dimensions**: 384
- **Speed**: Very fast
- **Size**: ~22MB
- **Use**: General purpose semantic search

**Setup:**
```bash
cd projects/03-semantic-search
pip install -r requirements.txt
python main.py
```

---

## 🎨 Web Interface

### **Streamlit Dashboard**

**Location:** `streamlit_app/`

**How to Run:**
```bash
cd streamlit_app
pip install -r requirements.txt
streamlit run app.py
# Open: http://localhost:8501
```

### **Features**

#### **Tab 1: 🔍 RAG Chat**
- Upload documents untuk indexing
- Real-time document counter
- Chat interface dengan source citations
- View documents dalam expander
- Clear chat history button

**Workflow:**
1. Upload .txt file
2. Wait for indexing (chunks akan diproses)
3. Type pertanyaan
4. Lihat jawaban + sources

#### **Tab 2: 💬 Direct LLM Chat**
- Model selector dropdown
- Temperature slider (0.0 - 1.0)
- Top P slider (0.0 - 1.0)
- Active sessions counter
- Available models display
- Conversation history
- Clear chat button

**Workflow:**
1. Select model dari dropdown
2. Adjust parameters jika perlu
3. Type message
4. Send & wait for response
5. History otomatis tersimpan

#### **Tab 3: 🔎 Semantic Search**
- Build index dari documents
- Real-time index status
- Search dengan semantic similarity
- Top K results selector (1-10)
- Similarity score display
- Expandable results

**Workflow:**
1. Upload .txt file dengan documents
2. Click "Build Index"
3. Wait for embeddings to be created
4. Type search query
5. View ranked results dengan scores

#### **Tab 4: 📊 Dashboard**
- Status semua 3 backends (online/offline)
- API endpoints list
- Health check info
- Tech stack display
- Quick start instructions
- Setup guide

**Displays:**
- Ollama running status
- Number of active sessions
- Available models
- Index ready status
- API documentation links

---

## 🏗 Architecture

### **Overall System Architecture**

```
┌───────────────────────────────────────────────────────────┐
│                   Users                                   │
└─────────────────────────┬─────────────────────────────────┘
                          │
                          ▼
┌───────────────────────────────────────────────────────────┐
│          Streamlit Web Interface (Port 8501)              │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ RAG Chat │ LLM Chat │ Search │ Dashboard           │  │
│  └────┬──────────┬────────────┬───────────┬───────────┘  │
└──────┼──────────┼────────────┼───────────┼───────────────┘
       │          │            │           │
       ▼          ▼            ▼           ▼
   ┌───────────────────────────────────────────────┐
   │       Microservices (FastAPI Backends)       │
   ├───────────────────────────────────────────────┤
   │                                               │
   │  RAG Backend  │  LLM Backend  │  Search      │
   │  (Port 8000)  │  (Port 8001)  │  (Port 8002) │
   │                                               │
   └──────────┬─────────────────┬─────────────┬───┘
              │                 │             │
              ▼                 ▼             ▼
         ┌────────────────────────────────────────────┐
         │    AI/ML & Storage Layer                   │
         ├────────────────────────────────────────────┤
         │                                            │
         │  Chroma (Vector DB)  │  FAISS (Search)    │
         │  LangChain           │  Sentence-Trans.   │
         │  Ollama (Port 11434) │  Embeddings        │
         │                                            │
         └────────────────────────────────────────────┘
```

### **Data Flow Examples**

**RAG Query Flow:**
```
User Input
    ↓
Streamlit Web
    ↓
RAG Backend (Port 8000)
    ↓
Document Search (Chroma)
    ↓
LLM (Ollama)
    ↓
Response + Sources
    ↓
Streamlit Display
```

**LLM Chat Flow:**
```
User Message
    ↓
Streamlit Web
    ↓
LLM Backend (Port 8001)
    ↓
Ollama Server (Port 11434)
    ↓
Model Response
    ↓
Streamlit Display
```

**Semantic Search Flow:**
```
User Query
    ↓
Streamlit Web
    ↓
Search Backend (Port 8002)
    ↓
Create Query Embedding
    ↓
FAISS Index Search
    ↓
Rank by Similarity
    ↓
Streamlit Display Results
```

---

## 📚 Learning Resources

### **Concepts**

**RAG (Retrieval-Augmented Generation)**
- Combines information retrieval dengan generative AI
- Gives LLMs access to external knowledge
- Reduces hallucinations
- Keeps knowledge updated
- [Read More](https://python.langchain.com/docs/use_cases/question_answering/)

**Vector Databases**
- Store embeddings untuk fast similarity search
- Enable semantic understanding
- Support different distance metrics
- [FAISS Docs](https://faiss.ai/)
- [Chroma Docs](https://docs.trychroma.com/)

**LangChain**
- Framework untuk orchestrate LLM applications
- Provides abstractions untuk models, prompts, chains
- Integrates dengan 100+ tools
- [Docs](https://python.langchain.com/)

**Embeddings & Semantic Similarity**
- Convert text to numerical vectors
- Measure semantic meaning
- Enable reasoning over text
- [Sentence-Transformers](https://www.sbert.net/)

### **Official Documentation**

- [LangChain Documentation](https://python.langchain.com/)
- [Ollama GitHub](https://github.com/ollama/ollama)
- [Chroma Documentation](https://docs.trychroma.com/)
- [FAISS](https://faiss.ai/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Sentence-Transformers](https://www.sbert.net/)

### **Interview Preparation Tips**

1. **Understand RAG Architecture**
   - Explain alur dari upload → indexing → query
   - Know trade-offs vector DBs
   - Chunking strategies

2. **Know LangChain Patterns**
   - Chains, agents, memory
   - Prompt engineering
   - Tool integration

3. **Backend Fundamentals**
   - REST API design
   - Async/await patterns
   - Error handling

4. **Experimentation Mindset**
   - Try different models
   - Benchmark performance
   - Optimize parameters

---

## 🔧 Troubleshooting

### **Ollama Connection Error**

**Problem:**
```
Error: Connection refused to http://localhost:11434
```

**Solution:**
```bash
# Make sure Ollama is running
ollama serve

# Verify in another terminal
curl http://localhost:11434/api/tags
```

### **Model Not Found**

**Problem:**
```
Error: model 'mistral' not found
```

**Solution:**
```bash
# Pull the model
ollama pull mistral

# List available models
ollama list
```

### **Port Already in Use**

**Problem:**
```
Error: Address already in use: ('0.0.0.0', 8000)
```

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
python main.py --port 8003
```

### **FAISS Index Error**

**Problem:**
```
Error: Cannot read index
```

**Solution:**
```bash
# Reset index
curl -X DELETE http://localhost:8002/index/reset

# Or manually delete files
rm semantic_search.index
rm documents_metadata.json
```

### **Memory Issues**

**Problem:**
```
MemoryError: Unable to allocate 4.5 GiB for array
```

**Solution:**
- Use smaller models (orca-mini instead of llama2-70b)
- Reduce chunk sizes
- Use FAISS instead of Chroma

### **Dependency Conflicts**

**Problem:**
```
Error: conflicting requirements
```

**Solution:**
```bash
# Fresh install
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

---

## 📊 Performance Metrics

### **Expected Response Times**

| Operation | Time | Model/Method |
|-----------|------|---------------|
| RAG Query | 2-5s | Mistral + Chroma |
| LLM Response | 5-15s | Mistral (7B) |
| Semantic Search | 100-500ms | FAISS |
| Document Indexing | 1-3s | 10 documents |

*Times may vary based on hardware*

### **Resource Requirements**

| Service | RAM | Disk | GPU |
|---------|-----|------|-----|
| Ollama (mistral) | 4-6GB | 5GB | Optional |
| Chroma | 1-2GB | 2GB | N/A |
| FAISS | 0.5-1GB | 0.5GB | N/A |
| Streamlit | 0.5GB | 0.5GB | N/A |
| **Total** | **8-10GB** | **10GB** | Optional |

---

## 📁 Project Structure

```
ai-backend-projects/
├── projects/
│   ├── 01-rag-langchain-chroma/
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   ├── .env.example
│   │   └── sample_documents.txt
│   ├── 02-ollama-integration/
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   ├── .env.example
│   │   └── models.md
│   └── 03-semantic-search/
│       ├── main.py
│       ├── requirements.txt
│       ├── .env.example
│       └── sample_documents.txt
│
├── streamlit_app/
│   ├── app.py
│   ├── requirements.txt
│   ├── .streamlit/
│   │   └── config.toml
│   └── .env.example
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 Next Steps & Improvements

### **Current Features** ✅
- 3 working backends
- Unified Streamlit interface
- Full documentation
- Health monitoring
- Error handling

### **Future Enhancements** 📋

**Backend Improvements:**
- [ ] Add LangGraph support for complex workflows
- [ ] Implement Neo4J for graph RAG
- [ ] Add Pinecone integration
- [ ] Multi-user authentication
- [ ] Database persistence (PostgreSQL)
- [ ] Rate limiting & caching
- [ ] Docker containerization

**Frontend Improvements:**
- [ ] Mobile-responsive design
- [ ] Advanced visualizations (embeddings plot)
- [ ] Document upload with drag-drop
- [ ] Export conversations
- [ ] Admin dashboard

**Deployment:**
- [ ] Docker Compose setup
- [ ] Kubernetes manifests
- [ ] CI/CD pipeline
- [ ] Cloud deployment (AWS/GCP)

---

## 🤝 Contributing

Feel free to fork and customize!

**Suggestions:**
1. Try different embedding models
2. Experiment with LangChain patterns
3. Add new vector databases
4. Implement new UI features

---

## 📝 License

Open source untuk educational purposes.

---

## 📞 Support & Contact

- **GitHub**: https://github.com/wardaini/ai-backend-projects
- **Issues**: Open an issue untuk bugs/questions

---

## 🎓 Learning Outcomes

Setelah project ini, Anda akan understand:

✅ **Backend Architecture**
- REST API design dengan FastAPI
- Async/await patterns
- Microservices approach
- Error handling & validation

✅ **AI/ML Concepts**
- RAG systems
- LLM integration
- Embeddings & vector search
- Prompt engineering

✅ **Vector Databases**
- Chroma for persistence
- FAISS for fast search
- Embeddings generation
- Similarity scoring

✅ **Web Development**
- Streamlit frameworks
- API integration
- State management
- UI/UX patterns

✅ **DevOps & Deployment**
- Virtual environments
- Dependency management
- Multi-service orchestration
- Health monitoring

---

## 🎯 For FXMedia Interview

**Show & Tell:**
1. Run all services
2. Demo RAG chat
3. Show Semantic search speed
4. Explain architecture
5. Ask about future enhancements

**Key Talking Points:**
- "I built this to showcase full-stack AI development"
- "All services are modular and scalable"
- "Uses production-grade tools (FastAPI, LangChain, FAISS)"
- "Integrated with local Ollama for privacy"
- "Ready to extend with LangGraph & Neo4J"

---

<div style='text-align: center'>

## **Good luck! 🚀**


*Last Updated: 2026-04-29*

</div>
