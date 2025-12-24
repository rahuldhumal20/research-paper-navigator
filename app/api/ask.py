from fastapi import APIRouter, Query
from app.services.agent import agentic_answer

ask_router = APIRouter()

@ask_router.get("/ask")
def ask(query: str = Query(...)):
    return agentic_answer(query)
