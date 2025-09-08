"""Command Line Interface for Company Research Assistant.

This module provides a simple CLI for testing and using the company research
assistant functionality.
"""

import asyncio
import argparse
import sys
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from company_research_assistant.company_research_workflow import company_research_workflow

async def research_company(
    company_name: str,
    job_description: Optional[str] = None,
    job_title: Optional[str] = None
) -> str:
    """Research a company using the specialized research agents.
    
    Args:
        company_name: Name of the company to research
        job_description: Optional job description for context
        job_title: Optional job title for context
        
    Returns:
        Comprehensive research report
    """
    # Prepare initial state
    initial_state = {
        "company_name": company_name,
        "job_description": job_description,
        "job_title": job_title,
        "messages": [],
        "research_brief": "",
        "research_iterations": 0,
        "processing_errors": []
    }
    
    try:
        # Execute the research workflow
        result = await company_research_workflow.ainvoke(initial_state)
        return result.get("comprehensive_report", "No report generated")
    
    except Exception as e:
        return f"Error during company research: {str(e)}"

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Company Research Assistant - AI-powered company research for job seekers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Research a company
  python -m company_research_assistant.cli --company "Google"
  
  # Research with job context
  python -m company_research_assistant.cli --company "Microsoft" --job-title "Software Engineer"
  
  # Research with job description
  python -m company_research_assistant.cli --company "OpenAI" --job-description "We are looking for a senior ML engineer..."
        """
    )
    
    parser.add_argument(
        "--company",
        required=True,
        help="Name of the company to research"
    )
    
    parser.add_argument(
        "--job-title",
        help="Job title for context-specific research"
    )
    
    parser.add_argument(
        "--job-description",
        help="Job description text or file path for detailed context"
    )
    
    parser.add_argument(
        "--output",
        help="Output file path (default: print to console)"
    )
    
    args = parser.parse_args()
    
    # Handle job description from file if it looks like a file path
    job_description = args.job_description
    if job_description and job_description.endswith(('.txt', '.md')):
        try:
            with open(job_description, 'r', encoding='utf-8') as f:
                job_description = f.read()
        except Exception as e:
            print(f"Error reading job description file: {e}", file=sys.stderr)
            sys.exit(1)
    
    # Run the research
    print(f"🔍 Researching {args.company}...")
    if args.job_title:
        print(f"📋 Job context: {args.job_title}")
    if job_description:
        print(f"📝 Job description provided ({len(job_description)} characters)")
    print()
    
    try:
        # Run the async research workflow
        report = asyncio.run(research_company(
            company_name=args.company,
            job_description=job_description,
            job_title=args.job_title
        ))
        
        # Output the report
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ Report saved to {args.output}")
        else:
            print("📊 Research Report:")
            print("=" * 80)
            print(report)
            print("=" * 80)
            
    except KeyboardInterrupt:
        print("\n❌ Research interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during research: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
