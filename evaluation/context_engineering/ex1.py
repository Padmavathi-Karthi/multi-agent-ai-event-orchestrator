"""
Context Engineering Evaluation — Experiment 1
============================================

This file documents results from prompt structure experiments
comparing different instruction formats:

- Plain text prompting
- XML-structured prompting
- Sandwich (delimited) prompting

The goal is to observe how formatting affects model reliability
under constraint-heavy decision tasks.
"""

# ─────────────────────────────────────────────────────────────
# Experiment A — Base Prompt vs Structured Prompting
# ─────────────────────────────────────────────────────────────

PLAIN_PROMPT_RESULT = "The Haymarket Vaults"
XML_PROMPT_RESULT = "The Albanach"
SANDBOX_PROMPT_RESULT = "The Albanach"

PLAIN_PROMPT_CORRECT = True
XML_PROMPT_CORRECT = True
SANDBOX_PROMPT_CORRECT = True


EXPERIMENT_A_OBSERVATION = """
The plain prompt produced a correct result, but structured formats
(XML and sandwich-style prompting) improved consistency and made
constraint handling more explicit.

Structured prompts reduced ambiguity by separating rules from data,
which helped the model prioritise constraints more reliably.
"""


# ─────────────────────────────────────────────────────────────
# Experiment B — Distractor Sensitivity Test
# ─────────────────────────────────────────────────────────────

PLAIN_PROMPT_RESULT_B = "The Haymarket Vaults"
XML_PROMPT_RESULT_B = "The Albanach"
SANDBOX_PROMPT_RESULT_B = "The Albanach"

PLAIN_PROMPT_CORRECT_B = True
XML_PROMPT_CORRECT_B = True
SANDBOX_PROMPT_CORRECT_B = True

DID_RESULTS_CHANGE_WITH_DISTRACTORS = True

MOST_CONFUSING_DISTRACTOR_EXPLANATION = """
The most challenging distractor was the one most similar in capacity
and features to valid options. When multiple venues appear valid at a
surface level, weaker prompt structure increases the likelihood of
selecting a "close enough" but incorrect match.

This highlights how distractors amplify the importance of structured prompts.
"""


# ─────────────────────────────────────────────────────────────
# Experiment C — Model Sensitivity (Smaller Model Test)
# ─────────────────────────────────────────────────────────────

PART_C_WAS_RUN = True

PLAIN_PROMPT_RESULT_C = "The Haymarket Vaults"
XML_PROMPT_RESULT_C = "The Haymarket Vaults"
SANDBOX_PROMPT_RESULT_C = "The Haymarket Vaults"

EXPERIMENT_C_OBSERVATION = """
Smaller models showed higher sensitivity to prompt structure.
Even when outputs remained correct, structured formats improved
stability and reduced variance in reasoning.

This suggests that context engineering becomes increasingly important
as model capability decreases.
"""


# ─────────────────────────────────────────────────────────────
# Key Insight — Context Engineering Principle
# ─────────────────────────────────────────────────────────────

CORE_INSIGHT = """
Context formatting becomes critical when tasks involve multiple
simultaneous constraints, competing options, or hidden distractors.

Well-structured prompts help models:
- separate constraints from content
- reduce ambiguity in decision-making
- improve consistency across similar inputs

In short, structure improves reliability more than verbosity.
"""