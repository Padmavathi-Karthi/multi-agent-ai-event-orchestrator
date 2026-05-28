"""
Research Agent (Sovereign Agent System)
=======================================

This module implements an autonomous ReAct-style research agent built
on LangGraph.

It is designed as a stable execution interface that can evolve internally
without breaking downstream consumers.

Architecture
------------
- LLM handles reasoning and tool selection
- Tools provide external capabilities (search, environment interaction)
- LangGraph manages execution flow and iterative reasoning

The public API remains stable across iterations:
    run_research_agent(task: str, max_turns: int) -> dict

All improvements (new tools, planning strategies, memory systems)
are implemented internally without changing this interface.
"""

import os
from typing import Dict, List, Any

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from sovereign_agent.tools.venue_tools import (
    check_pub_availability,
    get_event_weather,
    calculate_catering_cost,
    generate_event_flyer,
)

load_dotenv()

# ---------------------------------------------------------------------
# Model configuration
# ---------------------------------------------------------------------

llm = ChatOpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=os.getenv("NEBIUS_KEY"),
    model="meta-llama/Llama-3.3-70B-Instruct",
    temperature=0,
)

# ---------------------------------------------------------------------
# Tool registry
# ---------------------------------------------------------------------

TOOLS = [
    check_pub_availability,
    get_event_weather,
    calculate_catering_cost,
    generate_event_flyer,
]

_agent = create_react_agent(llm, TOOLS)

# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

def run_research_agent(task: str, max_turns: int = 8) -> Dict[str, Any]:
    """
    Executes an autonomous research task using a ReAct agent loop.

    Args:
        task: Natural language instruction for the agent
        max_turns: Maximum reasoning iterations allowed

    Returns:
        Dictionary containing:
            - final_answer: Agent's final response
            - tool_calls_made: List of tool invocations
            - full_trace: Execution trace of reasoning steps
            - success: Whether the agent produced a final answer
    """

    result = _agent.invoke(
        {"messages": [("user", task)]},
        config={"recursion_limit": max_turns * 2},
    )

    tool_calls: List[Dict[str, Any]] = []
    trace: List[Dict[str, Any]] = []
    final_answer: str = ""

    for message in result.get("messages", []):
        role = getattr(message, "type", "unknown")
        content = message.content

        # Extract tool usage events
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "tool_use":
                    tool_calls.append({
                        "tool": item.get("name"),
                        "args": item.get("input", {}),
                    })
                    trace.append({
                        "type": "tool_call",
                        "tool": item.get("name"),
                        "args": item.get("input", {}),
                    })
            continue

        if content:
            trace.append({
                "role": role,
                "content": str(content),
            })

            if role == "ai":
                final_answer = str(content)

    return {
        "final_answer": final_answer,
        "tool_calls_made": tool_calls,
        "full_trace": trace,
        "success": bool(final_answer),
    }

