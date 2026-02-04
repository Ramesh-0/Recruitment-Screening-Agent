import ollama

def match_skills(resume_text, job_description):
    prompt = f"""
    Compare this resume and job description.
    Resume: {resume_text}
    Job Description: {job_description}
    Return:
    - Matching skills
    - Missing skills
    - Overall match score out of 100
    """

    response = ollama.chat(model="llama3.2:1b", messages=[
        {"role": "user", "content": prompt}
    ])

    return response["message"]["content"]
