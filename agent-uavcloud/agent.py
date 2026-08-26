"""ADK root agent for UAV cloud platform conversations."""

import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from tavily import TavilyClient


def tavily_search(query: str) -> dict:
    """Search current UAV, aviation, and cloud-platform information."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return {"error": "TAVILY_API_KEY is not configured."}

    client = TavilyClient(api_key=api_key)
    payload = client.search(
        query=query,
        search_depth="basic",
        max_results=5,
    )

    return {
        "query": query,
        "results": [
            {
                "title": result["title"],
                "url": result["url"],
                "content": result["content"],
            }
            for result in payload.get("results", [])
        ],
    }


use_tavily_search = os.getenv("ENABLE_TAVILY_SEARCH", "0") == "1"
agent_tools = [tavily_search] if use_tavily_search else []

root_agent = Agent(
    name="uav_cloud_agent",
    model=LiteLlm(model="deepseek/deepseek-chat"),
    description=(
        "A conversational assistant for UAV operations and cloud platform design."
    ),
    instruction=(
        "You are a senior UAV cloud platform consultant and helpful technical chat agent. "
        "Help users design, operate, and troubleshoot drone systems connected to cloud "
        "services. Cover mission planning, telemetry, command and control, fleet and "
        "device management, video and sensor streaming, edge computing, storage, event "
        "pipelines, digital twins, dashboards, APIs, observability, cost, reliability, "
        "privacy, cybersecurity, aviation compliance, and safe operating procedures. "
        "Start by clarifying the user's goal, drone hardware, communication link, scale, "
        "region, latency, and compliance requirements when those details affect the answer. "
        "Offer concrete architecture diagrams in text, API contracts, data models, rollout "
        "plans, and implementation steps when useful. Distinguish cloud simulation from "
        "real-world flight control: never present untested code as flight-safe, and advise "
        "human authorization, geofencing, fail-safe behavior, and local regulations for "
        "real aircraft. Do not invent vendor capabilities or regulatory requirements. "
        "When current information is needed and tavily_search is enabled, use it and cite "
        "the source URLs. If search is unavailable, clearly state the uncertainty."
    ),
    tools=agent_tools,
)
