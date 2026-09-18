# Sequence Diagram Templates

## 1. Basic Request-Response
```mermaid
sequenceDiagram
    participant Client
    participant Server
    Client->>Server: GET /api/users
    activate Server
    Server-->>Client: 200 OK [{id: 1, name: "John"}]
    deactivate Server
```

## 2. With Fragments (alt, opt, loop)
```mermaid
sequenceDiagram
    participant User
    participant Auth
    participant DB
    User->>Auth: POST /login {email, password}
    activate Auth
    Auth->>DB: SELECT * FROM users WHERE email=?
    activate DB
    DB-->>Auth: User record / null
    deactivate DB
    alt credentials valid
        Auth->>Auth: Generate JWT
        Auth-->>User: 200 OK {token}
    else invalid credentials
        Auth-->>User: 401 Unauthorized
    end
    deactivate Auth
```

## 3. Async Communication
```mermaid
sequenceDiagram
    participant Client
    participant Queue
    participant Worker
    participant DB
    Client->>Queue: Publish job (async)
    Note right of Queue: Fire-and-forget
    Worker->>Queue: Consume job
    activate Worker
    Worker->>DB: Process & save
    activate DB
    DB-->>Worker: Result
    deactivate DB
    Worker->>Queue: Acknowledge
    deactivate Worker
```

## 4. With Lifeline Activation/Deactivation
```mermaid
sequenceDiagram
    autonumber
    participant Browser
    participant CDN
    participant App
    participant Cache
    participant DB
    Browser->>CDN: GET /app.js
    CDN-->>Browser: Cached JS
    Browser->>App: GET /api/data
    activate App
    App->>Cache: GET cache:data
    activate Cache
    alt cache hit
        Cache-->>App: Cached data
    else cache miss
        Cache-->>App: Miss
        App->>DB: SELECT * FROM data
        activate DB
        DB-->>App: Fresh data
        deactivate DB
        App->>Cache: SET cache:data
        Cache-->>App: OK
    end
    deactivate Cache
    App-->>Browser: JSON data
    deactivate App
```

## 5. Multi-Participant with Parallel
```mermaid
sequenceDiagram
    participant User
    participant Gateway
    participant AuthService
    participant PaymentService
    participant NotificationService
    User->>Gateway: POST /checkout
    activate Gateway
    Gateway->>AuthService: Validate token
    activate AuthService
    AuthService-->>Gateway: User ID
    deactivate AuthService
    par Parallel processing
        Gateway->>PaymentService: Process payment
        activate PaymentService
        PaymentService-->>Gateway: Transaction ID
        deactivate PaymentService
    and
        Gateway->>NotificationService: Send confirmation
        activate NotificationService
        NotificationService-->>Gateway: Sent
        deactivate NotificationService
    end
    Gateway-->>User: 200 OK {orderId}
    deactivate Gateway
```