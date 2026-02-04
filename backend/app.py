from flask import Flask, request, jsonify
from resume_parser import parse_resume
from skill_matcher import match_skills
from bias_detector import check_bias

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload_resume():
    file = request.files["resume"]
    job_desc = request.form["job_desc"]

    file.save("temp.pdf")
    resume_text = parse_resume("temp.pdf")

    result = match_skills(resume_text, job_desc)
    bias_report = check_bias(job_desc)

    return jsonify({
        "analysis": result,
        "bias_report": bias_report
    })

if __name__ == "__main__":
    app.run(debug=False)
