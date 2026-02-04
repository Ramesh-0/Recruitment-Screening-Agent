import ollama

def check_bias(job_description):
    prompt = f"""
    Analyze this job description for bias:
    {job_description}

    Identify:
    - Gender bias
    - Age bias
    - Cultural bias
    - Language bias
    """

    response = ollama.chat(model="llama3.2:1b", messages=[
        {"role": "user", "content": prompt}
    ])

    return response["message"]["content"]
