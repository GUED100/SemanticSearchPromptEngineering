import streamlit as st
import os
import openai
from weaviate_utils import init_client
from dotenv import load_dotenv
from functools import lru_cache
import pickle
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# OpenAI setup
openai.api_key = os.getenv("OPENAI_API_KEY")

# Weaviate client
client = init_client()

# 🔐 Authentication
def check_password():
    def login_form():
        with st.form("Login"):
            st.write("🔒 Login Required")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                if username == st.secrets["STREAMLIT_USERNAME"] and password == st.secrets["STREAMLIT_PASSWORD"]:
                    st.session_state["logged_in"] = True
                    logging.info(f"✅ Correctly logged as {username}")
                    print(f"Correctly logged as {username}")
                else:
                    st.session_state["logged_in"] = False
                    logging.warning("❌ Login failed")
                    st.error("Incorrect username or password")

    if "logged_in" not in st.session_state:
        login_form()
    

    return st.session_state.get("logged_in", False)

# 🧠 Embed query with caching
@lru_cache(maxsize=128)
def embed_query(text):
    response = openai.embeddings.create(
        input=[text],
        model="text-embedding-3-small",
    )
    embedding = response.data[0]
    if hasattr(embedding, "to_dict"):
        return embedding.to_dict()["embedding"]
    else:
        return embedding["embedding"]

# 💾 Optional embedding cache (not used actively here)
def cache_query_embedding(text, vector):
    with open(f"cache/{text[:50]}.pkl", "wb") as f:
        pickle.dump(vector, f)

# 🔍 Semantic search
def semantic_search(query_text):
    vector = embed_query(query_text)
    result = client.query.get("Document", ["text", "source"]).with_near_vector({
        "vector": vector
    }).with_limit(5).do()

    return result["data"]["Get"]["Document"]

# 🚪 Gate access before main app
if check_password():
     # 🚀 Your actual app starts here
    st.set_page_config(page_title="Prompt Search", layout="wide")
    st.title("🔍 Semantic Search over Prompt Engineering PDFs")

    query = st.text_input("Enter your search prompt:")

    if query:
        with st.spinner("Searching..."):
            try:
                docs = semantic_search(query)
                for i, doc in enumerate(docs):
                    st.markdown(f"**{i+1}. Source:** `{doc['source']}`")
                    st.markdown(f"> {doc['text'][:500]}...")
                    st.markdown("---")
            except Exception as e:
                st.error(f"An error occurred: {e}")
else:
    st.stop()