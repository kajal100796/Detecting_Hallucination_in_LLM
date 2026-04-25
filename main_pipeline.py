import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pdf_processing.test_loader_extractor import extract_text_from_pdf
from text_processing.text_cleanandchunk import chunk_text
from embeddings.embedder import Embedder
from vector_store.faiss_store import FAISSStore
from Retrieval.Retriever import retrieve
from LLM.generator import generate_answer   # ✅ FIXED (lowercase)

def run_pipeline():
    print("=== STEP 1 & 2: PDF HANDLING & EXTRACTION ===")
    file_path = input("Enter the name of your PDF (e.g., pdf_processing/career_comparison_formatted.pdf): ").strip()
    
    if not os.path.exists(file_path):
        print(f"Error: Could not find file at {file_path}")
        return

    print("Extracting text...")
    raw_text = extract_text_from_pdf(file_path)

    print("\n=== STEP 3 & 4: TEXT CLEANING & CHUNKING ===")
    print("Creating 1000-character chunks with overlap...")
    final_chunks = chunk_text(raw_text, max_chars=1000, overlap=200)
    print(f"Total Chunks Created: {len(final_chunks)}")

    if len(final_chunks) == 0:
        print("No text could be extracted or chunked. Exiting.")
        return

    print("\n=== STEP 5: EMBEDDINGS ===")
    embedder = Embedder('all-MiniLM-L6-v2')
    embeddings = embedder.embed_chunks(final_chunks)

    print("\n=== STEP 6: VECTOR DATABASE (FAISS) ===")
    vector_store = FAISSStore(embedding_dim=384)
    vector_store.add_embeddings(embeddings, final_chunks)

    print("\n=== STEP 7: RETRIEVAL SYSTEM ===")
    user_question = input("\nEnter a question to search for: ").strip()
    
    print("\n=== OUTPUT: RELEVANT CHUNKS ===")
    top_chunks = retrieve(user_question, vector_store.index, final_chunks, top_k=3)

    # ✅ FIX: KEEP INSIDE FUNCTION
    context = " ".join(top_chunks)

    print("\n=== STEP 8: LLM ANSWER GENERATION ===")
    final_answer = generate_answer(user_question, context)

    print("\n=== FINAL ANSWER ===")
    print(final_answer)
    

    print("\n--- TOP RESULTS ---")
    seen = set()
    result_num = 1
    for chunk in top_chunks:
        if chunk not in seen:
            print(f"\nResult {result_num}:")
            print("-" * 60)
            print(chunk)
            print("-" * 60)
            seen.add(chunk)
            result_num += 1


if __name__ == "__main__":
    run_pipeline()
