import os
import re
import fitz  # PyMuPDF
from docx import Document
from sentence_transformers import SentenceTransformer, util

# -------- CONFIGURATION --------
RESUME_FOLDER = "resumes"  # folder containing all resumes
JOB_DESCRIPTION = """
Looking for a Python developer with experience in SQL, Machine Learning, 
and Data Analysis. Candidate must have a Bachelor's degree in Computer Science.
"""
SKILL_LIST = ["Python", "SQL", "Machine Learning", "Data Analysis"]

# -------- UTILITY FUNCTIONS --------
def clean_text(text):
    text = text.replace("\n", " ")
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    
    if ext == ".pdf":
        try:
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text() + "\n"
        except Exception as e:
            print(f"Failed to read PDF {file_path}: {e}")
    elif ext == ".docx":
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    elif ext == ".txt":
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        print(f"Unsupported file type: {file_path}")
    
    return clean_text(text)

def keyword_score(resume_text, skills):
    resume_text_lower = resume_text.lower()
    return sum(1 for skill in skills if skill.lower() in resume_text_lower) / len(skills)

# -------- MAIN RANKING FUNCTION --------
def rank_resumes():
    # Load embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    job_embedding = model.encode(JOB_DESCRIPTION, convert_to_tensor=True)
    
    # Process resumes
    scores = {}
    for filename in os.listdir(RESUME_FOLDER):
        file_path = os.path.join(RESUME_FOLDER, filename)
        text = extract_text(file_path)
        if not text:
            continue
        
        # Semantic similarity
        resume_embedding = model.encode(text, convert_to_tensor=True)
        semantic_score = util.pytorch_cos_sim(resume_embedding, job_embedding).item()
        
        # Keyword score
        k_score = keyword_score(text, SKILL_LIST)
        
        # Final weighted score
        final_score = 0.6 * semantic_score + 0.4 * k_score
        scores[filename] = final_score
    
    # Sort resumes
    ranked_resumes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    print("\n--- Ranked Resumes ---")
    for i, (filename, score) in enumerate(ranked_resumes, 1):
        print(f"{i}. {filename} -> Score: {score:.2f}")

# -------- RUN THE RANKER --------
if __name__ == "__main__":
    rank_resumes()
