# 🏢 Company Research Assistant

An AI-powered company research tool specifically designed for job seekers to make informed career decisions. This application transforms the original deep research framework into a specialized multi-agent system that provides comprehensive company analysis across three key dimensions: history, future prospects, and culture.

## 🎯 What This Application Does

### For Job Seekers

Get comprehensive insights about potential employers to make informed career decisions:

- **Company Background**: Historical context, founding story, and evolution
- **Future Opportunities**: Growth prospects, strategic plans, and career potential
- **Cultural Fit**: Values, work environment, and employee satisfaction
- **Role-Specific Insights**: Tailored information when job descriptions are provided

### Why This Matters

- **Information Asymmetry**: Job seekers often lack deep insights about companies beyond surface-level information
- **Cultural Fit Assessment**: Understanding if your values align with company culture
- **Career Growth Potential**: Evaluating future opportunities and company trajectory
- **Informed Decision Making**: Comprehensive research enables better career choices

## 🏗️ Architecture Overview

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

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Required API keys (see Environment Setup below)

### Installation

```bash
# Clone and navigate to project
cd deep_research_from_scratch

# Install dependencies
uv sync

# Activate environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Environment Setup

Create a `.env` file with your API keys:

```env
# Required for web research
TAVILY_API_KEY=your_tavily_api_key_here

# Required for AI models
OPENAI_API_KEY=your_openai_api_key_here

# Optional: For tracing and evaluation
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=company_research_assistant
```

### Basic Usage

#### Command Line Interface

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

#### Programmatic Usage

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

#### Jupyter Notebooks

```bash
# Start Jupyter
uv run jupyter notebook

# Open the demo notebook
# notebooks/company_research_demo.ipynb
```

## 📋 Input Options

### Required Input

- **Company Name**: The company you want to research

### Optional Context (Enhances Research Quality)

- **Job Title**: Position you're considering (e.g., "Product Manager", "Software Engineer")
- **Job Description**: Full job posting text or requirements for role-specific insights

### When Job Context is Provided

- Research agents tailor their findings to the specific role
- Culture research focuses on relevant team/department aspects
- Future research emphasizes career growth in that domain
- Past research highlights relevant company experience

## 📊 Output Structure

### Comprehensive Research Report

```markdown
# Company Research Report: [Company Name]

## Executive Summary

- Overall company assessment
- Key strengths and opportunities
- Cultural fit indicators
- Growth potential analysis

## Company History and Background

- Founding story and mission evolution
- Key milestones and achievements
- Leadership and management history
- Market position development

## Future Prospects and Strategy

- Strategic initiatives and roadmaps
- Growth opportunities and investments
- Market positioning and trends
- Innovation and development focus

## Company Culture and Work Environment

- Core values and cultural principles
- Employee satisfaction and reviews
- Work-life balance and benefits
- Professional development opportunities
- Diversity and inclusion practices

## [Role-Specific Insights] (when job context provided)

- Department-specific culture
- Career growth paths in this role
- Relevant company initiatives
- Team structure and dynamics

## Sources and References

- Comprehensive citation list
- Research confidence indicators
- Data freshness timestamps
```

## 🛠️ Technical Architecture

### Technology Stack

- **LangGraph**: Multi-agent workflow orchestration
- **LangChain**: LLM abstraction and tool integration
- **OpenAI GPT-4**: Primary reasoning and synthesis for all research tasks
- **Tavily Search**: Web research and content processing
- **Pydantic**: Data validation and type safety

### Key Design Patterns

- **Multi-Agent System**: Specialized agents for different research domains
- **Supervisor Pattern**: Coordinated research orchestration
- **Parallel Processing**: Concurrent research execution for efficiency
- **State Management**: Immutable state updates with audit trails
- **Structured Output**: Reliable data extraction and synthesis

## 📂 Project Structure

```
company_research_assistant/
├── src/company_research_assistant/
│   ├── agents/                    # Research agent implementations
│   │   ├── past_research_agent.py
│   │   ├── future_research_agent.py
│   │   └── culture_research_agent.py
│   ├── prompts.py                 # Specialized prompt templates
│   ├── company_research_workflow.py  # Main orchestration workflow
│   ├── company_research_state.py    # State definitions
│   ├── multi_agent_supervisor.py    # Agent coordination
│   ├── cli.py                        # Command line interface
│   └── utils.py                      # Shared utilities
├── notebooks/                        # Demo and tutorial notebooks
├── docs/                            # Documentation
│   ├── product.md                   # Product overview and requirements
│   ├── tech.md                      # Technology stack details
│   └── structure.md                 # Project structure guide
└── README_COMPANY_RESEARCH.md      # This file
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

## 🚀 Future Enhancements

### Planned Features

- **Industry Benchmarking**: Compare companies within industry context
- **Salary Analysis**: Integration with compensation data
- **Social Media Sentiment**: Employee sentiment analysis from social platforms
- **Alumni Networks**: Connect with current/former employees
- **Interview Question Prediction**: Role-specific interview preparation

### Technical Roadmap

- **Real-time Updates**: Continuous research refresh mechanisms
- **Custom Research Templates**: Industry or role-specific research patterns
- **Interactive Reports**: Dynamic filtering and exploration capabilities
- **API Integration**: Third-party career platform integration

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

## 📄 License

This project builds upon the original deep research framework and maintains the same open-source principles. See the original project for license details.

## 🙏 Acknowledgments

Built upon the excellent foundation of the LangChain deep research tutorial, this specialized application demonstrates the power of multi-agent systems for domain-specific research challenges. Special thanks to the LangChain team for the robust architectural patterns and the broader AI research community for the underlying technologies.

---

**Ready to make more informed career decisions? Start researching your next opportunity today!** 🎯
