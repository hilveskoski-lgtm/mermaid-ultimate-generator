# Use Case Diagram Templates

## 1. E-commerce System
```mermaid
useCaseDiagram
    actor Customer
    actor Admin
    actor PaymentGateway
    actor ShippingProvider
    
    package "Shopping" {
        usecase "Browse Products" as UC1
        usecase "Search Products" as UC2
        usecase "View Product Details" as UC3
        usecase "Add to Cart" as UC4
        usecase "Update Cart" as UC5
        usecase "View Cart" as UC6
    }
    
    package "Checkout" {
        usecase "Guest Checkout" as UC7
        usecase "Login/Register" as UC8
        usecase "Enter Shipping" as UC9
        usecase "Select Payment" as UC10
        usecase "Place Order" as UC11
    }
    
    package "Account" {
        usecase "View Orders" as UC12
        usecase "Track Shipment" as UC13
        usecase "Return Item" as UC14
        usecase "Manage Profile" as UC15
    }
    
    package "Admin" {
        usecase "Manage Products" as UC16
        usecase "Manage Orders" as UC17
        usecase "Manage Users" as UC18
        usecase "View Analytics" as UC19
    }
    
    Customer --> UC1
    Customer --> UC2
    Customer --> UC3
    Customer --> UC4
    Customer --> UC5
    Customer --> UC6
    Customer --> UC7
    Customer --> UC8
    Customer --> UC9
    Customer --> UC10
    Customer --> UC11
    Customer --> UC12
    Customer --> UC13
    Customer --> UC14
    Customer --> UC15
    
    Admin --> UC16
    Admin --> UC17
    Admin --> UC18
    Admin --> UC19
    
    UC11 --> PaymentGateway : "Process Payment"
    UC17 --> ShippingProvider : "Create Shipment"
```

## 2. Banking System
```mermaid
useCaseDiagram
    actor Customer
    actor Teller
    actor Admin
    actor ExternalBank
    
    package "Accounts" {
        usecase "Open Account" as UC1
        usecase "Close Account" as UC2
        usecase "View Balance" as UC3
        usecase "View Statements" as UC4
    }
    
    package "Transactions" {
        usecase "Deposit" as UC5
        usecase "Withdraw" as UC6
        usecase "Transfer Internal" as UC7
        usecase "Transfer External" as UC8
        usecase "Pay Bills" as UC9
    }
    
    package "Loans" {
        usecase "Apply Loan" as UC10
        usecase "View Loan Status" as UC11
        usecase "Make Payment" as UC12
    }
    
    package "Admin" {
        usecase "Manage Users" as UC13
        usecase "Approve Loans" as UC14
        usecase "View Reports" as UC15
        usecase "Configure Rates" as UC16
    }
    
    Customer --> UC1
    Customer --> UC2
    Customer --> UC3
    Customer --> UC4
    Customer --> UC5
    Customer --> UC6
    Customer --> UC7
    Customer --> UC8
    Customer --> UC9
    Customer --> UC10
    Customer --> UC11
    Customer --> UC12
    
    Teller --> UC1
    Teller --> UC5
    Teller --> UC6
    Teller --> UC7
    Teller --> UC8
    
    Admin --> UC13
    Admin --> UC14
    Admin --> UC15
    Admin --> UC16
    
    UC8 --> ExternalBank : "SWIFT/ACH"
    UC10 ..> UC14 : "<<include>>"
```

## 3. Healthcare System
```mermaid
useCaseDiagram
    actor Patient
    actor Doctor
    actor Nurse
    actor Receptionist
    actor Insurance
    actor Lab
    
    package "Appointments" {
        usecase "Schedule Appointment" as UC1
        usecase "Reschedule" as UC2
        usecase "Cancel" as UC3
        usecase "Check-in" as UC4
    }
    
    package "Medical Records" {
        usecase "View Records" as UC5
        usecase "Update Records" as UC6
        usecase "Add Notes" as UC7
        usecase "Prescribe" as UC8
    }
    
    package "Billing" {
        usecase "Verify Insurance" as UC9
        usecase "Submit Claim" as UC10
        usecase "Process Payment" as UC11
    }
    
    package "Lab" {
        usecase "Order Tests" as UC12
        usecase "View Results" as UC13
    }
    
    Patient --> UC1
    Patient --> UC2
    Patient --> UC3
    Patient --> UC5
    
    Doctor --> UC1
    Doctor --> UC2
    Doctor --> UC5
    Doctor --> UC6
    Doctor --> UC7
    Doctor --> UC8
    Doctor --> UC12
    Doctor --> UC13
    
    Nurse --> UC4
    Nurse --> UC6
    Nurse --> UC7
    
    Receptionist --> UC1
    Receptionist --> UC2
    Receptionist --> UC3
    Receptionist --> UC4
    Receptionist --> UC9
    Receptionist --> UC11
    
    Insurance --> UC9
    Insurance --> UC10
    
    Lab --> UC12
    Lab --> UC13
```

## 4. With Extend/Include Relationships
```mermaid
useCaseDiagram
    actor User
    actor Admin
    
    usecase "Login" as UC1
    usecase "Register" as UC2
    usecase "Reset Password" as UC3
    usecase "Two-Factor Auth" as UC4
    usecase "Social Login" as UC5
    
    usecase "View Dashboard" as UC6
    usecase "Export Data" as UC7
    usecase "Generate Report" as UC8
    usecase "Schedule Report" as UC9
    
    usecase "Manage Users" as UC10
    usecase "Audit Logs" as UC11
    usecase "System Config" as UC12
    
    User --> UC1
    User --> UC2
    User --> UC3
    User --> UC6
    User --> UC7
    User --> UC8
    User --> UC9
    
    Admin --> UC1
    Admin --> UC10
    Admin --> UC11
    Admin --> UC12
    
    UC1 ..> UC4 : "<<extend>>"
    UC1 ..> UC5 : "<<extend>>"
    UC3 ..> UC4 : "<<include>>"
    UC8 ..> UC9 : "<<extend>>"
    UC10 ..> UC11 : "<<include>>"
```

## 5. Smart Home System
```mermaid
useCaseDiagram
    actor Homeowner
    actor Guest
    actor MobileApp
    actor VoiceAssistant
    actor SecurityCompany
    actor EnergyProvider
    
    package "Lighting" {
        usecase "Turn On/Off Lights" as UC1
        usecase "Dim Lights" as UC2
        usecase "Set Scenes" as UC3
        usecase "Schedule Lights" as UC4
    }
    
    package "Climate" {
        usecase "Adjust Temperature" as UC5
        usecase "Set Schedule" as UC6
        usecase "View Energy Usage" as UC7
    }
    
    package "Security" {
        usecase "Arm/Disarm" as UC8
        usecase "View Cameras" as UC9
        usecase "Receive Alerts" as UC10
        usecase "Grant Access" as UC11
    }
    
    package "Automation" {
        usecase "Create Routines" as UC12
        usecase "Voice Control" as UC13
        usecase "Geofencing" as UC14
    }
    
    Homeowner --> UC1
    Homeowner --> UC2
    Homeowner --> UC3
    Homeowner --> UC4
    Homeowner --> UC5
    Homeowner --> UC6
    Homeowner --> UC7
    Homeowner --> UC8
    Homeowner --> UC9
    Homeowner --> UC10
    Homeowner --> UC11
    Homeowner --> UC12
    Homeowner --> UC13
    Homeowner --> UC14
    
    Guest --> UC11
    Guest --> UC1
    
    MobileApp --> UC1
    MobileApp --> UC5
    MobileApp --> UC8
    MobileApp --> UC9
    MobileApp --> UC12
    
    VoiceAssistant --> UC1
    VoiceAssistant --> UC2
    VoiceAssistant --> UC5
    VoiceAssistant --> UC8
    VoiceAssistant --> UC13
    
    SecurityCompany --> UC10
    EnergyProvider --> UC7
```