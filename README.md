# `factorio-scripts`

- lambda-calculus
  - `mit-scheme`
  - `chibi-scheme`
- `fcpu`
- app
  - `threejs`

## browser bookmarks

- <https://hellogithub.com/>
- `codewars`
- `cpprefereneces`
- <https://plato.stanford.edu/entries/lambda-calculus/>

## `flowable6`

### `bpmn`, Business Process Model and Notation

- Process-driven

- main elements
  - `startEvent`, where the process start
  - `serviceTask`, java/system Task
  - `userTask`, Human approval task
  - `receiveTask`, wait for external callback
  - `exclusiveGateway`, if/else decision
  - `parallelGateway`, run branches in parallel
  - `sequenceFlow`, connection nodes
  - `endEvent`, process ends
  - `boundaryEvent`, timeout/error handler attached to task
  -

### `CMMN`, Case Management Model and Notation

- case-driven
- scenario-driven

- core elements
- case, the whole case instance
- stage, a group of related tasks
- `humanTask`, task for a person
- `processTask`, start a `BPMN` process
- `caseTask` start another `CMMN` case
- milestone important state reached
- sentry, condition to activate/complete something
- `planItem`, runtime instance of a task/stage/milestone
- `eventListener`, wait for timer/user/event

### `DMN`, Decision Model and Notation

- core elements
  - decision, a business decision to be make
  - input data, data needed by the decision
  - business knowledge model, reusable decision logic/function
  - knowledge source, authority/source of rules
  - decision service, a callable group of decisions
  - decision table, table-base rules definition
  - `DRD`, decision requirements diagram
  - FEEL, expression language used by `DMN`

### Lane and Pool

### `bpmn-visualization`

## Observability

- The Three Pillars of Observability
  - logs
  - metrics
  - traces

### `OpenTelemetry`

### Micrometer

## Object Storage

### AWE `S3`

- bucket, top-level container
- object, file plus metadata
- key, unique object name/path inside the bucket

## LangChain demo

The `demo-langchain/langchain-demo.py` script sends a question to an OpenAI chat model through
LangChain. Install the provider integration and configure an API key:

```zsh
/Users/zhangqishang/factorio-scripts/.venv/bin/python -m pip install -U langchain-openai
export OPENAI_API_KEY="your-openai-api-key"
/Users/zhangqishang/factorio-scripts/.venv/bin/python demo-langchain/langchain-demo.py "What is a LangChain runnable?"
```

## LangGraph demo

The `demo-langgraph/langgraph-demo.py` script runs a question through a minimal
LangGraph state graph using DeepSeek V4 Flash by default:

```zsh
export DEEPSEEK_API_KEY="your-deepseek-api-key"
/Users/zhangqishang/factorio-scripts/.venv/bin/python demo-langgraph/langgraph-demo.py "What is a graph state?"
```

Override the model with `LANGGRAPH_MODEL` or `--model` when needed.
