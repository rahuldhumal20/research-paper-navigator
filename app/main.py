from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.api.ask import ask_router
from app.api.upload import upload_router
from app.api.delete import delete_router
from app.services.pdf_registry import load_pdfs

pdf_router = APIRouter()

@pdf_router.get("/pdfs")
def list_pdfs():
    return load_pdfs()

app = FastAPI(title="Research Paper Navigator")

# ✅ CORS FIX (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allows web + mobile + deployed frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ask_router)
app.include_router(upload_router)
app.include_router(pdf_router)
app.include_router(delete_router)

@app.get("/")
def root():
    return {"status": "API running"}
