import pdfplumber
import os

def extract_chunks(filepath):
    chunks = []
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                for chunk in text.split("\n\n"):
                    if len(chunk.strip()) >= 50:
                        chunks.append(chunk.strip())
    return chunks
