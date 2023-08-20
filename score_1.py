import pdfplumber
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import datetime
import spacy
from collections import Counter
import nltk

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_education(text):
    pattern = r"(?i)(?:(?:Bachelor|Master|Ph\.?D\.?|Doctor(?:ate)?|B\.?S\.?|M\.?S\.?|D\.?S\.?|J\.?D\.?|LL\.?B\.?|LL\.?M\.?)(?![a-zA-Z])\.?)+[^a-zA-Z]*[a-zA-Z]+[^a-zA-Z]*"

    # Use the regular expression to find education entries in the text
    education_info = re.findall(pattern, text)

    return education_info

def evaluate_ats_best_practices(text,filename,job_description_education):
    # Simulate ATS best practices scoring
    # Check if file format is compatible
    print("File Format: ", re.search(r'\.pdf$|\.docx$', filename))
    compatible_file_format = re.search(r'\.pdf$|\.docx$', filename) is not None
    print("Email: ", re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', text))
    # Check if email address is present
    email_present = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', text) is not None
    print("Phone Number: ",re.search(r'\b(?:\+?\d{1,3}[-.\s]??\d{3}[-.\s]??\d{3}[-.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-.\s]??\d{4}|\d{10}|\d{3}[-.\s]??\d{3}[-.\s]??\d{4})\b', text))
    # Check if phone number is present
    phone_number_present = re.search(r'\b(?:\+?\d{1,3}[-.\s]??\d{3}[-.\s]??\d{3}[-.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-.\s]??\d{4}|\d{10}|\d{3}[-.\s]??\d{3}[-.\s]??\d{4})\b', text) is not None
    
    # Check if LinkedIn profile is mentioned
    linkedin_profile_present = "linkedin.com" in text.lower()
    print("Linkedin Link Present: ","linkedin.com" in text.lower())
    # Check if job title match exists
    job_title_match = "compliance lawyer" in text.lower()
    print("Job Title Match: ","compliance lawyer" in text.lower())
    
    # Check if education match exists
    resume_education = extract_education(resume_text)
    print("Resume Education:", resume_education)
    print("Job Description Education:", job_description_education)
    # Threshold for considering a match
    threshold = 0.5  # You can adjust this threshold as needed

    # Function to determine if there is a match based on Jaccard similarity
    def is_match(set1, set2, threshold):
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        similarity = intersection / union if union != 0 else 0  # Avoid division by zero
        return similarity >= threshold
    
    # Initialize sets of education entries
    resume_education_sets = [set(education.split(' ')) for education in resume_education]
    job_description_education_sets = [set(education.split(' ')) for education in job_description_education]

    # Initialize a matrix of False values
    is_education_match = any(any(is_match(resume_set, job_set, threshold) for job_set in job_description_education_sets) for resume_set in resume_education_sets)

    # Check if standard sections are present
    standard_sections_present = all(section in text.lower() for section in ["experience", "education"])
    print("Standard sections present: ",all(section in text.lower() for section in ["experience", "education"]))
    # Check if proper date formatting is used
    proper_date_formatting = re.search(r'\b\d{1,2}/\d{2,4}\b', text) is not None
    print("Proper Date Formatting: ", re.search(r'\b\d{1,2}/\d{2,4}\b', text))
    # Check if unknown characters are present
    no_unknown_characters = not bool(re.search(r'[^\x00-\x7F]', text))
    print("Unknown Characters: ", re.search(r'[^\x00-\x7F]', text))
    score = (
        compatible_file_format +
        email_present +
        phone_number_present +
        linkedin_profile_present +
        job_title_match +
        is_education_match +
        standard_sections_present +
        proper_date_formatting +
        no_unknown_characters
    ) / 9 * 100  # Total possible points / number of criteria

    return score

def extract_keywords(text, num_keywords=10):
    # Tokenize the text
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    
    # Count word frequencies
    word_freq = Counter(words)
    
    # Get the most common keywords
    keywords = word_freq.most_common(num_keywords)
    
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
    resume_keywords = [keyword for keyword, _ in extract_keywords(resume_text)]
    print("Resume Keywords: ", resume_keywords)
    print("Job Description Keywords: ", required_keywords_skills)
    similarity = calculate_similarity(resume_keywords,required_keywords_skills)
    formatted_score = format(similarity, '.2f')
    score = float(formatted_score)*100
    return score

def evaluate_experience_abilities(resume_text,job_experiences,job_abilities):
    doc = nlp(resume_text)
    experience_keywords = ["experience", "skills", "abilities"]

    extracted_experience = []
    extracted_abilities = []

    for sentence in doc.sents:
        for keyword in experience_keywords:
            if keyword in sentence.text.lower():
                if "experience" in sentence.text.lower():
                    extracted_experience.append(sentence.text)
                else:
                    extracted_abilities.append(sentence.text)
    print("Abilities: ",extracted_abilities)
    print("Experience: ",extracted_experience)
    similarity = calculate_similarity(extracted_abilities,job_abilities)
    formatted_score = format(similarity, '.2f')
    scoreAbilities = float(formatted_score)*100
    similarity = calculate_similarity(extracted_experience,job_experiences)
    formatted_score = format(similarity, '.2f')
    scoreExperience = float(formatted_score)*100
    score = scoreAbilities+scoreExperience/2
    return score

def evaluate_requirements_qualifications(resume_text,job_description_education):
    resume_education = extract_education(resume_text)
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    # Combine the education lists into a single list
    combined_education = resume_education + job_description_education

    # Create a CountVectorizer to convert education entries into vectors
    vectorizer = CountVectorizer()

    # Fit and transform the combined education list
    education_vectors = vectorizer.fit_transform(combined_education)

    # Calculate cosine similarity between the vectors
    cosine_similarities = cosine_similarity(education_vectors)

    average_similarity = cosine_similarities.mean()
    return average_similarity*100

def evaluate_word_count(resume_text):
    words = resume_text.split()
    resume_word_count = len(words)
    print("Word Count: ", resume_word_count)
    if resume_word_count >= 750 and resume_word_count <= 2000:
        word_count_score = 1.0
    elif resume_word_count >= 400:
        word_count_score = (resume_word_count - 400) / (2000 - 400)
    else:
        word_count_score = 0.0
    return word_count_score

def evaluate_measurable_results(text):
    measurable_results = re.findall(r'\d+\s*[\w\s]*\s*accomplishment[s]*', text, re.I)
    print("Measureable Results: ", re.findall(r'\d+\s*[\w\s]*\s*accomplishment[s]*', text, re.I))
    if len(measurable_results)>5:
        score = 100
    else:
        score = 0
    return score

def evaluate_action_verbs(text):
    action_verbs = re.findall(r'\b(?:\w+(?:-\w+)*)\s+(?:\w+(?:-\w+)*)\s+(?:\w+(?:-\w+)*)\b', text)
    print("Action Verbs: ", len(action_verbs))
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
    print("Cliches: ", cliches_fluffy_count)
    print("Personal Pronouns: ", sum(text.lower().count(pronoun) for pronoun in personal_pronouns))
    personal_pronouns_count = sum(text.lower().count(pronoun) for pronoun in personal_pronouns)
    cliches_pronouns_score = 100 - (cliches_fluffy_count + personal_pronouns_count) / len(text.split()) * 100
    return cliches_pronouns_score


def read_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text


# Sample job description text
job_description = """
Compliance Lawyer at Enerflex
Company Mission In this role, you will play a crucial part in ensuring that Enerflex’s operations and initiatives comply with the regulatory requirements of the countries in which we operate, including Canada and the U.S., and that Enerflex’s Values are appropriately reflected in our business activities. Reporting to the Senior Vice President & General Counsel, the Associate General Counsel, Compliance will be responsible for enhancing and maintaining the company’s global compliance program, providing strategic legal guidance on compliance-related matters to regional businesses, overseeing the company’s records management practices, and collaborating with regional and functional teams to maintain the highest standards of ethical conduct and legal adherence.
Job Responsibilities & Duties
•	Compliance Program Management: Design, implement, maintain, and enhance compliance programs tailored to the specific requirements of the company, keeping abreast of regulatory changes and integrating recommended practices, to prevent illegal, unethical, or improper conduct.
•	Risk Management: Proactively identify potential compliance risks and legal challenges within the company's operations and projects. Provide expert legal counsel to, and collaborate with, relevant stakeholders to develop mitigation strategies to internal departments and teams, ensuring that business decisions align with regulatory requirements, company policies, and ethical standards.
•	Privacy Program Management: Oversee the company's global data privacy program, ensuring compliance with relevant data protection laws and regulations. Develop and implement policies, procedures, and training related to data privacy and protection.
•	Records Management: Implement and manage a robust records management program to ensure the proper retention, storage, and disposal of company records in accordance with company and regulatory requirements.
•	Training and Education: Develop, maintain and deliver, as appropriate, training programs promoting awareness of compliance risks and mitigation strategies and fostering a culture of ethical behavior. Establish programs to instill a culture of compliance, including communications programs and leadership initiatives.
•	Monitoring and Reporting: Establish systems to track compliance with relevant laws and regulations. Prepare regular reports for senior management and regulatory authorities, as required. Provide reports to senior management and the Audit Committee of the Board of Directors as to the operation and effectiveness of compliance efforts. Provide leadership in support of corporate governance objectives.
•	Investigations: Conduct or oversee internal and independent third-party investigations, as appropriate, to address compliance concerns, ensuring thorough and objective assessments while recommending appropriate corrective actions arising from such investigations.
•	Collaboration: Work closely with regional and functional teams, including Legal, Operations, Human Resources, Finance, and HSE, to ensure alignment of compliance efforts with broader business objectives. Participate in regular Global Legal Team initiatives and meetings.
•	Broader Support Duties: As a member of Enerflex’s Global Legal team, the Associate General Counsel, Compliance will provide broader support to Enerflex from time to time as directed by the General Counsel. This may include advising and assisting on corporate transactions, collaborating with business support functions, and providing advice on various matters including commercial transactions, policies, and processes.
Required Qualifications
•	Minimum 10 years of legal experience, with a focus on compliance, including management of anti-corruption, trade controls, and sanctions compliance programs.
•	Juris Doctor or equivalent degree from an accredited law school.
•	Active membership in good standing with the bar association of at least one Canadian province or US state.
•	In-house legal counsel experience, preferably for a global energy company.
•	Prior experience in managing and conducting internal investigations.
•	Knowledge of data privacy and protection laws, including GDPR, and experience managing privacy programs.
•	Ability to manage records management programs to ensure compliance and efficiency.
Preferred Qualifications
•	[No information provided in the job description]
Keywords
•	Compliance lawyer
•	Regulatory requirements
•	Strategic legal guidance
•	Records management
•	Ethical conduct
•	Privacy program
•	Data protection laws
•	Mitigation strategies
•	Corporate governance
•	Investigations
Soft Skills
•	Collaboration
•	Strong analytical and problem-solving skills
•	Approachability, resolve, and diplomacy
•	Interpersonal skills
•	Resourcefulness
Hard Skills
•	Legal experience with compliance focus
•	Knowledge of data privacy laws
•	Records management expertise
Technical Skills
•	[No specific technical skills mentioned in the job description]
"""

# Tokenize the text
sentences = nltk.sent_tokenize(job_description)
job_description_education = extract_education(job_description)
doc = nlp(job_description)
experience_keywords = ["experience", "skills", "abilities"]

extracted_experience = []
extracted_abilities = []

for sentence in doc.sents:
    for keyword in experience_keywords:
        if keyword in sentence.text.lower():
            if "experience" in sentence.text.lower():
                extracted_experience.append(sentence.text)
            else:
                extracted_abilities.append(sentence.text)
# Extract job title
job_title_pattern = re.compile(r'^(.*?) at (.+)$', re.DOTALL)
job_title_match = job_title_pattern.search(job_description)
if job_title_match:
    job_title = job_title_match.group(1).strip()
else:
    job_title = "Job title not found"

duties_section_pattern = re.compile(r'Job Responsibilities & Duties\n(.*?)(?:Required Qualifications|Preferred Qualifications|Keywords|Soft Skills|Hard Skills|Technical Skills|\Z)', re.DOTALL)
duties_section_match = duties_section_pattern.search(job_description)
if duties_section_match:
    duties_section = duties_section_match.group(1).strip()
else:
    duties_section = "Duties section not found"

# Split the duties into a list of bullet points
duties_list = [duty.strip() for duty in re.split(r'\n•\s*', duties_section) if duty.strip()]

# Extract required qualifications
# Extract the "Required Qualifications" section
qualifications_section_pattern = re.compile(r'Required Qualifications\n(.*?)(?:Preferred Qualifications|Keywords|Soft Skills|Hard Skills|Technical Skills|\Z)', re.DOTALL)
qualifications_section_match = qualifications_section_pattern.search(job_description)
if qualifications_section_match:
    qualifications_section = qualifications_section_match.group(1).strip()
else:
    qualifications_section = "Required Qualifications section not found"

# Split the required qualifications into a list of bullet points
required_qualifications_list = [qualification.strip() for qualification in re.split(r'\n•\s*', qualifications_section) if qualification.strip()]

# Extract preferred qualifications
preferred_qualifications = []
for sentence in sentences:
    if "Preferred Qualifications" in sentence:
        preferred_qualifications_text = re.sub(r'\s+', ' ', sentence).strip()
        preferred_qualifications_text = preferred_qualifications_text.replace("Preferred Qualifications", "")
        preferred_qualifications = preferred_qualifications_text.split("•")

# Extract keywords
# Extract the "Keywords" section
keywords_section_pattern = re.compile(r'Keywords\n(.*?)(?:Soft Skills|Hard Skills|Technical Skills|\Z)', re.DOTALL)
keywords_section_match = keywords_section_pattern.search(job_description)
if keywords_section_match:
    keywords_section = keywords_section_match.group(1).strip()
else:
    keywords_section = "Keywords section not found"

# Split the keywords into a list
keywords_list = [keyword.strip() for keyword in keywords_section.split('•') if keyword.strip()]


# Extract the "Soft Skills" section
soft_skills_section_pattern = re.compile(r'Soft Skills\n(.*?)(?:Hard Skills|Technical Skills|\Z)', re.DOTALL)
soft_skills_section_match = soft_skills_section_pattern.search(job_description)
if soft_skills_section_match:
    soft_skills_section = soft_skills_section_match.group(1).strip()
else:
    soft_skills_section = "Soft Skills section not found"

# Split the soft skills into a list
soft_skills_list = [skill.strip() for skill in soft_skills_section.split('•') if skill.strip()]

# Extract the "Hard Skills" section
hard_skills_section_pattern = re.compile(r'Hard Skills\n(.*?)(?:Technical Skills|\Z)', re.DOTALL)
hard_skills_section_match = hard_skills_section_pattern.search(job_description)
if hard_skills_section_match:
    hard_skills_section = hard_skills_section_match.group(1).strip()
else:
    hard_skills_section = "Hard Skills section not found"

# Split the hard skills into a list
hard_skills_list = [skill.strip() for skill in hard_skills_section.split('•') if skill.strip()]

# Extract the "Technical Skills" section
technical_skills_section_pattern = re.compile(r'Technical Skills\n(.*?)\Z', re.DOTALL)
technical_skills_section_match = technical_skills_section_pattern.search(job_description)
if technical_skills_section_match:
    technical_skills_section = technical_skills_section_match.group(1).strip()
else:
    technical_skills_section = "Technical Skills section not found"

# Split the technical skills into a list
technical_skills_list = [skill.strip() for skill in technical_skills_section.split('•') if skill.strip()]

resume_path = "data/Michael Goff.pdf"
resume_text = read_pdf(resume_path)

# Define the factors and their corresponding evaluation functions
ats_score = evaluate_ats_best_practices(resume_text,resume_path,job_description_education)
skills_score = evaluate_keywords_skills(resume_text,keywords_list)
experience_score = evaluate_experience_abilities(resume_text,extracted_experience,extracted_abilities)
education_score = evaluate_requirements_qualifications(resume_text,job_description_education)
word_score = evaluate_word_count(resume_text)
measureable_score = evaluate_measurable_results(resume_text)
action_score = evaluate_action_verbs(resume_text)
cliche_score = evaluate_cliches_fluffy_words(resume_text)

total_score = (ats_score*0.10)+(skills_score*0.30)+(experience_score*0.25)+(education_score*0.25)+(word_score*0.05)+(measureable_score*0.025)+(cliche_score*0)
print("Total Score: ",total_score)
# print("ATS Best Practices Score: ", ats_score)
# print("Skills Score: ", skills_score)
# print("Experience Score: ", experience_score)
# print("Education Score: ", education_score)
# print("Word Score: ", word_score)
# print("Measureable Score: ", measureable_score)
# print("Action Score: ", action_score)
# print("Cliche Score: ", cliche_score)