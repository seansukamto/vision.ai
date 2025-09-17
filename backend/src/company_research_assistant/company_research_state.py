"""State Definitions for Company Research Workflow.

This module defines the state objects used for the complete company research
workflow, including job description processing and company analysis.
"""

import operator
from typing_extensions import Annotated, TypedDict, Sequence, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

class CompanyResearchState(TypedDict):
    """
    State for the complete company research workflow.
    
    Manages the entire process from user input through specialized research
    to final report generation, including optional job description context.
    """
    
    # User inputs
    company_name: str
    job_description: Optional[str] = None
    job_title: Optional[str] = None
    
    # Conversation management  
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
    # Research brief and coordination
    research_brief: str
    
    # Research results from specialized agents
    past_research_findings: str = ""
    future_research_findings: str = ""
    culture_research_findings: str = ""
    
    # Final outputs
    comprehensive_report: str = ""
    research_complete: bool = False
    
    # Processing metadata
    research_iterations: int = 0
    processing_errors: Annotated[list[str], operator.add] = []

class JobDescriptionAnalysis(BaseModel):
    """Schema for analyzing and extracting key information from job descriptions."""
    
    job_title: str = Field(
        description="Extracted or clarified job title"
    )
    department: Optional[str] = Field(
        description="Department or team mentioned in the job description",
        default=None
    )
    key_responsibilities: list[str] = Field(
        description="Main responsibilities and duties listed in the job description"
    )
    required_skills: list[str] = Field(
        description="Technical skills, qualifications, and requirements mentioned"
    )
    company_values_mentioned: list[str] = Field(
        description="Any company values, culture aspects, or work environment details mentioned",
        default_factory=list
    )
    seniority_level: Optional[str] = Field(
        description="Seniority level (entry, mid, senior, lead, etc.) if mentioned",
        default=None
    )
    
class CompanyResearchPlan(BaseModel):
    """Schema for planning comprehensive company research based on inputs."""
    
    research_objectives: list[str] = Field(
        description="Main research objectives based on company name and job context"
    )
    past_research_focus: str = Field(
        description="Specific areas to focus on for company history research"
    )
    future_research_focus: str = Field(
        description="Specific areas to focus on for company future prospects research"
    )
    culture_research_focus: str = Field(
        description="Specific areas to focus on for company culture research"
    )
    job_specific_considerations: list[str] = Field(
        description="Additional research considerations based on job description",
        default_factory=list
    )

# ===== RESEARCH AGENT STATES =====

class ResearcherState(TypedDict):
    """
    State for individual research agents (past, future, culture).
    
    Used by specialized research agents to manage their research process,
    including conversation history and research topic context.
    """
    
    # Research context
    research_topic: str
    
    # Conversation management for the research agent
    researcher_messages: Annotated[Sequence[BaseMessage], add_messages]

class ResearcherOutputState(TypedDict):
    """
    Output state for individual research agents.
    
    Contains the compressed research findings and raw notes from
    the research agent's work.
    """
    
    # Research results
    compressed_research: str
    raw_notes: list[str]

class Summary(BaseModel):
    """Schema for webpage content summarization."""
    
    summary: str = Field(
        description="Concise summary of the webpage content"
    )
    key_excerpts: list[str] = Field(
        description="Important quotes or excerpts from the webpage",
        default_factory=list
    )