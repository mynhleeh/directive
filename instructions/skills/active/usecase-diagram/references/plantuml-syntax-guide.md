# PlantUML Use Case Diagram Syntax Guide

Cheatsheet and architectural styling patterns for production-grade UML 2.5 Use Case diagrams in PlantUML.

---

## 1. Professional Styling Template

Always prepend diagrams with standard skinparam styling to produce clear, publication-quality SVGs:

```plantuml
@startuml
!theme plain
skinparam roundCorner 10
skinparam defaultFontName "Inter", "Segoe UI", "Helvetica", sans-serif
skinparam defaultFontSize 13
skinparam packageFontSize 14
skinparam packageFontStyle bold
skinparam usecaseFontSize 12
skinparam arrowColor #4A5568
skinparam actorBorderColor #2D3748
skinparam usecaseBorderColor #2B6CB0
skinparam usecaseBackgroundColor #EBF8FF
skinparam rectangleBorderColor #718096
skinparam rectangleBackgroundColor #F7FAFC

left to right direction

' System Boundary and Elements here

@enduml
```

---

## 2. Declaration Syntax

### Actors
```plantuml
actor "Customer" as Customer
actor "Administrator" as Admin
actor "Payment Gateway" as PaymentGW <<System>>
actor "Email Service" as EmailService <<System>>
```

### System Boundary & Packages
```plantuml
rectangle "System: Food Delivery Platform" {
    package "Order Management" {
        usecase "Browse Menu" as UC_Browse
        usecase "Place Order" as UC_PlaceOrder
        usecase "Track Delivery Status" as UC_Track
    }

    package "Checkout & Payment" {
        usecase "Checkout Cart" as UC_Checkout
        usecase "Process Card Payment" as UC_PayCard
        usecase "Apply Coupon Code" as UC_Coupon
    }
}
```

---

## 3. Relationships & Arrow Conventions

| Relationship | Semantics | PlantUML Syntax | Direction Rule |
|---|---|---|---|
| **Association** | Actor communicates with Use Case | `Customer -- UC_Browse`<br>`UC_PayCard -- PaymentGW` | Solid undirected line (`--`) |
| **`<<include>>`** | Base usecase requires included usecase | `UC_Checkout .> UC_PayCard : <<include>>` | Base points to Included (`.>`) |
| **`<<extend>>`** | Extension conditionally adds to base | `UC_Coupon .> UC_Checkout : <<extend>>` | Extension points to Base (`.>`) |
| **Generalization** | Specific element specializes general | `UC_PayCard --|> UC_Checkout`<br>`VIPCustomer --|> Customer` | Child points to Parent (`--\|>`) |

---

## 4. Layout Stabilization Patterns

PlantUML uses Graphviz under the hood. Complex diagrams with many cross-links can produce tangled arrows. Apply these patterns:

1. **`left to right direction`**:
   Positions primary actors on the far left, system boundary in the center, and external systems/secondary actors on the far right.
2. **Hidden Links (`-[hidden]-`)**:
   Enforce visual ordering between actors or packages without drawing a line:
   ```plantuml
   Customer -[hidden]down- VIPCustomer
   ```
3. **Directional Arrow Hints**:
   Use directional qualifiers (`up`, `down`, `left`, `right`) when an arrow crosses uncomfortably:
   ```plantuml
   UC_Checkout .down.> UC_PayCard : <<include>>
   ```
