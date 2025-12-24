import os

provider = os.getenv("LLM_PROVIDER")

if provider == "openai":
    from app.services.llm_openai import generate_answer
elif provider == "gemini":
    from app.services.llm_gemini import generate_answer
else:
    raise ValueError("Invalid LLM_PROVIDER")
