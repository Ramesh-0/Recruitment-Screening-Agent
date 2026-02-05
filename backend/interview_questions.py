"""
Interview Question Generator
Generates role-specific interview questions based on job requirements
"""

import requests
import json

def generate_interview_questions(job_desc, resume_text, num_questions=5):
    """
    Generate interview questions based on job requirements and candidate profile
    
    Args:
        job_desc: Job description text
        resume_text: Candidate resume text
        num_questions: Number of questions to generate (default 5)
    
    Returns:
        List of interview questions with categories
    """
    
    prompt = f"""Based on this job description and candidate resume, generate {num_questions} targeted interview questions.

JOB DESCRIPTION:
{job_desc[:500]}

CANDIDATE BACKGROUND:
{resume_text[:500]}

Generate interview questions in these categories:
1. Technical Skills (2 questions)
2. Experience & Projects (2 questions)
3. Cultural Fit (1 question)

Format each question as:
**Category**: Question text

Focus on:
- Verifying skills mentioned in resume
- Assessing gaps identified in job requirements
- Understanding project experience depth
- Evaluating problem-solving abilities
"""

    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'recruitment-screener',
                'prompt': prompt,
                'stream': False,
                'options': {
                    'temperature': 0.7,
                    'num_predict': 500
                }
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            questions_text = result.get('response', '')
            
            # Parse questions into structured format
            questions = parse_questions(questions_text)
            
            return {
                'questions': questions,
                'raw_output': questions_text
            }
        else:
            return generate_fallback_questions(job_desc)
            
    except Exception as e:
        print(f"Error generating questions: {e}")
        return generate_fallback_questions(job_desc)


def parse_questions(text):
    """Parse AI-generated questions into structured format"""
    import re
    
    questions = []
    lines = text.split('\n')
    
    current_category = "General"
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if line is a category
        if '**' in line or line.endswith(':'):
            current_category = line.replace('**', '').replace(':', '').strip()
        # Check if line is a question (starts with number or bullet)
        elif re.match(r'^[\d\-\*\•]', line):
            question_text = re.sub(r'^[\d\-\*\•\.\)]+\s*', '', line)
            if len(question_text) > 10:  # Valid question
                questions.append({
                    'category': current_category,
                    'question': question_text
                })
    
    return questions if questions else generate_default_questions()


def generate_fallback_questions(job_desc):
    """Generate default questions if AI generation fails"""
    
    # Extract key skills from job description
    common_skills = ['python', 'javascript', 'react', 'node', 'sql', 'aws', 'docker', 'agile']
    found_skills = [skill for skill in common_skills if skill.lower() in job_desc.lower()]
    
    questions = [
        {
            'category': 'Technical Skills',
            'question': f"Can you walk me through a recent project where you used {found_skills[0] if found_skills else 'your primary technology'}?"
        },
        {
            'category': 'Technical Skills',
            'question': "Describe a challenging technical problem you solved. What was your approach?"
        },
        {
            'category': 'Experience',
            'question': "Tell me about your most impactful project. What was your role and contribution?"
        },
        {
            'category': 'Experience',
            'question': "How do you stay updated with new technologies and industry trends?"
        },
        {
            'category': 'Cultural Fit',
            'question': "Describe a situation where you had to work with a difficult team member. How did you handle it?"
        }
    ]
    
    return {
        'questions': questions,
        'raw_output': 'Fallback questions generated'
    }


def generate_default_questions():
    """Generate basic default questions"""
    return [
        {'category': 'Technical', 'question': 'Describe your technical experience'},
        {'category': 'Experience', 'question': 'Tell me about your recent projects'},
        {'category': 'Cultural Fit', 'question': 'How do you handle team collaboration?'}
    ]
