# Requirement Diagram Templates

## 1. Basic Requirements Hierarchy
```mermaid
requirementDiagram
    requirement "REQ-001" {
        id: "REQ-001"
        text: "The system shall allow users to authenticate"
        type: functional
        priority: high
        risk: high
    }
    requirement "REQ-002" {
        id: "REQ-002"
        text: "Authentication shall use OAuth 2.0"
        type: functional
        priority: high
        risk: medium
    }
    requirement "REQ-003" {
        id: "REQ-003"
        text: "Session timeout after 30 minutes of inactivity"
        type: functional
        priority: medium
        risk: low
    }
    requirement "REQ-004" {
        id: "REQ-004"
        text: "System shall respond within 200ms for 95th percentile"
        type: performance
        priority: high
        risk: medium
    }
    requirement "REQ-005" {
        id: "REQ-005"
        text: "All data shall be encrypted at rest and in transit"
        type: security
        priority: critical
        risk: high
    }
    
    element "Auth Service" {
        type: component
    }
    element "API Gateway" {
        type: component
    }
    element "Database" {
        type: component
    }
    
    "Auth Service" - satisfies -> "REQ-001"
    "Auth Service" - satisfies -> "REQ-002"
    "Auth Service" - satisfies -> "REQ-003"
    "API Gateway" - satisfies -> "REQ-004"
    "Database" - satisfies -> "REQ-005"
```

## 2. With Traceability (V-Model)
```mermaid
requirementDiagram
    requirement "SYS-REQ-001" {
        id: "SYS-REQ-001"
        text: "Vehicle shall accelerate 0-100 km/h in under 5 seconds"
        type: performance
        priority: high
    }
    requirement "SYS-REQ-002" {
        id: "SYS-REQ-002"
        text: "Vehicle shall have range of at least 500 km"
        type: performance
        priority: high
    }
    requirement "SW-REQ-001" {
        id: "SW-REQ-001"
        text: "Motor controller shall deliver 400kW peak power"
        type: functional
        priority: high
    }
    requirement "SW-REQ-002" {
        id: "SW-REQ-002"
        text: "BMS shall balance cells within 10mV"
        type: functional
        priority: high
    }
    requirement "HW-REQ-001" {
        id: "HW-REQ-001"
        text: "Battery pack capacity >= 100 kWh"
        type: physical
        priority: high
    }
    requirement "HW-REQ-002" {
        id: "HW-REQ-002"
        text: "Motor torque >= 800 Nm"
        type: physical
        priority: high
    }
    
    element "Motor Control SW" {
        type: software
    }
    element "BMS SW" {
        type: software
    }
    element "Battery Pack" {
        type: hardware
    }
    element "Electric Motor" {
        type: hardware
    }
    
    "SYS-REQ-001" - derives -> "SW-REQ-001"
    "SYS-REQ-001" - derives -> "HW-REQ-002"
    "SYS-REQ-002" - derives -> "SW-REQ-002"
    "SYS-REQ-002" - derives -> "HW-REQ-001"
    
    "Motor Control SW" - satisfies -> "SW-REQ-001"
    "BMS SW" - satisfies -> "SW-REQ-002"
    "Battery Pack" - satisfies -> "HW-REQ-001"
    "Electric Motor" - satisfies -> "HW-REQ-002"
    
    "SW-REQ-001" - verifies -> "SYS-REQ-001"
    "HW-REQ-002" - verifies -> "SYS-REQ-001"
    "SW-REQ-002" - verifies -> "SYS-REQ-002"
    "HW-REQ-001" - verifies -> "SYS-REQ-002"
```

## 3. Safety Requirements (ISO 26262)
```mermaid
requirementDiagram
    requirement "SR-001" {
        id: "SR-001"
        text: "ASIL-D: Braking system shall activate within 100ms of pedal press"
        asil: D
        type: safety
    }
    requirement "SR-002" {
        id: "SR-002"
        text: "ASIL-C: Steering torque sensor shall detect failure within 50ms"
        asil: C
        type: safety
    }
    requirement "SR-003" {
        id: "SR-003"
        text: "ASIL-B: Infotainment shall not interfere with CAN bus"
        asil: B
        type: safety
    }
    requirement "SR-004" {
        id: "SR-004"
        text: "QM: UI theme shall be customizable"
        asil: QM
        type: functional
    }
    
    element "Brake ECU" {
        type: component
        asil: D
    }
    element "Steering ECU" {
        type: component
        asil: C
    }
    element "Gateway ECU" {
        type: component
        asil: B
    }
    element "Infotainment ECU" {
        type: component
        asil: QM
    }
    
    "Brake ECU" - satisfies -> "SR-001"
    "Steering ECU" - satisfies -> "SR-002"
    "Gateway ECU" - satisfies -> "SR-003"
    "Infotainment ECU" - satisfies -> "SR-004"
```

## 4. Agile User Stories as Requirements
```mermaid
requirementDiagram
    requirement "US-001" {
        id: "US-001"
        text: "As a customer, I want to save my cart so I can continue later"
        type: user_story
        priority: high
        story_points: 5
    }
    requirement "US-002" {
        id: "US-002"
        text: "As a customer, I want guest checkout so I don't need an account"
        type: user_story
        priority: high
        story_points: 8
    }
    requirement "US-003" {
        id: "US-003"
        text: "As an admin, I want to view order analytics"
        type: user_story
        priority: medium
        story_points: 13
    }
    
    element "Cart Service" {
        type: microservice
    }
    element "Checkout Service" {
        type: microservice
    }
    element "Analytics Service" {
        type: microservice
    }
    element "PostgreSQL" {
        type: database
    }
    element "Redis" {
        type: cache
    }
    
    "Cart Service" - satisfies -> "US-001"
    "Checkout Service" - satisfies -> "US-002"
    "Analytics Service" - satisfies -> "US-003"
    
    "Cart Service" - contains -> "Redis"
    "Cart Service" - contains -> "PostgreSQL"
    "Checkout Service" - contains -> "PostgreSQL"
    "Analytics Service" - contains -> "PostgreSQL"
```

## 5. With Test Cases
```mermaid
requirementDiagram
    requirement "REQ-LOGIN-001" {
        id: "REQ-LOGIN-001"
        text: "User can login with valid credentials"
        priority: high
    }
    requirement "REQ-LOGIN-002" {
        id: "REQ-LOGIN-002"
        text: "User cannot login with invalid password"
        priority: high
    }
    requirement "REQ-LOGIN-003" {
        id: "REQ-LOGIN-003"
        text: "Account locks after 5 failed attempts"
        priority: medium
    }
    
    element "LoginController" {
        type: class
    }
    element "AuthService" {
        type: class
    }
    element "UserRepository" {
        type: class
    }
    
    "LoginController" - satisfies -> "REQ-LOGIN-001"
    "AuthService" - satisfies -> "REQ-LOGIN-001"
    "AuthService" - satisfies -> "REQ-LOGIN-002"
    "AuthService" - satisfies -> "REQ-LOGIN-003"
    "UserRepository" - satisfies -> "REQ-LOGIN-003"
    
    element "TC-LOGIN-001" {
        type: test_case
        text: "Valid credentials return JWT token"
    }
    element "TC-LOGIN-002" {
        type: test_case
        text: "Invalid password returns 401"
    }
    element "TC-LOGIN-003" {
        type: test_case
        text: "5 failures lock account for 15 min"
    }
    
    "TC-LOGIN-001" - verifies -> "REQ-LOGIN-001"
    "TC-LOGIN-002" - verifies -> "REQ-LOGIN-002"
    "TC-LOGIN-003" - verifies -> "REQ-LOGIN-003"
```