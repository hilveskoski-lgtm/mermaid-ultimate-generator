# Architecture Beta Templates

## 1. Microservices Architecture
```mermaid
architecture-beta
    group aws(cloud)[AWS]
    group eks(cluster)[EKS Cluster]
    group data(data)[Data Layer]
    group ext(external)[External Services]
    
    service web(frontend)[Web App] in eks
    service api(gateway)[API Gateway] in eks
    service catalog[Catalog Svc] in eks
    service cart[Cart Svc] in eks
    service order[Order Svc] in eks
    service payment[Payment Svc] in eks
    service notification[Notification Svc] in eks
    
    database postgres[(PostgreSQL)] in data
    database redis[(Redis)] in data
    database elastic[(Elasticsearch)] in data
    queue rabbitmq[RabbitMQ] in data
    
    service stripe[Stripe] in ext
    service sendgrid[SendGrid] in ext
    service auth0[Auth0] in ext
    service datadog[Datadog] in ext
    
    web:L -- R:api
    api:B -- T:catalog
    api:B -- T:cart
    api:B -- T:order
    api:B -- T:payment
    order:R -- L:rabbitmq
    notification:T -- B:rabbitmq
    catalog:B -- T:elastic
    cart:B -- T:redis
    order:B -- T:postgres
    payment:B -- T:postgres
    payment:R -- L:stripe
    notification:R -- L:sendgrid
    api:L -- R:auth0
    api:R -- L:datadog
```

## 2. Serverless Architecture
```mermaid
architecture-beta
    group aws(cloud)[AWS]
    group compute(compute)[Compute]
    group data(data)[Data]
    group integration(integration)[Integration]
    
    service api_gw[API Gateway] in compute
    service lambda_auth[Auth Lambda] in compute
    service lambda_api[API Lambdas] in compute
    service lambda_worker[Worker Lambdas] in compute
    
    database dynamodb[(DynamoDB)] in data
    database s3[(S3)] in data
    
    queue sqs[SQS] in integration
    queue sns[SNS] in integration
    queue eventbridge[EventBridge] in integration
    
    service cognito[Cognito] in aws
    service cloudfront[CloudFront] in aws
    
    cloudfront:B -- T:api_gw
    api_gw:B -- T:lambda_auth
    api_gw:B -- T:lambda_api
    lambda_api:R -- L:dynamodb
    lambda_api:B -- T:sqs
    lambda_worker:T -- B:sqs
    lambda_worker:R -- L:dynamodb
    lambda_worker:B -- T:s3
    lambda_api:R -- L:sns
    eventbridge:L -- R:lambda_worker
    api_gw:L -- R:cognito
```

## 3. Hybrid Cloud
```mermaid
architecture-beta
    group onprem(onprem)[On-Premises]
    group azure(cloud)[Azure]
    group gcp(cloud)[GCP]
    
    service legacy[Legacy App] in onprem
    service vpn[VPN Gateway] in onprem
    
    service aks[AKS Cluster] in azure
    service api_mgmt[API Management] in azure
    service sql[Azure SQL] in azure
    service redis[Azure Redis] in azure
    
    service gke[GKE Cluster] in gcp
    service cloud_run[Cloud Run] in gcp
    service firestore[(Firestore)] in gcp
    service pubsub[Pub/Sub] in gcp
    
    service datadog[Datadog] in azure
    
    legacy:R -- L:vpn
    vpn:R -- L:api_mgmt
    api_mgmt:B -- T:aks
    aks:B -- T:sql
    aks:R -- L:redis
    aks:R -- L:pubsub
    gke:B -- T:firestore
    gke:R -- L:pubsub
    cloud_run:T -- B:pubsub
    aks:R -- L:datadog
    gke:R -- L:datadog
```

## 4. Event-Driven Architecture
```mermaid
architecture-beta
    group platform(platform)[Platform]
    group services(services)[Services]
    group messaging(messaging)[Event Bus]
    
    service producer1[Order Service] in services
    service producer2[Payment Service] in services
    service producer3[Inventory Service] in services
    service consumer1[Notification Svc] in services
    service consumer2[Analytics Svc] in services
    service consumer3[Shipping Svc] in services
    service consumer4[Audit Svc] in services
    
    queue kafka[Kafka] in messaging
    queue schema[Schema Registry] in messaging
    
    database pg[(PostgreSQL)] in platform
    database redis[(Redis)] in platform
    
    producer1:R -- L:kafka
    producer2:R -- L:kafka
    producer3:R -- L:kafka
    kafka:R -- L:consumer1
    kafka:R -- L:consumer2
    kafka:R -- L:consumer3
    kafka:R -- L:consumer4
    producer1:B -- T:pg
    producer2:B -- T:pg
    producer3:B -- T:pg
    consumer2:B -- T:redis
    kafka:T -- B:schema
```

## 5. Zero Trust Network
```mermaid
architecture-beta
    group internet(internet)[Internet]
    group dmz(dmz)[DMZ]
    group app(app)[Application Zone]
    group data(data)[Data Zone]
    group mgmt(mgmt)[Management]
    
    service waf[WAF] in dmz
    service lb[Load Balancer] in dmz
    service api[API Gateway] in app
    service svc1[Service A] in app
    service svc2[Service B] in app
    service svc3[Service C] in app
    database pg[(PostgreSQL)] in data
    database redis[(Redis)] in data
    database vault[Vault] in data
    service iam[Identity] in mgmt
    service policy[Policy Engine] in mgmt
    service audit[Audit Log] in mgmt
    
    internet:B -- T:waf
    waf:B -- T:lb
    lb:B -- T:api
    api:B -- T:svc1
    api:B -- T:svc2
    api:B -- T:svc3
    svc1:B -- T:pg
    svc2:B -- T:redis
    svc3:B -- T:vault
    api:L -- R:iam
    svc1:L -- R:policy
    svc2:L -- R:policy
    svc3:L -- R:policy
    api:B -- T:audit
    svc1:B -- T:audit
    svc2:B -- T:audit
    svc3:B -- T:audit
```