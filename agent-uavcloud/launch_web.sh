#!/bin/zsh
set -eu

ROOT_DIR=${0:A:h:h}

if [[ -z "${DEEPSEEK_API_KEY:-}" ]]; then
    printf '%s\n' "DEEPSEEK_API_KEY is not set." >&2
    printf '%s\n' 'Run: export DEEPSEEK_API_KEY="your-deepseek-api-key"' >&2
    exit 1
fi

if [[ "${ENABLE_TAVILY_SEARCH:-0}" == "1" && -z "${TAVILY_API_KEY:-}" ]]; then
    printf '%s\n' 'TAVILY_API_KEY is required when ENABLE_TAVILY_SEARCH=1.' >&2
    exit 1
fi

cd "$ROOT_DIR/agent-uavcloud"
exec "$ROOT_DIR/.venv/bin/adk" web . --port "${ADK_PORT:-8001}" "$@"
