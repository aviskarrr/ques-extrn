import re
import pandas as pd


subject_keywords = {
    "Electrical Machine": ["motor", "transformer", "generator", "induction", "machine", "winding", "synchronous", "torque"],
    "Numerical Methods": ["bisection", "newton-raphson", "interpolation", "integration", "differential", "error", "iteration", "eigenvalue"],
    "Applied Mathematics": ["calculus", "algebra", "matrix", "probability", "geometry", "differential equations", "linear", "vector"],
    "Instrumentation I": ["sensor", "transducer", "measurement", "amplifier", "calibration", "bridge", "strain gauge", "thermocouple"],
    "Data Structure & Algorithm": ["algorithm", "data structure", "linked list", "queue", "stack", "binary tree", "graph", "sorting", "searching"],
    "Microprocessor": ["assembly language", "8085", "8086", "instruction set", "register", "memory", "interrupt", "addressing"],
    "Discrete Structure": ["graph theory", "logic", "set theory", "combinatorics", "boolean algebra", "relations", "functions", "permutations"]
}


def extract_year(text):
    match = re.search(r'\b(19|20)\d{2}\b', text)
    return match.group() if match else "Unknown"


def classify_subject(text):
    text_lower = text.lower()
    for subject, keywords in subject_keywords.items():
        if any(re.search(rf'\b{keyword}\b', text_lower) for keyword in keywords):
            return subject
    return "Unknown"


def process_text(text):
    year = extract_year(text)
    subject = classify_subject(text)
    return {"Year": year, "Subject": subject}

# Read extracted text from a file
with open("extracted_text_ocr.txt", "r", encoding="utf-8") as file:
    extracted_text = file.read()


questions = re.split(r'(?i)\b(?:question\s*\d+|q\s*\d+)\b', extracted_text)


results = []
for i in range(1, len(questions), 2):
    question_text = questions[i] + questions[i+1] if i+1 < len(questions) else questions[i]
    data = process_text(question_text)
    data["Question"] = question_text.strip()
    print(f"Processing Question {i//2 + 1}: {data}")  # progress log
    results.append(data)


df = pd.DataFrame(results)
df.to_excel("classified_questions.xlsx", index=False)

print("Classification complete! Results saved to classified_questions.xlsx")