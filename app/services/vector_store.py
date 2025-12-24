import chromadb
from chromadb.utils import embedding_functions

PERSIST_DIR = "data/chroma"

# Local embedding model
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# ✅ Correct way in new ChromaDB
client = chromadb.PersistentClient(
    path=PERSIST_DIR
)

collection = client.get_or_create_collection(
    name="research_papers",
    embedding_function=embedding_function
)

def add_document(doc_id, text):
    collection.add(
        documents=[text],
        ids=[doc_id]
    )

def search_documents(query, n_results=3):
    return collection.query(
        query_texts=[query],
        n_results=n_results
    )
