import pdfplumber
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import datetime

def evaluate_ats_best_practices(text,):
    # Simulate ATS best practices scoring
    # Check if file format is compatible
    compatible_file_format = re.search(r'\.pdf$', text) is not None
    
    # Check if email address is present
    email_present = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', text) is not None
    
    # Check if phone number is present
    phone_number_present = re.search(r'\b(?:\d{3}-\d{3}-\d{4}|\d{10})\b', text) is not None
    
    # Check if LinkedIn profile is mentioned
    linkedin_profile_present = "linkedin.com" in text.lower()
    
    # Check if job title match exists
    job_title_match = "software engineer" in text.lower()
    
    # Check if education match exists
    education_match = "computer science" in text.lower()
    
    # Check if standard sections are present
    standard_sections_present = all(section in text.lower() for section in ["experience", "education"])
    
    # Check if proper date formatting is used
    proper_date_formatting = re.search(r'\b\d{1,2}/\d{2,4}\b', text) is not None
    
    # Check if unknown characters are present
    no_unknown_characters = not bool(re.search(r'[^\x00-\x7F]', text))
    
    score = (
        compatible_file_format +
        email_present +
        phone_number_present +
        linkedin_profile_present +
        job_title_match +
        education_match +
        standard_sections_present +
        proper_date_formatting +
        no_unknown_characters
    ) / 9 * 100  # Total possible points / number of criteria

    return score
def keywords_extract(text,required_keywords_skills): 
    '''
    Tokenize webpage text and extract keywords
    Input: 
        text (str): text to extract keywords from
    Output: 
        keywords (list): keywords extracted and filtered by pre-defined dictionary
    '''        
    # Remove non-alphabet; 3 for d3.js and + for C++
    text = re.sub("[^a-zA-Z+3]"," ", text) 
    text = text.lower().split()
    stops = set(stopwords.words("english")) #filter out stop words in english language
    text = [w for w in text if not w in stops]
    text = list(set(text))
    # We only care keywords from the pre-defined skill dictionary
    keywords = [str(word) for word in text if word in required_keywords_skills]
    return keywords

def calculate_similarity(resume_keywords, job_keywords):
    # Combine the keywords into strings
    resume_keywords_text = " ".join(resume_keywords)
    job_keywords_text = " ".join(job_keywords)
    
    # Combine the keywords texts into a list
    all_keywords_text = [resume_keywords_text, job_keywords_text]
    
    # Create a CountVectorizer and fit transform the data
    vectorizer = CountVectorizer(lowercase=True, stop_words='english')
    vectorized_keywords = vectorizer.fit_transform(all_keywords_text).toarray()
    
    # Calculate cosine similarity
    cosine_similarities = cosine_similarity([vectorized_keywords[0]], [vectorized_keywords[1]])[0][0]
    
    return cosine_similarities

def evaluate_keywords_skills(resume_text,required_keywords_skills):
    resume_keywords = keywords_extract(resume_text,required_keywords_skills)
    similarity = calculate_similarity(resume_keywords,required_keywords_skills)
    formatted_score = format(similarity, '.2f')
    score = float(formatted_score)*100
    return score

def evaluate_experience_abilities(resume_text,job_experience):
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

    job_experience = 2
    experience_score = min(total_experience / job_experience, 1) if job_experience > 0 else 0
    return experience_score

def evaluate_requirements_qualifications(resume_text,desired_education):
    # Define a regular expression pattern to extract the education section
    pattern = re.compile(r'Education([\s\S]+?)(?:Work experience|Qualifications|Projects|Skills|\Z)', re.IGNORECASE)
    match = pattern.search(resume_text)

    if match:
        education_section = match.group(1)
    else:
        education_section = ""

    # Extract education entries
    education_entries = re.findall(r'(\d{4} — \d{4})([\s\S]+?)(?=\d{4} — \d{4}|$)', education_section)
    # print(education_entries)
    # Check if any of the desired education criteria is present in the education entries
    matched_education = []

    for entry in education_entries:
        for education in desired_education:
            if education in entry[1]:
                matched_education.append(education)

    if matched_education:
        score = 100
    else:
        score = 0
    return score

def evaluate_word_count(resume_text):
    words = resume_text.split()
    resume_word_count = len(words)
    if resume_word_count >= 750 and resume_word_count <= 2000:
        word_count_score = 1.0
    elif resume_word_count >= 400:
        word_count_score = (resume_word_count - 400) / (2000 - 400)
    else:
        word_count_score = 0.0
    return word_count_score

def evaluate_measurable_results(text):
    measurable_results = re.findall(r'\d+\s*[\w\s]*\s*accomplishment[s]*', text, re.I)
    if len(measurable_results)>5:
        score = 100
    else:
        score = 0
    return score

def evaluate_action_verbs(text):
    action_verbs = re.findall(r'\b(?:\w+(?:-\w+)*)\s+(?:\w+(?:-\w+)*)\s+(?:\w+(?:-\w+)*)\b', text)
    if len(action_verbs)>10:
        score = 100
    else:
        score = 0
    return score

def evaluate_cliches_fluffy_words(text):
    cliches_and_fluffy_words = [
    "team player", "self-motivated", "detail-oriented", "results-driven",
    "excellent communication skills", "hard worker", "dynamic",
    "problem solver", "innovative", "proactive", "strategic thinker"
    ]

    # Define personal pronouns
    personal_pronouns = ["I", "me", "my", "mine", "we", "us", "our", "ours"]
    cliches_fluffy_count = sum(text.lower().count(word) for word in cliches_and_fluffy_words)
    personal_pronouns_count = sum(text.lower().count(pronoun) for pronoun in personal_pronouns)
    cliches_pronouns_score = 100 - (cliches_fluffy_count + personal_pronouns_count) / len(text.split()) * 100
    return cliches_pronouns_score


def read_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

resume_path = "data/resume.pdf"
resume_text = read_pdf(resume_path)
weights = {
    "ATS Best Practices": 0.10,
    "Keywords and Skills": 0.30,
    "Experience & Abilities": 0.25,
    "Requirements & Qualifications": 0.25,
    "Word Count": 0.05,
    "Measurable Results": 0.025,
    "Action Verbs": 0.025,
    "Cliches, Fluffy Words, Personal Pronouns": 0.0
}

# Define the factors and their corresponding evaluation functions
ats_score = evaluate_ats_best_practices(resume_text)
required_keywords_skills = ["python", "web development", "machine learning"]
skills_score = evaluate_keywords_skills(resume_text,required_keywords_skills)
experience_score = evaluate_experience_abilities(resume_text,2)*100
education_score = evaluate_requirements_qualifications(resume_text,"BSCS")
word_score = evaluate_word_count(resume_text)
measureable_score = evaluate_measurable_results(resume_text)
action_score = evaluate_action_verbs(resume_text)
cliche_score = evaluate_cliches_fluffy_words(resume_text)

total_score = (ats_score*0.10)+(skills_score*0.30)+(experience_score*0.25)+(education_score*0.25)+(word_score*0.05)+(measureable_score*0.025)+(cliche_score*0)
print("Total Score: ",total_score)
print("ATS Best Practices Score: ", ats_score)
print("Skills Score: ", skills_score)
print("Experience Score: ", experience_score)
print("Education Score: ", education_score)
print("Word Score: ", word_score)
print("Measureable Score: ", measureable_score)
print("Action Score: ", action_score)
print("Cliche Score: ", cliche_score)