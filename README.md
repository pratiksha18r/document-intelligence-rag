# 📚 Document Intelligence RAG

A document-grounded question-answering application built with Retrieval-Augmented Generation (RAG). It allows users to ask questions about indexed PDF documents and receive answers grounded in the document content.

## 🎯 Project Overview

Large documents can contain useful information that is difficult to find manually.

This project provides a simple way to ask natural-language questions about a document and receive an answer based onldocument-y on the information available in that document.

The application:

- Extracts text from PDF documents
- Splits documents into smaller chunks
- Generates semantic embeddings
- Stores embeddings using FAISS
- Retrieves the most relevant document chunks
- Sends retrieved context to an LLM through the Groq API
- Generates document-grounded answers
- Displays relevant source pages
- Refuses to answer when the requested information is not found in the document

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
              Sentence Transformers
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
                         ▼
                  User Question
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

                   ---

## 📸 Application Screenshots

### Document-Grounded Answer

The application retrieves relevant information from the indexed document and generates a grounded answer using the Groq API.

![RAG Answer](screenshots/rag-answer.png)

### Out-of-Document Question

The system refuses to answer when the requested information is not available in the indexed document.

![Out-of-Document Question](screenshots/out-of-document.png)