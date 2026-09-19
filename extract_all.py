import docx
import json
import os
import re

def extract_evaluation(filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return None
    
    doc = docx.Document(filename)
    questions = []
    current_question = None

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        
        # Check if text is a question (starts with number and dot/hyphen)
        if re.match(r'^\d+[\.\-]', text) or "?" in text or "¿" in text:
            if current_question and current_question["options"]:
                questions.append(current_question)
            current_question = {
                "question": text,
                "options": [],
                "correctIndex": -1
            }
        elif current_question:
            # Check if it's an option (starts with A), B), a., etc.)
            if re.match(r'^[A-Ea-e][\.\)]', text):
                is_bold = any(run.bold for run in para.runs if run.text.strip())
                current_question["options"].append(text)
                if is_bold:
                    current_question["correctIndex"] = len(current_question["options"]) - 1
            else:
                # Append to current question text if not an option
                if not current_question["options"]:
                    current_question["question"] += " " + text
                    
    if current_question and current_question["options"]:
        questions.append(current_question)
        
    return questions

all_evaluations = {}
for i in range(1, 5):
    filename = f"EVALUACIÓN MODULAR {i}.docx"
    print(f"Extracting {filename}...")
    eval_data = extract_evaluation(filename)
    if eval_data:
        # filter out invalid questions
        valid_questions = [q for q in eval_data if len(q["options"]) > 0 and q["correctIndex"] != -1]
        all_evaluations[f"Modular {i}"] = valid_questions
        print(f"Found {len(valid_questions)} valid questions for Modular {i}.")
    else:
        print(f"No valid data found for Modular {i}")

with open("evaluations_data.json", "w", encoding="utf-8") as f:
    json.dump(all_evaluations, f, ensure_ascii=False, indent=2)

print("Extraction complete. Saved to evaluations_data.json.")
