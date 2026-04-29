"""
Project 2: LLM API Backend dengan Ollama Integration
Direct integration dengan local LLM models
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
import json
import os
from datetime import datetime
import httpx
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Ollama LLM Backend", version="1.0.0")

# Models
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    model: str = "mistral"
    session_id: Optional[str] = None
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9

class ChatResponse(BaseModel):
    response: str
    model: str
    session_id: str
    timestamp: str
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None

class StreamRequest(BaseModel):
    message: str
    model: str = "mistral"
    session_id: Optional[str] = None

class ModelInfo(BaseModel):
    name: str
    description: str
    parameter_size: str
    use_case: str

# Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_API_ENDPOINT = f"{OLLAMA_BASE_URL}/api/generate"
OLLAMA_CHAT_ENDPOINT = f"{OLLAMA_BASE_URL}/api/chat"

# In-memory storage for conversation history
conversation_history: Dict[str, List[ChatMessage]] = {}

# Available models
AVAILABLE_MODELS = {
    "mistral": ModelInfo(
        name="Mistral",
        description="Fast and powerful model for general purpose",
        parameter_size="7B",
        use_case="General chat, coding, analysis"
    ),
    "neural-chat": ModelInfo(
        name="Neural Chat",
        description="Optimized for conversational AI",
        parameter_size="7B",
        use_case="Chat and dialogue"
    ),
    "llama2": ModelInfo(
        name="Llama 2",
        description="Meta's powerful open-source model",
        parameter_size="7B/13B/70B",
        use_case="General purpose, high quality"
    )
}

async def check_ollama_health():
    """Check if Ollama is running"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5.0)
            return response.status_code == 200
    except Exception:
        return False

async def query_ollama(message: str, model: str, temperature: float = 0.7, top_p: float = 0.9):
    """Query Ollama API"""
    try:
        async with httpx.AsyncClient() as client:
            payload = {
                "model": model,
                "prompt": message,
                "stream": False,
                "temperature": temperature,
                "top_p": top_p
            }
            
            response = await client.post(
                OLLAMA_API_ENDPOINT,
                json=payload,
                timeout=120.0
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            else:
                raise Exception(f"Ollama API error: {response.text}")
    
    except Exception as e:
        raise Exception(f"Error querying Ollama: {str(e)}")

async def query_ollama_chat(messages: List[Dict], model: str, temperature: float = 0.7):
    """Query Ollama Chat API"""
    try:
        async with httpx.AsyncClient() as client:
            payload = {
                "model": model,
                "messages": messages,
                "stream": False,
                "temperature": temperature
            }
            
            response = await client.post(
                OLLAMA_CHAT_ENDPOINT,
                json=payload,
                timeout=120.0
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["message"]["content"]
            else:
                raise Exception(f"Ollama API error: {response.text}")
    
    except Exception as e:
        raise Exception(f"Error querying Ollama: {str(e)}")

# Endpoints
@app.get("/models")
async def list_models():
    """List available models"""
    return {
        "available_models": AVAILABLE_MODELS,
        "note": "Make sure models are pulled: ollama pull <model-name>"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with LLM"""
    
    # Check Ollama
    if not await check_ollama_health():
        raise HTTPException(
            status_code=503,
            detail=f"Ollama not running at {OLLAMA_BASE_URL}. Start with: ollama serve"
        )
    
    try:
        session_id = request.session_id or f"session_{datetime.now().timestamp()}"
        
        # Initialize session history if needed
        if session_id not in conversation_history:
            conversation_history[session_id] = []
        
        # Add user message to history
        conversation_history[session_id].append(
            ChatMessage(role="user", content=request.message)
        )
        
        # Prepare messages for context
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in conversation_history[session_id]
        ]
        
        # Query Ollama
        response_text = await query_ollama_chat(
            messages=messages,
            model=request.model,
            temperature=request.temperature
        )
        
        # Add assistant response to history
        conversation_history[session_id].append(
            ChatMessage(role="assistant", content=response_text)
        )
        
        return ChatResponse(
            response=response_text,
            model=request.model,
            session_id=session_id,
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stream")
async def stream_chat(request: StreamRequest):
    """Stream chat response (line by line)"""
    
    if not await check_ollama_health():
        raise HTTPException(
            status_code=503,
            detail=f"Ollama not running at {OLLAMA_BASE_URL}"
        )
    
    try:
        async def generate():
            async with httpx.AsyncClient() as client:
                payload = {
                    "model": request.model,
                    "prompt": request.message,
                    "stream": True
                }
                
                async with client.stream(
                    "POST",
                    OLLAMA_API_ENDPOINT,
                    json=payload,
                    timeout=120.0
                ) as response:
                    async for line in response.aiter_lines():
                        if line:
                            try:
                                chunk = json.loads(line)
                                if "response" in chunk:
                                    yield chunk["response"]
                            except json.JSONDecodeError:
                                pass
        
        return {
            "status": "streaming",
            "message": "Use EventSource or SSE client to consume stream"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/{session_id}")
async def get_history(session_id: str):
    """Get conversation history"""
    if session_id not in conversation_history:
        raise HTTPException(
            status_code=404,
            detail=f"Session {session_id} not found"
        )
    
    return {
        "session_id": session_id,
        "messages": conversation_history[session_id],
        "message_count": len(conversation_history[session_id])
    }

@app.delete("/history/{session_id}")
async def clear_history(session_id: str):
    """Clear conversation history"""
    if session_id in conversation_history:
        del conversation_history[session_id]
        return {"status": "success", "message": f"History for {session_id} cleared"}
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Session {session_id} not found"
        )

@app.get("/health")
async def health():
    """Health check"""
    ollama_running = await check_ollama_health()
    
    return {
        "status": "healthy" if ollama_running else "degraded",
        "ollama_running": ollama_running,
        "ollama_url": OLLAMA_BASE_URL,
        "active_sessions": len(conversation_history),
        "available_models": list(AVAILABLE_MODELS.keys())
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Ollama LLM Backend",
        "description": "Direct integration with local LLM models",
        "ollama_url": OLLAMA_BASE_URL,
        "setup_instructions": [
            "1. Download Ollama from https://ollama.ai",
            "2. Run: ollama serve",
            "3. In another terminal: ollama pull mistral",
            "4. This API will connect to http://localhost:11434"
        ],
        "endpoints": {
            "GET /models": "List available models",
            "POST /chat": "Chat with LLM",
            "POST /stream": "Stream chat response",
            "GET /history/{session_id}": "Get conversation history",
            "DELETE /history/{session_id}": "Clear history",
            "GET /health": "Health check",
            "GET /docs": "API documentation"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
