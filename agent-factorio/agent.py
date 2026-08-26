"""Google ADK agent for assisting with Factorio scripting tasks."""

import os
from pathlib import Path

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.google_search_agent_tool import (
    GoogleSearchAgentTool,
    create_google_search_agent,
)
from tavily import TavilyClient

from .blueprint_agent import blueprint_agent
from .layout_optimizer_agent import layout_optimizer_agent


def tavily_search(query: str) -> dict:
    """Search the web with Tavily and return concise source-backed results."""
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
            {"title": item["title"], "url": item["url"], "content": item["content"]}
            for item in payload.get("results", [])
        ],
    }


use_google_search = os.getenv("ENABLE_GOOGLE_SEARCH", "0") == "1"
use_tavily_search = os.getenv("ENABLE_TAVILY_SEARCH", "1") == "1"
google_search_agent = (
    create_google_search_agent(model="gemini-2.0-flash") if use_google_search else None
)

agent_tools = []
if google_search_agent:
    agent_tools.append(GoogleSearchAgentTool(google_search_agent))
if use_tavily_search:
    agent_tools.append(tavily_search)

instruction = (Path(__file__).with_name("instruction.md")).read_text(encoding="utf-8")

root_agent = Agent(
    name="factorio_script_agent",
    model=LiteLlm(model="deepseek/deepseek-chat"),
    description="An assistant that helps write, explain, and debug Factorio scripts.",
    instruction=instruction,
    tools=agent_tools,
    sub_agents=[layout_optimizer_agent, blueprint_agent],
)
