"""
Module: Test Pipeline
Purpose: Combine PDF Loader + Text Extractor
"""
import pdfplumber

def extract_text_from_pdf(pdf_path):
    """Opens a local PDF and returns all text."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading file: {e}")
    
    return text

if __name__ == "__main__":
    print("--- Extracted Text Preview ---")
    
    
    filename = "career_comparison_formatted.pdf"
    
    test_text = extract_text_from_pdf(filename)
    
    # Printing first 1000 characters 
    print(test_text[:1000])