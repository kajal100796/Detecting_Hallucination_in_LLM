import os
from pdf_processing.test_loader_extractor import extract_text_from_pdf
from text_processing.text_cleanandchunk import chunk_text



def run():
    print("=== UNIVERSITY RAG PROJECT: PDF PROCESSOR ===")

    # User Input
    file_path = input("Enter the name of your PDF (e.g., paper.pdf): ").strip()

    if os.path.exists(file_path):
        # Extract
        print("Extracting text...")
        raw_text = extract_text_from_pdf(file_path)

        #Chunk (1000 chars)
        print("Creating 1000-character chunks...")
        final_chunks = chunk_text(raw_text, max_chars=1000, overlap=200)

        print(f"\nSuccessfully processed!")
        print(f"Total Chunks Created: {len(final_chunks)}")
        
        # print a TINY bit to prevent freezing
        if len(final_chunks) > 0:
            print(f"Preview (Chunk 1): {final_chunks[0][:100]}...")
            
        print("Ready for Embeddings: Yes")
    else:
        print(f"Error: Could not find file at {file_path}")

if __name__ == "__main__":
    run()