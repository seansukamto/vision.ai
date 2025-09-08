/**
 * Company Research Assistant - Frontend Application
 * 
 * This JavaScript application handles the frontend logic for the Company Research Assistant,
 * including form submission, API communication, loading states, and results display.
 */

class CompanyResearchApp {
    constructor() {
        this.apiBaseUrl = 'http://localhost:8000'; // Will be configurable
        this.currentRequest = null;
        this.loadingStages = [
            'stage-1', 'stage-2', 'stage-3', 'stage-4', 'stage-5', 'stage-6'
        ];
        this.currentStage = 0;
        this.stageInterval = null;
        
        this.init();
    }

    /**
     * Initialize the application by setting up event listeners and DOM references
     */
    init() {
        this.setupDOMReferences();
        this.setupEventListeners();
        this.setupFormValidation();
        
        // Check if backend is available
        this.checkBackendHealth();
    }

    /**
     * Set up DOM element references for efficient access
     */
    setupDOMReferences() {
        // Form elements
        this.form = document.getElementById('research-form');
        this.companyNameInput = document.getElementById('company-name');
        this.jobTitleInput = document.getElementById('job-title');
        this.jobDescriptionInput = document.getElementById('job-description');
        this.researchBtn = document.getElementById('research-btn');

        // Section elements
        this.formSection = document.querySelector('.research-form-section');
        this.loadingSection = document.getElementById('loading-section');
        this.resultsSection = document.getElementById('results-section');
        this.errorSection = document.getElementById('error-section');

        // Results elements
        this.reportContent = document.getElementById('report-content');
        this.copyBtn = document.getElementById('copy-btn');
        this.downloadBtn = document.getElementById('download-btn');
        this.newResearchBtn = document.getElementById('new-research-btn');

        // Error elements
        this.errorMessage = document.getElementById('error-message');
        this.retryBtn = document.getElementById('retry-btn');

        // Toast container
        this.toastContainer = document.getElementById('toast-container');
    }

    /**
     * Set up event listeners for user interactions
     */
    setupEventListeners() {
        // Form submission
        this.form.addEventListener('submit', (e) => this.handleFormSubmit(e));

        // Action buttons
        this.copyBtn.addEventListener('click', () => this.copyReport());
        this.downloadBtn.addEventListener('click', () => this.downloadReport());
        this.newResearchBtn.addEventListener('click', () => this.startNewResearch());
        this.retryBtn.addEventListener('click', () => this.retryResearch());

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyboardShortcuts(e));

        // Auto-resize textarea
        this.jobDescriptionInput.addEventListener('input', () => this.autoResizeTextarea());
    }

    /**
     * Set up form validation
     */
    setupFormValidation() {
        this.companyNameInput.addEventListener('input', () => {
            const value = this.companyNameInput.value.trim();
            const isValid = value.length >= 2;
            
            if (!isValid && value.length > 0) {
                this.companyNameInput.setCustomValidity('Company name must be at least 2 characters long');
            } else {
                this.companyNameInput.setCustomValidity('');
            }
        });
    }

    /**
     * Check if the backend API is available
     */
    async checkBackendHealth() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`, {
                method: 'GET',
                timeout: 5000
            });
            
            if (!response.ok) {
                throw new Error('Backend not healthy');
            }
        } catch (error) {
            console.warn('Backend health check failed:', error);
            this.showToast('Backend service may be unavailable. Some features might not work.', 'warning');
        }
    }

    /**
     * Handle form submission
     */
    async handleFormSubmit(event) {
        event.preventDefault();
        
        const formData = this.getFormData();
        if (!this.validateFormData(formData)) {
            return;
        }

        this.startResearch(formData);
    }

    /**
     * Get form data from inputs
     */
    getFormData() {
        return {
            companyName: this.companyNameInput.value.trim(),
            jobTitle: this.jobTitleInput.value.trim() || null,
            jobDescription: this.jobDescriptionInput.value.trim() || null
        };
    }

    /**
     * Validate form data
     */
    validateFormData(data) {
        if (!data.companyName || data.companyName.length < 2) {
            this.showToast('Please enter a valid company name (at least 2 characters)', 'error');
            this.companyNameInput.focus();
            return false;
        }

        if (data.jobDescription && data.jobDescription.length > 10000) {
            this.showToast('Job description is too long (max 10,000 characters)', 'error');
            this.jobDescriptionInput.focus();
            return false;
        }

        return true;
    }

    /**
     * Start the research process
     */
    async startResearch(formData) {
        try {
            this.showLoadingState();
            this.startLoadingAnimation();

            const response = await this.submitResearchRequest(formData);
            
            if (response.success) {
                this.showResults(response.data.report);
                this.showToast('Research completed successfully!', 'success');
            } else {
                throw new Error(response.error || 'Research failed');
            }
        } catch (error) {
            console.error('Research error:', error);
            this.showError(error.message);
            this.showToast('Research failed. Please try again.', 'error');
        } finally {
            this.stopLoadingAnimation();
        }
    }

    /**
     * Submit research request to backend API
     */
    async submitResearchRequest(formData) {
        const controller = new AbortController();
        this.currentRequest = controller;

        // Set timeout for the request (2.5 minutes)
        const timeoutId = setTimeout(() => controller.abort(), 150000);

        try {
            const response = await fetch(`${this.apiBaseUrl}/research`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    company_name: formData.companyName,
                    job_title: formData.jobTitle,
                    job_description: formData.jobDescription
                }),
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            clearTimeout(timeoutId);
            
            if (error.name === 'AbortError') {
                throw new Error('Request timed out. The research process took too long.');
            }
            
            throw error;
        } finally {
            this.currentRequest = null;
        }
    }

    /**
     * Show loading state and hide other sections
     */
    showLoadingState() {
        this.hideAllSections();
        this.loadingSection.style.display = 'block';
        this.disableForm(true);
    }

    /**
     * Start loading animation with stage progression
     */
    startLoadingAnimation() {
        this.currentStage = 0;
        this.updateLoadingStage();
        
        // Progress through stages every 15-20 seconds
        this.stageInterval = setInterval(() => {
            this.currentStage = (this.currentStage + 1) % this.loadingStages.length;
            this.updateLoadingStage();
        }, 18000);
    }

    /**
     * Update the active loading stage
     */
    updateLoadingStage() {
        this.loadingStages.forEach((stageId, index) => {
            const stageElement = document.getElementById(stageId);
            if (stageElement) {
                stageElement.classList.remove('active', 'completed');
                
                if (index < this.currentStage) {
                    stageElement.classList.add('completed');
                } else if (index === this.currentStage) {
                    stageElement.classList.add('active');
                }
            }
        });
    }

    /**
     * Stop loading animation
     */
    stopLoadingAnimation() {
        if (this.stageInterval) {
            clearInterval(this.stageInterval);
            this.stageInterval = null;
        }
        
        // Mark all stages as completed
        this.loadingStages.forEach(stageId => {
            const stageElement = document.getElementById(stageId);
            if (stageElement) {
                stageElement.classList.remove('active');
                stageElement.classList.add('completed');
            }
        });
    }

    /**
     * Show research results
     */
    showResults(reportData) {
        this.hideAllSections();
        this.resultsSection.style.display = 'block';
        
        // Process and display the report
        this.displayReport(reportData);
        this.disableForm(false);
    }

    /**
     * Display the research report with proper formatting
     */
    displayReport(reportData) {
        // Convert markdown-like content to HTML
        let htmlContent = this.processReportContent(reportData);
        this.reportContent.innerHTML = htmlContent;
        
        // Scroll to results
        this.resultsSection.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
    }

    /**
     * Process report content for better HTML display
     */
    processReportContent(content) {
        if (!content) return '<p>No report content available.</p>';
        
        // Basic markdown-to-HTML conversion
        let html = content
            // Headers
            .replace(/^# (.*$)/gm, '<h1>$1</h1>')
            .replace(/^## (.*$)/gm, '<h2>$1</h2>')
            .replace(/^### (.*$)/gm, '<h3>$1</h3>')
            .replace(/^#### (.*$)/gm, '<h4>$1</h4>')
            
            // Bold and italic
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            
            // Lists
            .replace(/^\- (.*$)/gm, '<li>$1</li>')
            .replace(/^\d+\. (.*$)/gm, '<li>$1</li>')
            
            // Line breaks
            .replace(/\n\n/g, '</p><p>')
            .replace(/\n/g, '<br>');
        
        // Wrap content in paragraphs
        html = '<p>' + html + '</p>';
        
        // Fix list formatting
        html = html.replace(/(<li>.*?<\/li>)/gs, (match) => {
            return '<ul>' + match.replace(/<br>/g, '') + '</ul>';
        });
        
        // Clean up paragraph tags around headers and lists
        html = html.replace(/<p>(<h[1-6]>.*?<\/h[1-6]>)<\/p>/g, '$1');
        html = html.replace(/<p>(<ul>.*?<\/ul>)<\/p>/gs, '$1');
        
        return html;
    }

    /**
     * Show error state
     */
    showError(errorMessage) {
        this.hideAllSections();
        this.errorSection.style.display = 'block';
        this.errorMessage.textContent = errorMessage;
        this.disableForm(false);
    }

    /**
     * Hide all main sections
     */
    hideAllSections() {
        this.loadingSection.style.display = 'none';
        this.resultsSection.style.display = 'none';
        this.errorSection.style.display = 'none';
    }

    /**
     * Enable/disable form elements
     */
    disableForm(disabled) {
        const elements = [
            this.companyNameInput,
            this.jobTitleInput, 
            this.jobDescriptionInput,
            this.researchBtn
        ];
        
        elements.forEach(element => {
            element.disabled = disabled;
        });
        
        if (disabled) {
            this.researchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Researching...</span>';
        } else {
            this.researchBtn.innerHTML = '<i class="fas fa-search"></i><span>Start Research</span>';
        }
    }

    /**
     * Copy report to clipboard
     */
    async copyReport() {
        try {
            const reportText = this.reportContent.textContent || this.reportContent.innerText;
            await navigator.clipboard.writeText(reportText);
            this.showToast('Report copied to clipboard!', 'success');
        } catch (error) {
            console.error('Copy failed:', error);
            this.showToast('Failed to copy report to clipboard', 'error');
        }
    }

    /**
     * Download report as PDF (placeholder - would need backend support)
     */
    downloadReport() {
        // For now, download as text file
        const reportText = this.reportContent.textContent || this.reportContent.innerText;
        const companyName = this.companyNameInput.value.trim();
        
        const blob = new Blob([reportText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `${companyName}_research_report_${new Date().toISOString().split('T')[0]}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        URL.revokeObjectURL(url);
        this.showToast('Report downloaded!', 'success');
    }

    /**
     * Start a new research session
     */
    startNewResearch() {
        this.hideAllSections();
        this.form.reset();
        this.companyNameInput.focus();
        
        // Cancel any ongoing request
        if (this.currentRequest) {
            this.currentRequest.abort();
            this.currentRequest = null;
        }
        
        this.stopLoadingAnimation();
        this.disableForm(false);
    }

    /**
     * Retry the last research request
     */
    retryResearch() {
        const formData = this.getFormData();
        if (this.validateFormData(formData)) {
            this.startResearch(formData);
        }
    }

    /**
     * Auto-resize textarea based on content
     */
    autoResizeTextarea() {
        const textarea = this.jobDescriptionInput;
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 300) + 'px';
    }

    /**
     * Handle keyboard shortcuts
     */
    handleKeyboardShortcuts(event) {
        // Ctrl/Cmd + Enter to submit form
        if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
            if (!this.researchBtn.disabled) {
                this.form.dispatchEvent(new Event('submit'));
            }
        }
        
        // Escape to cancel or start new research
        if (event.key === 'Escape') {
            if (this.currentRequest) {
                this.currentRequest.abort();
                this.startNewResearch();
            } else if (this.resultsSection.style.display === 'block') {
                this.startNewResearch();
            }
        }
    }

    /**
     * Show toast notification
     */
    showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const iconMap = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle'
        };
        
        toast.innerHTML = `
            <i class="${iconMap[type] || iconMap.info}"></i>
            <span class="toast-message">${message}</span>
            <button class="toast-close" onclick="this.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        this.toastContainer.appendChild(toast);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 5000);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.researchApp = new CompanyResearchApp();
});

// Export for potential module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CompanyResearchApp;
}
