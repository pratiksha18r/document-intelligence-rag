#--For testing purposes, you can use the following code snippet to load a PDF document and split it into chunks --#
# from src.document_loader import load_pdf


# pdf_path = "data/documents/Unit 1.pdf"

# documents = load_pdf(pdf_path)

# print(f"Number of pages loaded: {len(documents)}")

# for document in documents[:2]:
#     print("\n--- Page", document["page_number"], "---")
#     print(document["text"][:1000])


#-- to test the chunking,  uncomment the following lines to see the length of each chunk and the overlap between chunks --#
# from src.document_loader import load_pdf
# from src.text_splitter import split_documents


# pdf_path = "data/documents/Unit 1.pdf"

# documents = load_pdf(pdf_path)

# chunks = split_documents(documents)

# print(f"Number of pages loaded: {len(documents)}")
# print(f"Number of chunks created: {len(chunks)}")

# for i, chunk in enumerate(chunks[:3], start=1):
#     print(f"\n--- Chunk {i} ---")
#     print(f"Page: {chunk['page_number']}")
#     print(chunk["text"])


    #-- to test sentence-Transformers --#
# from src.document_loader import load_pdf
# from src.text_splitter import split_documents
# from src.embeddings import create_embeddings


# pdf_path = "data/documents/Unit 1.pdf"

# documents = load_pdf(pdf_path)
# chunks = split_documents(documents)

# texts = [chunk["text"] for chunk in chunks[:3]]

# embeddings = create_embeddings(texts)

# print(f"Number of chunks embedded: {len(embeddings)}")
# print(f"Dimensions of each embedding: {len(embeddings[0])}")
# print(f"\nFirst embedding:\n{embeddings[0]}")


#--test semantic search--#

# import numpy as np
# from src.document_loader import load_pdf
# from src.text_splitter import split_documents
# from src.embeddings import create_embeddings
# from src.vector_store import create_vector_store


# pdf_path = "data/documents/Unit 1.pdf"

# # 1. Load PDF
# documents = load_pdf(pdf_path)

# # 2. Split into chunks
# chunks = split_documents(documents)

# # 3. Create embeddings
# texts = [chunk["text"] for chunk in chunks]
# embeddings = create_embeddings(texts)

# # 4. Create vector store
# index = create_vector_store(embeddings)

# print(f"Number of chunks: {len(chunks)}")
# print(f"Vector dimension: {embeddings.shape[1]}")

# # 5. Create embedding for our search question
# question = "What is the Internet of Things?"

# question_embedding = create_embeddings([question])

# # 6. Search for the 3 most relevant chunks
# distances, indices = index.search(
#     np.array(question_embedding).astype("float32"),
#     3
# )

# print("\nTop 3 relevant chunks:\n")

# for rank, index_position in enumerate(indices[0], start=1):
#     chunk = chunks[index_position]

#     print(f"--- Result {rank} ---")
#     print(f"Page: {chunk['page_number']}")
#     print(f"Distance: {distances[0][rank - 1]}")
#     print(chunk["text"][:500])
#     print()


#Test the complete RAG pipeline
import os

from src.document_loader import load_pdf
from src.text_splitter import split_documents
from src.embeddings import create_embeddings
from src.vector_store import (
    create_vector_store,
    save_vector_store,
    load_vector_store
)
from src.rag_pipeline import generate_answer


pdf_path = "data/documents/Unit 1.pdf"
vector_store_path = "data/vector_store"


# ==========================================
# STEP 1: Process the PDF
# ==========================================

documents = load_pdf(pdf_path)

chunks = split_documents(documents)

texts = [chunk["text"] for chunk in chunks]

embeddings = create_embeddings(texts)


# ==========================================
# STEP 2: Create FAISS vector store
# ==========================================

index = create_vector_store(embeddings)

print(f"Number of chunks: {len(chunks)}")
print(f"Vector dimension: {embeddings.shape[1]}")


# ==========================================
# STEP 3: Save vector store
# ==========================================

save_vector_store(
    index,
    chunks,
    vector_store_path
)

print("\nVector store saved successfully.")


# ==========================================
# STEP 4: Load vector store
# ==========================================

loaded_index, loaded_chunks = load_vector_store(
    vector_store_path
)

print("Vector store loaded successfully.")


# ==========================================
# STEP 5: Ask a question
# ==========================================

question = "How do airplanes fly?"


answer, sources = generate_answer(
    question,
    loaded_index,
    loaded_chunks,
    k=3
)


# ==========================================
# STEP 6: Display answer
# ==========================================

print("\n==============================")
print("QUESTION")
print("==============================")

print(question)


print("\n==============================")
print("ANSWER")
print("==============================")

print(answer)


print("\n==============================")
print("SOURCES")
print("==============================")

for source in sources:
    print(
        f"Page {source['page_number']} "
        f"(distance: {source['distance']:.4f})"
    )