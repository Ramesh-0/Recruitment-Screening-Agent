// File input handling - Single Resume
document.getElementById('resume').addEventListener('change', function(e) {
    const fileName = e.target.files[0]?.name || 'Choose PDF file...';
    document.getElementById('file-name').textContent = fileName;
    
    if (e.target.files[0]) {
        document.querySelector('.file-input-wrapper').classList.add('file-selected');
    }
});

// File input handling - Batch Resumes
document.getElementById('batch-resumes').addEventListener('change', function(e) {
    const fileCount = e.target.files.length;
    const fileName = fileCount > 0 ? `${fileCount} file(s) selected` : 'Choose PDF files (up to 50)...';
    document.getElementById('batch-file-name').textContent = fileName;
    
    if (fileCount > 0) {
        document.querySelectorAll('.file-input-wrapper')[1].classList.add('file-selected');
    }
});

// Mode Switching
function switchMode(mode) {
    // Update tab states
    document.querySelectorAll('.mode-tab').forEach(tab => tab.classList.remove('active'));
    event.target.classList.add('active');
    
    // Hide all modes
    document.querySelectorAll('.mode-content').forEach(content => content.classList.add('hidden'));
    
    // Show selected mode
    document.getElementById(`${mode}-mode`).classList.remove('hidden');
    
    // Hide error messages
    document.getElementById('error').classList.add('hidden');
}

// Result Tab Switching
function switchResultTab(tab) {
    // Update tab states
    document.querySelectorAll('.result-tab').forEach(t => t.classList.remove('active'));
    event.target.classList.add('active');
    
    // Hide all tab contents
    document.querySelectorAll('.result-tab-content').forEach(content => content.classList.remove('active'));
    
    // Show selected tab
    document.getElementById(`${tab}-tab`).classList.add('active');
}

// Single Resume Analysis
async function submitData() {
    const resumeFile = document.getElementById("resume").files[0];
    const jobDesc = document.getElementById("job_desc").value.trim();
    
    // Validation
    if (!resumeFile) {
        showError("Please select a resume PDF file");
        return;
    }
    
    if (!jobDesc) {
        showError("Please enter a job description");
        return;
    }
    
    if (!resumeFile.name.toLowerCase().endsWith('.pdf')) {
        showError("Please upload a PDF file");
        return;
    }
    
    // Hide previous results and errors
    document.getElementById("results").classList.add("hidden");
    document.getElementById("error").classList.add("hidden");
    
    // Show loading state with time estimate
    const btnText = document.getElementById("btn-text");
    const loading = document.getElementById("loading");
    const analyzeBtn = document.querySelector(".analyze-btn");
    
    btnText.classList.add("hidden");
    loading.innerHTML = '<span class="spinner"></span> Analyzing (may take 30-60s)...';
    loading.classList.remove("hidden");
    analyzeBtn.disabled = true;
    
    // Add timeout warning after 30 seconds
    const timeoutWarning = setTimeout(() => {
        loading.innerHTML = '<span class="spinner"></span> Still processing... AI analysis in progress...';
    }, 30000);
    
    try {
        let formData = new FormData();
        formData.append("resume", resumeFile);
        formData.append("job_desc", jobDesc);

        let response = await fetch("http://127.0.0.1:5000/upload", {
            method: "POST",
            body: formData
        });

        clearTimeout(timeoutWarning);

        if (!response.ok) {
            throw new Error(`Server error: ${response.status} ${response.statusText}`);
        }

        let data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        displayResults(data);
        
    } catch (error) {
        clearTimeout(timeoutWarning);
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            showError(`Connection error: Make sure the Flask server is running on http://127.0.0.1:5000`);
        } else {
            showError(`Error: ${error.message}. Please try again or check server logs.`);
        }
    } finally {
        // Reset button state
        btnText.classList.remove("hidden");
        loading.classList.add("hidden");
        analyzeBtn.disabled = false;
    }
}

function displayResults(data) {
    // Overview Tab - Summary
    const summaryOutput = document.getElementById("summary-output");
    summaryOutput.innerHTML = formatAnalysis(data.analysis);
    
    // Overview Tab - Stats
    const statsOutput = document.getElementById("stats-output");
    statsOutput.innerHTML = generateStatsHTML(data);
    
    // Skills Tab
    const analysisOutput = document.getElementById("analysis-output");
    analysisOutput.innerHTML = formatAnalysis(data.analysis);
    
    // Bias Tab
    const biasOutput = document.getElementById("bias-output");
    biasOutput.innerHTML = formatBiasReport(data.bias_report);
    
    // Culture Fit Tab
    const cultureOutput = document.getElementById("culture-output");
    if (data.culture_fit) {
        cultureOutput.innerHTML = formatCultureFit(data.culture_fit);
    } else {
        cultureOutput.innerHTML = '<p class="info-text">Culture fit data not available</p>';
    }
    
    // Salary Tab
    const salaryOutput = document.getElementById("salary-output");
    if (data.salary_benchmark) {
        salaryOutput.innerHTML = formatSalaryBenchmark(data.salary_benchmark);
    } else {
        salaryOutput.innerHTML = '<p class="info-text">Salary benchmark data not available</p>';
    }
    
    // Questions Tab
    const questionsOutput = document.getElementById("questions-output");
    if (data.interview_questions) {
        questionsOutput.innerHTML = formatInterviewQuestions(data.interview_questions);
    } else {
        questionsOutput.innerHTML = '<p class="info-text">Interview questions not available</p>';
    }
    
    // Show results section
    document.getElementById("results").classList.remove("hidden");
    
    // Smooth scroll to results
    document.getElementById("results").scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function generateStatsHTML(data) {
    let html = '';
    
    // Culture Fit Score
    if (data.culture_fit && data.culture_fit.culture_score) {
        html += `
            <div class="stat-item">
                <div class="stat-label">Culture Fit Score</div>
                <div class="stat-value">${data.culture_fit.culture_score}/100</div>
            </div>
        `;
    }
    
    // Salary Range
    if (data.salary_benchmark && data.salary_benchmark.salary_range) {
        const median = data.salary_benchmark.salary_range.median;
        html += `
            <div class="stat-item">
                <div class="stat-label">Est. Salary</div>
                <div class="stat-value">$${(median/1000).toFixed(0)}k</div>
            </div>
        `;
    }
    
    // Interview Questions Count
    if (data.interview_questions && data.interview_questions.questions) {
        html += `
            <div class="stat-item">
                <div class="stat-label">Interview Questions</div>
                <div class="stat-value">${data.interview_questions.questions.length}</div>
            </div>
        `;
    }
    
    return html || '<p class="info-text">No quick stats available</p>';
}

function formatCultureFit(cultureFit) {
    let html = `
        <div style="margin-bottom: 20px;">
            <h3 style="color: var(--primary-color);">Overall Score: ${cultureFit.culture_score}/100</h3>
            <p><strong>Recommendation:</strong> ${cultureFit.recommendation || 'N/A'}</p>
        </div>
    `;
    
    if (cultureFit.analysis) {
        html += `<p>${formatText(cultureFit.analysis)}</p>`;
    }
    
    if (cultureFit.strengths && cultureFit.strengths.length > 0) {
        html += `<h4>✅ Cultural Strengths:</h4><ul>`;
        cultureFit.strengths.forEach(strength => {
            html += `<li>${strength}</li>`;
        });
        html += `</ul>`;
    }
    
    if (cultureFit.concerns && cultureFit.concerns.length > 0) {
        html += `<h4>⚠️ Potential Concerns:</h4><ul>`;
        cultureFit.concerns.forEach(concern => {
            html += `<li>${concern}</li>`;
        });
        html += `</ul>`;
    }
    
    return html;
}

function formatSalaryBenchmark(salary) {
    let html = '';
    
    if (salary.salary_range) {
        const range = salary.salary_range;
        html += `
            <div style="margin-bottom: 20px;">
                <h3 style="color: var(--primary-color);">Salary Range</h3>
                <p><strong>Minimum:</strong> $${range.min.toLocaleString()}</p>
                <p><strong>Median:</strong> $${range.median.toLocaleString()}</p>
                <p><strong>Maximum:</strong> $${range.max.toLocaleString()}</p>
            </div>
        `;
    }
    
    if (salary.market_position) {
        html += `<p><strong>Market Position:</strong> ${salary.market_position}</p>`;
    }
    
    if (salary.recommendation) {
        html += `<p>${formatText(salary.recommendation)}</p>`;
    }
    
    if (salary.breakdown) {
        html += `<h4>💡 Breakdown:</h4><p>${formatText(salary.breakdown)}</p>`;
    }
    
    return html;
}

function formatInterviewQuestions(questions) {
    if (!questions.questions || questions.questions.length === 0) {
        return '<p>No questions generated</p>';
    }
    
    let html = '<div style="line-height: 2;">';
    
    let currentCategory = '';
    questions.questions.forEach((q, index) => {
        if (q.category && q.category !== currentCategory) {
            if (currentCategory !== '') html += '</ol>';
            html += `<h4 style="margin-top: 20px; color: var(--primary-color);">📌 ${q.category}</h4><ol>`;
            currentCategory = q.category;
        } else if (index === 0) {
            html += '<ol>';
        }
        
        html += `<li style="margin-bottom: 15px;"><strong>${q.question}</strong></li>`;
    });
    
    html += '</ol></div>';
    return html;
}

function formatText(text) {
    return text.replace(/\n/g, '<br>');
}

// Batch Processing
async function submitBatchData() {
    const files = document.getElementById("batch-resumes").files;
    const jobDesc = document.getElementById("batch-job-desc").value.trim();
    
    if (files.length === 0) {
        showError("Please select at least one resume");
        return;
    }
    
    if (files.length > 50) {
        showError("Maximum 50 resumes allowed");
        return;
    }
    
    if (!jobDesc) {
        showError("Please enter a job description");
        return;
    }
    
    document.getElementById("batch-results").classList.add("hidden");
    document.getElementById("error").classList.add("hidden");
    
    const btnText = document.getElementById("batch-btn-text");
    const loading = document.getElementById("batch-loading");
    
    btnText.classList.add("hidden");
    loading.innerHTML = `<span class="spinner"></span> Processing ${files.length} resume(s)...`;
    loading.classList.remove("hidden");
    
    try {
        let formData = new FormData();
        for (let file of files) {
            formData.append("resumes", file);
        }
        formData.append("job_desc", jobDesc);
        
        let response = await fetch("http://127.0.0.1:5000/batch", {
            method: "POST",
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        
        let data = await response.json();
        displayBatchResults(data);
        
    } catch (error) {
        showError(`Error: ${error.message}`);
    } finally {
        btnText.classList.remove("hidden");
        loading.classList.add("hidden");
    }
}

function displayBatchResults(data) {
    // Summary
    const summary = document.getElementById("batch-summary");
    summary.innerHTML = `
        <div class="summary-stat">
            <div class="summary-stat-value">${data.total_processed}</div>
            <div class="summary-stat-label">Total Processed</div>
        </div>
        <div class="summary-stat">
            <div class="summary-stat-value">${data.summary.excellent || 0}</div>
            <div class="summary-stat-label">Excellent</div>
        </div>
        <div class="summary-stat">
            <div class="summary-stat-value">${data.summary.good || 0}</div>
            <div class="summary-stat-label">Good</div>
        </div>
        <div class="summary-stat">
            <div class="summary-stat-value">${data.summary.moderate || 0}</div>
            <div class="summary-stat-label">Moderate</div>
        </div>
        <div class="summary-stat">
            <div class="summary-stat-value">${data.summary.poor || 0}</div>
            <div class="summary-stat-label">Poor</div>
        </div>
    `;
    
    // Ranking Table
    const ranking = document.getElementById("batch-ranking");
    let html = `
        <table>
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Candidate</th>
                    <th>Skill Score</th>
                    <th>Exp Score</th>
                    <th>Total Score</th>
                    <th>Recommendation</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    data.ranked_candidates.forEach((candidate, index) => {
        const rankClass = index < 3 ? `rank-${index + 1}` : 'rank-other';
        const scoreClass = getScoreClass(candidate.total_score);
        const recClass = getRecommendationClass(candidate.recommendation);
        
        html += `
            <tr>
                <td><span class="rank-badge ${rankClass}">${index + 1}</span></td>
                <td><strong>${candidate.name}</strong></td>
                <td>${candidate.skill_score.toFixed(1)}</td>
                <td>${candidate.experience_score.toFixed(1)}</td>
                <td><span class="score-badge ${scoreClass}">${candidate.total_score.toFixed(1)}</span></td>
                <td><span class="recommendation-badge ${recClass}">${candidate.recommendation}</span></td>
            </tr>
        `;
    });
    
    html += `</tbody></table>`;
    ranking.innerHTML = html;
    
    document.getElementById("batch-results").classList.remove("hidden");
    document.getElementById("batch-results").scrollIntoView({ behavior: 'smooth' });
}

function getScoreClass(score) {
    if (score >= 80) return 'score-excellent';
    if (score >= 60) return 'score-good';
    if (score >= 40) return 'score-moderate';
    return 'score-poor';
}

function getRecommendationClass(rec) {
    if (rec === 'STRONG HIRE') return 'rec-strong-hire';
    if (rec === 'HIRE') return 'rec-hire';
    if (rec === 'MAYBE') return 'rec-maybe';
    return 'rec-no-hire';
}

// Interview Scheduling
async function scheduleInterview() {
    const name = document.getElementById("candidate-name").value.trim();
    const email = document.getElementById("candidate-email").value.trim();
    const date = document.getElementById("interview-date").value;
    const time = document.getElementById("interview-time").value;
    const type = document.getElementById("interview-type").value;
    const duration = document.getElementById("interview-duration").value;
    
    if (!name || !email || !date || !time) {
        showError("Please fill in all required fields");
        return;
    }
    
    try {
        const response = await fetch("http://127.0.0.1:5000/schedule", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                candidate_name: name,
                candidate_email: email,
                date: date,
                time: time,
                interview_type: type,
                duration_minutes: parseInt(duration)
            })
        });
        
        if (!response.ok) throw new Error(`Error: ${response.status}`);
        
        const data = await response.json();
        displayScheduleResult(data);
        
        // Clear form
        document.getElementById("candidate-name").value = '';
        document.getElementById("candidate-email").value = '';
        document.getElementById("interview-date").value = '';
        document.getElementById("interview-time").value = '';
        
    } catch (error) {
        showError(`Scheduling error: ${error.message}`);
    }
}

function displayScheduleResult(data) {
    const output = document.getElementById("schedule-output");
    const interview = data.interview;
    
    output.innerHTML = `
        <p><strong>✅ Interview successfully scheduled!</strong></p>
        <p><strong>Candidate:</strong> ${interview.candidate_name}</p>
        <p><strong>Email:</strong> ${interview.candidate_email}</p>
        <p><strong>Date & Time:</strong> ${interview.date} at ${interview.time}</p>
        <p><strong>Type:</strong> ${interview.interview_type}</p>
        <p><strong>Duration:</strong> ${interview.duration_minutes} minutes</p>
        <p><strong>Meeting Link:</strong> <a href="${interview.meeting_link}" target="_blank">${interview.meeting_link}</a></p>
        <p><strong>Interview ID:</strong> ${interview.interview_id}</p>
    `;
    
    document.getElementById("schedule-results").classList.remove("hidden");
    document.getElementById("schedule-results").scrollIntoView({ behavior: 'smooth' });
    
    // Refresh the list
    loadScheduledInterviews();
}

async function loadScheduledInterviews() {
    try {
        const response = await fetch("http://127.0.0.1:5000/schedule/list");
        const data = await response.json();
        
        const listDiv = document.getElementById("scheduled-list");
        
        if (data.interviews.length === 0) {
            listDiv.innerHTML = '<p class="info-text">No scheduled interviews</p>';
            return;
        }
        
        let html = '';
        data.interviews.forEach(interview => {
            html += `
                <div class="interview-item">
                    <div class="interview-header">
                        <div class="interview-name">${interview.candidate_name}</div>
                        <div class="interview-type">${interview.interview_type}</div>
                    </div>
                    <div class="interview-details">
                        📅 ${interview.date} at ${interview.time}<br>
                        📧 ${interview.candidate_email}<br>
                        ⏱️ ${interview.duration_minutes} minutes<br>
                        🔗 <a href="${interview.meeting_link}" target="_blank">Join Meeting</a>
                    </div>
                    <button class="cancel-btn" onclick="cancelInterview('${interview.interview_id}')">
                        ❌ Cancel Interview
                    </button>
                </div>
            `;
        });
        
        listDiv.innerHTML = html;
        
    } catch (error) {
        showError(`Error loading interviews: ${error.message}`);
    }
}

async function cancelInterview(interviewId) {
    if (!confirm('Are you sure you want to cancel this interview?')) return;
    
    try {
        const response = await fetch(`http://127.0.0.1:5000/schedule/cancel/${interviewId}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ reason: "Cancelled by recruiter" })
        });
        
        if (!response.ok) throw new Error(`Error: ${response.status}`);
        
        loadScheduledInterviews();
        
    } catch (error) {
        showError(`Cancellation error: ${error.message}`);
    }
}

// Offer Letter Generation
async function generateOffer() {
    const name = document.getElementById("offer-candidate-name").value.trim();
    const email = document.getElementById("offer-candidate-email").value.trim();
    const title = document.getElementById("offer-job-title").value.trim();
    const dept = document.getElementById("offer-department").value.trim();
    const startDate = document.getElementById("offer-start-date").value;
    const salary = document.getElementById("offer-salary").value;
    const bonus = document.getElementById("offer-signing-bonus").value || 0;
    const shares = document.getElementById("offer-equity-shares").value || 0;
    
    if (!name || !email || !title || !dept || !startDate || !salary) {
        showError("Please fill in all required fields");
        return;
    }
    
    try {
        const response = await fetch("http://127.0.0.1:5000/offer", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                candidate_data: { name, email },
                job_details: {
                    title,
                    department: dept,
                    start_date: startDate
                },
                salary_data: {
                    salary: parseInt(salary),
                    signing_bonus: parseInt(bonus),
                    equity: { shares: parseInt(shares), strike_price: 10.0 }
                }
            })
        });
        
        if (!response.ok) throw new Error(`Error: ${response.status}`);
        
        const data = await response.json();
        displayOfferLetter(data.offer_letter);
        
    } catch (error) {
        showError(`Offer generation error: ${error.message}`);
    }
}

function displayOfferLetter(offerText) {
    const output = document.getElementById("offer-output");
    output.textContent = offerText;
    
    document.getElementById("offer-results").classList.remove("hidden");
    document.getElementById("offer-results").scrollIntoView({ behavior: 'smooth' });
}

function copyOfferLetter() {
    const offerText = document.getElementById("offer-output").textContent;
    navigator.clipboard.writeText(offerText).then(() => {
        alert('Offer letter copied to clipboard!');
    });
}

function formatAnalysis(text) {
    // Convert markdown-style text to properly formatted HTML
    let formatted = text
        // Bold: **text** or __text__
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/__(.+?)__/g, '<strong>$1</strong>')
        // Italic: *text* or _text_ (but not ** or __)
        .replace(/(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)/g, '<em>$1</em>')
        .replace(/(?<!_)_(?!_)(.+?)(?<!_)_(?!_)/g, '<em>$1</em>')
        // Headers
        .replace(/^### (.+)$/gm, '<h4>$1</h4>')
        .replace(/^## (.+)$/gm, '<h3>$1</h3>')
        // Lists (bullet points)
        .replace(/\n- (.+)/g, '\n<li>$1</li>')
        .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
        // Numbered lists
        .replace(/\n\d+\. (.+)/g, '\n<li>$1</li>')
        // Line breaks and paragraphs
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>');
    
    return `<p>${formatted}</p>`;
}

function formatBiasReport(text) {
    // Convert markdown-style bias report to formatted HTML
    let formatted = text
        // Bold: **text** or __text__
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/__(.+?)__/g, '<strong>$1</strong>')
        // Italic: *text* or _text_
        .replace(/(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)/g, '<em>$1</em>')
        .replace(/(?<!_)_(?!_)(.+?)(?<!_)_(?!_)/g, '<em>$1</em>')
        // Headers
        .replace(/^### (.+)$/gm, '<h4>$1</h4>')
        .replace(/^## (.+)$/gm, '<h3>$1</h3>')
        // Lists (bullet points)
        .replace(/\n- (.+)/g, '\n<li>$1</li>')
        .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
        // Line breaks and paragraphs
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>');
    
    return `<p>${formatted}</p>`;
}

function showError(message) {
    const errorDiv = document.getElementById("error");
    errorDiv.textContent = message;
    errorDiv.classList.remove("hidden");
    errorDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        errorDiv.classList.add("hidden");
    }, 5000);
}

// Load scheduled interviews on page load
window.addEventListener('load', () => {
    // Set minimum date to today for date inputs
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('interview-date').min = today;
    document.getElementById('offer-start-date').min = today;
});
