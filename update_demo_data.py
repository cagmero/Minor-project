
import sqlite3
import os
from werkzeug.security import generate_password_hash

def update_data():
    db_file = 'test_wise.db'
    if not os.path.exists(db_file):
        print(f"Error: {db_file} not found. Run migrate_to_sqlite.py first.")
        return

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    hashed_pwd = generate_password_hash('12345678')

    # 1. Update Admin (Anish Jonathan)
    cursor.execute("""
        UPDATE admin 
        SET F_name = 'ANISH', L_name = 'JONATHAN', M_name = 'DEV', A_email = 'admin@test.com', 
            A_pass = ?, dept = 'Information Technology', first_login = 1
        WHERE A_id = 1
    """, (hashed_pwd,))

    # 2. Update scores (Anish Jonathan)
    cursor.execute("""
        UPDATE score 
        SET username = 'ANISH JONATHAN' 
        WHERE username LIKE '%BHAVYA MISTRY%'
    """, [])

    # 3. Clear and Add Students
    cursor.execute("DELETE FROM student")
    # S_id, S_pass, L_name, F_name, M_name, roll, batch, S_email, KT, Type, S_num, P_email, P_num, current_sem, image, gender, dept, electives, first_login
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

    # 4. Clear and Add Faculty
    cursor.execute("DELETE FROM faculty")
    # F_id, Designation, L_name, F_name, M_name, F_email, F_password, dept, F_num, gender, img, first_login
    faculties = [
        ('F001', 'Prof.', 'TEACHER', 'ONE', '', 'faculty1@test.com', hashed_pwd, 'INFORMATION TECHNOLOGY', '9000000001', 'M', '', 1),
        ('F002', 'Prof.', 'TEACHER', 'TWO', '', 'faculty2@test.com', hashed_pwd, 'INFORMATION TECHNOLOGY', '9000000002', 'F', '', 1),
        ('F003', 'Prof.', 'TEACHER', 'THREE', '', 'faculty3@test.com', hashed_pwd, 'INFORMATION TECHNOLOGY', '9000000003', 'M', '', 1),
    ]
    cursor.executemany("""
        INSERT INTO faculty (F_id, Designation, L_name, F_name, M_name, F_email, F_password, dept, F_num, gender, img, first_login) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, faculties)

    conn.commit()
    conn.close()
    print("Database updated with Anish Jonathan and demo credentials.")

if __name__ == '__main__':
    update_data()
