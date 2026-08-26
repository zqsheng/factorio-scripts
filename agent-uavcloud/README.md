# UAV Cloud Platform Agent

A Google ADK conversational agent for UAV operations and cloud-platform design.
It uses DeepSeek through LiteLLM.

## Configure

From the repository root:

```zsh
export DEEPSEEK_API_KEY="your-deepseek-api-key"
```

Optional current-information search:

```zsh
export TAVILY_API_KEY="your-tavily-api-key"
export ENABLE_TAVILY_SEARCH=1
```

Do not commit API keys.

## Launch

Interactive terminal chat:

```zsh
./agent-uavcloud/launch_cli.sh
```

Web UI:

```zsh
./agent-uavcloud/launch_web.sh
```

The web UI uses port `8001` by default. Override it with `ADK_PORT`.

```zsh
ADK_PORT=8081 ./agent-uavcloud/launch_web.sh
```

## Scope

The agent helps with mission planning, fleet management, telemetry, command and control,
video and sensor pipelines, edge/cloud architecture, APIs, observability, security,
privacy, compliance, cost, reliability, and incident response.

For real aircraft, review all plans with qualified operators and applicable aviation
regulations. Treat generated flight-control code as untested until it has been validated
in simulation and through an appropriate safety process.
