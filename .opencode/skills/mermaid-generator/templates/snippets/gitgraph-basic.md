---
trigger: "git"
description: "Basic Git Graph Template"
---
```mermaid
gitGraph
    commit id: "Initial"
    branch develop
    checkout develop
    commit id: "Feature A"
    commit id: "Feature B"
    checkout main
    merge develop id: "Merge develop"
    tag: "v1.0.0"
```