# LangChain Demo

This directory contains a minimal LangChain chat example.

## How the framework works

LangChain provides standard interfaces for building applications around language
models. The application assembles a pipeline from reusable components:

```text
user question -> prompt/messages -> chat model -> model response -> application output
```

This demo uses the following flow:

1. `argparse` reads a question and an optional model name.
2. `init_chat_model` creates a LangChain chat-model abstraction for the OpenAI provider.
3. `model.invoke(question)` sends the question to the configured model.
4. The returned message content is printed to the terminal.

The main benefit is that application code talks to a common model interface. The
model provider, prompt, parser, tools, and storage can be changed independently
as the application grows.

## Current capabilities

This example supports:

- Single-turn question answering.
- A default question when no argument is provided.
- Model selection with `--model` or `LANGCHAIN_MODEL`.
- OpenAI-compatible chat models through `langchain`.
- Deterministic generation with `temperature=0`.

It intentionally does not yet include conversation memory, streaming, tool calls,
retrieval-augmented generation, structured output, or a web interface.

## LangChain capabilities

LangChain can be extended with:

- Prompt templates and reusable chains.
- Multi-turn message history and persistent conversation state.
- Tool calling and agents that choose tools during execution.
- Document loaders, text splitters, embeddings, and vector stores for RAG.
- Structured output parsed into typed application data.
- Streaming tokens and asynchronous execution.
- Callbacks, tracing, retries, and runtime configuration.
- Integration with many model providers and data sources.

For workflows with explicit branching, loops, durable state, or human approval,
LangGraph is a related option in `demo-langgraph`.

## Run

Use the workspace virtual environment:

```zsh
export OPENAI_API_KEY="your-openai-api-key"
/Users/zhangqishang/factorio-scripts/.venv/bin/python \
  demo-langchain/langchain-demo.py \
  "What is a LangChain runnable?"
```

Optional model override:

```zsh
LANGCHAIN_MODEL="gpt-4o-mini" \
/Users/zhangqishang/factorio-scripts/.venv/bin/python \
  demo-langchain/langchain-demo.py
```

Do not commit API keys to the repository.
