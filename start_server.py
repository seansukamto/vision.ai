#!/usr/bin/env python3
"""
Startup script for Company Research Assistant Web Application

This script starts the web server and ensures all dependencies are properly configured.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_environment():
    """Check if the environment is properly set up."""
    logger.info("Checking environment setup...")
    
    # Check if .env file exists
    env_file = Path('.env')
    env_example = Path('backend/.env.example')
    
    if not env_file.exists():
        if env_example.exists():
            logger.warning("No .env file found. Consider copying from backend/.env.example")
            logger.info("You may need to set up API keys (OPENAI_API_KEY, TAVILY_API_KEY) in a .env file")
        else:
            logger.warning("No .env file found. You may need to set environment variables manually")
    else:
        logger.info("Found .env file")
    
    # Check if the research module path is accessible
    research_path = Path('backend/src')
    if not research_path.exists():
        logger.error(f"Research module path not found: {research_path}")
        logger.error("Make sure you're running from the correct directory")
        return False
    
    logger.info("Environment check passed")
    return True

def install_dependencies():
    """Install required dependencies if needed."""
    logger.info("Checking dependencies...")
    
    try:
        import fastapi
        import uvicorn
        logger.info("Web server dependencies found")
    except ImportError:
        logger.info("Installing web server dependencies...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        logger.info("Dependencies installed successfully")

def start_server():
    """Start the web server."""
    logger.info("Starting Company Research Assistant Web Server...")
    logger.info("Server will be available at: http://localhost:8000")
    logger.info("API documentation available at: http://localhost:8000/docs")
    logger.info("Press Ctrl+C to stop the server")
    
    # Import and run the server
    try:
        import uvicorn
        uvicorn.run(
            "api_server:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            reload_dirs=[".", "backend/src"],
            log_level="info"
        )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)

def main():
    """Main entry point."""
    logger.info("=" * 60)
    logger.info("Company Research Assistant - Web Application")
    logger.info("=" * 60)
    
    if not check_environment():
        logger.error("Environment check failed. Please fix the issues above.")
        sys.exit(1)
    
    install_dependencies()
    start_server()

if __name__ == "__main__":
    main()
