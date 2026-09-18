# ER Diagram Templates

## 1. Basic E-commerce (Chen Notation)
```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
    PRODUCT ||--o{ LINE_ITEM : "is in"
    CATEGORY ||--o{ PRODUCT : categorizes
    SUPPLIER }|--o{ PRODUCT : supplies
    
    CUSTOMER {
        string id PK
        string email UK
        string name
        string phone
        date created_at
    }
    ORDER {
        int id PK
        string customer_id FK
        date order_date
        string status
        decimal total
    }
    LINE_ITEM {
        int id PK
        int order_id FK
        int product_id FK
        int quantity
        decimal unit_price
    }
    PRODUCT {
        int id PK
        string name
        string description
        decimal price
        int stock
        int category_id FK
        int supplier_id FK
    }
    CATEGORY {
        int id PK
        string name
        string description
    }
    SUPPLIER {
        int id PK
        string name
        string contact_email
        string phone
    }
```

## 2. Crow's Foot Notation
```mermaid
erDiagram
    USER ||--o{ POST : creates
    USER ||--o{ COMMENT : writes
    POST ||--o{ COMMENT : has
    POST }|--o{ TAG : tagged
    TAG }|--o{ POST : "tags"
    
    USER {
        uuid id PK
        string username UK
        string email UK
        string password_hash
        datetime created_at
    }
    POST {
        uuid id PK
        uuid user_id FK
        string title
        text content
        datetime published_at
        boolean is_published
    }
    COMMENT {
        uuid id PK
        uuid post_id FK
        uuid user_id FK
        text content
        datetime created_at
    }
    TAG {
        uuid id PK
        string name UK
        string slug UK
    }
```

## 3. Weak Entity (Identifying Relationship)
```mermaid
erDiagram
    BUILDING ||--|{ ROOM : contains
    ROOM ||--|{ BED : has
    ROOM {
        string building_id FK
        string room_number PK
        string type
        int capacity
    }
    BED {
        string building_id FK
        string room_number FK
        int bed_number PK
        string type
    }
    BUILDING {
        string id PK
        string name
        string address
    }
```

## 4. Self-Referencing (Hierarchy)
```mermaid
erDiagram
    EMPLOYEE ||--o{ EMPLOYEE : manages
    EMPLOYEE {
        int id PK
        string name
        string email
        int manager_id FK
        string department
        decimal salary
    }
    DEPARTMENT ||--o{ EMPLOYEE : employs
    DEPARTMENT {
        int id PK
        string name
        int manager_id FK
        string location
    }
```

## 5. Many-to-Many with Attributes
```mermaid
erDiagram
    STUDENT }|--o{ ENROLLMENT : enrolls
    COURSE ||--o{ ENROLLMENT : offered
    
    STUDENT {
        int id PK
        string student_number UK
        string first_name
        string last_name
        date enrollment_date
    }
    COURSE {
        int id PK
        string code UK
        string name
        int credits
        string semester
    }
    ENROLLMENT {
        int student_id FK
        int course_id FK
        date enrolled_at
        string grade
        string status
    }
```

## 6. Complete System (SaaS)
```mermaid
erDiagram
    TENANT ||--o{ USER : owns
    TENANT ||--o{ SUBSCRIPTION : has
    TENANT ||--o{ PROJECT : contains
    USER ||--o{ PROJECT_MEMBER : member_of
    PROJECT ||--o{ PROJECT_MEMBER : has
    PROJECT ||--o{ TASK : contains
    TASK ||--o{ TASK_ASSIGNEE : assigned
    USER ||--o{ TASK_ASSIGNEE : assigned_to
    TASK ||--o{ COMMENT : has
    USER ||--o{ COMMENT : writes
    
    TENANT {
        uuid id PK
        string name
        string slug UK
        string plan
        datetime trial_ends_at
        datetime created_at
    }
    USER {
        uuid id PK
        uuid tenant_id FK
        string email UK
        string name
        string avatar_url
        datetime last_login
    }
    SUBSCRIPTION {
        uuid id PK
        uuid tenant_id FK
        string stripe_id
        string status
        decimal amount
        datetime current_period_end
    }
    PROJECT {
        uuid id PK
        uuid tenant_id FK
        string name
        string key
        string description
        datetime created_at
    }
    PROJECT_MEMBER {
        uuid project_id FK
        uuid user_id FK
        string role
        datetime joined_at
    }
    TASK {
        uuid id PK
        uuid project_id FK
        string title
        text description
        string status
        int priority
        uuid reporter_id FK
        datetime due_date
        datetime created_at
    }
    TASK_ASSIGNEE {
        uuid task_id FK
        uuid user_id FK
        datetime assigned_at
    }
    COMMENT {
        uuid id PK
        uuid task_id FK
        uuid author_id FK
        text content
        datetime created_at
    }
```