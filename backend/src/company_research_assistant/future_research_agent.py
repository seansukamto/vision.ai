"""Future Research Agent for Company Prospects Analysis.

This module implements a specialized research agent that focuses on gathering
information about a company's future plans, strategic initiatives, growth
prospects, and potential developments.
"""

from typing_extensions import Literal

from langgraph.graph import StateGraph, START, END
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage, filter_messages
from langchain.chat_models import init_chat_model

from company_research_assistant.company_research_state import ResearcherState, ResearcherOutputState
from company_research_assistant.utils import tavily_search, get_today_str, think_tool
from company_research_assistant.prompts import future_research_agent_prompt, compress_research_system_prompt, compress_research_human_message

# ===== CONFIGURATION =====

# Set up tools and model binding
tools = [tavily_search, think_tool]
tools_by_name = {tool.name: tool for tool in tools}

# Initialize models
model = init_chat_model(model="openai:gpt-4.1-nano")
model_with_tools = model.bind_tools(tools)
compress_model = init_chat_model(model="openai:gpt-4.1-nano", max_tokens=32000)

# ===== AGENT NODES =====

def llm_call(state: ResearcherState):
    """Analyze current state and decide on research actions for company future prospects.

    The model analyzes the company research request and decides whether to:
    1. Call search tools to gather more future-oriented information
    2. Provide a final answer based on gathered information

    Returns updated state with the model's response.
    """
    return {
        "researcher_messages": [
            model_with_tools.invoke(
                [SystemMessage(content=future_research_agent_prompt.format(date=get_today_str()))] + state["researcher_messages"]
            )
        ]
    }

def tool_node(state: ResearcherState):
    """Execute all tool calls from the previous LLM response.

    Executes all tool calls from the previous LLM responses for company future research.
    Returns updated state with tool execution results.
    """
    tool_calls = state["researcher_messages"][-1].tool_calls

    # Execute all tool calls
    observations = []
    for tool_call in tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observations.append(tool.invoke(tool_call["args"]))

    # Create tool message outputs
    tool_outputs = [
        ToolMessage(
            content=observation,
            name=tool_call["name"],
            tool_call_id=tool_call["id"]
        ) for observation, tool_call in zip(observations, tool_calls)
    ]

    return {"researcher_messages": tool_outputs}

def compress_research(state: ResearcherState) -> dict:
    """Compress future research findings into a concise summary.

    Takes all the company future prospects research messages and tool outputs and creates
    a compressed summary suitable for the supervisor's decision-making.
    """
    system_message = compress_research_system_prompt.format(date=get_today_str())
    research_topic = state.get("research_topic", "Company future prospects and strategic plans research")
    human_message = compress_research_human_message.format(research_topic=research_topic)
    
    messages = [SystemMessage(content=system_message)] + state.get("researcher_messages", []) + [HumanMessage(content=human_message)]
    response = compress_model.invoke(messages)

    # Extract raw notes from tool and AI messages
    raw_notes = [
        str(m.content) for m in filter_messages(
            state["researcher_messages"], 
            include_types=["tool", "ai"]
        )
    ]

    return {
        "compressed_research": str(response.content),
        "raw_notes": ["\n".join(raw_notes)]
    }

# ===== ROUTING LOGIC =====

def should_continue(state: ResearcherState) -> Literal["tool_node", "compress_research"]:
    """Determine whether to continue future research or provide final answer.

    Determines whether the agent should continue the research loop or provide
    a final answer based on whether the LLM made tool calls.

    Returns:
        "tool_node": Continue to tool execution
        "compress_research": Stop and compress research
    """
    messages = state["researcher_messages"]
    last_message = messages[-1]

    # If the LLM makes a tool call, continue to tool execution
    if last_message.tool_calls:
        return "tool_node"
    # Otherwise, we have a final answer
    return "compress_research"

# ===== GRAPH CONSTRUCTION =====

# Build the future research agent workflow
future_research_builder = StateGraph(ResearcherState, output_schema=ResearcherOutputState)

# Add nodes to the graph
future_research_builder.add_node("llm_call", llm_call)
future_research_builder.add_node("tool_node", tool_node)
future_research_builder.add_node("compress_research", compress_research)

# Add edges to connect nodes
future_research_builder.add_edge(START, "llm_call")
future_research_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    {
        "tool_node": "tool_node", # Continue research loop
        "compress_research": "compress_research", # Provide final answer
    },
)
future_research_builder.add_edge("tool_node", "llm_call") # Loop back for more research
future_research_builder.add_edge("compress_research", END)

# Compile the agent
future_research_agent = future_research_builder.compile()
