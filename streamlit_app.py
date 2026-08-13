import streamlit as st
import requests

st.set_page_config(page_title="Resume Matcher", page_icon="📄", layout="centered")
st.title("📄 Resume ↔ Job Description Matcher")
st.markdown("Upload your resume and paste a job description to see how well you match — and what to improve.")
st.divider()

resume_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])
job_description = st.text_area("Paste the job description here")

if st.button("Analyze"):
    if resume_file is not None and job_description.strip() != "":
        files = {"resume_file": (resume_file.name, resume_file.getvalue())}
        data = {"job_description": job_description}

        response = requests.post("http://127.0.0.1:8000/analyze", files=files, data=data)
        result = response.json()

        st.divider()
        st.subheader("Your Results")

        col1, col2, col3 = st.columns(3)
        col1.metric("Final Match Score", f"{result['final_score']}%")
        col2.metric("Keyword Score", f"{result['keyword_score']}%")
        col3.metric("Semantic Score", f"{result['semantic_score']}%")

        st.progress(min(int(result["final_score"]), 100) / 100)

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
        for suggestion in result["suggestions"]:
            st.info(suggestion)
    else:
        st.warning("Please upload a resume and paste a job description first.")