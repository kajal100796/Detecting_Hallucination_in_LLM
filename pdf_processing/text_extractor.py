"""
Module: Text Extractor
Purpose: Extract text content from PDF files
"""

import pdfplumber
import os

def extract_text_from_pdf(pdf_path):
    text = ""

    if not os.path.exists(pdf_path):
        print("File not found!")
        return ""

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")

    return text


if __name__== "__main__":
    sample_file = input("Enter PDF file name: ")
    extracted_text = extract_text_from_pdf(sample_file)

    print("\nExtracted Text Preview:\n")
    print(extracted_text[:500] if extracted_text else "No text extracted")