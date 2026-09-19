# Package Diagram Templates

## 1. Java Package Structure (Layered)
```mermaid
packageDiagram
    package "com.company.app" {
        package "presentation" {
            package "rest" {
                [UserController]
                [OrderController]
                [ProductController]
            }
            package "graphql" {
                [UserResolver]
                [OrderResolver]
            }
            package "grpc" {
                [UserGrpcService]
                [OrderGrpcService]
            }
        }
        
        package "application" {
            package "service" {
                [UserService]
                [OrderService]
                [PaymentService]
                [CatalogService]
            }
            package "event" {
                [OrderEventHandler]
                [UserEventHandler]
                [EventPublisher]
            }
            package "saga" {
                [OrderSaga]
                [PaymentSaga]
            }
        }
        
        package "domain" {
            package "model" {
                [User]
                [Order]
                [Product]
                [ValueObjects]
            }
            package "event" {
                [DomainEvent]
                [OrderCreatedEvent]
                [OrderShippedEvent]
            }
            package "service" {
                [PricingService]
                [InventoryService]
            }
            package "repository" {
                [UserRepository]
                [OrderRepository]
                [ProductRepository]
            }
        }
        
        package "infrastructure" {
            package "persistence" {
                [JpaUserRepository]
                [JpaOrderRepository]
                [JpaProductRepository]
                [RedisCartRepository]
                [ElasticsearchProductRepository]
            }
            package "messaging" {
                [KafkaEventPublisher]
                [RabbitMQConsumer]
            }
            package "external" {
                [StripeClient]
                [SendGridClient]
                [Auth0Client]
            }
            package "config" {
                [SecurityConfig]
                [DatabaseConfig]
                [CacheConfig]
            }
        }
    }
    
    package "com.company.app.presentation.rest" {
        [UserController] ..> [UserService]
        [OrderController] ..> [OrderService]
    }
    
    package "com.company.app.application.service" {
        [UserService] ..> [UserRepository]
        [OrderService] ..> [OrderRepository]
        [OrderService] ..> [PaymentService]
        [OrderService] ..> [EventPublisher]
    }
    
    package "com.company.app.infrastructure.persistence" {
        [JpaUserRepository] ..|> [UserRepository]
        [JpaOrderRepository] ..|> [OrderRepository]
        [RedisCartRepository] ..|> [CartRepository]
    }
```

## 2. Go Module Structure
```mermaid
packageDiagram
    package "github.com/company/platform" {
        package "cmd" {
            [api-server]
            [worker]
            [migrate]
            [cli]
        }
        
        package "internal" {
            package "app" {
                [application.go]
                [config.go]
            }
            package "module" {
                package "user" {
                    [handler.go]
                    [service.go]
                    [repository.go]
                    [model.go]
                }
                package "order" {
                    [handler.go]
                    [service.go]
                    [repository.go]
                    [model.go]
                    [saga.go]
                }
                package "catalog" {
                    [handler.go]
                    [service.go]
                    [repository.go]
                    [model.go]
                }
                package "payment" {
                    [handler.go]
                    [service.go]
                    [repository.go]
                    [model.go]
                }
            }
            package "platform" {
                package "database" {
                    [postgres.go]
                    [redis.go]
                    [migrations]
                }
                package "messaging" {
                    [kafka.go]
                    [rabbitmq.go]
                    [publisher.go]
                }
                package "http" {
                    [middleware.go]
                    [router.go]
                    [response.go]
                }
                package "observability" {
                    [metrics.go]
                    [tracing.go]
                    [logging.go]
                }
            }
        }
        
        package "pkg" {
            package "errors" {
                [errors.go]
            }
            package "validation" {
                [validator.go]
            }
            package "pagination" {
                [paginator.go]
            }
        }
    }
    
    [api-server] ..> [internal/app]
    [worker] ..> [internal/app]
    [internal/module/user/service] ..> [internal/module/user/repository]
    [internal/module/order/service] ..> [internal/module/order/repository]
    [internal/module/order/service] ..> [internal/module/payment/service]
    [internal/module/order/saga] ..> [internal/platform/messaging]
```

## 3. Python Package Structure
```mermaid
packageDiagram
    package "ecommerce" {
        package "api" {
            [__init__.py]
            [routes.py]
            [schemas.py]
            [dependencies.py]
            package "v1" {
                [users.py]
                [orders.py]
                [products.py]
                [payments.py]
            }
        }
        
        package "core" {
            [__init__.py]
            [config.py]
            [security.py]
            [database.py]
            [cache.py]
            [events.py]
        }
        
        package "models" {
            [__init__.py]
            [user.py]
            [order.py]
            [product.py]
            [enums.py]
        }
        
        package "services" {
            [__init__.py]
            [user_service.py]
            [order_service.py]
            [payment_service.py]
            [catalog_service.py]
            [notification_service.py]
        }
        
        package "repositories" {
            [__init__.py]
            [user_repo.py]
            [order_repo.py]
            [product_repo.py]
            [base.py]
        }
        
        package "integrations" {
            [__init__.py]
            [stripe.py]
            [sendgrid.py]
            [auth0.py]
        }
        
        package "tasks" {
            [__init__.py]
            [celery_app.py]
            [email_tasks.py]
            [order_tasks.py]
        }
    }
    
    [api.routes] ..> [api.v1.users]
    [api.v1.orders] ..> [services.order_service]
    [services.order_service] ..> [repositories.order_repo]
    [services.order_service] ..> [services.payment_service]
    [services.order_service] ..> [core.events]
    [integrations.stripe] ..> [services.payment_service]
    [tasks.email_tasks] ..> [services.notification_service]
```

## 4. Monorepo with Shared Libraries
```mermaid
packageDiagram
    package "monorepo" {
        package "apps" {
            package "web" {
                [src]
                [package.json]
            }
            package "admin" {
                [src]
                [package.json]
            }
            package "mobile" {
                [src]
                [package.json]
            }
            package "api-gateway" {
                [src]
                [package.json]
            }
        }
        
        package "packages" {
            package "ui-components" {
                [Button]
                [Input]
                [Modal]
                [Table]
                [Form]
            }
            package "design-tokens" {
                [colors]
                [spacing]
                [typography]
                [shadows]
            }
            package "api-client" {
                [userApi]
                [orderApi]
                [productApi]
            }
            package "utils" {
                [date]
                [format]
                [validation]
            }
            package "config" {
                [eslint]
                [typescript]
                [jest]
            }
        }
        
        package "tools" {
            [build]
            [lint]
            [test]
            [deploy]
        }
    }
    
    [apps/web] ..> [packages/ui-components]
    [apps/web] ..> [packages/design-tokens]
    [apps/web] ..> [packages/api-client]
    [apps/admin] ..> [packages/ui-components]
    [apps/admin] ..> [packages/api-client]
    [apps/mobile] ..> [packages/ui-components]
    [apps/api-gateway] ..> [packages/api-client]
```

## 5. Domain-Driven Design (Bounded Contexts)
```mermaid
packageDiagram
    package "E-Commerce Platform" {
        package "Identity & Access" {
            package "domain" {
                [User]
                [Role]
                [Permission]
                [Session]
            }
            package "application" {
                [AuthService]
                [RegistrationService]
                [PasswordService]
            }
            package "infrastructure" {
                [UserRepository]
                [OAuth2Provider]
                [JWTService]
            }
        }
        
        package "Catalog" {
            package "domain" {
                [Product]
                [Category]
                [Attribute]
                [Inventory]
            }
            package "application" {
                [ProductService]
                [CategoryService]
                [SearchService]
            }
            package "infrastructure" {
                [ProductRepository]
                [ElasticsearchIndex]
                [CacheInvalidator]
            }
        }
        
        package "Ordering" {
            package "domain" {
                [Order]
                [OrderItem]
                [ShippingAddress]
                [OrderStatus]
            }
            package "application" {
                [OrderService]
                [CartService]
                [CheckoutService]
            }
            package "infrastructure" {
                [OrderRepository]
                [EventPublisher]
                [SagaOrchestrator]
            }
        }
        
        package "Payment" {
            package "domain" {
                [Payment]
                [Transaction]
                [Refund]
            }
            package "application" {
                [PaymentService]
                [RefundService]
            }
            package "infrastructure" {
                [PaymentRepository]
                [StripeAdapter]
                [WebhookHandler]
            }
        }
        
        package "Notification" {
            package "domain" {
                [Notification]
                [Template]
                [Channel]
            }
            package "application" {
                [NotificationService]
                [TemplateService]
            }
            package "infrastructure" {
                [EmailSender]
                [SMSSender]
                [PushSender]
            }
        }
    }
    
    "Ordering" ..> "Identity & Access" : validates user
    "Ordering" ..> "Catalog" : validates product
    "Ordering" ..> "Payment" : processes payment
    "Ordering" ..> "Notification" : sends confirmation
    "Payment" ..> "Notification" : sends receipt
```