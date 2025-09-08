#!/usr/bin/env python3
"""Debug script to test the company research workflow."""

import asyncio
import sys
import traceback
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from company_research_assistant.company_research_workflow import company_research_workflow

async def test_research():
    print('Testing company research workflow...')
    
    initial_state = {
        'company_name': 'Microsoft',
        'job_title': 'Software Engineer',
        'job_description': None,
        'messages': [],
        'research_brief': '',
        'research_iterations': 0,
        'processing_errors': []
    }
    
    try:
        print("Starting workflow...")
        result = await company_research_workflow.ainvoke(initial_state)
        
        print('Result keys:', list(result.keys()))
        
        if 'processing_errors' in result and result['processing_errors']:
            print('Processing errors:', result['processing_errors'])
        
        if 'comprehensive_report' in result:
            report = result['comprehensive_report']
            print('Report length:', len(report))
            print('Report preview (first 500 chars):')
            print(report[:500])
        else:
            print('No comprehensive_report found in result')
            
        return result
        
    except Exception as e:
        print('Exception caught:', str(e))
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = asyncio.run(test_research())
    if result:
        print("\n✅ Test completed successfully")
    else:
        print("\n❌ Test failed")
        sys.exit(1)
