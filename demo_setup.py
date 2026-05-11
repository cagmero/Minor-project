
import sqlite3
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

def ensure_column(cursor, table, column, type_def):
    try:
        cursor.execute(f"SELECT {column} FROM {table} LIMIT 1")
    except sqlite3.OperationalError:
        print(f"Adding '{column}' column to {table} table...")
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {type_def}")

def setup_demo_data():
    db_file = 'test_wise.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # 1. Ensure Tables and Columns exist
    ensure_column(cursor, 'admin', 'first_login', 'INTEGER DEFAULT 0')
    ensure_column(cursor, 'student', 'first_login', 'INTEGER DEFAULT 0')
    ensure_column(cursor, 'student', 'electives', 'TEXT')
    ensure_column(cursor, 'faculty', 'first_login', 'INTEGER DEFAULT 0')

    # 2. Update Credentials
    hashed_pwd = generate_password_hash('12345678')

    # Update Admin
    cursor.execute("""
        UPDATE admin 
        SET F_name = 'ANISH', L_name = 'JONATHAN', M_name = 'DEV', A_email = 'admin@test.com', 
            A_pass = ?, dept = 'Information Technology', first_login = 1
        WHERE A_id = 1
    """, (hashed_pwd,))

    # Update Students
    cursor.execute("DELETE FROM student")
    students = [
        ('S001', hashed_pwd, 'STUDENT', 'ONE', '', 101, 1, 'student1@test.com', 0, 0, '9876543210', 'parent1@test.com', '9876543211', 6, '', 'M', 'IT', None, 1),
        ('S002', hashed_pwd, 'STUDENT', 'TWO', '', 102, 1, 'student2@test.com', 0, 0, '9876543212', 'parent2@test.com', '9876543213', 6, '', 'F', 'IT', None, 1),
        ('S003', hashed_pwd, 'STUDENT', 'THREE', '', 103, 1, 'student3@test.com', 0, 0, '9876543214', 'parent3@test.com', '9876543215', 6, '', 'M', 'IT', None, 1),
        ('S004', hashed_pwd, 'STUDENT', 'FOUR', '', 104, 1, 'student4@test.com', 0, 0, '9876543216', 'parent4@test.com', '9876543217', 6, '', 'F', 'IT', None, 1),
        ('S005', hashed_pwd, 'STUDENT', 'FIVE', '', 105, 1, 'student5@test.com', 0, 0, '9876543218', 'parent5@test.com', '9876543219', 6, '', 'M', 'IT', None, 1),
    ]
    cursor.executemany("""
        INSERT INTO student (S_id, S_pass, L_name, F_name, M_name, roll, batch, S_email, KT, Type, S_num, P_email, P_num, current_sem, image, gender, dept, electives, first_login) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, students)

    # Update Faculty
    cursor.execute("DELETE FROM faculty")
    faculties = [
        ('F001', 'Prof.', 'TEACHER', 'ONE', '', 'faculty1@test.com', hashed_pwd, 'INFORMATION TECHNOLOGY', '9000000001', 'M', '', 1),
        ('F002', 'Prof.', 'TEACHER', 'TWO', '', 'faculty2@test.com', hashed_pwd, 'INFORMATION TECHNOLOGY', '9000000002', 'F', '', 1),
        ('F003', 'Prof.', 'TEACHER', 'THREE', '', 'faculty3@test.com', hashed_pwd, 'INFORMATION TECHNOLOGY', '9000000003', 'M', '', 1),
    ]
    cursor.executemany("""
        INSERT INTO faculty (F_id, Designation, L_name, F_name, M_name, F_email, F_password, dept, F_num, gender, img, first_login) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, faculties)

    # 3. Add Subjects for all semesters (Sem 1 to 8)
    cursor.execute("DELETE FROM subject")
    subjects = []
    dept_id = 'ST2202' # IT
    for sem in range(1, 9):
        sem_str = f"sem{sem}"
        for i in range(1, 4):
            sub_name = f"Subject {sem}.{i} for Demo"
            sub_id = f"IT{sem}0{i}"
            subjects.append((sub_id, sub_name, sub_id, sem_str, 1, 0, 1, 1, dept_id))

    cursor.executemany("""
        INSERT INTO subject (course_code, sub_name_long, sub_name_short, sem, sub_type, is_elective, elective_of, marks, dept_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, subjects)

    # 4. Create Demo Quizzes (MCQ, Mixed, Descriptive)
    cursor.execute("DELETE FROM quiz_det")
    cursor.execute("DELETE FROM questions")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='quiz_det'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='questions'")
    
    today = datetime.now().strftime('%Y-%m-%d')
    start_time = "00:00"
    end_time = "23:59"
    
    # Quiz 1: Pure MCQ (quiz_type='0')
    cursor.execute("""
        INSERT INTO quiz_det (q_title, q_dept, q_sem, q_sub, q_batch, q_date, quiz_type, q_timer, q_time_start, q_time_end, q_time_division, show_answer, fac_inserted, switch_limit, desc_time, quiz_status, quiz_started)
        VALUES ('Computer Networks MCQ', 'IT', '6', 'Subject 6.1 for Demo', 'All', ?, '0', 30, ?, ?, '-', 1, 'F001', 3, 0, 1, 1)
    """, (today, start_time, end_time))
    mcq_quiz_id = cursor.lastrowid

    # Quiz 2: Mixed (MCQ + Descriptive) (quiz_type='1')
    cursor.execute("""
        INSERT INTO quiz_det (q_title, q_dept, q_sem, q_sub, q_batch, q_date, quiz_type, q_timer, q_time_start, q_time_end, q_time_division, show_answer, fac_inserted, switch_limit, desc_time, quiz_status, quiz_started)
        VALUES ('Operating Systems Mixed Test', 'IT', '6', 'Subject 6.2 for Demo', 'All', ?, '1', 60, ?, ?, '-', 1, 'F001', 5, 30, 1, 1)
    """, (today, start_time, end_time))
    mixed_quiz_id = cursor.lastrowid

    # Quiz 3: Pure Descriptive (quiz_type='1')
    cursor.execute("""
        INSERT INTO quiz_det (q_title, q_dept, q_sem, q_sub, q_batch, q_date, quiz_type, q_timer, q_time_start, q_time_end, q_time_division, show_answer, fac_inserted, switch_limit, desc_time, quiz_status, quiz_started)
        VALUES ('Software Engineering Theory', 'IT', '6', 'Subject 6.3 for Demo', 'All', ?, '1', 45, ?, ?, '-', 1, 'F001', 3, 45, 1, 1)
    """, (today, start_time, end_time))
    desc_quiz_id = cursor.lastrowid

    # 5. Add Questions
    # Questions for MCQ Quiz
    mcq_questions = [
        (1, 'Which layer of OSI model is responsible for routing?', 0, 'Physical', 'Data Link', 'Network', 'Transport', 'option3', 'None', 2, mcq_quiz_id),
        (2, 'What does HTTP stand for?', 0, 'HyperText Transfer Protocol', 'HyperText Transmission Protocol', 'Hyperlink Text Transfer Protocol', 'None', 'option1', 'None', 2, mcq_quiz_id),
        (3, 'Which protocol is used for sending emails?', 0, 'HTTP', 'FTP', 'SMTP', 'POP3', 'option3', 'None', 2, mcq_quiz_id),
    ]
    cursor.executemany("""
        INSERT INTO questions (q_no, question, ans_type, opt1, opt2, opt3, opt4, correct_opt, q_time, points, quiz_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, mcq_questions)

    # Questions for Mixed Quiz
    mixed_questions = [
        (1, 'What is a Deadlock in OS?', 0, 'A state where processes wait for each other', 'A state of fast execution', 'A memory management technique', 'None', 'option1', 'None', 5, mixed_quiz_id),
        (2, 'Explain the process lifecycle in Operating Systems.', 2, '', '', '', '', '', 'None', 10, mixed_quiz_id),
        (3, 'Which scheduling algorithm uses time slices?', 0, 'FCFS', 'SJF', 'Round Robin', 'Priority', 'option3', 'None', 5, mixed_quiz_id),
    ]
    cursor.executemany("""
        INSERT INTO questions (q_no, question, ans_type, opt1, opt2, opt3, opt4, correct_opt, q_time, points, quiz_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, mixed_questions)

    # Questions for Descriptive Quiz
    desc_questions = [
        (1, 'Compare Waterfall and Agile models of Software Development.', 2, '', '', '', '', '', 'None', 20, desc_quiz_id),
        (2, 'Explain the importance of Testing in Software Engineering.', 2, '', '', '', '', '', 'None', 20, desc_quiz_id),
    ]
    cursor.executemany("""
        INSERT INTO questions (q_no, question, ans_type, opt1, opt2, opt3, opt4, correct_opt, q_time, points, quiz_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, desc_questions)

    conn.commit()
    conn.close()
    print("DEMO SETUP SUCCESSFUL - Mixed Tests Added!")

if __name__ == '__main__':
    setup_demo_data()
