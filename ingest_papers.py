import os
from app.services.pdf_loader import load_pdf_text
from app.services.text_splitter import split_text
from app.services.vector_store import add_document

PAPERS_DIR = "data/papers"

for filename in os.listdir(PAPERS_DIR):
    if filename.endswith(".pdf"):
        file_path = os.path.join(PAPERS_DIR, filename)

        print(f"Reading {filename}...")
        text = load_pdf_text(file_path)

        chunks = split_text(text)

        for i, chunk in enumerate(chunks):
            doc_id = f"{filename}_{i}"
            add_document(doc_id, chunk)

        print(f"Ingested {filename} with {len(chunks)} chunks\n")
