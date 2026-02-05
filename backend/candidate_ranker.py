"""
Candidate Ranking System
Ranks candidates based on multiple criteria: skills, experience, culture fit
"""

def rank_candidates(candidates, job_requirements):
    """
    Rank candidates based on match score and other criteria
    
    Args:
        candidates: List of dicts with 'name', 'score', 'analysis', 'resume_text'
        job_requirements: Dict with job description details
    
    Returns:
        Sorted list of candidates with ranking
    """
    ranked = []
    
    for idx, candidate in enumerate(candidates):
        # Extract score from analysis
        score = extract_score(candidate.get('analysis', ''))
        
        # Calculate ranking factors
        skill_score = score if score else 0
        experience_score = calculate_experience_score(candidate.get('resume_text', ''))
        
        # Calculate total ranking score
        total_score = (skill_score * 0.7) + (experience_score * 0.3)
        
        ranked.append({
            'rank': 0,  # Will be set after sorting
            'name': candidate.get('name', f'Candidate {idx+1}'),
            'skill_score': skill_score,  # Frontend expects 'skill_score'
            'skill_match_score': skill_score,  # Backwards compatibility
            'experience_score': experience_score,
            'total_score': round(total_score, 2),
            'analysis': candidate.get('analysis', ''),
            'recommendation': get_recommendation(total_score)
        })
    
    # Sort by total score descending
    ranked.sort(key=lambda x: x['total_score'], reverse=True)
    
    # Assign ranks
    for idx, candidate in enumerate(ranked):
        candidate['rank'] = idx + 1
    
    return ranked


def extract_score(analysis_text):
    """Extract numerical score from analysis text"""
    import re
    match = re.search(r'(?:Match Score|Final Score).*?(\d+)/100', analysis_text, re.IGNORECASE)
    return int(match.group(1)) if match else 50


def calculate_experience_score(resume_text):
    """
    Calculate experience score based on resume content
    Simple heuristic based on years mentioned
    """
    import re
    
    # Look for year patterns (e.g., "5+ years", "3 years")
    year_patterns = re.findall(r'(\d+)\+?\s*years?', resume_text.lower())
    
    if year_patterns:
        max_years = max([int(y) for y in year_patterns])
        # Cap at 100, scale linearly (10 years = 100)
        return min(100, max_years * 10)
    
    # Look for job titles/positions as proxy
    experience_keywords = ['senior', 'lead', 'manager', 'director', 'principal', 'architect']
    count = sum(1 for keyword in experience_keywords if keyword in resume_text.lower())
    
    return min(100, count * 15)


def get_recommendation(score):
    """Get hiring recommendation based on total score"""
    if score >= 85:
        return "STRONG HIRE - Excellent match, proceed to interview"
    elif score >= 70:
        return "HIRE - Good match, recommend interview"
    elif score >= 55:
        return "MAYBE - Adequate match, consider if no better candidates"
    else:
        return "NO HIRE - Poor match, not recommended"
