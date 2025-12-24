import os
import json

REGISTRY_FILE = "data/pdfs.json"

os.makedirs("data", exist_ok=True)

def load_pdfs():
    if not os.path.exists(REGISTRY_FILE):
        return []
    with open(REGISTRY_FILE, "r") as f:
        return json.load(f)

def save_pdfs(pdfs):
    with open(REGISTRY_FILE, "w") as f:
        json.dump(pdfs, f, indent=2)

def add_pdf(filename, chunks):
    pdfs = load_pdfs()
    pdfs.append({
        "filename": filename,
        "chunks": chunks
    })
    save_pdfs(pdfs)

def remove_pdf(filename):
    pdfs = load_pdfs()
    pdfs = [p for p in pdfs if p["filename"] != filename]
    save_pdfs(pdfs)
