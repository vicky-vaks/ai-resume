# AI Resume Ranker

## Project Overview
The AI Resume Ranker is a Python-based application that automates the evaluation and ranking of resumes based on job descriptions. It extracts skills, experience, and other relevant information from resumes and scores them according to relevance to a given job description. This project helps recruiters and HR professionals save time, improve accuracy, and make data-driven hiring decisions.

## Features

- **Resume Parsing:** Extracts skills, education, and experience from resumes in PDF format.  
- **Keyword Matching & Scoring:** Compares resume content against job descriptions and assigns relevance scores.  
- **Skill Extraction:** Identifies relevant skills using NLP techniques.  
- **Report Generation:** Generates a summarized ranking report of all resumes.  
- **Web Interface:** Simple HTML templates (`index.html` and `result.html`) to upload resumes and display results.  
- **Modular Code:** Separate Python scripts for parsing, scoring, vectorizing, and report generation.  

## Project Structure

python -m venv venv
pip install -r requirements.txt
