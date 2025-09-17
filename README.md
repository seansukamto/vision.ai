# Company Research Assistant

> **AI-powered company research for job seekers** - A modern web application that provides comprehensive company insights using specialized AI agents.

## 🚀 Quick Start

### 1. Set Up API Keys

Create a `.env` file in the project root:

```bash
# Create .env file
touch .env
```

Add your API keys:

```env
# Required for AI research agents
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

# Optional: For evaluation and tracing
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=company_research_assistant
```

### 2. Start the Application

```bash
# Install dependencies (if needed)
pip install -r requirements.txt

# Start the web server
python start_server.py
```

### 3. Open Your Browser

Navigate to: **http://localhost:8000**

## ✨ What This App Does

The Company Research Assistant is a **full-stack web application** that uses AI agents to provide comprehensive company research. Perfect for job seekers who want to understand potential employers.

### Key Features

- **🔍 Comprehensive Research**: AI agents analyze company history, future prospects, and culture
- **🎯 Job-Specific Analysis**: Tailor research to specific roles and job descriptions
- **📊 Professional Reports**: Generate detailed, well-formatted research reports
- **💻 Modern Interface**: Clean, responsive web design that works on all devices
- **⚡ Real-Time Progress**: Visual progress tracking through 6 research stages
- **📋 Easy Sharing**: Copy reports to clipboard or download as files

## 🏗️ AI Research Architecture

### Three Specialized Research Agents

#### 🏛️ Past Research Agent

**Focus**: Company history and background analysis

- Founding story and original mission
- Key historical milestones and pivotal moments
- Leadership evolution and management changes
- Product/service development timeline
- Financial performance trends
- Market position evolution
- Notable achievements and challenges overcome

#### 🚀 Future Research Agent

**Focus**: Strategic plans and growth prospects

- Strategic initiatives and long-term roadmaps
- Planned expansions and new markets
- Investment activities and funding rounds
- R&D focus and innovation plans
- Industry positioning for future trends
- Growth trajectory and projections
- Partnership announcements

#### 👥 Culture Research Agent

**Focus**: Values, culture, and work environment

- Core values and mission alignment
- Employee satisfaction and retention
- Diversity, equity, and inclusion practices
- Work-life balance policies
- Professional development opportunities
- Employee reviews and testimonials
- Management style and structure
- Benefits and compensation philosophy

### 🎯 Intelligent Orchestration

- **Supervisor Agent**: Coordinates all three research agents
- **Parallel Processing**: Simultaneous research for efficiency
- **Context Integration**: Job description analysis for role-specific insights
- **Report Synthesis**: Comprehensive final reports tailored for job seekers

## 🎨 User Interface

### Research Form

- **Company Name** (required): Enter any company you want to research
- **Job Title** (optional): Add context for targeted research
- **Job Description** (optional): Paste full job descriptions for detailed analysis

### Research Process

The app shows progress through 6 stages:

1. **Analyzing job description** - Processing any job context provided
2. **Planning research strategy** - Creating targeted research plan
3. **Researching company history** - Past Research Agent working
4. **Analyzing future prospects** - Future Research Agent working
5. **Investigating company culture** - Culture Research Agent working
6. **Generating comprehensive report** - Synthesizing all findings

### Results & Actions

- **Copy Report**: Copy the full report to your clipboard
- **Download**: Save the report as a text file
- **New Research**: Start a fresh research session
- **Keyboard Shortcuts**: `Ctrl/Cmd + Enter` to submit, `Escape` to cancel

## 🛠 Technology Stack

### Frontend

- **HTML5**: Semantic markup with accessibility best practices
- **CSS3**: Modern design with Grid, Flexbox, and custom properties
- **Vanilla JavaScript**: ES6+ with async/await, no framework dependencies
- **Font Awesome**: Professional icons
- **Inter Font**: Modern, readable typography

### Backend

- **FastAPI**: High-performance Python web framework
- **Uvicorn**: ASGI server with hot reload for development
- **LangGraph**: Multi-agent AI workflow orchestration
- **LangChain**: AI agent framework with external tool integration
- **Tavily**: Web search for real-time company information
- **OpenAI GPT-4**: Primary reasoning and synthesis for all research tasks
- **Pydantic**: Data validation and type safety

## 📁 Project Structure

```
vision.ai/
├── frontend/                    # Web interface
│   ├── index.html              # Main application page
│   ├── styles.css              # Modern CSS styling
│   └── app.js                  # JavaScript application logic
├── backend/                    # AI research system
│   ├── src/company_research_assistant/
│   │   ├── cli.py              # Command line interface
│   │   ├── company_research_workflow.py  # Main orchestration workflow
│   │   ├── company_research_state.py    # State definitions
│   │   ├── past_research_agent.py      # Historical analysis
│   │   ├── future_research_agent.py    # Future prospects
│   │   ├── culture_research_agent.py   # Company culture
│   │   ├── prompts.py          # Specialized prompt templates
│   │   └── utils.py            # Shared utilities
│   ├── notebooks/              # Development notebooks
│   ├── pyproject.toml          # Backend dependencies
│   └── README.md               # Backend documentation
├── api_server.py               # FastAPI web server
├── start_server.py             # Easy startup script
├── demo.py                     # Setup verification
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🔧 Alternative Startup Methods

### Option 1: Direct API Server

```bash
python api_server.py
```

### Option 2: Demo/Verification

```bash
python demo.py
```

### Option 3: Command Line Interface

```bash
# Basic company research
python -m company_research_assistant.cli --company "Google"

# With job context
python -m company_research_assistant.cli --company "Microsoft" --job-title "Software Engineer"

# With detailed job description
python -m company_research_assistant.cli --company "OpenAI" --job-description "job_description.txt"

# Save to file
python -m company_research_assistant.cli --company "Meta" --output "meta_research.md"
```

### Option 4: Programmatic Usage

```python
from company_research_assistant.company_research_workflow import company_research_workflow

async def research_company():
    initial_state = {
        "company_name": "Tesla",
        "job_description": "Software Engineer position focusing on autonomous driving...",
        "job_title": "Software Engineer",
        "messages": [],
        "research_brief": "",
        "research_iterations": 0,
        "processing_errors": []
    }

    result = await company_research_workflow.ainvoke(initial_state)
    return result.get("comprehensive_report", "No report generated")

# Run research
report = await research_company()
print(report)
```

## 📚 Usage Examples

### Basic Company Research

1. Enter company name: "Google"
2. Click "Start Research"
3. Wait for comprehensive analysis
4. Review the detailed report

### Job-Specific Research

1. Enter company: "Microsoft"
2. Add job title: "Software Engineer"
3. Paste job description (optional)
4. Get targeted insights for that specific role

### Research Output

The app generates comprehensive reports including:

- **Company Overview**: Mission, values, and key facts
- **Historical Analysis**: Company evolution and milestones
- **Future Prospects**: Growth plans and market position
- **Culture Insights**: Work environment and employee experience
- **Job-Specific Context**: How the role fits into the company

## 🌐 API Endpoints

The frontend communicates with these API endpoints:

- `GET /` - Serve the frontend application
- `GET /health` - Health check for API availability
- `POST /research` - Submit company research request
- `GET /validate/company/{name}` - Validate company name
- `GET /docs` - Interactive API documentation

### Request Format

```json
{
  "company_name": "Google",
  "job_title": "Software Engineer",
  "job_description": "We are looking for a senior software engineer..."
}
```

### Response Format

```json
{
  "success": true,
  "data": {
    "report": "# Company Research Report...",
    "company_name": "Google",
    "processing_time_seconds": 45.2
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## 🎯 Use Cases

### Individual Job Seekers

- **Career Transitions**: Research companies in new industries
- **Role Comparison**: Compare similar positions across companies
- **Cultural Assessment**: Evaluate cultural fit before applying
- **Interview Preparation**: Deep company knowledge for interviews

### Career Professionals

- **Strategic Moves**: Assess long-term career opportunities
- **Industry Analysis**: Understand company positioning and prospects
- **Compensation Research**: Context for salary negotiations
- **Team Dynamics**: Department-specific culture insights

### Career Services

- **Student Guidance**: Help students research potential employers
- **Career Coaching**: Support clients in making informed decisions
- **Industry Insights**: Provide comprehensive company analysis
- **Interview Preparation**: Detailed company background for coaching

## 🔄 Research Quality Features

### Multi-Source Validation

- Cross-references information across multiple sources
- Identifies contradictory information and flags uncertainties
- Prioritizes recent and authoritative sources

### Bias Awareness

- Distinguishes between company marketing and employee experiences
- Includes both positive and negative perspectives
- Provides balanced analysis across different viewpoints

### Recency Tracking

- Timestamps all research findings
- Prioritizes recent developments and current information
- Indicates data freshness in final reports

## 🎯 Browser Support

### Fully Supported

- Chrome 80+ (recommended)
- Firefox 75+
- Safari 13+
- Edge 80+

### Features Used

- ES6+ JavaScript (async/await, classes, modules)
- CSS Grid and Flexbox
- CSS Custom Properties
- Fetch API
- Clipboard API (for copy functionality)

## 🚨 Troubleshooting

### Common Issues

**"Backend service may be unavailable"**

- Ensure the API server is running on port 8000
- Check that all dependencies are installed
- Verify .env file has required API keys

**Research takes too long or times out**

- Research can take up to 2 minutes for comprehensive analysis
- Ensure stable internet connection for web research
- Check API rate limits for OpenAI and Tavily

**Copy/Download not working**

- Copy requires HTTPS or localhost (browser security)
- Download should work in all modern browsers
- Check browser console for specific errors

**Styling issues**

- Ensure CSS file is loading (check Network tab)
- Clear browser cache
- Check for CSS syntax errors in console

### Debug Mode

Enable detailed logging in browser console:

```javascript
localStorage.setItem("debug", "true");
// Refresh page
```

## 🏗 Development

### Development Workflow

1. Make changes to frontend files
2. The API server serves files directly (no build step needed)
3. Refresh browser to see changes
4. Use browser dev tools for debugging

### Jupyter Notebooks

```bash
# Start Jupyter
uv run jupyter notebook

# Open the demo notebook
# notebooks/company_research_demo.ipynb
```

### Debugging

- Open browser developer tools (F12)
- Check Console tab for JavaScript errors
- Check Network tab for API request/response details
- Use the `/docs` endpoint for API documentation

## 🔮 Future Enhancements

### Planned Features

- [ ] Dark/light theme toggle
- [ ] Research history and saved reports
- [ ] Company comparison features
- [ ] Export to PDF format
- [ ] Real-time progress with WebSockets
- [ ] Collaborative research sharing
- [ ] Advanced filtering and search
- [ ] Mobile app companion
- [ ] Industry Benchmarking: Compare companies within industry context
- [ ] Salary Analysis: Integration with compensation data
- [ ] Social Media Sentiment: Employee sentiment analysis from social platforms
- [ ] Alumni Networks: Connect with current/former employees
- [ ] Interview Question Prediction: Role-specific interview preparation

### Technical Roadmap

- [ ] Real-time Updates: Continuous research refresh mechanisms
- [ ] Custom Research Templates: Industry or role-specific research patterns
- [ ] Interactive Reports: Dynamic filtering and exploration capabilities
- [ ] API Integration: Third-party career platform integration

## 🤝 Contributing

This project welcomes contributions! Key areas for enhancement:

### Research Agent Improvements

- Enhanced domain-specific research strategies
- Additional specialized agents (e.g., compensation, location)
- Improved research quality and accuracy

### User Experience

- Web-based interface development
- Mobile application support
- Integration with job search platforms

### Technical Enhancements

- Performance optimization
- Enhanced error handling and recovery
- Expanded API integrations

## 📞 Support & Resources

- **API Documentation**: Available at `/docs` when server is running
- **Demo Script**: `demo.py` - Verify setup and see examples
- **Health Check**: `GET /health` - Verify system status
- **Backend Documentation**: `backend/README.md` - AI research system details

## 🎉 Success Metrics

✅ **Modern Design**: Sleek, professional interface that rivals commercial platforms  
✅ **Full Integration**: Seamless connection between frontend and AI research system  
✅ **Responsive Layout**: Perfect experience on desktop, tablet, and mobile  
✅ **Performance**: Fast loading and smooth interactions  
✅ **Accessibility**: Inclusive design following web standards  
✅ **Documentation**: Comprehensive guides for users and developers

## 📄 License

This project builds upon the original deep research framework and maintains the same open-source principles.

## 🙏 Acknowledgments

Built upon the excellent foundation of the LangChain deep research tutorial, this specialized application demonstrates the power of multi-agent systems for domain-specific research challenges. Special thanks to the LangChain team for the robust architectural patterns and the broader AI research community for the underlying technologies.

---

**Ready to start researching companies?** Run `python start_server.py` and open http://localhost:8000! 🚀
