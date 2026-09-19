import docx
import json

def extract_evaluation(filename):
    doc = docx.Document(filename)
    questions = []
    current_question = None

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        
        # Determine if paragraph is a question or an option
        # Questions usually start with a number or just have a different format
        # Let's just collect all text and see its formatting
        runs = []
        is_bold = False
        for run in para.runs:
            if run.text.strip():
                runs.append({"text": run.text, "bold": run.bold})
                if run.bold:
                    is_bold = True
        
        print(f"TEXT: {text}")
        print(f"RUNS: {runs}")
        print("---")

extract_evaluation("EVALUACIÓN MODULAR 1.docx")
