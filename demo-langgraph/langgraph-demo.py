"""Minimal LangGraph demo using DeepSeek's OpenAI-compatible API."""

import argparse
import os
import sqlite3
from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

ROOT_DIR = Path(__file__).resolve().parent.parent
SKILLS_DIR = Path(__file__).with_name("skills")


@tool
def search_factorio_files(query: str) -> str:
    """Search tracked text files in the repository for a keyword."""
    if not query.strip():
        return "The search query is empty."

    matches = []
    for path in ROOT_DIR.rglob("*"):
        if not path.is_file() or ".git" in path.parts or ".venv" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if query.lower() in text.lower():
            matches.append(str(path.relative_to(ROOT_DIR)))
        if len(matches) >= 20:
            break

    return "\n".join(matches) if matches else "No matching files found."


def build_graph(model_name: str, checkpointer: SqliteSaver):
    model = ChatOpenAI(
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com",
        model=model_name,
        temperature=0,
    )

    tools = [search_factorio_files]
    model_with_tools = model.bind_tools(tools)

    def call_model_with_tools(state: MessagesState) -> MessagesState:
        return {"messages": [model_with_tools.invoke(state["messages"])]}

    graph = StateGraph(MessagesState)
    graph.add_node("chat", call_model_with_tools)
    graph.add_node("tools", ToolNode(tools))
    graph.add_edge(START, "chat")
    graph.add_conditional_edges("chat", tools_condition, {"tools": "tools", END: END})
    graph.add_edge("tools", "chat")
    return graph.compile(checkpointer=checkpointer)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a question through LangGraph.")
    parser.add_argument(
        "question",
        nargs="?",
        default="Explain LangGraph in one short paragraph.",
        help="The question to send to the model.",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("LANGGRAPH_MODEL", "deepseek-v4-flash"),
        help="DeepSeek model name (default: LANGGRAPH_MODEL or deepseek-v4-flash).",
    )
    parser.add_argument(
        "--session-id",
        default=os.getenv("LANGGRAPH_SESSION_ID", "default"),
        help="Conversation ID to resume (default: LANGGRAPH_SESSION_ID or default).",
    )
    parser.add_argument(
        "--db",
        default=os.getenv("LANGGRAPH_CHECKPOINT_DB", "demo-langgraph/checkpoints.db"),
        help="SQLite checkpoint database path.",
    )
    args = parser.parse_args()

    if not os.getenv("DEEPSEEK_API_KEY"):
        parser.error("DEEPSEEK_API_KEY is not set.")

    skill = "\n\n".join(
        path.read_text(encoding="utf-8") for path in sorted(SKILLS_DIR.glob("*.md"))
    )
    database_path = Path(args.db)
    database_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database_path, check_same_thread=False) as connection:
        checkpointer = SqliteSaver(connection)
        checkpointer.setup()
        graph = build_graph(args.model, checkpointer)
        config = {"configurable": {"thread_id": args.session_id}}
        existing_state = graph.get_state(config)
        messages = [HumanMessage(content=args.question)]
        if not existing_state.values.get("messages"):
            messages.insert(0, SystemMessage(content=skill))
        result = graph.invoke(
            {"messages": messages},
            config=config,
        )
        print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
