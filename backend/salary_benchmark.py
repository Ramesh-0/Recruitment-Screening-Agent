"""
Salary Benchmarking Module
Provides salary recommendations based on role, experience, and market data
"""

def benchmark_salary(job_title, location, years_experience, skills):
    """
    Estimate salary range based on role and market data
    
    Args:
        job_title: Job position title
        location: Geographic location
        years_experience: Years of relevant experience
        skills: List of key skills
    
    Returns:
        Salary benchmark data with ranges
    """
    
    # Salary base rates by common tech roles (USD annual)
    role_bases = {
        'software engineer': {'min': 80000, 'max': 150000, 'median': 110000},
        'senior software engineer': {'min': 120000, 'max': 200000, 'median': 155000},
        'frontend developer': {'min': 75000, 'max': 140000, 'median': 105000},
        'backend developer': {'min': 85000, 'max': 155000, 'median': 115000},
        'full stack developer': {'min': 90000, 'max': 160000, 'median': 120000},
        'data scientist': {'min': 95000, 'max': 170000, 'median': 125000},
        'devops engineer': {'min': 90000, 'max': 165000, 'median': 120000},
        'product manager': {'min': 100000, 'max': 180000, 'median': 135000},
        'data engineer': {'min': 95000, 'max': 170000, 'median': 125000},
        'machine learning engineer': {'min': 110000, 'max': 190000, 'median': 145000},
        'web developer': {'min': 70000, 'max': 130000, 'median': 95000}
    }
    
    # Location multipliers (relative to US national average)
    location_multipliers = {
        'san francisco': 1.45,
        'new york': 1.35,
        'seattle': 1.30,
        'boston': 1.25,
        'austin': 1.15,
        'denver': 1.10,
        'chicago': 1.10,
        'remote': 1.05,
        'atlanta': 1.05,
        'default': 1.0
    }
    
    # Premium skills that add to salary
    premium_skills = {
        'kubernetes': 5000,
        'aws': 8000,
        'azure': 7000,
        'gcp': 7000,
        'terraform': 5000,
        'react': 5000,
        'python': 5000,
        'golang': 8000,
        'rust': 10000,
        'machine learning': 10000,
        'ai': 10000,
        'blockchain': 12000
    }
    
    # Find matching role
    job_title_lower = job_title.lower()
    base_salary = None
    
    for role, data in role_bases.items():
        if role in job_title_lower:
            base_salary = data
            break
    
    if not base_salary:
        # Default for unknown roles
        base_salary = {'min': 75000, 'max': 140000, 'median': 100000}
    
    # Apply experience multiplier
    exp_multiplier = 1.0 + (min(years_experience, 10) * 0.05)  # 5% per year, cap at 10 years
    
    # Apply location multiplier
    location_lower = location.lower() if location else 'default'
    loc_multiplier = location_multipliers.get(location_lower, location_multipliers['default'])
    
    # Calculate skill premium
    skill_premium = 0
    if skills:
        skills_lower = [s.lower() for s in skills]
        for skill, premium in premium_skills.items():
            if any(skill in s for s in skills_lower):
                skill_premium += premium
    
    # Calculate final ranges
    min_salary = int((base_salary['min'] * exp_multiplier * loc_multiplier) + skill_premium)
    max_salary = int((base_salary['max'] * exp_multiplier * loc_multiplier) + skill_premium)
    median_salary = int((base_salary['median'] * exp_multiplier * loc_multiplier) + skill_premium)
    
    return {
        'job_title': job_title,
        'location': location or 'Not specified',
        'years_experience': years_experience,
        'salary_range': {
            'min': min_salary,
            'max': max_salary,
            'median': median_salary,
            'currency': 'USD'
        },
        'market_position': get_market_position(median_salary),
        'factors': {
            'base_role': base_salary['median'],
            'experience_adjustment': f'+{int((exp_multiplier - 1) * 100)}%',
            'location_adjustment': f'+{int((loc_multiplier - 1) * 100)}%',
            'skill_premium': f'+${skill_premium:,}'
        },
        'recommendation': generate_salary_recommendation(min_salary, max_salary, median_salary)
    }


def get_market_position(salary):
    """Determine market position of salary"""
    if salary >= 150000:
        return "Top 10% - Highly competitive"
    elif salary >= 120000:
        return "Top 25% - Above market average"
    elif salary >= 90000:
        return "Market average - Competitive"
    else:
        return "Below market average - Entry to mid-level"


def generate_salary_recommendation(min_sal, max_sal, median_sal):
    """Generate hiring recommendation based on salary analysis"""
    return f"""**Salary Recommendation:**

- **Target Offer**: ${median_sal:,} (Market median)
- **Negotiation Range**: ${min_sal:,} - ${max_sal:,}
- **Competitive Offer**: ${int(median_sal * 1.1):,}+ (10% above median)

**Notes**: 
- Consider candidate's total experience and skill level
- Factor in benefits package (health, equity, bonus)
- Adjust for remote vs on-site work arrangement
- Review annually based on performance
"""


def extract_salary_info_from_resume(resume_text, job_desc):
    """
    Extract salary-relevant information from resume and job description
    Helper function to prepare data for benchmarking
    """
    import re
    
    # Extract years of experience
    year_patterns = re.findall(r'(\d+)\+?\s*years?', resume_text.lower())
    years_exp = max([int(y) for y in year_patterns]) if year_patterns else 2
    
    # Extract skills
    skill_keywords = ['python', 'javascript', 'react', 'node', 'aws', 'kubernetes', 'docker', 
                     'sql', 'mongodb', 'golang', 'rust', 'machine learning', 'ai', 'terraform']
    skills = [skill for skill in skill_keywords if skill in resume_text.lower() or skill in job_desc.lower()]
    
    return years_exp, skills
