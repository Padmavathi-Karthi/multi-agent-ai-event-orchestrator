"""
MCP Evaluation — Sovereign Agent System
=======================================

This file documents observed behaviour of the MCP (Model Context Protocol)
venue server within the sovereign_agent architecture.

It evaluates:
- dynamic tool discovery
- separation of client and tool runtime
- impact of server-side state changes on agent behaviour
"""

# ── MCP Tool Discovery ─────────────────────────────────────────────────────

TOOLS_DISCOVERED = [
    "search_venues",
    "get_venue_details",
]

# ── Query Observations ─────────────────────────────────────────────────────

# Query 1: high-capacity / edge-case request
QUERY_1_VENUE_NAME = "none"
QUERY_1_VENUE_ADDRESS = "none"

QUERY_1_FINAL_ANSWER = """
The MCP client did not return a fully composed natural-language response.
It issued a search_venues tool call for a high-capacity request (e.g. 300 guests with vegan requirements).

This reflects the current system design where:
- reasoning and synthesis are minimal in the MCP client
- tool execution is delegated to the MCP server
- final response formatting is not yet handled at agent level
"""

# Query 2: standard lookup flow
QUERY_2_FINAL_ANSWER = """
The MCP client executed a two-step tool workflow:

1. search_venues to retrieve matching candidates
2. get_venue_details to fetch structured information for a selected venue

The returned data included structured fields:
- capacity
- vegan availability
- operational status
- address

The output remains tool-structured rather than fully natural language,
which is consistent with the current implementation stage.
"""

# ── Server-side experiment ──────────────────────────────────────────────────

EX4_EXPERIMENT_DONE = True

EX4_EXPERIMENT_RESULT = """
A venue's availability status was modified in
sovereign_agent/tools/mcp_venue_server.py and the MCP client was rerun.

No changes were required in the client implementation, yet the output changed
because the server-side data changed.

This confirms a key property of MCP in this architecture:
tool behaviour is centrally controlled on the server, while clients remain
stateless consumers of tool outputs.
"""

# ── Architecture comparison ────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 4
LINES_OF_TOOL_CODE_EX4 = 0

MCP_VALUE_PROPOSITION = """
MCP introduces a shared tool runtime where:
- tools are defined once on a central server
- multiple clients can discover and use tools dynamically
- updates to tool logic or data propagate immediately without client changes

Compared to LangGraph's locally defined tools, MCP improves:
- reuse across agents
- consistency of operational data
- separation of concerns between reasoning and execution
"""

# ── System design (Week 5 vision) ──────────────────────────────────────────

WEEK_5_ARCHITECTURE = """
- A routing layer should classify incoming requests into research, booking, or hybrid tasks before execution.
- A LangGraph research agent should handle open-ended reasoning tasks such as venue discovery, pricing estimation, and weather analysis using iterative tool use.
- A CALM-based conversational agent should manage structured booking flows with strict guardrails for business constraints.
- An MCP server should expose shared operational tools such as venue search and venue metadata retrieval across all agents.
- A central policy layer should enforce consistent constraints such as capacity limits and deposit rules across the entire system.
"""

# ── System-level reflection ─────────────────────────────────────────────────

GUIDING_QUESTION_ANSWER = """
The LangGraph agent is better suited for research tasks because it can iteratively explore tools, compare venues, and refine results dynamically.

The CALM booking agent is better suited for structured workflows because it enforces deterministic constraints such as deposit limits and cutoff rules.

Swapping them breaks the design assumptions: research requires flexibility and exploration, while booking requires strict control and auditability.

MCP sits between them as a shared infrastructure layer, providing consistent tool access without embedding decision logic in the clients.
"""