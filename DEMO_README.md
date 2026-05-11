
# Online Exam Portal - Workflow Guide

This guide explains how to use the portal for your presentation from three perspectives: **Admin**, **Faculty**, and **Student**.

---

## 1. Admin Workflow
**Goal**: Manage the core data of the institution.
- **Login**: Use `admin@test.com` / `12345678`.
- **Master Data**:
    - Navigate to **Master Data** on the sidebar.
    - View/Edit **Students**: Manage student records across different years.
    - View/Edit **Faculty**: Manage teacher accounts and assignments.
    - View/Edit **Subjects**: Manage courses offered per semester.
- **Bulk Import**: Use the "Upload Excel" feature to add hundreds of students or teachers at once.

## 2. Faculty Workflow
**Goal**: Create quizzes and monitor results.
- **Login**: Use `faculty1@test.com` (or 2, 3) / `12345678`.
- **Create Quiz**:
    - Go to **Quizzes** -> **Create New Quiz**.
    - Set Title, Date, Time, and Duration.
    - **Anti-Cheating Config**: Set the "Violation Limit" (e.g., 3 switches allowed).
- **Manage Questions**:
    - Add Multiple Choice, One-line, or Descriptive questions.
- **Dashboard**: Monitor active quizzes and see which students are currently attempting them.
- **Results**: View detailed scorecards and download them as Excel files.

## 3. Student Workflow
**Goal**: Attempt exams in a secure environment.
- **Login**: Use `student1@test.com` (to 5) / `12345678`.
- **Attempt Quiz**:
    - Active quizzes appear on the student dashboard.
    - Click **Start Quiz** to enter **Secure Mode**.
- **Secure Mode (Anti-Cheating)**:
    - The browser is forced into **Fullscreen**.
    - **Alerts**: If the student tries to switch tabs or exit fullscreen, an on-screen warning appears.
    - **Auto-Submit**: If the student exceeds the violation limit, the quiz is submitted automatically.
- **Submission**: View immediate scores (for MCQs) once the quiz is finished.

---

## Presentation Credentials
| Role | Email | Password |
| :--- | :--- | :--- |
| **Admin** | `admin@test.com` | `12345678` |
| **Faculty** | `faculty1@test.com` | `12345678` |
| **Student** | `student1@test.com` | `12345678` |

---

## How to Run
Run the following command to start the demo:
```bash
python3 run_demo.py
```
Open `http://127.0.0.1:5001` in your browser.
