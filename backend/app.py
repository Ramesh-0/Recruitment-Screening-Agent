from flask import Flask, request, jsonify
from flask_cors import CORS
from resume_parser import parse_resume
from skill_matcher import match_skills
from bias_detector import check_bias
import os
import tempfile

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/upload", methods=["POST"])
def upload_resume():
    file = request.files["resume"]
    job_desc = request.form["job_desc"]

    # Use temporary file that auto-deletes
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
        temp_path = temp_file.name
        file.save(temp_path)
    
    try:
        resume_text = parse_resume(temp_path)
        result = match_skills(resume_text, job_desc)
        bias_report = check_bias(job_desc)
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return jsonify({
        "analysis": result,
        "bias_report": bias_report
    })

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)
