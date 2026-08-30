import os

from dotenv import load_dotenv
from groq import Groq

from src.embeddings import create_embeddings
from src.vector_store import search_vector_store


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(question, index, chunks, k=3):

    # Create embedding for the user's question
    question_embedding = create_embeddings([question])

    # Retrieve relevant chunks
    results = search_vector_store(
        index,
        question_embedding,
        chunks,
        k=k
    )

    # Build context from retrieved chunks
    context_parts = []

    for result in results:
        context_parts.append(
            f"[Page {result['page_number']}]\n{result['text']}"
        )

    context = "\n\n".join(context_parts)

    # Create prompt for the LLM
    prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the information provided
in the document context below.

If the answer cannot be found in the context, say:
"I couldn't find the answer in the provided document."

Do not use outside knowledge.

Document context:
{context}

User question:
{question}
"""

    # Send context + question to Groq
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response.choices[0].message.content
     # If the answer is not available in the document,
    # don't show retrieved chunks as supporting sources.
    if answer == "I couldn't find the answer in the provided document.":
        return answer, []

    return answer, results