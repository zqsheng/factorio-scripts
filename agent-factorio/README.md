# Factorio Script Agent

A Google ADK agent for writing, explaining, and debugging Factorio scripts.
The main model is DeepSeek, accessed through LiteLLM.

## Requirements

- Python 3.13+
- DeepSeek API key
- Tavily API key for web search (enabled by default)

The project environment is located at `../.venv`.

## Configure

From the repository root:

```zsh
export DEEPSEEK_API_KEY="your-deepseek-api-key"
export TAVILY_API_KEY="your-tavily-api-key"
```

Do not commit API keys to the repository.

## Launch

Interactive terminal mode:

```zsh
./agent-factorio/launch_cli.sh
```

Web UI:

```zsh
./agent-factorio/launch_web.sh
```

The web UI runs at <http://127.0.0.1:8000>. Set a different port with `ADK_PORT`.

```zsh
ADK_PORT=8080 ./agent-factorio/launch_web.sh
```

## Search Providers

Tavily search is enabled by default and works with the DeepSeek agent:

```zsh
ENABLE_TAVILY_SEARCH=1 ./agent-factorio/launch_cli.sh
```

Run without web search:

```zsh
ENABLE_TAVILY_SEARCH=0 ./agent-factorio/launch_cli.sh
```

Google Search is optional and uses a Gemini search sub-agent. It requires a
Google API key and may be subject to Gemini quota limits:

```zsh
export GOOGLE_API_KEY="your-google-api-key"
ENABLE_GOOGLE_SEARCH=1 ./agent-factorio/launch_cli.sh
```

## Files

- `agent.py`: Defines the ADK root agent and search tools.
- `instruction.md`: Root agent behavior and delegation instructions.
- `launch_cli.sh`: Starts interactive ADK terminal mode.
- `launch_web.sh`: Starts the ADK local web UI.
