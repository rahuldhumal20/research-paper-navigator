# 🔍 Research Paper Navigator – Agentic RAG System

An intelligent research assistant that enables semantic and graph-based exploration of research papers using an Agentic RAG architecture.

## 🚀 Features
- Upload and ingest research papers (PDF)
- Semantic search using vector embeddings (ChromaDB)
- Graph-based author–paper queries (Neo4j)
- Interactive React UI with upload progress and document management
- FastAPI backend with modular services

## 🛠 Tech Stack
- Frontend: React (Vite)
- Backend: FastAPI
- Vector Database: ChromaDB
- Graph Database: Neo4j
- Language: Python, JavaScript

## ⚙️ Architecture
React UI → FastAPI → ChromaDB (Semantic Search)  
                     → Neo4j (Graph Queries)

## ▶️ How to Run Locally

### Backend

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

### Backend

npm install
npm run dev

Open: http://localhost:5173

## 📌 Example Queries

Explain MapReduce

Papers by Vaswani

What problem does this paper solve?

## 📈 Future Enhancements

LLM-based answer generation

Graph visualization

User authentication

Cloud deployment