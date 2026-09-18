# material_logistics_er_pure

```mermaid
erDiagram
    WORKSITE ||--o{ WORK_PACKAGE : contains
    WORK_PACKAGE ||--o{ TASK : contains
    TASK }|--o{ MATERIAL_REQUIREMENT : requires
    MATERIAL_REQUIREMENT }|--|| MATERIAL_CATALOG : specifies
    MATERIAL_CATALOG ||--o{ SUPPLIER_CATALOG : supplied_by
    SUPPLIER_CATALOG }|--|| SUPPLIER : provided_by
    
    MATERIAL_REQUEST ||--o{ MATERIAL_REQUEST_LINE : contains
    MATERIAL_REQUEST }o--|| WORKSITE : for
    MATERIAL_REQUEST }o--|| TASK : for
    MATERIAL_REQUEST }o--|| SUPPLIER : from
    
    DELIVERY ||--o{ DELIVERY_LINE : contains
    DELIVERY }o--|| MATERIAL_REQUEST : fulfills
    DELIVERY }o--|| WORKSITE : to
    DELIVERY }o--|| SUPPLIER : from
    
    STOCK_LEVEL }|--|| WORKSITE : at
    STOCK_LEVEL }|--|| MATERIAL_CATALOG : of
    
    WORKSITE {
        string id PK
        string name
        string address
        string site_manager
        date start_date
        date end_date
    }
    
    WORK_PACKAGE {
        string id PK
        string worksite_id FK
        string name
        string trade
        date planned_start
        date planned_end
    }
    
    TASK {
        string id PK
        string work_package_id FK
        string worksite_id FK
        string description
        string trade
        string location
        string status
        decimal estimated_hours
        decimal actual_hours
        date planned_start
        date planned_end
    }
    
    MATERIAL_CATALOG {
        string id PK
        string code UK
        string name
        string unit
        string category
        decimal unit_weight
        boolean hazardous
    }
    
    MATERIAL_REQUIREMENT {
        string task_id FK
        string material_id FK
        decimal quantity
        date needed_by
        string priority
    }
    
    SUPPLIER {
        string id PK
        string name
        string contact_person
        string email
        string phone
        int lead_time_days
        string payment_terms
    }
    
    SUPPLIER_CATALOG {
        string supplier_id FK
        string material_id FK
        decimal unit_price
        string supplier_sku
        int min_order_qty
    }
    
    MATERIAL_REQUEST {
        string id PK
        string worksite_id FK
        string task_id FK
        string supplier_id FK
        string requested_by
        date requested_at
        date needed_by
        string status
        string priority
    }
    
    MATERIAL_REQUEST_LINE {
        string request_id FK
        string material_id FK
        decimal quantity
        string unit
        string notes
    }
    
    DELIVERY {
        string id PK
        string request_id FK
        string worksite_id FK
        string supplier_id FK
        string delivery_note
        date delivered_at
        string received_by
        string status
    }
    
    DELIVERY_LINE {
        string delivery_id FK
        string material_id FK
        decimal quantity_ordered
        decimal quantity_delivered
        decimal quantity_damaged
        string unit
        string batch_number
    }
    
    STOCK_LEVEL {
        string worksite_id FK
        string material_id FK
        decimal quantity_on_hand
        decimal quantity_reserved
        decimal quantity_available
        date last_counted
        string location_on_site
    }
```