from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.ask import ask_router
from app.api.upload import upload_router
from fastapi import APIRouter
from app.services.pdf_registry import load_pdfs
from app.api.delete import delete_router

pdf_router = APIRouter()

@pdf_router.get("/pdfs")
def list_pdfs():
    return load_pdfs()


app = FastAPI(title="Research Paper Navigator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
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
