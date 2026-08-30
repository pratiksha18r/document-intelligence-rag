#--it creates the searchable memory of our RAG system.--#
# import faiss
# import numpy as np


# def create_vector_store(embeddings):
#     embeddings = np.array(embeddings).astype("float32")

#     dimension = embeddings.shape[1]

#     index = faiss.IndexFlatL2(dimension)

#     index.add(embeddings)

#     return index


# the above function only creates the FAISS index. Let's add a search function.
import faiss
import numpy as np
import json


def create_vector_store(embeddings):
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index


def search_vector_store(index, query_embedding, chunks, k=3):
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, k)

    results = []

    for distance, index_position in zip(distances[0], indices[0]):
        results.append({
            "text": chunks[index_position]["text"],
            "page_number": chunks[index_position]["page_number"],
            "distance": float(distance)
        })

    return results


def save_vector_store(index, chunks, folder_path):
    faiss.write_index(
        index,
        f"{folder_path}/index.faiss"
    )

    with open(
        f"{folder_path}/chunks.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(chunks, file, ensure_ascii=False, indent=2)


def load_vector_store(folder_path):
    index = faiss.read_index(
        f"{folder_path}/index.faiss"
    )

    with open(
        f"{folder_path}/chunks.json",
        "r",
        encoding="utf-8"
    ) as file:
        chunks = json.load(file)

    return index, chunks