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
job_description = "Looking for a software engineer with 3+ years of experience, 2-4 yrs experience, and 5 years experience."
resume_path = "data/resume.pdf"

# Read job description
job_text = job_description.lower()

# Read the resume PDF and preprocess
resume_text = read_pdf(resume_path).lower()

# Extract experience from job description using regex
job_experience_matches = re.findall(r'(\d+)[ -]*((?:\+|\-)?\d*)\s*yr[s]*', job_text)

# Convert various experience formats to a single value
job_experience_years = []
for match in job_experience_matches:
    years = int(match[0])
    if match[1]:
        modifier = 1 if match[1] == '+' else -1
        modifier_years = int(match[1])
        years += modifier * modifier_years
    job_experience_years.append(years)

# Extract work experience section from resume using regex
work_experience_section = re.findall(r'work experience:(.*?)(?:\n\n|\n|$)', resume_text, re.DOTALL)
work_experience_text = ' '.join(work_experience_section).strip()

# Extract years from work experience section using regex
experience_years_matches = re.findall(r'\b\d{4}\b', work_experience_text)
experience_years = list(map(int, experience_years_matches))

# Classify experience years as start and end years
start_years = experience_years[::2]
end_years = experience_years[1::2]

# Calculate total experience based on start and end years
total_experience = sum(end_year - start_year + 1 for start_year, end_year in zip(start_years, end_years))

# Calculate experience score
max_job_experience = max(job_experience_years)
experience_score = min(total_experience / max_job_experience, 1) if max_job_experience > 0 else 0

print(f"Experience Score: {experience_score:.2f}")