import pdfplumber
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import datetime

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



def read_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

resume_path = "data/resume.pdf"
resume_text = read_pdf(resume_path)

# Define the factors and their corresponding evaluation functions
required_keywords_skills = ["python", "web development", "machine learning"]
skills_score = evaluate_keywords_skills(resume_text,required_keywords_skills)
experience_score = evaluate_experience_abilities(resume_text,2)*100
education_score = evaluate_requirements_qualifications(resume_text,"BSCS")

total_score = (skills_score*0.40)+(experience_score*0.40)+(education_score*0.20)
print("Total Score: ",total_score)
print("Skills Score: ", skills_score)
print("Experience Score: ", experience_score)
print("Education Score: ", education_score)