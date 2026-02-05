# 🤖 AI Recruitment Screening Agent

An AI-powered recruitment system that automates resume screening, skill matching, bias detection, and interview scheduling. Built with Flask, Ollama AI, and modern web technologies to process resumes at scale and reduce time-to-hire by 50%.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

## ✨ Features

- **📄 Resume Parsing**: Extract and analyze text from PDF resumes with automatic cleanup
- **🎯 Skill Matching**: AI-powered skill comparison between resume and job description
- **⚖️ Bias Detection**: Identify gender, age, cultural, and language bias in job descriptions
- **📊 Match Scoring**: Quantitative assessment (0-100) of candidate fit
- **🎨 Modern UI**: Responsive bento-box grid layout with custom logo and beige/olive green theme
- **✨ Professional Output**: Proper markdown rendering without asterisks - bold, italic, lists, and headers
- **⚡ Real-time Analysis**: Fast processing with loading indicators and error handling
- **🗑️ Auto-Cleanup**: Temporary files automatically deleted after processing

## 🏗️ Architecture

```
Recruitment-Screening-Agent/
├── backend/
│   ├── app.py                 # Flask API server with auto-cleanup
│   ├── resume_parser.py       # PDF text extraction
│   ├── skill_matcher.py       # AI skill comparison (optimized)
│   ├── bias_detector.py       # Bias analysis (hallucination-free)
│   ├── scheduler.py           # Interview scheduling (future)
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── index.html            # Main UI with logo
│   ├── style.css             # Beige/olive green bento design
│   ├── script.js             # Frontend logic & markdown rendering
│   └── logo.svg              # Custom AI recruitment logo
├── test_cases/
│   ├── webdev_job_description.txt
│   └── webdev_resume_sample.pdf
├── docs/
│   └── FINAL_CONCLUSION.md   # Production readiness report
├── .gitignore                # Git ignore rules
├── LICENSE                   # MIT License
├── Modelfile                 # Custom Ollama model configuration
└── README.md                 # This file
```
## Demo


https://github.com/user-attachments/assets/3743078e-c348-429d-b154-25010700e327



## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.ai/) installed and running
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Recruitment-Screening-Agent
   ```

2. **Set up Python environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Create custom Ollama model**
   ```bash
   ollama create recruitment-screener -f Modelfile
   ```
   
   This creates a specialized model optimized for recruitment screening with:
   - Custom system prompts for resume analysis
   - Bias detection expertise
   - Structured output formatting
   - Professional assessment capabilities

5. **Verify model installation**
   ```bash
   ollama list
   ```
   You should see `recruitment-screener` in the list.

## 🎮 Usage

### Starting the Application

1. **Start the backend server**
   ```bash
   cd backend
   python app.py
   ```
   Server runs on `http://127.0.0.1:5000`

2. **Start the frontend**
   ```bash
   cd frontend
   python -m http.server 5500
   ```
   UI available at `http://127.0.0.1:5500`

### Using the Application

1. Open `http://127.0.0.1:5500` in your browser
2. Upload a PDF resume using the file picker
3. Paste the job description in the text area
4. Click "🔍 Analyze Resume"
5. View results in the bento-grid layout:
   - **Left panel**: Skill match analysis with score
   - **Right panel**: Bias detection report

### Test Cases

Use the provided test cases in the `test_cases/` folder:

1. Use `webdev_resume_sample.pdf` as the resume
2. Copy content from `webdev_job_description.txt` as the job description
3. Run the analysis

**Expected Results:**
- Match Score: 85-95%
- Matching Skills: React, JavaScript, HTML5, CSS3, Node.js, Git
- Bias Report: Analysis of job description language for discriminatory terms

## 🔧 Configuration

### Custom Ollama Model

The `Modelfile` configures the AI model with:

```dockerfile
FROM llama3.2:1b
PARAMETER temperature 0.7
PARAMETER num_ctx 4096
PARAMETER top_p 0.9
```

**Customization options:**
- `temperature`: Adjust creativity (0.0-1.0)
- `num_ctx`: Context window size
- `top_p`: Nucleus sampling threshold

### Color Theme

Modify CSS variables in `frontend/style.css`:

```css
:root {
    --primary-color: #6B7A3E;      /* Olive green */
    --bg-primary: #F5F1E8;          /* Beige */
    --bg-card: #FDFCF7;             /* Light beige */
}
```

### Logo Customization

The custom SVG logo (`frontend/logo.svg`) features:
- Document icon representing resumes
- Checkmark for approval/screening
- AI sparkle for automation
- Matches the beige/olive green color scheme

Edit the SVG file directly to customize colors, shapes, or add your brand.

## 📡 API Endpoints

### POST `/upload`

Analyze resume against job description.

**Request:**
- `resume`: PDF file (multipart/form-data)
- `job_desc`: Job description text (string)

**Response:**
```json
{
  "analysis": "Skill match analysis with score...",
  "bias_report": "Bias detection results..."
}
```

**Example with curl:**
```bash
curl -X POST http://127.0.0.1:5000/upload \
  -F "resume=@resume.pdf" \
  -F "job_desc=Looking for Python developer..."
```

## 🎨 Frontend Features

### Markdown Rendering

The frontend properly renders markdown formatting without showing asterisks:
- **Bold text**: `**text**` or `__text__`
- *Italic text*: `*text*` or `_text_`
- Lists: `-` or numbered
- Headers: `##` and `###`

### Bento Box Layout

Responsive asymmetric grid system:
- Desktop: 7-column skill analysis, 5-column bias report
- Mobile: Stacks vertically
- Modern, professional appearance

### Custom Logo

Professional SVG logo featuring:
- Document icon for resumes
- Checkmark for screening approval
- AI sparkle for automation
- Animated fade-in effect

### Color Scheme

Professional beige and olive green palette:
- Primary: Olive green (`#6B7A3E`)
- Background: Beige tones (`#F5F1E8`)
- Accent: Muted green (`#8B956A`)
- Cards: Light beige (`#FDFCF7`)

## 🛠️ Technology Stack

- **Backend**: Flask, Python 3.8+
- **AI**: Ollama (llama3.2:1b base model)
- **PDF Processing**: PyPDF2 / pdfplumber
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Styling**: CSS Grid (Bento layout), CSS Variables

## 📦 Dependencies

See [backend/requirements.txt](backend/requirements.txt) for the complete list:

```txt
flask>=2.3.0
flask-cors>=4.0.0
requests>=2.31.0
PyPDF2>=3.0.0
pdfplumber>=0.10.0
```

## 🔍 Troubleshooting

**Server won't start:**
- Ensure virtual environment is activated
- Check port 5000 is not in use
- Verify all dependencies are installed

**Model not found:**
```bash
ollama create recruitment-screener -f Modelfile
ollama list  # Verify installation
```

**Slow response times (>60s):**
- Default model (llama3.2:1b) is optimized for speed
- For better accuracy, try: `ollama pull llama3.2:3b`
- Update Modelfile first line to: `FROM llama3.2:3b`
- Recreate model: `ollama create recruitment-screener -f Modelfile`

**Markdown not rendering:**
- Check browser console for JavaScript errors
- Verify `script.js` has updated formatting functions
- Clear browser cache
- Ensure you're viewing the latest version

**Logo not displaying:**
- Verify `logo.svg` exists in the frontend folder
- Check browser developer tools for 404 errors
- Clear cache and hard refresh (Ctrl+F5)

**PDF parsing errors:**
- Ensure PDF is text-based (not scanned image)
- Check PDF file size (< 10MB recommended)
- Verify file upload permissions

## 🚧 Known Limitations & Future Enhancements

**Current Limitations:**
- Scoring accuracy may over-rate candidates with domain mismatches (see [docs/FINAL_CONCLUSION.md](docs/FINAL_CONCLUSION.md))
- Requires human oversight for final hiring decisions
- Best suited for initial screening, not final selection

**Planned Enhancements:**
- [ ] Improved scoring algorithm for domain mismatch detection
- [ ] Interview scheduling integration
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Candidate ranking system
- [ ] Email notifications
- [ ] Database integration for candidate tracking
- [ ] Export reports to PDF
- [ ] Batch resume processing

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## � Production Status

**Current Grade: B (83/100)**

✅ **Ready for production** with human oversight  
✅ **Excellent UI/UX** with modern design  
✅ **Fast response times** (~37 seconds average)  
⚠️ **Scoring accuracy** requires monitoring  

For detailed test results and recommendations, see [docs/FINAL_CONCLUSION.md](docs/FINAL_CONCLUSION.md)

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check [docs/FINAL_CONCLUSION.md](docs/FINAL_CONCLUSION.md) for known issues
- Review closed issues for solutions

## 🙏 Acknowledgments

- Built with [Ollama](https://ollama.ai/) for local AI inference
- Powered by [Flask](https://flask.palletsprojects.com/) web framework
- Inspired by modern recruitment challenges

---

**Made with ❤️ to make recruitment fairer and more efficient**
