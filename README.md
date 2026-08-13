# Resume ↔ Job Description Matcher

An NLP-powered tool that compares a resume against a job description and returns a match score, matched skills, missing skills, and actionable suggestions — similar to how real ATS (Applicant Tracking Systems) screen resumes before a human ever sees them.

## Demo

Upload a resume (PDF/DOCX), paste a job description, and get:
- **Final match score** — weighted combination of keyword overlap and semantic similarity
- **Matched & missing skills** — categorized by type (languages, frameworks, cloud, etc.)
- **Improvement suggestions** — grouped, readable recommendations on what to add

## How It Works

1. **Text extraction** — pulls raw text from PDF/DOCX using `pdfplumber` and `python-docx`
2. **Keyword matching** — checks a curated skills database against both texts to find overlaps
3. **Semantic similarity** — uses `sentence-transformers` (`all-MiniLM-L6-v2`) to convert text into embeddings and compute cosine similarity, catching relevant experience even when exact keywords don't match
4. **Weighted scoring** — combines keyword match (65%) and semantic similarity (35%) into one final score
5. **Suggestion engine** — groups missing skills by category and generates readable improvement suggestions

## Tech Stack

- **Backend:** FastAPI (Python) — REST API with auto-generated Swagger docs
- **NLP:** sentence-transformers, custom skill-phrase matching
- **File parsing:** pdfplumber, python-docx
- **Frontend:** Streamlit
- **Deployment target:** Render/Railway (backend) + Streamlit Community Cloud (frontend)

## Project Structure