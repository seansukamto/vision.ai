"""Main Company Research Workflow.

This module implements the complete company research workflow that coordinates
specialized research agents and integrates job description context for 
comprehensive company analysis tailored to job seekers.
"""

import asyncio
from typing_extensions import Literal

from langchain.chat_models import init_chat_model
from langchain_core.messages import (
    HumanMessage, 
    BaseMessage, 
    SystemMessage, 
    ToolMessage,
)
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command

from company_research_assistant.company_research_state import (
    CompanyResearchState, 
    JobDescriptionAnalysis,
    CompanyResearchPlan
)
from company_research_assistant.past_research_agent import past_research_agent
from company_research_assistant.future_research_agent import future_research_agent
from company_research_assistant.culture_research_agent import culture_research_agent
from company_research_assistant.prompts import final_report_generation_prompt
from company_research_assistant.utils import get_today_str

# ===== CONFIGURATION =====

# Initialize models
planning_model = init_chat_model(model="openai:gpt-4.1-nano")
analysis_model = init_chat_model(model="openai:gpt-4.1-nano")
report_model = init_chat_model(model="openai:gpt-4.1-nano")

# ===== WORKFLOW NODES =====

async def analyze_job_description(state: CompanyResearchState) -> Command[Literal["plan_research"]]:
    """Analyze job description to extract key information for targeted research.
    
    If a job description is provided, extracts relevant details that will help
    tailor the company research to the specific role and context.
    
    Args:
        state: Current workflow state with company name and optional job description
        
    Returns:
        Command to proceed to research planning with job analysis results
    """
    job_description = state.get("job_description", "")
    
    job_analysis = None
    if job_description and job_description.strip():
        # Analyze the job description for key information
        analysis_prompt = f"""Analyze the following job description and extract key information:

Job Description:
{job_description}

Extract the job title, department, key responsibilities, required skills, 
company values mentioned, and seniority level. This information will be used 
to tailor company research for this specific role."""

        try:
            response = analysis_model.with_structured_output(JobDescriptionAnalysis).invoke([
                SystemMessage(content="You are an expert at analyzing job descriptions to extract key information for company research."),
                HumanMessage(content=analysis_prompt)
            ])
            job_analysis = response
        except Exception as e:
            # If structured analysis fails, continue without it
            print(f"Job description analysis failed: {e}")
    
    return Command(
        goto="plan_research",
        update={
            "job_analysis": job_analysis.dict() if job_analysis else {},
            "messages": [HumanMessage(content=f"Analyzing company research for {state['company_name']}" + 
                                    (f" for {job_analysis.job_title} position" if job_analysis else ""))]
        }
    )

async def plan_research(state: CompanyResearchState) -> Command[Literal["conduct_research"]]:
    """Plan the comprehensive research strategy based on company and job context.
    
    Creates a detailed research plan that specifies what each specialized agent
    should focus on, potentially customized based on job description analysis.
    
    Args:
        state: Current workflow state with company info and job analysis
        
    Returns:
        Command to proceed to research execution with detailed plan
    """
    company_name = state["company_name"]
    job_analysis = state.get("job_analysis", {})
    
    # Create research planning prompt
    planning_context = f"Company: {company_name}"
    if job_analysis and job_analysis.get("job_title"):
        planning_context += f"\nJob Title: {job_analysis['job_title']}"
        if job_analysis.get("department"):
            planning_context += f"\nDepartment: {job_analysis['department']}"
        if job_analysis.get("seniority_level"):
            planning_context += f"\nSeniority Level: {job_analysis['seniority_level']}"
    
    planning_prompt = f"""Create a comprehensive company research plan for a job seeker:

{planning_context}

Plan detailed research objectives and focus areas for three specialized research agents:
1. Past Research Agent (company history and background)
2. Future Research Agent (strategic plans and growth prospects)  
3. Culture Research Agent (values, work environment, employee satisfaction)

Consider any job-specific context to tailor the research appropriately."""

    try:
        research_plan = planning_model.with_structured_output(CompanyResearchPlan).invoke([
            SystemMessage(content="You are an expert research planner specializing in company analysis for job seekers."),
            HumanMessage(content=planning_prompt)
        ])
    except Exception as e:
        # Fallback to default research plan if structured planning fails
        research_plan = CompanyResearchPlan(
            research_objectives=[f"Comprehensive analysis of {company_name} for job seekers"],
            past_research_focus=f"Research {company_name} history, founding, key milestones, and evolution up to present",
            future_research_focus=f"Research {company_name} future prospects, strategic plans, and growth opportunities",
            culture_research_focus=f"Research {company_name} company culture, values, work environment, and employee satisfaction"
        )
    
    return Command(
        goto="conduct_research",
        update={
            "research_plan": research_plan.dict(),
            "research_brief": f"Comprehensive company research for {company_name}" + 
                            (f" - {job_analysis.get('job_title', '')} position" if job_analysis.get('job_title') else "")
        }
    )

async def conduct_research(state: CompanyResearchState) -> Command[Literal["generate_report"]]:
    """Conduct parallel research using all three specialized agents.
    
    Launches the past, future, and culture research agents in parallel to gather
    comprehensive information about the company from all three perspectives.
    
    Args:
        state: Current workflow state with research plan
        
    Returns:
        Command to proceed to report generation with research findings
    """
    research_plan = state.get("research_plan", {})
    
    # Prepare research topics for each specialized agent
    past_research_topic = research_plan.get("past_research_focus", 
        f"Research {state['company_name']} history, founding, key milestones, and evolution up to present")
    
    future_research_topic = research_plan.get("future_research_focus",
        f"Research {state['company_name']} future prospects, strategic plans, and growth opportunities")
    
    culture_research_topic = research_plan.get("culture_research_focus",
        f"Research {state['company_name']} company culture, values, work environment, and employee satisfaction")
    
    # Launch all three research agents in parallel
    research_coroutines = [
        past_research_agent.ainvoke({
            "researcher_messages": [HumanMessage(content=past_research_topic)],
            "research_topic": past_research_topic
        }),
        future_research_agent.ainvoke({
            "researcher_messages": [HumanMessage(content=future_research_topic)],
            "research_topic": future_research_topic
        }),
        culture_research_agent.ainvoke({
            "researcher_messages": [HumanMessage(content=culture_research_topic)],
            "research_topic": culture_research_topic
        })
    ]
    
    try:
        # Wait for all research to complete
        past_results, future_results, culture_results = await asyncio.gather(*research_coroutines)
        
        return Command(
            goto="generate_report",
            update={
                "past_research_findings": past_results.get("compressed_research", ""),
                "future_research_findings": future_results.get("compressed_research", ""),
                "culture_research_findings": culture_results.get("compressed_research", ""),
                "research_complete": True
            }
        )
    except Exception as e:
        return Command(
            goto="generate_report",
            update={
                "processing_errors": [f"Research error: {str(e)}"],
                "research_complete": False
            }
        )

async def generate_report(state: CompanyResearchState) -> Command[Literal["__end__"]]:
    """Generate the final comprehensive company research report.
    
    Synthesizes findings from all three research agents into a coherent,
    well-structured report tailored for job seekers, with job-specific
    insights when applicable.
    
    Args:
        state: Current workflow state with all research findings
        
    Returns:
        Command to end workflow with final report
    """
    # Compile all research findings
    findings = []
    
    if state.get("past_research_findings"):
        findings.append(f"## Company History and Background\n{state['past_research_findings']}")
    
    if state.get("future_research_findings"):
        findings.append(f"## Future Prospects and Strategy\n{state['future_research_findings']}")
    
    if state.get("culture_research_findings"):
        findings.append(f"## Company Culture and Work Environment\n{state['culture_research_findings']}")
    
    if not findings:
        comprehensive_report = f"# Company Research Report: {state['company_name']}\n\nNo research findings available due to processing errors."
    else:
        # Generate comprehensive report
        all_findings = "\n\n".join(findings)
        research_brief = state.get("research_brief", f"Company research for {state['company_name']}")
        
        report_prompt = final_report_generation_prompt.format(
            research_brief=research_brief,
            findings=all_findings,
            date=get_today_str()
        )
        
        try:
            report_response = report_model.invoke([
                SystemMessage(content="You are an expert at synthesizing company research into comprehensive reports for job seekers."),
                HumanMessage(content=report_prompt)
            ])
            comprehensive_report = str(report_response.content)
        except Exception as e:
            comprehensive_report = f"# Company Research Report: {state['company_name']}\n\n{all_findings}\n\n*Note: Report generation encountered an error: {e}*"
    
    return Command(
        goto=END,
        update={
            "comprehensive_report": comprehensive_report,
            "messages": [HumanMessage(content="Company research completed successfully.")]
        }
    )

# ===== GRAPH CONSTRUCTION =====

# Build the company research workflow
workflow_builder = StateGraph(CompanyResearchState)

# Add nodes to the graph
workflow_builder.add_node("analyze_job_description", analyze_job_description)
workflow_builder.add_node("plan_research", plan_research)
workflow_builder.add_node("conduct_research", conduct_research)
workflow_builder.add_node("generate_report", generate_report)

# Add edges to connect nodes
workflow_builder.add_edge(START, "analyze_job_description")
workflow_builder.add_edge("analyze_job_description", "plan_research")
workflow_builder.add_edge("plan_research", "conduct_research")
workflow_builder.add_edge("conduct_research", "generate_report")
workflow_builder.add_edge("generate_report", END)

# Compile the workflow
company_research_workflow = workflow_builder.compile()
