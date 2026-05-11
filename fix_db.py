
import sqlite3
import os

def fix_missing_tables():
    db_file = 'test_wise.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create electives table if missing
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS `electives` (
      `u_key` INTEGER PRIMARY KEY AUTOINCREMENT,
      `sub_name` TEXT NOT NULL,
      `subject_id` TEXT NOT NULL,
      `sem` TEXT NOT NULL,
      `dept_id` TEXT NOT NULL,
      `course_code` TEXT DEFAULT NULL
    )""")

    conn.commit()
    conn.close()
    print("Fixed missing tables (electives).")

if __name__ == '__main__':
    fix_missing_tables()
