"""ADK sub-agent for Factorio layout optimization tasks."""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

layout_optimizer_agent = Agent(
    name="layout_optimizer_agent",
    model=LiteLlm(model="deepseek/deepseek-chat"),
    description=(
        "An expert sub-agent for designing and debugging the Factorio grid-based "
        "belt layout optimizer."
    ),
    instruction=(
        "You are the layout optimization specialist. Help with the code in "
        "layout-optimizer/, especially LayoutOptimizer, Grid, A* routing, BeltNetwork, "
        "BeltPath, labs, obstacles, rendering, metrics, and tests. Explain the algorithm "
        "before proposing changes. Prefer small, testable Python fixes that match the "
        "existing APIs. Consider path length, turns, belt capacity, travel time, "
        "obstacle footprints, and unreachable routes. Do not invent project APIs; ask "
        "for the relevant file or error when context is missing."
    ),
)
