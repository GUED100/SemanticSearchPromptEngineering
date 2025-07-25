---
title: Semantic Prompt Search
emoji: 🔍
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: "1.46.0"
app_file: app.py
pinned: false
---

# 🔍 Semantic Prompt Search

This is a Hugging Face Space powered by **Streamlit** that enables semantic search across a collection of PDFs focused on **Prompt Engineering**. It uses NLP embeddings to provide intelligent, context-aware results beyond keyword matching.

## 🧠 What It Does

- Upload or explore curated Prompt Engineering PDFs
- Perform **semantic similarity-based search**
- View contextual snippets and document matches
- Optionally fine-tune with custom query filters or embeddings

## 🚀 How It Works

This app processes PDF content using an NLP pipeline that extracts and embeds semantic information. It then indexes the embeddings to power fast and flexible search queries. Built with:

- 🐍 Python + Streamlit for the UI
- 📚 SentenceTransformers / Hugging Face models for embeddings
- 🗃️ Weavite for vector indexing

## ⚙️ Setup & Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
