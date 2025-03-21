import re
import csv


subject_keywords = {
    "Electrical Machine": ["motor", "transformer", "generator", "induction", "machine"],
    "Numerical Methods": ["bisection", "newton-raphson", "interpolation", "integration", "differential"],
    "Applied Mathematics": ["calculus", "algebra", "matrix", "probability", "geometry", "differential equations"],
    "Instrumentation I": ["sensor", "transducer", "measurement", "amplifier", "calibration"],
    "Data Structure & Algorithm": ["algorithm", "data structure", "linked list", "queue", "stack", "binary tree", "graph"],
    "Microprocessor": ["assembly language", "8085", "8086", "instruction set", "register", "memory"],
    "Discrete Structure": ["graph theory", "logic", "set theory", "combinatorics", "boolean algebra"]
}


def extract_year(text):
    match = re.search(r'\b(19|20)\d{2}\b', text)
    return match.group() if match else "Unknown"

def classify_subject(text):
    text_lower = text.lower()
    for subject, keywords in subject_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            return subject
    return "Unknown"

def process_text(text):
    year = extract_year(text)
    subject = classify_subject(text)
    return {"Year": year, "Subject": subject}


with open("extracted_text_ocr.txt", "r", encoding="utf-8") as file:
    extracted_text = file.read()


questions = re.split(r'(?i)\b(question\s*\d+|q\s*\d+)\b', extracted_text)



results = []
for i in range(1, len(questions), 2):
    question_text = questions[i] + questions[i+1] if i+1 < len(questions) else questions[i]
    data = process_text(question_text)
    data["Question"] = question_text.strip()
    results.append(data)

csv_file = "classified_questions.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["Year", "Subject", "Question"])
    writer.writeheader()
    writer.writerows(results)

print(f"Classification complete! Results saved to {csv_file}")
