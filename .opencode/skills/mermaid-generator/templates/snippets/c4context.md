---
trigger: "c4context"
description: "C4 Context Diagram Template"
---
```mermaid
C4Context
    title System Context
    
    Person(user, "User", "Uses the system")
    System(system, "My System", "Does something useful")
    System_Ext(ext, "External API", "Provides data")
    
    Rel(user, system, "Uses")
    Rel(system, ext, "Gets data from")
```