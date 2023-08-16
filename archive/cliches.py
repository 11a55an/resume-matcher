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

# Define a list of cliches and fluffy words
cliches_and_fluffy_words = [
    "team player", "self-motivated", "detail-oriented", "results-driven",
    "excellent communication skills", "hard worker", "dynamic",
    "problem solver", "innovative", "proactive", "strategic thinker"
]

# Define personal pronouns
personal_pronouns = ["I", "me", "my", "mine", "we", "us", "our", "ours"]

# Function to check for cliches, fluffy words, and personal pronouns
def check_cliches_fluffy_words_personal_pronouns(text):
    cliches_fluffy_count = sum(text.lower().count(word) for word in cliches_and_fluffy_words)
    personal_pronouns_count = sum(text.lower().count(pronoun) for pronoun in personal_pronouns)

    return cliches_fluffy_count, personal_pronouns_count

# Get the counts from the resume text
cliches_fluffy_count, personal_pronouns_count = check_cliches_fluffy_words_personal_pronouns(resume_text)
cliches_pronouns_score = 100 - (cliches_fluffy_count + personal_pronouns_count) / len(resume_text.split()) * 100
    
print(cliches_pronouns_score)