# Object Diagram Templates

## 1. Runtime Object Snapshot (E-commerce)
```mermaid
objectDiagram
    object customer1 {
        id: "CUST-001"
        email: "john@example.com"
        name: "John Doe"
        status: "ACTIVE"
    }
    object cart1 {
        id: "CART-001"
        customerId: "CUST-001"
        items: 3
        total: 149.97
        currency: "EUR"
    }
    object item1 {
        id: "ITEM-001"
        cartId: "CART-001"
        productId: "PROD-100"
        quantity: 1
        unitPrice: 79.99
    }
    object item2 {
        id: "ITEM-002"
        cartId: "CART-001"
        productId: "PROD-101"
        quantity: 2
        unitPrice: 34.99
    }
    object product100 {
        id: "PROD-100"
        name: "Wireless Headphones"
        price: 79.99
        stock: 45
    }
    object product101 {
        id: "PROD-101"
        name: "Phone Case"
        price: 34.99
        stock: 120
    }
    
    customer1 -- cart1 : owns
    cart1 -- item1 : contains
    cart1 -- item2 : contains
    item1 -- product100 : references
    item2 -- product101 : references
```

## 2. Order Processing State
```mermaid
objectDiagram
    object order123 {
        orderId: "ORD-123"
        customerId: "CUST-001"
        status: "CONFIRMED"
        total: 149.97
        createdAt: "2024-01-15T10:30:00Z"
    }
    object payment456 {
        paymentId: "PAY-456"
        orderId: "ORD-123"
        amount: 149.97
        method: "CREDIT_CARD"
        status: "CAPTURED"
        transactionId: "txn_abc123"
    }
    object shipment789 {
        shipmentId: "SHP-789"
        orderId: "ORD-123"
        carrier: "DHL"
        trackingNumber: "DHL123456789"
        status: "IN_TRANSIT"
        estimatedDelivery: "2024-01-18"
    }
    object address1 {
        addressId: "ADDR-1"
        street: "Main Str. 123"
        city: "Berlin"
        postalCode: "10115"
        country: "DE"
    }
    
    order123 -- payment456 : paidBy
    order123 -- shipment789 : shippedVia
    order123 -- address1 : shippingTo
```

## 3. Class Instance with Links
```mermaid
objectDiagram
    class User {
        +id: Long
        +email: String
        +name: String
        +roles: Set<Role>
    }
    class Role {
        +id: Long
        +name: String
        +permissions: Set<Permission>
    }
    class Permission {
        +id: Long
        +resource: String
        +action: String
    }
    
    object user1 : User {
        id: 1
        email: "admin@company.com"
        name: "Admin User"
    }
    object role_admin : Role {
        id: 1
        name: "ADMIN"
    }
    object role_user : Role {
        id: 2
        name: "USER"
    }
    object perm_read : Permission {
        id: 1
        resource: "*"
        action: "READ"
    }
    object perm_write : Permission {
        id: 2
        resource: "*"
        action: "WRITE"
    }
    object perm_delete : Permission {
        id: 3
        resource: "*"
        action: "DELETE"
    }
    
    user1 -- role_admin : hasRole
    user1 -- role_user : hasRole
    role_admin -- perm_read : hasPermission
    role_admin -- perm_write : hasPermission
    role_admin -- perm_delete : hasPermission
    role_user -- perm_read : hasPermission
```

## 4. Composite Pattern (File System)
```mermaid
objectDiagram
    object root {
        name: "/"
        type: "Directory"
        size: 4096
    }
    object home {
        name: "home"
        type: "Directory"
        size: 4096
    }
    object user {
        name: "john"
        type: "Directory"
        size: 4096
    }
    object documents {
        name: "Documents"
        type: "Directory"
        size: 4096
    }
    object report_pdf {
        name: "report.pdf"
        type: "File"
        size: 2048576
    }
    object notes_txt {
        name: "notes.txt"
        type: "File"
        size: 1024
    }
    object pictures {
        name: "Pictures"
        type: "Directory"
        size: 4096
    }
    object photo_jpg {
        name: "vacation.jpg"
        type: "File"
        size: 5242880
    }
    
    root -- home : contains
    home -- user : contains
    user -- documents : contains
    user -- pictures : contains
    documents -- report_pdf : contains
    documents -- notes_txt : contains
    pictures -- photo_jpg : contains
```

## 5. Observer Pattern Instance
```mermaid
objectDiagram
    class Subject {
        +observers: List<Observer>
        +attach(Observer)
        +detach(Observer)
        +notify()
    }
    class Observer {
        +update(Subject)
    }
    class ConcreteSubject {
        +state: String
        +getState()
        +setState(String)
    }
    class ConcreteObserverA {
        +observerState: String
    }
    class ConcreteObserverB {
        +observerState: String
    }
    
    object subject1 : ConcreteSubject {
        state: "ACTIVE"
    }
    object observerA1 : ConcreteObserverA {
        observerState: "ACTIVE"
    }
    object observerB1 : ConcreteObserverB {
        observerState: "ACTIVE"
    }
    object observerA2 : ConcreteObserverA {
        observerState: "ACTIVE"
    }
    
    subject1 -- observerA1 : observes
    subject1 -- observerB1 : observes
    subject1 -- observerA2 : observes
```

## 6. Microservice Runtime Topology
```mermaid
objectDiagram
    object api_gateway_1 {
        instance: "api-gateway-1"
        version: "v2.1.0"
        status: "HEALTHY"
        requests_per_sec: 1250
    }
    object api_gateway_2 {
        instance: "api-gateway-2"
        version: "v2.1.0"
        status: "HEALTHY"
        requests_per_sec: 1180
    }
    object catalog_svc_1 {
        instance: "catalog-svc-1"
        version: "v1.5.0"
        status: "HEALTHY"
        cpu: "45%"
        memory: "512Mi"
    }
    object catalog_svc_2 {
        instance: "catalog-svc-2"
        version: "v1.5.0"
        status: "HEALTHY"
        cpu: "38%"
        memory: "480Mi"
    }
    object cart_svc_1 {
        instance: "cart-svc-1"
        version: "v1.2.0"
        status: "DEGRADED"
        cpu: "85%"
        memory: "890Mi"
    }
    object redis_primary {
        instance: "redis-primary"
        role: "PRIMARY"
        memory: "2.1Gi"
        connected_clients: 245
    }
    object redis_replica {
        instance: "redis-replica"
        role: "REPLICA"
        memory: "2.1Gi"
        lag: "0s"
    }
    
    api_gateway_1 -- catalog_svc_1 : routes_to
    api_gateway_1 -- catalog_svc_2 : routes_to
    api_gateway_2 -- catalog_svc_1 : routes_to
    api_gateway_2 -- catalog_svc_2 : routes_to
    api_gateway_1 -- cart_svc_1 : routes_to
    cart_svc_1 -- redis_primary : connects
    redis_primary -- redis_replica : replicates
```