# Service Design Diagram Templates

## 1. Service Blueprint (Comprehensive)
```mermaid
flowchart TB
    subgraph Customer_Actions["Customer Actions"]
        CA1[Browse Website]
        CA2[Select Product]
        CA3[Add to Cart]
        CA4[Checkout]
        CA5[Pay]
        CA6[Receive Confirmation]
        CA7[Track Delivery]
        CA8[Receive Product]
        CA9[Use Product]
        CA10[Support Request]
    end
    
    subgraph Frontstage["Frontstage (Visible)"]
        FS1[Website/UI]
        FS2[Product Pages]
        FS3[Cart Page]
        FS4[Checkout Form]
        FS5[Payment Gateway]
        FS6[Order Confirmation]
        FS7[Tracking Page]
        FS8[Email/SMS]
        FS9[Help Center]
        FS10[Chat Support]
    end
    
    subgraph Backstage["Backstage (Invisible)"]
        BS1[Inventory Check]
        BS2[Price Calculation]
        BS3[Payment Processing]
        BS4[Order Creation]
        BS5[Inventory Reservation]
        BS6[Warehouse Pick]
        BS7[Packing]
        BS8[Shipping Label]
        BS9[Carrier Handoff]
        BS10[Delivery Tracking]
        BS11[Return Processing]
        BS12[Refund Processing]
    end
    
    subgraph Support_Processes["Support Processes"]
        SP1[Inventory Management]
        SP2[Supplier Management]
        SP3[Payment Gateway]
        SP4[Shipping Carriers]
        SP5[CRM System]
        SP6[Analytics]
        SP7[Fraud Detection]
    end
    
    CA1 --> FS1
    CA2 --> FS2
    CA3 --> FS3
    CA4 --> FS4
    CA5 --> FS5
    CA6 --> FS6
    CA7 --> FS7
    CA8 --> FS8
    CA9 --> FS1
    CA10 --> FS9
    CA10 --> FS10
    
    FS1 --> BS1
    FS2 --> BS1
    FS3 --> BS2
    FS4 --> BS2
    FS5 --> BS3
    FS5 --> BS7
    FS6 --> BS4
    FS7 --> BS10
    FS8 --> BS4
    FS9 --> BS11
    FS10 --> BS11
    
    BS3 --> SP3
    BS6 --> SP1
    BS7 --> SP1
    BS8 --> SP4
    BS9 --> SP4
    BS11 --> SP2
    BS12 --> SP3
    BS1 --> SP1
    BS2 --> SP6
    BS4 --> SP5
    BS4 --> SP7
    
    classDef customer fill:#e3f2fd,stroke:#1976d2
    classDef front fill:#f3e5f5,stroke:#7b1fa2
    classDef back fill:#fff3e0,stroke:#f57c00
    classDef support fill:#e8f5e9,stroke:#388e3c
    
    class CA1,CA2,CA3,CA4,CA5,CA6,CA7,CA8,CA9,CA10 customer
    class FS1,FS2,FS3,FS4,FS5,FS6,FS7,FS8,FS9,FS10 front
    class BS1,BS2,BS3,BS4,BS5,BS6,BS7,BS8,BS9,BS10,BS11,BS12 back
    class SP1,SP2,SP3,SP4,SP5,SP6,SP7 support
```

## 2. Customer Journey Map with Emotions
```mermaid
journey
    title E-commerce Customer Journey
    section Awareness
      See Ad: 3: Customer
      Visit Site: 4: Customer
      Browse: 4: Customer
    section Consideration
      Compare: 3: Customer
      Read Reviews: 4: Customer
      Add to Cart: 5: Customer
    section Purchase
      Checkout: 5: Customer
      Pay: 4: Customer
      Confirm: 5: Customer
    section Delivery
      Wait: 2: Customer
      Track: 3: Customer
      Receive: 5: Customer
    section Usage
      Unbox: 5: Customer
      Use: 4: Customer
      Issues?: 2: Customer
    section Loyalty
      Review: 3: Customer
      Reorder: 4: Customer
      Refer: 3: Customer
```

## 3. Service Ecosystem Map
```mermaid
graph TD
    subgraph Core["Core Service"]
        CS[E-commerce Platform]
    end
    
    subgraph Customers["Customers"]
        C1[B2C Shoppers]
        C2[B2B Buyers]
        C3[Guest Users]
    end
    
    subgraph Partners["Partners"]
        P1[Suppliers]
        P2[Marketplace Sellers]
        P3[Affiliates]
    end
    
    subgraph Providers["Service Providers"]
        PR1[Payment: Stripe/PayPal]
        PR2[Shipping: DHL/UPS]
        PR3[Email: SendGrid]
        PR4[SMS: Twilio]
        PR5[Auth: Auth0]
        PR6[Search: Algolia]
        PR7[CDN: CloudFront]
        PR8[Monitoring: Datadog]
    end
    
    subgraph Internal["Internal Systems"]
        I1[ERP]
        I2[PIM]
        I3[WMS]
        I4[CRM]
        I5[BI/Analytics]
    end
    
    C1 --> CS
    C2 --> CS
    C3 --> CS
    P1 --> CS
    P2 --> CS
    P3 --> CS
    CS --> PR1
    CS --> PR2
    CS --> PR3
    CS --> PR4
    CS --> PR5
    CS --> PR6
    CS --> PR7
    CS --> PR8
    CS --> I1
    CS --> I2
    CS --> I3
    CS --> I4
    CS --> I5
```

## 4. Touchpoint Analysis
```mermaid
quadrantChart
    title Touchpoint Impact vs Effort
    x-axis Low Effort --> High Effort
    y-axis Low Impact --> High Impact
    quadrant-1 Quick Wins
    quadrant-2 Strategic Investments
    quadrant-3 Low Priority
    quadrant-4 Major Projects
    "Homepage": [0.3, 0.8]
    "Product Page": [0.4, 0.9]
    "Cart": [0.5, 0.8]
    "Checkout": [0.8, 0.9]
    "Payment": [0.7, 0.9]
    "Order Confirmation": [0.3, 0.7]
    "Email Receipt": [0.2, 0.6]
    "Tracking": [0.4, 0.7]
    "Delivery": [0.6, 0.8]
    "Returns": [0.7, 0.6]
    "Support Chat": [0.5, 0.5]
    "Help Center": [0.3, 0.4]
    "Account Dashboard": [0.4, 0.5]
    "Wishlist": [0.3, 0.4]
    "Recommendations": [0.5, 0.6]
    "Loyalty Program": [0.6, 0.7]
```

## 5. Service Design: Frontstage/Backstage Detail
```mermaid
flowchart LR
    subgraph Customer["Customer"]
        C[Customer]
    end
    
    subgraph Physical["Physical Evidence"]
        PE1[Website]
        PE2[Email]
        PE3[Package]
        PE4[Receipt]
    end
    
    subgraph Frontstage["Frontstage Actions"]
        FA1[Browse]
        FA2[Select]
        FA3[Pay]
        FA4[Track]
        FA5[Unbox]
    end
    
    subgraph Backstage["Backstage Actions"]
        BA1[Inventory]
        BA2[Pricing]
        BA3[Payment]
        BA4[Fulfillment]
        BA5[Shipping]
    end
    
    subgraph Support["Support Processes"]
        SA1[Suppliers]
        SA2[Logistics]
        SA3[Payment GW]
        SA4[CRM]
    end
    
    C --> PE1
    C --> FA1
    FA1 --> FA2
    FA2 --> FA3
    FA3 --> FA4
    FA4 --> FA5
    
    FA1 --> BA1
    FA2 --> BA2
    FA3 --> BA3
    FA4 --> BA5
    FA5 --> BA4
    
    BA1 --> SA1
    BA3 --> SA3
    BA4 --> SA1
    BA5 --> SA2
    
    PE1 --> FA1
    PE2 --> FA3
    PE2 --> FA4
    PE3 --> FA5
    PE4 --> FA3
```

## 6. Moments of Truth
```mermaid
timeline
    title Moments of Truth in Customer Journey
    2024-01-15 : First Visit
               : MOT 1: Homepage load < 3s
               : MOT 2: Clear value prop
    2024-01-15 : Product Discovery
               : MOT 3: Search relevance
               : MOT 4: Product info quality
    2024-01-15 : Add to Cart
               : MOT 5: Smooth animation
               : MOT 6: Cart persistence
    2024-01-15 : Checkout
               : MOT 7: Guest option
               : MOT 8: Form validation
               : MOT 9: Payment options
    2024-01-16 : Post-Purchase
               : MOT 10: Instant confirmation
               : MOT 11: Clear next steps
    2024-01-18 : Delivery
               : MOT 12: Accurate tracking
               : MOT 13: Package condition
    2024-01-20 : Usage
               : MOT 14: Product meets expectations
               : MOT 15: Easy returns if needed
```