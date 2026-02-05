import ollama

def check_bias(job_description):
    prompt = f"""CRITICAL: You must ONLY analyze the exact text provided below. DO NOT invent or imagine phrases.

JOB DESCRIPTION TO ANALYZE:
---START---
{job_description}
---END---

**RULES - READ CAREFULLY**:
1. ONLY flag phrases that ACTUALLY APPEAR in the text above
2. QUOTE the EXACT TEXT when reporting bias
3. If you cannot quote it, DO NOT report it
4. If NO bias found, say "No bias detected"
5. DO NOT use examples like "Rockstar", "ninja" unless they are IN THE TEXT

**CHECK FOR** (only if present):
- Gendered language (he/she, masculine/feminine coded words)
- Age terms ("young", "recent graduate", "energetic", "digital native")
- Cultural requirements ("native speaker", "cultural fit" undefined)
- Unnecessary physical requirements

**FORMAT**:

## Bias Found: [YES/NO]

[If YES, for EACH issue:]
### [Category] Bias
**Exact Quote**: "[copy exact text from job description]"
**Issue**: [Why problematic]
**Better Alternative**: "[neutral version]"

[If NO:]
### Analysis Result
No discriminatory language detected in this job description. The language used appears inclusive and focused on job-relevant qualifications.

**VERIFICATION CHECK**: Have you quoted actual text from the job description? If not, revise your answer."""

    response = ollama.chat(
        model="recruitment-screener",
        messages=[{"role": "user", "content": prompt}],
        options={
            "temperature": 0.1,
            "num_predict": 500
        }
    )

    return response["message"]["content"]
