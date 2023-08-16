import pdfplumber
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
# import nltk
# nltk.download('stopwords')
# Read resume PDF using pdfplumber
def read_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def keywords_extract(text): 
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

job_description = "Looking for a software engineer with Python skills and web development experience."
required_keywords_skills = ["python", "web development", "machine learning"]
resume_text = read_pdf("data/resume.pdf")
resume_keywords = keywords_extract(resume_text)
print(resume_keywords)
similarity = calculate_similarity(resume_keywords,required_keywords_skills)
formatted_score = format(similarity, '.2f')
score = float(formatted_score)*100
print(f"Similarity Score: {score}")