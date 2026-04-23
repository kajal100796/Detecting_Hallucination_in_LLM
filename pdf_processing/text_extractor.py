"""
Module: Text Extractor
Purpose: Extract text from PDF files
"""

import pdfplumber


def extract_text_from_pdf(pdf_path):
    text = ""

    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Loop through all pages
            for page in pdf.pages:
                page_text = page.extract_text()
                
                if page_text:  # avoid None
                    text += page_text

    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")

    return text


# Testing block
if __name__ == "__main__":
    sample_file = "hallucinations rspaper.pdf"  # actual file name
    extracted_text = extract_text_from_pdf(sample_file)

    print("Extracted Text:\n")
    print(extracted_text[:500])  # first 500 charactors