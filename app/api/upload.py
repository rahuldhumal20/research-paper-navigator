from fastapi import APIRouter, UploadFile, File
from pypdf import PdfReader
import uuid, re
from app.services.vector_store import add_document
from app.services.pdf_registry import add_pdf
from app.services.graph_store import add_paper

upload_router = APIRouter()

@upload_router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    reader = PdfReader(file.file)
    full_text = ""

    for page in reader.pages:
        full_text += page.extract_text() or ""

    # 🔹 Auto-extract author (simple heuristic)
    author_match = re.search(r"Author[s]?:\s*(.+)", full_text, re.IGNORECASE)
    author = author_match.group(1).strip() if author_match else "Unknown"

    chunk_size = 500
    chunks = [
        full_text[i:i + chunk_size]
        for i in range(0, len(full_text), chunk_size)
    ]

    for chunk in chunks:
        doc_id = f"{file.filename}_{uuid.uuid4()}"
        add_document(doc_id, chunk)

    # Add to Neo4j
    add_paper(file.filename, author)

    # Save registry
    add_pdf(file.filename, len(chunks))

    return {
        "status": "success",
        "filename": file.filename,
        "author": author,
        "chunks_added": len(chunks)
    }
