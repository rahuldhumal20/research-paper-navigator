from app.services.vector_store import search_documents
from app.services.graph_store import get_papers_by_author
import re

def agentic_answer(query: str):
    # 1️⃣ Always do semantic search
    vector_results = search_documents(query)

    # 2️⃣ Try to extract author name
    author_match = re.search(r"papers by ([A-Za-z ]+)", query, re.IGNORECASE)
    author = author_match.group(1).strip() if author_match else None

    graph_results = []
    if author:
        graph_results = get_papers_by_author(author)

    # 3️⃣ Decide response type
    if graph_results:
        return {
            "type": "graph",
            "author": author,
            "papers": graph_results
        }

    # 4️⃣ Always return semantic (fallback)
    return {
        "type": "vector",
        "results": vector_results
    }
