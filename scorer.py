from vectorizer import get_embedding
from extractor import extract_text_from_file
from sentence_transformers import util
import os
from io import BytesIO

def keyword_score(resume_text, skills):
    resume_text_lower = resume_text.lower()
    return sum(1 for skill in skills if skill.lower() in resume_text_lower) / len(skills)

def skill_match_flags(resume_text, skills):
    resume_text_lower = resume_text.lower()
    return {skill: (skill.lower() in resume_text_lower) for skill in skills}

def rank_resumes(resume_folder, job_description, skill_list):
    job_embedding = get_embedding(job_description)
    scores = {}
    skills_flags = {}
    
    for filename in os.listdir(resume_folder):
        file_path = os.path.join(resume_folder, filename)

        # Open file as BytesIO for the extractor
        with open(file_path, "rb") as f:
            file_bytes = BytesIO(f.read())

        text = extract_text_from_file(file_bytes, filename)
        if not text:
            continue
        
        resume_embedding = get_embedding(text)
        semantic_score = util.pytorch_cos_sim(resume_embedding, job_embedding).item()
        k_score = keyword_score(text, skill_list)
        final_score = 0.6 * semantic_score + 0.4 * k_score
        
        scores[filename] = final_score
        skills_flags[filename] = skill_match_flags(text, skill_list)
    
    ranked_resumes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked_resumes, skills_flags
