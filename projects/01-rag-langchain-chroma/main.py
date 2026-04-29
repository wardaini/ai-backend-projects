"""
Project 1: RAG Backend dengan LangChain + Chroma
Retrieval-Augmented Generation untuk kontekstual AI responses
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional, List
import os
import tempfile
from pathlib import Path

from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.callbacks import StreamingStdOutCallbackHandler

from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="RAG Backend", version="1.0.0")

# Models
class QueryRequest(BaseModel):
    query: str
    model: str = "mistral"
    k: int = 3

class QueryResponse(BaseModel):
    query: str
    answer: str
    sources: List[str]
    model: str

class DocumentInfo(BaseModel):
    count: int
    names: List[str]

# Configuration
PERSIST_DIRECTORY = "./chroma_storage"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")

# Global variables
vector_store = None
embeddings = None
documents_loaded = []

def initialize_embeddings():
    """Initialize embeddings model"""
    global embeddings
    try:
        print(f"Loading embeddings model: {EMBEDDING_MODEL}...")
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        print("✅ Embeddings model loaded")
        return embeddings
    except Exception as e:
        print(f"❌ Error loading embeddings: {str(e)}")
        return None

def initialize_vector_store():
    """Initialize or load Chroma vector store"""
    global vector_store
    try:
        print(f"Initializing Chroma with persistence at: {PERSIST_DIRECTORY}")
        vector_store = Chroma(
            embedding_function=embeddings,
            persist_directory=PERSIST_DIRECTORY,
            collection_name="documents"
        )
        print("✅ Vector store initialized")
        return vector_store
    except Exception as e:
        print(f"❌ Error initializing vector store: {str(e)}")
        return None

def chunk_documents(file_path: str, chunk_size: int = 500, overlap: int = 50):
    """Split documents into chunks"""
    try:
        # Load document
        loader = TextLoader(file_path)
        documents = loader.load()
        
        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        
        chunks = text_splitter.split_documents(documents)
        print(f"✅ Document split into {len(chunks)} chunks")
        return chunks
    except Exception as e:
        raise Exception(f"Error chunking document: {str(e)}")

# Endpoints
@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    initialize_embeddings()
    initialize_vector_store()

@app.post("/rag/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """Query the RAG system"""
    
    if not vector_store or not embeddings:
        raise HTTPException(
            status_code=503,
            detail="Vector store not initialized. Upload documents first."
        )
    
    try:
        # Initialize LLM
        llm = Ollama(
            base_url=OLLAMA_BASE_URL,
            model=request.model,
            callbacks=[StreamingStdOutCallbackHandler()]
        )
        
        # Create RAG chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever(search_kwargs={"k": request.k}),
            return_source_documents=True
        )
        
        # Query
        result = qa_chain({"query": request.query})
        
        # Extract sources
        sources = [
            doc.metadata.get("source", "Unknown") 
            for doc in result.get("source_documents", [])
        ]
        
        return QueryResponse(
            query=request.query,
            answer=result["result"],
            sources=sources,
            model=request.model
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/rag/upload-documents")
async def upload_documents(file: UploadFile = File(...)):
    """Upload and index documents"""
    
    if not vector_store or not embeddings:
        raise HTTPException(
            status_code=503,
            detail="Vector store not initialized"
        )
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        # Chunk documents
        chunks = chunk_documents(tmp_path)
        
        # Add to vector store
        print(f"Adding {len(chunks)} chunks to vector store...")
        vector_store.add_documents(chunks)
        vector_store.persist()
        
        # Track loaded documents
        documents_loaded.append(file.filename)
        
        # Cleanup
        os.unlink(tmp_path)
        
        return {
            "status": "success",
            "filename": file.filename,
            "chunks_indexed": len(chunks),
            "total_documents_loaded": len(documents_loaded)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/rag/documents", response_model=DocumentInfo)
async def get_documents():
    """Get information about loaded documents"""
    return DocumentInfo(
        count=len(documents_loaded),
        names=documents_loaded
    )

@app.delete("/rag/reset")
async def reset_rag():
    """Reset the RAG system"""
    global vector_store, documents_loaded
    
    try:
        # Clear documents list
        documents_loaded = []
        
        # Reset vector store
        if vector_store:
            # Reinitialize
            vector_store = Chroma(
                embedding_function=embeddings,
                persist_directory=PERSIST_DIRECTORY,
                collection_name="documents",
                collection_metadata={"hnsw:space": "cosine"}
            )
        
        return {"status": "success", "message": "RAG system reset"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "vector_store_ready": vector_store is not None,
        "embeddings_loaded": embeddings is not None,
        "documents_loaded": len(documents_loaded),
        "embedding_model": EMBEDDING_MODEL,
        "default_ollama_model": OLLAMA_MODEL,
        "ollama_base_url": OLLAMA_BASE_URL
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "RAG Backend with LangChain & Chroma",
        "description": "Retrieval-Augmented Generation API",
        "endpoints": {
            "POST /rag/upload-documents": "Upload files for indexing",
            "POST /rag/query": "Query the RAG system",
            "GET /rag/documents": "List loaded documents",
            "DELETE /rag/reset": "Reset the system",
            "GET /health": "Health check",
            "GET /docs": "API documentation"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
