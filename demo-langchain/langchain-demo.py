"""Minimal LangChain chat demo."""

import argparse
import os

from langchain.chat_models import init_chat_model


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask a question with LangChain.")
    parser.add_argument(
        "question",
        nargs="?",
        default="Explain LangChain in one short paragraph.",
        help="The question to send to the model.",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("LANGCHAIN_MODEL", "gpt-4o-mini"),
        help="Chat model name (default: LANGCHAIN_MODEL or gpt-4o-mini).",
    )
    args = parser.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        parser.error("OPENAI_API_KEY is not set.")

    model = init_chat_model(
        args.model,
        model_provider="openai",
        temperature=0,
    )
    response = model.invoke(args.question)
    print(response.content)


if __name__ == "__main__":
    main()
