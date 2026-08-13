from app.skills_db import get_all_skills, get_skill_category
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer("all-MiniLM-L6-v2")

def find_skills_in_text(text):
    text = text.lower()
    found_skills = []
    all_skills = get_all_skills()
    for skill in all_skills:
        if skill in text:
            found_skills.append(skill)
    return found_skills

def compare_skills(resume_text, jd_text):
    resume_skills = set(find_skills_in_text(resume_text))
    jd_skills = set(find_skills_in_text(jd_text))

    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills

    keyword_score = (len(matched) / len(jd_skills) * 100) if jd_skills else 0

    return {
        "matched_skills": list(matched),
        "missing_skills": list(missing),
        "keyword_score": round(keyword_score, 2)
    }

def generate_suggestions(missing_skills):
    if not missing_skills:
        return ["Great job! Your resume covers all the key skills mentioned in this job description."]

    grouped = {}
    for skill in missing_skills:
        category = get_skill_category(skill)
        grouped.setdefault(category, []).append(skill)

    suggestions = []
    for category, skills in grouped.items():
        category_name = category.replace("_", " ").title()
        skills_text = ", ".join(skills)
        suggestions.append(f"Consider highlighting {category_name} skills such as: {skills_text}")

    return suggestions

def semantic_similarity(resume_text, jd_text):
    embeddings = model.encode([resume_text, jd_text])
    score = util.cos_sim(embeddings[0], embeddings[1])
    return round(float(score[0][0]) * 100, 2)

def compute_final_score(keyword_score, semantic_score):
    final_score = (0.65 * keyword_score) + (0.35 * semantic_score)
    return round(final_score, 2)
    
if __name__ == "__main__":
    from app.extraction import extract_text_from_pdf
    resume_text = extract_text_from_pdf("myresume.pdf")

    sample_jd = "We are looking for a Python developer with experience in React, Docker, AWS, and MongoDB."

    result = compare_skills(resume_text, sample_jd)
    similarity = semantic_similarity(resume_text, sample_jd)
    final = compute_final_score(result["keyword_score"], similarity)

    print("Matched skills:", result["matched_skills"])
    print("Missing skills:", result["missing_skills"])
    print("Keyword score:", result["keyword_score"])
    print("Semantic similarity score:", similarity)
    print("FINAL MATCH SCORE:", final)
    suggestions = generate_suggestions(result["missing_skills"])
    print("Suggestions:")
    for s in suggestions:
        print("-", s)
