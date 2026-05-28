"""
Tool Tests (Sovereign Agent System)
==========================================

This test suite validates the correctness of core tool implementations
used by the sovereign_agent system.

Scope
-----
These tests focus on individual tool functions rather than full agent
execution. This makes them:

- Fast to run
- Deterministic (no LLM dependency)
- Useful for debugging tool-level failures

Test Strategy
-------------
Each tool is tested for:
- Correct output schema
- Deterministic behavior
- Edge case handling
- Error conditions

These tests form the foundation of system reliability before integration
into the full agent loop.
"""

import json
import sys
from pathlib import Path

import pytest

# Ensure package imports resolve correctly
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sovereign_agent.tools.venue_tools import (
    check_pub_availability,
    get_event_weather,
    calculate_catering_cost,
    generate_event_flyer,
)


# ---------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------

def _call(tool_fn, **kwargs) -> dict:
    """
    Safely execute a tool function and return parsed JSON output.
    Handles both raw dict returns and JSON-string wrapped outputs.
    """
    raw_fn = tool_fn.func if hasattr(tool_fn, "func") else tool_fn
    result = raw_fn(**kwargs)
    return json.loads(result) if isinstance(result, str) else result


# ---------------------------------------------------------------------
# Tests: check_pub_availability
# ---------------------------------------------------------------------

class TestCheckPubAvailability:

    def test_available_venue_meets_all_constraints(self):
        result = _call(
            check_pub_availability,
            pub_name="The Haymarket Vaults",
            required_capacity=160,
            requires_vegan=True,
        )
        assert result["success"] is True
        assert result["meets_all_constraints"] is True

    def test_full_venue_fails_constraints(self):
        result = _call(
            check_pub_availability,
            pub_name="The Bow Bar",
            required_capacity=160,
            requires_vegan=True,
        )
        assert result["success"] is True
        assert result["meets_all_constraints"] is False
        assert result["status"] == "full"

    def test_insufficient_capacity_fails(self):
        result = _call(
            check_pub_availability,
            pub_name="The Bow Bar",
            required_capacity=160,
            requires_vegan=False,
        )
        assert result["success"] is True
        assert result["meets_all_constraints"] is False

    def test_vegan_requirement_enforced(self):
        result = _call(
            check_pub_availability,
            pub_name="The Guilford Arms",
            required_capacity=100,
            requires_vegan=True,
        )
        assert result["success"] is True
        assert result["meets_all_constraints"] is False

    def test_unknown_venue_returns_error_payload(self):
        result = _call(
            check_pub_availability,
            pub_name="The Imaginary Pub",
            required_capacity=100,
            requires_vegan=False,
        )
        assert result["success"] is False
        assert "error" in result
        assert "known_venues" in result
        assert isinstance(result["known_venues"], list)

    def test_returns_address_field(self):
        result = _call(
            check_pub_availability,
            pub_name="The Albanach",
            required_capacity=100,
            requires_vegan=False,
        )
        assert result["success"] is True
        assert isinstance(result["address"], str)
        assert len(result["address"]) > 0

    def test_returns_valid_json_string(self):
        raw_fn = (
            check_pub_availability.func
            if hasattr(check_pub_availability, "func")
            else check_pub_availability
        )
        raw = raw_fn(
            pub_name="The Albanach",
            required_capacity=100,
            requires_vegan=False,
        )

        assert isinstance(raw, str)
        parsed = json.loads(raw)
        assert isinstance(parsed, dict)


# ---------------------------------------------------------------------
# Tests: calculate_catering_cost
# ---------------------------------------------------------------------

class TestCalculateCateringCost:

    def test_correct_cost_calculation(self):
        result = _call(
            calculate_catering_cost,
            guests=160,
            price_per_head_gbp=35.0,
        )
        assert result["success"] is True
        assert result["total_cost_gbp"] == 5600.0

    def test_zero_guests_rejected(self):
        result = _call(
            calculate_catering_cost,
            guests=0,
            price_per_head_gbp=35.0,
        )
        assert result["success"] is False

    def test_negative_price_rejected(self):
        result = _call(
            calculate_catering_cost,
            guests=160,
            price_per_head_gbp=-5.0,
        )
        assert result["success"] is False

    def test_cost_rounding_precision(self):
        result = _call(
            calculate_catering_cost,
            guests=3,
            price_per_head_gbp=33.333,
        )
        assert result["success"] is True
        assert abs(result["total_cost_gbp"] - 100.0) < 0.01


# ---------------------------------------------------------------------
# Tests: generate_event_flyer
# ---------------------------------------------------------------------

class TestGenerateEventFlyer:

    def test_required_output_schema(self):
        result = _call(
            generate_event_flyer,
            venue_name="The Haymarket Vaults",
            guest_count=160,
            event_theme="AI Meetup",
        )

        assert "success" in result
        assert "prompt_used" in result
        assert "image_url" in result

    def test_prompt_contains_venue_reference(self):
        result = _call(
            generate_event_flyer,
            venue_name="The Haymarket Vaults",
            guest_count=160,
            event_theme="AI Meetup",
        )
        assert "Haymarket" in result["prompt_used"]

    def test_tool_not_stubbed(self):
        result = _call(
            generate_event_flyer,
            venue_name="The Haymarket Vaults",
            guest_count=160,
            event_theme="AI Meetup",
        )

        assert "STUB" not in str(result.get("error", ""))

    def test_image_url_valid_when_successful(self):
        result = _call(
            generate_event_flyer,
            venue_name="The Haymarket Vaults",
            guest_count=160,
            event_theme="AI Meetup",
        )

        if result.get("success"):
            assert isinstance(result["image_url"], str)
            assert len(result["image_url"]) > 0

