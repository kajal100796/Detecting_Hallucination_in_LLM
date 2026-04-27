import os
import sys

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pdf_processing.test_loader_extractor import extract_text_from_pdf
from text_processing.text_cleanandchunk import chunk_text
from embeddings.embedder import Embedder
from vector_store.faiss_store import FAISSStore
from Retrieval.Retriever import retrieve
from LLM.generator import generate_answer
from evaluation.hallucination_detector import detect_hallucination


def run_pipeline():
    print("=== STEP 1 & 2: PDF HANDLING & EXTRACTION ===")
    
    file_path = input("Enter PDF path (e.g., pdf_processing/sample.pdf): ").strip()

    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    print("\nExtracting text...")
    raw_text = extract_text_from_pdf(file_path)

    # ----------------------------------------
    print("\n=== STEP 3 & 4: TEXT CLEANING & CHUNKING ===")
    final_chunks = chunk_text(raw_text, max_chars=1000, overlap=200)
    print(f"Total Chunks Created: {len(final_chunks)}")

    if len(final_chunks) == 0:
        print("No chunks created. Exiting.")
        return

    # ----------------------------------------
    print("\n=== STEP 5: EMBEDDINGS ===")
    embedder = Embedder('all-MiniLM-L6-v2')
    embeddings = embedder.embed_chunks(final_chunks)

    # ----------------------------------------
    print("\n=== STEP 6: VECTOR DATABASE (FAISS) ===")
    vector_store = FAISSStore(embedding_dim=384)
    vector_store.add_embeddings(embeddings, final_chunks)

    # ----------------------------------------
    print("\n=== STEP 7: RETRIEVAL SYSTEM ===")
    user_question = input("\nEnter your question: ").strip()

    print("\n=== OUTPUT: RELEVANT CHUNKS ===")
    top_chunks = retrieve(user_question, vector_store.index, final_chunks, top_k=3)

    # Combine retrieved chunks
    context = " ".join(top_chunks)

    # ----------------------------------------
    print("\n=== STEP 8: LLM ANSWER GENERATION ===")
    final_answer = generate_answer(user_question, context)

    print("\n=== FINAL ANSWER ===")
    print(final_answer)

    # ----------------------------------------
    print("\n=== STEP 9: HALLUCINATION DETECTION ===")

    result = detect_hallucination(user_question, context, final_answer)

    print("Confidence Score:", round(result["confidence_score"], 2))
    print("Status:", result["label"])

    # ----------------------------------------
    print("\n=== TOP RETRIEVED CHUNKS ===")
    seen = set()
    count = 1

    for chunk in top_chunks:
        if chunk not in seen:
            print(f"\nResult {count}:")
            print("-" * 60)
            print(chunk)
            print("-" * 60)
            seen.add(chunk)
            count += 1


if __name__ == "__main__":
    run_pipeline()
