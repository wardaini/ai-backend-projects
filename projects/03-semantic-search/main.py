"""
Project 3: Semantic Search Engine
Search documents menggunakan embeddings dan FAISS
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional, List
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Semantic Search Engine", version="1.0.0")

# Models
class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResult(BaseModel):
    doc: str
    score: float
    index: int

class SearchResponse(BaseModel):
    results: List[SearchResult]
    query: str
    total_results: int

# Configuration
FAISS_INDEX_PATH = "./semantic_search.index"
METADATA_PATH = "./documents_metadata.json"
MODEL_NAME = "all-MiniLM-L6-v2"

# Global variables
model = None
index = None
documents = []
document_metadata = []

def initialize_model():
    """Initialize sentence transformer model"""
    global model
    try:
        print(f"Loading model: {MODEL_NAME}...")
        model = SentenceTransformer(MODEL_NAME)
        print("✅ Model loaded successfully")
        return model
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        return None

def initialize_index():
    """Initialize or load FAISS index"""
    global index, documents, document_metadata
    
    try:
        if os.path.exists(FAISS_INDEX_PATH) and os.path.exists(METADATA_PATH):
            print("Loading existing FAISS index...")
            index = faiss.read_index(FAISS_INDEX_PATH)
            
            with open(METADATA_PATH, 'r') as f:
                data = json.load(f)
                documents = data.get("documents", [])
                document_metadata = data.get("metadata", [])
            
            print(f"✅ Loaded index with {len(documents)} documents")
        else:
            print("No index found. Create one using /index/build endpoint")
            index = None
        
        return index
    
    except Exception as e:
        print(f"❌ Error loading index: {str(e)}")
        return None

def create_embeddings(texts: List[str]) -> np.ndarray:
    """Create embeddings for texts"""
    if not model:
        raise Exception("Model not initialized")
    
    embeddings = model.encode(texts, show_progress_bar=True)
    return np.array(embeddings).astype('float32')

def save_index():
    """Save index and metadata"""
    if index and documents:
        faiss.write_index(index, FAISS_INDEX_PATH)
        
        with open(METADATA_PATH, 'w') as f:
            json.dump({
                "documents": documents,
                "metadata": document_metadata,
                "model": MODEL_NAME
            }, f, indent=2)
        
        print(f"✅ Index saved with {len(documents)} documents")

# Endpoints
@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    initialize_model()
    initialize_index()

@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """Search documents using semantic similarity"""
    
    if not index or not documents:
        raise HTTPException(
            status_code=503,
            detail="No index available. Build index using /index/build endpoint"
        )
    
    if not model:
        raise HTTPException(status_code=500, detail="Model not initialized")
    
    try:
        # Create query embedding
        query_embedding = create_embeddings([request.query])
        
        # Search
        distances, indices = index.search(query_embedding, k=min(request.top_k, len(documents)))
        
        # Build results
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(documents):
                # Convert distance to similarity score (0-1)
                # For L2 distance, smaller is better
                similarity = 1 / (1 + distances[0][i])
                
                results.append(SearchResult(
                    doc=documents[idx],
                    score=float(similarity),
                    index=int(idx)
                ))
        
        return SearchResponse(
            results=results,
            query=request.query,
            total_results=len(results)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/index/build")
async def build_index(file: UploadFile = File(...)):
    """Build index from text file (one document per line)"""
    global index, documents, document_metadata
    
    if not model:
        raise HTTPException(status_code=500, detail="Model not initialized")
    
    try:
        # Read file
        content = await file.read()
        text = content.decode('utf-8')
        
        # Parse documents (one per line)
        documents = [line.strip() for line in text.split('\n') if line.strip()]
        
        if not documents:
            raise ValueError("File is empty or has no valid documents")
        
        print(f"📄 Loaded {len(documents)} documents")
        
        # Create embeddings
        print("🔄 Creating embeddings...")
        embeddings = create_embeddings(documents)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)
        
        # Save index
        save_index()
        
        return {
            "status": "success",
            "documents_indexed": len(documents),
            "embedding_dimension": dimension,
            "model": MODEL_NAME
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error building index: {str(e)}")

@app.post("/index/add-documents")
async def add_documents(docs: List[str]):
    """Add documents to existing index"""
    global index, documents, document_metadata
    
    if not model:
        raise HTTPException(status_code=500, detail="Model not initialized")
    
    if not index:
        raise HTTPException(status_code=400, detail="No index exists. Build one first using /index/build")
    
    try:
        # Create embeddings for new docs
        new_embeddings = create_embeddings(docs)
        
        # Add to index
        index.add(new_embeddings)
        
        # Add to documents list
        documents.extend(docs)
        
        # Save
        save_index()
        
        return {
            "status": "success",
            "new_documents_added": len(docs),
            "total_documents": len(documents)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/index/info")
async def index_info():
    """Get index information"""
    if not index:
        return {
            "status": "not_created",
            "message": "Build index using /index/build endpoint"
        }
    
    return {
        "status": "ready",
        "total_documents": len(documents),
        "index_dimension": index.d,
        "model": MODEL_NAME,
        "faiss_index_type": "L2 (Euclidean distance)"
    }

@app.delete("/index/reset")
async def reset_index():
    """Reset index"""
    global index, documents, document_metadata
    
    try:
        index = None
        documents = []
        document_metadata = []
        
        if os.path.exists(FAISS_INDEX_PATH):
            os.remove(FAISS_INDEX_PATH)
        if os.path.exists(METADATA_PATH):
            os.remove(METADATA_PATH)
        
        return {"status": "success", "message": "Index reset"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "index_ready": index is not None,
        "documents_indexed": len(documents),
        "model": MODEL_NAME
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Semantic Search Engine",
        "description": "Search documents using semantic similarity with embeddings",
        "model": MODEL_NAME,
        "endpoints": {
            "POST /search": "Search documents",
            "POST /index/build": "Build index from text file",
            "POST /index/add-documents": "Add documents to index",
            "GET /index/info": "Get index info",
            "DELETE /index/reset": "Reset index",
            "GET /health": "Health check",
            "GET /docs": "API documentation"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
