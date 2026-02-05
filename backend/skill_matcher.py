import ollama

def match_skills(resume_text, job_description):
    prompt = f"""You are a VERY STRICT recruitment analyst. Score accurately based on actual skill overlap.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

**ULTRA-STRICT SCORING**:

1. LIST required skills from job (be specific)
2. CHECK each skill in resume - mark ✓ or ✗
3. BASE SCORE = (✓ skills / total skills) × 100

4. MANDATORY PENALTIES:
   - WRONG FIELD (web dev vs data science, frontend vs backend): START WITH 30/100 MAX
   - Missing core skill: -20 points EACH
   - Missing required degree: -25 points
   - Missing required experience level: -15 points

5. DOMAIN MATCH RULE:
   - Same domain (web→web, data→data): Use base score
   - Different domain: MAX score is 35/100, regardless of transferable skills
   - Opposite domain (frontend→backend): MAX score is 25/100

**IMPORTANT**: 
- "Python" for data science ≠ "JavaScript" for web
- React/Vue skills are WORTHLESS for data science jobs
- Web development skills DON'T transfer to data science
- If candidate is in WRONG FIELD, score must be <40

**OUTPUT**:

## Match Score: [X]/100

## Domain Check:
Resume field: [field]
Job field: [field]
Match: [YES/NO] - [If NO: "Domain mismatch penalty applied"]

## Skills Checklist:
[For each required skill]
✓/✗ [Skill name] - [Status]

## Penalties Applied:
- Domain mismatch: -[X] or "N/A"
- Missing core skills: -[X]
- Missing qualifications: -[X]
**Final Score: [X]/100**

## Verdict:
[STRONG MATCH / MODERATE MATCH / WEAK MATCH / POOR MATCH]

## One-line Recommendation:
[Brief suggestion]

Remember: Different fields = score must be <35"""

    response = ollama.chat(
        model="recruitment-screener",
        messages=[{"role": "user", "content": prompt}],
        options={
            "temperature": 0.05,
            "num_predict": 600
        }
    )

    return response["message"]["content"]
