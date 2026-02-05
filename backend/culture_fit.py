"""
Culture Fit Assessment
Analyzes candidate values, work style, and team compatibility
"""

import requests

def assess_culture_fit(resume_text, company_values, job_desc):
    """
    Assess candidate's cultural fit based on resume and company values
    
    Args:
        resume_text: Candidate resume content
        company_values: Company culture description
        job_desc: Job description with team details
    
    Returns:
        Culture fit analysis with score
    """
    
    # Default company values if not provided
    if not company_values:
        company_values = "collaborative, innovative, results-driven, growth mindset"
    
    prompt = f"""Analyze this candidate's cultural fit for the organization.

COMPANY VALUES:
{company_values}

JOB CONTEXT:
{job_desc[:300]}

CANDIDATE BACKGROUND:
{resume_text[:500]}

Assess cultural fit based on:
1. **Team Collaboration**: Evidence of teamwork and collaboration
2. **Innovation**: Shows initiative, learning, and adaptability
3. **Work Style**: Matches team dynamics and work environment
4. **Values Alignment**: Personal values align with company culture

Provide:
- Culture Fit Score: X/100
- Key Strengths: List 2-3 cultural strengths
- Potential Concerns: List any red flags
- Overall Assessment: 2-3 sentences

Be objective and evidence-based. Look for indicators in their experience, projects, and communication style.
"""

    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'recruitment-screener',
                'prompt': prompt,
                'stream': False,
                'options': {
                    'temperature': 0.3,
                    'num_predict': 400
                }
            },
            timeout=45
        )
        
        if response.status_code == 200:
            result = response.json()
            analysis = result.get('response', '')
            
            # Extract score
            import re
            score_match = re.search(r'(?:Culture Fit Score|Score).*?(\d+)/100', analysis, re.IGNORECASE)
            score = int(score_match.group(1)) if score_match else 70
            
            return {
                'culture_score': score,
                'analysis': analysis,
                'recommendation': get_culture_recommendation(score)
            }
        else:
            return generate_fallback_culture_assessment(resume_text)
            
    except Exception as e:
        print(f"Error assessing culture fit: {e}")
        return generate_fallback_culture_assessment(resume_text)


def get_culture_recommendation(score):
    """Get recommendation based on culture fit score"""
    if score >= 85:
        return "EXCELLENT FIT - Strong cultural alignment"
    elif score >= 70:
        return "GOOD FIT - Suitable cultural match"
    elif score >= 55:
        return "MODERATE FIT - Some concerns about cultural alignment"
    else:
        return "POOR FIT - Significant cultural misalignment"


def generate_fallback_culture_assessment(resume_text):
    """Generate basic culture assessment if AI fails"""
    
    # Simple keyword-based assessment
    collaboration_keywords = ['team', 'collaborated', 'partnership', 'cross-functional']
    innovation_keywords = ['innovative', 'created', 'developed', 'improved', 'optimized']
    leadership_keywords = ['led', 'managed', 'mentored', 'coordinated']
    
    collab_count = sum(1 for kw in collaboration_keywords if kw in resume_text.lower())
    innov_count = sum(1 for kw in innovation_keywords if kw in resume_text.lower())
    leader_count = sum(1 for kw in leadership_keywords if kw in resume_text.lower())
    
    # Calculate simple score
    base_score = 60
    score = base_score + (collab_count * 5) + (innov_count * 5) + (leader_count * 3)
    score = min(100, score)
    
    analysis = f"""**Culture Fit Assessment**

**Collaboration**: {'Strong' if collab_count >= 2 else 'Moderate'} evidence of teamwork
**Innovation**: {'Strong' if innov_count >= 2 else 'Moderate'} signs of innovative thinking
**Leadership**: {'Strong' if leader_count >= 2 else 'Moderate'} leadership indicators

**Culture Fit Score**: {score}/100

**Overall Assessment**: Based on resume analysis, candidate shows {'strong' if score >= 75 else 'adequate'} cultural alignment with focus on {'collaboration and innovation' if collab_count + innov_count >= 4 else 'professional growth'}.
"""
    
    return {
        'culture_score': score,
        'analysis': analysis,
        'recommendation': get_culture_recommendation(score)
    }
