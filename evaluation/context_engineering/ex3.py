"""
Rasa CALM Evaluation — Structured Dialogue & Policy Enforcement
==============================================================

This file documents behavioural observations from a Rasa Pro CALM
conversational agent used for booking confirmation workflows.

The evaluation compares:

- CALM (flow + LLM + deterministic actions)
- Traditional Rasa (NLU + rules + forms + validation classes)

Focus areas:
- slot extraction behaviour
- escalation logic under constraints
- out-of-scope handling
- system determinism vs flexibility
"""

# ─────────────────────────────────────────────────────────────
# Conversation 1 — Happy Path (Successful Booking)
# ─────────────────────────────────────────────────────────────

CONVERSATION_1_LOG = """
User:  I am calling to confirm a booking
Agent: How many guests are you confirming for tonight's event?
User:  160 guests
Agent: And how many of those guests will need vegan meals?
User:  about 50 need vegan
Agent: What deposit amount in GBP are you proposing to secure the booking?
User:  £200 deposit
Agent: Booking confirmed. 160 guests, 50 vegan meals, £200 deposit accepted.
"""

CONVERSATION_1_OUTCOME = "confirmed"


# ─────────────────────────────────────────────────────────────
# Conversation 2 — Policy Violation (Deposit Limit)
# ─────────────────────────────────────────────────────────────

CONVERSATION_2_LOG = """
User:  I am calling to confirm a booking
Agent: How many guests are you confirming for tonight's event?
User:  160 guests
Agent: And how many of those guests will need vegan meals?
User:  about 50 need vegan
Agent: What deposit amount in GBP are you proposing to secure the booking?
User:  £500 deposit
Agent: Escalation triggered due to deposit exceeding £300 limit.
"""

CONVERSATION_2_OUTCOME = "escalated"

CONVERSATION_2_REASON = """
Deposit value exceeded the authorised business limit of £300,
triggering deterministic escalation in ActionValidateBooking.
"""


# ─────────────────────────────────────────────────────────────
# Conversation 3 — Out-of-Scope Input Handling
# ─────────────────────────────────────────────────────────────

CONVERSATION_3_LOG = """
User:  I am calling to confirm a booking
Agent: How many guests are you confirming for tonight's event?
User:  160 guests
Agent: And how many of those guests will need vegan meals?
User:  can you arrange parking for the speakers?
Agent: Out-of-scope request detected. Redirecting to booking flow.
"""

CONVERSATION_3_OUTCOME = "redirected"

OUT_OF_SCOPE_BEHAVIOUR = """
The system refused to process unrelated requests and redirected the
conversation back to the booking workflow.

This demonstrates bounded conversational behaviour rather than open-ended
generation.
"""


# ─────────────────────────────────────────────────────────────
# Cross-System Comparison — CALM vs LangGraph
# ─────────────────────────────────────────────────────────────

OUT_OF_SCOPE_COMPARISON = """
LangGraph (Exercise 2) attempted to continue reasoning but produced weak
domain containment when faced with out-of-scope inputs.

CALM, in contrast, enforces strict flow boundaries. It does not attempt
to improvise answers outside its defined booking workflow, making it
more predictable and safer for operational deployment.

Trade-off:
- LangGraph → flexible reasoning, weaker constraints
- CALM → constrained behaviour, stronger safety guarantees
"""


# ─────────────────────────────────────────────────────────────
# Task B — Cutoff Guard Evaluation
# ─────────────────────────────────────────────────────────────

CUTOFF_GUARD_ENABLED = True

FILES_MODIFIED = [
    "exercise3_rasa/actions/actions.py",
    "evaluation/context_engineering/ex3.py"
]

CUTOFF_TESTING_METHOD = """
The cutoff logic was validated by enabling the 16:45 time guard,
retraining the Rasa model, restarting the action server, and testing
a booking flow after the cutoff threshold. The expected escalation
behaviour was confirmed.
"""


# ─────────────────────────────────────────────────────────────
# System Design Reflection — CALM vs Classic Rasa
# ─────────────────────────────────────────────────────────────

CALM_VS_CLASSIC_RASA = """
Traditional Rasa required explicit intent classification (NLU), rule
definition (rules.yml), and custom validation classes for slot parsing.

CALM removes most of this boilerplate by shifting responsibility to the
LLM for:
- flow selection
- slot extraction

Python is still used for deterministic enforcement of business rules,
which is where reliability is most important.

This simplifies development significantly while maintaining control
over critical decision logic.
"""


# ─────────────────────────────────────────────────────────────
# System Trade-off Analysis
# ─────────────────────────────────────────────────────────────

SYSTEM_TRADEOFF = """
CALM reduces implementation complexity and improves natural language
understanding, but introduces opacity in decision-making compared to
fully explicit rule-based systems.

It is best suited for constrained operational workflows (e.g., booking,
support triage) where correctness is defined by business rules rather
than open-ended reasoning.
"""