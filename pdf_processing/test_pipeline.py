from pdf_processing.pdf_loader import load_pdfs
from pdf_processing.text_extractor import extract_text_from_pdf


def run_pipeline():
    # Step 1: Load all PDFs
    pdf_files = load_pdfs(".")

    print("PDFs found:", pdf_files)

    # Step 2: Extract text from each PDF
    for pdf in pdf_files:
        print(f"\nProcessing: {pdf}")
        text = extract_text_from_pdf(pdf)

        print("Extracted text (first 200 chars):")
        print(text[:200])


if __name__ == "_main_":
    run_pipeline()