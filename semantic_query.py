from weaviate_utils import init_client
import openai, os
from dotenv import load_dotenv
import logging

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = init_client()

def embed_query(text):
    if not text.strip():
        raise ValueError("The query text is empty.")
    
    logging.info("Embedding query: %s", text)

    # Use the OpenAI API to embed the query text
    response = openai.embeddings.create(
        input=[text],
        #model="text-embedding-ada-002",
        model="text-embedding-3-small",
    )
    
    embedding = response.data[0]
    # Convert to dict if needed
    if hasattr(embedding, "to_dict"):
        return embedding.to_dict()["embedding"]
    else:
        return embedding["embedding"]  # fallback for older versions    

    #return response.data[0].embedding
    #return response.data[0].to_dict()["embedding"]

def query_semantically(prompt):
    logging.info("Processing prompt: %s", prompt)

    try:
        if not prompt.strip():
            raise ValueError("The query prompt is empty.")
        
        vector = embed_query(prompt)
        results = client.query.get("Document", ["text", "source"]).with_near_vector({
            "vector": vector
        }).with_limit(5).do()

        print("\n🔍 Search Results:")
        for i, doc in enumerate(results["data"]["Get"]["Document"]):
            print(f"\n{i+1}. Source: {doc['source']}")
            print(f"   Snippet: {doc['text'][:200]}...")

    except Exception as e:
        logging.error("An error occurred during semantic search: %s", e)
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    query_text = input("Enter your semantic search query: ")
    query_semantically(query_text)
