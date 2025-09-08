"""
FastAPI Web Server for Company Research Assistant

This server provides a REST API interface for the Company Research Assistant,
allowing the frontend to interact with the research workflow.
"""

import asyncio
import logging
from datetime import datetime
from typing import Optional
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the research workflow from the existing codebase
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend/src'))

from company_research_assistant.cli import research_company

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Company Research Assistant API",
    description="AI-powered company research for job seekers",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class ResearchRequest(BaseModel):
    """Request model for company research."""
    company_name: str = Field(..., min_length=2, max_length=200, description="Name of the company to research")
    job_title: Optional[str] = Field(None, max_length=200, description="Optional job title for context")
    job_description: Optional[str] = Field(None, max_length=10000, description="Optional job description for detailed context")

class ResearchResponse(BaseModel):
    """Response model for successful research."""
    success: bool = True
    data: dict
    timestamp: datetime
    processing_time: Optional[float] = None

class ErrorResponse(BaseModel):
    """Response model for errors."""
    success: bool = False
    error: str
    error_code: str
    timestamp: datetime

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint to verify API availability."""
    return {
        "status": "healthy",
        "service": "Company Research Assistant API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

# Main research endpoint
@app.post("/research", response_model=ResearchResponse)
async def conduct_company_research(
    request: ResearchRequest,
    http_request: Request
):
    """
    Conduct comprehensive company research.
    
    This endpoint orchestrates the full research workflow including:
    - Job description analysis (if provided)
    - Research planning
    - Parallel execution of specialized research agents
    - Report generation and synthesis
    
    Args:
        request: Research request containing company name and optional job context
        
    Returns:
        Comprehensive research report with findings from all research agents
    """
    start_time = asyncio.get_event_loop().time()
    client_ip = http_request.client.host
    
    logger.info(f"Starting research for company: {request.company_name} (Client: {client_ip})")
    
    try:
        # Validate request
        if not request.company_name or len(request.company_name.strip()) < 2:
            raise HTTPException(
                status_code=400,
                detail="Company name must be at least 2 characters long"
            )
        
        # Log research context
        context_info = f"Company: {request.company_name}"
        if request.job_title:
            context_info += f", Job Title: {request.job_title}"
        if request.job_description:
            context_info += f", Job Description: {len(request.job_description)} chars"
        logger.info(f"Research context: {context_info}")
        
        # Execute the research workflow
        try:
            report = await research_company(
                company_name=request.company_name,
                job_description=request.job_description,
                job_title=request.job_title
            )
            
            if not report or report.startswith("Error during company research:"):
                error_msg = report if report else "No report generated"
                logger.error(f"Research workflow failed: {error_msg}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Research workflow failed: {error_msg}"
                )
            
        except Exception as workflow_error:
            logger.error(f"Research workflow error: {str(workflow_error)}")
            raise HTTPException(
                status_code=500,
                detail=f"Research processing failed: {str(workflow_error)}"
            )
        
        # Calculate processing time
        end_time = asyncio.get_event_loop().time()
        processing_time = end_time - start_time
        
        logger.info(f"Research completed successfully for {request.company_name} in {processing_time:.2f}s")
        
        # Return successful response
        return ResearchResponse(
            success=True,
            data={
                "report": report,
                "company_name": request.company_name,
                "job_title": request.job_title,
                "has_job_context": bool(request.job_title or request.job_description),
                "report_length": len(report),
                "processing_time_seconds": round(processing_time, 2)
            },
            timestamp=datetime.now(),
            processing_time=processing_time
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error during research: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

# Research status endpoint (for potential future use with async processing)
@app.get("/research/status/{request_id}")
async def get_research_status(request_id: str):
    """Get the status of a research request (placeholder for future async implementation)."""
    # This would be used if we implement async processing with job queues
    return {
        "request_id": request_id,
        "status": "not_implemented",
        "message": "Async research status tracking not yet implemented"
    }

# Company validation endpoint
@app.get("/validate/company/{company_name}")
async def validate_company_name(company_name: str):
    """
    Validate if a company name appears to be legitimate.
    
    This is a simple validation endpoint that could be enhanced with
    company database lookups or web validation.
    """
    if len(company_name.strip()) < 2:
        return {
            "valid": False,
            "reason": "Company name too short"
        }
    
    # Basic validation - could be enhanced with external APIs
    invalid_patterns = ['test', 'example', 'dummy', '123']
    name_lower = company_name.lower()
    
    if any(pattern in name_lower for pattern in invalid_patterns):
        return {
            "valid": False,
            "reason": "Company name appears to be a test or placeholder"
        }
    
    return {
        "valid": True,
        "company_name": company_name.strip()
    }

# Serve static frontend files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Additional static file routes for direct access
@app.get("/styles.css")
async def serve_styles():
    """Serve CSS file."""
    return FileResponse("frontend/styles.css", media_type="text/css")

@app.get("/app.js")
async def serve_app_js():
    """Serve JavaScript file."""
    return FileResponse("frontend/app.js", media_type="application/javascript")

@app.get("/")
async def serve_frontend():
    """Serve the main frontend application."""
    return FileResponse("frontend/index.html")

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return ErrorResponse(
        success=False,
        error="Internal server error occurred",
        error_code="INTERNAL_ERROR",
        timestamp=datetime.now()
    )

# Application startup event
@app.on_event("startup")
async def startup_event():
    """Application startup tasks."""
    logger.info("Company Research Assistant API starting up...")
    
    # Verify that the research workflow is available
    try:
        # Test import of the research workflow
        from company_research_assistant.company_research_workflow import company_research_workflow
        logger.info("Research workflow successfully imported")
    except ImportError as e:
        logger.error(f"Failed to import research workflow: {e}")
        logger.error("Make sure the backend dependencies are installed")
    
    logger.info("API startup completed successfully")

# Application shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown tasks."""
    logger.info("Company Research Assistant API shutting down...")

if __name__ == "__main__":
    # Development server configuration
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[".", "backend/src"],
        log_level="info"
    )
