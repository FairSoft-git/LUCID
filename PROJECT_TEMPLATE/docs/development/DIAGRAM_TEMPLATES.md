# Diagram Templates

> **Project:** [Project Name]  
> **Version:** 1.0  
> **Last Updated:** 2025-11-27  
> **Status:** Active

---

## Purpose

This document provides copy-paste templates for creating standard UML diagrams using **Mermaid.js**. Use these in your Feature READMEs and architectural documentation.

---

## 1. Class Diagram (Structure)

**Use for:** Showing class attributes, methods, and relationships.

```mermaid
classDiagram
    %% Relationships
    Deck "1" *-- "many" Card : contains
    Deck o-- User : belongs_to
    Card <|-- PokemonCard : inherits
    Card <|-- TrainerCard : inherits

    %% Class Definitions
    class Deck {
        +UUID id
        +String name
        +List~Card~ cards
        +add_card(card)
        +validate() bool
    }

    class Card {
        <<Abstract>>
        +String id
        +String name
        +play()
    }

    class PokemonCard {
        +int hp
        +String type
        +attack()
    }
```

**Source Code:**
````markdown
```mermaid
classDiagram
    %% Relationships
    Deck "1" *-- "many" Card : contains
    Deck o-- User : belongs_to
    Card <|-- PokemonCard : inherits
    Card <|-- TrainerCard : inherits

    %% Class Definitions
    class Deck {
        +UUID id
        +String name
        +List~Card~ cards
        +add_card(card)
        +validate() bool
    }

    class Card {
        <<Abstract>>
        +String id
        +String name
        +play()
    }

    class PokemonCard {
        +int hp
        +String type
        +attack()
    }
```
````

---

## 2. Sequence Diagram (Interactions)

**Use for:** Showing how objects interact over time to complete a task.

```mermaid
sequenceDiagram
    autonumber
    participant User
    participant API as API Gateway
    participant Svc as CardService
    participant DB as Database

    User->>API: GET /cards/{id}
    activate API
    API->>Svc: get_card(id)
    activate Svc
    
    Svc->>DB: query(id)
    alt Card Found
        DB-->>Svc: Card Data
        Svc-->>API: CardDTO
        API-->>User: 200 OK
    else Card Not Found
        DB-->>Svc: null
        Svc-->>API: Error
        API-->>User: 404 Not Found
    end
    
    deactivate Svc
    deactivate API
```

**Source Code:**
````markdown
```mermaid
sequenceDiagram
    autonumber
    participant User
    participant API as API Gateway
    participant Svc as CardService
    participant DB as Database

    User->>API: GET /cards/{id}
    activate API
    API->>Svc: get_card(id)
    activate Svc
    
    Svc->>DB: query(id)
    alt Card Found
        DB-->>Svc: Card Data
        Svc-->>API: CardDTO
        API-->>User: 200 OK
    else Card Not Found
        DB-->>Svc: null
        Svc-->>API: Error
        API-->>User: 404 Not Found
    end
    
    deactivate Svc
    deactivate API
```
````

---

## 3. Flowchart (Logic/Process)

**Use for:** Decision trees, algorithms, and workflows.

```mermaid
flowchart TD
    Start([Start]) --> Input{Valid Input?}
    
    Input -->|Yes| Process[Process Data]
    Input -->|No| Log[Log Error]
    
    Process --> DB[(Database)]
    
    DB --> Success{Save OK?}
    Success -->|Yes| Notify[Notify User]
    Success -->|No| Retry[Retry Operation]
    
    Retry --> DB
    
    Notify --> End([End])
    Log --> End
```

**Source Code:**
````markdown
```mermaid
flowchart TD
    Start([Start]) --> Input{Valid Input?}
    
    Input -->|Yes| Process[Process Data]
    Input -->|No| Log[Log Error]
    
    Process --> DB[(Database)]
    
    DB --> Success{Save OK?}
    Success -->|Yes| Notify[Notify User]
    Success -->|No| Retry[Retry Operation]
    
    Retry --> DB
    
    Notify --> End([End])
    Log --> End
```
````

---

## 4. State Diagram (Lifecycle)

**Use for:** Object lifecycles (e.g., Order status, Game state).

```mermaid
stateDiagram-v2
    [*] --> Draft
    
    Draft --> Review : submit()
    Review --> Approved : approve()
    Review --> Rejected : reject()
    
    Rejected --> Draft : edit()
    
    Approved --> Published : publish()
    Published --> Archived : archive()
    
    Archived --> [*]
```

**Source Code:**
````markdown
```mermaid
stateDiagram-v2
    [*] --> Draft
    
    Draft --> Review : submit()
    Review --> Approved : approve()
    Review --> Rejected : reject()
    
    Rejected --> Draft : edit()
    
    Approved --> Published : publish()
    Published --> Archived : archive()
    
    Archived --> [*]
```
````

---

## 5. Entity Relationship Diagram (Data)

**Use for:** Database schemas and data relationships.

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ ORDER_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : included_in
    
    USER {
        string id PK
        string email
        string password_hash
    }
    
    ORDER {
        int id PK
        string user_id FK
        date created_at
        string status
    }
```

**Source Code:**
````markdown
```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ ORDER_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : included_in
    
    USER {
        string id PK
        string email
        string password_hash
    }
    
    ORDER {
        int id PK
        string user_id FK
        date created_at
        string status
    }
```
````
