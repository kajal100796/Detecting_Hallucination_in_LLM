"""
Module: Text Chunker
Purpose: Splits text into clean chunks at logical points (Paragraphs or Sentences).
"""


import re

def chunk_text(text, max_chars=500, overlap=50):
    """Splits text into chunks at logical points (Paragraphs, Sentences, or Spaces)."""
    chunks = []
    separators = ["\n\n", "\n", ". ", " "]
    current_pos = 0
    text_len = len(text)

    while current_pos < text_len:
        end_pos = min(current_pos + max_chars, text_len)
        if end_pos == text_len:
            chunks.append(text[current_pos:].strip())
            break
            
        chunk_slice = text[current_pos:end_pos]
        best_break = -1
        for sep in separators:
            found_idx = chunk_slice.rfind(sep)
            if found_idx != -1:
                best_break = found_idx + len(sep)
                break
        
        if best_break == -1:
            best_break = max_chars
            
        chunks.append(text[current_pos:current_pos + best_break].strip())
        current_pos += (best_break - overlap)
        
    return chunks

if __name__ == "__main__":
    
    sample_text = "This is a sample text " * 100 
    results = chunk_text(sample_text)
    print(f"Total chunks: {len(results)}")
    for i, chunk in enumerate(results[:3]):
        print(f"\nChunk {i+1}:\n{chunk}")
