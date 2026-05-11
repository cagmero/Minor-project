
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
    # Admin
    ensure_column(cursor, 'admin', 'first_login', 'INTEGER DEFAULT 0')
    ensure_column(cursor, 'admin', 'otp', 'TEXT')
    ensure_column(cursor, 'admin', 'expiry_at', 'TEXT')
    ensure_column(cursor, 'admin', 'otp_used', 'INTEGER DEFAULT 0')

    # Student
    ensure_column(cursor, 'student', 'first_login', 'INTEGER DEFAULT 0')
    ensure_column(cursor, 'student', 'electives', 'TEXT')
    ensure_column(cursor, 'student', 'otp', 'TEXT')
    ensure_column(cursor, 'student', 'expiry_at', 'TEXT')
    ensure_column(cursor, 'student', 'otp_used', 'INTEGER DEFAULT 0')

    # Faculty
    ensure_column(cursor, 'faculty', 'first_login', 'INTEGER DEFAULT 0')
    ensure_column(cursor, 'faculty', 'otp', 'TEXT')
    ensure_column(cursor, 'faculty', 'expiry_at', 'TEXT')
    ensure_column(cursor, 'faculty', 'otp_used', 'INTEGER DEFAULT 0')

    # Subject Table - Ensure correct columns
    try:
        cursor.execute("SELECT course_code FROM subject LIMIT 1")
    except sqlite3.OperationalError:
        print("Re-creating subject table...")
        cursor.execute("DROP TABLE IF EXISTS subject")
        cursor.execute("""
        CREATE TABLE `subject` (
          `course_code` varchar(20) PRIMARY KEY,
          `sub_name_long` text NOT NULL,
          `sub_name_short` varchar(30) NOT NULL,
          `sem` varchar(5) NOT NULL,
          `sub_type` int NOT NULL,
          `is_elective` int NOT NULL DEFAULT '0',
          `elective_of` int NOT NULL DEFAULT '1',
          `marks` int NOT NULL,
          `dept_id` varchar(20) NOT NULL
        )""")

    # Electives Category
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS `electives_category` (
      `category_id` INTEGER PRIMARY KEY AUTOINCREMENT,
      `cat_name` TEXT NOT NULL,
      `sem` TEXT NOT NULL,
      `dept_id` TEXT NOT NULL
    )""")

    # 2. Update Credentials and Profile Info
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

    # 4. Create two Demo Quizzes
    cursor.execute("DELETE FROM quiz_det")
    cursor.execute("DELETE FROM questions")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='quiz_det'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='questions'")
    
    today = datetime.now().strftime('%Y-%m-%d')
    start_time = "00:00"
    end_time = "23:59"
    
    # Quiz 1: MCQ (quiz_type='0')
    cursor.execute("""
        INSERT INTO quiz_det (q_title, q_dept, q_sem, q_sub, q_batch, q_date, quiz_type, q_timer, q_time_start, q_time_end, q_time_division, show_answer, fac_inserted, switch_limit, desc_time, quiz_status, quiz_started)
        VALUES ('Python Basics Demo Quiz', 'IT', '6', 'Subject 6.1 for Demo', 'All', ?, '0', 30, ?, ?, '-', 1, 'F001', 3, 0, 1, 1)
    """, (today, start_time, end_time))
    mcq_quiz_id = cursor.lastrowid

    # Quiz 2: Mixed/Descriptive (quiz_type='1')
    cursor.execute("""
        INSERT INTO quiz_det (q_title, q_dept, q_sem, q_sub, q_batch, q_date, quiz_type, q_timer, q_time_start, q_time_end, q_time_division, show_answer, fac_inserted, switch_limit, desc_time, quiz_status, quiz_started)
        VALUES ('Advanced DBMS Demo Exam', 'IT', '6', 'Subject 6.2 for Demo', 'All', ?, '1', 60, ?, ?, '-', 1, 'F001', 5, 30, 1, 1)
    """, (today, start_time, end_time))
    desc_quiz_id = cursor.lastrowid

    # 5. Add Questions
    mcq_questions = [
        (1, 'Which data type is used to store multiple items in a single variable in Python?', 0, 'List', 'Integer', 'String', 'Boolean', 'option1', 'None', 2, mcq_quiz_id),
        (2, 'What is the correct syntax to output "Hello World" in Python?', 0, 'p("Hello World")', 'print("Hello World")', 'echo("Hello World")', 'console.log("Hello World")', 'option2', 'None', 2, mcq_quiz_id),
    ]
    cursor.executemany("""
        INSERT INTO questions (q_no, question, ans_type, opt1, opt2, opt3, opt4, correct_opt, q_time, points, quiz_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, mcq_questions)

    desc_questions = [
        (1, 'Explain the 3-tier architecture of DBMS with a neat diagram.', 2, '', '', '', '', '', 'None', 10, desc_quiz_id),
        (2, 'What are ACID properties in a database transaction?', 2, '', '', '', '', '', 'None', 10, desc_quiz_id),
    ]
    cursor.executemany("""
        INSERT INTO questions (q_no, question, ans_type, opt1, opt2, opt3, opt4, correct_opt, q_time, points, quiz_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, desc_questions)

    conn.commit()
    conn.close()
    print("DEMO SETUP SUCCESSFUL!")

if __name__ == '__main__':
    setup_demo_data()
