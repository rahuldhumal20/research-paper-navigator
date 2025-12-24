from fastapi import APIRouter
from app.services.pdf_registry import remove_pdf
from app.services.vector_store import collection

delete_router = APIRouter()

@delete_router.delete("/delete/{filename}")
def delete_pdf(filename: str):
    # Remove vectors
    collection.delete(where={"source": filename})

    # Remove metadata
    remove_pdf(filename)

    return {"status": "deleted", "filename": filename}
