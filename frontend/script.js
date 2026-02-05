// File input handling
document.getElementById('resume').addEventListener('change', function(e) {
    const fileName = e.target.files[0]?.name || 'Choose PDF file...';
    document.getElementById('file-name').textContent = fileName;
    
    if (e.target.files[0]) {
        document.querySelector('.file-input-wrapper').classList.add('file-selected');
    }
});

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
    // Format and display analysis
    const analysisOutput = document.getElementById("analysis-output");
    analysisOutput.innerHTML = formatAnalysis(data.analysis);
    
    // Format and display bias report
    const biasOutput = document.getElementById("bias-output");
    biasOutput.innerHTML = formatBiasReport(data.bias_report);
    
    // Show results section
    document.getElementById("results").classList.remove("hidden");
    
    // Smooth scroll to results
    document.getElementById("results").scrollIntoView({ behavior: 'smooth', block: 'nearest' });
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
