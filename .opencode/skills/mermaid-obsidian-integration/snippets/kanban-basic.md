---
trigger: "kanban"
description: "Basic Kanban Board Template"
---
```mermaid
kanban
    title Team Board
    column Backlog [5]
    column Ready [3]
    column In Progress [3]
    column Review [2]
    column Done [10]
    
    task[Backlog] Research
    task[Backlog] Design
    task[Ready] Task 1
    task[Ready] Task 2
    task[In Progress] Task 3
    task[Review] Task 4
    task[Done] Task 5
```