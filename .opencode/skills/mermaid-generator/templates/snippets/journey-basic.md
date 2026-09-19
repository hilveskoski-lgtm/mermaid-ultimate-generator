---
trigger: "journey"
description: "Basic User Journey Template"
---
```mermaid
journey
    title User Journey
    section Discovery
      Visit Site: 4: User
      Browse: 3: User
    section Purchase
      Add to Cart: 5: User
      Checkout: 5: User
      Pay: 4: User
    section Post-Purchase
      Receive: 5: User
      Review: 3: User
```