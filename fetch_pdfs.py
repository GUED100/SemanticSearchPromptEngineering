import requests
import os
from config import PDF_URLS

def is_pdf(url):
    response = requests.get(url, stream=True)
    content_type = response.headers.get("Content-Type", "")
    return "application/pdf" in content_type.lower()

def download_pdfs(folder="pdfs"):
    os.makedirs(folder, exist_ok=True)
    for url in PDF_URLS:
        if not is_pdf(url):
            print(f"❌ Skipped (not a real PDF): {url}")
            continue        
        filename = url.split("/")[-1]
        filepath = os.path.join(folder, filename)
        response = requests.get(url)
        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"✅ Downloaded: {filename}")


if __name__ == "__main__":
    download_pdfs()
