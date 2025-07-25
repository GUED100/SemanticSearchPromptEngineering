import weaviate
import os
from dotenv import load_dotenv

load_dotenv()

def init_client():
    return weaviate.Client(
        url=os.getenv("WEAVIATE_URL"),
        auth_client_secret=weaviate.AuthApiKey(os.getenv("WEAVIATE_API_KEY")),
        additional_headers={"X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")}
    )
