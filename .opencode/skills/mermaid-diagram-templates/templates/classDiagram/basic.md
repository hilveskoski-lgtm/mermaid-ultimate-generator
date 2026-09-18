# Class Diagram Templates

## 1. Basic Inheritance
```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +makeSound()
        +move()
    }
    class Dog {
        +String breed
        +bark()
        +fetch()
    }
    class Cat {
        +String color
        +meow()
        +climb()
    }
    Animal <|-- Dog
    Animal <|-- Cat
```

## 2. Composition & Aggregation
```mermaid
classDiagram
    class Engine {
        +int horsepower
        +start()
        +stop()
    }
    class Wheel {
        +int size
        +rotate()
    }
    class Car {
        +String model
        +drive()
        +brake()
    }
    class Garage {
        +List~Car~ cars
        +park(Car)
        +unpark(Car)
    }
    Car *-- Engine : composition
    Car *-- "4" Wheel : composition
    Garage o-- Car : aggregation
```

## 3. With Interfaces & Generics
```mermaid
classDiagram
    class Repository~T~ {
        <<interface>>
        +save(T)
        +findById(ID)
        +findAll()
        +delete(T)
    }
    class UserRepository {
        +save(User)
        +findByEmail(String)
        +findByRole(Role)
    }
    class User {
        +Long id
        +String email
        +String name
        +Role role
    }
    Repository <|.. UserRepository
    UserRepository ..> User
```

## 4. Design Patterns (Strategy)
```mermaid
classDiagram
    class PaymentStrategy {
        <<interface>>
        +pay(amount: double)
    }
    class CreditCardPayment {
        +String cardNumber
        +pay(amount)
    }
    class PayPalPayment {
        +String email
        +pay(amount)
    }
    class CryptoPayment {
        +String walletAddress
        +pay(amount)
    }
    class ShoppingCart {
        +PaymentStrategy strategy
        +setStrategy(PaymentStrategy)
        +checkout(amount)
    }
    PaymentStrategy <|.. CreditCardPayment
    PaymentStrategy <|.. PayPalPayment
    PaymentStrategy <|.. CryptoPayment
    ShoppingCart --> PaymentStrategy
```

## 5. With Visibility & Annotations
```mermaid
classDiagram
    class OrderService {
        -OrderRepository repository
        -PaymentService paymentService
        +createOrder(OrderDTO)
        +cancelOrder(Long)
        #validateOrder(Order)
        ~calculateTotal(Order)
    }
    class OrderRepository {
        <<interface>>
        +save(Order)
        +findById(Long)
    }
    class JpaOrderRepository {
        -EntityManager em
        +save(Order)
        +findById(Long)
    }
    OrderService --> OrderRepository
    OrderRepository <|.. JpaOrderRepository
```

## 6. Domain Model (E-commerce)
```mermaid
classDiagram
    class Customer {
        +Long id
        +String email
        +String name
        +Address address
        +placeOrder()
    }
    class Address {
        +String street
        +String city
        +String postalCode
        +String country
    }
    class Order {
        +Long id
        +LocalDateTime createdAt
        +OrderStatus status
        +BigDecimal total
        +addItem(OrderItem)
        +calculateTotal()
    }
    class OrderItem {
        +Long id
        +int quantity
        +BigDecimal unitPrice
        +Product product
    }
    class Product {
        +Long id
        +String name
        +String description
        +BigDecimal price
        +int stock
    }
    class OrderStatus {
        <<enumeration>>
        PENDING
        CONFIRMED
        SHIPPED
        DELIVERED
        CANCELLED
    }
    Customer "1" --> "*" Order
    Order "1" --> "*" OrderItem
    OrderItem "*" --> "1" Product
    Order --> OrderStatus
    Customer --> Address
```