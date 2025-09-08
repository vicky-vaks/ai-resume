from flask import Flask, request, render_template
from sentence_transformers import SentenceTransformer, util
import pdfplumber
from docx import Document
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_file(file_path):
    if file_path.endswith('.pdf'):
        text = ''
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        return text
    elif file_path.endswith('.docx'):
        doc = Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])
    return ''

def keyword_score(resume_text, skills):
    if not skills or not resume_text.strip():
        return 0
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    skills_embedding = model.encode(skills, convert_to_tensor=True)
    cosine_scores = util.cos_sim(resume_embedding, skills_embedding)
    score = float(cosine_scores.mean())
    return round(score * 100, 2)

@app.route('/', methods=['GET', 'POST'])
def index():
    score = None
    if request.method == 'POST':
        skills_text = request.form.get('skills', '')
        skills = [s.strip() for s in skills_text.split(',') if s.strip()]
        file = request.files.get('resume')
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            resume_text = extract_text_from_file(filepath)
            score = keyword_score(resume_text, skills)
            print("Score computed:", score)  # debug in terminal
    return render_template('index.html', score=score)

if __name__ == '__main__':
    app.run(debug=True)
