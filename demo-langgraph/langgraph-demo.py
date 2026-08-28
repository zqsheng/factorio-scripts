"""Minimal LangGraph demo using DeepSeek's OpenAI-compatible API."""

import argparse
import os

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph


def build_graph(model_name: str):
    model = ChatOpenAI(
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com",
        model=model_name,
        temperature=0,
    )

    def call_model(state: MessagesState) -> MessagesState:
        return {"messages": [model.invoke(state["messages"])]}

    graph = StateGraph(MessagesState)
    graph.add_node("chat", call_model)
    graph.add_edge(START, "chat")
    graph.add_edge("chat", END)
    return graph.compile()


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
    args = parser.parse_args()

    if not os.getenv("DEEPSEEK_API_KEY"):
        parser.error("DEEPSEEK_API_KEY is not set.")

    graph = build_graph(args.model)
    result = graph.invoke({"messages": [HumanMessage(content=args.question)]})
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()