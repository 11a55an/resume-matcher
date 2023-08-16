import pdfplumber

def read_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def calculate_word_count(resume_text):
    words = resume_text.split()
    return len(words)

# Path to the resume PDF file
resume_pdf_path = "data/resume.pdf"

# Read the resume PDF
resume_text = read_pdf(resume_pdf_path)

# Calculate word count
resume_word_count = calculate_word_count(resume_text)

if resume_word_count >= 750 and resume_word_count <= 2000:
    word_count_score = 1.0
elif resume_word_count >= 400:
    word_count_score = (resume_word_count - 400) / (2000 - 400)
else:
    word_count_score = 0.0

