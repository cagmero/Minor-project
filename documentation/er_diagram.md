# ER Diagram - System Schema

This diagram represents the relational structure of the database tables and their interconnections.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#f4f4f4', 'tertiaryColor': '#ffffff'}}}%%
erDiagram
    STUDENT ||--o{ SCORE : "obtains"
    STUDENT ||--o{ QUIZ_RESPONSES : "submits"
    FACULTY ||--o{ QUIZ_DET : "creates"
    DEPARTMENT ||--o{ STUDENT : "enrolled_in"
    DEPARTMENT ||--o{ FACULTY : "belongs_to"
    DEPARTMENT ||--o{ SUBJECT : "offers"
    QUIZ_DET ||--o{ QUESTIONS : "contains"
    QUIZ_DET ||--o{ QUIZ_RESPONSES : "collects"
    QUIZ_DET ||--o{ SCORE : "generates"
    SUBJECT ||--o{ QUIZ_DET : "is_tested_in"

    STUDENT {
        string s_id PK
        string s_email
        string s_pass
        int current_sem
        string dept_id FK
    }

    FACULTY {
        int f_id PK
        string f_email
        string f_pass
        string dept_id FK
    }

    QUIZ_DET {
        int quiz_id PK
        string q_title
        datetime q_date
        int switch_limit
        int quiz_status
        int fac_id FK
    }

    QUESTIONS {
        int q_id PK
        int q_no
        string question
        int ans_type
        string correct_opt
        int quiz_id FK
    }

    QUIZ_RESPONSES {
        int response_id PK
        string selected_opt
        string user_id FK
        int quiz_id FK
    }

    SCORE {
        int score_id PK
        float user_score
        int total_points
        int quiz_id FK
        string user_id FK
    }

    DEPARTMENT {
        string dept_id PK
        string dept_name
    }

    SUBJECT {
        string course_code PK
        string sub_name
        string dept_id FK
    }
```

---
### Key Relationships:
- **Normalization**: The schema is normalized to ensure data integrity across departments and subjects.
- **Traceability**: Every score and response is tied to both a student and a specific quiz instance.
- **Configuration**: `QUIZ_DET` serves as the configuration hub for the anti-cheating engine.
