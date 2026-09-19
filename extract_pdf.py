import sys
import subprocess

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("PyMuPDF")

import fitz  # PyMuPDF

def extract_pdf():
    pdf_path = "PROTOCOLOS_PERÚ_FIBRA.pptx 28.08.pdf"
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
        text += "\n---PAGE_BREAK---\n"
    
    with open("pdf_text_dump.txt", "w", encoding="utf-8") as f:
        f.write(text)
        
if __name__ == "__main__":
    extract_pdf()
