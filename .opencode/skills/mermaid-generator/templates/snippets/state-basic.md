---
trigger: "state"
description: "Basic State Diagram Template"
---
```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing: start()
    Processing --> Done: complete()
    Processing --> Error: fail()
    Done --> [*]
    Error --> [*]
```