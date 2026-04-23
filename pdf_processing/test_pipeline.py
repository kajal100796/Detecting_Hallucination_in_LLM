"""
Module: Test Pipeline
Purpose: Combine PDF Loader + Text Extractor
"""


from pdf_loader import load_pdfs
from text_extractor import extract_text_from_pdf

def run_pipeline():
    # Step 1: Load PDFs from the current directory
    pdf_files = load_pdfs(".")

    print("PDF Files Found:\n", pdf_files)

    # Step 2: Extract text from each PDF
    for pdf in pdf_files:
        print("\n" + "="*50)
        print(f"Processing: {pdf}")

        try:
            text = extract_text_from_pdf(pdf)
            
            # Print only first 300 characters
            print("Extracted Text Preview:\n")
            print(text[:300])
        except Exception as e:
            print(f"Error processing {pdf}: {e}")

# Fixed the syntax here: Double underscores are required
if __name__ == "__main__":
    run_pipeline()