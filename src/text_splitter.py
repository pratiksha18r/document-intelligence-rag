from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = []

    for document in documents:
        page_chunks = text_splitter.split_text(document["text"])

        for chunk in page_chunks:
            chunks.append({
                "page_number": document["page_number"],
                "text": chunk
            })

    return chunks