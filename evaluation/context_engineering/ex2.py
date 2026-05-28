"""
LangGraph Agent Evaluation — Tool Use & Reasoning Behaviour
===========================================================

This file documents observed behaviour of a LangGraph-based
tool-using agent across multiple controlled scenarios.

The evaluation focuses on:

- tool invocation reliability
- fallback and recovery behaviour
- constraint satisfaction under conflicting inputs
- hallucination resistance
- structured vs unstructured reasoning traces

This is not a correctness test — it is a behavioural analysis.
"""

# ─────────────────────────────────────────────────────────────
# Task A — Tool Usage Trace
# ─────────────────────────────────────────────────────────────

TOOLS_CALLED_IN_ORDER = [
    "check_pub_availability",
    "calculate_catering_cost",
    "get_edinburgh_weather",
    "generate_event_flyer",
]

FINAL_VENUE_DECISION = "none"

CATERING_COST_GBP = 0.0

OUTDOOR_WEATHER_OK = True

TASK_A_OBSERVATION = """
The agent initiated multiple tool calls in sequence, but no stable
final decision was produced. Despite invoking tools relevant to
venue selection, cost estimation, and weather evaluation, the
reasoning loop failed to converge on a confirmed venue.

This indicates weak final-state consolidation after tool usage.
"""


# ─────────────────────────────────────────────────────────────
# Task B — Image Generation Tool Evaluation
# ─────────────────────────────────────────────────────────────

EVENT_FLYER_IMPLEMENTED = True

IMAGE_GENERATION_RESULT = "Request timed out."

IMAGE_PROMPT_USED = """
Professional event flyer for Edinburgh AI Meetup, tech professionals,
modern venue at The Haymarket Vaults, Edinburgh. 160 guests tonight.
Warm lighting, Scottish architecture background, clean modern typography.
"""

TASK_B_OBSERVATION = """
The prompt generation logic is correct and includes venue, theme,
and attendance constraints.

However, the image generation step is unstable in execution context,
suggesting external API dependency or timeout sensitivity rather than
prompt design issues.
"""


# ─────────────────────────────────────────────────────────────
# Task C — Constraint Handling & Failure Modes
# ─────────────────────────────────────────────────────────────

SCENARIO_1_PIVOT = """
After the Bow Bar was evaluated and rejected due to capacity and
availability constraints, the agent correctly shifted focus to
alternative venues. This shows functional fallback reasoning,
but lacks structured ranking between remaining options.
"""

SCENARIO_1_SELECTED_VENUE = "The Albanach"

SCENARIO_2_OUT_OF_CAPACITY_HALLUCINATION = False

SCENARIO_2_FINAL_RESPONSE = """
No known venue satisfies the requirement for 300 guests with current
constraints. Available venues (The Albanach, The Haymarket Vaults,
The Guilford Arms, The Bow Bar) all fall below required capacity.
"""

SCENARIO_3_TOOL_USAGE_IN_UNRELATED_DOMAIN = False

SCENARIO_3_RESPONSE = """
The agent correctly refused to answer an out-of-scope request but did
not explicitly classify the limitation (no explanation of tool boundary),
which reduces user clarity.
"""

SCENARIO_3_EVALUATION = """
The refusal is safe but not informative. In production systems, a better
response would explicitly state domain limitation (venue booking only)
and optionally redirect the user to supported tasks.
"""


# ─────────────────────────────────────────────────────────────
# Task D — Graph vs Declarative Flow Systems
# ─────────────────────────────────────────────────────────────

LANGGRAPH_FLOW = """
graph TD;
    agent --> tools;
    tools --> agent;
    agent --> end;
"""

FLOW_COMPARISON = """
LangGraph represents an adaptive execution loop where tool usage is
decided dynamically at runtime by the model.

In contrast, Rasa-style flow systems define explicit conversational
paths in advance. This makes Rasa more predictable and auditable,
while LangGraph provides higher flexibility but lower determinism.
"""


# ─────────────────────────────────────────────────────────────
# Key Insight — System Behaviour Summary
# ─────────────────────────────────────────────────────────────

KEY_INSIGHT = """
The system demonstrates strong tool integration capability but weak
final-state reasoning consolidation.

Key trade-off observed:
- LangGraph → flexible tool orchestration, weaker determinism
- Flow-based systems → structured control, stronger predictability

The most important limitation is not tool usage itself, but consistent
decision finalisation after multiple tool calls.
"""