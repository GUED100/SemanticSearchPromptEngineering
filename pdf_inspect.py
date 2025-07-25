import mimetypes
import requests
from config import PDF_URLS



for url in PDF_URLS:
    response = requests.get(url)
    print(f"{url.split("/")[-1]} ---> {response.headers["Content-Type"]}")  # Should be 'application/pdf'

#print(mimetypes.guess_type("file.pdf"))

#with open("file.pdf", "rb") as f:
#    print(f.read(20))
