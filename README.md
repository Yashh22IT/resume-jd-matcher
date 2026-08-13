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

resume-screener/
├── app/
│ ├── main.py # FastAPI app + /analyze endpoint
│ ├── extraction.py # PDF/DOCX text extraction
│ ├── matcher.py # Keyword matching, semantic similarity, scoring, suggestions
│ └── skills_db.py # Curated skills database
├── streamlit_app.py # Frontend UI
├── requirements.txt
└── README.md

## Setup & Run Locally

```bash
# Clone the repo
git clone https://github.com/Yashh22IT/resume-jd-matcher.git
cd resume-jd-matcher

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Start the backend (Terminal 1)
uvicorn app.main:app --reload

# Start the frontend (Terminal 2, same venv activated)
streamlit run streamlit_app.py
```

- Backend Swagger docs: `http://127.0.0.1:8000/docs`
- Frontend UI: `http://localhost:8501`

> Note: the first request downloads the `all-MiniLM-L6-v2` model (~80MB), which takes 30-60 seconds. It's cached after that.

## Possible Future Improvements

- Resume section/structure detection (Education, Experience, Skills)
- Batch comparison — rank multiple resumes against one JD
- Export analysis as a downloadable PDF report
- Expand the skills database dynamically using NER instead of a fixed list