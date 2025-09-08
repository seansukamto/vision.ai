# Company Research Assistant - Frontend Application

A sleek, modern web interface for the AI-powered Company Research Assistant.

## Features

### 🎨 Modern UI Design

- Clean, professional interface following modern design principles
- Responsive design that works on desktop, tablet, and mobile devices
- Smooth animations and transitions for better user experience
- Dark/light theme support with system preference detection

### 🔍 Intelligent Research Interface

- Simple company name input with smart validation
- Optional job title and description fields for targeted research
- Real-time form validation and helpful error messages
- Visual progress indication during research processing

### 📊 Rich Results Display

- Comprehensive research reports with structured formatting
- Copy-to-clipboard functionality for easy sharing
- Download reports as text files
- Markdown-style formatting with proper typography

### ⚡ Performance Optimized

- Fast loading with optimized assets
- Responsive design for all screen sizes
- Keyboard shortcuts for power users
- Progressive loading states with visual feedback

## Architecture

### Frontend Structure

```
frontend/
├── index.html          # Main application page
├── styles.css          # Modern CSS with CSS Grid and Flexbox
├── app.js             # JavaScript application logic
└── assets/            # Images and other static assets (if needed)
```

### Backend Integration

- FastAPI-based REST API server
- Real-time research processing with WebSocket support (future)
- CORS-enabled for cross-origin requests
- Comprehensive error handling and validation

## Technology Stack

### Frontend Technologies

- **HTML5**: Semantic markup with accessibility in mind
- **CSS3**: Modern CSS with custom properties, Grid, and Flexbox
- **Vanilla JavaScript**: No framework dependencies, pure ES6+
- **Web APIs**: Clipboard API, File API, Fetch API

### Design System

- **Typography**: Inter font family for excellent readability
- **Colors**: Professional blue/gray palette with high contrast
- **Icons**: Font Awesome for consistent iconography
- **Layout**: CSS Grid and Flexbox for responsive layouts

## Getting Started

### Prerequisites

- Python 3.8+ with the research assistant dependencies installed
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Quick Start

1. **Start the Web Server**

   ```bash
   python start_server.py
   ```

2. **Open Your Browser**
   Navigate to: http://localhost:8000

3. **Start Researching**
   - Enter a company name (required)
   - Add job title/description for targeted research (optional)
   - Click "Start Research" and wait for results

### Manual Setup

If you prefer to run components separately:

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**

   ```bash
   cp backend/.env.example .env
   # Edit .env file with your API keys
   ```

3. **Start API Server**

   ```bash
   python api_server.py
   ```

4. **Serve Frontend**
   The API server automatically serves the frontend at http://localhost:8000

## Usage Guide

### Basic Research

1. Enter a company name (e.g., "Google", "Microsoft", "OpenAI")
2. Click "Start Research"
3. Wait for the AI agents to complete their analysis
4. Review the comprehensive report

### Targeted Research

1. Enter company name
2. Add job title (e.g., "Software Engineer", "Product Manager")
3. Optionally paste a job description for detailed context
4. The research will be tailored to your specific role interest

### Research Process

The application shows progress through six stages:

1. **Analyzing job description** - Processing any job context provided
2. **Planning research strategy** - Creating targeted research plan
3. **Researching company history** - Past Research Agent working
4. **Analyzing future prospects** - Future Research Agent working
5. **Investigating company culture** - Culture Research Agent working
6. **Generating comprehensive report** - Synthesizing all findings

### Managing Results

- **Copy Report**: Copy the full report to your clipboard
- **Download**: Save the report as a text file
- **New Research**: Start a fresh research session
- **Keyboard Shortcuts**:
  - `Ctrl/Cmd + Enter`: Submit research form
  - `Escape`: Cancel current research or start new session

## API Endpoints

The frontend communicates with these API endpoints:

### Core Endpoints

- `GET /` - Serve the frontend application
- `GET /health` - Health check for API availability
- `POST /research` - Submit company research request
- `GET /validate/company/{name}` - Validate company name

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

## Customization

### Styling

The CSS uses CSS custom properties (variables) for easy theming:

```css
:root {
  --primary-color: #2563eb; /* Main brand color */
  --secondary-color: #64748b; /* Secondary elements */
  --success-color: #10b981; /* Success states */
  --error-color: #ef4444; /* Error states */
  /* ... more variables */
}
```

### Configuration

Modify these settings in `app.js`:

```javascript
class CompanyResearchApp {
    constructor() {
        this.apiBaseUrl = 'http://localhost:8000'; // API server URL
        this.loadingStages = [...];                // Customize loading stages
        // ... other configuration
    }
}
```

## Browser Support

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

## Performance Features

### Optimization Techniques

- Minimal external dependencies (only Font Awesome for icons)
- Efficient CSS with modern layout techniques
- Debounced form validation
- Optimized API requests with timeout handling
- Progressive loading states

### Accessibility Features

- Semantic HTML structure
- ARIA labels and roles
- Keyboard navigation support
- High contrast color schemes
- Focus management
- Screen reader friendly

## Development

### File Structure

```
├── frontend/
│   ├── index.html     # Main HTML structure
│   ├── styles.css     # Complete styling system
│   └── app.js         # Application logic
├── api_server.py      # FastAPI backend server
├── requirements.txt   # Python dependencies
├── start_server.py    # Easy startup script
└── README_FRONTEND.md # This documentation
```

### Development Workflow

1. Make changes to frontend files
2. The API server serves files directly (no build step needed)
3. Refresh browser to see changes
4. Use browser dev tools for debugging

### Debugging

- Open browser developer tools (F12)
- Check Console tab for JavaScript errors
- Check Network tab for API request/response details
- Use the `/docs` endpoint for API documentation

## Troubleshooting

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

### Browser Console Errors

Enable detailed logging by setting debug mode:

```javascript
// In browser console
localStorage.setItem("debug", "true");
// Refresh page
```

## Future Enhancements

### Planned Features

- [ ] Dark/light theme toggle
- [ ] Research history and saved reports
- [ ] Company comparison features
- [ ] Export to PDF format
- [ ] Real-time progress with WebSockets
- [ ] Collaborative research sharing
- [ ] Advanced filtering and search
- [ ] Mobile app companion

### Contributing

This frontend is designed to be easily extensible. Key areas for contribution:

- Enhanced visualizations for research data
- Additional export formats
- Improved accessibility features
- Performance optimizations
- Mobile experience improvements

## License

This frontend application is part of the Company Research Assistant project. See the main project documentation for licensing information.
