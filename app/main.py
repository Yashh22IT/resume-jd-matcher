from fastapi import FastAPI, UploadFile, File, Form
from app.extraction import extract_text_from_pdf, extract_text_from_docx
from app.matcher import compare_skills, semantic_similarity, compute_final_score, generate_suggestions
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Resume Screener API is running"}

@app.post("/analyze")
async def analyze_resume(resume_file: UploadFile = File(...), job_description: str = Form(...)):
    file_bytes = await resume_file.read()

    temp_path = "temp_" + resume_file.filename
    with open(temp_path, "wb") as f:
        f.write(file_bytes)

    if resume_file.filename.endswith(".pdf"):
        resume_text = extract_text_from_pdf(temp_path)
    else:
        resume_text = extract_text_from_docx(temp_path)

    result = compare_skills(resume_text, job_description)
    similarity = semantic_similarity(resume_text, job_description)
    final = compute_final_score(result["keyword_score"], similarity)
    suggestions = generate_suggestions(result["missing_skills"])

    return {
        "matched_skills": result["matched_skills"],
        "missing_skills": result["missing_skills"],
        "keyword_score": result["keyword_score"],
        "semantic_score": similarity,
        "final_score": final,
        "suggestions": suggestions
    }