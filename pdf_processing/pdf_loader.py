"""
Module: PDF Loader
Purpose: Load all PDF file paths from a folder
"""

import os

def load_pdfs(folder_path):
    pdf_files = []

    # Loop through all files in folder
    for file in os.listdir(folder_path):
        # Check if file is PDF
        if file.lower().endswith(".pdf"):
            full_path = os.path.join(folder_path, file)
            pdf_files.append(full_path)

    return pdf_files
if __name__ == "__main__":
    files = load_pdfs(".")
    print(files)