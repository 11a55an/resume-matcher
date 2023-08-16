
import re
import pdfplumber
def read_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text
resume_path = "data/resume.pdf"
resume_text = read_pdf(resume_path).lower()

# Desired education criteria
desired_education = ["BS Computer Science", "FSc Pre Engineering"]

# Define a regular expression pattern to extract the education section
pattern = re.compile(r'Education([\s\S]+?)(?:Work experience|Qualifications|Projects|Skills|\Z)', re.IGNORECASE)
match = pattern.search(resume_text)

if match:
    education_section = match.group(1)
else:
    education_section = ""

# Extract education entries
education_entries = re.findall(r'(\d{4} — \d{4})([\s\S]+?)(?=\d{4} — \d{4}|$)', education_section)
print(education_entries)
# Check if any of the desired education criteria is present in the education entries
matched_education = []

for entry in education_entries:
    for education in desired_education:
        if education in entry[1]:
            matched_education.append(education)

if matched_education:
    print("Matched education criteria:")
    for education in matched_education:
        print(education)
else:
    print("No matched education criteria found.")
