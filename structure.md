# Project Structure - Company Research Assistant

## Directory Organization

### Root Level Structure

```
company_research_assistant/
├── src/
│   └── company_research_assistant/
│       ├── __init__.py
│       ├── agents/                    # Research agent implementations
│       ├── core/                      # Core system components
│       ├── prompts/                   # Prompt templates and messaging
│       ├── state/                     # State management and schemas
│       ├── tools/                     # Research tools and integrations
│       └── utils/                     # Utility functions and helpers
├── notebooks/                         # Development and tutorial notebooks
├── tests/                            # Test suite
├── docs/                             # Documentation and guides
├── pyproject.toml                    # Project configuration and dependencies
├── uv.lock                           # Dependency lock file
├── .env.example                      # Environment variables template
├── product.md                        # Product overview and requirements
├── tech.md                           # Technology stack documentation
└── structure.md                      # This file - project structure guide
```

## Source Code Organization (`src/company_research_assistant/`)

### Agent Implementations (`agents/`)

Specialized research agents for different company research domains:

```
agents/
├── __init__.py
├── base_agent.py                     # Base agent class and common functionality
├── past_research_agent.py            # Company history and background research
├── future_research_agent.py          # Strategic plans and future prospects
├── culture_research_agent.py         # Values, culture, and workplace analysis
└── supervisor_agent.py               # Multi-agent coordination and synthesis
```

**Naming Convention:** `{research_domain}_agent.py`
**Base Class:** All agents inherit from `BaseResearchAgent`
**State Management:** Each agent maintains isolated state using domain-specific schemas

### Core System Components (`core/`)

Fundamental system architecture and workflow management:

```
core/
├── __init__.py
├── workflow.py                       # Main workflow orchestration
├── config.py                         # System configuration and settings
├── models.py                         # LLM initialization and management
└── exceptions.py                     # Custom exception definitions
```

**Architecture Pattern:** Single entry point via `workflow.py` with modular component injection
**Configuration Management:** Environment-based config with validation via Pydantic

### Prompt Templates (`prompts/`)

Organized prompt templates for different research contexts:

```
prompts/
├── __init__.py
├── base_prompts.py                   # Common prompt templates and formatting
├── company_research_prompts.py       # Company-specific research prompts
├── agent_prompts.py                  # Individual agent prompt templates
└── synthesis_prompts.py              # Report generation and synthesis prompts
```

**Template Organization:** Prompts grouped by functional area and agent type
**Variable Injection:** All prompts use `.format()` with named parameters
**Internationalization Ready:** Template structure supports multi-language expansion

### State Management (`state/`)

State schemas and management for different workflow components:

```
state/
├── __init__.py
├── base_state.py                     # Base state classes and common schemas
├── agent_states.py                   # Individual agent state definitions
├── supervisor_state.py               # Multi-agent coordination state
└── workflow_state.py                 # End-to-end workflow state management
```

**State Pattern:** TypedDict-based state with Pydantic validation
**Immutability:** State updates via Command pattern for auditability
**Type Safety:** Comprehensive type hints for all state attributes

### Research Tools (`tools/`)

External integrations and research utilities:

```
tools/
├── __init__.py
├── web_search.py                     # Tavily search integration and web research
├── content_processing.py             # Web content summarization and extraction
├── file_research.py                  # MCP-based local file research
├── company_apis.py                   # Third-party company data API integrations
└── validation.py                     # Research quality validation tools
```

**Tool Interface:** All tools implement standardized LangChain tool interface
**Error Handling:** Graceful degradation for external service failures
**Rate Limiting:** Built-in throttling for external API compliance

### Utility Functions (`utils/`)

Shared utilities and helper functions:

```
utils/
├── __init__.py
├── formatting.py                     # Output formatting and presentation
├── logging.py                        # Logging configuration and utilities
├── date_utils.py                     # Date handling and formatting
└── text_processing.py                # Text analysis and processing utilities
```

## File Naming Conventions

### Python Modules

- **Snake Case:** All Python files use `snake_case.py`
- **Descriptive Names:** File names clearly indicate functionality
- **Domain Prefixes:** Agent files prefixed with research domain (e.g., `past_research_agent.py`)

### Classes and Functions

```python
# Class naming - PascalCase
class PastResearchAgent(BaseResearchAgent):
    pass

class CompanyResearchState(TypedDict):
    pass

# Function naming - snake_case
def conduct_company_research(company_name: str, job_description: Optional[str] = None):
    pass

def format_research_findings(findings: List[ResearchFinding]) -> str:
    pass

# Constants - UPPER_SNAKE_CASE
MAX_RESEARCH_ITERATIONS = 6
DEFAULT_SEARCH_TIMEOUT = 30
```

### State and Schema Naming

```python
# State classes - descriptive and domain-specific
class PastResearchState(TypedDict):
    company_history: str
    founding_details: str
    key_milestones: List[str]

class FutureResearchState(TypedDict):
    strategic_plans: str
    growth_projections: str
    expansion_initiatives: List[str]

# Tool schemas - action-oriented
class SearchCompanyNews(BaseModel):
    company_name: str
    time_range: Optional[str] = "1y"

class AnalyzeCompanyCulture(BaseModel):
    company_name: str
    focus_areas: List[str]
```

## Import Patterns

### Standard Import Organization

```python
# Standard library imports
import asyncio
import operator
from typing import Optional, List, Dict, Any
from typing_extensions import Literal, TypedDict, Annotated

# Third-party imports
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command

# Local imports - absolute from package root
from company_research_assistant.agents.base_agent import BaseResearchAgent
from company_research_assistant.state.agent_states import PastResearchState
from company_research_assistant.tools.web_search import tavily_search
from company_research_assistant.utils.formatting import format_research_report
```

### Relative Import Guidelines

- **Avoid Relative Imports:** Use absolute imports from package root
- **Explicit Imports:** Import specific classes/functions rather than modules
- **Dependency Order:** Standard library → Third-party → Local imports

## Architecture Decisions

### Multi-Agent Pattern

**Supervisor-Worker Architecture:**

- `SupervisorAgent` coordinates research across specialized agents
- Each research agent operates independently with isolated state
- Parallel execution for independent research domains
- Sequential synthesis for final report generation

### State Management Strategy

**Command-Based State Updates:**

```python
# State updates via LangGraph Commands
return Command(
    goto="next_node",
    update={
        "research_findings": new_findings,
        "research_iterations": state.get("research_iterations", 0) + 1
    }
)
```

### Tool Integration Pattern

**Standardized Tool Interface:**

```python
@tool
class ResearchCompanyBackground(BaseModel):
    """Tool for researching company history and background."""
    company_name: str = Field(description="Name of the company to research")
    focus_areas: Optional[List[str]] = Field(
        description="Specific areas to focus research on",
        default=None
    )
```

### Error Handling Strategy

**Graceful Degradation:**

```python
try:
    research_result = await agent.conduct_research(company_name)
except ExternalAPIError as e:
    logger.warning(f"External API failed: {e}")
    research_result = await agent.conduct_fallback_research(company_name)
except Exception as e:
    logger.error(f"Unexpected error in research: {e}")
    research_result = create_error_research_result(str(e))
```

## Development Workflow

### Local Development Setup

1. **Environment Creation:** `uv sync` for dependency installation
2. **Configuration:** Copy `.env.example` to `.env` and configure API keys
3. **Testing:** Run individual agent tests before integration testing
4. **Documentation:** Update relevant documentation for any architectural changes

### Code Organization Guidelines

- **Single Responsibility:** Each module focuses on one specific aspect of the system
- **Clear Interfaces:** Well-defined contracts between components
- **Testability:** Modular design enables comprehensive unit testing
- **Extensibility:** Easy addition of new research agents or tools

### Quality Standards

- **Type Hints:** All functions and classes must include comprehensive type annotations
- **Documentation:** Google-style docstrings for all public interfaces
- **Testing:** Minimum 80% code coverage for core functionality
- **Linting:** Ruff compliance for code style and quality

This structure provides a scalable foundation for the company research application while maintaining clear separation of concerns and facilitating future enhancements.
