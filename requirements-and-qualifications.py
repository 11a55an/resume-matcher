import pdfplumber
import re
import numpy as np

# Read resume PDF using pdfplumber
def read_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Simulated job description and a single resume
job_description = "Looking for a software engineer with a Bachelor's degree in Computer Science and strong programming skills."
resume_path = "data/resume.pdf"

# Read job description
job_text = job_description.lower()

# Read the resume PDF and preprocess
resume_text = read_pdf(resume_path).lower()

# Regular expression patterns for degree abbreviations and full names
degree_patterns = {
    'bachelor\'s degree': ['b\\.?s\\.?c\\.?s?\\.?', 'bachelor\'s'],
    'master\'s degree': ['m\\.?s\\.?c\\.?s?\\.?', 'master\'s'],
    'ph.d. degree': ['ph\\.d\\.?', 'doctorate', 'phd']
}

# Extract qualifications and requirements from job description using regex
job_qualifications = []
for full_degree, patterns in degree_patterns.items():
    pattern = '|'.join(patterns)
    job_qualifications.extend(re.findall(pattern, job_text))

# Extract qualifications from resume using regex
resume_qualifications = []
for full_degree, patterns in degree_patterns.items():
    pattern = '|'.join(patterns)
    resume_qualifications.extend(re.findall(pattern, resume_text))

# Calculate qualifications & requirements similarity
common_qualifications = set(job_qualifications) & set(resume_qualifications)
qualifications_score = len(common_qualifications) / len(job_qualifications)

print(f"Qualifications Score: {qualifications_score:.2f}")
