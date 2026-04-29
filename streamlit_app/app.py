"""
Streamlit Web Interface - Unified Dashboard
Integrates all 3 backend projects (RAG, Ollama LLM, Semantic Search)
"""

import streamlit as st
import requests
from datetime import datetime
import json
from typing import Optional, Dict, List

# Page configuration
st.set_page_config(
    page_title="AI Backend Projects",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stTabs [role="tablist"] button {
        font-size: 16px;
        padding: 10px 20px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Configuration
RAG_API_URL = "http://localhost:8000"
OLLAMA_API_URL = "http://localhost:8001"
SEARCH_API_URL = "http://localhost:8002"

# Session state initialization
if "rag_session_id" not in st.session_state:
    st.session_state.rag_session_id = f"rag_{datetime.now().timestamp()}"

if "llm_session_id" not in st.session_state:
    st.session_state.llm_session_id = f"llm_{datetime.now().timestamp()}"

if "rag_messages" not in st.session_state:
    st.session_state.rag_messages = []

if "llm_messages" not in st.session_state:
    st.session_state.llm_messages = []

if "search_results" not in st.session_state:
    st.session_state.search_results = []

# Header
st.title("🤖 AI Backend Projects Dashboard")
st.markdown("""
Unified interface untuk 3 AI backend projects:
- **RAG Chat** - Retrieval-Augmented Generation dengan LangChain
- **Direct LLM** - Chat langsung dengan Ollama models
- **Semantic Search** - Document search dengan FAISS & embeddings
""")

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["🔍 RAG Chat", "💬 Direct LLM", "🔎 Semantic Search", "📊 Dashboard"])

# ============================================================================
# TAB 1: RAG CHAT
# ============================================================================
with tab1:
    st.header("RAG Chat - Document Q&A")
    st.markdown("Upload documents dan tanya dengan context dari dokumen tersebut")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📤 Upload Documents")
        uploaded_file = st.file_uploader(
            "Upload file (.txt)",
            type=["txt"],
            key="rag_uploader"
        )
        
        if uploaded_file is not None:
            with st.spinner("🔄 Indexing dokumen..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file, "text/plain")}
                    response = requests.post(
                        f"{RAG_API_URL}/rag/upload-documents",
                        files=files,
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"✅ {result['chunks_indexed']} chunks indexed!")
                        st.info(f"Total documents: {result['total_documents_loaded']}")
                    else:
                        st.error(f"❌ Error: {response.text}")
                
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to RAG backend. Make sure it's running on port 8000")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    with col2:
        st.subheader("📊 Status")
        try:
            response = requests.get(f"{RAG_API_URL}/rag/documents", timeout=5)
            if response.status_code == 200:
                data = response.json()
                st.metric("Documents Loaded", data["count"])
                if data["names"]:
                    st.write("**Files:**")
                    for name in data["names"]:
                        st.write(f"  • {name}")
            else:
                st.warning("⚠️ Could not fetch status")
        except:
            st.error("❌ RAG backend not running")
    
    # Chat interface
    st.subheader("💬 Chat")
    
    # Display chat messages
    for message in st.session_state.rag_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("📚 Sources"):
                    for source in message["sources"]:
                        st.write(f"• {source}")
    
    # Chat input
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input(
            "Ask a question:",
            placeholder="Type your question here...",
            key="rag_input"
        )
    with col2:
        send_button = st.button("Send", key="rag_send", use_container_width=True)
    
    if send_button and user_input:
        # Add user message
        st.session_state.rag_messages.append({
            "role": "user",
            "content": user_input
        })
        
        with st.chat_message("user"):
            st.write(user_input)
        
        # Query RAG backend
        with st.spinner("🔄 Thinking..."):
            try:
                response = requests.post(
                    f"{RAG_API_URL}/rag/query",
                    json={
                        "query": user_input,
                        "model": "mistral",
                        "k": 3
                    },
                    timeout=120
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.session_state.rag_messages.append({
                        "role": "assistant",
                        "content": result["answer"],
                        "sources": result["sources"]
                    })
                    
                    with st.chat_message("assistant"):
                        st.write(result["answer"])
                        with st.expander("📚 Sources"):
                            for source in result["sources"]:
                                st.write(f"• {source}")
                    
                    st.rerun()
                else:
                    st.error(f"❌ Error: {response.text}")
            
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to RAG backend")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # Clear history button
    if st.button("🗑️ Clear Chat History", key="rag_clear"):
        st.session_state.rag_messages = []
        st.rerun()

# ============================================================================
# TAB 2: DIRECT LLM CHAT
# ============================================================================
with tab2:
    st.header("Direct LLM Chat")
    st.markdown("Chat langsung dengan Ollama models tanpa document context")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("⚙️ Settings")
        model = st.selectbox(
            "Select Model:",
            ["mistral", "neural-chat", "llama2"],
            key="llm_model"
        )
        temperature = st.slider(
            "Temperature:",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            key="llm_temp"
        )
        top_p = st.slider(
            "Top P:",
            min_value=0.0,
            max_value=1.0,
            value=0.9,
            step=0.1,
            key="llm_topp"
        )
    
    with col2:
        st.subheader("📊 Status")
        try:
            response = requests.get(f"{OLLAMA_API_URL}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                status_color = "🟢" if data["ollama_running"] else "🔴"
                st.write(f"**Ollama:** {status_color} {data['status'].upper()}")
                st.write(f"**Active Sessions:** {data['active_sessions']}")
                st.write(f"**Available Models:** {', '.join(data['available_models'])}")
            else:
                st.warning("⚠️ Could not fetch status")
        except:
            st.error("❌ LLM backend not running")
    
    with col3:
        st.subheader("🎛️ Actions")
        if st.button("🔄 Refresh Models", key="llm_refresh"):
            try:
                response = requests.get(f"{OLLAMA_API_URL}/models", timeout=5)
                if response.status_code == 200:
                    st.success("✅ Models refreshed")
                else:
                    st.error("❌ Failed to refresh")
            except:
                st.error("❌ Connection error")
        
        if st.button("🗑️ Clear Chat", key="llm_clear"):
            st.session_state.llm_messages = []
            st.rerun()
    
    st.divider()
    
    # Chat interface
    st.subheader("💬 Chat")
    
    # Display chat messages
    for message in st.session_state.llm_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input(
            "Type your message:",
            placeholder="Ask anything...",
            key="llm_input"
        )
    with col2:
        send_button = st.button("Send", key="llm_send", use_container_width=True)
    
    if send_button and user_input:
        # Add user message
        st.session_state.llm_messages.append({
            "role": "user",
            "content": user_input
        })
        
        with st.chat_message("user"):
            st.write(user_input)
        
        # Query LLM backend
        with st.spinner("🔄 Thinking..."):
            try:
                response = requests.post(
                    f"{OLLAMA_API_URL}/chat",
                    json={
                        "message": user_input,
                        "model": model,
                        "session_id": st.session_state.llm_session_id,
                        "temperature": temperature,
                        "top_p": top_p
                    },
                    timeout=120
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.session_state.llm_messages.append({
                        "role": "assistant",
                        "content": result["response"]
                    })
                    
                    with st.chat_message("assistant"):
                        st.write(result["response"])
                    
                    st.rerun()
                else:
                    st.error(f"❌ Error: {response.text}")
            
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to LLM backend")
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timeout - model taking too long")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# ============================================================================
# TAB 3: SEMANTIC SEARCH
# ============================================================================
with tab3:
    st.header("Semantic Search Engine")
    st.markdown("Search documents menggunakan semantic similarity")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📤 Build Index")
        search_file = st.file_uploader(
            "Upload documents for indexing (.txt):",
            type=["txt"],
            key="search_uploader"
        )
        
        if search_file is not None:
            if st.button("🔨 Build Index", key="search_build"):
                with st.spinner("🔄 Building index..."):
                    try:
                        files = {"file": (search_file.name, search_file, "text/plain")}
                        response = requests.post(
                            f"{SEARCH_API_URL}/index/build",
                            files=files,
                            timeout=120
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.success(f"✅ Index built!")
                            st.info(
                                f"Documents: {result['documents_indexed']}\n"
                                f"Dimension: {result['embedding_dimension']}\n"
                                f"Model: {result['model']}"
                            )
                        else:
                            st.error(f"❌ Error: {response.text}")
                    
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Cannot connect to Search backend")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    with col2:
        st.subheader("📊 Index Info")
        try:
            response = requests.get(f"{SEARCH_API_URL}/index/info", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data["status"] == "ready":
                    st.success(f"✅ Index Status: {data['status'].upper()}")
                    st.metric("Total Documents", data["total_documents"])
                    st.metric("Index Dimension", data["index_dimension"])
                    st.write(f"**Model:** {data['model']}")
                else:
                    st.warning(f"⚠️ {data['message']}")
        except:
            st.error("❌ Search backend not running")
    
    st.divider()
    
    # Search interface
    st.subheader("🔎 Search")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        search_query = st.text_input(
            "Enter search query:",
            placeholder="Search for documents...",
            key="search_query"
        )
    with col2:
        search_button = st.button("Search", key="search_btn", use_container_width=True)
    
    top_k = st.slider(
        "Number of results:",
        min_value=1,
        max_value=10,
        value=5,
        key="search_topk"
    )
    
    if search_button and search_query:
        with st.spinner("🔄 Searching..."):
            try:
                response = requests.post(
                    f"{SEARCH_API_URL}/search",
                    json={
                        "query": search_query,
                        "top_k": top_k
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    results = response.json()
                    st.session_state.search_results = results["results"]
                    
                    st.success(f"Found {results['total_results']} results")
                    
                    for i, result in enumerate(results["results"], 1):
                        with st.expander(
                            f"📄 Result #{i} - Similarity: {result['score']:.2%}"
                        ):
                            st.write(result["doc"])
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Score", f"{result['score']:.4f}")
                            with col2:
                                st.metric("Index", result["index"])
                else:
                    st.error(f"❌ Error: {response.text}")
            
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to Search backend")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # Show previous results
    if st.session_state.search_results:
        st.subheader("📊 Previous Results")
        for i, result in enumerate(st.session_state.search_results, 1):
            with st.expander(f"Result #{i}"):
                st.write(result["doc"])

# ============================================================================
# TAB 4: DASHBOARD
# ============================================================================
with tab4:
    st.header("📊 System Dashboard")
    
    # Check all backends
    col1, col2, col3 = st.columns(3)
    
    # RAG Backend
    with col1:
        st.subheader("RAG Backend")
        try:
            response = requests.get(f"{RAG_API_URL}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                st.success("🟢 Online")
                st.write(f"**Status:** {data['status'].upper()}")
                st.write(f"**Model:** {data['embedding_model']}")
                st.write(f"**Documents:** {data['documents_loaded']}")
            else:
                st.error("🔴 Error")
        except:
            st.error("🔴 Offline")
            st.write("Run: `cd projects/01-rag-langchain-chroma && python main.py`")
    
    # LLM Backend
    with col2:
        st.subheader("Ollama LLM Backend")
        try:
            response = requests.get(f"{OLLAMA_API_URL}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                status_color = "🟢" if data["ollama_running"] else "🟡"
                st.write(f"{status_color} {data['status'].upper()}")
                if data["ollama_running"]:
                    st.success("Ollama Running")
                else:
                    st.warning("Ollama Not Running")
                st.write(f"**Sessions:** {data['active_sessions']}")
                st.write(f"**Models:** {', '.join(data['available_models'])}")
            else:
                st.error("🔴 Error")
        except:
            st.error("🔴 Offline")
            st.write("Run: `cd projects/02-ollama-integration && python main.py`")
    
    # Search Backend
    with col3:
        st.subheader("Semantic Search Backend")
        try:
            response = requests.get(f"{SEARCH_API_URL}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                st.success("🟢 Online")
                st.write(f"**Status:** {data['status'].upper()}")
                st.write(f"**Model:** {data['model']}")
                st.write(f"**Index Ready:** {'Yes' if data['index_ready'] else 'No'}")
            else:
                st.error("🔴 Error")
        except:
            st.error("🔴 Offline")
            st.write("Run: `cd projects/03-semantic-search && python main.py`")
    
    st.divider()
    
    # API Endpoints
    st.subheader("🔗 API Endpoints")
    
    endpoints_data = {
        "Service": [
            "RAG Backend",
            "LLM Backend",
            "Search Backend"
        ],
        "Base URL": [
            RAG_API_URL,
            OLLAMA_API_URL,
            SEARCH_API_URL
        ],
        "Port": ["8000", "8001", "8002"],
        "Docs": [
            f"{RAG_API_URL}/docs",
            f"{OLLAMA_API_URL}/docs",
            f"{SEARCH_API_URL}/docs"
        ]
    }
    
    st.dataframe(endpoints_data, use_container_width=True)
    
    st.divider()
    
    # Tech Stack
    st.subheader("🛠️ Tech Stack")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.write("**Backend**")
        st.write("- FastAPI")
        st.write("- Python")
        st.write("- Async/Await")
    
    with col2:
        st.write("**AI/ML**")
        st.write("- LangChain")
        st.write("- Ollama")
        st.write("- Hugging Face")
    
    with col3:
        st.write("**Vector DB**")
        st.write("- Chroma")
        st.write("- FAISS")
        st.write("- Embeddings")
    
    with col4:
        st.write("**Frontend**")
        st.write("- Streamlit")
        st.write("- Python")
        st.write("- REST API")
    
    st.divider()
    
    # Setup Instructions
    st.subheader("🚀 Quick Start")
    st.code("""
# Terminal 1: Ollama
ollama serve

# Terminal 2: RAG Backend
cd projects/01-rag-langchain-chroma
python main.py

# Terminal 3: LLM Backend
cd projects/02-ollama-integration
python main.py

# Terminal 4: Search Backend
cd projects/03-semantic-search
python main.py

# Terminal 5: Streamlit
cd streamlit_app
streamlit run app.py
    """, language="bash")
    
    st.markdown("""
    **Then open:** http://localhost:8501
    """)
    
    st.divider()
    
    # About
    st.subheader("ℹ️ About")
    st.markdown("""
    **AI Backend Projects - LLM Developer Intern Portfolio**
    
    This is a comprehensive portfolio project showcasing:
    - RAG implementation with LangChain
    - Vector database integration (Chroma, FAISS)
    - Ollama local LLM integration
    - REST API backend design
    - Streamlit web interface
    
    Built for FXMedia LLM Developer Intern position.
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p>Made with ❤️ for FXMedia | GitHub: github.com/wardaini/ai-backend-projects</p>
    </div>
    """, unsafe_allow_html=True)
