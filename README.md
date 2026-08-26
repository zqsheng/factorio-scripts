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
