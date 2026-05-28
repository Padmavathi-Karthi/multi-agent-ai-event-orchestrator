"""
MCP Venue Service (Sovereign Agent System)
==========================================

This module implements a Model Context Protocol (MCP) server that exposes
venue-related tools as a shared service interface.

It allows multiple clients to access the same underlying venue data
through a standardised tool protocol, including:

- LangGraph research agents
- Rasa conversational agents
- Future external systems (APIs, UI, voice agents)

Architecture Role
------------------
This server acts as a shared capability layer:

    Clients (agents)  →  MCP protocol  →  Venue service tools

The internal dataset is intentionally simple in Week 1.
In later iterations, this layer can be replaced with:
- live APIs
- database queries
- web scraping or retrieval systems

The client interface remains unchanged.
"""

import json
from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------
# MCP server instance
# ---------------------------------------------------------------------

mcp = FastMCP("VenueService")

# ---------------------------------------------------------------------
# Venue registry (Week 1 static dataset)
# ---------------------------------------------------------------------

VENUES = {
    "The Albanach": {
        "capacity": 180,
        "vegan": True,
        "status": "available",
        "address": "2 Hunter Square, Edinburgh",
    },
    "The Haymarket Vaults": {
        "capacity": 160,
        "vegan": True,
        "status": "available",
        "address": "1 Dalry Road, Edinburgh",
    },
    "The Guilford Arms": {
        "capacity": 200,
        "vegan": False,
        "status": "available",
        "address": "1 West Register Street, Edinburgh",
    },
    "The Bow Bar": {
        "capacity": 80,
        "vegan": True,
        "status": "full",
        "address": "80 West Bow, Edinburgh",
    },
}

# ---------------------------------------------------------------------
# MCP tools
# ---------------------------------------------------------------------

@mcp.tool()
def search_venues(min_capacity: int, requires_vegan: bool) -> str:
    """
    Search for venues matching capacity and dietary constraints.

    Returns:
        JSON string containing:
        - matching venues
        - total count
    """
    matches = [
        {"name": name, **info}
        for name, info in VENUES.items()
        if info["capacity"] >= min_capacity
        and (not requires_vegan or info["vegan"])
        and info["status"] == "available"
    ]

    return json.dumps({
        "matches": matches,
        "count": len(matches),
    })


@mcp.tool()
def get_venue_details(pub_name: str) -> str:
    """
    Retrieve full structured information for a specific venue.

    Args:
        pub_name: Exact venue name as returned by search_venues

    Returns:
        JSON string with venue details or error payload
    """
    venue = VENUES.get(pub_name)

    if not venue:
        return json.dumps({
            "success": False,
            "error": f"Venue not found: {pub_name}",
            "known_venues": list(VENUES.keys()),
        })

    return json.dumps({
        "success": True,
        "name": pub_name,
        **venue,
    })


# ---------------------------------------------------------------------
# Local execution entrypoint (debug only)
# ---------------------------------------------------------------------

if __name__ == "__main__":
    print(f"MCP Venue Service | {len(VENUES)} venues loaded")
    mcp.run()

