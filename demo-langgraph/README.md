# LangGraph Demo

This directory contains a minimal LangGraph workflow that calls DeepSeek through
its OpenAI-compatible API.

## How the framework works

LangGraph models an application as a graph of stateful nodes. Nodes perform work,
while edges define the execution order:

```text
START -> chat node -> END
```

This demo follows that flow:

1. `MessagesState` defines the graph state as a list of chat messages.
2. `build_graph` creates a `ChatOpenAI` client configured for DeepSeek.
3. The `chat` node sends the current messages to the model.
4. The node returns the model response as an updated `messages` state.
5. `graph.invoke` starts the graph and the final message is printed.

The graph structure is explicit, so additional nodes and branches can be added
without changing the model-call interface.

## Current capabilities

This example supports:

- A single stateful graph invocation.
- One model node with explicit `START` and `END` edges.
- DeepSeek's OpenAI-compatible API through `ChatOpenAI`.
- Model selection with `--model` or `LANGGRAPH_MODEL`.
- Deterministic generation with `temperature=0`.
- A default question when no argument is provided.

It intentionally does not yet include conversation persistence, branching, loops,
tool calls, human approval, streaming, retries, or checkpoint storage.

## LangGraph capabilities

LangGraph is useful for workflows that require:

- Multiple specialized agent or processing nodes.
- Conditional routing and branches.
- Loops for planning, tool use, and iterative refinement.
- Shared state across steps.
- Durable checkpoints and resumable execution.
- Human-in-the-loop approval.
- Streaming intermediate state and custom events.
- Fault handling, retries, and observability.

LangChain supplies model, prompt, tool, and message integrations; LangGraph adds
explicit workflow orchestration and state management around those components.

## Run

Configure a DeepSeek API key and use the workspace virtual environment:

```zsh
export DEEPSEEK_API_KEY="your-deepseek-api-key"
/Users/zhangqishang/factorio-scripts/.venv/bin/python \
  demo-langgraph/langgraph-demo.py \
  "What is a graph state?"
```

The default model is `deepseek-v4-flash`. Override it with either option:

```zsh
LANGGRAPH_MODEL="deepseek-v4-flash" \
/Users/zhangqishang/factorio-scripts/.venv/bin/python \
  demo-langgraph/langgraph-demo.py
```

```zsh
/Users/zhangqishang/factorio-scripts/.venv/bin/python \
  demo-langgraph/langgraph-demo.py \
  --model deepseek-v4-flash \
  "Summarize state graphs."
```

Do not commit API keys to the repository.
