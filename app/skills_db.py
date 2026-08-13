SKILLS_DB = {
    "language": ["python", "javascript", "java", "c++", "c", "sql"],
    "web_frameworks": ["django", "flask", "react", "fastapi", "angular", "node.js"],
    "databases": ["postgresql", "mysql", "mongodb", "sqlite"],
    "cloud_devops": ["aws", "azure", "gcp", "docker", "kubernetes", "git", "linux"],
    "data_ml": ["tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "matplotlib", "machine learning"],
}

def get_all_skills():
    all_skills = []
    for category, skills in SKILLS_DB.items():
        all_skills.extend(skills)
    return all_skills

def get_skill_category(skill):
    for category, skills in SKILLS_DB.items():
        if skill in skills:
            return category
    return "other"

if __name__ == "__main__":
    print(get_all_skills())
    print(get_skill_category("docker"))
    print(get_skill_category("python"))