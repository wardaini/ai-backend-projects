# AI Backend Projects - LLM Developer Intern Portfolio

🚀 **Portofolio untuk LLM Developer Intern - FXMedia**

Koleksi project backend AI yang showcase skill-skill untuk posisi LLM Developer Intern:
- **RAG Systems** dengan LangChain & Vector Databases
- **LLM Integration** dengan Ollama & local models
- **Semantic Search** dengan embeddings dan FAISS

---

## 📋 Daftar Project

### 1. **RAG Backend dengan LangChain + Chroma** 
`projects/01-rag-langchain-chroma/`

**Apa itu RAG?**
RAG (Retrieval-Augmented Generation) adalah teknik menggabungkan document retrieval dengan LLM untuk jawaban yang lebih kontekstual dan akurat.

**Yang di-cover:**
- Upload & indexing documents ke Chroma
- Query dengan semantic search
- Generate response dari LLM dengan context dari retrieved documents
- Integration dengan Ollama untuk local LLM

**Tech Stack:**
- FastAPI (backend)
- LangChain (orchestration)
- Chroma (vector database - gratis & local)
- Ollama (local LLM)
- Sentence-Transformers (embeddings)

**API Endpoints:**
```
POST   /rag/upload-documents    - Upload file untuk indexing
POST   /rag/query              - Query dengan RAG
GET    /rag/documents          - List documents yang sudah diindex
DELETE /rag/reset              - Reset knowledge base
GET    /health                 - Health check
```

**Quick Start:**
```bash
cd projects/01-rag-langchain-chroma
pip install -r requirements.txt
python main.py

# Test dengan curl:
curl -X POST http://localhost:8000/rag/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Apa itu RAG?", "model": "mistral"}'
```

---

### 2. **LLM API Backend dengan Ollama Integration**
`projects/02-ollama-integration/`

**Apa yang bisa dilakukan:**
- Direct chat dengan local LLM models
- Support multiple Ollama models
- Streaming responses real-time
- Conversation history management
- Model switching on-the-fly

**Tech Stack:**
- FastAPI (REST API)
- Ollama (local LLM runtime)
- Request/Response streaming
- Python async/await

**API Endpoints:**
```
GET    /models                 - List available models
POST   /chat                   - Chat completion
POST   /stream                 - Streaming response
POST   /history                - Get chat history
DELETE /history/{session_id}   - Clear history
GET    /health                 - Health check
```

**Quick Start:**
```bash
cd projects/02-ollama-integration
pip install -r requirements.txt

# Make sure Ollama is running:
# ollama run mistral

python main.py

# Test:
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Jelaskan apa itu machine learning",
    "model": "mistral",
    "session_id": "user123"
  }'
```

---

### 3. **Semantic Search Engine dengan FAISS**
`projects/03-semantic-search/`

**Apa yang bisa dilakukan:**
- Upload documents untuk indexing
- Search berdasarkan semantic similarity (bukan keyword matching)
- FAISS untuk fast similarity search
- Embeddings dengan Sentence-Transformers

**Tech Stack:**
- FastAPI (REST API)
- FAISS (vector search library - gratis & cepat)
- Sentence-Transformers (embeddings model)
- NumPy (numerical computation)

**API Endpoints:**
```
POST   /search                 - Search documents
POST   /index/build            - Build index dari file
POST   /index/add-documents    - Tambah documents ke index
GET    /index/info             - Info tentang index
DELETE /index/reset            - Reset index
GET    /health                 - Health check
```

**Quick Start:**
```bash
cd projects/03-semantic-search
pip install -r requirements.txt
python main.py

# Upload documents:
curl -X POST http://localhost:8002/index/build \
  -F "file=@documents.txt"

# Search:
curl -X POST http://localhost:8002/search \
  -H "Content-Type: application/json" \
  -d '{"query": "machine learning", "top_k": 5}'
```

---

## 🛠️ Setup & Prerequisites

### Requirements
- Python 3.8+
- Ollama (untuk Project 1 & 2)
- Git

### Installation

**1. Clone repository:**
```bash
git clone https://github.com/wardaini/ai-backend-projects.git
cd ai-backend-projects
```

**2. Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate     # Windows
```

**3. Install Ollama (jika belum):**
- Download dari: https://ollama.ai
- Setup model: `ollama pull mistral` atau `ollama pull neural-chat`
- Run: `ollama serve` (default: localhost:11434)

**4. Install dependencies untuk semua projects:**
```bash
# Install global requirements
pip install -r requirements.txt
```

---

## 🚀 Running All Projects

### Terminal 1 - Ollama (jika ada Project 1 & 2)
```bash
ollama serve
```

### Terminal 2 - Project 1 (RAG)
```bash
cd projects/01-rag-langchain-chroma
python main.py
# Running on http://localhost:8000
```

### Terminal 3 - Project 2 (Ollama Integration)
```bash
cd projects/02-ollama-integration
python main.py
# Running on http://localhost:8001
```

### Terminal 4 - Project 3 (Semantic Search)
```bash
cd projects/03-semantic-search
python main.py
# Running on http://localhost:8002
```

---

## 📚 Learning Resources & Implementation Details

### RAG (Retrieval-Augmented Generation)
**Alur kerja:**
1. User upload dokumen
2. Sistem chunking dokumen menjadi bagian-bagian kecil
3. Create embeddings untuk setiap chunk
4. Store embeddings di vector DB (Chroma)
5. Saat user query:
   - Create embedding dari query
   - Search similar chunks dari vector DB
   - Pass chunks + query ke LLM
   - LLM generate response dengan context

**Keuntungan RAG:**
- LLM dapat akses informasi terbaru
- Mengurangi hallucination (jawaban asal-asalan)
- Lebih cost-effective daripada fine-tuning
- Mudah update knowledge base

### Vector Databases & Embeddings
**Konsep:**
- **Embedding**: Representasi teks dalam bentuk numerik (vector)
- **Semantic Similarity**: Mengukur kesamaan makna antar teks
- **Vector DB**: Database yang dioptimalkan untuk similarity search

**Perbandingan Vector DB gratis:**
| Database | Local | Setup | Speed | Use Case |
|----------|-------|-------|-------|----------|
| **Chroma** | ✅ | Easy | Fast | Development, prototyping |
| **FAISS** | ✅ | Easy | Very Fast | Large-scale search |
| **Weaviate** | ✅ | Medium | Fast | Production-ready |
| **Pinecone** | ❌ | Very Easy | Very Fast | Cloud-hosted |

### LangChain
**Apa itu LangChain:**
- Framework untuk orchestrate LLM applications
- Menyediakan tools untuk chain multiple LLM calls
- Support berbagai models & tools

**Komponen utama:**
- **Models**: Interface ke berbagai LLM
- **Prompts**: Template untuk struktur input
- **Chains**: Urutan operasi yang terikat
- **Tools**: Integrasi dengan external APIs
- **Memory**: Menyimpan conversation history

---

## 🔧 API Testing

### Menggunakan cURL
```bash
# Test RAG
curl -X POST http://localhost:8000/rag/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Apa itu AI?", "model": "mistral"}'

# Test Ollama LLM
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "model": "mistral", "session_id": "test"}'

# Test Semantic Search
curl -X POST http://localhost:8002/search \
  -H "Content-Type: application/json" \
  -d '{"query": "search term", "top_k": 5}'
```

### Menggunakan Postman
1. Import collection dari `postman_collection.json`
2. Set environment variables
3. Run requests

### Menggunakan Python
```python
import requests

# RAG Query
response = requests.post(
    "http://localhost:8000/rag/query",
    json={"query": "Your question here", "model": "mistral"}
)
print(response.json())
```

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
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🎯 Tech Stack yang Dicovered

✅ **Backend**: FastAPI, Python async/await  
✅ **AI/ML**: LangChain, Ollama, Sentence-Transformers  
✅ **Vector Databases**: Chroma, FAISS  
✅ **APIs**: REST, JSON, streaming responses  
✅ **Database Integration**: File-based storage, in-memory indexing  
✅ **DevTools**: Git, virtual environments, requirements.txt  

---

## 💡 Tips untuk FXMedia Interview

1. **Pahami RAG Architecture**
   - Bisa jelaskan alur dari upload → query → response
   - Tahu trade-offs antara vector databases

2. **LangChain Best Practices**
   - Error handling yang baik
   - Proper prompting techniques
   - Memory management

3. **Performance Optimization**
   - Chunking strategies untuk documents
   - Index optimization untuk search
   - Caching untuk response yang sering diakses

4. **Backend Fundamentals**
   - REST API design yang clean
   - Error handling & validation
   - Async operations untuk performance

5. **Experimentation Mindset**
   - Try different models
   - Test various embeddings
   - Benchmark performance

---

## 🚀 Next Steps

1. **Clone & Setup** repository ini locally
2. **Run semua projects** dan test endpoints
3. **Modifikasi & experiment**:
   - Try different Ollama models
   - Customize RAG prompts
   - Optimize search parameters
4. **Deploy ke cloud** (optional):
   - Railway, Render, atau Heroku
5. **Share portfolio** dengan recruiter!

---

## 📖 Learning Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Ollama GitHub](https://github.com/ollama/ollama)
- [Chroma Documentation](https://docs.trychroma.com/)
- [FAISS Documentation](https://faiss.ai/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/)
- [Sentence-Transformers](https://www.sbert.net/)

---

## 📞 Troubleshooting

**Problem: "Ollama connection refused"**
```bash
# Make sure Ollama is running
ollama serve
```

**Problem: "Model not found in Ollama"**
```bash
# Pull model first
ollama pull mistral
```

**Problem: "FAISS index error"**
```bash
# Reset index
curl -X DELETE http://localhost:8002/index/reset
```

**Problem: "Import error for dependencies"**
```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

---

## 📝 License

Open source untuk educational purposes.

---

**Happy learning & good luck with FXMedia! 🎯**
