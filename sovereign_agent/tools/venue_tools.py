"""
Venue Tool Layer (Sovereign Agent System)
=========================================

This module defines the core tool interface used by the autonomous
research agent and external MCP clients.

Design Principles
------------------
Each tool:
- performs a single atomic operation
- returns a structured dictionary
- never raises exceptions for expected failures
- is safe to use inside iterative agent loops

These tools are shared across:
- LangGraph research agent
- MCP tool server
- future external agent clients
"""

import os
import requests
from typing import Dict, Any
from openai import OpenAI
from langchain_core.tools import tool


# ---------------------------------------------------------------------
# Static venue registry (Week 1 baseline dataset)
# ---------------------------------------------------------------------

VENUES: Dict[str, Dict[str, Any]] = {
    "The Albanach": {
        "capacity": 180,
        "vegan": True,
        "status": "available",
        "address": "2 Hunter Square",
    },
    "The Haymarket Vaults": {
        "capacity": 160,
        "vegan": True,
        "status": "available",
        "address": "1 Dalry Road",
    },
    "The Guilford Arms": {
        "capacity": 200,
        "vegan": False,
        "status": "available",
        "address": "1 West Register Street",
    },
    "The Bow Bar": {
        "capacity": 80,
        "vegan": True,
        "status": "full",
        "address": "80 West Bow",
    },
}


# ---------------------------------------------------------------------
# Tool: venue availability check
# ---------------------------------------------------------------------

@tool
def check_pub_availability(
    pub_name: str,
    required_capacity: int,
    requires_vegan: bool,
) -> Dict[str, Any]:
    """
    Evaluate whether a venue satisfies booking constraints.
    """

    venue = VENUES.get(pub_name)

    if not venue:
        return {
            "success": False,
            "error": f"Unknown venue: {pub_name}",
            "known_venues": list(VENUES.keys()),
        }

    meets_constraints = (
        venue["capacity"] >= required_capacity
        and (not requires_vegan or venue["vegan"])
        and venue["status"] == "available"
    )

    return {
        "success": True,
        "pub_name": pub_name,
        "capacity": venue["capacity"],
        "vegan": venue["vegan"],
        "status": venue["status"],
        "address": venue["address"],
        "meets_all_constraints": meets_constraints,
    }


# ---------------------------------------------------------------------
# Tool: weather lookup
# ---------------------------------------------------------------------

@tool
def get_venue_weather() -> Dict[str, Any]:
    """
    Fetch current weather for event planning purposes.
    """

    try:
        resp = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": 55.95,
                "longitude": -3.19,
                "current": "temperature_2m,weather_code,precipitation",
            },
            timeout=8,
        )
        resp.raise_for_status()

        data = resp.json().get("current", {})
        code = data.get("weather_code", -1)

        return {
            "success": True,
            "temperature_c": data.get("temperature_2m"),
            "weather_code": code,
            "outdoor_ok": code in {0, 1, 2},
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


# ---------------------------------------------------------------------
# Tool: cost estimation
# ---------------------------------------------------------------------

@tool
def calculate_catering_cost(
    guests: int,
    price_per_head_gbp: float,
) -> Dict[str, Any]:
    """
    Compute total catering cost for an event.
    """

    if guests <= 0 or price_per_head_gbp < 0:
        return {
            "success": False,
            "error": "Invalid input values",
        }

    return {
        "success": True,
        "guests": guests,
        "price_per_head_gbp": price_per_head_gbp,
        "total_cost_gbp": round(guests * price_per_head_gbp, 2),
    }


# ---------------------------------------------------------------------
# Tool: event flyer generation
# ---------------------------------------------------------------------

@tool
def generate_event_flyer(
    venue_name: str,
    guest_count: int,
    event_theme: str,
) -> Dict[str, Any]:
    """
    Generate an AI event flyer image for a confirmed venue.
    """

    client = OpenAI(
        base_url="https://api.tokenfactory.nebius.com/v1/",
        api_key=os.getenv("NEBIUS_KEY"),
        timeout=20,
    )

    prompt = (
        f"Event flyer for {event_theme} at {venue_name}. "
        f"{guest_count} attendees. Modern design, cinematic lighting."
    )

    try:
        response = client.images.generate(
            model="black-forest-labs/flux-schnell",
            prompt=prompt,
            n=1,
        )

        return {
            "success": True,
            "prompt": prompt,
            "image_url": response.data[0].url,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "prompt": prompt,
        }

