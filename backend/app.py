from flask import Flask, request, jsonify
from flask_cors import CORS
from resume_parser import parse_resume
from skill_matcher import match_skills
from bias_detector import check_bias
from candidate_ranker import rank_candidates
from interview_questions import generate_interview_questions
from culture_fit import assess_culture_fit
from salary_benchmark import benchmark_salary, extract_salary_info_from_resume
from scheduler import schedule_interview, get_available_slots, cancel_interview, get_scheduled_interviews
from offer_letter import generate_offer_letter, generate_quick_offer
import os
import tempfile
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/upload", methods=["POST"])
def upload_resume():
    file = request.files["resume"]
    job_desc = request.form["job_desc"]
    company_values = request.form.get("company_values", "")
    job_location = request.form.get("location", "")

    # Use temporary file that auto-deletes
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
        temp_path = temp_file.name
        file.save(temp_path)
    
    try:
        resume_text = parse_resume(temp_path)
        
        # Core analysis
        skill_analysis = match_skills(resume_text, job_desc)
        bias_report = check_bias(job_desc)
        
        # New features
        culture_fit = assess_culture_fit(resume_text, company_values, job_desc)
        interview_qs = generate_interview_questions(job_desc, resume_text, num_questions=5)
        
        # Salary benchmarking
        years_exp, skills = extract_salary_info_from_resume(resume_text, job_desc)
        job_title = extract_job_title(job_desc)
        salary_data = benchmark_salary(job_title, job_location, years_exp, skills)
        
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return jsonify({
        "analysis": skill_analysis,
        "bias_report": bias_report,
        "culture_fit": culture_fit,
        "interview_questions": interview_qs,
        "salary_benchmark": salary_data
    })


@app.route("/batch", methods=["POST"])
def batch_process():
    """Process multiple resumes at once"""
    files = request.files.getlist("resumes")
    job_desc = request.form["job_desc"]
    company_values = request.form.get("company_values", "")
    
    if len(files) > 50:
        return jsonify({"error": "Maximum 50 resumes per batch"}), 400
    
    candidates = []
    
    for idx, file in enumerate(files):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
            temp_path = temp_file.name
            file.save(temp_path)
        
        try:
            resume_text = parse_resume(temp_path)
            skill_analysis = match_skills(resume_text, job_desc)
            culture_fit = assess_culture_fit(resume_text, company_values, job_desc)
            
            candidates.append({
                'name': file.filename.replace('.pdf', ''),
                'analysis': skill_analysis,
                'resume_text': resume_text,
                'culture_score': culture_fit.get('culture_score', 70)
            })
        except Exception as e:
            print(f"Error processing {file.filename}: {e}")
            continue
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    # Rank candidates
    ranked = rank_candidates(candidates, {'job_desc': job_desc})
    
    return jsonify({
        "total_candidates": len(ranked),
        "ranked_candidates": ranked[:10],  # Top 10
        "summary": {
            "excellent": len([c for c in ranked if c['total_score'] >= 85]),
            "good": len([c for c in ranked if 70 <= c['total_score'] < 85]),
            "moderate": len([c for c in ranked if 55 <= c['total_score'] < 70]),
            "poor": len([c for c in ranked if c['total_score'] < 55])
        }
    })


@app.route("/questions", methods=["POST"])
def get_interview_questions():
    """Generate interview questions endpoint"""
    data = request.get_json()
    job_desc = data.get('job_desc', '')
    resume_text = data.get('resume_text', '')
    num_questions = data.get('num_questions', 5)
    
    questions = generate_interview_questions(job_desc, resume_text, num_questions)
    return jsonify(questions)


@app.route("/salary", methods=["POST"])
def get_salary_benchmark():
    """Get salary benchmark endpoint"""
    data = request.get_json()
    job_title = data.get('job_title', 'Software Engineer')
    location = data.get('location', '')
    years_exp = data.get('years_experience', 3)
    skills = data.get('skills', [])
    
    salary_data = benchmark_salary(job_title, location, years_exp, skills)
    return jsonify(salary_data)


def extract_job_title(job_desc):
    """Extract job title from job description"""
    import re
    
    # Look for common patterns
    patterns = [
        r'(?:position|role|job):\s*([^\n]+)',
        r'(?:hiring|seeking)\s+(?:a\s+)?([a-zA-Z\s]+?)(?:\s+to|\s+for)',
        r'^([a-zA-Z\s]+)\s+(?:Position|Role|Job)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, job_desc, re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(1).strip()
    
    # Default fallback
    return "Software Engineer"


@app.route("/schedule", methods=["POST"])
def create_interview_schedule():
    """Schedule an interview"""
    data = request.get_json()
    
    result = schedule_interview(
        candidate_name=data.get('candidate_name'),
        candidate_email=data.get('candidate_email'),
        date=data.get('date'),
        time=data.get('time'),
        interview_type=data.get('interview_type', 'Technical'),
        duration_minutes=data.get('duration_minutes', 60)
    )
    
    return jsonify(result)


@app.route("/schedule/available", methods=["GET"])
def get_available_interview_slots():
    """Get available interview slots for a date"""
    date = request.args.get('date')
    interview_type = request.args.get('type', 'Technical')
    
    slots = get_available_slots(date, interview_type)
    return jsonify({'date': date, 'available_slots': slots})


@app.route("/schedule/list", methods=["GET"])
def list_scheduled_interviews():
    """List all scheduled interviews"""
    date = request.args.get('date')
    interviews = get_scheduled_interviews(date)
    return jsonify({'interviews': interviews, 'count': len(interviews)})


@app.route("/schedule/cancel/<int:interview_id>", methods=["POST"])
def cancel_interview_endpoint(interview_id):
    """Cancel an interview"""
    data = request.get_json()
    reason = data.get('reason', '')
    
    result = cancel_interview(interview_id, reason)
    return jsonify(result)


@app.route("/offer", methods=["POST"])
def create_offer_letter():
    """Generate an offer letter"""
    data = request.get_json()
    
    candidate_data = data.get('candidate_data', {})
    job_details = data.get('job_details', {})
    salary_data = data.get('salary_data', {})
    company_info = data.get('company_info')
    
    offer = generate_offer_letter(candidate_data, job_details, salary_data, company_info)
    return jsonify(offer)


@app.route("/offer/quick", methods=["POST"])
def create_quick_offer():
    """Generate a quick offer letter with minimal details"""
    data = request.get_json()
    
    offer = generate_quick_offer(
        candidate_name=data.get('candidate_name'),
        job_title=data.get('job_title'),
        salary=data.get('salary')
    )
    
    return jsonify(offer)

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)
