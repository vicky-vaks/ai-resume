from keybert import KeyBERT
import spacy

nlp = spacy.load("en_core_web_sm")
kw_model = KeyBERT()

def extract_skills_from_job(job_description, top_n=10):
    """
    Extract top skills/keywords from the job description
    Returns a list of skills
    """
    job_description = job_description.replace("\n", " ")
    keywords = kw_model.extract_keywords(job_description, keyphrase_ngram_range=(1,2), stop_words='english', top_n=top_n)
    skills = [kw[0] for kw in keywords]
    return skills
