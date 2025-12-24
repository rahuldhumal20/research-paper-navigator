from fastapi import APIRouter
from app.services.pdf_registry import load_pdfs

pdf_router = APIRouter()

@pdf_router.get("/pdfs")
def list_pdfs():
    return load_pdfs()
