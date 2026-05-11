# Use Case Diagram - Testwise

This diagram illustrates the primary interactions between the different users (Actors) and the system.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#f4f4f4', 'tertiaryColor': '#ffffff'}}}%%
graph LR
    subgraph Actors
        S[Student]
        F[Faculty]
        A[Admin]
        Sys[Anti-Cheat Engine]
    end

    subgraph "Testwise Online Exam Portal"
        UC1((Manage Users & Departments))
        UC2((Import/Export Data))
        UC3((Create & Configure Quiz))
        UC4((Manage Question Bank))
        UC5((Monitor Participation))
        UC6((Review & Grade Answers))
        UC7((View Available Quizzes))
        UC8((Attempt Quiz))
        UC9((Detect Tab Switches))
        UC10((Auto-Terminate Quiz))
        UC11((View Results))
    end

    A --- UC1
    A --- UC2
    
    F --- UC3
    F --- UC4
    F --- UC5
    F --- UC6
    
    S --- UC7
    S --- UC8
    S --- UC11
    
    UC8 -.->|includes| UC9
    UC9 -.->|extends| UC10
    Sys --- UC9
    Sys --- UC10

    %% Styling for Use Case look
    style UC1 fill:#f9f,stroke:#333,stroke-width:2px
    style UC2 fill:#f9f,stroke:#333,stroke-width:2px
    style UC3 fill:#f9f,stroke:#333,stroke-width:2px
    style UC4 fill:#f9f,stroke:#333,stroke-width:2px
    style UC5 fill:#f9f,stroke:#333,stroke-width:2px
    style UC6 fill:#f9f,stroke:#333,stroke-width:2px
    style UC7 fill:#f9f,stroke:#333,stroke-width:2px
    style UC8 fill:#f9f,stroke:#333,stroke-width:2px
    style UC9 fill:#f9f,stroke:#333,stroke-width:2px
    style UC10 fill:#f9f,stroke:#333,stroke-width:2px
    style UC11 fill:#f9f,stroke:#333,stroke-width:2px
```

---
### Use Case Descriptions:
- **Admin**: Focuses on the structural setup of the portal, ensuring departments and users are correctly provisioned.
- **Faculty**: Handles the academic core—creating assessments and evaluating performance.
- **Student**: The primary consumer of the quiz engine, subject to the monitoring constraints.
- **Anti-Cheat Engine**: An automated background actor that enforces integrity rules during active attempts.
