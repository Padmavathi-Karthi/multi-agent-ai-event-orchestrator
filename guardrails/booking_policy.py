"""
Booking Policy Engine (Guardrails Layer)
========================================

This module defines deterministic business rules for an AI event
coordination system.

It acts as a guardrails layer between:
- probabilistic LLM-based understanding (slot extraction)
- deterministic booking approval logic

The goal is to ensure all decisions comply with strict operational,
financial, and capacity constraints that cannot be overridden by
natural language interpretation.
"""

import datetime
from typing import Any, Dict, List, Tuple

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


# -----------------------------
# Policy Configuration
# -----------------------------
MAX_GUESTS = 170
MAX_DEPOSIT_GBP = 300
MAX_VEGAN_RATIO = 0.80

CUTOFF_HOUR = 16
CUTOFF_MINUTE = 45


# -----------------------------
# Core policy logic (framework-agnostic)
# -----------------------------
def validate_booking_policy(
    guests: float,
    vegans: float,
    deposit: float,
) -> Tuple[bool, str]:
    """
    Evaluates booking request against deterministic constraints.

    Returns:
        (is_valid, rejection_reason)
    """

    # Time cutoff policy
    now = datetime.datetime.now()
    if now.hour > CUTOFF_HOUR or (
        now.hour == CUTOFF_HOUR and now.minute >= CUTOFF_MINUTE
    ):
        return False, "request received after processing cutoff (16:45)"

    # Capacity constraint
    if guests > MAX_GUESTS:
        return False, f"guest count {int(guests)} exceeds maximum capacity"

    # Financial constraint
    if deposit > MAX_DEPOSIT_GBP:
        return False, f"deposit exceeds authorised limit ({MAX_DEPOSIT_GBP} GBP)"

    # Dietary constraint
    vegan_ratio = vegans / guests if guests > 0 else 0
    if vegan_ratio > MAX_VEGAN_RATIO:
        return False, "vegan meal ratio exceeds acceptable threshold"

    return True, "approved"


# -----------------------------
# Framework adapter (Rasa action layer)
# -----------------------------
class BookingPolicyValidator(Action):
    """
    Rasa adapter that executes the booking policy engine and
    maps results into conversational events.
    """

    def name(self) -> str:
        return "action_validate_booking"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any],
    ) -> List[Dict]:

        guests = float(tracker.get_slot("guest_count") or 0)
        vegans = float(tracker.get_slot("vegan_count") or 0)
        deposit = float(tracker.get_slot("deposit_amount_gbp") or 0)

        def reject(reason: str):
            dispatcher.utter_message(
                text=(
                    f"Booking requires manual review. "
                    f"Reason: {reason}."
                )
            )
            return [
                SlotSet("booking_valid", False),
                SlotSet("rejection_reason", reason),
            ]

        is_valid, reason = validate_booking_policy(guests, vegans, deposit)

        if not is_valid:
            return reject(reason)

        dispatcher.utter_message(
            text=(
                "Booking validated and approved. "
                f"{int(guests)} guests, {int(vegans)} vegan meals, "
                f"{deposit:.0f} GBP deposit."
            )
        )

        return [SlotSet("booking_valid", True)]

