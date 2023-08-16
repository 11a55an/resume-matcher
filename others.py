import pdfplumber
import re

# Function to read text from a PDF file
def read_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Read the resume PDF and preprocess
resume_path = "data/resume.pdf"
resume_text = read_pdf(resume_path)

# Function to count measurable results and action verbs
def count_measurable_results_and_action_verbs(text):
    measurable_results = re.findall(r'\d+\s*[\w\s]*\s*accomplishment[s]*', text, re.I)
    action_verbs = re.findall(r'\b(?:\w+(?:-\w+)*)\s+(?:\w+(?:-\w+)*)\s+(?:\w+(?:-\w+)*)\b', text)

    return len(measurable_results), len(action_verbs)

# Get the counts from the resume text
measurable_results_count, action_verbs_count = count_measurable_results_and_action_verbs(resume_text)
print(measurable_results_count)