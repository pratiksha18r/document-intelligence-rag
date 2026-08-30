# 📚 Document Intelligence RAG

A document-grounded question-answering application that uses Retrieval-Augmented Generation (RAG) to answer questions from indexed PDF documents.

The system combines semantic search with an LLM to retrieve relevant document content and generate answers grounded in the provided documents.

---

## 🎯 Project Overview

Large documents can contain useful information that is difficult to find manually.

This project provides a simple way to ask natural-language questions about a document and receive an answer based only on the information available in that document.

The application:

- Extracts text from PDF documents
- Splits documents into smaller chunks
- Generates semantic embeddings
- Stores embeddings using FAISS
- Retrieves the most relevant document chunks
- Sends retrieved context to an LLM through the Groq API
- Generates document-grounded answers
- Displays the source pages used for the answer
- Refuses to answer when the requested information is not found in the document

---

## 🏗️ Architecture

```text
                    PDF DOCUMENT
                         │
                         ▼
                ┌─────────────────┐
                │ Document Loader │
                └────────┬────────┘
                         │
                         ▼
                   Text Chunking
                         │
                         ▼
                Sentence Transformer
                  Embeddings
                         │
                         ▼
                ┌─────────────────┐
                │      FAISS      │
                │  Vector Store   │
                └────────┬────────┘
                         │
                         ▼
                  Persistent Store
                  index.faiss
                  chunks.json
                         │
                         │
              ┌──────────▼──────────┐
              │    User Question    │
              └──────────┬──────────┘
                         │
                         ▼
                  Query Embedding
                         │
                         ▼
                    FAISS Search
                         │
                         ▼
                 Top-k Relevant
                    Chunks
                         │
                         ▼
                 ┌──────────────┐
                 │   Groq API   │
                 │  GPT-OSS-20B │
                 └──────┬───────┘
                        │
                        ▼
                Grounded Answer
                        │
                        ▼
                  Streamlit UI