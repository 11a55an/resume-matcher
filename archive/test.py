import re
import pdfplumber
import datetime
def read_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text
resume_path = "data/resume.pdf"
resume_text = read_pdf(resume_path).lower()

# Extract work experience section
pattern = re.compile(r'Work experience([\s\S]+?)(?:Qualifications|Projects|Skills|\Z)', re.IGNORECASE)
match = pattern.search(resume_text)

if match:
    work_experience_section = match.group(1)
else:
    work_experience_section = ""

# Extract start and end years from work experience
# Extract start and end years from work experience
work_experience_entries = re.findall(r'(\d{4}) — (\S+)', work_experience_section)

# Calculate total years of work experience
current_year = datetime.datetime.now().year
total_experience = 0
for start_year, end_year in work_experience_entries:
    if end_year.lower() == 'present':
        end_year = current_year
    total_experience += int(end_year) - int(start_year) + 1  # +1 to include both start and end years

max_job_experience = 2
experience_score = min(total_experience / max_job_experience, 1) if max_job_experience > 0 else 0
print(experience_score)