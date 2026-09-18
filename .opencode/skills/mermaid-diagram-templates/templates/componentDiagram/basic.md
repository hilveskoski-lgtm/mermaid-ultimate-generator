# Component Diagram Templates

## 1. Microservices Component View
```mermaid
componentDiagram
    package "Frontend" {
        [Web App]
        [Admin Portal]
        [Mobile App]
    }
    
    package "API Gateway" {
        [Kong Gateway]
        [Auth Plugin]
        [Rate Limit Plugin]
    }
    
    package "Core Services" {
        [Catalog Service]
        [Cart Service]
        [Order Service]
        [Payment Service]
        [User Service]
        [Notification Service]
    }
    
    package "Infrastructure" {
        [PostgreSQL]
        [Redis]
        [Elasticsearch]
        [RabbitMQ]
    }
    
    package "External" {
        [Stripe]
        [SendGrid]
        [Auth0]
        [Datadog]
    }
    
    [Web App] --> [Kong Gateway]
    [Admin Portal] --> [Kong Gateway]
    [Mobile App] --> [Kong Gateway]
    
    [Kong Gateway] --> [Catalog Service]
    [Kong Gateway] --> [Cart Service]
    [Kong Gateway] --> [Order Service]
    [Kong Gateway] --> [Payment Service]
    [Kong Gateway] --> [User Service]
    
    [Catalog Service] --> [PostgreSQL]
    [Catalog Service] --> [Elasticsearch]
    [Cart Service] --> [Redis]
    [Order Service] --> [PostgreSQL]
    [Order Service] --> [RabbitMQ]
    [Payment Service] --> [PostgreSQL]
    [Payment Service] --> [Stripe]
    [User Service] --> [PostgreSQL]
    [User Service] --> [Auth0]
    [Notification Service] --> [RabbitMQ]
    [Notification Service] --> [SendGrid]
    
    [Kong Gateway] --> [Datadog]
    [Catalog Service] --> [Datadog]
    [Order Service] --> [Datadog]
```

## 2. Layered Architecture (Clean Architecture)
```mermaid
componentDiagram
    package "Presentation" {
        [REST Controllers]
        [GraphQL Resolvers]
        [gRPC Handlers]
        [WebSocket Handlers]
    }
    
    package "Application" {
        [User Service]
        [Order Service]
        [Payment Service]
        [Catalog Service]
        [Event Handlers]
        [Saga Orchestrators]
    }
    
    package "Domain" {
        [User Entity]
        [Order Entity]
        [Product Entity]
        [Value Objects]
        [Domain Events]
        [Domain Services]
        [Repository Interfaces]
    }
    
    package "Infrastructure" {
        [JPA Repositories]
        [Redis Repositories]
        [Elasticsearch Repositories]
        [Message Publishers]
        [External API Clients]
        [Security Config]
    }
    
    [REST Controllers] --> [User Service]
    [REST Controllers] --> [Order Service]
    [GraphQL Resolvers] --> [User Service]
    [gRPC Handlers] --> [Order Service]
    
    [User Service] --> [User Entity]
    [User Service] --> [User Repository]
    [Order Service] --> [Order Entity]
    [Order Service] --> [Order Repository]
    [Order Service] --> [Payment Service]
    [Payment Service] --> [External API Clients]
    
    [JPA Repositories] ..> [Repository Interfaces]
    [Redis Repositories] ..> [Repository Interfaces]
    [Message Publishers] --> [Domain Events]
```

## 3. Plugin Architecture
```mermaid
componentDiagram
    package "Core Application" {
        [Kernel]
        [Plugin Manager]
        [Event Bus]
        [Service Registry]
        [Configuration]
    }
    
    package "Plugins" {
        [Auth Plugin]
        [Logging Plugin]
        [Metrics Plugin]
        [Cache Plugin]
        [Auth0 Adapter]
        [OAuth2 Adapter]
        [SAML Adapter]
        [File Logger]
        [Console Logger]
        [Syslog Logger]
        [Prometheus Exporter]
        [Datadog Exporter]
        [Redis Cache]
        [Memory Cache]
    }
    
    [Kernel] --> [Plugin Manager]
    [Plugin Manager] --> [Auth Plugin]
    [Plugin Manager] --> [Logging Plugin]
    [Plugin Manager] --> [Metrics Plugin]
    [Plugin Manager] --> [Cache Plugin]
    
    [Auth Plugin] --> [Auth0 Adapter]
    [Auth Plugin] --> [OAuth2 Adapter]
    [Auth Plugin] --> [SAML Adapter]
    [Logging Plugin] --> [File Logger]
    [Logging Plugin] --> [Console Logger]
    [Logging Plugin] --> [Syslog Logger]
    [Metrics Plugin] --> [Prometheus Exporter]
    [Metrics Plugin] --> [Datadog Exporter]
    [Cache Plugin] --> [Redis Cache]
    [Cache Plugin] --> [Memory Cache]
    
    [Plugin Manager] --> [Event Bus]
    [Plugin Manager] --> [Service Registry]
    [Auth Plugin] --> [Event Bus]
    [Logging Plugin] --> [Event Bus]
    [Metrics Plugin] --> [Event Bus]
```

## 4. Component with Ports & Interfaces
```mermaid
componentDiagram
    component "Order Processing" {
        port "inbound" as InPort
        port "outbound" as OutPort
        
        [Order Controller] -- InPort
        [Order Service] -- InPort
        [Order Service] -- OutPort
        [Order Repository] -- OutPort
        [Event Publisher] -- OutPort
    }
    
    component "Payment Gateway" {
        port "payment" as PayPort
        [Payment Client] -- PayPort
    }
    
    component "Inventory" {
        port "inventory" as InvPort
        [Inventory Client] -- InvPort
    }
    
    component "Messaging" {
        port "events" as EventPort
        [Kafka Producer] -- EventPort
    }
    
    [Order Service] --> [Payment Client] : PayPort
    [Order Service] --> [Inventory Client] : InvPort
    [Event Publisher] --> [Kafka Producer] : EventPort
```

## 5. Deployment Components
```mermaid
componentDiagram
    node "Kubernetes Cluster" {
        component "Ingress Nginx" {
            [Ingress Controller]
            [TLS Termination]
        }
        
        component "Monitoring" {
            [Prometheus]
            [Grafana]
            [Alertmanager]
        }
        
        component "Logging" {
            [Fluentd]
            [Elasticsearch]
            [Kibana]
        }
        
        component "Service Mesh" {
            [Istio Pilot]
            [Istio Citadel]
            [Istio Galley]
        }
    }
    
    node "Applications" {
        component "Order Service" {
            [Order Pod 1]
            [Order Pod 2]
            [Order Pod 3]
            [Order Service]
            [Order HPA]
        }
        
        component "Payment Service" {
            [Payment Pod 1]
            [Payment Pod 2]
            [Payment Service]
            [Payment HPA]
        }
    }
    
    [Ingress Controller] --> [Order Service]
    [Ingress Controller] --> [Payment Service]
    [Istio Pilot] --> [Order Service]
    [Istio Pilot] --> [Payment Service]
    [Prometheus] --> [Order Service]
    [Prometheus] --> [Payment Service]
    [Fluentd] --> [Order Service]
    [Fluentd] --> [Payment Service]
```