#!/usr/bin/env python3
"""
Demo script for Company Research Assistant Web Application

This script demonstrates the functionality and helps verify the setup.
"""

import asyncio
import json
from pathlib import Path
import sys

def check_setup():
    """Check if all required files are in place."""
    required_files = [
        'frontend/index.html',
        'frontend/styles.css', 
        'frontend/app.js',
        'api_server.py',
        'requirements.txt',
        'backend/src/company_research_assistant/cli.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files are present")
    return True

def check_dependencies():
    """Check if required dependencies are available."""
    try:
        import fastapi
        import uvicorn
        print("✅ Web server dependencies available")
    except ImportError as e:
        print(f"❌ Missing web server dependencies: {e}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    # Check if research dependencies are available
    try:
        sys.path.append('backend/src')
        from company_research_assistant import cli
        print("✅ Research workflow dependencies available")
    except ImportError as e:
        print(f"❌ Missing research dependencies: {e}")
        print("   Ensure the backend project is properly set up")
        return False
    
    return True

async def test_research_function():
    """Test the core research function."""
    try:
        sys.path.append('backend/src')
        from company_research_assistant.cli import research_company
        
        print("🧪 Testing research function with a simple query...")
        
        # Test with a minimal request
        result = await research_company(
            company_name="Test Company",
            job_description=None,
            job_title=None
        )
        
        if result and not result.startswith("Error"):
            print("✅ Research function is working")
            return True
        else:
            print(f"❌ Research function returned error: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Research function test failed: {e}")
        return False

def display_startup_instructions():
    """Display instructions for starting the application."""
    print("\n" + "="*60)
    print("🚀 COMPANY RESEARCH ASSISTANT - READY TO START")
    print("="*60)
    print("\n📋 STARTUP INSTRUCTIONS:")
    print("\n1. Start the web server:")
    print("   python start_server.py")
    print("\n2. Open your web browser and navigate to:")
    print("   http://localhost:8000")
    print("\n3. Start researching companies!")
    print("   - Enter a company name (required)")
    print("   - Add job title/description for targeted research (optional)")
    print("   - Click 'Start Research' and wait for AI analysis")
    
    print("\n📚 ADDITIONAL RESOURCES:")
    print("   - API Documentation: http://localhost:8000/docs")
    print("   - Project README: README.md")
    print("   - Original Research Project: backend/")
    
    print("\n⚡ FEATURES:")
    print("   ✓ Modern, responsive web interface")
    print("   ✓ AI-powered company research")
    print("   ✓ Job-specific analysis")
    print("   ✓ Comprehensive reports with copy/download")
    print("   ✓ Real-time progress tracking")
    
    print("\n🔧 TROUBLESHOOTING:")
    print("   - Ensure .env file has API keys (OPENAI_API_KEY, TAVILY_API_KEY)")
    print("   - Check that port 8000 is available")
    print("   - Install dependencies: pip install -r requirements.txt")
    
    print("\n" + "="*60)

async def main():
    """Main demo function."""
    print("🔍 Company Research Assistant - Setup Verification")
    print("=" * 50)
    
    # Check file setup
    if not check_setup():
        print("\n❌ Setup incomplete. Please ensure all files are in place.")
        return
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependencies missing. Please install required packages.")
        return
    
    # Test research function (optional, as it requires API keys)
    print("\n🧪 Testing core functionality...")
    try:
        # Only test if environment variables are available
        import os
        if os.getenv('OPENAI_API_KEY') and os.getenv('TAVILY_API_KEY'):
            await test_research_function()
        else:
            print("⚠️  Skipping research test (API keys not configured)")
            print("   Configure API keys in .env file for full functionality")
    except Exception as e:
        print(f"⚠️  Research test skipped: {e}")
    
    # Display success and instructions
    print("\n✅ Setup verification completed!")
    display_startup_instructions()

if __name__ == "__main__":
    asyncio.run(main())
