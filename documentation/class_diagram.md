# Class Diagram - Conceptual Model

This diagram illustrates the logical structure of the application's components and their relationships.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#f4f4f4', 'tertiaryColor': '#ffffff'}}}%%
classDiagram
    class User {
        +String ID
        +String email
        +String password
        +login()
        +logout()
    }

    class Student {
        +int rollNumber
        +int semester
        +attemptQuiz(quizID)
        +submitAnswer(questionID, answer)
    }

    class Faculty {
        +String designation
        +createQuiz()
        +addQuestion()
        +reviewResults()
    }

    class Admin {
        +manageDepartments()
        +importBulkData(file)
        +assignFaculty()
    }

    class Quiz {
        +int quizID
        +String title
        +DateTime startTime
        +int switchLimit
        +questions[]
        +start()
        +close()
    }

    class Question {
        +int questionID
        +String text
        +int type
        +validateAnswer(answer)
    }

    class AntiCheatMonitor {
        +int currentSwitches
        +int maxLimit
        +onTabSwitch()
        +terminateSession()
    }

    class DatabaseShim {
        +executeQuery(query)
        +toSQLite()
        +toMySQL()
    }

    User <|-- Student
    User <|-- Faculty
    User <|-- Admin
    
    Faculty "1" -- "many" Quiz : manages
    Quiz "1" -- "many" Question : contains
    Student "1" -- "many" Quiz : attempts
    
    Student "1" -- "1" AntiCheatMonitor : monitored by
    Quiz "1" -- "1" AntiCheatMonitor : configures
    
    Student ..> DatabaseShim : uses
    Faculty ..> DatabaseShim : uses
    Admin ..> DatabaseShim : uses
```

---
### Structural Overview:
- **Inheritance**: All user types inherit from a base `User` class for shared authentication logic.
- **Composition**: A `Quiz` is composed of multiple `Question` objects.
- **Dependency**: The system relies on the `DatabaseShim` for environment-agnostic data access.
- **Monitoring**: The `AntiCheatMonitor` is the bridge between the `Quiz` configuration and the active `Student` session.
