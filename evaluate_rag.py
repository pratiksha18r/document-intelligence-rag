from src.vector_store import load_vector_store
from src.rag_pipeline import generate_answer



# Configuration

VECTOR_STORE_PATH = "data/vector_store"


# Evaluation questions

evaluation_questions = [
    {
        "question": "What is the Internet of Things?",
        "expected": "answer"
    },
    {
        "question": "What are the main challenges of IoT?",
        "expected": "answer"
    },
    {
        "question": "How is IoT used in smart grids?",
        "expected": "answer"
    },
    {
        "question": "What is GPS used for in smartphones?",
        "expected": "answer"
    },
    {
        "question": "How do airplanes fly?",
        "expected": "refuse"
    },
    {
        "question": "What is photosynthesis?",
        "expected": "refuse"
    }
]



# Load persistent vector store

index, chunks = load_vector_store(
    VECTOR_STORE_PATH
)


# Run evaluation

passed = 0

print("\n========================================")
print("RAG EVALUATION")
print("========================================")


for number, item in enumerate(
    evaluation_questions,
    start=1
):

    question = item["question"]
    expected = item["expected"]

    answer, sources = generate_answer(
        question,
        index,
        chunks,
        k=3
    )

    # Determine whether the system answered
    # or correctly refused.
    if "couldn't find the answer" in answer.lower():

        actual = "refuse"

    else:

        actual = "answer"


    # Compare actual vs expected
    if actual == expected:

        status = "PASS"
        passed += 1

    else:

        status = "FAIL"


    print(f"\n{number}. {question}")
    print(f"   Expected: {expected.upper()}")
    print(f"   Result:   {actual.upper()}")
    print(f"   Status:   {status}")


# Final result

total = len(evaluation_questions)

print("\n========================================")
print(f"RESULT: {passed}/{total} PASS")
print("========================================")