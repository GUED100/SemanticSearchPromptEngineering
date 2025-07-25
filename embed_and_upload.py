import openai, os
from dotenv import load_dotenv
from extract_chunks import extract_chunks
from weaviate_utils import init_client
from config import SCHEMA_CONFIG
import numpy as np
import logging
import uuid
import hashlib


load_dotenv()

def get_deterministic_uuid(text):
    hash = hashlib.md5(text.encode("utf-8")).hexdigest()
    return str(uuid.UUID(hash))

openai.api_key = os.getenv("OPENAI_API_KEY")
client = init_client()

# Create schema if not exists
if not client.schema.contains(SCHEMA_CONFIG):
    client.schema.create_class(SCHEMA_CONFIG)

def embed(text):
    response = openai.embeddings.create(
        input=[text],
        encoding_format= "float",
        #model="text-embedding-ada-002",
        model="text-embedding-3-small",
    )
    #return response["data"][0]["embedding"]
    #return[d.embedding for d in response.data]
    return  response.data[0].embedding
    #vec = response.data[0].embedding
    #return np.array(vec, dtype=np.float32).tolist()    

def process_pdf(file_path):
    logging.info("Processing file: %s", file_path)
    try:
        source_name = os.path.basename(file_path)
        chunks = extract_chunks(file_path)
        for chunk in chunks:
            logging.info("Processing chunk: %s", chunk[:30])  # Log the first 30 characters of the chunk
            vector = embed(chunk)
            if isinstance(vector, list):
                # Convert to a format expected by the API if necessary
                # E.g., if the API expects a single float array
                vector = [float(v) for v in vector]  # Ensure all elements are float
                if len(vector) == 0:
                    raise ValueError("The generated vector is empty.")
            
            logging.info("Vector data being sent: %s", vector)

            #first check if the object already exists
            existing_objects = client.query.get("Document", []).with_additional(["id"]).with_where({
            "path": ["source"],
            "operator": "Equal",
            "valueText": source_name
            }).with_limit(5).do()
            if existing_objects["data"]["Get"]["Document"]:
                logging.info("Object already exists, skipping creation.")
                continue

            data_object = {
                "text": chunk,
                "source": source_name
            }

            #client.data_object.create(data_object, "Document", vector=vector)
            client.data_object.create(data_object, class_name="Document", vector=vector, uuid=get_deterministic_uuid(chunk))

    except Exception as e:
        logging.error("An error occurred: %s", e)

if __name__ == "__main__":
    folder = "pdfs"
    for fname in os.listdir(folder):
        if fname.endswith(".pdf"):
            print(f"🔗 Processing: {fname}")
            process_pdf(os.path.join(folder, fname))
