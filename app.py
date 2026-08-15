import streamlit as st
from app.extraction import extract_text_from_pdf, extract_text_from_docx
from app.matcher import compare_skills, semantic_similarity, compute_final_score, generate_suggestions

st.set_page_config(page_title="Resume Matcher", page_icon="📄", layout="centered")
st.title("📄 Resume ↔ Job Description Matcher")
st.markdown("Upload your resume and paste a job description to see how well you match — and what to improve.")
st.divider()

resume_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])
job_description = st.text_area("Paste the job description here")

if st.button("Analyze"):
    if resume_file is not None and job_description.strip() != "":
        temp_path = "temp_" + resume_file.name
        with open(temp_path, "wb") as f:
            f.write(resume_file.getvalue())

        if resume_file.name.endswith(".pdf"):
            resume_text = extract_text_from_pdf(temp_path)
        else:
            resume_text = extract_text_from_docx(temp_path)

        result = compare_skills(resume_text, job_description)
        similarity = semantic_similarity(resume_text, job_description)
        final = compute_final_score(result["keyword_score"], similarity)
        suggestions = generate_suggestions(result["missing_skills"])

        st.divider()
        st.subheader("Your Results")

        col1, col2, col3 = st.columns(3)
        col1.metric("Final Match Score", f"{final}%")
        col2.metric("Keyword Score", f"{result['keyword_score']}%")
        col3.metric("Semantic Score", f"{similarity}%")

        st.progress(min(int(final), 100) / 100)
        st.divider()

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("### ✅ Matched Skills")
            for skill in result["matched_skills"]:
                st.success(skill)

        with col_b:
            st.markdown("### ❌ Missing Skills")
            for skill in result["missing_skills"]:
                st.error(skill)

        st.divider()
        st.markdown("### 💡 Suggestions to Improve Your Resume")
        for suggestion in suggestions:
            st.info(suggestion)
    else:
        st.warning("Please upload a resume and paste a job description first.")