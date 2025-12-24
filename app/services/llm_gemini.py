import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def generate_answer(question: str, context_chunks: list[str]) -> str:
    context = "\n\n".join(context_chunks)

    prompt = f"""
You are a research assistant.
Answer only using the context below.

Context:
{context}

Question:
{question}
"""

    response = model.generate_content(prompt)
    return response.text
