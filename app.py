import streamlit as st

from src.vector_store import load_vector_store
from src.rag_pipeline import generate_answer


# Configuration

VECTOR_STORE_PATH = "data/vector_store"


# Page configuration

st.set_page_config(
    page_title="Document Intelligence RAG",
    page_icon="📚",
    layout="wide"
)


# Custom styling

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        margin-bottom: 30px;
    }

    .answer-box {
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-top: 10px;
    }

    .source-box {
        padding: 10px 15px;
        border-radius: 8px;
        border: 1px solid #ddd;
        margin-bottom: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# Header

st.markdown(
    '<div class="main-title">📚 Document Intelligence RAG</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Ask questions about your indexed PDF documents and receive '
    'answers grounded in the document.'
    '</div>',
    unsafe_allow_html=True
)

# Sidebar

with st.sidebar:

    st.header("📄 Document")

    st.write("**Indexed document:**")
    st.write("Unit 1.pdf")

    st.divider()

    st.header("⚙️ System")

    st.write("**Retrieval:** FAISS")
    st.write("**Embeddings:** all-MiniLM-L6-v2")
    st.write("**LLM:** GPT-OSS-20B via Groq")
    st.write("**Architecture:** RAG")

    st.divider()

    st.caption(
        "Answers are generated using retrieved "
        "document context."
    )


# Load vector store

@st.cache_resource
def load_data():
    return load_vector_store(VECTOR_STORE_PATH)


try:
    index, chunks = load_data()

except FileNotFoundError:
    st.error(
        "Vector store not found. "
        "Please run test_loader.py first to create it."
    )
    st.stop()


# Document statistics

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Indexed Chunks",
        len(chunks)
    )

with col2:

    st.metric(
        "Embedding Model",
        "MiniLM-L6-v2"
    )


st.divider()

# Question input

st.subheader("💬 Ask a question")

question = st.text_input(
    "Question",
    placeholder="e.g. What are the main challenges of IoT?",
    label_visibility="collapsed"
)



# Ask button

if st.button(
    "🔎 Ask Question",
    type="primary"
):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Searching the document and generating an answer..."
        ):

            answer, sources = generate_answer(
                question,
                index,
                chunks,
                k=3
            )


        # Answer
       
        st.subheader("💡 Answer")

        st.markdown(
            f'<div class="answer-box">{answer}</div>',
            unsafe_allow_html=True
        )


        # Sources
        
        st.subheader("📚 Sources")

        seen_pages = set()

        for source in sources:

                page = source["page_number"]

                if page not in seen_pages:

                    st.markdown(
                        f'<div class="source-box">📄 '
                        f'<strong>Page {page}</strong></div>',
                        unsafe_allow_html=True
                    )

                    seen_pages.add(page)