# Sequence Diagram - Quiz Attempt Flow

This diagram tracks the lifecycle of a single quiz attempt, highlighting the communication between the browser, server, and database.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#ffffff', 'primaryTextColor': '#000000', 'primaryBorderColor': '#000000', 'lineColor': '#000000', 'secondaryColor': '#f4f4f4', 'tertiaryColor': '#ffffff'}}}%%
sequenceDiagram
    autonumber
    actor Student
    participant Browser
    participant Server as Flask Server
    participant DB as Database
    participant AC as Anti-Cheat Monitor

    Student->>Browser: Login & Select Quiz
    Browser->>Server: GET /quiz_attempt
    Server->>DB: Fetch Quiz Details & Question IDs
    DB-->>Server: quiz_data, question_list
    Server-->>Browser: Render quiz.html
    
    loop During Quiz
        Student->>Browser: Select Answer
        Browser->>Server: POST /submit_question
        Server->>DB: Save/Update Response
        
        alt Tab Switched
            Browser->>AC: detect 'visibilitychange'
            AC->>Server: POST /browser_switch
            Server->>Server: Increment Switch Counter
            Server-->>Browser: Return updated counter
            alt Limit Exceeded
                Server->>Server: Set status to 'Finished'
                Server-->>Browser: Redirect to /quiz_submitted
            end
        end
    end

    Student->>Browser: Click Finish
    Browser->>Server: GET /finish_quiz
    Server->>DB: Calculate Final Score
    Server->>DB: Set quiz_attempted = 1
    Server-->>Browser: Show result/score summary
```

---
### Flow Significance:
1. **Initialization**: The server shuffles questions and initializes the session to prevent static pattern cheating.
2. **Real-time Sync**: Every question submission is saved immediately, ensuring no data loss if the student's connection drops.
3. **Integrity Enforcement**: The `Anti-Cheat Monitor` acts as an asynchronous watchdog, communicating directly with the session to enforce rules without interrupting the legitimate flow.
